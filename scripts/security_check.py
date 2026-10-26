#!/usr/bin/env python3
"""Static security check for the built page (docs/index.html).

Fails if the release could talk to the network, run dynamic code, load
anything external, or lost its Content Security Policy. Run after build.py.
"""
import re, sys, pathlib
path = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html')
html = path.read_text(encoding='utf-8')
problems = []
def forbid(pattern, why, flags=0):
    hits = re.findall(pattern, html, flags)
    if hits:
        problems.append(f'{why}: {len(hits)} hit(s), e.g. {hits[0][:60]!r}')

forbid(r'<script[^>]+src=', 'external script tag')
forbid(r'<link[^>]+href="https?://', 'external stylesheet or resource link')
forbid(r'\b(?:fetch|XMLHttpRequest|WebSocket|EventSource)\s*\(', 'network API call')
forbid(r'navigator\.sendBeacon', 'beacon call')
forbid(r'\beval\s*\(', 'eval')
forbid(r'document\.write\s*\(', 'document.write')
forbid(r'\bimport\s*\(', 'dynamic import')
forbid(r'\bon(?:click|load|error|mouseover)\s*=\s*"', 'inline event handler attribute')
forbid(r'location\.(?:hash|search)', 'URL-driven state')
forbid(r'https?://(?!stuartk\.com|raw\.github\.com|github\.com/(?:Stuk|nodeca)|stuk\.github\.io|nodeca\.github\.io|opensource\.org|www\.w3\.org)[a-z0-9.-]+', 'unexpected external URL (allowed: license and help URLs inside the JSZip library)', re.I)
csp = re.search(r'http-equiv="Content-Security-Policy" content="([^"]*)"', html)
if not csp:
    problems.append('Content Security Policy meta tag missing')
else:
    c = csp.group(1)
    for need in ["default-src 'none'", "object-src 'none'", "base-uri 'none'", "form-action 'none'"]:
        if need not in c: problems.append(f'CSP lacks {need}')
    if 'unsafe-eval' in c or 'unsafe-inline' in c.split('script-src')[1].split(';')[0]:
        problems.append('CSP allows unsafe script execution')
    for m in re.finditer(r'<script>(.*?)</script>', html, re.S):
        import base64, hashlib
        h = "'sha256-" + base64.b64encode(hashlib.sha256(m.group(1).encode('utf-8')).digest()).decode() + "'"
        if h not in c: problems.append('an inline script is not covered by the CSP hash list')
if 'if(self!==top)' not in html: problems.append('frame guard missing')
if re.search(r'innerHTML\s*=\s*`[^`]*\$\{(?!esc\()[^}]*\.(?:name|text)\b', html):
    problems.append('innerHTML interpolates a name/text field without esc()')
if problems:
    print('SECURITY CHECK FAILED'); [print(' -', p) for p in problems]; sys.exit(1)
print(f'security check passed for {path} ({len(html)//1024} KB)')
