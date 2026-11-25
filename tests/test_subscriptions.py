from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient

from app.main import app, subscriptions

client = TestClient(app)


@pytest.fixture(autouse=True)
def temizle():
    subscriptions.clear()


def ekle(name="Netflix", price=200, cycle="monthly", gun=5):
    return client.post(
        "/subscriptions",
        json={
            "name": name,
            "price": price,
            "billing_cycle": cycle,
            "next_renewal": (date.today() + timedelta(days=gun)).isoformat(),
        },
    )


def test_gecerli_abonelik_201_doner():
    response = ekle()
    assert response.status_code == 201
    assert response.json()["name"] == "Netflix"


def test_fiyat_sifir_veya_negatifse_422_doner():
    assert ekle(price=0).status_code == 422
    assert ekle(price=-10).status_code == 422


def test_eklenen_abonelik_listede_gorunur():
    ekle(name="Spotify")
    response = client.get("/subscriptions")
    assert response.status_code == 200
    assert [s["name"] for s in response.json()] == ["Spotify"]


def test_ozet_aylik_ve_yillik_toplami_hesaplar():
    ekle(name="Netflix", price=200, cycle="monthly")
    ekle(name="Spor Salonu", price=1200, cycle="yearly")
    data = client.get("/subscriptions/summary").json()
    assert data["monthly_total"] == 300.0
    assert data["yearly_total"] == 3600.0


def test_abonelik_yoksa_ozet_sifir_doner():
    data = client.get("/subscriptions/summary").json()
    assert data["monthly_total"] == 0
    assert data["subscription_count"] == 0


def test_yaklasan_sadece_istenen_gun_icindekileri_dondurur():
    ekle(name="Yakin", gun=3)
    ekle(name="Uzak", gun=30)
    response = client.get("/upcoming?days=7")
    assert response.status_code == 200
    assert [s["name"] for s in response.json()] == ["Yakin"]


def test_yaklasan_tarihe_gore_siralidir():
    ekle(name="Gec", gun=6)
    ekle(name="Erken", gun=2)
    names = [s["name"] for s in client.get("/upcoming?days=7").json()]
    assert names == ["Erken", "Gec"]


def test_suresi_gecmis_abonelik_listelenmez():
    ekle(name="Gecmis", gun=-2)
    assert client.get("/upcoming?days=7").json() == []


def test_gecersiz_gun_degeri_422_doner():
    assert client.get("/upcoming?days=0").status_code == 422


def test_arayuz_sayfasi_acilir():
    response = client.get("/ui")
    assert response.status_code == 200
    assert "Abonelik Avcısı" in response.text
