ilk iş egenin notebookta çıkardığı oturum tablosunu ve saatlik doluluk matrisini bağımsız olarak kontrol etmek 31424 oturum ve 55 nokta sayısını kendi okumanla tekrar bulmak birkaç oturumu ham json ile elle karşılaştırıp dolu saatlerin doğru yazıldığına bakmak

her noktanın gözlenen ilk ve son kaydını ve uzun kayıt boşluklarını çıkarmak bunlar gerçek hizmet başlangıcı ve bitişini tek başına vermiyor kaynakta kurulum veya kapanış bilgisi varsa onu da kontrol etmek gerekiyor şu an kayıt olmayan hücreler 0 nokta o sırada çalışmıyor da olabilir dönemleri çıkarmadan veya ayrı işaretlemeden önce bu belirsizliği egeyle kararlaştırmak lazım

kapsama kontrolü yapmak özellikle 2020 de oturumlar çok düşüyor eylül ve ekimde hiç oturum yok bunun kullanım azalması mı yoksa kayıt eksiği mi olduğunu kaynak notlarından ve verinin kendisinden anlamaya çalışmak sonucu egeyle paylaşıp bölme sınırlarını buna göre konuşmak

open meteo üzerinden caltech sahası için saatlik geçmiş hava durumu çekmek sıcaklık yağış gibi alanlar yeterli zamanları utc olarak tutup doluluk tablosunun saatleriyle eşleştirmek tahmin anında bilinmeyecek bilgileri vermemek için bir saat sonrasının gerçek hava durumunu değil o ana kadar bilinen değeri kullanmak gerekiyor

takvim özelliklerini genişletmek şu an yerel saat gün ve hafta sonu var buna abd ve kaliforniya resmi tatillerini caltech akademik takvimini yani dönem arası ve tatil haftalarını eklemek hepsi los angeles yerel tarihine göre çıkarılacak

eda çizimlerini hazırlamak saate ve haftanın gününe göre ortalama doluluk aylara göre oturum sayısı noktalar arası doluluk farkı oturum süresi dağılımı ve hava durumu ile doluluk ilişkisi bunlar sıfır kayıtlı ve hizmet dışı dönemler ayrılarak çizilsin

bilstm modelini pytorch ile kurmak egeyle aynı hedefi yani bir saat sonraki saat başında doluluğu ve aynı kronolojik eğitim validation test sınırlarını kullanmak ölçekleme yalnız eğitim kısmından öğrenilecek validation ve teste aynı ölçek uygulanacak

bilstm için zaman pencerelerini hazırlamak her örnek yalnız tahmin saatinden önceki saatleri görsün pencere uzunluğunu mesela 24 ve 168 saat gibi değerlerle validationda denemek test kısmına ayar yaparken bakmamak sonuçları egenin baseline ve tabular sonuçlarıyla aynı metriklerle karşılaştırmak

bilstm iyi çalıştıktan sonra hibrit model için aynı saatler ve noktalar için olasılık çıktılarını kaydetmek egenin tabular çıktılarıyla birleştirme ve değerlendirmeyi beraber yapacağız

en sonda ortak rapor için veri temizleme hava durumu takvim ve eda bölümlerini yazmak bilstm ve hibrit sonuçlarını hata incelemesi doluluk eğrileri ve konfüzyon matrisleriyle eklemek
