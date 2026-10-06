# Proje Yol Haritası & İş Bölümü

Bu doküman, dönem boyunca Mahmud ve Ege olarak geliştireceğimiz Elektrikli Araç Şarj İstasyonlarında Doluluk Tahmini projesinin haftalık planını ve görev dağılımını içerir.

## Ekip & Görev Dağılımı
- **Ege Arhan YILDIZALKAN (241230013):** Veri hattı mimarisi, zaman serisi dönüşümleri, derin öğrenme (BiLSTM / Hibrit mimariler) ve modelleme.
- **Mahmud Selman ŞAHİN (241230008):** Dış veri entegrasyonu (hava durumu / takvim), veri temizleme/EDA, tabular modeller (Random Forest, XGBoost, CatBoost).

---

## Haftalık Çalışma Takvimi

### 1. Hafta (6 - 12 Ekim)
- [ ] Proje repo düzeni, sanal ortam ve temel gereksinimlerin (`requirements.txt`) hazırlanması.
- [ ] ACN-Data ve Zenodo veri setlerinin indirilip ham veri (`data/raw/`) formatlarının incelenmesi.
- [ ] İlk veri okuma fonksiyonunun yazılması.

### 2. Hafta (13 - 19 Ekim)
- [ ] Ham şarj oturum verisinden saatlik doluluk matrisine geçiş betiğinin oluşturulması.
- [ ] Takvim özellikleri (haftanın günü, saat, tatil günleri) çıkarma.
- [ ] İlk keşifsel veri analizi (EDA) notebook'unun tamamlanması.

### 3. Hafta (20 - 26 Ekim)
- [ ] Open-Meteo API üzerinden ilgili lokasyonların geçmiş hava durumu verilerinin çekilmesi.
- [ ] Veri setlerinin birleştirilmesi ve eksik/hatalı oturumların temizlenmesi.
- [ ] Train/validation/test bölme mantığının (zaman serisine uygun şekilde sızıntısız) kurulması.

### 4. Hafta (27 Ekim - 2 Kasım)
- [ ] Baseline modellerin kurulması (Lojistik Regresyon / Basit Karar Ağacı).
- [ ] Tabular modellerin eğitilmesi (Random Forest ve XGBoost).
- [ ] Değerlendirme metriklerinin (MAE, RMSE, F1, Doğruluk) standartlaştırılması.

### 5. Hafta (3 - 9 Kasım) — *Ara Rapor Hazırlığı*
- [ ] Ara rapor / Vize teslimi için yöntem ve veri ön işleme bölümlerinin yazılması.
- [ ] Modellerin ilk kıyaslama tablosunun rapora eklenmesi.

### 6. Hafta (10 - 16 Kasım)
- [ ] PyTorch ile BiLSTM tabanlı doluluk tahmin modelinin geliştirilmesi.
- [ ] Hibrit model denemeleri (Tabular + Dizi modelleri).

### 7. Hafta (17 - 23 Kasım)
- [ ] Farklı coğrafi istasyonlar arası transfer kabiliyetinin test edilmesi (UrbanEV vs ACN-Data).
- [ ] Hiperparametre optimizasyonu (Optuna denemeleri).

### 8. Hafta (24 - 30 Kasım)
- [ ] Model sonuçlarının hata analizi ve grafikleştirilmesi (doluluk eğrileri, konfüzyon matrisleri).
- [ ] Final makale/rapor taslağının oluşturulması.

### 9. Hafta & Final Süreci (Aralık)
- [ ] Kod refaktörü ve testlerin tamamlanması.
- [ ] Proje sonuç raporunun ve sunumunun hazırlanması.
