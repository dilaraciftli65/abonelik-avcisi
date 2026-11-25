# Abonelik Avcısı

Netflix, Spotify, spor salonu gibi aboneliklerini tek yerde takip eden basit bir REST API.

## Hangi problemi çözüyor?

İnsanlar kullanmadıkları aboneliklere her ay para ödemeye devam ediyor, çünkü yenilenme tarihlerini ve toplam maliyeti bilmiyor. Abonelik Avcısı, aboneliklerini kaydetmeni, aylık/yıllık toplam maliyeti görmeni ve yakında yenilenecek olanları önceden fark etmeni sağlar.

## Kimin için?

Birden fazla dijital abonelik kullanan öğrenciler ve genç çalışanlar için.

## İş takip panosu

https://github.com/users/dilaraciftli65/projects/4

## Projeyi çalıştırma

```bash
git clone https://github.com/dilaraciftli65/abonelik-avcisi.git
cd abonelik-avcisi
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Tarayıcıda http://127.0.0.1:8000/docs adresini aç.

## Testleri çalıştırma

```bash
python -m pytest
```

## Geliştirilen iki özelliği deneme

### Özellik 1: Abonelik ekleme, listeleme ve aylık maliyet

1. `/docs` sayfasında `POST /subscriptions` endpoint'ini aç, "Try it out" de ve şunu gönder:
   ```json
   {"name": "Netflix", "price": 199.99, "billing_cycle": "monthly", "next_renewal": "2026-12-01"}
   ```
2. `GET /subscriptions` ile eklenen aboneliğin listede göründüğünü doğrula.
3. `GET /subscriptions/summary` ile aylık ve yıllık toplam maliyeti gör.

### Özellik 2: Yaklaşan yenilemeler

1. Yenilenme tarihi bugünden 1-7 gün sonra olan bir abonelik ekle.
2. `GET /upcoming?days=7` çağır. Sadece 7 gün içinde yenilenenler döner.

## Yol haritası

Silme, güncelleme, GitHub Actions ile otomatik test ve Docker desteği pano üzerinde "Yapılacak" durumundadır.