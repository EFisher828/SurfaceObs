import matplotlib.tri as tri
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.patches as patches
import urllib.request
import math
import scipy.ndimage
import numpy as np
import shapefile as shp
from bs4 import BeautifulSoup


def main():
    SCOfile = open('stations.txt')
    print('Collecting Data...\n\n')


    Wind = []
    plotdata = []
    plotdew = []
    Latitude = []
    Longitude = []
    u = []
    v = []
    x = []
    y = []
    q = 0
    p = 0
    invest = 0

    for line in SCOfile:
        url = line
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html,features='html.parser')
        try:

            #A bunch of nonsense to isolate the temperature within the webpage's html
            
            Table = str(soup.find('table', {"class":"CurrentConditions"}).find_all('tr'))
            Tr = Table.split(',')

            length = len(Wind)
            lengthlat = len(Latitude)

            Wind_1 = str(Tr[6])
            Wind_2 = Wind_1.split('<')
            Wind_3 = str(Wind_2[9])
            Wind_4 = Wind_3.split('>')
            Wind_5 = str(Wind_4[1])
            Wind_Sum = Wind_5[1:]
            Wind.append(Wind_5)
            #print(Wind_Sum)

            if len(Wind) == length + 1:
                try:
                    #A bunch of nonsense to isolate the temperature within the webpage's html   
                    Table = str(soup.find('table', {"class":"StationDetails"}).find_all('tr'))
                    Tr = Table.split(',')

                    cord_1 = str(Tr[15])
                    #print(cord_1)
                    cord_2 = cord_1.split('</strong>')
                    lat_1 = str(cord_2[1])
                    lat_2 = lat_1.split('°')
                    lon_1 = str(cord_2[2])
                    lon_2 = lon_1.split('°')
                    lat = eval(lat_2[0])
                    lon = eval(lon_2[0])
                    #print(url[-5:])
                    #print(lat)
                    #print(lon)
                    Latitude.append(lat)
                    Longitude.append(lon)
                except:
                    try:
                        #A bunch of nonsense to isolate the temperature within the webpage's html   
                        Table = str(soup.find('table', {"class":"StationDetails"}).find_all('tr'))
                        Tr = Table.split(',')                
                        cord_1 = str(Tr[11])
                        #print(cord_1)
                        cord_2 = cord_1.split('</strong>')
                        lat_1 = str(cord_2[1])
                        lat_2 = lat_1.split('°')
                        lon_1 = str(cord_2[2])
                        lon_2 = lon_1.split('°')
                        lat = eval(lat_2[0])
                        lon = eval(lon_2[0])
                        #print(url[-5:])
                        #print(lat)
                        #print(lon)
                        Latitude.append(lat)
                        Longitude.append(lon)

                    except:
                        try:
                            #A bunch of nonsense to isolate the temperature within the webpage's html   
                            Table = str(soup.find('table', {"class":"StationDetails"}).find_all('tr'))
                            Tr = Table.split(',')                
                            cord_1 = str(Tr[12])
                            print(cord_1)
                            cord_2 = cord_1.split('</strong>')
                            lat_1 = str(cord_2[1])
                            lat_2 = lat_1.split('°')
                            lon_1 = str(cord_2[2])
                            lon_2 = lon_1.split('°')
                            lat = eval(lat_2[0])
                            lon = eval(lon_2[0])
                            #print(url[-5:])
                            #print(lat)
                            #print(lon)
                            Latitude.append(lat)
                            Longitude.append(lon)
                        except:
                            print("Abandon all hope for "+url[-5:])
            if len(Wind) == length + 1:
                try:
                    Table = str(soup.find('table', {"class":"CurrentConditions"}).find_all('tr'))
                    Tr = Table.split(',')

                    Temp_1 = str(Tr[4])
                    Temp_2 = Temp_1.split('<')
                    Temp_3 = str(Temp_2[9])
                    Temp_4 = Temp_3.split('>')
                    Temp_5 = str(Temp_4[1])
                    Temp_6 = Temp_5.split('°')
                    Temp_7 = str(Temp_6[0])
                    Temp_8 = Temp_7.strip(' ')
                    Temperature1 = eval(Temp_8)
                    Temperature = round(Temperature1)
                    plotdata.append(Temperature)
                except:
                    Temperature = 'M'
                    plotdata.append(Temperature)
                    #print(url + " temp missing")
                try:
                    Table = str(soup.find('table', {"class":"CurrentConditions"}).find_all('tr'))
                    Tr = Table.split(',')

                    Dew_1 = str(Tr[5])
                    Dew_2 = Dew_1.split('<')
                    Dew_3 = str(Dew_2[9])
                    Dew_4 = Dew_3.split('>')
                    Dew_5 = str(Dew_4[1])
                    Dew_6 = Dew_5.split('calculated at ')
                    Dew_7 = str(Dew_6[1])
                    Dew_8 = Dew_7.split('°')
                    Dew_9 = str(Dew_8[0])
                    Dewpoint1 = eval(Dew_9)
                    Dewpoint = round(Dewpoint1)
                    plotdew.append(Dewpoint)
                except:
                    try:
                        Table = str(soup.find('table', {"class":"CurrentConditions"}).find_all('tr'))
                        Tr = Table.split(',')

                        Dew_1 = str(Tr[5])
                        Dew_2 = Dew_1.split('size="-1"> ')
                        Dew_3 = str(Dew_2[1])
                        Dew_4 = Dew_3.split(' °F')
                        Dew_5 = str(Dew_4[0])
                        Dewpoint1 = eval(Dew_5)
                        Dewpoint = round(Dewpoint1)
                        plotdew.append(Dewpoint)
                    except:
                        Dewpoint = 'M'
                        plotdew.append(Dewpoint)
                    
        except:
            print(" missing and very broken")
        print(url[-4:] + Wind_Sum + ' ' + str(lat) + ' ' + str(lon) + ' ' + str(Temperature) + ' ' + str(Dewpoint))
        print(len(Latitude))
        print(len(plotdata))

    for i in Wind:
        temp_wind = str(Wind[q])
        if temp_wind[:4] == ' not':
            print("in not available with " + temp_wind)
            u.append(1)
            v.append(1)
            x.append(Longitude[q])
            y.append(Latitude[q])
            #print(u)
            #print(v)
            q = q + 1
        elif temp_wind[:5] == ' Calm':
            print("in Calm with " + temp_wind)
            u.append(1)
            v.append(1)
            x.append(Longitude[q])
            y.append(Latitude[q])
            #print(u)
            #print(v)
            q = q + 1

        elif temp_wind[:9] == ' Variable':
            print("in Variable with " + temp_wind)
            u.append(1)
            v.append(1)
            x.append(Longitude[q])
            y.append(Latitude[q])
            #print(u)
            #print(v)
            q = q + 1

        elif temp_wind[6:8] == '°F':
            print("Somehow got temp with " + temp_wind)
            u.append(1)
            v.append(1)
            x.append(Longitude[q])
            y.append(Latitude[q])
            q = q + 1

        elif temp_wind[:11] == ' calculated':
            print("Somehow got temp with " + temp_wind)
            u.append(1)
            v.append(1)
            x.append(Longitude[q])
            y.append(Latitude[q])
            q = q + 1
            
        elif temp_wind[4:6] == '°F':
            print("Somehow got temp with " + temp_wind)
            u.append(1)
            v.append(1)
            x.append(Longitude[q])
            y.append(Latitude[q])
            q = q + 1

        else:
            print("in not calm with " + temp_wind)
            Dir_1 = Wind[q].split('(')
            Dir_2 = str(Dir_1[1])
            Dir_3 = Dir_2.split('°')
            Dir_4 = eval(Dir_3[0])
            #print(Dir_4)
            Speed_1 = Wind[q].split('at ')
            Speed_2 = str(Speed_1[1])
            Speed_3 = Speed_2.split(' mph')
            Speed_4 = eval(Speed_3[0])

            if Dir_4 < 90:
                offset = 90 - Dir_4
                deg_direction = Dir_4 + 90 + 2*offset
            else:
                offset = 90 - Dir_4
                
            deg_direction = Dir_4 + 90 + 2*offset
            rad_direction = math.radians(deg_direction)
            speed = Speed_4
            u.append(speed*math.cos(rad_direction))
            v.append(speed*math.sin(rad_direction))
            x.append(Longitude[q])
            y.append(Latitude[q])
            #print(u)
            #print(v)
            q = q + 1
        
    print(x)
    print(y)
    fig = plt.figure(figsize=(13,8))
    #fig.patch.set_facecolor('grey')
    ax = plt.axes()
    #ax.set_facecolor('grey')
    ax.axis('off')
    ax.barbs(x,y,u,v, length=6,color='black')
    uf = len(plotdata)
    df = len(plotdew)
    hf = len(x)
    jf = len(y)
    print("Length plotdata " + str(df))
    print("Length plotdew " + str(uf))
    print("Length x " + str(hf))
    print("Length y " + str(jf))
    for b in x:
        plt.text((x[p])-0.2,(y[p])+0.1,plotdata[p],color='red',size=8)
        print("Temp " + str(p))
        plt.text((x[p])-0.2,(y[p])-0.1,plotdew[p],color='green',size=8)
        p = p + 1
    ax.set(xlim=(-84.6, -75.2), ylim=(31.82, 37))
    plt.xlim(-84.6, -75.2)
    plt.ylim(31.82, 37)
    #plt.text(-3,-0.7,"Valid: " + Time_7 + "     " + "Source: NCSCO",ha='center',size=12,color='white')

    sf = shp.Reader("GT NC & SC Counties.shp")

    for shape in sf.shapeRecords():
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            e = [i[0] for i in shape.shape.points[i_start:i_end]]
            f = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(e,f, color='grey', linewidth=0.2)

    rect = patches.Rectangle((-78.9,32.5),3.6,0.8,linewidth=1,edgecolor='black',facecolor='none')
    ax.add_patch(rect)
    
    plt.text(-77.1,32.7,'NC & SC\nSurface Observations',color='black',size=20,weight='bold',ha='center')
    plt.savefig("output/NcScMap.png",bbox_inches='tight',dpi=200)



main()
