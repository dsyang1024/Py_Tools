import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

sns.set_style('whitegrid', {'font.family': 'serif', 'font.serif': ['Times New Roman']})

path = os.getcwd()

data = pd.read_csv('example (30).csv')
print(data.dtypes)

index = data.columns.tolist()  # 필드명 리스트


# y 값을 보고자 하는 항목으로 확인하면 됩니다.
# x 값은 보고자 하는 분류 방법으로 생각하시고 연도 혹은 월/계절 기준으로 확인 가능합니다.
for i in index[5:]:
    plt.figure(figsize=(8, 4))
    
    # 연단위 그래프 생성
    sns.boxplot(x="Year", y=i, data=data, color='grey', showfliers=False)
    plt.tight_layout()
    plt.savefig(path + '/' + i[:-6] + '_entire_boxplot_graph.png', dpi=300)
    
    # 월단위 그래프 생성
    sns.boxplot(x="Month", y=i, data=data, color='grey', showfliers=False)
    plt.tight_layout()
    plt.savefig(path + '/' + i[:-6] + '_monthly_boxplot_graph.png', dpi=300)
    plt.show()
