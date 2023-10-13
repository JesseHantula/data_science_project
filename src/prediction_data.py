#imports
import pandas as pd
import datetime as dt
from fmiopendata.wfs import download_stored_query


def get_prediction_data():
    #start time is tomorrow 00:00
    start_time = dt.datetime.now() + dt.timedelta(days=1)
    start_time = start_time.replace(hour=0, minute=0, second=0, microsecond=0)
    #end time in 10 days
    end_time = start_time + dt.timedelta(days=5) - dt.timedelta(hours=1)

    #put into correct format
    start_time = start_time.isoformat(timespec="seconds") + "Z"
    end_time = end_time.isoformat(timespec="seconds") + "Z"

    forecast = download_stored_query("fmi::forecast::edited::weather::scandinavia::point::multipointcoverage", args=["starttime="+start_time, "endtime="+end_time, "place=Helsinki", "timestep=60"])

    for key in forecast.data.keys():
        forecast.data[key] = forecast.data[key]["Helsinki"]

    forecast_data = pd.DataFrame.from_dict(forecast.data, orient='index')

    #we can drop everything except Air temperature and Precipitation amount 1 hour

    simple_data = forecast_data[['Air temperature', 'Precipitation amount 1 hour']].copy()

    #each row for both columns contains a dictionary, so we extract the value for key 'value' from each dictionary

    simple_data['Air temperature'] = simple_data['Air temperature'].apply(lambda x: x['value'])
    simple_data['Precipitation amount 1 hour'] = simple_data['Precipitation amount 1 hour'].apply(lambda x: x['value'])

    #Now we can make a dataframe with the same columns as our training data 
    #and use the models to predict the number of departures and returns for each day

    predict_data = simple_data.reset_index()

    predict_data['Year'] = predict_data['index'].apply(lambda x: x.year - 2016)
    predict_data['Month'] = predict_data['index'].apply(lambda x: x.month)
    predict_data['Day'] = predict_data['index'].apply(lambda x: x.day)
    predict_data['Weekend'] = predict_data['index'].apply(lambda x: x.weekday() > 4)
    predict_data = predict_data.drop('index', axis=1)

    min_temp = predict_data.groupby(['Year', 'Month', 'Day', 'Weekend']).agg({'Air temperature': ['min']})
    max_temp = predict_data.groupby(['Year', 'Month', 'Day', 'Weekend']).agg({'Air temperature': ['max']})

    predict_data = predict_data.groupby(['Year', 'Month', 'Day', 'Weekend']).agg({'Precipitation amount 1 hour': ['sum'], 'Air temperature': ['mean']})
    predict_data = predict_data.merge(max_temp, on=['Year', 'Month', 'Day', 'Weekend'])
    predict_data = predict_data.merge(min_temp, on=['Year', 'Month', 'Day', 'Weekend'])
    predict_data.columns = ['Precipitation amount (mm)', 'Air temperature (degC)', 'Maximum temperature (degC)', 'Minimum temperature (degC)']
    predict_data = predict_data.reset_index()
    predict_data['Weekend'] = predict_data['Weekend'].apply(lambda x: 1 if x else 0)
    predict_data = predict_data[['Year', 'Month', 'Day', 'Precipitation amount (mm)', 'Air temperature (degC)', 'Maximum temperature (degC)', 'Minimum temperature (degC)', 'Weekend']]

    return predict_data
