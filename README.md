# Elektrikli Araç Şarj İstasyonlarında Doluluk Tahmini

Caltech ACN-Data ile bir şarj noktasının bir sonraki saat başında dolu mu boş mu olacağını tahmin ediyoruz. Norveç konut şarjı ve UrbanEV verileri ikinci ve üçüncü veri seti olarak inceleniyor.

Ekip: Ege Arhan Yıldızalkan, Mahmud Selman Şahin

## Kurulum

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m ipykernel install --user --name ev-doluluk --display-name "Python (EV Doluluk)"
```

## Veri

Ham veri repoda yok (`data/raw/` git dışı).

- ACN-Data: [ev.caltech.edu/dataset](https://ev.caltech.edu/dataset) sayfasında Caltech seçip çeyrek çeyrek indiriyoruz (büyük aralıkta dosya yarıda kesiliyor). Dosyalar `data/raw/acn/caltech_2018_Q2.json` ... `caltech_2021_Q3.json`, toplam 14 dosya ve 31.424 oturum. Ayrıntı: `yapilanlar.md`.
- Norveç: [doi.org/10.5281/zenodo.13896176](https://doi.org/10.5281/zenodo.13896176), dosyaları `data/raw/` altına koy.
- UrbanEV: [doi.org/10.5061/dryad.np5hqc04z](https://doi.org/10.5061/dryad.np5hqc04z), `data/raw/UrbanEVDataset/` altına koy.

Veri setlerinin alanları, tarih aralıkları ve lisansları `data/VERI_SETLERI.md` içinde.

## Çalıştırma

Notebook'lar sırayla:

1. `notebooks/01_veri_inceleme.ipynb` ilk veri hazırlama ve random forest denemesi
2. `notebooks/02_selman_kontrol.ipynb` bağımsız kontrol
3. `notebooks/03_kapsama_2020.ipynb` kayıt boşlukları
4. `notebooks/04_eda_grafikleri.ipynb` EDA
5. `notebooks/05_model_verisi_ve_baseline.ipynb` model tablosu, train/val/test bölmesi, doğrulama sonuçları
6. `notebooks/06_norvec_eda.ipynb` Norveç verisi

Testler:

```bash
python -m pytest tests -q
```

## Klasörler

- `src/load_data.py` oturumları okur, kalite kontrolü yapar, saatlik doluluk matrisi üretir
- `src/split.py` train/val/test tarih sınırları
- `src/features/` takvim, hava durumu ve lag özellikleri
- `tests/` birim testleri
- `reports/figures/` rapor görselleri

Haftalık plan `ROADMAP.md`, yapılanlar `yapilanlar.md` içinde.
