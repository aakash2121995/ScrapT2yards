import plotly.plotly as py
import pandas as pd

df = pd.read_csv('info.csv') #reading the stored info
df.head()

df['text'] = df['Location'] + '<br>Matches ' + (df['Matches']).astype(str) #text for labeling data

limits = [(0,1),(1,7),(7,14),(14,23),(23,46)]                               #limits
colors = ["rgb(0,116,217)","rgb(255,65,54)","rgb(133,20,75)","rgb(255,133,27)","lightgrey"] #colors for bubbles
cities = [] #list of locations


for i in range(len(limits)):
    lim = limits[i]
    df_sub = df[lim[0]:lim[1]]
    
    city = dict(
        type = 'scattergeo',
        locationmode = 'WORLD',
        lon = df_sub['Lon'],            #longitude values
        lat = df_sub['Lat'],            #latitude values
        text = df_sub['text'],          
        marker = dict(
            size = 20*df_sub['Matches']**1.3, #scaling for radius of the bubble
            color = colors[i],                 # color for the bubble
            line = dict(width=0.5, color='rgb(40,40,40)'),
            sizemode = 'area'
        ),
        name = '{0} - {1}'.format(lim[0],lim[1]) )
    cities.append(city)

layout = dict(
        title = 'Matches happening around the globe between July 2016 and January 2017<br>(Click legend to toggle traces)',
        showlegend = True,
        geo = dict(
            scope='world',
            showland = True,
            landcolor = 'rgb(217, 217, 217)',
            subunitwidth=1,
            countrywidth=1,
            subunitcolor="rgb(255, 255, 255)",
            countrycolor="rgb(255, 255, 255)"
        ),
    )

fig = dict( data=cities, layout=layout )
url = py.plot( fig, validate=False, filename='d3-bubble-map-populations' )