import pandas as pd
import os

def load_data():
    data = pd.read_csv('data.csv')
    print(data.head())
    return data

load_data()
