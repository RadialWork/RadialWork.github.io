# import numpy as np
# import pandas as pd
# import shapefile as shp
# import matplotlib.pyplot as plt
# import seaborn as sns

# sns.set(style="whitegrid", palette="pastel", color_codes=True) 
# sns.mpl.rc("figure", figsize=(10,6))

# #opening the vector map
# shp_path = 'regional-council-2020-generalised.shp'
# #reading the shape file by using reader function of the shape lib
# sf = shp.Reader(shp_path)

# def read_shapefile(sf):
#     #fetching the headings from the shape file
#     fields = [x[0] for x in sf.fields][1:]
# #fetching the records from the shape file
#     records = [list(i) for i in sf.records()]
#     shps = [s.points for s in sf.shapes()]
# #converting shapefile data into pandas dataframe
#     df = pd.DataFrame(columns=fields, data=records)
# #assigning the coordinates
#     df = df.assign(coords=shps)
#     return df

# def plot_shape(id, s=None):
#     plt.figure()
#     #plotting the graphical axes where map ploting will be done
#     ax = plt.axes()
#     ax.set_aspect('equal')
# #storing the id number to be worked upon
#     shape_ex = sf.shape(id)
# #NP.ZERO initializes an array of rows and column with 0 in place of each elements 
#     #an array will be generated where number of rows will be(len(shape_ex,point))and number of columns will be 1 and stored into the variable
#     x_lon = np.zeros((len(shape_ex.points),1))
# #an array will be generated where number of rows will be(len(shape_ex,point))and number of columns will be 1 and stored into the variable
#     y_lat = np.zeros((len(shape_ex.points),1))
#     for ip in range(len(shape_ex.points)):
#         x_lon[ip] = shape_ex.points[ip][0]
#         y_lat[ip] = shape_ex.points[ip][1]
# #plotting using the derived coordinated stored in array created by numpy
#     plt.plot(x_lon,y_lat) 
#     x0 = np.mean(x_lon)
#     y0 = np.mean(y_lat)
#     plt.text(x0, y0, s, fontsize=10)
# # use bbox (bounding box) to set plot limits
#     plt.xlim(shape_ex.bbox[0],shape_ex.bbox[2])
#     return x0, y0


# def plot_map(sf, x_lim = None, y_lim = None, figsize = (11,9)):
#     plt.figure(figsize = figsize)
#     id=0
#     for shape in sf.shapeRecords():
#         x = [i[0] for i in shape.shape.points[:]]
#         y = [i[1] for i in shape.shape.points[:]]
#         plt.plot(x, y, 'k')
        
#         if (x_lim == None) & (y_lim == None):
#             x0 = np.mean(x)
#             y0 = np.mean(y)
#             plt.text(x0, y0, id, fontsize=10)
#         id = id+1
    
#     if (x_lim != None) & (y_lim != None):     
#         plt.xlim(x_lim)
#         plt.ylim(y_lim)

# #calling the function and passing required parameters to plot the full map
# df = read_shapefile(sf)
# plot_map(sf)


# plt.show()

# import shapefile
# from json import dumps

# myshp = open("regional.shp", "rb")
# mydbf = open("regional.dbf", "rb")
# reader = shapefile.Reader(shp=myshp, dbf=mydbf)

#    # read the shapefile
# fields = reader.fields[1:]
# field_names = [field[0] for field in fields]
# buffer = []
# for sr in reader.shapeRecords():
#    atr = dict(zip(field_names, sr.record))
#    geom = sr.shape.__geo_interface__
#    buffer.append(dict(type="Feature", \
#     geometry=geom, properties=atr)) 

#    # write the GeoJSON file

# geojson = open("regional-council-2020-generalised.json", "w")
# geojson.write(dumps({"type": "FeatureCollection", "features": buffer}, indent=2) + "\n")
# geojson.close()





import folium
import random
import base64

map = folium.Map(location=[-40.9,174.89],zoom_start = 6)

def my_colour_function(x):
	return random.choice(['red',
    'blue',
    'gray',
    'darkred',
    'lightred',
    'orange',
    'beige',
    'green',
    'darkgreen',
    'lightgreen',
    'darkblue',
    'lightblue',
    'purple',
    'darkpurple',
    'pink',
    'cadetblue',
    'lightgray'])



fg = folium.FeatureGroup(name="NZ MAP")
data = open('nz_region.geojson','r', encoding='utf-8-sig').read()
fg.add_child(folium.GeoJson(data,style_function = lambda x: {'fillColor':my_colour_function(x)}))

regions = [['Auckland',[-36.8,174.76]],
 ['Wellington',[-41.28,174.77]],
 ['Bay of Plenty',[-37.99,176.92]],
 ['Canterbury',[-43.56,172.11]],
 ['Gisbourne',[-38.65333, 178.00417]],
 ["Hawke's Bay",[-39.48333, 176.91667]],
 ['Manawatu Wanganui',[-39.87, 175.24]],
 ["Marlborough",[-41.51603, 173.9528]],
 ['Nelson',[-37.78333, 175.28333]],
['Northland',[-35.822177, 174.29132]],
['Taranaki',[-39.353, 174.044]],
['Tasman',[-41.38909, 172.82]],
['Otago',[-45.606,170.05]],
['West Coast',[-43.13,170.485]],
['Southland',[-45.993068,167.90]],
 ['Waikato',[-37.78333, 175.28333]]]


fg2 = folium.FeatureGroup(name="popups")

for i in regions:
    file = './graphs/New Job Ads by Week - ' + i[0] + '.png'
    encoded = base64.b64encode(open(file, 'rb').read())
    html = '<img src="data:image/png;base64,{}">'.format
    width = 806
    height = 500 
    iframe = folium.IFrame(html(encoded.decode('UTF-8')), width=(width)+20, height=(height)+20)
    popup = folium.Popup(iframe, max_width=2650)

    icon = folium.Icon(color="blue", icon="bar-chart",prefix='fa')
    marker = folium.Marker(i[1], popup=popup, icon=icon)
    marker.add_to(fg2)


map.add_child(fg)
map.add_child(fg2)

map.save("Map.html")


