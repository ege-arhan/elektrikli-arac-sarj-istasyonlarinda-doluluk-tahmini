# proje yol haritası

19 ekim 2026 durumu

şu an yalnız acn caltech ile ilerliyoruz
14 çeyrek dosyada 31424 oturum 55 şarj noktası saatlik tablo 29705 x 55
veri hazırlama ve ilk model karşılaştırması notebooks/01_veri_inceleme.ipynb içinde yapıldı
selman bağımsız kontrolü notebooks/02_selman_kontrol.ipynb ile tekrarladı sayılar uyumlu

hedef bir şarj noktasının bir sonraki saat başında dolu olup olmayacağını tahmin etmek
aracın bağlı kaldığı zamanı connectionTime ile disconnectTime arasından alıyoruz
doneChargingTime şarjın bittiği an araç o sırada hala bağlı olabilir

saatleri utc olarak tutuyoruz takvim bilgilerini los angeles saatine göre çıkarıyoruz
şimdilik bağlı araç kaydı olmayan hücreleri 0 yaptık ama bunun kesin boş anlamına geldiğini doğrulamadık
2020 deki kayıt boşlukları ve noktaların hangi tarihlerde hizmette olduğu ayrıca incelenecek

ilk denemede önceki saatin durumunu koruyan yöntem random foresttan daha iyi çıktı
baseline f1 yaklaşık 0,733 random forest f1 yaklaşık 0,689
bu sonuçlar ilk deneme sonuçları test kısmına birkaç kez baktığımız için yeni ayarları oraya göre seçmeyeceğiz

çoklu veri seti stratejisi

norveç ve urbanev dosyaları klasörde duruyor ama ilk modele katılmadı
yapıları acn ile aynı değil hepsini tek tabloya birleştiremeyiz

norveçte şarj noktası kimliği yok kullanıcı kimliği var bunu stationID yerine koymayacağız
urbanev bölge ve istasyon düzeyinde zaman serisi içeriyor nokta bazlı 0/1 oturum tablosu değil

sonraki aşamada her kaynak için önce neyi tahmin edeceğimizi ayrı netleştireceğiz
ayrı hazırlayıp aynı doluluk hedefini ne kadar kurabildiğimize bakacağız
uygun olanlarda yöntemi deneyip karşılaştıracağız
hedef uyumunu görmeden aynı modeli aynen kullanırız demiyoruz
farklı hedefleri aynı skor tablosuna koymayacağız

iş bölümü

ege arhan yıldızalkan 241230013 veri hattı saatlik dönüşüm ve tabular modellerle ilgileniyor
random forest xgboost catboost tarafı ege de

mahmud selman şahin 241230008 hava durumu takvim veri kontrolü eda ve derin öğrenmeyle ilgileniyor
bilstm tarafı selman da

hibrit modeli sonuç karşılaştırmasını ve raporu birlikte yapacağız
sonraki kişisel işler ege.md ve selman.md içinde yapılanların ayrıntısı yapilanlar.md içinde

## 1 hafta 6 - 12 ekim

- [x] repo ve veri klasörleri açıldı

ortam kurulumu veri indirme ve okuyucu ikinci haftada yapıldı aşağıdaki kutular onların güncel durumu

## 2 hafta 13 - 19 ekim

- [x] sanal ortam kuruldu pandas matplotlib jupyter ve scikit-learn çalışıyor requirements dosyası var
- [x] notebooks src ve tests klasörleri yerelde açıldı src ve tests şu an boş
- [x] ocak 2020 örneğiyle ilk dosya okuma ve doluluk hesabı denendi
- [x] caltech verisi 14 çeyrek dosyası olarak indirildi jsonlar açıldı toplam 31424 kayıt doğrulandı
- [x] norveç csvlerinin alanları ve boyutları incelendi urbanev dosyaları yerelde duruyor
- [x] bütün caltech dosyalarını birleştiren okuyucu notebook içinde yazıldı kaynak dosya adı kayıtlara eklendi
- [x] tarihler utc ye çevrildi eksik tarih hatalı zaman aralığı ve tekrar eden oturum sayıldı hepsi 0 çıktı
- [x] 29705 saat ve 55 noktadan oluşan doluluk tablosu üretildi
- [x] yerel saat haftanın günü hafta sonu ve önceki 1 ile 24 saatin doluluğu eklendi
- [x] aylık oturum ve dolu saat tabloları çıkarıldı 2020 deki düşüş görüldü
- [x] notebook sadeleştirildi hücrelerin üstüne açıklama yazıldı 12 kod hücresi baştan sona çalıştırıldı
- [ ] okuyucuyu src/load_data.py içine alıp notebook dışından da çalıştıracağız
- [ ] eksik stationID siteID sessionID alanlarını ve aynı noktadaki çakışan oturumları ayrıca kontrol edeceğiz
- [ ] normal gece yarısını aşan saat başında biten ve hatalı oturumlar için küçük testler yazacağız
- [ ] veri boşluklarıyla noktaların hizmette olduğu dönemleri inceleyip 0 etiketinin nasıl yorumlanacağını netleştireceğiz
- [ ] eda grafiklerini ekleyeceğiz tablolar hazır ama grafik kısmı henüz yok
- [ ] kaynakların lisans ve atıf bilgilerini tamamlayacağız

## 3 hafta 20 - 26 ekim

- [x] ilk deneme için sıralamayı bozmadan yüzde 80 eğitim yüzde 20 test ayrıldı bu iş ikinci haftada yapıldı
- [ ] yeni denemeler için eğitim döneminden ayrı doğrulama bölümü ayırıp ortak tarih sınırlarını belirleyeceğiz
- [ ] selman geçmiş hava durumunu open-meteo üzerinden alacak
- [ ] selman yerel takvim ve tatil bilgisini ekleyecek saat gün hafta sonu şu an var tatil henüz yok
- [ ] hava durumunu saha ve zaman üzerinden eşleştireceğiz tahmin anında hangi bilgilerin bilinebileceğini kontrol edeceğiz
- [ ] oturum sonunda belli olan enerji ve toplam süreyi giriş özelliği yapmayacağız ölçekleme gerekirse yalnız eğitimden öğreneceğiz

## 4 hafta 27 ekim - 2 kasım

- [x] önceki saatin durumunu kullanan baseline denendi bu iş ikinci haftada yapıldı
- [x] ege ilk random forest modelini bütün dönem üzerinde eğitti
- [x] accuracy precision recall ve f1 aynı testte hesaplandı ay ve nokta bazında karşılaştırıldı
- [x] testte dolu saat görülen 45 noktada baseline 32 random forest 2 noktada daha iyi çıktı 11 noktada eşit kaldı
- [ ] önceki haftanın aynı saatini kullanan baseline ve lojistik regresyon ile karar ağacını deneyeceğiz
- [ ] ege önceki haftanın doluluğu ve geçmiş birkaç saatin ortalaması gibi özellikleri doğrulama bölümünde deneyecek
- [ ] ege random forest xgboost ve catboost modellerini aynı hedef ve zaman ayrımıyla karşılaştıracak
- [ ] tahmin eşiği ve model ayarları doğrulama verisiyle seçilecek test sonucu ilk deneme olarak ayrıca kaydedilecek
- [ ] dolu nokta sayısı veya oranı için ayrı regresyon yaparsak mae ve rmse kullanacağız

## 5 hafta 3 - 9 kasım

- [ ] yöntem ve veri hazırlama kısmını ara rapora yazacağız
- [ ] ilk karşılaştırmayı ve veriyle ilgili sınırlamaları rapora ekleyeceğiz

## 6 hafta 10 - 16 kasım

- [ ] selman pytorch ile bilstm modelini hazırlayacak
- [ ] ege ve selman aynı hedef zaman ayrımı ve tahmin ufkuyla modelleri karşılaştıracak
- [ ] tabular ve derin öğrenme tarafını birleştiren hibrit modeli birlikte deneyeceğiz

## 7 hafta 17 - 23 kasım

- [ ] norveç ve urbanev verisinin bizim hedefle ne kadar uyuştuğunu kontrol edeceğiz kullanıcıyı şarj noktası gibi kullanmayacağız
- [ ] uygunsa başka saha ve bölgede deneyeceğiz farklı hedefleri aynı skor tablosuna koymayacağız
- [ ] optuna denemelerini eğitim ve doğrulama üzerinde yapacağız
- [ ] bölge ve döneme uygun elektrik fiyatı bulunursa eklemeyi değerlendireceğiz bulunmazsa raporda yazacağız

## 8 hafta 24 - 30 kasım

- [ ] hatalı tahminleri doluluk grafikleri ve karışıklık matrisiyle inceleyeceğiz
- [ ] sonuçları ve final raporunun taslağını hazırlayacağız

## 9 hafta ve final aralık

- [ ] kodu düzenleyip eksik testleri tamamlayacağız
- [ ] son raporu ve sunumu hazırlayacağız
