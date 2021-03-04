import matplotlib as mpl
import numpy as np
import csv

from matplotlib.cm import get_cmap
from mpl_toolkits.basemap import Basemap

def draw_map(basemap, shaded=True):
    # draw coastlines
    basemap.readshapefile('shapefiles/physical/ne_50m_coastline', 'ne_50m_coastlines',
                          drawbounds=True, linewidth=.35)
    # draw state boundaries
    basemap.readshapefile('shapefiles/cultural/ne_50m_admin_0_boundary_lines_land',
                          'ne_50m_statebounds', drawbounds=True, linewidth=.5)

    # İl sınırlarını çiz
    basemap.readshapefile('shapefiles/Turkiye_iller/iller','iller', drawbounds=True, linewidth=.25)

    # draw parallels
    basemap.drawparallels(np.arange(30,45,2),labels=[1,0,0,0])

    # draw meridians
    basemap.drawmeridians(np.arange(15,55,5),labels=[0,0,0,1])

    #bm.drawcoastlines(linewidth=0.5)
    #bm.drawstates(linewidth=0.5)
    #bm.drawcountries(linewidth=0.5)
    #bm.shadedrelief()

    if shaded:
        basemap.shadedrelief()

    return

def draw_iller(basemap):
    names_nokta=[]; enlem_nokta=[]; boylam_nokta=[]
    with open('shapefiles/Turkiye_iller/sehir_merkezleri.csv') as csvfile:
        reader = csv.DictReader(csvfile,delimiter=',')
        for data in reader:
            names_nokta.append(data['City'])
            enlem_nokta.append(float(data['Lat']))
            boylam_nokta.append(float(data['Long']))

    x,y = basemap(boylam_nokta, enlem_nokta)
    basemap.plot(x, y, 'r*',markersize=4)
    return

def plot_full_title(ax, ncfile):
    pass
    # TODO: Her görsel için ortak olabilecek başlık özelliklerini bir araya topla
    '''
    utc_time = to_datetime(time)
    local_time = utc_time + timedelta(hours=3)
    ilk_saat = utc_time + timedelta(hours=2)
    ilk_date = ilk_saat.strftime("%A, %H:00-")
    display_date = local_time.strftime("%H:00, %d-%m-%Y")
    date = ilk_date+display_date
'''
    return

def snow_cmap():
    # cmap = mpl.colors.ListedColormap(['lightcyan','powderblue','skyblue','deepskyblue','dodgerblue','blue',
    #                                   'mediumblue','midnightblue','yellow','orange','red'])
    # cmap.set_over('darkred')
    # cmap.set_under('0.75')
    #
    # bounds = [.01,0.1,0.2,0.4,0.7,1,1.5,2.5,4,6,9]
    cmap = mpl.colors.ListedColormap(["xkcd:light blue grey","xkcd:silver","xkcd:greyish","xkcd:steel"])
    bounds = [.01,1,5,20,50]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    return bounds, norm, cmap

def rain_cmap():
    # Old colormap
    cmap = mpl.colors.ListedColormap(['lightcyan','powderblue','skyblue','deepskyblue','dodgerblue','blue',
                                      'mediumblue','midnightblue','xkcd:yellowish',"xkcd:amber",'xkcd:faded red','xkcd:auburn'])
    cmap.set_over('darkred')
    bounds = [.01,0.1,0.2,0.4,0.7,1,1.5,2.5,5,10,15,20,30]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    # New colormap
    # cmap = mpl.colors.ListedColormap (['xkcd:pale blue','palegreen','xkcd:yellow tan',"xkcd:amber","xkcd:faded red","xkcd:auburn","xkcd:very dark brown"])
    #
    # bounds = [.01,.05,.2,.5,.75,1,5,15]
    # norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    return bounds, norm, cmap

def temperature_cmap():
    cmap = mpl.colors.ListedColormap(["darkblue",'royalblue',"cornflowerblue",
                                    'lightskyblue',"mediumseagreen","seagreen",
                                    "goldenrod","lightcoral",'indianred',
                                    'firebrick',"darkred","crimson"])

    # cmap = get_cmap('rainbow')
    cmap.set_over('darkorchid')
    cmap.set_under('orchid')

    bounds = [-20,-10,-5,0,5,8,12,15,18,21,25,30,40]
    # bounds = np.arange(min-1, max+1, 2)

    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    return bounds, norm, cmap

def height_cmap():
    pass

def wind_cmap():
    cmap = mpl.colors.ListedColormap(['xkcd:manilla',"xkcd:dandelion","xkcd:dusty orange","xkcd:rust","xkcd:deep red",'xkcd:deep brown'])

    bounds = [10,20,30,40,50,60]
    # m/s
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    return bounds, norm, cmap

if __name__ == '__main__':
    print('Hello this is tools.py')
