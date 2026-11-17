# -*- coding: utf-8 -*-
"""mobilcv.net icerik guvenlik politikasi (CSP) – 17.11.
  python3 .github/csp.py ekle     # CSP'si olmayan her HTML'e <meta charset> satirindan sonra ekler (uretici/bot sonrasi)
  python3 .github/csp.py kontrol  # CSP eksik ya da farkli sayfa varsa cikis 1 (CI)
Izinli dis kaynaklar: Google Analytics (yalniz cerez onayi sonrasi yuklenir) ve geri bildirim formu (formspree, yalniz bizim form).
Yeni bir dis servis eklenecekse once buraya yazilir; CI farki yakalar."""
import pathlib, re, sys
CSP = ("default-src 'self'; script-src 'self' 'unsafe-inline' https://*.googletagmanager.com; style-src 'self' 'unsafe-inline'; "
       "img-src 'self' data: https://*.google-analytics.com https://*.googletagmanager.com; font-src 'self' data:; "
       "connect-src 'self' https://*.google-analytics.com https://*.analytics.google.com https://*.googletagmanager.com; "
       "form-action 'self' https://formspree.io/f/movkoozp; base-uri 'self'; object-src 'none'; frame-src 'none'")
ETIKET = f'<meta http-equiv="Content-Security-Policy" content="{CSP}">'
KOK = pathlib.Path(__file__).resolve().parent.parent
ATLA = {'.git', 'node_modules'}
def sayfalar():
    # arama motoru dogrulama dosyalari (google*.html, yandex_*.html) dokunulmaz
    return [p for p in KOK.rglob('*.html') if not (set(p.relative_to(KOK).parts) & ATLA)
            and not re.match(r'(google[0-9a-f]+|yandex_[0-9a-f]+)\.html$', p.name)]
def main(kip):
    sorun, eklenen = [], 0
    for p in sayfalar():
        t = p.read_text(encoding='utf-8')
        m = re.findall(r'<meta http-equiv="Content-Security-Policy" content="([^"]*)"', t)
        if kip == 'ekle' and not m:
            yeni, n = re.subn(r'(<meta charset="[^"]+">)', r'\1\n    ' + ETIKET.replace('\\', '\\\\'), t, count=1)
            if n: p.write_text(yeni, encoding='utf-8'); eklenen += 1; continue
            sorun.append(f'{p.relative_to(KOK)}: <meta charset> yok, CSP eklenemedi')
        elif m != [CSP]:
            sorun.append(f'{p.relative_to(KOK)}: CSP ' + ('yok' if not m else 'farkli'))
    if kip == 'ekle': print(f'{eklenen} sayfaya CSP eklendi')
    for s in sorun: print('::error::' + s)
    print(f'{len(sayfalar())} sayfa, {len(sorun)} sorun'); return 1 if sorun else 0
sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else 'kontrol'))
