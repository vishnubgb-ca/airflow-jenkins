import pandas as pd
import numpy as np
#from datavisualization import visualise_data
import boto3
import os

def feature_engineer():
    #data = visualise_data()
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    bucket_name = os.environ.get("Bucket_Name")
    s3 = boto3.client('s3', aws_access_key_id=access_key,
                          aws_secret_access_key=secret_key,
                          region_name='us-east-1')
    obj = s3.get_object(Bucket=bucket_name, Key='Student_Performance_Classifier/rawdata.csv')
    data = pd.read_csv(obj['Body'])
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
    categorical_features = data.select_dtypes("object").columns
    numerical_features = data.select_dtypes("number").columns
    # Outlier Treatment
    percentile25 = data['absences'].quantile(0.25)
    percentile75 = data['absences'].quantile(0.75)
    iqr = percentile75 - percentile25
    upper_limit = percentile75 + 1.5 * iqr
    lower_limit = percentile25 - 1.5 * iqr
    data['absences'] = np.where(
        data['absences'] > upper_limit,
        upper_limit,
        np.where(
            data['absences'] < lower_limit,
            lower_limit,
            data['absences']
        ))
    data['absences'] = data['absences'].astype(int) 
    # labelling the features
    data.replace({'sex':{'F':0,'M':1}},inplace=True)
    data.replace({'address':{'U':0,'R':1}},inplace=True)
    data.replace({'famsize':{'LE3':0,'GT3':1}},inplace=True)
    data.replace({'Pstatus':{'A':0,'T':1}},inplace=True)
    data.replace({'schoolsup':{'no':0,'yes':1}},inplace=True)
    data.replace({'famsup':{'no':0,'yes':1}},inplace=True)
    data.replace({'paid':{'no':0,'yes':1}},inplace=True)
    data.replace({'activities':{'no':0,'yes':1}},inplace=True)
    data.replace({'higher':{'no':0,'yes':1}},inplace=True)
    data.replace({'internet':{'no':0,'yes':1}},inplace=True)
    data.replace({'grade':{'L':0,'M':1,'H':2}},inplace=True)
    # Balancing the dataset
    grade_0_count, grade_1_count, grade_2_count =data['grade'].value_counts()
    grade_0 = data[data['grade'] == 0]
    grade_1 = data[data['grade'] == 1]
    grade_2 = data[data['grade'] == 2]
    grade_1_oversample = grade_1.sample(grade_0_count, replace=True)
    grade_2_oversample = grade_2.sample(grade_0_count, replace=True)
    data_balanced = pd.concat([grade_1_oversample, grade_2_oversample, grade_0], axis=0)
    data_balanced['grade'].groupby(data_balanced['grade']).count()
    data_balanced.to_csv("cleanseddata.csv",index=False)
    #csv_buffer = data_balanced.to_csv(index=False)
    #object_key = 'airflow-jenkins/cleanseddata.csv'
    #csv_buffer = data.to_csv(index=False)
    #s3.put_object(Bucket=bucket_name, Key=object_key, Body=csv_buffer)
    #print(f"CSV file uploaded to S3://{bucket_name}/{object_key}")
    print("cleansed_data:", data_balanced.head())

feature_engineer()
