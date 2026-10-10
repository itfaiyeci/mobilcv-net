# -*- coding: utf-8 -*-
"""Blog yazilarindan icerigi olmayan genel 'Yararlanilan Kaynaklar' ifadelerini ve doldurulmamis yer tutuculari kaldirir.
Gercek link iceren kaynak bolumlerine dokunmaz. Kullanim: python3 kaynak_temizle.py <repo>"""
import re, sys
from pathlib import Path
KW = r'(?:Yararlanılan Kaynaklar|Sources|المصادر|Источники|Quellen|Fonti|Fuentes|Fontes|来源)'
P = r'<p>(?:(?!</p>)(?!<a )[\s\S])*?</p>'
PATS = [
    rf'\s*<(aside|section|footer)>\s*(?:<section>\s*)?<h[234]>{KW}:?</h[234]>\s*{P}\s*(?:</section>\s*)?</\1>',
    rf'\s*<(aside|section|footer)>\s*<p>(?:<strong>)?{KW}:?(?:</strong>)?(?:(?!</p>)(?!<a )[\s\S])*?</p>\s*</\1>',
    rf'\s*<h[234]>{KW}:?</h[234]>\s*{P}',
    rf'\s*<p>(?:<strong>)?{KW}:?(?:</strong>)?(?:(?!</p>)(?!<a )[\s\S])*?</p>',
    rf'\s*<!--\s*{KW}[^>]*-->',
    rf'\s*\*\*{KW}:\*\*[^<]*',
]
PLACEHOLDER = re.compile(r'\s*<h2>İlham Verici Girişimcilik Hikayeleri</h2>[\s\S]*?(?=<h2>)')

def clean(s):
    a, b = s.split('<article', 1) if '<article' in s else (s, '')
    if not b: return s, 0
    body, rest = b.split('</article>', 1) if '</article>' in b else (b, '')
    n = 0
    for pat in PATS:
        body, k = re.subn(pat, '', body); n += k
    if '***' in body:
        body, k = PLACEHOLDER.subn('\n', body); n += k
    return a + '<article' + body + ('</article>' + rest if rest else ''), n

if __name__ == '__main__':
    root = Path(sys.argv[1]); tot = 0
    for p in sorted(root.rglob('*.html')):
        if any(x in str(p) for x in ('cv-rules', 'ulkelere', 'cv-guide', 'cv-rehberi', '.git/')): continue
        s = p.read_text(encoding='utf-8'); t, n = clean(s)
        if n: p.write_text(t, encoding='utf-8'); print(n, p.relative_to(root)); tot += n
    print('toplam', tot)
