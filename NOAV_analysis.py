import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

df = pd.read_table('NOAV/NOAV.txt',sep='\t',header='infer',encoding='latin1')
df = df[pd.notnull(df['NOAVIssueDate'])]
year = []
for i in df['NOAVIssueDate']:
    mth, day, x = i.split('/')
    try:
        yr, tm = x.split(" ")
        year.extend([int(yr)])
    except:
        yr = int(x)
        year.extend([yr])
df['ViolationYear'] = year

penalty = df[['ViolationYear','OperatorName','NOAVIssueDate','FinalResolutionComments']]
penalty = penalty[(penalty['FinalResolutionComments'].str.contains('$')) |
                  (penalty['FinalResolutionComments'].str.contains('fine',case=False))]

this = penalty['FinalResolutionComments'].str.contains('no fine',case=False)
penalty = penalty[np.logical_not(this)]

penalty.to_csv('NOAV/fined.csv')

yrs = list(df['ViolationYear'].drop_duplicates())

percent = []
for i in yrs:
    tot = len(df[df['ViolationYear'] == i])
    pen = len(penalty[penalty['ViolationYear'] == i])
    per = (pen/tot)*100
    percent.extend([per])

sns.barplot(yrs,percent)
plt.xlabel('Year')
plt.ylabel('Percent Fined')
plt.title('Percent of NOAVs Resulting in Fines')
plt.savefig('fig1.png')
plt.show()
plt.close()

operators = list(penalty['OperatorName'].drop_duplicates())
violators = []
for i in operators:
    tot = len(penalty[penalty['OperatorName'] == i])
    violators.extend([tot])
new = pd.DataFrame(data=[violators,operators])
new = new.T
new.columns = ['Vi','Op']
new = new[new['Vi'] >= 10]
sns.barplot(x='Vi',y='Op',data=new)
plt.ylabel('Operator')
plt.yticks(size=6)
plt.xlabel('Number Violations')
plt.title('Violations Resulting in Fines by Operator')
plt.tight_layout()
plt.savefig('fig2.png')
plt.show()
plt.close()