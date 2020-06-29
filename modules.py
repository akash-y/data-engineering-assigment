#importing necessary libraries
import pyodbc
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import yaml

def sql_reader(table,conn):
    query = "SELECT * from [dbo].[%s]" % (table);
    table = pd.read_sql(query, conn)
    return table

def encounter_timestamp(row):
    if row['period_start'] < row['period_end']:
        val = row['period_end']
    else:
        val = row['period_start']
    return val

def procedure_timestamp(row):
    if row['performedPeriod_start'] < row['performedPeriod_end']:
        val = row['performedPeriod_end']
    else:
        val = row['performedPeriod_start']
    return val

def col_rename(col_info,table,t_filter):
    table.rename(columns=col_info.loc[col_info['table_name'] == t_filter].set_index(['column_name'])['alias'], inplace=True)
    
def extract_datetime(table,time_col): 
    table[time_col] = pd.to_datetime(table[time_col])
    table['date'] = table[time_col].dt.date
    table[time_col] = table[time_col].dt.time
    
def merge_op(df1,df2,df1_params,df2_params,join_param,join_cond):
    df = pd.merge(df1[df1_params],df2[df2_params],on=join_param,how=join_cond)
    return df

def update_params(table):
    df_params = list(table.columns)
    return df_params