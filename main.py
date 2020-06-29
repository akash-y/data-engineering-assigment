#Importing needed libraries 
import pyodbc
import pandas as pd
import numpy as np
import yaml
import modules as m
import new_populate as n


### TASK 2

#Creating schema for patient timeline dataframe
n.create_schema()

#Reading username-password from config file

with open('config.yaml','r') as yaml_file:
    config = yaml.load(yaml_file, Loader=yaml.Loader)

    Conf = config['database']
    user = Conf['uid']
    password = Conf['password']

    conn = pyodbc.connect(
        'Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.5.so.2.1};'
        #Changing driver for MAC
        #'Driver={ODBC Driver 17 for SQL Server};'
        'Server=localhost;'
        'Database=master;'
        'uid=%s;'
        'pwd=%s;'
        'MARS_Connection=Yes' % (user,password))

#Defining a function to insert rows into patient timeline dataframe after all merges and preprocessing
def load_data(df):
    cursor = conn.cursor()
     
    #Inserting each row 
    for index, row in df.iterrows():
        cursor.execute("INSERT INTO patient_timeline([patient_id],[encounter_id],[date],[time_stamp],[encounter_class],[encounter_type],[encounter_reason],[condition_code],[clinical_status],[procedure_reason],[procedure_code],[observation_code],[observation_unit],[observation_value],[observation_valueString],[obervation_coding] ,[component_code],[component_value],[component_unit],[observation_text],[dose_quantity],[dose_additional_instruction],[medication_type],[dose_repeat_timeperiod],[dose_repeat_frequency],[dose_as_needed],[dose_repeat_timeunit],[dose_sequence],[dose_add_instruct_text]) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", row['patient_id'], row['encounter_id'], row['date'], row['time_stamp'],row['encounter_class'],row['encounter_type'],row['encounter_reason'],row['condition_code'],row['clinical_status'],row['procedure_reason'],row['procedure_code'],row['observation_code'],row['observation_unit'],row['observation_value'],row['observation_valueString'],row['obervation_coding'],row['component_code'],row['component_value'],row['component_unit'],row['observation_text'],row['dose_quantity'],row['dose_additional_instruction'],row['medication_type'],row['dose_repeat_timeperiod'],row['dose_repeat_frequency'],row['dose_as_needed'],row['dose_repeat_timeunit'],row['dose_sequence'],row['dose_add_instruct_text'])
        conn.commit()
    #Closing connection
    cursor.close()
    conn.close()
    
#Running the merge and preprocessing steps
def main():

    #Accessing data dictionary
    col_info = pd.read_csv('col_info.csv')

    #Loading datasets directly from MSSQL 
    encounter_df = m.sql_reader("encounter",conn)
    condition_df = m.sql_reader("condition",conn)
    procedure_df = m.sql_reader("procedure",conn)
    observation_df = m.sql_reader("observation",conn)
    medicationrequest_df = m.sql_reader("medicationrequest",conn)

    #Creating time-stamp for encounter and procedure tables
    encounter_df['time_stamp'] = encounter_df.apply(m.encounter_timestamp, axis=1)
    procedure_df['p_time_stamp'] = procedure_df.apply(m.procedure_timestamp, axis=1) 
    
    #Renaming columns using data dictionary
    m.col_rename(col_info,encounter_df,'encounter_df')
    m.col_rename(col_info,condition_df,'condition_df')
    m.col_rename(col_info,procedure_df,'procedure_df')
    m.col_rename(col_info,observation_df,'observation_df')
    m.col_rename(col_info,medicationrequest_df,'medicationrequest_df')

    #Creating date-time columns for each table
    m.extract_datetime(encounter_df,'time_stamp')
    m.extract_datetime(condition_df,'c_time_stamp')
    m.extract_datetime(procedure_df,'p_time_stamp')
    m.extract_datetime(observation_df,'o_time_stamp')
    m.extract_datetime(medicationrequest_df,'m_time_stamp')

    #Merging datasets after subsetting columns and specifying joining parameters 
    encounter_params = ['patient_id','encounter_id','date','time_stamp','encounter_class','encounter_type','encounter_reason']
    condition_params = ['patient_id','encounter_id', 'condition_code','date','c_time_stamp','clinical_status']
    procedure_params = ['patient_id','encounter_id','procedure_reason','date','p_time_stamp','procedure_code']
    observation_params = ['patient_id','encounter_id','date','o_time_stamp','observation_code','observation_unit',
                      'observation_value','observation_valueString','obervation_coding','component_code',
                      'component_value','component_unit','observation_text']
    medication_params = ['patient_id','encounter_id','m_time_stamp','date','dose_quantity','dose_additional_instruction',
                     'medication_type','dose_repeat_timeperiod','dose_repeat_frequency','dose_as_needed',
                     'dose_repeat_timeunit','dose_sequence','dose_add_instruct_text']

    on_condition = ['patient_id','encounter_id','date']

    join_type = "left"

    #Merge steps
    df = m.merge_op(encounter_df,condition_df,encounter_params,condition_params,on_condition,join_type)
    df_params = m.update_params(df)
    df = m.merge_op(df,procedure_df,df_params,procedure_params,on_condition,join_type)
    df_params = m.update_params(df)
    df = m.merge_op(df,observation_df,df_params,observation_params,on_condition,join_type)
    df_params = m.update_params(df)
    df = m.merge_op(df,medicationrequest_df,df_params,medication_params,on_condition,join_type)
    
    #Converting the dataframe into longitudnal having each patient_id and their entire timeline in a vertical format and sorting by patient id and timeline
    df = pd.concat([df[encounter_params], 
                df[condition_params].rename(columns={'c_time_stamp': 'time_stamp'}),
                df[procedure_params].rename(columns={'p_time_stamp': 'time_stamp'}),
                df[observation_params].rename(columns={'o_time_stamp': 'time_stamp'}),
                df[medication_params].rename(columns={'m_time_stamp':'time_stamp'})]).dropna(how='all').sort_values(['patient_id','date','time_stamp','encounter_id'], ascending=[True, True, True, True])
    
    #Dropping time_stamps with NA values
    df = df.dropna(axis=0, subset=['time_stamp'])
    
    #Filling NA's with 0  
    df = df.fillna(value=0)
    
    print(df.shape)
    
    
    for index,row in df.iterrows():
        print(row['patient_id'])
        break
    
    load_data(df)
    
main()

###TASK 3

#Defining a function to vectorize the values from patients_timeline table
def vectorize():
    #Accessing key-vault file
    with open('config.yaml','r') as yaml_file:
        config = yaml.load(yaml_file, Loader=yaml.Loader)

        Conf = config['database']
        user = Conf['uid']
        password = Conf['password']
        
        conn = pyodbc.connect(
            'Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.5.so.2.1};'
            #'Driver={ODBC Driver 17 for SQL Server};'
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