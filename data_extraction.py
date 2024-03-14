import pandas as pd
import os
import boto3

#data = pd.read_csv('data.csv')
#print(data.head())
    
s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-1',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key
)
