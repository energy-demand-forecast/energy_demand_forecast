# Energy Demand Forecast
*Audience: Data Science Teams for Energy Grid Operators*


<hr style="background-color:silver;height:3px;" />

## Project Summary
<hr style="background-color:silver;height:3px;" />
There is a need for accurate energy demand forecasting in order for ERCOT to schedule energy generation and inform bidding prices. We analyzed historical weather data and ERCOT demand from 2010-2022 in order to create a time-series model to predict a three day forecast for energy demand in ERCOT's coastal region. Through exploration we examined the relationship between weather and ERCOT demand, as well as, date/time information and ERCOT demand. We utilized time-series models (Holt Winters and Facebook Prophet) to forecast ERCOT demand for a three-day period. The top performing model was a tuned Prophet model. It had a 3 day MAPE of 8.5% over the Test subset, compared to baseline's performance of 18.8%. We suggest deploying this model to predict energy demand, allowing for informed energy generation capacity planning.

### Project Deliverables
> - A final report notebook
> - Python modules for automation and to facilitate project reproduction
> - Presentation 19 August 2022 (slides)
> - Notebooks that show:
>  - Data acquisition and preparation 
>  - exploratory analysis not included in final report
>  - model creation, refinement and evaluation

### Initial questions on the data

Weather and Energy Demand:
>   - How does temperature impact energy demand? 
>   - Does humidity impact energy demand?

Date/Time and Energy Demand:
>   - How does the day of the week impact energy demand?
>   - Does the time of day impact energy demand?
>   - How does energy demand differ on holidays?

---

<hr style="background-color:silver;height:3px;" />

## Executive Summary
<hr style="background-color:silver;height:3px;" />

**Project Goal:**
Produce a time-series model that forecasts three days of energy demand in ERCOT's coastal region. Deploying this model will allow ERCOT to anticipate demand effectively in order to schedule energy generation and inform bidding prices.

**Discoveries and Recommendations**

Key Findings:
> - Temperature has a strong correlation with ERCOT energy demand when the temperature is above 70 degrees and a moderate correlation when the temperature is below 50 degrees.
> - Weekdays require more energy demand than the weekend.
> - Holidays use less demand than non-holidays.
> - Energy demand is lowest at 0400 and begins to increase shortly after. Energy demand peaks at 1700, and then gradually declines back to the lowest point.
> - The top performing model was a tuned Prophet model. It had a 3 day MAPE of 8.5% over the Test subset, compared to baseline's performance of 18.8%.
> - We did not see significant improvements in 1 day MAPE compared to 3 day MAPE for the Prophet models, however Holts-Winters performed significantly beter over the shorter time period.

Recommendations:
> - We suggest deploying this model to predict energy demand, allowing for informed energy generation capacity planning.
> - Utilizing uniform data entry processes in regards to date and time would ease in future acquisition of data.

Next Steps:
> - Review how load data is written and stored for more reliable acquisition and preparation for the model. Currently, the datetime format changes throughout the historical data. It would also be beneficial to have this information stored in UTC.
> - Use historical weather forecasts compared with actual weather to create uncertainty bands for the model
> - Add additional holidays. For example, while the day after Thanksgiving is not a holiday, it likely has a distinct energy demand pattern that differs from a standard Friday.
> - Create LSTM models. These will like better be able to forecast as they will use long-term historical data for day type patterning combined with short term historical data for time series forecasting.



<hr style="background-color:silver;height:3px;" />

## Data Dictionary
<hr style="background-color:silver;height:3px;" />

|Target|Definition|
|:-------|:----------|
| ercot_load| ERCOT's energy load for the coastal region - measured in megawatts(MW)|

|Feature|Definition|
|:-------|:----------|
| dow | Day of the week. Mon-Sun |
| is_weeekday | 1 = weekday 0 = weekend |
| is_obs_holiday | 1 = holiday 0 = non-holiday|
| hs_temp | Temperature in Fahrenheit in Houston |
| hs_feelslike | Combination of temperature, wind chill & heat index in Houston|
| hs_dew | Dew point in Houston |
| hs_humidity | Relative humidity in Houston|
| hs_precip | Amount of liquid equivalent precipitation (rain, snow etc.) in Houston |
| hs_windgust | Instantaneous speed of wind in Houston|
| hs_windir | Two minute average of wind direction in Houston|
| hs_sealevelpressure | Sea level pressure in Houston| 
| hs_cloudcover | Percentage of sky that is covered by cloud in Houston|
| hs_visibility | Distance that can be viewed in Houston|
| hs_solarradiation | Solar radiation in Houston |
| hs_solarenergy | Solar energy in Houston |
| hs_uvindex | UV index in Houston |
| gv_temp | Temperature in Fahrenheit in Galveston |
| gv_feelslike | Combination of temperature, wind chill & heat index in Galveston |
| gv_dew | Dew point in Galveston|
| gv_humidity | Relative humidity in Galveston|
| gv_precip | Amount of liquid equivalent precipitation (rain, snow etc.) in Galveston  |
| gv_windgust | Instantaneous speed of wind in Galveston |
| gv_windir | Two minute average of wind direction in Galveston |
| gv_sealevelpressure | Sea level pressure in Galveston| 
| gv_cloudcover | Percentage of sky that is covered by cloud in Galveston |
| gv_visibility | Distance that can be viewed in Galveston |
| gv_solarradiation | Solar radiation in Galveston  |
| gv_solarenergy | Solar energy in Galveston  |
| gv_uvindex | UV index in Galveston |
| pl_temp | Temperature in Fahrenheit in Port Lavaca|
| pl_feelslike | Combination of temperature, wind chill & heat index in Port Lavaca |
| pl_dew | Dew point in Port Lavaca |
| pl_humidity | Relative humidity in Port Lavaca|
| pl_precip | Amount of liquid equivalent precipitation (rain, snow etc.) in Port Lavaca  |
| pl_windgust | Instantaneous speed of wind in Port Lavaca |
| pl_windir | Two minute average of wind direction in Port Lavaca |
| pl_sealevelpressure | Sea level pressure in Port Lavaca| 
| pl_cloudcover | Percentage of sky that is covered by cloud in Port Lavaca |
| pl_visibility | Distance that can be viewed in Port Lavaca |
| pl_solarradiation | Solar radiation in Port Lavaca  |
| pl_solarenergy | Solar energy in Port Lavaca  |
| pl_uvindex | UV index in Port Lavaca |
| vc_temp | Temperature in Fahrenheit in Victoria|
| vc_feelslike | Combination of temperature, wind chill & heat index in Victoria|
| vc_dew | Dew point in Victoria|
| vc_humidity | Relative humidity in Victoria|
| vc_precip | Amount of liquid equivalent precipitation (rain, snow etc.) in Victoria  |
| vc_windgust | Instantaneous speed of wind in Victoria |
| vc_windir | Two minute average of wind direction in Victoria|
| vc_sealevelpressure | Sea level pressure in Victoria| 
| vc_cloudcover | Percentage of sky that is covered by cloud in Victoria |
| vc_visibility | Distance that can be viewed in Victoria |
| vc_solarradiation | Solar radiation in Victoria  |
| vc_solarenergy | Solar energy in Victoria  |
| vc_uvindex | UV index in Victoria |
|mean_temp| The average temperature in Fahrenheit for all four geographic locactions|
|mean_feelslike| The average feelslike temperature for all four greographic locations|
|mean_humidity| The average humidity for all four geographic locations|


<hr style="background-color:silver;height:3px;" />

## Reproducing this project
<hr style="background-color:silver;height:3px;" />

> You can reproduce this project with the following steps:
> - Read this README
> - Clone the repository or download all files into your working directory
> - Libraries used:
>     - pandas
>     - matplotlib
>     - seaborn
>     - numpy
>     - scikit-learn
>     - plotly
>     - sktime
>     - Prophet
> - Run the Final_Report notebook or explore the other notebooks for greater insight into the project.

### Project Plan 

<details>
  <summary><i>Click to expand</i></summary>
  <ul>
   <li><b>Acquire</b> data from https://www.ercot.com/gridinfo/load/load_hist and https://www.visualcrossing.com/weather-data</li>
    <li>Clean and <b>prepare</b>data for the exploration. </li>
    <li>Create wrangle.py to store functions we created to automate the cleaning and preparation process.</li>
    <li>Separate train, validate, test subsets and scaled data.</li>
    <li><b>Explore</b> the data through visualizations; Document findings and takeaways.</li>
    <li>Perform <b>modeling</b>:
    <ul>
        <li>Identify model evaluation criteria</li>
        <li>Create at least three different models.</li>
        <li>Evaluate models on appropriate data subsets.</li>
    </ul>
    </li>
    <li>Create <b>Final Report</b> notebook with a curtailed version of the above steps.</li>
    <li>Create and review README. </li>
    
  </ul>
</details
