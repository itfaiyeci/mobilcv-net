# -*- coding: utf-8 -*-
"""Threads resmi API ile paylasim.
Kullanim:
  python3 scripts/th_paylas.py kontrol   -> anahtar ve hesap kontrolu (paylasim YOK)
  python3 scripts/th_paylas.py paylas    -> sosyal/kuyruk.json'da onay=true, platformlarda "threads" olan
                                            ve th_paylasildi bos olanlari paylasir
Anahtar: THREADS_TOKEN ortam degiskeni (GitHub Secrets). Tanimli degilse sessizce atlar (hata vermez).
Metin: kayitta "aciklama_threads" varsa o, yoksa "aciklama" kullanilir (Threads siniri 500 karakter)."""
import json, os, sys, time, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = "https://graph.threads.net/v1.0"
BEKLENEN_KULLANICI = "mobilcvcom"
KUYRUK = Path("sosyal/kuyruk.json")
TOKEN = os.environ.get("THREADS_TOKEN", "").strip()

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
    print(f"Threads anahtari calisiyor. Hesap: @{me['username']} | id: {me.get('id')}")

def paylas():
    me = hesap(); uid = me["id"]
    kuyruk = json.loads(KUYRUK.read_text(encoding="utf-8")) if KUYRUK.exists() else []
    bekleyen = [g for g in kuyruk if g.get("onay") is True and "threads" in g.get("platformlar", ["instagram"]) and not g.get("th_paylasildi")]
    if not bekleyen:
        print("Threads icin onayli ve paylasilmamis gonderi yok."); return
    for g in bekleyen[:2]:  # bir calismada en fazla 2 gonderi
        metin = (g.get("aciklama_threads") or g.get("aciklama") or "").strip()
        if len(metin) > 500:
            raise SystemExit(f"Threads metni 500 karakteri asiyor ({g['id']}: {len(metin)}). Durduruldu.")
        veri = {"media_type": "IMAGE", "image_url": g["gorsel_url"], "text": metin} if g.get("gorsel_url") else {"media_type": "TEXT", "text": metin}
        cid = istek(f"{uid}/threads", veri, "POST")["id"]
        for _ in range(24):
            time.sleep(5)
            durum = istek(cid, {"fields": "status,error_message"})
            if durum.get("status") == "FINISHED": break
            if durum.get("status") in ("ERROR", "EXPIRED"):
                raise SystemExit(f"Threads gorseli islenemedi ({g['id']}): {durum}")
        mid = istek(f"{uid}/threads_publish", {"creation_id": cid}, "POST")["id"]
        link = istek(mid, {"fields": "permalink"}).get("permalink", "")
        g["th_paylasildi"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"); g["th_medya_id"] = mid; g["th_baglanti"] = link
        print(f"Threads'te paylasildi: {g['id']} -> {link}")
        time.sleep(10)
    KUYRUK.write_text(json.dumps(kuyruk, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

if __name__ == "__main__":
    islem = sys.argv[1] if len(sys.argv) > 1 else "kontrol"
    if not TOKEN:
        if islem == "kontrol": raise SystemExit("THREADS_TOKEN tanimli degil.")  # kontrolde eksik anahtar hata sayilir
        print("THREADS_TOKEN tanimli degil; Threads adimi atlandi."); sys.exit(0)
    {"kontrol": kontrol, "paylas": paylas}[islem]()
