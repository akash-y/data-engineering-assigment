import glob
import collections
import json
import pyodbc

conn = pyodbc.connect(
        'Driver={/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.5.so.2.1};'
        'Server=localhost;'
        'Database=master;'
        'uid=sa;pwd=Password123')

def create_schema():
    schema_configuration, dataset = load_resources()

    for table_name, columns in schema_configuration.items():
        column_strings = []
        for c in columns:
            column_strings.append(f"{c} VARCHAR(255)")

        column_strings = ','.join(column_strings)
        drop_statement = f"IF EXISTS (SELECT * FROM sysobjects WHERE id = object_id(N'[dbo].[{table_name}]') AND OBJECTPROPERTY(id, N'IsUserTable') = 1) DROP TABLE [dbo].[{table_name}]"
        create_statement = f"CREATE TABLE [{table_name}] (\n{column_strings})"

        with conn:
            try:
                cursor = conn.cursor()
                cursor.execute(drop_statement)
                cursor.commit()
                cursor.execute(create_statement)
                cursor.commit()
            except pyodbc.ProgrammingError as e:
                import ipdb
                ipdb.set_trace()
                print(e)

    for table_name, data_points in dataset.items():
        columns = schema_configuration[table_name]
        columns_string = ','.join(columns)

        for data in data_points:
            values = []
            insert_statement = f"INSERT INTO [{table_name}] ({columns_string}) VALUES"
            for column in columns:
                column_data = str(data.get(column, 'NULL'))
                column_data = column_data.replace('-', '')
                column_data = column_data.replace('\'', '')
                if 'id' in column:
                    column_data = 'a' + column_data
                values.append(column_data)

            values = ','.join([f"'{v}'" if v != 'NULL' else f"{v}" for v in values])
            try:
                insert_statement += f"({values})\n"
            except Exception as e:
                # import ipdb
                # ipdb.set_trace()
                print('asd')

            insert_statement += ';'
            print(insert_statement)
            with conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute(insert_statement)
                    cursor.commit()
                except pyodbc.ProgrammingError as e:
                    import ipdb
                    ipdb.set_trace()
                    print(e)


def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        if isinstance(v, list):
            v = v[0]

        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def load_resources():
    resource_columns = collections.defaultdict(set)
    flatten_dataset = collections.defaultdict(list)
    for file in glob.glob('patients/*.json'):
        with open(file, 'r') as f:
            data = json.load(f)
            for item in data:
                flatten_data = flatten(item)
                if 'resourceType' in flatten_data:
                    del flatten_data['resourceType']

                flatten_dataset[item['resourceType'].lower()].append(flatten_data)
                resource_columns[item['resourceType'].lower()].update(
                    set(flatten_data.keys()))


                # print(flatten(item).keys())

        print(dict(resource_columns))
    return dict(resource_columns), flatten_dataset

create_schema()