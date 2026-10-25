"""Örnek oyun fonksiyonları ve etkileşim döngüsü."""
from .dekoratorler import log_cagri, sinirla, sure_olc
from .komutlar import KOMUTLAR


@log_cagri
def galaksi_kur(ad="Samanyolu"):
    """Bir galaksi için örnek açıklama üretir."""
    return f"{ad} galaksisi kuruldu"


@log_cagri
def hedef_menusu(hedefler=None):
    """Hedef listesini metin olarak döndürür."""
    return ", ".join(hedefler or ["orion", "dünya", "kara_delik"])


@sinirla(0, 100)
def yakit_harca(miktar):
    """100 birimlik depodan yakıt harcar ve kalan miktarı döndürür."""
    return 100 - miktar


@sure_olc
def ornek_rota(adim=20):
    """Önbelleksiz rota sayacı için örnek çalışma."""
    toplam = 0
    for i in range(adim * 1000):
        toplam += i
    return toplam


def travel(durum, input_fn=input, print_fn=print):
    """Komutları çalıştırır; diğer girdileri gezegen seçimi sayar."""
    gezegenler = durum.get("baglantilar", {}).get(durum.get("konum"), [])
    while True:
        print_fn("Nereye gitmek istersin?")
        for i, gezegen in enumerate(gezegenler, 1):
            print_fn(f"[{i}] {gezegen}")
        secim = input_fn("> ").strip()
        if secim in KOMUTLAR:
            fonksiyon, _ = KOMUTLAR[secim]
            print_fn(fonksiyon(durum))
            continue
        if secim.isdigit() and 1 <= int(secim) <= len(gezegenler):
            durum["konum"] = gezegenler[int(secim) - 1]
            print_fn(f"{durum['konum']} konumuna ulaştın.")
            return durum["konum"]
        if secim.lower() in {"q", "quit", "çık", "cik"}:
            return None
        print_fn("Geçersiz seçim.")
