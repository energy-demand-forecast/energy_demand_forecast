# Project Title
*Audience: Target audience for my final report is*


<hr style="background-color:silver;height:3px;" />

## Project Summary
<hr style="background-color:silver;height:3px;" />

### Project Deliverables
> - A final report notebook
> - Python modules for automation and to facilitate project reproduction
> - Notebooks that show:
>  - Data acquisition and preparation 
>  - exploratory analysis not included in final report
>  - model creation, refinement and evaluation

### Initial questions on the data

>  - Weather and Energy Demand:
>   - How does temperature impact energy demand? 
>   - Does humidity impact energy demand?
>   - Is there a relationship between precipitation and energy demand?

>  - Date/Time and Energy Demand:
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


<hr style="background-color:silver;height:3px;" />

## Data Dictionary
<hr style="background-color:silver;height:3px;" />

|Target|Definition|
|:-------|:----------|
| ercot_load| ERCOT's energy load for the coastal region - measured in megawatts(MW)|

|Feature|Definition|
|:-------|:----------|
| Feature       | Definition |
| Feature        | Definition |
| Feature       | Definition |
| Feature        | Definition 


<hr style="background-color:silver;height:3px;" />

## Reproducing this project
<hr style="background-color:silver;height:3px;" />

> In order to reproduce this project you will need your own environment file and access to the database. You can reproduce this project with the following steps:
> - Read this README
> - Clone the repository or download all files into your working directory
> - Add your environment file to your working directory:
>  - filename should be env.py
>  - contains variables: username, password, host
> - Run the Final_Report notebook or explore the other notebooks for greater insight into the project.

### Project Plan 

<details>
  <summary><i>Click to expand</i></summary>
  <ul>
   <li><b>Acquire</b> data from https://www.ercot.com/gridinfo/load/load_hist and https://www.visualcrossing.com/weather-data</li>
    <li>Clean and <b>prepare</b>data for the exploration. </li>
    <li>Create wrangle.py to store functions I created to automate the cleaning and preparation process.</li>
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
