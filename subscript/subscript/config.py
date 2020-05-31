# config.py

from pathlib import Path
import os

home_dir = Path('/Users/haleyspeed/Docs/insight/git/')
raw_dir = os.path.join(home_dir,'data','raw')
processed_dir = os.path.join(home_dir, 'data', 'processed')
clean_dir = os.path.join(home_dir,'data', 'cleaned')



#customer_db_url = 'sql:///customer/db/url'
#purchases_db_url = 'sql:///purchases/db/url'