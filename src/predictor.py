import pickle
import pandas as pd
import numpy as np
import datetime as dt
from prediction_data import get_prediction_data

def load_models(models_path='./data/models.pkl'):
    with open(models_path, 'rb') as f:
        models = pickle.load(f)
    return models


def predict(data, models, avgs_path):

    last3avgs = pd.read_csv(avgs_path)

    predictions = {}

    for station in models.keys():

        stationavgs = last3avgs[last3avgs['Station'] == station]
        stationavgs = stationavgs.drop(['Station'], axis=1)
        data = pd.merge(data, stationavgs, left_on="Month", right_on="Month", how="left")

        #get model for departures
        model = models[station]['Departures'][0]
        #get model for returns
        model2 = models[station]['Returns'][0]

        #get predictions for departures
        departures = model.predict(data)
        returns = model2.predict(data)

        #round predictions to nearest integer, as we can't have a fraction of a departure or return
        departures = [round(x) for x in departures]
        returns = [round(x) for x in returns]

        #add predictions to dictionary
        predictions[station] = {'Predicted Departures (5 days)': np.array(departures), 'Predicted Returns (5 days)': np.array(returns)}

        data = data.drop(['Last 3 Year Avg Departures', 'Last 3 Year Avg Returns'], axis=1)
    
    return predictions


def get_predictions(models_path='./data/models.pkl', avgs_path='./data/last_3_year_averages.csv'):
    predict_data = get_prediction_data()
    models = load_models(models_path)

    predictions = predict(predict_data, models, avgs_path)

    predictions = pd.DataFrame.from_dict(predictions, orient='index')

    return predictions


def get_predictions_as_words(models_path='./data/models.pkl', avgs_path='./data/last_3_year_averages.csv', save_path='./data/predictions.csv'):
    predictions = get_predictions(models_path, avgs_path)
    stationavgs = pd.read_csv(avgs_path)

    start_time = dt.datetime.now() + dt.timedelta(days=1)
    months = np.empty(5)
    for i in range(5):
        months[i] = (start_time + dt.timedelta(days=i)).month

    new_predictions = pd.DataFrame(columns=['Station', 'Predicted Busyness'])

    for index, row in predictions.iterrows():
        depavgs = np.empty(5)
        retavgs = np.empty(5)
        for i in range(5):
            depavgs[i] = stationavgs[(stationavgs['Station'] == index) & (stationavgs['Month'] == months[i])]['Last 3 Year Avg Departures']
            retavgs[i] = stationavgs[(stationavgs['Station'] == index) & (stationavgs['Month'] == months[i])]['Last 3 Year Avg Returns']

        avg_avgs = np.divide(np.add(depavgs, retavgs), 2)
        difference = np.subtract(row['Predicted Departures (5 days)'], row['Predicted Returns (5 days)'])
        scaled_difference = np.divide(difference, avg_avgs)

        busy_values = np.subtract(np.divide(np.add(np.divide(row['Predicted Departures (5 days)'], depavgs), np.divide(row['Predicted Returns (5 days)'], retavgs)), 2), scaled_difference)
        busy_values = list(busy_values)

        for i in range(5):
            if busy_values[i] < 0.4:
                busy_values[i] = "Quiet"
            elif busy_values[i] < 0.8:
                busy_values[i] = "Not Busy"
            elif busy_values[i] < 1.2:
                busy_values[i] = "Average"
            elif busy_values[i] < 1.6:
                busy_values[i] = "Busy"
            else:
                busy_values[i] = "Very Busy"


        temp = {'Station': index, 'Predicted Busyness': busy_values}
        #add row temp to new_predictions
        new_predictions.loc[len(new_predictions)] = temp

    new_predictions.to_csv(save_path, index=False)
    
    return new_predictions
