18 ekim 2026

şu ana kadar caltech verisini indirip birleştirdim saatlik doluluk çıkardım ve ilk random forest denemesini yaptım
kodlar notebooks/01_veri_inceleme.ipynb içinde hücrelerin üstüne ne yaptığımı yazdım

ilk başta ocak 2020 dosyasıyla uğraşıyordum 783 oturum ve 44 nokta vardı
dosya okuma tarih çevirme ve doluluk hesabını onun üzerinde denedim
sonra örnek dosyayı bırakıp elimizdeki bütün caltech çeyreklerini kullanmaya geçtim
şu an notebook eski örnek dosyayı okumuyor caltech_*.json dosyalarını okuyor

ortam için .venv açtım pandas matplotlib jupyter kurdum model için sonradan scikit-learn ekledim
jupyter içinde python ev doluluk kernelini kullanıyorum
requirements.txt ortamda kullandığım paketleri tutuyor notebooks src tests klasörleri var
src ve tests şu an boş okuyucu henüz ayrı python dosyasına taşınmadı

veriyi nasıl indirdik

ev.caltech.edu/dataset sayfasında site caltech seçildi
from ve to tarihleriyle önce geniş aralık denendi sayfa 31424 oturum gösterdi
ama tek seferde inen büyük jsonlar yarıda kesildi adını değiştirmek dosyayı düzeltmedi
json olarak açılmayan dosyaları tam veri saymadık

sonra çeyrek çeyrek indirdik
2018 q2 ile başladık 2021 q3 e kadar 14 dosya var
2018 q1 ve 2021 q4 sayfada 0 kayıt gösterdiği için onlar için dosya yok
minimum energy alanını boş bıraktık enerjiye göre kayıt elemedik
from çeyreğin ilk günü 12:00 am to son günü 11:59 pm olacak şekilde seçildi
meta içindeki saatler utc olarak geldi son sınır 23:59:00 yazıyor bunu son dakikanın bütün saniyeleri dahil diye düşünmemek gerekiyor

ilk 2018 q2 dosyasını tarayıcıdaki download düğmesinden indirdim
kalanları claude aldı sayfayı yerleşik tarayıcıda açıp tarih biçimini ve sessions found sayılarını okudu
indirme işlemini ise aynı download formunun isteğini komut satırından göndererek yaptı
bütün dosyalara tarayıcıdan tek tek tıklamadı
ilk q2 dosyasını bizim indirdiğimiz dosyayla bayt bayt karşılaştırıp aynı olduğunu bildirdi
bu yöntem indirme sırasında kullanılan yöntem aynı sayfanın formu kullanıldı
formun adresini ve alan adlarını tahmin etmek yerine sayfadan okumak gerekiyor

2018 q4 ve 2019 q2 q3 q4 ilk denemede kesik gelmiş onları geçerli json gelene kadar yeniden indirdi
sonunda her dosyayı json olarak açtı _meta tarihlerini ve kayıt sayılarını kontrol etti
her çeyreğin sayısı sayfadaki sessions found ile aynı çıktı
ben de proje içindeki 14 dosyayı yeniden okuyup toplam 31424 farklı sessionID olduğunu kontrol ettim
bu sayı elimizdeki sorguların sonucu acn verisinin gelecekte de aynı kalacağını göstermiyor

dosyalar data/raw/acn içinde
caltech_2018_Q2.json 3880 oturum
caltech_2018_Q3.json 6793 oturum
caltech_2018_Q4.json 4624 oturum
caltech_2019_Q1.json 2876 oturum
caltech_2019_Q2.json 2884 oturum
caltech_2019_Q3.json 2508 oturum
caltech_2019_Q4.json 2349 oturum
caltech_2020_Q1.json 2051 oturum
caltech_2020_Q2.json 81 oturum
caltech_2020_Q3.json 71 oturum
caltech_2020_Q4.json 269 oturum
caltech_2021_Q1.json 614 oturum
caltech_2021_Q2.json 1085 oturum
caltech_2021_Q3.json 1339 oturum

aynı veriyi tekrar alacak olsam yine çeyrek çeyrek aynı formdan alırdım
tek büyük indirmeye güvenmek yerine her dosyanın açıldığını ve sayacın tuttuğunu kontrol ederdim
form değişmişse önce yeni alanları okurdum eksik jsonun sonuna parantez ekleyip tam veri diye kullanmazdım
ham dosyalar ve üretilen csvler gitignore içinde githuba gitmiyor
repoyu indiren kişinin bu dosyaları ayrıca alması gerekiyor

claude veya başka bir tarayıcı ajanına verilebilecek prompt

açık olan ev.caltech.edu/dataset sayfasındaki caltech verisini proje için indir
2018 ikinci çeyrekten 2021 üçüncü çeyreğe kadar her çeyreği ayrı al
sayfadaki tarih biçimini formun gerçek alanlarını ve download isteğini incele
from ilk gün 12:00 am to son gün 11:59 pm olsun minimum energy boş kalsın
sayfanın gerçek download formunu kullanarak komut satırından da indirebilirsin
istek adresi veya alan adı uydurma tarihleri ve saat dilimini _meta üzerinden kontrol et
her çeyrek için sessions found sayısını not et inen jsondaki _items sayısıyla karşılaştır
json kesikse yeniden indir eksik dosyanın sonunu kapatıp tamamlandı sayma
0 kayıt görünen dönemleri dosya uydurmadan not et
başka indirmelerden gelen tekrarları toplamda sessionID ile kontrol et
çeyreklerin bitişi _meta içinde 23:59:00 olabilir sınırdaki son dakikayı not et ve toplamı geniş aralık sorgusuyla karşılaştır
klasörde dosya varsa önce doğrula sağlam olanın üstüne yazma
sağlam dosyaları data/raw/acn altında caltech_2018_Q2.json gibi adlandır
her dosyanın oturum sayısını tarih filtresini ilk ve son bağlantısını kısa bir raporla yaz
kodları ve git geçmişini değiştirme commit veya push yapma

verileri birleştirme ve kontroller

14 dosyanın oturumlarını aynı listeye aldım sonra pandas tablosu yaptım
hangi dosyadan geldiği belli olsun diye _source_file alanı ekledim
ham kayıtlarda 13 alan var kaynak dosya alanıyla 14 sütun oluyor
3 utc tarih sütunu eklenince tablo 31424 satır 17 sütun oluyor

bağlantı ayrılma ve şarj bitişini tarih saat olarak çevirdim
bağlantı ve ayrılmada eksik veya okunamayan zaman 0 hatalı aralık 0 tekrar eden sessionID 0 çıktı
55 farklı stationID var bu bütün yıllarda görülen noktaların sayısı
hepsinin aynı tarihte hizmette olduğunu veya sahanın kapasitesinin 55 olduğunu söylemiyorum
aynı noktadaki çakışmaları ayrıca kontrol eden kod henüz yok

ilk bağlantı 25 nisan 2018 11:08:04 utc
son bağlantı 14 eylül 2021 01:52:37 utc
birleştirilmiş oturumlar data/processed/caltech_all_sessions.csv olarak kaydediliyor
bu csv saatlik matris değil oturum tablosu

saatlik tablo

bağlantı ile ayrılma arasındaki saat başlarını dolu saydım
18:10 da gelip 21:05 te ayrılan araç için 19 20 ve 21 saatleri dolu oluyor
şarjın bittiği anı ayrılma saymadım araç bağlı kalabilir
aynı saat ve noktaya birkaç kayıt gelirse max ile 1 bıraktım bu çakışma kontrolünün yerini tutmuyor

ilk saat 25 nisan 2018 11:00 utc son saat 14 eylül 2021 03:00 utc
matris 29705 satır ve 55 sütun
19791 saatte en az bir dolu nokta kaydı var
kayıt olmayan hücreler 0 ama veri eksikse bunlar gerçek boşlukla karışabilir
saatlik matris şu an notebook içinde üretiliyor ayrıca csv olarak kaydedilmedi

aylık tablolarda 2020 de oturumların çok azaldığını gördüm eylül ve ekimde hiç oturum yok
bunu kesin pandemi etkisi veya kesin veri hatası diye yazmadım ikisini ayıracak bilgi henüz yok
norveçteki 4 csv de yerelde var boyutları 35377 x 7 267 x 3 34537 x 8 ve 469897 x 9
urbanev dosyaları da data/raw/UrbanEVDataset içinde duruyor
bu iki kaynağı modele katmadım norveçte kullanıcı kimliği şarj noktası kimliği yerine geçmiyor

ilk model

yerel saat haftanın günü hafta sonu önceki saat ve 24 saat önceki doluluğu giriş yaptım
oturum sonunda belli olan enerji ve toplam süreyi modele vermedim
24 saat geriye bakmak için ilk 24 satırı çıkardım
model girdisi 29681 satır 113 sütun hedef 29681 satır 55 sütun

eğitim 26 nisan 2018 11:00 utc ile 9 ocak 2021 18:00 utc arasında
test 9 ocak 2021 19:00 utc ile 14 eylül 2021 03:00 utc arasında
ilk yüzde 80 eğitim son yüzde 20 test sıralamayı karıştırmadım
ayrı doğrulama bölümü henüz yok

her nokta için random forest eğittim 30 ağaç en fazla 12 seviye yaprakta en az 5 satır
class_weight balanced_subsample random_state 42 kullandım
bir de önceki saat neyse sonraki saat de odur diyen baseline yaptım

baseline accuracy 0,9849 precision 0,7333 recall 0,7332 f1 0,7333
random forest accuracy 0,9807 precision 0,6314 recall 0,7590 f1 0,6893
random forest daha fazla dolu saat buldu ama yanlış dolu tahminleri de arttı
bu denemede baseline daha iyi çıktı

sonuçları ay ay ve her nokta için ayrı hesapladım
testte dolu saat görülen 45 noktanın 32 sinde baseline iyi 2 sinde random forest iyi 11 inde eşit
hiç dolu saat görülmeyen 10 noktayı bu f1 kazanma sayısına katmadım
sadece birkaç dolu saati olan noktalarda skora fazla anlam yüklememek gerekiyor
aylık model sonuçları utc ayına göre oturum özeti los angeles ayına göre hesaplanıyor
ocak ve eylül testte tam ay değil

notebook baştan sona temiz kernelde çalıştırıldı 12 kod hücresinde hata çıkmadı
veri boyutları zaman hizası ve f1 değerleri önceki çalıştırmayla aynı kaldı

buradan sonra

önce veri okuyucusunu src içine almak gerekiyor notebooktan bağımsız çalışabilsin
çakışan oturumları ve eksik kimlikleri ayrıca kontrol edeceğiz
saat başında bağlanma ayrılma gece yarısı ve hatalı kayıt örnekleriyle küçük testler yazacağız

sonra eğitimden ayrı doğrulama aralığı ayıracağız
model ayarlarını yeni özellikleri ve eşikleri doğrulama kısmında seçeceğiz
şu anki teste birkaç kez baktık bunlar ilk deneme sonuçları tamamen dokunulmamış final test gibi yazmayacağız
önceki haftanın doluluğu ve geçmiş birkaç saatin ortalaması denenebilir

selman hava durumu tatil ve takvim tarafını tamamlayacak eda grafiklerini ekleyecek
ege tabular modelleri ilerletecek xgboost catboost ve daha basit modeller de aynı ayrımla denenecek
selman bilstm hazırlayacak sonra aynı hedefle hibrit tarafını beraber deneyeceğiz
norveç ve urbanev için önce hedefin anlamı uyuyor mu bakılacak
raporda başarının yanında veri boşluklarını hizmet dönemi belirsizliğini ve baseline ın daha iyi çıktığını da yazacağız
