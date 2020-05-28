# config.py

from pathlib import Path  # pathlib is seriously awesome!

raw_dir = Path('~/Docs/insight/git/data/raw')
processed_dir = Path('~/Docs/insight/git/data/processed')
clean_dir = Path ('~/Docs/insight/git/data/raw')
raw_path = data_dir / 'dataforazeroth_complete_dataset.csv'

# Will convert these to feather files on the next run
processed_path = data_dir / 'wow_player_stats.csv'
achievement_categories_path = raw_dir / 'wow_achievement_categories.csv'
achievement_list_path = raw_dir / 'wow_achievement_list.csv'
dfa_path = raw_dir / 'dataforazeroth_complete_dataset.csv'

#customer_db_url = 'sql:///customer/db/url'
#purchases_db_url = 'sql:///purchases/db/url'