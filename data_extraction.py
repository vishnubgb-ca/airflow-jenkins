import pandas as pd
import os
import boto3

#data = pd.read_csv('data.csv')
#print(data.head())
    
'''s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-1',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
)'''

def read_csv_from_s3():
    s3 = boto3.client('s3', aws_access_key_id=$access_key,
                      aws_secret_access_key=$secret_key,
                      region_name='us-east-1')
 
    obj = s3.get_object(Bucket='mlangles-githubrepos', Key='Student_Performance_Classifier/data.csv')
    data = pd.read_csv(obj['Body'])
    print(data.head())
    return data

read_csv_from_s3()
