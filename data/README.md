# DATASETS

## Datasets can be downloaded from:
(http://n-coding.net/subscript)

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
- Collected on June 10, 2020 (final scrape)
- Source: Blizzard Web API
- Collection Method: Requests package and custom wrapper for Blizzard API calls
- Data Storage:
  - 6-10_scrapes / wow_roster_...csv


## Individual player stats
- Processed June 12, 2020
- Source: 6-10_scrapes
- achievement_time_processor.py (time series aggregation)
  - processed / 6-10_scrapes / processed_6-10-20 / time / time...csv.
- achievement_feature_processor.py (feature importance processor)
  - processed / 6-10_scrapes / processed_6-10_20/ bfa_features / bfa_features...csv.


## Added engagement and status features
- Processed June 12, 2020
- Source: Output of achievement_time/feature_processor.py
- 'status' is the label classifying the player as active, at-risk of lapse, lapsed, inactive
- 'engagement' is the numeric label for status (0,1,2,3, respectively)
- engagement_adder_time.py
  - processed / 6-10_scrapes / processed_6-10-20 / time / engaged / engaged....csv
- engagement_adder_features.py
  - processed / 6-10_scrapes / processed_6-10-20 / bfa_features / engaged / engaged....csv


## Concatenate batched csv files
- Processed June 12, 2020
- Source: Output of engagment_adder_features/time.py
- file_concatenator.py
  - / cleaned / final_time_stats.csv
  - / cleaned / final_feature_stats.csv

## Feature importances
- Trained on June 13, 2020
- Source: final_feature_stats.csv
- feature_importance.py
  - / cleaned / feature_importance / feature_importance.csv
  - / cleaned / feature_importance / feature_importance.sav (pickle)

## Random forest classifier
- Trained on June 13, 2020
- Source: final_time_stats.csv
- random_forest_classifier.py
  - / cleaned / random_forest_classifier / predictions.csv
  - / cleaned /random_forest_classifier / random_forest_model.sav (pickle)
