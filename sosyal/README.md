# Sosyal medya kuyruğu

- `kuyruk.json`: paylaşılacak Instagram gönderileri. Her kayıt: `id`, `gorsel_url` (https://mobilcv.net/sosyal/... JPEG), `aciklama`, `onay` (kurucu "ok" deyince true), `paylasildi` (otomatik doldurulur).
- Paylaşım `.github/workflows/instagram.yml` ile yapılır; anahtar GitHub Secrets'ta `IG_TOKEN`.
- Kurucu onayı olmadan `onay: true` yapılmaz.
