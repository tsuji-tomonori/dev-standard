#!/usr/bin/env python3
"""固定版比較台帳の全source blobを再照合する。ネットワーク取得・対象の変更は行わない。"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / 'docs/audits/lazunex-slotkeeper/inventory.json'


def check_snapshot(root: Path, entry: dict) -> list[str]:
    expected = {item['path']: item['blob_sha'] for item in entry['files']}
    errors = []
    if len(expected) != entry['file_count']:
        errors.append('inventory count/duplicate mismatch')
    digest = hashlib.sha256(''.join(f'{p}\t{sha}\n' for p, sha in sorted(expected.items())).encode()).hexdigest()
    if digest != entry['tree_sha256']:
        errors.append('inventory tree digest mismatch')
    if (root / '.git').exists():
        tracked = subprocess.check_output(['git', '-C', str(root), 'ls-files', '-z']).decode().split('\0')
        actual = {p for p in tracked if p}
    else:
        actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    if actual != set(expected):
        errors.append('missing/excess source files: ' + repr(sorted(actual ^ set(expected))))
    for value, expected_sha in expected.items():
        path = root / value
        if (Path(value).is_absolute() or '..' in Path(value).parts or not path.resolve().is_relative_to(root.resolve())
                or path.is_symlink() or not path.is_file()):
            errors.append(f'invalid/missing source: {value}')
            continue
        body = path.read_bytes()
        actual_sha = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
        if actual_sha != expected_sha:
            errors.append(f'blob mismatch: {value}')
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lazunex', type=Path, required=True)
    parser.add_argument('--slotkeeper', type=Path, required=True)
    args = parser.parse_args()
    inventory = json.loads(INVENTORY.read_text())
    roots = {'lazunex': args.lazunex, 'SlotKeeper': args.slotkeeper}
    results = []
    for entry in inventory['repositories']:
        name = entry['repository'].rsplit('/', 1)[1]
        errors = check_snapshot(roots[name], entry)
        results.append({'repository': name, 'revision': entry['revision'], 'file_count': entry['file_count'],
                        'status': 'fail' if errors else 'pass', 'errors': errors})
    print(json.dumps(results, ensure_ascii=False, indent=2))
    raise SystemExit(any(item['errors'] for item in results))


if __name__ == '__main__':
    main()
