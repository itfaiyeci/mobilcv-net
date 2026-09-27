# ============================================================
# MobilCV - Mevcut Makalelere "CV Örnekleri" Linkini Toplu Ekleme
# ============================================================
# Bu script, mobilcv.net reponuzdaki TÜM .html dosyalarını tarar.
# Eski (CV Örnekleri linki OLMAYAN) header/footer yapısını bulursa
# otomatik olarak günceller. Zaten güncel olan dosyalara (index.html,
# cv-ornekleri.html, meslek şablonları) DOKUNMAZ - güvenlidir,
# birden fazla kez çalıştırılabilir.
#
# KULLANIM:
# 1. Bu dosyayı "fix_headers.py" adıyla mobilcv.net reponuzun
#    KÖK dizinine kaydedin (index.html ile AYNI klasöre).
# 2. Terminal/komut satırında o klasöre gidin.
# 3. Şunu çalıştırın:  python fix_headers.py
# 4. Script hangi dosyaları güncellediğini ekrana yazacaktır.
# 5. Sonuçları git ile commit edip GitHub'a push edin.
# ============================================================

import os
import glob

OLD_NAV = '''<ul class="nav-links">
                <li><a href="https://mobilcv.com">Ana Site</a></li>
                <li><a href="https://mobilcv.net">Blog</a></li>
                <li><a href="cv-rehberi.html">CV Rehberi</a></li>
                <li><a href="iletisim.html">İletişim</a></li>
                <li><a href="https://mobilcv.net" class="nav-cta">🚀 Keşfet</a></li>
            </ul>'''

NEW_NAV = '''<ul class="nav-links">
                <li><a href="https://mobilcv.com">Ana Site</a></li>
                <li><a href="https://mobilcv.net">Blog</a></li>
                <li><a href="cv-ornekleri.html">CV Örnekleri</a></li>
                <li><a href="cv-rehberi.html">CV Rehberi</a></li>
                <li><a href="iletisim.html">İletişim</a></li>
                <li><a href="https://mobilcv.net" class="nav-cta">🚀 Keşfet</a></li>
            </ul>'''

OLD_FOOTER = '''<div class="footer-links">
            <a href="https://mobilcv.com">Ana Site</a>
            <a href="https://mobilcv.net">Blog</a>
            <a href="cv-rehberi.html">CV Rehberi</a>
            <a href="iletisim.html">İletişim</a>
        </div>'''

NEW_FOOTER = '''<div class="footer-links">
            <a href="https://mobilcv.com">Ana Site</a>
            <a href="https://mobilcv.net">Blog</a>
            <a href="cv-ornekleri.html">CV Örnekleri</a>
            <a href="cv-rehberi.html">CV Rehberi</a>
            <a href="iletisim.html">İletişim</a>
        </div>'''


def main():
    html_files = glob.glob("*.html")
    if not html_files:
        print("⚠️  Bu klasörde hiç .html dosyası bulunamadı.")
        print("    Script'i mobilcv.net reponuzun KÖK dizininde çalıştırdığınızdan emin olun.")
        return

    updated = []
    already_ok = []
    no_match = []

    for filename in html_files:
        with open(filename, encoding='utf-8') as f:
            content = f.read()

        original_content = content
        changed = False

        if OLD_NAV in content:
            content = content.replace(OLD_NAV, NEW_NAV)
            changed = True

        if OLD_FOOTER in content:
            content = content.replace(OLD_FOOTER, NEW_FOOTER)
            changed = True

        if changed:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            updated.append(filename)
        elif "cv-ornekleri.html" in original_content:
            already_ok.append(filename)
        else:
            no_match.append(filename)

    print(f"\n✅ Güncellenen dosyalar ({len(updated)}):")
    for f in updated:
        print(f"   - {f}")

    if already_ok:
        print(f"\n☑️  Zaten güncel olan dosyalar ({len(already_ok)}):")
        for f in already_ok:
            print(f"   - {f}")

    if no_match:
        print(f"\n⚠️  Beklenen yapı bulunamayan dosyalar ({len(no_match)}) - bunlara elle bakmanız gerekebilir:")
        for f in no_match:
            print(f"   - {f}")

    print(f"\n🎉 Tamamlandı! {len(updated)} dosya güncellendi.")


if __name__ == "__main__":
    main()
