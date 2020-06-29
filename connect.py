import pyodbc

conn = pyodbc.connect(
    'Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.5.so.2.1};'
    #Changing driver for Mac
    #'Driver={ODBC Driver 17 for SQL Server};'
    'Server=localhost;'
    'Database=master;'
    'uid=sa;pwd=Password123')


def test_connection():
    with conn:
        try:
            cursor = conn.cursor()
            result = cursor.execute("SELECT * FROM encounter;")
        except pyodbc.ProgrammingError as e:
            print(f'DB access failed: {e}')
        else:
            print('Success')

test_connection()
