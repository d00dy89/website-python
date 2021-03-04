from wrf import (getvar, extract_times, ALL_TIMES, latlon_coords, to_np, smooth2d, interplevel)
from pandas import to_datetime
from datetime import timedelta
from cmaps import snow_cmap, rain_cmap, temperature_cmap, wind_cmap, draw_map, draw_iller

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import locale

### yazı fontu belirleme
# from matplotlib import rcParams
# rcParams['font.family'] = 'Fira Sans Condensed'

def plot_temperature(ncfile, basemap, show_option=True, save_option=True, frameNo='all'):
    r''' ### doc string ###
    # # TODO: ingilizce ve türkçe gün isimlerini aynı süreçte almak
    # Gün ismi için locale belirle, sistemde yüklü olması gerekiyor!
    # locale.setlocale(locale.LC_ALL,"us_US.utf8")
    # en_day = prehour.strftime("%A")
    # locale.setlocale(locale.LC_ALL,"tr_TR.utf8")
    # tr_day = prehour.strftime("%A")
    # day = tr_day+"/"+en_day
    #
    # şuan sadece türkçe
    '''
    locale.setlocale(locale.LC_ALL,"tr_TR.utf8")

    for i in range(1, 41):
        if frameNo != 'all':
            if i != frameNo:
                continue
                
        # -- -- #
        time = extract_times(ncfile, timeidx=i)
        temp = smooth2d(getvar(ncfile, 'tc', timeidx=i)[0,:,:], 4, cenweight=5)
        slp = getvar(ncfile, 'slp', units='mb', timeidx=i)
        sslp = smooth2d(slp, 8, cenweight=10)
        # -- -- #
        lats, lons = latlon_coords(slp)

        x, y = basemap(to_np(lons), to_np(lats))

        # Veriden alınan UTC cinsinden saatler
        utc_time = to_datetime(time)
        # Yerel saat UTC+3
        local_time = utc_time + timedelta(hours=3)
        # arkadan gelen saat
        prehour = local_time - timedelta(hours=1)

        # Gün, saat ve tarih formatında stringler
        day = prehour.strftime("%A")
        hour = prehour.strftime("%H:00-")+local_time.strftime("%H:00")+" UTC+3"
        date = local_time.strftime("%d/%m/%Y")

        # save_time = local_time.strftime("%Y-%m-%d_%H")

        fig, ax = plt.subplots(1,1, figsize=(12,12))

        # plotta index no yazsın - silinecek
        plt.text(x=.02, y=-.05, s="#:"+str(i), fontsize=14, transform=ax.transAxes)
        # Başlıkta gözükecek textler

        # Sol ilk satır başlığı
        plt.text(s='Deniz Seviyesi Basıncı (mb), 10m Rüzgar (m/s)',
                 x=.0002, y=1.05, fontsize=18, transform=ax.transAxes)

        # Sol alt satır
        plt.text(s='SLP, Winds and Temperature',
                 x=.05, y=1.01, fontsize=14, transform=ax.transAxes)

        # Saat ve Tarih başlığı
        plt.text(.72, 1.05, s=hour, fontsize=16, transform=ax.transAxes)
        # Türkçe olarak gün başlığı
        plt.text(.79, 1.012, s=day+"-"+date, fontsize=14, transform=ax.transAxes)

        draw_map(basemap, shaded=False)
        draw_iller(basemap)

        # Yüzey basınç contourları,
        C = basemap.contour(x, y, to_np(sslp), colors='black')
        # contour label
        plt.clabel(C, fontsize=12, inline=True, inline_spacing=2.5, fmt="%i")

        bounds, norm, cmap = temperature_cmap()

        # -- # TODO: Max-mix sıcaklığa göre değişen bir colorbar yapılabilir
             # ##### veya renk aralıkları sıklaştırılıp ton atanabilir.
        CF = basemap.contourf(x, y, to_np(temp), bounds, norm=norm, cmap=cmap,
                             extend='both', alpha=.9)
        temp_cbar = plt.colorbar(CF, orientation='horizontal', ticks=bounds,
                                 shrink=.77, pad=.04, format='%.1f')

        temp_cbar.ax.set_xlabel('2m Sıcaklık ($^{\degree}$C)', fontsize=10)
        temp_cbar.ax.tick_params(labelsize=9.5)
        # u10 = getvar(ncfile, 'U10', timeidx=i)
        # v10 = getvar(ncfile, 'V10', timeidx=i)
        #
        # # wi = 12
        # # B = basemap.barbs(x[::wi, ::wi], y[::wi, ::wi],
        # #              u10[::wi, ::wi], v10[::wi, ::wi],
        # #              pivot='middle', alpha=.8)
        if show_option:
            plt.show()
        if save_option:
            # Save ismi ve lokasyonu serverda düzenlenmeli
            print("sicaklik_"+str(i)+".jpg --- Kaydedildi.")
            plt.savefig("gorseller/sicaklik/sicaklik_"+str(i)+".jpg",)
        plt.close(fig)
    return

def plot_rain(ncfile, basemap, show_option=True, save_option=True, frameNo='all'):
    r''' ### doc string ###
        ...
    '''
    locale.setlocale(locale.LC_ALL,"tr_TR.utf8")

    rainc = getvar(ncfile, 'RAINC', timeidx=ALL_TIMES)
    rainnc = getvar(ncfile, 'RAINNC', timeidx=ALL_TIMES)

    lats, lons = latlon_coords(rainc)

    times = extract_times(ncfile, ALL_TIMES)

    for i in range(1, 41):
        if frameNo != 'all':
            if i != frameNo:
                continue

        time = extract_times(ncfile, timeidx=i)
        # if i == 0:
        #  rainsum = rainc[i,:,:] + rainnc[i,:,:]
        # else: indent
        rainsum = (rainc[i,:,:]-rainc[i-1,:,:]) + (rainnc[i,:,:]-rainnc[i-1,:,:])

        rain = to_np(rainsum)*10 # mm to cm

        # Veriden alınan UTC cinsinden saatler
        utc_time = to_datetime(time)
        # Yerel saat UTC+3
        local_time = utc_time + timedelta(hours=3)
        # arkadan gelen saat
        prehour = local_time - timedelta(hours=1)
        # Gün, saat ve tarih formatında stringler
        day = prehour.strftime("%A")
        hour = prehour.strftime("%H:00-")+local_time.strftime("%H:00")
        date = local_time.strftime("%d/%m/%Y")

        # save_time = local_time.strftime("%Y-%m-%d_%H")

        fig, ax = plt.subplots(1,1, figsize=(12,12))

        # Başlıkta gözükecek textler
        plt.text(x=.2, y=-.5, s="frame:"+str(i))
        plt.text(.0002, 1.05, 'Toplam Yagis (cm)', fontsize=18, transform=ax.transAxes)
        plt.text(.001, 1.01, 'Total Precipitation', fontsize=14, transform=ax.transAxes)
        plt.text(.72, 1.05, s=day+"  "+hour, fontsize=16, transform=ax.transAxes)
        plt.text(.75, 1.015, s=date, fontsize=14, transform=ax.transAxes)

        # cmaps.py betiğinden gelen arka plan haritası özellikleri
        draw_map(basemap, shaded=True)
        draw_iller(basemap)

        x, y = basemap(to_np(lons), to_np(lats))

        # cmaps.py betiğindeki, rain_cmap()
        levels, norm, cmap = rain_cmap()
        # Contour fill
        CF = basemap.contourf(x, y, rain, levels,  norm=norm, cmap=cmap, extend='max')
        rain_cbar = plt.colorbar(CF, orientation='horizontal', ticks=levels,
                                 shrink=.77, pad=.04, format='%.1f')
        # rain_cbar.ax.set_ylabel('(mm)', rotation=-90)

        u10 = to_np(getvar(ncfile, 'U10', timeidx=i))
        v10 = to_np(getvar(ncfile, 'V10', timeidx=i))
        wi = 12

        barb = basemap.barbs(x[::wi, ::wi], y[::wi, ::wi],
                             u10[::wi, ::wi], v10[::wi, ::wi],
                             pivot='middle', alpha=.7)

        if show_option:
            plt.show()
        if save_option:
            print("yagis_"+str(i)+".jpg --- Kaydedildi.")
            plt.savefig("gorseller/yagis/yagis_"+str(i)+".jpg",
                        dpi=300, bbox_inches='tight', pad_inches=0.2)
        plt.close(fig)

def plot_snow(ncfile, basemap, show_option=True, save_option=True, frameNo='all'):
    r''' ### doc string ###
        ...
    '''
    locale.setlocale(locale.LC_ALL,"tr_TR.utf8")

    snowh = getvar(ncfile, 'SNOWH', timeidx=ALL_TIMES)
    times = extract_times(ncfile, ALL_TIMES)

    lats, lons = latlon_coords(snowh)

    for i, time in zip(range(len(times)), times):
        if frameNo != 'all':
            if i != frameNo:
                continue


        # u10 = to_np(getvar(ncfile, 'U10', timeidx=i))
        # v10 = to_np(getvar(ncfile, 'V10', timeidx=i))

        if i == 0:
         continue
         snow = snowh[i,:,:] #+ rainnc[i,:,:]
        else:
         snow = ((snowh[i,:,:]-snowh[i-1,:,:])) #+ (rainnc[i,:,:]-rainnc[i-1,:,:]))

        np_snow = to_np(snow)*10 # convert to cm

        utc_time = to_datetime(time)
        local_time = utc_time + timedelta(hours=3)
        ilk_saat = utc_time + timedelta(hours=2)
        ilk_date = ilk_saat.strftime("%A, %H:00-")
        display_date = local_time.strftime("%H:00, %d-%m-%Y")
        date = ilk_date+display_date
        # save_time = local_time.strftime("%Y-%m-%d_%H")

        fig, ax = plt.subplots(1,1, figsize=(12,12))

        plt.text(.0002, 1.05, 'Toplam Kar (cm)', fontsize=18, transform=ax.transAxes)
        plt.text(.0002, 1.01, 'Total Snow', fontsize=14, transform=ax.transAxes)
        plt.text(.59, 1.03,s=date, fontsize=16, transform=ax.transAxes)

        draw_map(basemap)
        draw_iller(basemap)

        x, y = basemap(to_np(lons), to_np(lats))

        levels, norm, cmap = snow_cmap()

        CF = basemap.contourf(x, y, np_snow, levels, norm=norm, cmap=cmap, extend='max')
        plt.colorbar(CF, orientation="horizontal", ticks=levels,
                     shrink=.77, pad=.04, format='%.1f')

        # cbar.ax.set_ylabel('(mm)', rotation=-90)

        # wi = 12
        # barbs = basemap.barbs(x[::wi, ::wi], y[::wi, ::wi],
        #     u10[::wi, ::wi], v10[::wi, ::wi],
        #     pivot='middle', alpha=.7)

        # plt.suptitle("Toplam Kar Yağışı (cm)            ",
        #              y=0.76, fontsize=18)
        # plt.title(str(utctime)+' - '+str(display_date)+' Tarihleri Arası',
        #           loc='center', fontsize=12)

        #!! Sol altta çıkan 'İTÜ Modelleme Takımı' kutusu
        # plt.text(x=.012, y=.022, s="İTÜ Modelleme Takımı", color='darkblue',
        #          bbox=dict(facecolor='none', edgecolor='darkblue', boxstyle='round'),
        #          fontsize=11, transform=ax.transAxes)

        #!! Sağ alt köşede çıkan 'OUTPUT FROM WRF 4.1.1 MODEL' yazısı
        # plt.text(x=0.73, y=.01, s=ncfile.TITLE, fontsize=8, transform=ax.transAxes)
        #plt.savefig('snow/testsnow_'+str(stime)+'.png')

        if show_option:
            plt.show()
        if save_option:
            print("kar_"+str(i)+".jpg --- Kaydedildi.")
            plt.savefig("gorseller/kar/kar_"+str(i)+".jpg",)
        plt.close(fig)

def plot_height(ncfile, basemap, show_option=True, save_option=True, frameNo='all'):
    r''' ### doc string ###
        ...
    '''
    locale.setlocale(locale.LC_ALL,"tr_TR.utf8")

    times = extract_times(ncfile, ALL_TIMES)

    for i, time in zip(range(len(times)), times):
        if frameNo != 'all':
            if i != frameNo:
                continue

        p = getvar(ncfile, "pressure", timeidx=i)
        z = getvar(ncfile, "z", units="dm", timeidx=i)
        ua = getvar(ncfile, "ua", units="m s-1", timeidx=i)
        va = getvar(ncfile, "va", units="m s-1", timeidx=i)
        wspd = getvar(ncfile, "wspd_wdir", units="ms-1", timeidx=i)[0,:]

        ht_500 = smooth2d(interplevel(z, p, 500), 3, cenweight=5)
        u_500 = to_np(interplevel(ua, p, 500))
        v_500 = to_np(interplevel(va, p, 500))
        wspd_500 = smooth2d(interplevel(wspd, p, 500),3,cenweight=4)

        lats, lons = latlon_coords(ht_500)
        x, y = basemap(to_np(lons), to_np(lats))

        utc_time = to_datetime(time)
        local_time = utc_time + timedelta(hours=3)
        ilk_saat = utc_time + timedelta(hours=2)
        ilk_date = ilk_saat.strftime("%A, %H:00-")
        display_date = local_time.strftime("%H:00, %d-%m-%Y")
        date = ilk_date+display_date
        # save_time = local_time.strftime("%Y-%m-%d_%H")

        fig, ax = plt.subplots(1,1, figsize=(12,12))

        plt.text(.0002, 1.05, '500mb Rüzgar (m/s)', fontsize=18, transform=ax.transAxes)
        plt.text(.0002, 1.01, '500mb Winds', fontsize=14, transform=ax.transAxes)
        plt.text(.59, 1.03,s=date, fontsize=16, transform=ax.transAxes)

        draw_map(basemap)
        draw_iller(basemap)
        # levels = np.arange(520., 580., 6.)
        contours = basemap.contour(x, y, to_np(ht_500), colors="black")
        plt.clabel(contours, inline=1, fontsize=11, fmt="%i")

        # Add the wind speed contours
        # levels = np.arange(40,81,5)
        bounds, norm, cmap = wind_cmap()
        wspd_contours = basemap.contourf(x, y, to_np(wspd_500),
                             levels=bounds, norm=norm,
                             cmap=cmap)
        # plt.colorbar(wspd_contours, ax=ax, orientation="horizontal", pad=.05)
        plt.colorbar(wspd_contours, orientation="horizontal", shrink=.6,
                     pad=.05, ticks=bounds, format='%.1f')

        wi = 12
        barbs = basemap.barbs(x[::wi, ::wi], y[::wi, ::wi],
                u_500[::wi, ::wi], v_500[::wi, ::wi],
                pivot='middle', alpha=.7)

        if show_option:
            plt.show()
        if save_option:
            print("rüzgar_"+str(i)+".jpg --- Kaydedildi.")
            plt.savefig("gorseller/rüzgar/rüzgar_"+str(i)+".jpg",
            dpi=300, bbox_inches = 'tight',pad_inches=0.2)
        plt.close(fig)
    return

def plot_meteogram():
    pass

def plot_skewt():
    pass

if __name__ == '__main__':
    print('hello')
