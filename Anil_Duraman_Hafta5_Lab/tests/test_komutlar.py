import pytest
from uzay_oyunu.komutlar import KOMUTLAR, komut, yardim, envanter, harita
from uzay_oyunu.oyun import travel


@pytest.fixture
def durum():
    return {
        "konum": "orion",
        "baglantilar": {"orion": ["dünya", "kara_delik"], "dünya": ["orion"]},
        "credits": 100,
        "engines": ["warp"],
        "copilot": "Ada",
        "envanter": ["anahtar", "kristal"],
    }


def test_yardim_komutu(durum):
    assert "yardim" in yardim(durum)
    assert "harita" in yardim(durum)


def test_envanter_komutu(durum):
    assert envanter(durum) == "anahtar, kristal"


def test_harita_komutu(durum):
    assert harita(durum) == "dünya, kara_delik"


def test_komut_cift_kayit_hatasi():
    with pytest.raises(ValueError):
        @komut("yardim", "yinelenen")
        def yardim_yeni(durum):
            return "olmaz"


def test_travel_komutu_calistirir_ve_devam_eder(durum):
    inputs = iter(["envanter", "1"])
    outputs = []
    sonuc = travel(durum, input_fn=lambda _: next(inputs), print_fn=outputs.append)
    assert sonuc == "dünya"
    assert any("anahtar, kristal" in satir for satir in outputs)
    assert outputs.count("Nereye gitmek istersin?") == 2
