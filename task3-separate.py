#Importing needed libraries
import pyodbc
import pandas as pd
import numpy as np
import yaml
import modules as m
import new_populate as n

#Defining a function to vectorize the values from patients_timeline table
def vectorize():
    #Accessing key-vault file
    with open('config.yaml','r') as yaml_file:
        config = yaml.load(yaml_file, Loader=yaml.Loader)
        Conf = config['database']
        user = Conf['uid']
        password = Conf['password']
        
    conn = pyodbc.connect(
        #'Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.5.so.2.1};'
        'Driver={ODBC Driver 17 for SQL Server};'
        'Server=localhost;'
        'Database=master;'
        'uid=%s;'
        'pwd=%s;'
        'MARS_Connection=Yes' % (user,password))

    #Reading the data
    patient_feature = m.sql_reader("patient_timeline",conn)

    #Listing columns to drop
    drop_cols = ['observation_unit','component_unit','date','time_stamp']

    #Dropping necessary columns
    patient_feature = patient_feature.drop(columns = drop_cols)

    #Replacing "nan","None" with None if any
    patient_feature['component_value'] = patient_feature['component_value'].replace(['nan', 'None'], None)

    #Changing dtypes for numerical columns to float
    patient_feature['observation_value'] = patient_feature['observation_value'].astype(float)
    patient_feature['component_value'] = patient_feature['component_value'].astype(float)
    patient_feature['dose_quantity'] = patient_feature['dose_quantity'].astype(float)

    #Listing all categorical variables
    cat_cols = ['encounter_class','encounter_type','encounter_reason','condition_code','clinical_status','procedure_code',
           'procedure_reason','observation_code','observation_value','observation_valueString','obervation_coding',
           'component_code','observation_text','dose_quantity','dose_additional_instruction','medication_type',
           'dose_repeat_timeperiod','dose_repeat_frequency','dose_as_needed','dose_repeat_timeunit','dose_sequence',
           'dose_add_instruct_text']

    #Factorising categorical variables
    patient_feature = pd.get_dummies(data = patient_feature, columns= cat_cols)

    #Creating feature vector as an array
    feature_vector = patient_feature.values

    #Printing top 10 results
    print(feature_vector[:10])

vectorize()
