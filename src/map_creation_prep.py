import pandas as pd
import datetime as dt
from predictor import get_predictions_as_words

"""To create the interactive map with busyness information for each station,
we need to create a dataframe with columns of the station coordinates, and the busyness for the next 5 days. 

First, we do the required imports and load the coordinate csv file and the predictions csv file.
"""

def get_color(busyness):
    if busyness == "Not Busy":
        return "#006400"
    elif busyness == "Moderately Busy":
        return "#FFD800"
    elif busyness == "Quite Busy":
        return "#F28500"
    elif busyness == "Very Busy":
        return "#FF0000"
    else:
        return "#451425"


def get_prediction_coordinates():

    station_coordinates = pd.read_csv("./data/HSL/city_bike_station_coordinates.csv")
    predictions = get_predictions_as_words()

    predictions = predictions[predictions["Station"] != "Workshop Helsinki"]
    predictions = predictions[predictions["Station"] != "Lumivaarantie"]
    predictions = predictions[predictions["Station"] != "Lintumetsä"]

    """We only need to retain the station names and coordinates (x and y columns)."""

    station_coordinates = station_coordinates.drop(columns=["FID", "ID", "Namn","Name","Osoite", "Adress", "Kaupunki", "Stad", "Operaattor","Kapasiteet"])

    """We merge the two dataframes, so the predictions df also has the coordinates for each station, and save the result to csv."""

    predictions = pd.merge(predictions, station_coordinates, left_on="Station", right_on="Nimi", how="left")
    predictions = predictions.drop(columns="Nimi")

    #Replace predictions with f string of Station name NEW LINE Date 1: Busyness NEW LINE Date 2: Busyness etc.

    day1 = (dt.datetime.today() + dt.timedelta(days=1)).strftime("%d.%m.%Y")
    day2 = (dt.datetime.today() + dt.timedelta(days=2)).strftime("%d.%m.%Y")
    day3 = (dt.datetime.today() + dt.timedelta(days=3)).strftime("%d.%m.%Y")
    day4 = (dt.datetime.today() + dt.timedelta(days=4)).strftime("%d.%m.%Y")
    day5 = (dt.datetime.today() + dt.timedelta(days=5)).strftime("%d.%m.%Y")

    days = [day1, day2, day3, day4, day5]

    dictionaries = []
    for row in predictions.iterrows():
        d = {}
        d["Station"] = row[1]['Station']
        for i in range(5):
            key = "Day " + str(i+1)
            d[key] = days[i]
            predkey = "Prediction " + str(i+1)
            d[predkey] = row[1]['Predicted Busyness'][i]
            colorkey = "Color " + str(i+1)
            d[colorkey] = get_color(row[1]['Predicted Busyness'][i])
        dictionaries.append(d)
    
    predictions["Prediction"] = dictionaries

    predictions = predictions.drop(columns=["Station", "Predicted Busyness"])

    predictions.to_csv('./data/predictions_with_coordinates.csv', index=False)

    return predictions