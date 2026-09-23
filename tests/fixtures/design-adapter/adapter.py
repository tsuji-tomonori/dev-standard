"""テスト専用adapter。対象repositoryの生成・checkを別processで実行する。"""
import json
import os
import sys
from pathlib import Path

mode = Path('mode.txt').read_text().strip()
outputs = json.loads(Path('templates.json').read_text())
source = Path('src/model.txt').read_text().strip()
expected = {path: text.replace('{{SOURCE}}', source) for path, text in outputs.items()}
checking = '--check' in sys.argv
print('fixture adapter: ' + ('check' if checking else 'generate'), flush=True)
if checking and mode == 'rewrite-check':
    Path('docs/generated/index.md').write_text('rewritten during check')
    sys.exit(0)
if checking:
    sys.exit(any(not Path(path).is_file() or Path(path).read_text() != text for path, text in expected.items()))
if mode == 'second-nondeterministic':
    target = Path('docs/generated/index.md')
    if target.stat().st_mtime == 2:
        expected['docs/generated/index.md'] += '\nsecond generation differs\n'
for path, text in expected.items():
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(text)
if mode == 'second-nondeterministic':
    os.utime('docs/generated/index.md', (2, 2))
if mode == 'unowned-write':
    Path('unowned.txt').write_text('outside declared ownership')
if mode == 'delete-output':
    Path('docs/generated/index.md').unlink()
if mode == 'directory-replacement':
    Path('docs/generated/index.md').unlink()
    Path('docs/generated/index.md').mkdir()
if mode == 'unowned-directory':
    Path('unowned-empty').mkdir()
if mode == 'unowned-symlink-replacement':
    Path('unowned-empty').rmdir()
    Path('unowned-empty').symlink_to('src', target_is_directory=True)
if mode == 'undeclared-output-directory':
    Path('docs/generated/unused').mkdir()
