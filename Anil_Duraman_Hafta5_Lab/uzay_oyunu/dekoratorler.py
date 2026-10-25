"""Hafta 5 lab ödevi için dekoratörler."""

from collections import OrderedDict
from functools import wraps
from time import perf_counter


def sure_olc(func):
    """Fonksiyonun çalışma süresini ölçer ve sonucu değiştirmeden döndürür."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        baslangic = perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            sure = perf_counter() - baslangic
            print(f"{func.__name__}: {sure:.4f} sn")
    return wrapper


def say(func):
    """Fonksiyonun çağrılma sayısını wrapper.cagri niteliğinde tutar."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.cagri += 1
        return func(*args, **kwargs)
    wrapper.cagri = 0
    return wrapper


def log_cagri(func):
    """Çağrı argümanlarını ve dönüş değerini yazdırır."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        parcalar = [repr(arg) for arg in args]
        parcalar.extend(f"{key}={value!r}" for key, value in kwargs.items())
        print(f"-> {func.__name__}({', '.join(parcalar)})")
        sonuc = func(*args, **kwargs)
        print(f"<- {func.__name__} = {sonuc!r}")
        return sonuc
    return wrapper


def sinirla(alt, ust):
    """İlk argümanın belirtilen kapalı aralıkta olmasını zorunlu kılar."""
    def dekorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if args:
                deger = args[0]
            elif func.__code__.co_varnames and func.__code__.co_varnames[0] in kwargs:
                deger = kwargs[func.__code__.co_varnames[0]]
            else:
                raise TypeError(f"{func.__name__} için ilk argüman eksik")
            if not alt <= deger <= ust:
                raise ValueError(
                    f"{func.__name__}: {deger} değeri {alt}-{ust} aralığında değil"
                )
            return func(*args, **kwargs)
        return wrapper
    return dekorator


def hafiza(maxsize=None):
    """lru_cache kullanmadan sözlük tabanlı, isteğe bağlı sınırlı önbellek."""
    if maxsize is not None and maxsize < 1:
        raise ValueError("maxsize en az 1 olmalıdır")
    def dekorator(func):
        cache = OrderedDict()

        @wraps(func)
        def wrapper(*args, **kwargs):
            anahtar = (args, tuple(sorted(kwargs.items())))
            try:
                hash(anahtar)
            except TypeError as exc:
                raise TypeError("hafiza önbelleği için argümanlar hash edilebilir olmalı") from exc
            if anahtar in cache:
                cache.move_to_end(anahtar)
                return cache[anahtar]
            sonuc = func(*args, **kwargs)
            cache[anahtar] = sonuc
            if maxsize is not None and len(cache) > maxsize:
                cache.popitem(last=False)
            return sonuc
        wrapper.cache = cache
        return wrapper
    return dekorator
