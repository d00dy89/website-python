from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
import matplotlib.colors as colors
import numpy as np
from wrf import getvar, interplevel

def draw_map(basemap, shaded=True):
    # draw coastlines
    basemap.readshapefile('shapefiles/physical/ne_50m_coastline', 'ne_50m_coastlines',
                          drawbounds=True, linewidth=.35)
    # draw state boundaries
    basemap.readshapefile('shapefiles/cultural/ne_50m_admin_0_boundary_lines_land',
                          'ne_50m_statebounds', drawbounds=True, linewidth=.35)

    # draw parallels
    basemap.drawparallels(np.arange(5,55,5),labels=[1,0,0,0])
    # draw meridians
    basemap.drawmeridians(np.arange(4,55,10),labels=[0,0,0,1])

    #bm.drawcoastlines(linewidth=0.5)
    #bm.drawstates(linewidth=0.5)
    #bm.drawcountries(linewidth=0.5)
    #bm.shadedrelief()

    if shaded:
        basemap.shadedrelief()

    return

def snow_cmap():
    cmap = colors.ListedColormap(['lightcyan','powderblue','skyblue','deepskyblue','dodgerblue','blue',
                                      'mediumblue','midnightblue','yellow','orange','red'])
    cmap.set_over('darkred')
    cmap.set_under('0.75')

    bounds = [.01,0.1,0.2,0.4,0.7,1,1.5,2.5,4,6,9]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    return bounds, norm, cmap

def rain_cmap():
    # ['lightcyan','powderblue','skyblue','deepskyblue','dodgerblue','blue','mediumblue','midnightblue','yellow','orange','red'])
    cols = ['xkcd:pale blue',
    'palegreen',
    'xkcd:yellow tan',
    "xkcd:amber",
    "xkcd:faded red",
    "xkcd:auburn",
    "xkcd:very dark brown"]

    cmap = colors.ListedColormap(cols)

    cmap.set_over('darkred')
    # cmap.set_under('white')

    # bounds = [.01,0.1,0.2,0.4,0.7,1,1.5,2.5,4,6,9]
    bounds = [0,.01,.05,.2,.5,.75,1,5]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    return bounds, norm, cmap

def temperature_cmap():
    cmap = colors.ListedColormap(["darkblue",'royalblue',"cornflowerblue",'lightskyblue',"mediumseagreen","seagreen",
                                  "goldenrod","lightcoral",'indianred','firebrick',"darkred","crimson"])
    cmap.set_over('darkorchid')
    cmap.set_under('orchid')

    bounds = [-20,-10,-5,0,5,8,12,15,18,21,25,30,40]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    return bounds, norm, cmap

def temp_cmap():
    cols = ['darkorchid', "darkblue",'royalblue',"cornflowerblue",'lightskyblue',"mediumseagreen","seagreen",
            "goldenrod","lightcoral",'indianred','firebrick',"darkred","crimson", 'orchid']
    # cmap.set_over()
    # cmap.set_under()

    # bounds = [-20,-10,-5,0,5,8,12,15,18,21,25,30,40]
    bounds = np.arange(-20,40,2)
    cmap, norm = colors.from_levels_and_colors(bounds, colors=cols, extend='both')

    # norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    return bounds, norm, cmap

def height_cmap():
    pass

def get_wind(ncfile, unit, time, z=10):
    if z == '10':
        u10 = getvar(ncfile, 'U10', units=unit, timeidx=time)
        v10 = getvar(ncfile, 'V10', units=unit, timeidx=time)
        return u10, v10
    else:
        p = getvar(ncfile, 'pressure', timeidx=time)
        uw = getvar(ncfile, 'ua', units=unit, timeidx=time)
        vw = getvar(ncfile, 'va', units=unit, timeidx=time)
        return interplevel(uw, p, z), interplevel(vw, p, z)

if __name__ == '__main__':
    print('Hello this is tools.py')
