# Dekoratör Sırası – Fibonacci

Özyinelemeli Fibonacci için `fib(20)` çağrısında ödev föyünde verilen sonuçlar:

| Dekorasyon | Çağrı sayısı |
|---|---:|
| Yalnızca `@say` | 21891 |
| `@say` üstte, `@lru_cache` altta | 39 |
| `@lru_cache` üstte, `@say` altta | 21 |

## Neden farklı?

- **Yalnızca `@say`:** Fibonacci'nin aynı alt problemleri tekrar tekrar hesaplanır. Sayaç her özyinelemeli çağrıyı sayar.
- **`@say` üstte, `@lru_cache` altta:** Dıştaki sayaç çağrıları sayarken içteki önbellek daha önce hesaplanan sonuçları tekrar hesaplamaz. Sayaç önbellek isabetleri dâhil dış çağrıları görür.
- **`@lru_cache` üstte, `@say` altta:** Önbellek sayaç sarmalayıcısının dışındadır. Önbellek isabetlerinde sayaç sarmalayıcısı yeniden çağrılmaz; bu nedenle sayaç yalnızca önbellek kaçırmalarını/ilk hesaplamaları sayar. Bu durumda sayaç değerine `fib.__wrapped__.cagri` üzerinden ulaşılabilir.

Sayılar Python sürümüne ve sayacın nasıl okunduğuna göre değişebileceğinden, proje testleri kullandığınız uygulamadaki gerçek sayımı kontrol etmelidir.
