# Dongseok Yang.
# Kangwon National University
# Any issues can be reported to dongseok.yang@kangwon.ac.kr
# Have good day!

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import hydroeval as he
import warnings
import os

path = os.getcwd()

plt.style.use('seaborn')
sns.set_style({'font_scale':'0.5', 'font.family': 'serif', 'font.serif': ['Times New Roman']})

# read csv file
df_flow = pd.read_csv('data.csv')

# visualize the first 5 rows
df_flow.head()



#simple data distribution
plt.figure(figsize=(7,7), edgecolor='black')

# scatter plot
ax = sns.scatterplot(x='sim', y='obs', data=df_flow, s=40)

# notations indicating an outlier
ax.annotate('Outlier', xy=(190,105), xytext=(183,102),
            arrowprops=dict(arrowstyle='->', ec='grey', lw=2), bbox = dict(boxstyle="round", fc="0.8"))
ax.annotate('Outlier', xy=(165,85), xytext=(158,82),
            arrowprops=dict(arrowstyle='->', ec='grey', lw=2), bbox = dict(boxstyle="round", fc="0.8"))


# NSE, R2 calculation
r2 = (np.corrcoef(df_flow['obs'], df_flow['sim']))[0, 1]** 2
r2_val = round(r2, 3)
nse = he.evaluator(he.nse, np.array(df_flow['obs']), np.array(df_flow['sim']))
nse_val = round(nse[0], 3)


# labels and title
lims = (0, max(df_flow.max()))
# ax.set(xlim=lims, ylim=lims)

plt.xlabel('Simulation', fontsize=14)
plt.ylabel('Observation', fontsize=14)
plt.title('Relation between obs. and sim.', fontsize=15)
# write r2, nse in the graph
plt.text(1, lims[1]*0.9, r'$R^2: $'+str(r2_val), fontdict={'size': 12})
plt.text(1, lims[1] * 0.85, r'$NSE: $' + str(nse_val), fontdict={'size': 12})

plt.show()






# linear model
linear_regression = LinearRegression()
# fit the linear model - calculate the coefficients 
linear_regression.fit(df_flow[['obs']], df_flow['sim'])
# make predictions using the linear model
obs_predicted = linear_regression.predict(df_flow[['obs']])

# coefficients learned during training
intercept = linear_regression.intercept_
slope = linear_regression.coef_[0]

# compute the residuals (actual value - predicted value)
residuals = df_flow.obs - obs_predicted






import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.outliers_influence import OLSInfluence

# Cook's distance
threshold = 4 / len(df_flow)
print('Cook\'s distance: ', round(threshold, 2))


# fit the regression model using statsmodels library 
f = 'obs ~ sim'
model = ols(formula=f, data=df_flow).fit()

# calculate the cooks_distance - the OLSInfluence object contains multiple influence measurements
cook_distance = OLSInfluence(model).cooks_distance
(distance, p_value) = cook_distance

# Drawing graph
plt.figure(figsize=(7,7), edgecolor='black')

# scatter plot - x axis (independent variable sim), y-axis (dependent variable obs), size and color of the marks according to its cook's distance
sns.scatterplot(df_flow.sim, df_flow.obs, hue=distance, size=distance, sizes=(50, 200), edgecolor='black', linewidth=1)


# labels and title
plt.xlabel('Simulation', fontsize=14)
plt.ylabel('Observation', fontsize=14)
plt.title('Cook\'s distance', fontsize=15)
plt.text(1, lims[1]*0.8, 'D= '+str(round(threshold, 3)), fontdict={'size': 12})
plt.show()






# the observations with Cook's distances higher than the threshold value are labeled in the plot
influencial_data = distance[distance > threshold]
index_list = []
for index, value in influencial_data.items():
    index_list.append(index)


# after erasing outliers, show outlier detected data and linear tendency.

# All data to list
data_list = np.array(df_flow.values.tolist())

# influencial data index list
print(index_list)






# append outliered data to lists
sim_list = []
obs_list = []
for i in range(len(data_list)):
    if i-1 not in index_list:
        sim_list.append(data_list[i][0])
        obs_list.append(data_list[i][1])

print('obs list :: ',len(obs_list))
print('sim list :: ',len(sim_list))

# NSE, R2 calculation
r2 = (np.corrcoef(obs_list, sim_list))[0, 1]** 2
r2_val = round(r2, 3)
nse = he.evaluator(he.nse, np.array(sim_list), np.array(obs_list))
nse_val = round(nse[0], 3)


# outliered dataframe
data = pd.DataFrame(data={'Simulation': sim_list, 'Observation': obs_list}, columns=['Simulation','Observation'])

warnings.filterwarnings('ignore')

# standard line
std_range = np.array([0, data['Simulation'].max()])
std_d = {'Simulation' : std_range, 'Observation' : std_range}
std_d = pd.DataFrame(std_d)








# drawing graph
lims = (0, max(data.max()))
plt.figure(figsize=(7,7), edgecolor='black')
r2graph = sns.regplot(x="Simulation", y="Observation", data=data, color='dimgray', line_kws={'color':'r'}, scatter_kws={'s':40})
sns.lineplot('Simulation', 'Observation', data = std_d, dashes=(2,2), color='lime', linewidth=0.75)


r2graph.set(xlim=lims, ylim=lims)
plt.savefig(path + '/' + 'outliered.png', dpi=300)
# write r2, nse in the graph
plt.text(1, lims[1]*0.9, r'$R^2: $'+str(r2_val), fontdict={'size': 12})
plt.text(1, lims[1] * 0.85, r'$NSE: $' + str(nse_val), fontdict={'size': 12})

# labels and title
plt.xlabel('Simulation', fontsize=14)
plt.ylabel('Observation', fontsize=14)
plt.title('Outliered data scatter', fontsize=15)
plt.show()
