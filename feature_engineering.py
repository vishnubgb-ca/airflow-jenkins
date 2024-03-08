import pandas as pd
import numpy as np
from datavisualization import visualise_data

def feature_engineer():
    data = visualise_data()
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
    data_balanced.to_csv('student_performance_cleansed_data.csv', index=False)
    return data_balanced

feature_engineer()