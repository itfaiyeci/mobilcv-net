# -*- coding: utf-8 -*-
"""Threads resmi API ile paylasim.
Kullanim:
  python3 scripts/th_paylas.py kontrol   -> anahtar ve hesap kontrolu (paylasim YOK)
  python3 scripts/th_paylas.py paylas    -> sosyal/kuyruk.json'da onay=true, platformlarda "threads" olan
                                            ve th_paylasildi bos olanlari paylasir
  python3 scripts/th_paylas.py kontrol en / paylas en
                                         -> Ingilizce hesap @mobilcv.en (THREADS_TOKEN_EN, platform "threads_en",
                                            metin "aciklama_threads_en", gorsel "gorsel_url_en", alanlar th_en_*)
Anahtar: THREADS_TOKEN (TR) / THREADS_TOKEN_EN (EN) ortam degiskeni (GitHub Secrets). Tanimli degilse paylasimda sessizce atlar.
Metin: TR'de "aciklama_threads" yoksa "aciklama"; EN'de "aciklama_threads_en" zorunlu (Threads siniri 500 karakter)."""
import json, os, sys, time, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = "https://graph.threads.net/v1.0"
DIL = sys.argv[2] if len(sys.argv) > 2 else "tr"
if DIL not in ("tr", "en"):
    raise SystemExit("Dil 'tr' ya da 'en' olmali.")
EN = DIL == "en"
BEKLENEN_KULLANICI = "mobilcv.en" if EN else "mobilcvcom"
KUYRUK = Path("sosyal/kuyruk.json")
ANAHTAR_ADI = "THREADS_TOKEN_EN" if EN else "THREADS_TOKEN"
TOKEN = os.environ.get(ANAHTAR_ADI, "").strip()
PLATFORM = "threads_en" if EN else "threads"
ALAN = "th_en_" if EN else "th_"

def istek(yol, veri=None, yontem="GET"):
    params = dict(veri or {}); params["access_token"] = TOKEN
    q = urllib.parse.urlencode(params)
    url = f"{API}/{yol}"
    req = urllib.request.Request(url + ("?" + q if yontem == "GET" else ""), data=(q.encode() if yontem == "POST" else None), method=yontem)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        govde = e.read().decode(errors="replace")
        govde = govde.replace(TOKEN, "***") if TOKEN else govde
        raise SystemExit(f"Threads API hatasi {e.code} ({yol}): {govde[:500]}")

def hesap():
    me = istek("me", {"fields": "id,username"})
    if me.get("username") != BEKLENEN_KULLANICI:
        raise SystemExit(f"Beklenmeyen Threads hesabi: {me.get('username')} (beklenen {BEKLENEN_KULLANICI}). Durduruldu.")
    return me

def kontrol():
    me = hesap()
    print(f"Threads ({DIL}) anahtari calisiyor. Hesap: @{me['username']} | id: {me.get('id')}")

def paylas():
    me = hesap(); uid = me["id"]
    kuyruk = json.loads(KUYRUK.read_text(encoding="utf-8")) if KUYRUK.exists() else []
    bekleyen = [g for g in kuyruk if g.get("onay") is True and PLATFORM in g.get("platformlar", ["instagram"]) and not g.get(ALAN + "paylasildi")]
    if not bekleyen:
        print(f"Threads ({DIL}) icin onayli ve paylasilmamis gonderi yok."); return
    for g in bekleyen[:2]:  # bir calismada en fazla 2 gonderi
        if EN:
            metin = (g.get("aciklama_threads_en") or "").strip()
            if not metin:
                raise SystemExit(f"EN Threads metni yok ({g['id']}): aciklama_threads_en gerekli. Durduruldu.")
            gorsel = g.get("gorsel_url_en") or g.get("gorsel_url")
        else:
            metin = (g.get("aciklama_threads") or g.get("aciklama") or "").strip()
            gorsel = g.get("gorsel_url")
        if len(metin) > 500:
            raise SystemExit(f"Threads metni 500 karakteri asiyor ({g['id']}: {len(metin)}). Durduruldu.")
        veri = {"media_type": "IMAGE", "image_url": gorsel, "text": metin} if gorsel else {"media_type": "TEXT", "text": metin}
        cid = istek(f"{uid}/threads", veri, "POST")["id"]
        for _ in range(24):
            time.sleep(5)
            durum = istek(cid, {"fields": "status,error_message"})
            if durum.get("status") == "FINISHED": break
            if durum.get("status") in ("ERROR", "EXPIRED"):
                raise SystemExit(f"Threads gorseli islenemedi ({g['id']}): {durum}")
        mid = istek(f"{uid}/threads_publish", {"creation_id": cid}, "POST")["id"]
        link = istek(mid, {"fields": "permalink"}).get("permalink", "")
        g[ALAN + "paylasildi"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"); g[ALAN + "medya_id"] = mid; g[ALAN + "baglanti"] = link
        print(f"Threads ({DIL}) paylasildi: {g['id']} -> {link}")
        time.sleep(10)
    KUYRUK.write_text(json.dumps(kuyruk, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

if __name__ == "__main__":
    islem = sys.argv[1] if len(sys.argv) > 1 else "kontrol"
    if not TOKEN:
        if islem == "kontrol": raise SystemExit(f"{ANAHTAR_ADI} tanimli degil.")  # kontrolde eksik anahtar hata sayilir
        print(f"{ANAHTAR_ADI} tanimli degil; Threads ({DIL}) adimi atlandi."); sys.exit(0)
    {"kontrol": kontrol, "paylas": paylas}[islem]()
