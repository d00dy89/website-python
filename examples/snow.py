from wrf import (getvar, extract_times, ALL_TIMES, get_basemap, latlon_coords, to_np)
from netCDF4 import Dataset
import matplotlib
matplotlib.use('Agg')
from matplotlib.cm import get_cmap
from mpl_toolkits.basemap import Basemap
from pandas import to_datetime
from datetime import timedelta
#from metpy.plots import colortables
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import locale, csv
locale.setlocale(locale.LC_ALL,"tr_TR.utf8")

def draw_borders(basemap):
 # draw coastlines
 basemap.readshapefile('shapefiles/physical/ne_50m_coastline', 'ne_50m_coastlines',
                       drawbounds=True, linewidth=.35)
 # draw state boundaries
 basemap.readshapefile('shapefiles/cultural/ne_50m_admin_0_boundary_lines_land',
                       'ne_50m_statebounds', drawbounds=True, linewidth=.35)
 basemap.readshapefile('shapefiles/Turkiye_iller/iller','iller',
                       drawbounds=True, linewidth=.35)

def snow_cmap():
    cmap = mpl.colors.ListedColormap(['lightcyan','powderblue','skyblue','deepskyblue','dodgerblue','royalblue',
                                      'mediumblue','midnightblue','yellow','orange','red'])
    cmap.set_over('darkred')
    cmap.set_under('0.75')

    bounds = [.01,0.1,0.2,0.4,0.7,1,1.5,2.5,4,6,9]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    return bounds, norm, cmap

names_nokta=[]; enlem_nokta=[]; boylam_nokta=[]
with open('shapefiles/Turkiye_iller/sehir_merkezleri.csv') as csvfile:
    reader = csv.DictReader(csvfile,delimiter=',')
    for data in reader:
        names_nokta.append(data['City'])
        enlem_nokta.append(float(data['Lat']))
        boylam_nokta.append(float(data['Long']))


ncfile = Dataset("/mnt/depo2/WRFOUT/hava12/wrfout_d01_2021-02-14_18.nc")

rainc = getvar(ncfile, 'SNOWNC', timeidx=ALL_TIMES)
#rainnc = getvar(ncfile, 'RAINNC', timeidx=ALL_TIMES)

times = extract_times(ncfile, ALL_TIMES)
bm = get_basemap(wrfin=ncfile)
lats, lons = latlon_coords(rainc)

for i, time in zip(range(len(times)), times):
    #if i != 17:
    # continue

    utc_time = to_datetime(time)
    local_time = utc_time + timedelta(hours=3)
    #utc_time = utc_time + timedelta(hours=2)

    #day = local_time.strftime("%a")
    #dtime = local_time.strftime("%H:00")
    date = local_time.strftime("%a, %H:00_%d-%m-%Y")
    utctime = utc_time.strftime("%a, %H:00_%d-%m-%Y")
    stime = local_time.strftime("%Y-%m-%d_%H")

    #u10 = to_np(getvar(ncfile, 'U10', timeidx=i))
    #v10 = to_np(getvar(ncfile, 'V10', timeidx=i))

    if i == 0:
     continue
     rainsum = rainc[i,:,:] #+ rainnc[i,:,:]
    else:
     rainsum = ((rainc[i,:,:]-rainc[i-1,:,:])) #+ (rainnc[i,:,:]-rainnc[i-1,:,:]))

    rain = to_np(rainsum)

    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot(111)

    bm.shadedrelief()
    #bm.drawcoastlines(linewidth=0.5)
    #bm.drawstates(linewidth=0.5)
    #bm.drawcountries(linewidth=0.5)
    draw_borders(bm)

    x, y = bm(to_np(lons), to_np(lats))

    #levels = [ .01, .1, 0.2, .4, .6, .8, 1., 1.5, 2., 3., 5., 8., 12., 16.]
    levels, norm, cmap = snow_cmap()
    CF = bm.contourf(x, y, rain/10, levels, norm=norm, cmap=cmap, extend='max')
    plt.colorbar(CF, shrink=.6, pad=.03, ticks=levels, format='%.1f')
    # cbar.ax.set_ylabel('(mm)', rotation=-90)
    # draw parallels
    bm.drawparallels(np.arange(5,55,5),labels=[1,0,0,0])
    # draw meridians
    bm.drawmeridians(np.arange(5,55,10),labels=[0,0,0,1])
    x,y = bm(boylam_nokta,enlem_nokta)
    bm.plot(x,y,'r*',markersize=4)
    #wi = 8
    #Q = bm.quiver(x[::wi, ::wi], y[::wi, ::wi],
    #     u10[::wi, ::wi], v10[::wi, ::wi],
    #     pivot='middle', alpha=.7)

    #wi = 8
    #B = bm.barb(x[::wi, ::wi], y[::wi, ::wi],
    #     u10[::wi, ::wi], v10[::wi, ::wi],
    #     pivot='middle', alpha=.7)

    plt.suptitle("Toplam Kar Yağışı (cm)            ",
                 y=0.76, fontsize=18)
    plt.title(str(utctime)+' - '+str(date)+' Tarihleri Arası',
              loc='center', fontsize=12)

    plt.text(x=.012, y=.022, s="İTÜ Modelleme Takımı", color='darkblue',
             bbox=dict(facecolor='none', edgecolor='darkblue', boxstyle='round'),
             fontsize=11, transform=ax.transAxes)
    #plt.text(x=0.73, y=.01, s=ncfile.TITLE, fontsize=8, transform=ax.transAxes)
    plt.savefig('snow/testsnow_twitter_'+str(stime)+'.jpg',dpi=300, bbox_inches = 'tight',pad_inches=0.2)
    plt.savefig('snow/testsnow_instagram_'+str(stime)+'.jpg',dpi=300)
    #plt.show()
    plt.close(fig)
    #exit()
