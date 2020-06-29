#Importing needed libraries
import glob
import collections
import json
import pyodbc


conn = pyodbc.connect(
        'Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.5.so.2.1};'
        #Do not expose passwords
        #Changing driver for Mac
        #'Driver={ODBC Driver 17 for SQL Server};'
        'Server=localhost;'
        'Database=master;'
        'uid=sa;pwd=Password123')


#Defining schema for new table 
def create_schema():
        
        
        column_strings = []

        columns = ['patient_id', 'encounter_id', 'date', 'time_stamp', 'encounter_class','encounter_type', 'encounter_reason', 'condition_code','clinical_status', 'procedure_reason', 'procedure_code', 'observation_code', 'observation_unit','observation_value', 'observation_valueString', 'obervation_coding','component_code', 'component_value','component_unit','observation_text', 'dose_quantity','dose_additional_instruction', 'medication_type','dose_repeat_timeperiod', 'dose_repeat_frequency', 'dose_as_needed','dose_repeat_timeunit', 'dose_sequence','dose_add_instruct_text']

        table_name = "patient_timeline"
        for c in columns:
            column_strings.append(f"{c} VARCHAR(255)")

        column_strings = ','.join(column_strings)
        drop_statement = f"IF EXISTS (SELECT * FROM sysobjects WHERE id = object_id(N'[dbo].[{table_name}]') AND OBJECTPROPERTY(id, N'IsUserTable') = 1) DROP TABLE [dbo].[{table_name}]"
        create_statement = f"CREATE TABLE [{table_name}] (\n{column_strings})"

        with conn:
            try:
                cursor = conn.cursor()
                print(cursor)
                cursor.execute(drop_statement)
                cursor.commit()
                cursor.execute(create_statement)
                cursor.commit()
                print('Schema Created!')
            except pyodbc.ProgrammingError as e:
                import ipdb
                ipdb.set_trace()
                print(e)
            