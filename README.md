# Solution

Task 1 available as a jupyter notebook. Task 2 and Task 3 are available in the main.py file. 

modules.py contains functions for preprocessing and merging

new_populate.py contains code for creating a new schema to insert the patient_timeline df into 

col_info.csv is a data dictionary for mapping alias of column names and for describing table and column features (ideal for non-technical audiences) 

config.yaml lists usernames and passwords

docker-compose.yaml and requirements.txt has been modified 


Things to note: 
1. Changed drivers for Mac while working on the solution (changed it back to default while submitting)
2. docker-compose up couldnt run on Mac. As a get-around created a new container and copied contents. Faced similar issues while dockerising the application. 


# Problem Description

We are excited to welcome you our take home assignment!

This assignment is part of application for the data engineering position at healthplusAI

Your task is to load data from MSSQL database, analyze medical data present and plot your findings in the dataset.

The code has to be written in Python, data processing part should be ideally dockerized and solution should be published on public github account. Clone or fork this project and modify it to your liking. All components and instructions are made on unix system, and so should be the assigment.

When you are happy with your solution share a git link to your solution.

# Setting up the MSSQL

There is a docker-compose.yaml file present, to be able to run the database you will need [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/) installed

For connecting to the MSSQL you will need to install [ODBC Driver](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15)

Starting MSSQL:

```bash
docker-compose up -d mssql
```

Example connection string can be found and tested using:
```bash
python connect.py
```

# Data structure

Please explore the data structure, there are 5 different tables:
```
encounter
codnition
procedure
observation
medicationrequest
```

Every table has the following schema:

```
id
patient_id
datetime-based feature
and other features
```

# Assigment
1. explore the data and present your findings using visualizations (jupyter notebook with plots please)
2. create a timeseries dataset, where each record is a timeline for each patient based on datetime feature in all tables - this should ideally be runnable as docker container
3. extract features from all tables and combine them into a single feature vector, indexed by patient_id and datetime feature - this should ideally be runnable as docker container

# Notes
We do not expect that you will complete everything. That's perfectly OK! But, please, make sure to acompany your code with comments as you go, commit often with commit messages.
If you get stuck on something, write down your intentions and how you would solve the rest of the tasks. Answer what, why and how you would like to accomplish.
We want to understand your thought process!

Data:

If you have problem to load mssql from volume, please remove content of mssqldata folder and run:

```bash
pip install -r requirements.txt
python populate.py
```



