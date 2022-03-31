#画新的箱式图
#数据基础从通用框架里引入
from 通用碳排放框架 import choice_veg, choice_meat, sell, store1, trans2, trans1, food, produce, energy, disposal, energyname, disposal_name, package_emission
from 通用碳排放框架 import percent, per_cum, mass

from matplotlib import pyplot as plt

#累积碳排放，随机生成用
percent_cum = per_cum(percent)

data_init =[
    [],[],[],[],[],[]
]

#生产，直接加上所有的碳排放（因为现在折半是区分了不同的生产）
def production_emission(f,mass,n):
    e = produce[f][0] * mass
    for i in range(1,len(produce[f])):
        e += produce[f][i] * mass
    return e
    



def get_emissions(f,i,j,k,l,p,n,m):
    #a\b\c\d\e分别为销售市内库存省际生产对应的元组,p:是否包装,energy:能耗，dis：废弃物处理方式
    #0.525为经过文献及实地调研对包装效果的预估值，结合JCP2021内线性模型以及保质期在包装前后变化的文献得出
    a = sell[f][i]
    b = trans2[f][j]
    c = store1[f][k]
    d = trans1[f][l]
    percent_line = percent[f][0][i]*percent[f][1][j]*percent[f][2][k]*percent[f][3][l]*percent[f][4][p]*percent[f][5][n]*percent[f][6][m]
    if p >= 1:
        packaged = 1
    else:
        packaged = 0
    lr1 = a[0]*(1-packaged*0.475)
    lr2 = b[0]*(1-packaged*0.475)
    lr3 = c[0]*(1-packaged*0.475)
    lr4 = d[0]*(1-packaged*0.475)
    m1 = 1/(1 - lr1)
    e_total = 0
    e_total += m1*a[1]*a[2]*energy[n]
    e_total += (m1-1)*disposal[m]
    e_total += production_emission(f,m1-1,n)
    e_total += package_emission[f][p]
    m2 = m1/(1 - lr2)
    e_total += b[1]*b[2]*m2
    e_total += (m2-m1)*disposal[m]
    e_total += production_emission(f,m2-m1,n)
    m3 = m2 / (1 - lr3)
    e_total += m3*c[1]*c[2]*energy[n]
    e_total += (m3-m2)*disposal[m]
    e_total += production_emission(f,m3-m2,n)
    if f >= 2:
        m3 = m3/0.9
        e_total += m3 * 1.6 * energy[n]
        e_total += m3 * 0.1 * disposal[m]
        e_total += production_emission(f,m3*0.1,n)
    m4 = m3 / (1 - lr4)
    e_total += d[1]*d[2]*m4
    e_total += (m4-m3) * disposal[m]
    e_total += production_emission(f,m4-m3,n)
    e_total += production_emission(f, 1, n)
    #返回1kg的完整碳排放
    return e_total

import random

BoxplotData = [[],[],[],[],[],[]]
for f in range(0,6):
    for i in range(0,10000):
        final_choice = []
        for j in range(0,7):
            decide=random.random()
            for k in range(0,len(percent_cum[f][j])):
                if decide <= percent_cum[f][j][k]:
                    final_choice.append(k)
                    break
        e_test = get_emissions(f,final_choice[0],final_choice[1],final_choice[2],final_choice[3],final_choice[4],final_choice[5],final_choice[6])
        BoxplotData[f].append(e_test)

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.rcParams['font.size']=9
fig, (ax_Veg,ax_Meat) = plt.subplots(1,2)
DataVeg = BoxplotData[0:2]
DataMeat = BoxplotData[2:] 
print(len(DataVeg))
ax_Veg.boxplot(DataVeg, widths=0.25, patch_artist=True,
                showmeans=False, showfliers=False,
                whis=(0,100),
                medianprops={"color": "black", "linewidth": 0.3},
                boxprops={"facecolor": "C0", "edgecolor": "black","linewidth": 1},
                whiskerprops={"color": "black", "linewidth": 1.5},
                capprops={"color": "black", "linewidth": 1.5},labels=["蔬菜","水果"])
ax_Veg.set_ylabel("单位食物碳排放/(kgCO2e/kg)")
ax_Meat.set_ylabel("单位食物碳排放/(kgCO2e/kg)")
ax_Meat.boxplot(DataMeat, widths=0.5, patch_artist=True,
                showmeans=False, showfliers=False,
                whis=(0,100),
                medianprops={"color": "black", "linewidth": 0.5},
                boxprops={"facecolor": "C1", "edgecolor": "black","linewidth": 1},
                whiskerprops={"color": "black", "linewidth": 1.5},
                capprops={"color": "black", "linewidth": 1.5},labels=["牛肉","羊肉","猪肉","禽肉"])
plt.suptitle("单位质量不同食品碳排放情况概述")
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.3, hspace=0.2)
plt.savefig("单位碳排放概述_updated.png",fontsize=12)
plt.show()