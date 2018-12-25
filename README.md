# OpenCity-Sprint-2018
- [What is a Sprint?](https://github.com/DataKind-BLR/Sprint/wiki)
- [About OpenCity](https://github.com/DataKind-BLR/OpenCity-Sprint-2018#about-opencity)
- [Problem Statement](https://github.com/DataKind-BLR/OpenCity-Sprint-2018/wiki)
- [Volunteering Opportunities](https://github.com/DataKind-BLR/OpenCity-Sprint-2018#volunteering-opportunities)
- [What would you like to solve for OpenCity?](https://github.com/DataKind-BLR/OpenCity-Sprint-2018/issues)

## About OpenCity

[OpenCity](http://opencity.in//) is an Urban Data Portal - A collaboration between Oorvani Foundation and DataMeet. 


## Problem Statment
  To compute livability index of cities at neighbourhood level. Refer to wiki for more details

### Data Points scoped for current sprint
- how green is the neighborhood? (trees and lakes availability) 
- Access to parks & playgrounds
- Polling stations
- Distance to nearest police stations
- Civic Engagements (Voter %)
- Metro stations
- BMTC bus stations
 
## Volunteering Opportunities
  ### Data Engineering
  - To Scrape/collect the data from sources like
    - OpenStreetMap
    - Indian Data Portal (data.gov.in)
    - BMTC
    - OpenBudgetsIndia
    - OpenAQ
  - Collate multiple data sources
  - Data Cleaning
  - Map data points to wards of Bengaluru
  - Model and setup Data Pipeline that could scrap, collate, clean and map all the data sources on a timely manner
  ### Design
  - Data Design
    - See how effectively various indicators can be packed for end users
  - Visual Design and Data Visualization
    - To model and implement an interface for various stakeholders (Citizen, Government officials, Journalists etc..) to select, prioritize and visualize indicators.
     
  ### Data Science
  - Data Analysis
    - Assess various datasets scraped and standradize the indicators.
    
  - Model data points to measurable indicators
  
    - Reachability
      - Create a model a way to compute rechability of various wards based on various transport data points
    - Civic participatiion
      - Create a model to calculate citizen participation basedon various data points (Complaints raised in platforms like Sahay, ICMCetc.. voter turnout in electins etc..) 
    - Environment
      - Create a model to compute green cover of areas bases on trees, parks, air pollution, water pollution etc...  
    - Safety
      - Create a model to calulate the safety of an area based on data points like street light cover, police stations etc... 
  
  - Model Livability index
    - Given all the datapoints model a way to compute livability index at ward level of a particular city (Bengaluru)

## Current Project State
  - Indicators
    - Various indicators brainstromed for the project are listed [here](https://docs.google.com/spreadsheets/d/1yrmouKdaCkhYW6U-Kh0UhcDiSBooThtr9fjFY6VgWTU/edit#gid=0)
  - Data Sources pending to collect/scrape
    - Green cover, parks
    - polling stations
  - Remaining tasks and signed up people
    - Livability Model - Raghuram, Atish, Mullai
    - Superset setup - DC, Ramya
    - Scrape polling station locations - DC, Mahesh Maney
    - Reachablity model - Shobana, Ananaditha, Ajay
    - EDA - Veena, Shilpa
  - Drive: All datasets and other resources listed [here](https://drive.google.com/drive/u/1/folders/1E6gX6oPp7koAskiLDRVXuDS3dAd6v9rq) 

## Current technologies being used
- Python
- NodeJs
- R
- Reactjs
- D3js
- Dash and plotly
