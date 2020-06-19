from setuptools import setup, find_packages

# python setup.py build
# python setup.py install
setup(
   name='subscript',
   version='1.0',
   description='Winning subscriber loyalty with curated content',
   author='Haley Speed',
   author_email='haley.e.speed@gmail.com',
   packages=['subscript'],  #same as name
   install_requires=['numpy', 'matplotlib', 'streamlit','seaborn','scikit-learn','bs4'], #external packages as dependencies
   scripts=[
            '../scripts/subscript.py',
            '../scripts/achievement_api_caller.py',
            '../scripts/achievement_categorizer.py',
            '../scripts/achievement_getter.py',
            '../scripts/achievement_list_maker.py',
            '../scripts/achievement_time_processor.py',
            '../scripts/engagement_adder_features.py',
            '../scripts/engagement_adder_time.py',
            '../scripts/feature_aggregator.py',
            '../scripts/feature_wrapper_classifier.py',
            '../scripts/file_concatenator_features.py',
            '../scripts/file_concatenator_time.py',
            '../scripts/gradient_boost.py',
            '../scripts/important_features_list.py',
            '../scripts/player_lapse_predictor.py',
            '../scripts/random_forest_time.py',
            '../subscript/subscript/config.py',
            '../subscript/subscript/custom_funcs.py',
            '../notebooks/dbscan.ipynb',
           ]
)
