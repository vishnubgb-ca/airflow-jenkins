import pandas as pd
import os
import boto3

#data = pd.read_csv('data.csv')
#print(data.head())
access_key = os.environ.get("AWS_ACCESS_KEY_ID")
secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
bucket_name = os.environ.get("Bucket_Name")

def read_csv_from_s3():
    s3 = boto3.client('s3', aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key,
                      region_name='us-east-1')
    obj = s3.get_object(Bucket='mlanglesdev', Key='Student_Performance_Classifier/data.csv')
    data = pd.read_csv(obj['Body'])
    print(data.head())
    return data

def upload_csv_to_s3(data, object_key):
    #data = pd.read_csv(csv_file_path)
    s3 = boto3.client('s3', aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key,
                      region_name='us-east-1')
    
    csv_buffer = data.to_csv(index=False)
    s3.put_object(Bucket='mlanglesdev', Key=object_key, Body=csv_buffer)
    print(f"CSV file uploaded to S3://mlanglesdev/{object_key}")

data = read_csv_from_s3()
object_key = 'Student_Performance_Classifier/rawdata.csv'
upload_csv_to_s3(data, object_key)
