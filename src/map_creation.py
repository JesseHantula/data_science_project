#https://python-graph-gallery.com/312-add-markers-on-folium-map/
import folium
from map_creation_prep import get_prediction_coordinates


def create_map():

    data = get_prediction_coordinates()

    m = folium.Map(location=[60.211,24.947], tiles="OpenStreetMap", zoom_start=11.5)

    # add marker one by one on the map
    for i in range(0,len(data)):
        folium.Marker(
            location=[data.iloc[i]['y'], data.iloc[i]['x']],
            popup=data.iloc[i]['Prediction'],
        ).add_to(m)

    # Save it as html
    m.save('./map.html')