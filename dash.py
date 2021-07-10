### IMPORT THE REQUIRED LIBRARIES ###
import pandas as pd
import os
from datetime import datetime,timedelta

### HANDLE DIRECTORY AND FILE NAMES IN THE PROJECT ###

### Get the parent directory name of the present python file ###
parentdirname = os.path.dirname(__file__)

### Get the folder name in which the excle file is present ###
filedirname = os.path.join(parentdirname,'Files')

### Get the File name in the files direcory ### Get
filename = os.listdir(os.path.join(filedirname))[0]

### FUNCTION TO IMPORT BASE DATA ###
def get_data(path,filename):
    '''Takes path and filename and returns the pandas dataframe'''
    df = pd.read_excel(os.path.join(path,filename))
    return df

### FUNCTION TO PRINT COLUMN NAMES & COLUMN TYPES OF DATASET ###
def describe_columns(dataset):
    '''Prints the column type and column names of the supplied dataset'''
    print(dataset.columns)
    print(dataset.dtypes)

### FUNCTION TO FILTER DATASET BY START AND END DATE AND SUMMARIZE THE RESULT ### 
def summarize_by_range(dataset, nature,start_date=pd.to_datetime('2000-01-01'), end_date = pd.to_datetime("today"), nature_column='MAIN', date_column='DATE',
                   amount_column='AMOUNT'):
    '''Filters the dataset by given daterange and summarizes the amount accounted
    during the period. Date to be provided in "YYYY-mm-dd" format'''
    # convert input start date and end date to datetime format
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    # Find the duration betweeen start and end date
    diff_days = (end_date - start_date).days
    
    # Find the previous period duration from the given start and end date
    previous_period_start = start_date - timedelta(days=diff_days)
    previous_period_end = start_date - timedelta(days=1)
    
    # Filter the dataset by dates    
    present_df = dataset[(dataset[date_column] >= start_date) & (dataset[date_column] <= end_date) & (dataset[nature_column] == nature)]
    previous_df = dataset[(dataset[date_column] >= previous_period_start) & (dataset[date_column] <= previous_period_end) & (dataset[nature_column] == nature)]
    
    # Prepare the Pivot Table and summarize by sum
    present_result = pd.pivot_table(present_df,index=nature_column,values=amount_column,aggfunc='sum')
    previous_result = pd.pivot_table(previous_df,index=nature_column,values=amount_column,aggfunc='sum')
    
    # Since pivot table is a dataframe, just get the amount
    previous_result = round(previous_result[amount_column][0],2)
    present_result = round(present_result[amount_column][0],2)
    
    # Calculate the % Increase or Decrease
    perc_change = round(((present_result - previous_result) / (previous_result))*100,2)
    
    return previous_result, present_result, perc_change
    
###################################### END OF LOGICS ######################################

### IMPLEMENTATION OF ABOVE LOGIC ###

df = get_data(filedirname,filename)    

describe_columns(df)

present, previous, percentage_change = summarize_by_range(df,'Income','2019-05-1','2019-05-31')

print(present, previous, percentage_change)


