# Veri setleri

Kontrol tarihi: 18 Ekim 2026. Satır sayıları başlık satırını içermiyor. Kaynaktaki boyutlarla yerelde saydığımız kayıtlar ayrı belirtiliyor; JSON alan sayısı, düzleştirilmiş bir tablonun sütun sayısıyla aynı olmayabilir.

## Genel görünüm

| Veri seti | Yer ve kullanım | Tarih kapsamı | Bir kayıt neyi anlatıyor? | Projedeki kullanımımız |
|---|---|---|---|---|
| ACN-Data | Kaliforniya, ABD; kampüs ve işyeri şarjı | Caltech için literatürde Nisan 2018 - Eylül 2021; diğer sahalar ayrıca kontrol edilmeli | Bir aracın şarj noktasına bağlanıp ayrıldığı oturum | İlk veri hattı ve nokta bazında dolu/boş tahmini |
| Norveç konut şarjı (Zenodo) | 12 konut lokasyonu, 267 kullanıcı | 6 Şubat 2018 - 6 Ağustos 2021; her lokasyon farklı dönemi kapsıyor | Oturum, kullanıcı veya oturumun bir saati; dosyaya göre değişiyor | Konut kullanımını incelemek ve ikinci veri kaynağında yöntemimizi denemek |
| UrbanEV | Shenzhen, Çin; halka açık şarj altyapısı | 1 Eylül 2022 - 28 Şubat 2023 | İstasyon veya bölgenin belirli bir zamandaki durumu | Bölge bazında doluluk ve farklı coğrafyada değerlendirme |

Bu üç veri setinin satırlarını doğrudan birleştiremeyiz. Önce oturum, şarj noktası, istasyon ve bölge düzeylerini ortak bir hedefe çevirmemiz gerekiyor.

## ACN-Data

ACN, araçların ne zaman geldiğini, ne zaman ayrıldığını ve ne kadar enerji aldığını kaydediyor. Caltech, JPL ve Office 1 sahaları var. Oturumlar JSON olarak indiriliyor; akım ve kontrol sinyali zaman serileri ayrı erişim seçeneğiyle alınabiliyor. [Resmî alan açıklamaları](https://ev.caltech.edu/dataset).

caltech için kaynak araştırmada nisan 2018 ile eylül 2021 arasında 31424 oturum var
bizim indirdiğimiz 14 çeyrek dosyasının toplamı da 31424 ve sessionID tekrar etmiyor
bu sayı elimizdeki indirmeye ait ileride kaynağın değişmeyeceği anlamına gelmiyor
[Araştırma](https://ev4eu.eu/wp-content/uploads/2025/04/2025_INESC-ID-and-PPC_Clustering-Methodologies-for-Flexibility-Characterization-of-Electric-Vehicles-Supply-Equipment.pdf)

### elimizdeki caltech verisi

| bilgi | yerelde doğrulanan değer |
|---|---|
| dosyalar | data/raw/acn/caltech_2018_Q2.json ile caltech_2021_Q3.json arası 14 dosya |
| oturum | 31424 |
| ham alan sayısı | 13 kaynak dosya adı ve 3 utc sütunuyla 17 sütun oluyor |
| farklı stationID | 55 bütün yıllarda görülen kimlikler aynı anda kurulu kapasite olarak alınmamalı |
| ilk bağlantı utc | 2018-04-25 11:08:04+00:00 |
| son bağlantı utc | 2021-09-14 01:52:37+00:00 |
| indirme filtreleri | 1 nisan 2018 00:00 ile 30 eylül 2021 23:59 utc arası çeyrekler |
| saat dilimi | ham tarihler utc takvim bilgisi America/Los_Angeles |
| eksik bağlantı veya ayrılma zamanı | 0 |
| geçersiz zaman aralığı | 0 |
| tekrar eden sessionID | 0 |
| saatlik matris | 29705 satır 55 sütun |

indirmeleri sayfanın download formuyla çeyrek çeyrek yaptık büyük dosyalar kesilebildiği için json açılmadan tamamlandı saymadık
formdan gelen _meta bitişi 23:59:00 son dakikanın bütün saniyeleri dahil diye düşünmemek gerekiyor
çeyreklerin toplamı o indirmede geniş aralık sorgusundaki 31424 sayısıyla eşleşti
ayrıntılı yöntem dosya sayıları ve tekrar indirmek için ajan promptu [yapılanlar](../yapilanlar.md) içinde

ilk ocak 2020 denemesinde 783 oturum ve 44 nokta vardı o örnek tüm veri değildi
şimdiki notebook yalnız caltech_*.json çeyreklerini okuyor eski acndata_sessions dosyaları bu seçime girmiyor

2020 de oturum sayısı çok düşüyor eylül ve ekimde kayıt yok
bu durumun kullanım değişimi mi yoksa veri eksikliği mi olduğunu henüz ayırmadık
saatlik tablodaki 0 bağlı araç kaydı bulunmadığı anlamına geliyor kesin boş etiketi olarak doğrulanmadı
noktalardaki çakışma kontrolü ve hizmet tarihleri de henüz tamamlanmadı

### Alanlar

| Alan | İçerik |
|---|---|
| `_id`, `sessionID` | Kayıt ve oturum kimlikleri |
| `siteID`, `clusterID` | Saha ve saha içindeki grup |
| `stationID`, `spaceID` | Şarj cihazı ve park yeri |
| `connectionTime` | Bağlantı zamanı |
| `disconnectTime` | Ayrılma zamanı |
| `doneChargingTime` | Son sıfırdan farklı akımın zamanı |
| `kWhDelivered` | Verilen enerji, kWh |
| `timezone` | Sahanın saat dilimi |
| `userID` | Kullanıcı kimliği; değer her oturumda dolu olmayabilir |
| `userInputs` | İç içe kullanıcı girişleri listesi |

Yerel örnekte `userInputs` içinde `WhPerMile`, `kWhRequested`, `milesRequested`, `minutesAvailable`, `modifiedAt`, `paymentRequired`, `requestedDeparture` ve `userID` alanları var. Bunları açarsak sütun veya satır sayısı değişebilir.

Doluluk için bağlantı ile ayrılma arasını kullanacağız. Şarj bittiğinde araç hâlâ park yerini işgal edebilir. Oturumun sonunda belli olan süre ve enerji, geleceği tahmin ederken giriş özelliği olarak kullanılamaz. Hava durumu hazır bir alan değil; ayrıca eşleştirmemiz gerekiyor.

## Norveç konut şarjı (Zenodo)

Ev çevresindeki şarj davranışını, yükü ve şarjın ertelenebilme potansiyelini incelemek için hazırlanmış. v2 kaydı dört CSV içeriyor. Dosyaların ayıracı noktalı virgül (`;`). Tarihler yerel CET/CEST saatinde ve yaz saati uygulaması var. [Veri kaydı](https://zenodo.org/records/13896176), [veriyi açıklayan makale](https://doi.org/10.1016/j.dib.2024.110883).

### Dosyalar ve boyutları

| Dosya | Satır | Sütun | Bir satırın anlamı |
|---|---:|---:|---|
| `Dataset1_charging_reports.csv` | 35.377 | 7 | Temizlenmiş gerçek oturum raporu |
| `Dataset2_user_predictions.csv` | 267 | 3 | Kullanıcının tahmin edilen şarj gücü ve batarya kapasitesi |
| `Dataset3_session_predictions.csv` | 34.537 | 8 | Bir oturum için hesaplanan şarj, SoC ve esneklik bilgileri |
| `Dataset4_hourly_predictions.csv` | 469.897 | 9 | Bir oturumun bir saatlik hesaplanmış enerji/SoC bilgileri |

dört dosya da data/raw altında yerelde okundu satır ve sütun sayıları doğrulandı. İkinci dosyada 267 kullanıcı satırı olsa da makaleye göre tahminler 261 kullanıcı için mevcut. Üçüncü dosya `session_id` üzerinden birinciyle eşleştiriliyor.

### Sütunlar

- Dataset 1: `location`, `user_id`, `session_id`, `plugin_time`, `plugout_time`, `connection_time`, `energy_session`. Süre saat, enerji kWh cinsinden.
- Dataset 2: `user_id`, `charging_power`, `battery_capacity`. Güç kW, kapasite kWh olarak yorumlanmalı; makaledeki kapasite birimi tablosunda kW yazması ayrıca birim kontrolü gerektiriyor.
- Dataset 3: `user_id`, `session_id`, `charging_time`, `SoC_diff`, `SoC_start`, `idle_time`, `idle_session`, `non_flex_session`. SoC şarj seviyesidir; süreler saat, enerji alanları kWh.
- Dataset 4: `user_id`, `session_id`, `date_from`, `energy_charged_i`, `energy_idle_i`, `energy_connected_i`, `SoC_diff_i`, `SoC_from_i`, `SoC_to_i`. `date_from` saatlik aralığın başlangıcıdır.

### Lokasyonların tarihleri

Makalenin ilk tablosundaki dönemler:

| Lokasyon | Başlangıç | Bitiş | Oturum |
|---|---|---|---:|
| ASK | 15 Kasım 2018 | 3 Şubat 2020 | 6.372 |
| BAR | 7 Eylül 2018 | 3 Şubat 2020 | 1.969 |
| BAR_2 | 4 Şubat 2020 | 6 Ağustos 2021 | 1.028 |
| BER | 31 Ekim 2019 | 3 Şubat 2020 | 308 |
| BOD | 24 Ekim 2018 | 2 Şubat 2020 | 508 |
| KRO | 15 Ocak 2021 | 6 Mayıs 2021 | 492 |
| OSL_1 | 8 Ekim 2019 | 2 Şubat 2020 | 464 |
| OSL_2 | 25 Kasım 2019 | 2 Şubat 2020 | 127 |
| OSL_S | 6 Şubat 2018 | 3 Şubat 2020 | 9.757 |
| OSL_T | 15 Kasım 2019 | 29 Mart 2021 | 5.478 |
| TRO | 8 Mart 2019 | 3 Şubat 2020 | 2.168 |
| TRO_R | 21 Aralık 2018 | 31 Ocak 2020 | 6.706 |

Dataset 1'de ayrı bir şarj cihazı kimliği yok. `user_id` bir kişiyi tanımlıyor; bunu doğrudan ACN'deki `stationID` yerine koyamayız. Ayrıca Dataset 2-4'teki değerler ölçüm değil, hesaplanmış tahminler. Batarya bitiş SoC'si için %95 varsayımı kullanılıyor. İlk doluluk çalışmasında bağlantı/ayrılma kayıtlarıyla başlayacağız; eksik ayrılma zamanlarını ayrıca kontrol etmeliyiz.

## UrbanEV

Shenzhen'deki halka açık şarj altyapısının doluluk, şarj süresi, enerji ve fiyat bilgilerini içeriyor. Dönem 1 Eylül 2022 - 28 Şubat 2023. Ham veri 5 dakikalık; bölge verisi 5 dakikalık ve saatlik olarak sunuluyor. Ham kapsam 1.682 istasyon ve 24.798 şarj noktası; makaledeki filtrelenmiş kapsam 275 bölge, 1.362 istasyon ve 17.532 nokta. [Makale](https://www.nature.com/articles/s41597-025-04874-4).

### Dosya yapısı ve boyutlar

urbanev dosyaları data/raw/UrbanEVDataset altında yerelde var ama modele katılmadı
aşağıdaki boyutlar kaynak açıklamalarından dosyaların tamamını tek tek sayıp doğrulamadık.

| Dosya/grup | Satır | Sütun | İçerik |
|---|---:|---:|---|
| Saatlik bölge tabloları | 4.344 zaman kaydı | 276: zaman + 275 bölge | Her değişken ayrı CSV |
| `adj.csv`, `distance.csv` | 275 | 275 sayısal değer | Bölgelerin komşuluğu ve metre cinsinden uzaklığı; indeks sütunları hariç |
| Ham istasyon CSV'leri | İstasyona göre değişiyor; eksikler var | Kaynakta 11 alan | Her istasyon için bir dosya, toplam 1.682 CSV |
| Hava durumu/konum/POI dosyaları | Dosyaya göre değişiyor | Dosyaya göre değişiyor | Başlıklar indirilen sürümden kontrol edilmeli |

Saatlik dosyalar `occupancy.csv`, `duration.csv`, `volume.csv`, `volume-11kW.csv`, `e_price.csv`, `s_price.csv`. Hava durumu sıcaklık, basınç ve nem bilgileriyle; konum, komşuluk, mesafe ve çevredeki işletmeler ise ayrı dosyalarla geliyor. Enerji, nominal güçten hesaplanıyor; doğrudan sayaç ölçümü gibi değerlendirilmemeli. [Yazarların deposu](https://github.com/IntelligentSystemsLab/UrbanEV).

Ham istasyon alanları: `time`, `busy`, `idle`, `s_price`, `e_price`, `fast_busy`, `fast_idle`, `slow_busy`, `slow_idle`, `duration`, `volume`. Fiyatlar CNY/kWh. [Dryad dosya açıklaması](https://datadryad.org/dataset/doi:10.5061/dryad.np5hqc04z).

### Sürüm seçerken dikkat

Makale ve GitHub örneğinde `occupancy.csv` doluluk oranı olarak anlatılıyor. Dryad değişiklik kaydı ise saatlik dosyanın daha sonra dolu şarj noktası sayısını verecek şekilde değiştiğini söylüyor. Dryad'ın güncel sürüm tarihi 4 Şubat 2026. Dosya adı aynı olsa da hedefin birimi değişebiliyor; hangi sürümü indirdiğimizi kaydetmeliyiz. Sayıyı orana çevirmek için ilgili bölgenin kapasitesi gerekir.

Hazır temizlenmiş veride ileri/geri doldurma ve aykırı değer düzeltmeleri var. Gelecekten bilgi kullanılıp kullanılmadığını zaman serisi değerlendirmesinde kontrol edeceğiz. Bölge doluluk oranı veya sayısını, tek noktanın `0/1` durumuyla doğrudan kıyaslamayacağız.

## İlk çalışma için seçim

caltech çeyreklerinin tamamıyla okuyucu saatlik tablo ve ilk random forest karşılaştırması yapıldı
ege tabular selman derin öğrenme tarafında aynı hedef ve zaman ayrımıyla ilerleyecek
norveç ve urbanev modele henüz katılmadı geçmeden önce hedefin neyi ölçtüğünü kontrol edeceğiz
veri olmayan saatler noktaların boş olduğunu kanıtlamaz

### doğrulama notu

caltech dosyalarının json olarak açıldığı toplam kayıt sayısı ve kimlik tekrarları yerelde kontrol edildi
notebook 12 kod hücresiyle çalıştırıldı baseline ve random forest sonuçları ilk deneme olarak tutuluyor
norveç csvlerinin dördünün boyutu da yerel dosyalardan sayıldı urbanev boyutları ise yukarıda belirtildiği gibi kaynak açıklamalarına dayanıyor
ham dosyalar ve işlenmiş csvler gitignore kapsamında githuba gönderilmiyor
kaynakların lisans şartlarının tamamı henüz ayrı ayrı doğrulanmadı
