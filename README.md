# Abonelik Avcısı

Abonelikleri takip eden, aylık/yıllık maliyeti ve yaklaşan yenilemeleri gösteren basit bir REST API ve tarayıcı arayüzü.

## Problem ve hedef kitle

Kullanılmayan aboneliklere farkında olmadan para ödeniyor. Bu uygulama, aboneliklerin toplam maliyetini ve yakında yenilenecek olanları gösterir. Hedef kitle: birden fazla dijital abonelik kullanan öğrenciler ve genç çalışanlar.

## İş takip panosu

https://github.com/users/dilaraciftli65/projects/4

Kartlar Yapılacak / Devam Ediyor / Tamamlandı sütunlarında. Tamamlanan özelliklerin PR bağlantıları ilgili issue'larda: [#1](https://github.com/dilaraciftli65/abonelik-avcisi/issues/1), [#2](https://github.com/dilaraciftli65/abonelik-avcisi/issues/2), [#7](https://github.com/dilaraciftli65/abonelik-avcisi/issues/7).

## Kurulum ve çalıştırma

```bash
git clone https://github.com/dilaraciftli65/abonelik-avcisi.git
cd abonelik-avcisi
python -m venv .venv
.venv\Scripts\Activate.ps1      # Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

- Arayüz: http://127.0.0.1:8000/ui
- API dokümantasyonu: http://127.0.0.1:8000/docs

## Testler

```bash
python -m pytest
```

Beklenen: `10 passed`.

## Özellikleri deneme

Veriler bellekte tutulur, sunucu yeniden başlatılırsa silinir.

**Özellik 1: Abonelik ekleme, listeleme, aylık maliyet** ([#1](https://github.com/dilaraciftli65/abonelik-avcisi/issues/1))
1. `/ui` sayfasında formu doldur ve **Ekle**'ye bas. Tarih `GG/AA/YYYY` biçiminde girilir.
2. Tabloda kaydı, özet kartlarında toplamları gör.
3. Alternatif: `/docs` içinde `POST /subscriptions` ile ekle, `GET /subscriptions/summary` ile toplamı kontrol et.

**Özellik 2: Yaklaşan yenilemeler** ([#2](https://github.com/dilaraciftli65/abonelik-avcisi/issues/2))
1. Yenilenme tarihi bugünden 3 gün sonra olan bir abonelik ekle.
2. "Önümüzdeki gün" kutusuna `7` yaz ve **Göster**'e bas. Abonelik listelenir.
3. Kutuyu `1` yap. Abonelik görünmez.

Alternatif: `/docs` içinde `GET /upcoming?days=7` çağır.

## Proje yapısı

```
app/main.py            API endpoint'leri
app/static/index.html  Tarayıcı arayüzü
tests/                 Testler
```