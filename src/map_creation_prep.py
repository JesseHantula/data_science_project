import pandas as pd
from predictor import get_predictions_as_words

"""To create the interactive map with busyness information for each station,
we need to create a dataframe with columns of the station coordinates, and the busyness for the next 5 days. 

First, we do the required imports and load the coordinate csv file and the predictions csv file.
"""

def get_prediction_coordinates():

    get_predictions_as_words()

    station_coordinates = pd.read_csv("./data/HSL/city_bike_station_coordinates.csv")
    predictions = pd.read_csv("./data/predictions.csv")
    #display(station_coordinates)

    """We only need to retain the station names and coordinates (x and y columns)."""

    station_coordinates = station_coordinates.drop(columns=["FID", "ID", "Namn","Name","Osoite", "Adress", "Kaupunki", "Stad", "Operaattor","Kapasiteet"])

    """We merge the two dataframes, so the predictions df also has the coordinates for each station, and save the result to csv."""

    predictions = pd.merge(predictions, station_coordinates, left_on="Station", right_on="Nimi", how="left")
    predictions = predictions.drop(columns="Nimi")

    #Replace predictions with f string of Station name NEW LINE Date: Busyness NEW LINE ...

    predictions.to_csv('./data/predictions_with_coordinates.csv', index=False)

    return predictions