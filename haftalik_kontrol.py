# -*- coding: utf-8 -*-
"""MobilCV haftalik kontrol: iki sitenin dosyalarini tarar, Markdown rapor yazar. Hicbir dosyayi degistirmez.
Kullanim: python3 haftalik_kontrol.py <cv-olusturucu klasoru> <mobilcv-net klasoru> [rapor.md]
Kontroller: yasak/yaniltici ifadeler, canonical, kirik ic baglantilar, site haritasi, robots.txt,
cerez onayi + Analytics, www'suz mobilcv.com baglantilari, son 8 gunde degisen sayfalar."""
import re, sys, subprocess
from pathlib import Path
from html import unescape

COM, NET = Path(sys.argv[1]), Path(sys.argv[2])
OUT = Path(sys.argv[3]) if len(sys.argv) > 3 else None
GA = "G-4W6V8KX8D8"
SITES = {"mobilcv.com": (COM, "https://www.mobilcv.com"), "mobilcv.net": (NET, "https://mobilcv.net")}
SKIP_DIRS = ("MobilCV.AIEngine/", ".git/", ".github/", "node_modules/")

# Yaniltici / yasak ifadeler (icerik-dogruluk-kurallari.md). Desen, aciklama
YASAK = [
    (r"\b\d+\s*dakikada\b|birkaç dakikada", "süre vaadi (TR)"),
    (r"\bin (?:a few |just )?minutes\b|\bin \d+ minutes?\b", "süre vaadi (EN)"),
    (r"in wenigen Minuten|en quelques minutes|en pocos minutos|in pochi minuti|em poucos minutos|за несколько минут|几分钟|数分で", "süre vaadi (diğer dil)"),
    (r"veri(?:ler(?:iniz)?)? toplanmaz|bilgileriniz kaydedilmez|hiçbir veri (?:toplanmaz|saklanmaz)", "yanlış gizlilik ifadesi (TR)"),
    (r"\bno data (?:is )?(?:collected|stored)\b|we (?:do not|don't) collect any data", "yanlış gizlilik ifadesi (EN)"),
    (r"araştırmalar(?:a göre| gösteriyor)|uzmanlara göre|studies show|according to (?:experts|research)", "dayanaksız otorite ifadesi"),
    (r"%\s?\d{2,3}[^<]{0,40}(?:işveren|recruiter|aday|şirket)|\d{2,3}\s?%[^<]{0,40}(?:of (?:employers|recruiters|candidates))", "doğrulanmamış istatistik şüphesi"),
]

def html_files(root):
    for f in sorted(root.rglob("*.html")):
        rel = f.relative_to(root).as_posix()
        if any(rel.startswith(d) or ("/" + d) in rel for d in SKIP_DIRS) or re.fullmatch(r"google[0-9a-f]+\.html", f.name):
            continue
        yield f, rel

def visible_text(s):
    s = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>", " ", s)
    return unescape(re.sub(r"<[^>]+>", " ", s))

def is_redirect(s):
    return 'http-equiv="refresh"' in s

def target_exists(root, path):
    path = path.split("#")[0].split("?")[0]
    if not path or path == "/":
        return (root / "index.html").exists()
    p = root / path.lstrip("/")
    return p.is_file() or (p / "index.html").is_file() or (p.with_suffix(".html")).is_file()

rows = {k: [] for k in ("yasak", "canonical", "link", "sitemap", "robots", "consent", "apex")}
counts = {}
for site, (root, base) in SITES.items():
    n = 0
    for f, rel in html_files(root):
        n += 1
        s = f.read_text(encoding="utf-8", errors="ignore")
        red = is_redirect(s)
        noindex = re.search(r'name="robots" content="[^"]*noindex', s) is not None
        if not red and not noindex:
            txt = visible_text(s)
            for pat, why in YASAK:
                m = re.search(pat, txt, re.I)
                if m:
                    rows["yasak"].append(f"{site}/{rel}: {why} → “{m.group(0).strip()}”")
        if f.name != "404.html" and 'rel="canonical"' not in s:
            rows["canonical"].append(f"{site}/{rel}: canonical yok")
        m = re.search(r'rel="canonical" href="([^"]+)"', s)
        if m and not m.group(1).startswith(base + "/"):
            rows["canonical"].append(f"{site}/{rel}: canonical başka alan adına gidiyor → {m.group(1)}")
        # ic baglantilar
        for href in re.findall(r'href="([^"#][^"]*)"', s):
            if href.startswith(("mailto:", "tel:", "javascript:", "data:", "whatsapp:")) or any(c in href for c in "'+{}$<>"):
                continue  # JavaScript icindeki parcalar baglanti degil
            target_root, path = None, None
            for s2, (r2, b2) in SITES.items():
                if href.startswith(b2 + "/") or href == b2:
                    target_root, path = r2, href[len(b2):]
            if href.startswith(("http://", "https://", "//")) and target_root is None:
                continue
            if target_root is None:
                target_root = root
                path = (Path(rel).parent / href.split("#")[0].split("?")[0]).as_posix() if not href.startswith("/") else href
                if ".." in path:
                    parts = []
                    for part in path.split("/"):
                        if part == "..":
                            parts = parts[:-1]
                        elif part not in ("", "."):
                            parts.append(part)
                    path = "/".join(parts)
            if not target_exists(target_root, path):
                rows["link"].append(f"{site}/{rel} → {href}")
        if site == "mobilcv.net" and not rel.startswith("en/") and re.search(r'href="https?://mobilcv\.com/?"', s):
            rows["apex"].append(f"{site}/{rel}")
        if GA in s and "mobilcv_consent" not in s:
            rows["consent"].append(f"{site}/{rel}: Analytics kodu var ama çerez onayı yok")
    counts[site] = n
    # site haritalari
    for sm in sorted(root.glob("sitemap*.xml")):
        for loc in re.findall(r"<loc>([^<]+)</loc>", sm.read_text(encoding="utf-8")):
            if not loc.startswith(base):
                rows["sitemap"].append(f"{site}/{sm.name}: başka alan adı → {loc}")
                continue
            path = loc[len(base):]
            if not target_exists(root, path):
                rows["sitemap"].append(f"{site}/{sm.name}: dosya yok → {loc}")
            else:
                p = root / path.lstrip("/")
                p = p if p.is_file() else p / "index.html"
                if p.is_file() and re.search(r'name="robots" content="[^"]*noindex', p.read_text(encoding="utf-8", errors="ignore")):
                    rows["sitemap"].append(f"{site}/{sm.name}: noindex sayfa haritada → {loc}")
    rb = root / "robots.txt"
    if rb.exists():
        for line in rb.read_text(encoding="utf-8").splitlines():
            if line.strip().lower().startswith(("disallow:", "crawl-delay", "host:")) and line.split(":", 1)[1].strip():
                rows["robots"].append(f"{site}/robots.txt: {line.strip()}")

def recent(root):
    try:
        out = subprocess.run(["git", "-C", str(root), "log", "--since=8 days ago", "--name-only", "--pretty=format:"],
                             capture_output=True, text=True).stdout
        return sorted({l for l in out.splitlines() if l.endswith(".html")})
    except Exception:
        return []

T = {"yasak": "Yanıltıcı / yasak ifade şüphesi", "canonical": "Standart adres (canonical)", "link": "Kırık iç bağlantı",
     "sitemap": "Site haritası", "robots": "robots.txt engelleri", "consent": "Çerez onayı / Analytics",
     "apex": "www'suz mobilcv.com bağlantısı (mobilcv.net)"}
lines = ["# MobilCV haftalık kontrol", "",
         f"Taranan sayfa: mobilcv.com {counts['mobilcv.com']}, mobilcv.net {counts['mobilcv.net']}", ""]
total = 0
for k, title in T.items():
    items = rows[k]; total += len(items)
    lines.append(f"## {title}: {'✅ sorun yok' if not items else f'⚠️ {len(items)}'}")
    lines += [f"- {x}" for x in items[:30]]
    if len(items) > 30:
        lines.append(f"- … ve {len(items) - 30} tane daha")
    lines.append("")
for site, (root, _) in SITES.items():
    r = recent(root)
    lines.append(f"## Son 8 günde değişen sayfalar ({site}): {len(r)}")
    lines += [f"- {x}" for x in r[:20]]
    lines.append("")
lines.insert(3, f"Toplam bulgu: {total}")
report = "\n".join(lines)
if OUT:
    OUT.write_text(report, encoding="utf-8")
print(report)
