from netCDF4 import Dataset
from wrf import get_basemap
from plots import plot_snow, plot_rain, plot_temperature, plot_height
# from test import font_test

import time
# import locale
# locale.setlocale(locale.LC_ALL,"tr_TR.utf8")

def main(wrfout='data/wrfout_d01_2020-12-07_18.nc'):

    start = time.time()

    ncfile = Dataset(str(wrfout))
    bm = get_basemap(wrfin=ncfile)

    # Görsel ekrana gösterilsin mi?
    # show_option=show, argümanları için birleştirici
    show = False # default True
    #
    # Görsel fonksiyonda belirtilmiş klasöre kaydedilsin mi?
    #    - save pathi bu dosyadan yazılabilir mi
    # save_option = default True
    save = True

    # Görselleri oluşturan fonksiyonlar plots.py dosyasının içinde
    #   Sistem hakkında planlama yapılabilir şuanda plots.py
    #   uzun fonksiyonlar içeren karmaşık bir dosya gibi
    # # # # # # # # TODO: Görsel sayısını çoğalt # # # # # # # # # # # # # #
    #
    #
    # değişkenlere erişim ve görselleştirme ayrı yapıların ürünü olabilir
    #       her görsel için ayrı scriptler kullanılabilir
    #  şuan ki sistemde devam edilip plots.py üzerinde hafifletme yapılabilir
    #


    # Kar görseli fonksiyonu
    #plot_snow(ncfile, bm, show_option=show, save_option=save, frameNo='all')

    # Yagis görseli foknsiyonu
    # contour olarak bir değişken eklenebilir (basınç, height, ..)
    plot_rain(ncfile, bm, show_option=show, save_option=save, frameNo='all')


    # 2m Sıcaklık görseli fonksiyonu
    # 2m Sıcaklık mı kontrol edilmesi gerekiyor.
    # şuanda getvar('tc'), celcius, yükseklikle
    plot_temperature(ncfile, bm, show_option=show, save_option=save, frameNo='all')

    # 500mb rüzgar görseli fonksiyonu
    #plot_height(ncfile, bm, show_option=show, save_option=save)

    end = time.time()
    print("Çalışma Süresi --> ",end - start)
    return

if __name__ == '__main__':
    main()
