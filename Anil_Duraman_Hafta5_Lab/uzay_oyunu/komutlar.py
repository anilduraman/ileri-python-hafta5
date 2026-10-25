"""Oyuncu komutlarının kaydedildiği modül."""
from functools import wraps

KOMUTLAR = {}


def komut(ad, aciklama=""):
    """Fonksiyonu değiştirmeden (fonksiyon, açıklama) biçiminde kaydeder."""
    if ad in KOMUTLAR:
        raise ValueError(f"'{ad}' komutu zaten kayıtlı")

    def dekorator(func):
        if ad in KOMUTLAR:
            raise ValueError(f"'{ad}' komutu zaten kayıtlı")
        KOMUTLAR[ad] = (func, aciklama)
        return func
    return dekorator


@komut("yardim", "komutları listeler")
def yardim(durum):
    """Kayıtlı komutların adlarını ve açıklamalarını döndürür."""
    return "\n".join(
        f"{ad:<10} {aciklama}".rstrip()
        for ad, (_, aciklama) in sorted(KOMUTLAR.items())
    )


@komut("envanter", "eşyalarını gösterir")
def envanter(durum):
    """Oyuncunun envanterini döndürür."""
    esyalar = durum.get("envanter", [])
    return ", ".join(map(str, esyalar)) if esyalar else "Envanter boş"


@komut("harita", "gidebileceğin gezegenleri gösterir")
def harita(durum):
    """Bulunulan konumdan erişilebilen gezegenleri döndürür."""
    konum = durum.get("konum")
    baglantilar = durum.get("baglantilar", {})
    return ", ".join(map(str, baglantilar.get(konum, []))) or "Gidilecek yer yok"
