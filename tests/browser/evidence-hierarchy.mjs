/* 実生成siteをChromiumで操作し、GWT画像と検証結果を保存する。 */
import { chromium, expect } from '@playwright/test';
import { spawnSync } from 'node:child_process';
import { createServer } from 'node:http';
import { createHash } from 'node:crypto';
import { readFile, mkdir, writeFile, mkdtemp } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import assert from 'node:assert/strict';

const destination = path.resolve(process.env.EVIDENCE_E2E_OUTPUT || await mkdtemp(path.join(tmpdir(), 'dev-standard-evidence-e2e-')));
const generated = spawnSync(process.env.PYTHON || 'python', ['tests/build_evidence_hierarchy_fixture.py', destination], { encoding: 'utf8', env: { ...process.env, PYTHONPATH: process.cwd() } });
assert.equal(generated.status, 0, generated.stderr + generated.stdout);
const site = path.join(destination, 'site');
const server = createServer(async (req, res) => {
  try {
    const filename = path.resolve(site, '.' + decodeURIComponent(new URL(req.url, 'http://local').pathname));
    if (!filename.startsWith(site + path.sep)) throw Error('outside site');
    const content = await readFile(filename);
    res.setHeader('Content-Type', ({ '.html': 'text/html; charset=utf-8', '.svg': 'image/svg+xml', '.js': 'text/javascript', '.css': 'text/css', '.csv': 'text/csv; charset=utf-8' })[path.extname(filename)] || 'application/octet-stream');
    res.end(content);
  } catch { res.writeHead(404); res.end(); }
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
let browser;
const cases = [];
try {
  browser = await chromium.launch({ headless: true, ...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE ? { executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE } : {}) });
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 }, acceptDownloads: true });
  const errors = [];
  page.on('pageerror', error => errors.push(String(error)));
  const base = `http://127.0.0.1:${server.address().port}`;
  await mkdir(path.join(destination, 'images'), { recursive: true });
  async function step(id, phase, text) {
    const image = `images/${id}-${phase}.png`;
    await page.screenshot({ path: path.join(destination, image), fullPage: true });
    return { phase, text, image };
  }
  async function scenario(id, name, action) {
    await page.goto(`${base}/design.html`);
    const steps = [await step(id, 'Given', 'adapter出力形式の6帳票とCRUDを持つ品質portalを開く')];
    await action(steps, (phase, text) => step(id, phase, text));
    cases.push({ id, name, group: '品質Pages', status: 'passed', steps });
  }
  await scenario('hierarchy', 'groupからAPIと帳票へ移動', async (steps, snap) => {
    const group = page.locator('aside details').filter({ has: page.locator(':scope > summary', { hasText: /^items$/ }) }).first();
    await group.locator(':scope > summary').click();
    assert.equal(await group.getAttribute('open'), null);
    await group.locator(':scope > summary').click();
    await page.locator('aside a', { hasText: /^interface$/ }).click();
    steps.push(await snap('When', 'items → getItem → interfaceを選択'));
    await expect(page.locator('#location')).toHaveText('items / getItem / interface');
    assert.equal(await page.locator('aside a[aria-current="location"]').textContent(), 'interface');
    steps.push(await snap('Then', '親階層と現在位置が選択帳票に一致する'));
  });
  await scenario('search', '検索後も親階層を保持', async (steps, snap) => {
    await page.locator('#search').fill('unit-test');
    steps.push(await snap('When', 'unit-testを検索'));
    assert.equal(await page.locator('article:visible').count(), 1);
    assert.equal(await page.locator('aside summary:visible').allTextContents().then(x => x.join('/')), 'items/getItem');
    await page.locator('aside a', { hasText: /^unit-test$/ }).click();
    await expect(page.locator('#location')).toHaveText('items / getItem / unit-test');
    steps.push(await snap('Then', '検索結果とitems/getItemの祖先が残る'));
    await page.locator('#search').fill('');
    assert.equal(await page.locator('article:visible').count(), 8);
    await page.locator('#search').fill('該当しない検索語');
    assert.equal(await page.locator('article:visible').count(), 0);
    assert.equal(await page.locator('aside summary:visible').count(), 0);
    await page.locator('#search').fill('');
    assert.equal(await page.locator('article:visible').count(), 8);
  });
  await scenario('links', '帳票間リンクを移動', async (steps, snap) => {
    await page.locator('#case-0').getByRole('link', { name: '設計HTMLを開く' }).click();
    await page.getByRole('link', { name: 'interface', exact: true }).first().click();
    steps.push(await snap('When', '詳細設計からinterface帳票へ移動'));
    assert.equal(await page.getByRole('heading', { name: 'Headers', exact: true }).count(), 1);
    await page.getByRole('link', { name: 'query', exact: true }).first().click();
    assert.equal(await page.getByRole('heading', { name: 'SQL種別', exact: true }).count(), 1);
    steps.push(await snap('Then', '別帳票の必須章へ辿れる'));
  });
  await scenario('exceptions', '例外応答と自然言語の検証単位を読める', async (steps, snap) => {
    await page.locator('aside a', { hasText: /^messages$/ }).click();
    const selected = await page.locator('aside a', { hasText: /^messages$/ }).getAttribute('href');
    await page.locator(selected).getByRole('link', { name: '設計HTMLを開く' }).click();
    steps.push(await snap('When', '運用ログ帳票を開く'));
    assert.ok(await page.getByText('モデル処理に失敗しました。', { exact: false }).count() > 0);
    assert.ok(await page.getByText('依存先の状態を確認し再試行する。', { exact: false }).count() > 0);
    await page.getByRole('link', { name: 'unit-test', exact: true }).first().click();
    assert.ok(await page.getByText('商品Aが登録されている。', { exact: false }).count() > 0);
    assert.ok(await page.getByText('前提（Given）', { exact: true }).count() > 0);
    steps.push(await snap('Then', '安全な応答・復旧手順・日本語の前提操作期待結果を読める'));
  });
  await scenario('crud', 'CRUD図とCSV取得', async (steps, snap) => {
    await page.locator('#search').fill('CRUD対応');
    const image = page.getByAltText('APIと保存先のCRUD対応図');
    await image.waitFor({ state: 'visible' });
    assert.equal(await image.evaluate(img => img.complete && img.naturalWidth > 0), true);
    const downloadPromise = page.waitForEvent('download');
    await page.getByRole('link', { name: 'CSV取得' }).click();
    const download = await downloadPromise;
    steps.push(await snap('When', 'CRUD図を確認しCSVを取得'));
    const csv = await readFile(await download.path(), 'utf8');
    assert.equal(csv, 'API,inventory:items\ngetItem,R\n');
    assert.equal(await page.locator('article:visible').count(), 1);
    steps.push(await snap('Then', 'fixtureモデルの参照操作Rと同じCSVを取得できる'));
  });
  await scenario('mobile', '狭い画面でも階層と現在位置を操作できる', async (steps, snap) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.locator('#search').fill('unit-test');
    const link = page.locator('aside a', { hasText: /^unit-test$/ });
    await link.focus();
    await page.keyboard.press('Enter');
    steps.push(await snap('When', '390px幅で検索しキーボードから帳票を選択'));
    await expect(page.locator('#location')).toHaveText('items / getItem / unit-test');
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth), true);
    steps.push(await snap('Then', '階層と現在位置が読め、横方向へはみ出さない'));
  });
  assert.deepEqual(errors, []);
  const inputs = ['.agents/skills/inspect-quality-gates/scripts/evidence.py',
    '.agents/skills/inspect-quality-gates/assets/evidence.js',
    '.agents/skills/inspect-quality-gates/assets/evidence.css',
    'tests/build_evidence_hierarchy_fixture.py', 'tests/test_evidence_portal.py',
    'tests/browser/evidence-hierarchy.mjs'];
  const sourceSha256 = Object.fromEntries(await Promise.all(inputs.map(async name => [name, createHash('sha256').update(await readFile(name)).digest('hex')])));
  await writeFile(path.join(destination, 'e2e.json'), JSON.stringify({ schemaVersion: 1,
    revision: spawnSync('git', ['rev-parse', 'HEAD'], { encoding: 'utf8' }).stdout.trim(),
    dirty: Boolean(spawnSync('git', ['status', '--porcelain'], { encoding: 'utf8' }).stdout.trim()),
    scope: 'local generated fixture and current worktree source, not deployed commit', sourceSha256, cases }, null, 2) + '\n');
  console.log(`Evidence hierarchy E2E: ${cases.length} passed; GWT: ${destination}`);
} finally {
  await browser?.close();
  await new Promise(resolve => server.close(resolve));
}
