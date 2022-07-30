import pandas as pd
import numpy as np
import datetime
import re
from pandas.tseries.holiday import USFederalHolidayCalendar

def clean_ercot_datetime(df):
    '''
    This function is designed to take in our coast_df.csv and clean up the datetimes that were provided.
    - gets dates in same format and stored as datetime
    - adjusts any 24:00 entries to be 00: the following day
    - Stores the datetime as the index
    
    Returns: Pandas Dateframe - w/ datetime index and load column
    Parameters: df: pandas dataframe - expecting our coast_df.csv file
    '''
    # 1. Pull out first 16 characters
    df.datetime = df.datetime.str[:16]
    # 2. Deconstruct into date and time columns
    df['date'] = df.datetime.str[:10]
    df['time'] = df.datetime.str[-5:]
    # 3. Convert date column into datetime format
    df['date'] = pd.to_datetime(df.date)
    
    # 4. Find any time where starts with 24, then for that index, add one day to to date column then update time to 00
    #For all indices w/ a time that starts with 24, add one day to the date
    df.loc[df.time.str.startswith('24'),'date'] = df.date + datetime.timedelta(days=1)
    #Replace all '24:' in time with '00:'
    df.time = df.time.apply(lambda x: re.sub(r'24:','00:',x))

    # 5. Convert date column back to string and Concat date and time column >> datetime
    df['new_datetime'] = df.date.astype(str) + ' ' + df.time
    
    # 6. Convert new datetime column to datetime
    df['new_datetime'] = pd.to_datetime(df.new_datetime)
    
    # 7. Perform dt.round
    df.new_datetime = df.new_datetime.dt.round("H")
    
    # 8. Drop old date/time columns and index
    df.drop(columns=['datetime','date','time','Unnamed: 0'],inplace=True)
    
    # 9. Rename datetime column and set as index
    df.rename(columns={'new_datetime':'datetime'},inplace=True)
    df = df.set_index('datetime').sort_index()
    
    return df

def create_day_columns(df2):
    '''
    Expects the cleaned ERCOT dataframe, returns the dataframe with new columns for:
    - dow: Day of week (category EX: Monday)
    - is_weekday: 1 if day is a weekday (M-F), else 0
    - is_obs_holiday: 1 if day is the observed holiday of a US Federal holiday. (only lands on weekdays)
    
    '''
    #create day of week category
    df2['dow'] = df2.index.day_name()
    #create bool is_weekday column
    df2['is_weekday'] = df2.dow.apply(lambda x: 0 if x in (['Saturday','Sunday']) else 1)
    
    #get holiday information
    start = df2.index[0] - datetime.timedelta(days=1) #this is need b/c it will skip 1/1/2010 (I think b/c it starts at one hour into that day)
    end = df2.index[-1] + datetime.timedelta(days=1)
    obsholidays = cal.holidays(start, end) #returns datetime index
    #Create is observed holiday column
    df2['is_obs_holiday'] = pd.Series(df2.index,index=df2.index).dt.date.isin(obsholidays.date).astype(int)
    
    return df2

def prep_ercot():
    '''
    Preps and the ercot dataframe - requires coast_df.csv file in working directory
    
    Returns: Pandas Dataframe
    '''
    #load ercot data
    df = pd.read_csv('coast_df.csv')
    
    #clean up datetime info
    df = clean_ercot_datetime(df)
    
    #create new day type features
    df = create_day_columns(df)
    
    return(df)

def get_ercot_df():
    '''
    Retrieves ERCOT data from local csv, and returns as dataframe
    '''
    return pd.read_csv('prepped_ercot.csv',index_col='datetime',parse_dates=['datetime'])