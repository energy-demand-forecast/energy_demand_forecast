import pandas as pd
import numpy as np
import datetime
import re
import os
from pandas.tseries.holiday import USFederalHolidayCalendar
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import Markdown, display

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

    #7.5 FIX TIME ZONES ######
    #Indices to be adjusted
    mar_adj_ind = [71809, 80545, 89281, 98017, 106921, 115657]
    nov_adj_ind = [68784, 59880, 51144, 42408, 33672, 24936, 16200, 7296, 77520, 86256, 94992, 103728, 112632]
    # to the March, we are adding 1 hour to the 2am time 
    #. b/c ERCOT skips 3am, when it should skip 2am
    df.loc[mar_adj_ind,'new_datetime'] = df.loc[mar_adj_ind,'new_datetime'] + datetime.timedelta(hours=1)

    #to the November, we are subtracting 1 hour from the first 2am, 
    #  as there are supposed to be two 1ams, not two 2ams
    df.loc[nov_adj_ind,'new_datetime'] = df.loc[nov_adj_ind,'new_datetime'] - datetime.timedelta(hours=1)
    #Make Time Zone aware
    df = df.set_index('new_datetime').tz_localize(tz='US/Central',ambiguous='infer')

    ################
    
    # 8. Drop old date/time columns and index
    df.drop(columns=['datetime','date','time','Unnamed: 0'],inplace=True)
    
    # 9. Rename datetime column and set as index
    # df.rename(columns={'new_datetime':'datetime'},inplace=True)
    # df = df.set_index('datetime').sort_index()
    # 10. Fill the null values using Series.interpolate that uses average
    # of close values (an hour apart in our case)
    df.ercot_load.interpolate(method='time',limit_direction='both', inplace=True)
    
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
    #create calendar
    cal = USFederalHolidayCalendar()
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

    #trim data timeframe
    df = df.loc['2010-01':'2022-06']
    
    #create new day type features
    df = create_day_columns(df)
    
    return(df)

def get_ercot_df():
    '''
    Retrieves ERCOT data from local csv, and returns as dataframe
    '''
    #set filename
    filename = 'prepped_ercot.csv'

    if os.path.isfile(filename):
        #If file exists, go ahead and grab that csv
        return pd.read_csv(filename,index_col='new_datetime',parse_dates=['new_datetime'])
    else: 
        #re-prep this data from coast_df.csv
        df = prep_ercot()
        #Save this dataframe to a csv
        df.to_csv(filename)
        return df
    
def get_combined_df(get_central = True):
    '''
    Retrieves a cleaned, combined DataFrame of energy demand
    and weather data. Returns as a DataFrame.
    '''
    #If file exists, grab the CSV
    df = pd.read_csv('combined_df.csv', index_col = 'datetime', parse_dates = ['datetime'], date_parser = lambda col: pd.to_datetime(col, utc = True))
    if get_central == True:
        #Converting UTC to CST
        return df.tz_convert('US/Central')
    else:
        return df

def get_prophet_df(get_central=True):
    '''
    Retrieves a cleaned dataframe and formats it for input into
    the FB Prophet model.

    Parameters:
      (O) get_central: Bool (Default True) - Return the datetime index in US/Central time. False returns UTC.  
    '''
    #Acquire combined dataframe
    df = get_combined_df(get_central = get_central)
    #Pull index/load data into new 
    df2 = pd.DataFrame(df.ercot_load)
    #Move index out
    df2.reset_index(drop=False, inplace=True)
    #Rename columns
    df2.rename(columns = {'datetime':'ds','ercot_load':'y'},inplace=True)
    
    return df2

def get_prophet_df_w_meantemp():
    '''
    Retrieves a cleaned dataframe and formats it for input into
    the FB Prophet model.
    
    NOTE: Prophet does not support timezone - need it in UTC, then make tz naive
    '''
    #Acquire combined dataframe
    df = get_combined_df(get_central = False)
    #Calculate mean_temp column
    df['mean_temp'] = (df.hs_temp + df.gv_temp + df.pl_temp + df.vc_temp)/4

    #Pull index/load/temp data into new dataframe
    df2 = pd.DataFrame(df[['ercot_load','mean_temp']])

    #Move index out
    df2.reset_index(drop=False, inplace=True)
    #Rename columns
    df2.rename(columns = {'datetime':'ds','ercot_load':'y'},inplace=True)
    #Make TZ naive
    df2.ds = df2.ds.dt.tz_localize(None)
    
    return df2
    
def print_model_results(name,df_p_1d,df_p_3d):
    #Print model name
    print(f'\033[1m{name} model performance:\033[0m')
    #grab model stats
    rmse1 = df_p_1d.loc[0,'rmse']
    mape1 = df_p_1d.loc[0,'mape']*100
    rmse3 = df_p_3d.loc[0,'rmse']
    mape3 = df_p_3d.loc[0,'mape']*100
    print(f'1 day rmse: {round(rmse1,0)} MW')
    print(f'1 day mape: {round(mape1,1)}%')
    print(f'3 day rmse: {round(rmse3,0)} MW')
    print(f'3 day mape: {round(mape3,1)}%')
    return None

#### EXPLORE FUNCTIONS ######
def plot_temp_ercot(train):
    sns.scatterplot(data=train, x='mean_temp',y='ercot_load')
    plt.xlabel('Mean Temperature (°F)',fontsize=16)
    plt.ylabel("Coastal ERCOT Demand (MW)",fontsize=16)
    plt.axvline(x=(50),color='black',ls='--', label = 'Temperature Range Cutoff')
    plt.legend(loc = 'upper left', fontsize = 16)
    plt.axvline(x=(70),color='black',ls='--')
    plt.title("ERCOT Demand and Mean Temperature",fontsize=18)
    plt.show()

def temp_subgroups(train):
    less_50 = train[train.mean_temp <=50]
    mid_temp = train[(train.mean_temp>50)& (train.mean_temp<70)]
    greater_70 = train[train.mean_temp >=70]
    return less_50, mid_temp, greater_70

def plot_weekday_energy(train):
    reg_days = train[train.is_obs_holiday == 0].copy()
    display(Markdown('### Energy Use by Weekday'));
    ax = reg_days.groupby([reg_days.dow, reg_days.index.hour]).ercot_load.mean().unstack(0).plot()
    holly_days = train[train.is_obs_holiday == 1].copy()
    holly_days.groupby([holly_days.index.hour]).ercot_load.mean().plot(label = 'Holiday', ax = ax, ls = '--')
    #Reorder legend
    handles, labels = ax.get_legend_handles_labels()
    handles = [handles[1]] + handles[5:7] + [handles[4]] + [handles[0]] + handles[2:4] + [handles[7]]
    labels = [labels[1]] + labels[5:7] + [labels[4]] + [labels[0]] + labels[2:4] + [labels[7]]
    plt.title('Average ERCOT Demand by Hour and Day of Week',fontsize=18)
    plt.xlabel('Hour of Day',fontsize=16)
    plt.ylabel('ERCOT Demand (MW)',fontsize=16)
    #plt.legend()
    plt.legend(handles=handles,labels=labels,title=None,fontsize=14)
    plt.show()
    return None

##### UTILS #####

# Getting Mean Absolute Percentage Error#

def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) 