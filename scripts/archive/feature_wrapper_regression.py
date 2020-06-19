#importing libraries
import pandas as pd
import os
import config as cn
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import RFE
from sklearn.linear_model import RidgeCV, LassoCV, Ridge, Lasso


# Read in data and set p value Elimination
p_limit = 0.0001
df = pd.read_csv(os.path.join(cn.clean_dir,'final_aggregated_categories.csv'), dtype = 'unicode')
player_cols =  ['Unnamed: 0','Unnamed: 0.1','player','realm','gear_score','last_login',
            'time_since_login','status']
df = df.drop(player_cols, axis = 1)
print(df.head())
dfp = pd.DataFrame()

y = df.engagement.astype(float)

#Adding constant column of ones, mandatory for sm.OLS model
X_1 = sm.add_constant(df).astype(float)
#print(c for c in df.columns.values)

# Fitting sm.OLS model
# Make all dates = 2 by using only the first character. sm.OLS requires floats
model = sm.OLS(y.astype(float), X_1.astype(float)).fit()
p_values = model.pvalues
print('pvalues: ', p_values)

#Backward Elimination
i = 0
cols = list(df.columns)
pmax = 1
while (len(cols)>0):
    print(i)
    p= []
    X_1 = df[cols]
    X_1 = sm.add_constant(X_1)
    model = sm.OLS(y.astype(float),X_1.astype(float)).fit()
    p = pd.Series(model.pvalues.values[1:],index = cols)
    dfp = dfp.append(p, ignore_index = True)

    pmax = max(p)
    feature_with_p_max = p.idxmax()
    if(pmax>p_limit):
        cols.remove(feature_with_p_max)
    else:
        break
    selected_features_BE = cols
    i = i + 1
print(selected_features_BE)
dfo = pd.DataFrame(selected_features_BE)
dfp.to_csv('p_values.csv')
dfo.to_csv('selected_features.csv')
