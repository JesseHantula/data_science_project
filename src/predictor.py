import pickle
import pandas as pd
from prediction_data import get_prediction_data

def load_models(models_path='./data/models.pkl'):
    with open(models_path, 'rb') as f:
        models = pickle.load(f)
    return models


def predict(data, models):

    predictions = {}

    for station in models.keys():
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
        predictions[station] = {'Predicted Departures (5 days)': departures, 'Predicted Returns (5 days)': returns}
    
    return predictions


def get_predictions(models_path='./data/models.pkl'):
    predict_data = get_prediction_data()
    models = load_models(models_path)

    predictions = predict(predict_data, models)

    predictions = pd.DataFrame.from_dict(predictions, orient='index')

    return predictions

