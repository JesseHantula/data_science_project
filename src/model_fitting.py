#imports
import pandas as pd
import pickle
from sklearn.linear_model import PoissonRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


def fit_models(data_path = './data/finalized_data.csv', save_path = './data/models.pkl'):
    df = pd.read_csv(data_path)

    #We use only data from 2019 onwards in order to benefit from our 'Last 3 year avg' features
    df = df[df['Year'] > 2]

    #get a list of all unique stations in the dataset from year 2021 (latest year)
    stations = df[df['Year'] == 5]['Station'].unique()

    models = {}

    for station in stations:
        #get data for station from df
        station_data = df[df['Station'] == station]

        if len(station_data) < 100:
            continue

        returns = station_data['Return Count']
        departures = station_data['Departure Count']

        station_data = station_data.drop(['Departure Count', 'Return Count', 'Station'], axis=1)

        #split data into train and test
        X_train, X_test, y_train, y_test = train_test_split(station_data, departures, test_size=0.2, shuffle=True, random_state=42)

        model = PoissonRegressor(max_iter=6000)
        model.fit(X_train, y_train)

        #find mean squared error of test data
        predictions = model.predict(X_test)
        score = mean_squared_error(y_test, predictions)

        models[station] = {'Departures': [model, score]}

        #repeat for returns

        X_train, X_test, y_train, y_test = train_test_split(station_data, returns, test_size=0.2, shuffle=True, random_state=42)

        model = PoissonRegressor(max_iter=6000)
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        score = mean_squared_error(y_test, predictions)

        models[station]['Returns'] = [model, score]

    #save models to file

    with open(save_path, 'wb') as f:
        pickle.dump(models, f)
