# güncel bağlam

19 ekim 2026
proje şarj noktalarında bir saat sonraki saat başı doluluk tahmini
şu an yalnız acn caltech ile veri hazırlama ve ilk model karşılaştırması yapıldı

notebooks/01_veri_inceleme.ipynb 12 kod hücresiyle baştan sona çalıştırıldı
notebooks/02_selman_kontrol.ipynb bağımsız kontrol geçti
14 caltech çeyreği 31424 oturum 55 farklı nokta
bağlantı kapsamı 2018-04-25 11:08:04 UTC ile 2021-09-14 01:52:37 UTC
saatlik tablo 29705 x 55 model girdisi 29681 x 113
baseline f1 0.7332501491889546 random forest f1 0.6893289979308306
45 aktif test noktasında baseline 32 RF 2 eşit 11
sıfır kayıt kesin boş demek değil noktaların hizmet dönemleri belirsiz
oturum çakışma kontrolü src okuyucu özel örnek testleri validation tatil hava durumu henüz yok

norveç ve urbanev sonraki aşama
klasörde duruyorlar ama yapılar farklı tek tabloya eklenmiyor
norveçte şarj noktası kimliği yok urbanev bölge ve istasyon düzeyinde
önce her kaynak için tahmin hedefini ayrı netleştirip aynı doluluk hedefini ne kadar kurabileceğimize bakacağız
bunu görmeden aynı modeli aynen kullanırız demiyoruz
ayrıntı ROADMAP.md çoklu veri seti stratejisi ve 7 hafta maddelerinde

ROADMAP.md tamamlananlarla kalanları ayrı kutularda tutuyor
yapilanlar.md indirme yöntemi ajan promptu veri hazırlama sonuçlar ve devam işleri
ege.md selman.md ayrı gelecek görevler
notbook ve notlar küçük harf gündelik az noktalama açıklamalarda ters tırnak yok
görev dosyaları düz paragraflar

ham dosyalar ve işlenmiş csvler gitignore kapsamında
requirements uyz ortamıyla kullanılıyor
selman sıradaki iş kapsama 2020 sonra takvim open-meteo eda
kaynak ayrıntılar yapilanlar.md data/VERI_SETLERI.md ve notebook içinde
