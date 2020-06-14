#importing libraries
import pandas as pd
import os
import config as cn
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import RFE
from sklearn.linear_model import RidgeCV, LassoCV, Ridge, Lasso


# Read in data and set p value Elimination
p_limit = 0.05
df = pd.read_csv(os.path.join(cn.processed_dir,'6-10_scrapes',
                'processed_6-10-20', 'concatenated', 'engaged',
                'final_concatenation', 'final_feature_stats.csv'), dtype = 'unicode')
dfa = pd.read_csv(os.path.join(cn.clean_dir, 'achievement_details_list.csv'))
df_bfa = dfa.achievement_id[dfa.category_name == 'Battle for Azeroth'].astype(int).astype(str)
keep = [c for c in df_bfa]
keep = keep + ['engagement','id']
df = df[keep]
del_cols = [c for c in df.columns.values if 'unnamed' in str(c).lower()]

df = df.set_index('id')
df = df.drop(del_cols, axis = 1)

df = df.astype(str).apply(lambda x: x.str[:1]).replace('n','0')
df = df.dropna(axis = 1)
print(df)

dfp = pd.DataFrame()

y = df.engagement.astype(float)

#Adding constant column of ones, mandatory for sm.OLS model
X_1 = sm.add_constant(df).astype(float)

# Fitting sm.OLS model
# Make all dates = 2 by using only the first character. sm.OLS requires floats

model = sm.OLS(y.astype(float), X_1.astype(float)).fit()
p_values = model.pvalues
print(p_values)

#Backward Elimination
cols = list(df.columns)
pmax = 1
while (len(cols)>0):
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
    print(selected_features_BE)
    dfo = pd.DataFrame(selected_features_BE)
    dfp.to_csv('p_values.csv')
    dfo.to_csv('selected_features.csv')
