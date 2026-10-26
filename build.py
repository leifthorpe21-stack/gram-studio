#!/usr/bin/env python3
"""Build the release version of Gram Studio.

Reads gram-studio.html, inlines the zip library (verifying its hash), adds a
strict Content Security Policy whose script hashes match the inline scripts,
and writes docs/index.html (the folder GitHub Pages serves). Run: python3 build.py [source] [output]
"""
import base64, hashlib, pathlib, re, sys
SRC = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'gram-studio.html')
OUT = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else 'docs/index.html')
VENDOR = pathlib.Path(__file__).with_name('vendor') / 'jszip.min.js'
JSZIP_SHA384 = '+mbV2IY1Zk/X1p/nWllGySJSUN8uMs+gUAN10Or95UBH0fpj6GfKgPmgC5EXieXG'

html = SRC.read_text(encoding='utf-8')
lib = VENDOR.read_bytes()
digest = base64.b64encode(hashlib.sha384(lib).digest()).decode()
if digest != JSZIP_SHA384:
    sys.exit(f'vendor/jszip.min.js does not match the expected hash ({digest})')

tag = re.search(r'<script src="https://cdnjs\.cloudflare\.com/ajax/libs/jszip/[^"]+"[^>]*></script>', html)
if not tag:
    sys.exit('zip library script tag not found')
html = html[:tag.start()] + '<script>' + lib.decode('utf-8') + '</script>' + html[tag.end():]

hashes = []
for m in re.finditer(r'<script>(.*?)</script>', html, re.S):
    hashes.append("'sha256-" + base64.b64encode(hashlib.sha256(m.group(1).encode('utf-8')).digest()).decode() + "'")
csp = ("default-src 'none'; script-src " + ' '.join(hashes) + "; style-src 'unsafe-inline'; img-src blob: data:; "
       "connect-src 'none'; base-uri 'none'; form-action 'none'; object-src 'none'")
html = html.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n<meta http-equiv="Content-Security-Policy" content="' + csp + '">', 1)
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(html, encoding='utf-8')
print(f'wrote {OUT} ({OUT.stat().st_size//1024} KB), {len(hashes)} inline script hash(es)')
