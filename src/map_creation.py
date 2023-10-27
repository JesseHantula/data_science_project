import folium
from map_creation_prep import get_prediction_coordinates


def create_map():

    data = get_prediction_coordinates()

    m = folium.Map(location=[60.211,24.947], tiles="OpenStreetMap", zoom_start=11.5)

    #add title to map
    title = '''
             <h1 align="center" style="font-size:30px"><b>HSL Bike Planner</b></h1>
             <h4 align ="center" style="font-size:15px"><b>Find your city bike station on the map and click on the pin to see how busy it will be during the next 5 days</b></h4>
             <h4 align ="center" style="font-size:15px"><b>Busy-ness scale: <font color=#006400>Not Busy</font>, <font color=#FFD800>Moderately Busy</font>, <font color=#F28500>Quite Busy</font>, <font color=#FF0000>Very Busy</font>, <font color=#451425>Extremely Busy</font></b></h4>
             '''
    m.get_root().html.add_child(folium.Element(title))

    # add marker one by one on the map
    for i in range(0,len(data)):
        html=f"""
        <h3> {data.iloc[i]['Prediction']['Station']}</h3>
        <ul>
            <li>{data.iloc[i]['Prediction']['Day 1']}:</br> <font color={data.iloc[i]['Prediction']['Color 1']}>{data.iloc[i]['Prediction']['Prediction 1']}</font></li>
            <li>{data.iloc[i]['Prediction']['Day 2']}:</br> <font color={data.iloc[i]['Prediction']['Color 2']}>{data.iloc[i]['Prediction']['Prediction 2']}</font></li>
            <li>{data.iloc[i]['Prediction']['Day 3']}:</br> <font color={data.iloc[i]['Prediction']['Color 3']}>{data.iloc[i]['Prediction']['Prediction 3']}</font></li>
            <li>{data.iloc[i]['Prediction']['Day 4']}:</br> <font color={data.iloc[i]['Prediction']['Color 4']}>{data.iloc[i]['Prediction']['Prediction 4']}</font></li>
            <li>{data.iloc[i]['Prediction']['Day 5']}:</br> <font color={data.iloc[i]['Prediction']['Color 5']}>{data.iloc[i]['Prediction']['Prediction 5']}</font></li>
        </ul>
        """
        iframe = folium.IFrame(html=html, width=200, height=200)
        popup = folium.Popup(iframe, max_width=2650)
        folium.Marker(
            location=[data.iloc[i]['y'], data.iloc[i]['x']],
            popup=popup,
            icon=folium.Icon(color="orange")
        ).add_to(m)

    # Save it as html
    m.save('./index.html')
