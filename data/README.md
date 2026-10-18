verilerle ilgili güncel durum 18 ekim 2026

caltech dosyaları data/raw/acn içinde 14 çeyrek dosyası ve toplam 31424 oturum var
ilk bağlantı 25 nisan 2018 son bağlantı 14 eylül 2021
notebook caltech_*.json dosyalarını okuyor eski örnek dosyalar bu listeye girmiyor

norveçteki Dataset1 ile Dataset4 arasındaki csvler doğrudan data/raw içinde duruyor
urbanev de data/raw/UrbanEVDataset altında
bu iki kaynak ilk modele katılmadı

notebook birleşmiş oturumları data/processed/caltech_all_sessions.csv olarak kaydediyor
saatlik matris notebook içinde hesaplanıyor ayrıca dosyaya yazılmıyor
ham veriler ve üretilen csvler gitignore içinde repoda yok

aynı veriyi almak için [indirme yöntemi ve ajan promptu](../yapilanlar.md)
alanlar tarih aralıkları ve boyutlar için [veri setleri](VERI_SETLERI.md)

kaynaklar

caltech [acn-data](https://ev.caltech.edu/dataset) ve [makale](https://doi.org/10.1145/3307772.3328313)
norveç [zenodo](https://zenodo.org/records/13896176)
urbanev [dryad](https://doi.org/10.5061/dryad.np5hqc04z)

kaynakların lisans şartlarını ayrıca tamamlayacağız burada link bulunması kullanım koşullarının kontrol edildiği anlamına gelmiyor
