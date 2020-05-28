# DATASETS


## Leaderboards 
- Collected on May 20-21, 2020
- Source: dataforazeroth.com and wowprogress.com
- Contents: Top 500 leaderboards for all categories
- Collection Method: Webscrapes using requests package and Beautiful Soup
- Data Storage: 
    - raw / dataforazeroth_complete_dataset.csv
    

## Guild Rosters
- Collected on May 21-22
- Guild name source: Dataforazeroth.com leaderboards
- Guild roster source: Blizzard Entertainment's Web API
- Collection Method: Requests package with custom wrapper for API calls
- Data Storage:
    - raw / wow_achievement_categories.csv
    - raw / wow_achievements.csv


## Player and Guild Statistics
- Collected on May 22-31
- Source: Blizzard Web API
- Collection Method: Requests package and custom wrapper for Blizzard API calls
- Data Storage:
-   Personal mySQL server hosted by siteground.com (domain n-coding.net)
-   Will save local csv/feather file once I pull the data for the training and test sets
