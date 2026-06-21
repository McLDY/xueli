#!/usr/bin/env python3
"""Build: copies index.html → _build/ (no changes, for test.py input)"""
import os, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
DEPLOY = os.path.join(ROOT, '_build')

def build():
    os.makedirs(DEPLOY, exist_ok=True)
    src = os.path.join(ROOT, 'index.html')
    dst = os.path.join(DEPLOY, 'index.html')
    shutil.copy2(src, dst)
    size = os.path.getsize(dst)
    print(f'Copied: {dst} ({size:,} bytes)')
    return True

if __name__ == '__main__':
    build()
