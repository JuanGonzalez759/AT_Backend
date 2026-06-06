#!/usr/bin/env python3
import io
from pathlib import Path

files = [Path('fixtures.json'), Path('AT_Backend') / 'fixtures.json']
any_changed = False
for p in files:
    if p.exists():
        with io.open(p, 'r', encoding='utf-8-sig') as src:
            data = src.read()
        with io.open(p, 'w', encoding='utf-8') as dst:
            dst.write(data)
        print('Normalized', p)
        any_changed = True
    else:
        print('Not found', p)
if not any_changed:
    print('No files changed')
