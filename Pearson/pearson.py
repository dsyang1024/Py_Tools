# Pearson 상관성 분석 Tool

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import warnings
import numpy as np
sns.set(font_scale=1.5)
sns.set_style('whitegrid', {'font.family': 'serif', 'font.serif': ['Times New Roman']})
path = os.getcwd()


print(pd.__version__)
warnings.filterwarnings('ignore')

data = pd.read_csv('data.csv')


corr = data.corr(method = 'pearson')
df_lt = corr.where(np.tril(np.ones(corr.shape)).astype(np.bool))
print(corr)

plt.figure(figsize=(9,9))
df_heatmap = sns.heatmap(df_lt, cbar=True, annot=True, annot_kws={'size': 15}, fmt='.2f', square=True, cmap='RdYlBu_r')
df_heatmap.set_xticklabels(df_lt, rotation=45)
df_heatmap.set_yticklabels(df_lt, rotation=45)
plt.tight_layout()
plt.savefig(path+'/'+'Pearson_heatmap.png',dpi=300)
# plt.show()


# plt.figure(figsize=(6,6))
df_clustermap = sns.clustermap(corr, 
               annot=True,  # 실제 값 화면에 나타내기
               figsize=(9,9),
               annot_kws={'size' : 12},
               cmap = 'RdYlBu_r',  # Red, Yellow, Blue 색상으로 표시
               vmin = -1, vmax = 1, #컬러차트 -1 ~ 1 범위로 표시
              )
plt.tight_layout()
plt.savefig(path+'/'+'clustermap.png',dpi=300)


# pairplot은 변수가 10개 미만일 때만 사용하세요.
# plt.figure(figsize=(6,6))
sns.pairplot(data, height=3.0, corner=True)
plt.tight_layout()
plt.savefig(path + '/' + 'pairplot.png', dpi=300)
plt.show()