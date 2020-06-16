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
df = pd.read_csv(os.path.join(cn.clean_dir,'final_feature_stats.csv'), dtype = 'unicode')
dfa = pd.read_csv(os.path.join(cn.clean_dir, 'achievement_short_list.csv'))
keep = [str(int(c)) for c in dfa.achievement_id]
if 'id' not in df.columns.values:
    df['id'] = df.player + '_' + df.realm
keep = keep + ['engagement','id']
keep = [c for c in keep if c in df.columns.values]
df = df[keep]
df = df.set_index('id')

df = df.astype(str).apply(lambda x: x.str[:1]).replace('n','0')
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
