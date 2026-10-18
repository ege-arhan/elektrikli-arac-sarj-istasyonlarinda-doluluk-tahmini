ilk iş notebooktaki okuma kısmını src/load_data.py içine almak 14 caltech json dosyasını okuyup oturum tablosunu döndüren bir fonksiyon olsun notebook da bunu çağırsın böylece selman ve sonraki modeller aynı tabloyu kullanır saatlik doluluk matrisini çıkaran kısım da ayrı bir fonksiyon olarak buraya gelebilir

okuyucuya kalite kontrolleri eklemek gerekiyor şimdilik eksik tarih hatalı aralık ve tekrar eden oturuma bakıyoruz ama aynı noktada zamanı çakışan oturumlara hiç bakmadık matriste max ile üstünü örtüyoruz çakışan oturumları sayıp raporlamak ve ne yapacağımıza karar vermek lazım

tests klasörüne küçük elle yazılmış örneklerle testler yazmak normal bir oturum gece yarısını aşan oturum tam saat başında bağlanıp ayrılan oturum saat başını hiç geçmeyen kısa oturum ve hatalı zamanlı oturum için beklenen dolu saatler doğru çıkıyor mu bakılacak yaz saati geçişine denk gelen bir örnek de eklenebilir

şu anki yüzde 80 eğitim yüzde 20 test bölmesini kronolojik eğitim validation test olarak yeniden ayırmak tarih sınırlarını selmanla birlikte belirleyip bir yere yazalım ikimiz de aynı sınırları ve aynı hedefi yani bir saat sonraki saat başında nokta dolu mu boş mu kullanalım test kısmına ayar yaparken bakmayacağız

yeni özellikleri yalnız validation sonucuna bakarak denemek önce lag168 yani 168 saat önceki doluluk sonra son birkaç saatin rolling ortalaması gibi özellikler eklenip önceki saat baseline ile karşılaştırılacak rolling hesaplarken yalnız geçmiş saatlerin kullanıldığından emin olmak lazım

önceki haftayı kullanan ayrı bir basit tahmin eklemek yaz saati geçişinde 168 saatin yerel aynı saat olmayabileceğini kontrol etmek baseline sadece önceki saat değil bu da olsun lojistik regresyon ve basit karar ağacı da aynı bölmede karşılaştırmaya girsin

random forest ayarlarını validation üzerinde yeniden denemek ardından xgboost ve catboost eğitmek hepsi aynı özellikler aynı bölme ve aynı f1 precision recall accuracy hesabıyla karşılaştırılacak sınıf dengesizliği için eşik ayarı da validationda denenebilir

tabular modellerde iyi giden ayarlar için optuna ile hiperparametre araması yapmak arama yalnız validation skoruna bakacak en son seçilen model bir kere testte ölçülecek

hibrit model için tabular tarafın çıktısını hazırlamak selmanın bilstm çıktısıyla birleştirilebilecek şekilde aynı saatler ve aynı noktalar için olasılıkları kaydetmek birleştirmeyi ve değerlendirmeyi beraber yapacağız

urbanev ile başka bölgede test için doluluk tanımı ve zaman çözünürlüğü uyuşuyorsa tabular modeli orada denemek uyuşmuyorsa raporda nedenini yazmak

en sonda selmanla ortak rapor için tabular modellerin sonuç tablosunu nokta ve ay bazlı karşılaştırmaları ve hata incelemesini hazırlamak
