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
            '../subscript/subscript/config.py',
            '../subscript/subscript/custom_funcs.py',
           ]
)
