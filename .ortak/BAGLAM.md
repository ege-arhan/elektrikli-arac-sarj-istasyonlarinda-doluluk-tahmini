# güncel bağlam

20 ekim 2026
proje şarj noktalarında bir saat sonraki saat başı doluluk tahmini
şu an yalnız acn caltech ile ilerliyoruz 2 hafta maddeleri kapatildi

notebooks/01_veri_inceleme.ipynb ilk model
notebooks/02_selman_kontrol.ipynb bagimsiz kontrol
notebooks/03_kapsama_2020.ipynb nokta kapsami ve 2020 sifir aylari
notebooks/04_eda_grafikleri.ipynb eda grafikleri
src/load_data.py oturum okuma saatlik matris kalite ve cakisma raporu
tests occupancy calendar weather 11 test gecti
src/features/calendar.py ve weather.py hazir

14 caltech ceyregi 31424 oturum 55 nokta saatlik 29705 x 55
eksik id 0 cakisan oturum cifti 0
baseline f1 ~0.733 random forest f1 ~0.689

0 etiketi gecici karar
kayit olmayan saatler simdilik 0 bos kaliyor
kapsama notu var maskeleme validation ayrimiyla egeyle netlestirilecek
2020-09 ve 2020-10 tamamen bos ~107 gunluk kesinti var

norvec ve urbanev sonraki asama ayri hedef
lisans ozeti data/VERI_SETLERI.md icinde

3 hafta
takvim/tatil src/features/calendar.py
open-meteo src/features/weather.py + data/processed/caltech_weather_hourly.csv
join_weather shift_hours=1 varsayilan
tum birim testler gecti
sirada egeyle validation tarihleri
