from functools import lru_cache
from uzay_oyunu.dekoratorler import sure_olc, say, log_cagri, sinirla, hafiza


def test_sure_olc_sonucu_korur(capsys):
    @sure_olc
    def topla(a, b):
        return a + b
    assert topla(2, 3) == 5
    assert "topla:" in capsys.readouterr().out


def test_sure_olc_adli_arguman():
    @sure_olc
    def selam(ad, son="!"):
        return ad + son
    assert selam(ad="Anıl", son=".") == "Anıl."


def test_sure_olc_name_doc_korur():
    def ornek():
        """belge"""
        return 1
    wrapped = sure_olc(ornek)
    assert wrapped.__name__ == "ornek"
    assert wrapped.__doc__ == "belge"


def test_say_sayar():
    @say
    def f(x):
        return x * 2
    assert f(3) == 6
    assert f(4) == 8
    assert f.cagri == 2


def test_log_cagri_yazar(capsys):
    @log_cagri
    def f(x, y=2):
        return x + y
    assert f(3, y=4) == 7
    output = capsys.readouterr().out
    assert "-> f(" in output and "<- f = 7" in output


def test_sinirla_sinirlar():
    @sinirla(0, 100)
    def yakit_harca(miktar):
        return 100 - miktar
    assert yakit_harca(0) == 100
    assert yakit_harca(100) == 0
    assert yakit_harca(30) == 70


def test_sinirla_aralik_disi():
    @sinirla(0, 100)
    def yakit_harca(miktar):
        return 100 - miktar
    for miktar in (-1, 101, 150):
        try:
            yakit_harca(miktar)
        except ValueError as exc:
            assert "yakit_harca" in str(exc)
        else:
            assert False, "ValueError bekleniyordu"


def test_hafiza_lru_ile_ayni_sonuclar():
    @hafiza(maxsize=2)
    def kare(x):
        return x * x
    @lru_cache(maxsize=2)
    def kare_lru(x):
        return x * x
    for x in [2, 3, 2, 4, 3]:
        assert kare(x) == kare_lru(x)
    assert len(kare.cache) <= 2
