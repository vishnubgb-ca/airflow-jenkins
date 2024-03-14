from data_analysis import analyse_data
import numpy as np
import pandas as pd

def data_preprocess():
    data, num_features, cat_features  = analyse_data()
    data['score'] = ((data["G1"]+data["G2"]+data["G3"])/60)*100
    # create a list of our conditions
    conditions = [
        (data['score'] <= 69),
        (data['score'] >= 70) & (data['score'] <= 89),
        (data['score'] >= 90)
        ]
    # create a list of the values we want to assign for each condition
    values = ['L', 'M', 'H']
    # create a new column and use np.select to assign values to it using our lists as arguments
    data['grade'] = np.select(conditions, values)
    data.drop(['Unnamed: 0', 'school', 'Mjob', 'Fjob', 'reason', 'guardian', 'nursery', 'romantic', 'famrel', 'Dalc', 'Walc', 'G1', 'G2', 'G3', 'score'], axis=1, inplace=True)
    data['score'] = ((data["G1"]+data["G2"]+data["G3"])/60)*100
    # create a list of our conditions
    conditions = [
        (data['score'] <= 69),
        (data['score'] >= 70) & (data['score'] <= 89),
        (data['score'] >= 90)
        ]
    # create a list of the values we want to assign for each condition
    values = ['L', 'M', 'H']
    # create a new column and use np.select to assign values to it using our lists as arguments
    data['grade'] = np.select(conditions, values)
    data.drop(['Unnamed: 0', 'school', 'Mjob', 'Fjob', 'reason', 'guardian', 'nursery', 'romantic', 'famrel', 'Dalc', 'Walc', 'G1', 'G2', 'G3', 'score'], axis=1, inplace=True)
    print(data.head())
    categorical_features = data.select_dtypes("object").columns
    numerical_features = data.select_dtypes("number").columns
    return data, numerical_features, categorical_features

data_preprocess()
