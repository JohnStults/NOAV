import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

def label_point(x, y, val, ax):
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for i, point in a.iterrows():
        if i == 7:
            ax.text(point['x']-.04, point['y'], str(point['val']),horizontalalignment='right',size= 5)
        elif i == 10:
            ax.text(point['x']+.04, point['y'], str(point['val']),horizontalalignment='left',size= 5)
        elif i == 9:
            ax.text(point['x'], point['y']+.1, str(point['val']),horizontalalignment='center',size= 5)
        elif i == 4:
            ax.text(point['x']+.1, point['y']-.16, str(point['val']),horizontalalignment='right',size= 5)
        elif i == 14:
            ax.text(point['x']-.04, point['y']-.08, str(point['val']),horizontalalignment='right',size= 5)
        elif i == 15:
            ax.text(point['x'], point['y']-.04, str(point['val']),horizontalalignment='left',size= 5)
        elif i == 2:
            ax.text(point['x']-.04, point['y']-.1, str(point['val']),horizontalalignment='right',size= 5)
        elif i == 0:
            ax.text(point['x']-.15, point['y']+.1, str(point['val']),horizontalalignment='center',size= 5)
        elif point['x'] <= 2.5:
            ax.text(point['x']+.04, point['y'], str(point['val']),size= 5)
        else:
            ax.text(point['x']-.04, point['y'], str(point['val']),horizontalalignment='right',size= 5)


df = pd.read_table('NOAV/NOAV.txt',sep='\t',header='infer',encoding='latin1')
df = df[pd.notnull(df['NOAVIssueDate'])]
year = []
print(df.columns)
for i in df['NOAVIssueDate']:
    mth, day, x = i.split('/')
    try:
        yr, tm = x.split(" ")
        year.extend([int(yr)])
    except:
        yr = int(x)
        year.extend([yr])
df['ViolationYear'] = year

# # ******** Portion of the code for penalties assessed
# penalty = df[['ViolationYear','OperatorName','NOAVIssueDate','FinalResolutionComments']]
# penalty = penalty[(penalty['FinalResolutionComments'].str.contains('$')) |
#                   (penalty['FinalResolutionComments'].str.contains('fine',case=False))]
#
# this = penalty['FinalResolutionComments'].str.contains('no fine',case=False)
# penalty = penalty[np.logical_not(this)]
#
# penalty.to_csv('NOAV/fined.csv')
#
# yrs = list(df['ViolationYear'].drop_duplicates())
#
# percent = []
# for i in yrs:
#     tot = len(df[df['ViolationYear'] == i])
#     pen = len(penalty[penalty['ViolationYear'] == i])
#     per = (pen/tot)*100
#     percent.extend([per])
#
# sns.barplot(yrs,percent)
# plt.xlabel('Year')
# plt.ylabel('Percent Fined')
# plt.title('Percent of NOAVs Resulting in Fines')
# plt.savefig('fig1.png')
# plt.show()
# plt.close()
#
# operators = list(penalty['OperatorName'].drop_duplicates())
# violators = []
# for i in operators:
#     tot = len(penalty[penalty['OperatorName'] == i])
#     violators.extend([tot])
# new = pd.DataFrame(data=[violators,operators])
# new = new.T
# new.columns = ['Vi','Op']
# new = new[new['Vi'] >= 10]
# sns.barplot(x='Vi',y='Op',data=new)
# plt.ylabel('Operator')
# plt.yticks(size=6)
# plt.xlabel('Number Violations')
# plt.title('Violations Resulting in Fines by Operator')
# plt.tight_layout()
# plt.savefig('fig2.png')
# plt.show()
# plt.close()
# # **********

# # *********** Penalties not assessed
# yrs = list(df['ViolationYear'].drop_duplicates())
# operators = df.drop_duplicates(subset=['OperatorName','OperatorNumber'])
# operators = operators[['OperatorNumber','OperatorName']]
# data = pd.read_csv('Production_Summaries/Colorado Production 2011-2017.txt',sep='\t',header='infer',encoding=None)
# data = data.drop(labels=data.columns.tolist()[0], axis=1)
# num = operators['OperatorNumber'].drop_duplicates()
# number_NOAV = []
# for i in num:
#         total = len(df[df['OperatorNumber'] == i])
#         number_NOAV.extend([total])
#
# new = pd.DataFrame([list(operators['OperatorName']),list(operators['OperatorNumber']),number_NOAV])
# new = new.T
# new.columns=['Operator Name','Operator Number','NOAV Count']
# for i in list(range(2011,2018,1)):
#     column = str(i)
#     new[column] = [np.nan]*len(new)
#
# data['report_year'] = list(map(int, list(data['report_year'])))
# this = data['operator_num'].drop_duplicates()
# check = this[this.isin(list(operators['OperatorNumber']))]
# print(len(this))
# print(len(check))
# print(len(new))
# for i in list(range(2011,2018,1)):
#     year_ct = []
#     column = str(i)
#     for j in list(new['Operator Number']):
#         dum = data[(data['operator_num'] == j) & (data['report_year'] == i)]
#         co = len(dum[(pd.notnull(dum['oil_prod'])) & (pd.notnull(dum['gas_prod']))])
#         year_ct.extend([co])
#     print(i)
#     new[column] = year_ct

# # *********** New stuff
sns.set_style('darkgrid')
new = pd.read_csv('Production_Summaries/NOAV_activeWell_company.csv')
avgs = []
for i in list(new['Operator Number']):
    series = new[new['Operator Number'] == i]
    series = series[['2011','2012','2013','2014','2015','2016','2017']]
    series = series.T
    series = list(series[series.columns.tolist()[0]])
    a = np.average(series)
    avgs.extend([a])
new['Average Active Wells'] = np.nan*len(new)
new['Average Active Wells'] = avgs
new = new[(new['Average Active Wells'] > 0) & (new['NOAV Count'] > 0)]
new = new[(pd.notnull(new['Average Active Wells'])) & (pd.notnull(new['NOAV Count']))]
# sns.regplot(x='Average Active Wells',y='NOAV Count',data=new,marker='+')
# plt.semilogx()
# plt.xlim(1,10000)
# plt.savefig('NOAV preliminary.png')
# plt.tight_layout()
# plt.show()
# plt.close()

new['NOAV per well'] = new['NOAV Count']/new['Average Active Wells']
new['Average Active Wells'] = np.log10(np.array(new['Average Active Wells']))
new['NOAV per well'] = np.log10(np.array(new['NOAV per well']))
x = np.array(new['Average Active Wells'])
y = np.array(new['NOAV per well'])
sns.regplot(x='Average Active Wells',y='NOAV per well',data=new,marker='+')
plt.ylim(-4,2)
plt.yticks(np.arange(2,-5,-1),['100','10','1','.1','.01','.001','.0001'],rotation=30)
plt.xlim(-1,4)
plt.xticks(np.arange(-1,5,1),['.1','1','10','100','1000','10000'],rotation=30)
s, inter, r, p ,std = stats.linregress(x,y)
r = -r
r = "{0:.3g}".format(r)
std = "{0:.3g}".format(std)
rho, p = stats.spearmanr(x,y)
p = "{0:.3g}".format(p)
rho = "{0:.3g}".format(rho)

plt.text(-0.2,-2.5,'R^2: ' +str(r),horizontalalignment='left',size=10)
plt.text(-0.2,-2.8,'Std. Err.: ' +str(std),horizontalalignment='left',size=10)
plt.text(-0.2,-3.1,'P-Val: ' +str(p),horizontalalignment='left',size=10)
plt.text(-0.2,-3.4,'Spearman Rank: ' +str(rho),horizontalalignment='left',size=10)
plt.tight_layout()
plt.savefig('NOAV as function of well.png')
plt.show()
plt.close()

new = new[(new['NOAV per well'] >= (1.3-new['Average Active Wells']))]
new['index'] = list(range(len(new)))
new = new.set_index('index')
x = np.array(new['Average Active Wells'])
y = np.array(new['NOAV per well'])
ex = [-2,5]
why = [((s*-2)+inter),((s*5)+inter)]
plt.plot(ex,why,'--k',alpha=0.5)
plt.scatter(x,y)
plt.ylim(-4,2)
plt.yticks(np.arange(2,-5,-1),['100','10','1','.1','.01','.001','.0001'],rotation=30)
plt.xlim(-1,4)
plt.xticks(np.arange(-1,5,1),['.1','1','10','100','1000','10000'],rotation=30)
label_point(new['Average Active Wells'],new['NOAV per well'],new['Operator Name'],plt.gca())
plt.savefig('Labeled Companies Issues.png')
plt.show()
plt.close()

count = []
yrs = list(range(2011,2019,1))
for i in yrs:
    total = len(df[df['ViolationYear'] == i])
    count.extend([total])
pdf = pd.DataFrame([yrs,count])
pdf = pdf.T
pdf.columns = ['Year','Number of NOAVs Issued']
sns.barplot(x='Year',y='Number of NOAVs Issued',data=pdf)
plt.title('Number of NOAVs per year')
plt.tight_layout()
plt.savefig('NOAVs per year.png')
plt.show()
plt.close()


# 'OperatorNumber',OperatorName','NOAVIssueDate',
# 'operator_num','name','report_year','oil_prod','gas_prod'