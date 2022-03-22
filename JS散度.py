
import matplotlib.pyplot as plt
import numpy as np

import scipy.stats as st

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.rcParams['font.size']=9
#基础数据库  不变
sell_veg = [
    (0.08625,0,0.625,0),
    (0.08625/3,0.0003,0.625,0.00005644),
]

name_store_veg=["包装常温","无包装常温","包装冷链","无包装冷链"]

name=[
    ["售\n卖\n常\n温","售\n卖\n冷\n链"],
    ["市\n内\n常\n温","市\n内\n冷\n链","市\n内\n常\n温\n新\n能\n源","市\n内\n冷\n链\n新\n能\n源"],
    ["存\n储\n常\n温","存\n储\n冷\n链"],
    ["省\n际\n常\n温","省\n际\n冷\n链","省\n际\n常\n温\n新\n能\n源","省\n际\n冷\n链\n新\n能\n源"],
    ["无\n包\n装",'包\n装'],
    ["火\n电","水\n电","核\n电","太\n阳\n能"],
    ["填\n埋","厌\n氧\n消\n化","堆\n肥","焚\n烧"]
]



veg_pack=[0.8,0]

#第1维，温度（常，冷）
#第2维，新能源(火、水、核、风、太阳能)
sell_veg_percent=[0.58,0.42]
trans2_veg_percent=[0.865*0.99, 0.135*0.99, 0.865*0.01, 0.135*0.01]
store1_veg_percent=[0.83,0.17]
trans1_veg_percent=[0.865*0.99, 0.135*0.99, 0.865*0.01, 0.135*0.01]
energy_percent=[0.818,0.155,0.019,0.008,0]
disposal_percent=[0.25,0.125,0.125,0.5]

#随机绘图用，累积频率
percent_cum_veg=[
    [0.58,1],
    [0.865*0.99, 0.865*0.99+0.135*0.99, 0.99+0.865*0.01,1],
    [0.83,1],
    [0.865*0.99, 0.865*0.99+0.135*0.99, 0.99+0.865*0.01,1],
    [1-0.68,1],
    [0.818,0.155+0.818,0.155+0.818+0.019,1],
    [0.25,0.375,0.5,1]
]

veg_trans1_dis = 935.87
veg_trans2_dis = 30


#纵向，不同温度（常温，冷链,新能源常温，新能源冷链）
#（损耗率，单位里程碳排，里程）
trans2_veg=[
    (0.17*veg_trans2_dis/veg_trans1_dis, 0.0000519, veg_trans2_dis),
    (0.09*veg_trans2_dis/veg_trans1_dis, 0.000186, veg_trans2_dis),
    (0.17*veg_trans2_dis/veg_trans1_dis, 0.0000519*0.576, veg_trans2_dis),
    (0.09*veg_trans2_dis/veg_trans1_dis, 0.000186*0.576, veg_trans2_dis),
]

#(损耗率（%），单位时间能耗（kWh/k(g*d)），时长（d）,包装碳排放+制冷剂碳排放（kgCO2e/kg）)
#包装的碳排加在这一级
store1_veg=[
    (0.15,0,2.5,0),
    (0.05,0.0003,2.5,0.00005644),
]

#纵向，不同温度（常温、冷藏）
#(损耗率（%），单位时间能耗（kWh/k(g*d)），时长（d）,包装碳排放+制冷剂碳排放（kgCO2e/kg）)
trans1_veg=[
    (0.17,0.0000519,935.87,0.3),
    (0.09,0.000186,935.87,0.307144),
    (0.17,0.0000519*0.576,935.87,0.3),
    (0.09,0.000186*0.576,935.87,0.307144),
]

energy=[1.28,0.00339,0.00779,0.00112]
energyname=["火电","水电","核电","太阳能"]

disposal=[0.625*0.02582/0.466,-0.02754,0.165,0.02582]
disposal_name=["填埋","厌氧消化","堆肥","焚烧"]

#包装率及1kg食物对应的碳排
package_percent_veg=0.68
package_emission_veg=0.116

sell_fruit = [
    (0.2*0.9,0,0.625,0),
    (0.2*0.9/3,0.0003,0.625,0.00005644),
]

package_emission_fruit=0.084
package_percent_fruit=0.608


sell_fruit_percent=[0.83,0.17]
trans2_fruit_percent=[0.865*0.99, 0.135*0.99, 0.865*0.01, 0.135*0.01]
store1_fruit_percent=[0.83,0.17]
trans1_fruit_percent=[0.865*0.99, 0.135*0.99, 0.865*0.01, 0.135*0.01]
energy_percent=[0.818,0.155,0.019,0.008,0]
fruit_trans1_dis = 1443.0488
fruit_trans2_dis = 30

percent_cum_fruit=[
    [0.83,1],
    [0.865*0.99, 0.865*0.99+0.135*0.99, 0.99+0.865*0.01,1],
    [0.83,1],
    [0.865*0.99, 0.99, 0.99+0.865*0.01,1],
    [1-0.608,1],
    [0.818,0.155+0.818,0.155+0.818+0.019,1],
    [0.25,0.375,0.5,1]
]


#纵向，不同温度（常温，冷链,新能源常温，新能源冷链）
#（损耗率，单位里程碳排，里程）
trans2_fruit=[
    (0.20*fruit_trans2_dis/fruit_trans1_dis, 0.0000519, fruit_trans2_dis),
    (0.10*fruit_trans2_dis/fruit_trans1_dis, 0.000186, fruit_trans2_dis),
    (0.20*fruit_trans2_dis/fruit_trans1_dis, 0.0000519*0.576, fruit_trans2_dis),
    (0.10*fruit_trans2_dis/fruit_trans1_dis, 0.000186*0.576, fruit_trans2_dis),
]

store1_fruit=[
    (0.075,0,2.5,0),
    (0.025,0.0003,2.5,0.00005644),
]

#纵向，不同温度（常温、冷藏）
#(损耗率（%），单位时间能耗（kWh/k(g*d)），时长（d）,生产（kgCO2e/kg）)因为不再产生额外损耗率所以干脆把生产放这里了
trans1_fruit=[
    (0.20,0.0000519,fruit_trans1_dis,0.32),
    (0.10,0.000186,fruit_trans1_dis,0.327144),
    (0.20,0.0000519*0.576,fruit_trans1_dis,0.32),
    (0.10,0.000186*0.576,fruit_trans1_dis,0.327144),
]

def get_emission(a0,a1,a2,a3,b0,b1,b2,c0,c1,c2,c3,d0,d1,d2,d3,package,en,dis,pack):
    #参数表依次为商店、市内运输、库存、省际运输、d3为生产，package为是否包装（0,1），en为单位电能的碳排放，dis为单位废弃物处理碳排放，pack为单位食物包装所对应过的碳排放
    #包装使得食物浪费降低损耗→0.525
    lr1 = a0*(1-package*0.475)
    lr2 = b0*(1-package*0.475)
    lr3 = c0*(1-package*0.475)
    lr4 = d0*(1-package*0.475)
    m = 1/(1 - lr1)
    e = m * a1*a2*en + a3
    if package == 1:
        e += pack
    m = m/(1 - lr2)
    e += m*b1*b2
    m = m / (1 - lr3)
    e += m * (c1*c2*en + c3)
    m = m / (1 - lr4)
    e += m * (d1*d2 + d3)
    e += (m-1) * dis
    return e

sell_meat = [
    (0.013325,0,0.625,0),
    (0.013325/3,0.0006,0.625,0.00005644),
]

#输出表格时使用的注解
name_meat=[
    ["售\n卖\n常\n温","售\n卖\n冷\n链"],
    ["市\n内\n常\n温","市\n内\n冷\n链","市\n内\n常\n温\n新\n能\n源","市\n内\n冷\n链\n新\n能\n源"],
    ["存\n储\n常\n温","存\n储\n冷\n链"],
    ["省\n际\n活\n畜","省\n际\n活\n畜\n新\n能\n源"],
    ["无\n包\n装",'包\n装'],
    ["火\n电","水\n电","核\n电","太\n阳\n能"],
    ["填\n埋","厌\n氧\n消\n化","堆\n肥","焚\n烧"]
]

#各环节不同属性的比例
#常温/冷链
sell_meat_percent=[0.15,0.85]
#常温/冷链/常温新能源/冷链新能源
trans2_meat_percent=[0.58*0.99, 0.42*0.99, 0.58*0.01, 0.42*0.01]
#常温/冷链
store1_meat_percent=[0.15,0.85]
#牛肉、羊肉、猪肉、禽肉对于的常温及新能源（活畜运输）
trans1_meat_percent=[0.99*3.9/27.3,0.01*3.9/27.3,0.99*3.1/27.3,0.01*3.1/27.3,0.99*15.3/27.3,0.01*15.3/27.3,0.99*5/27.3,0.01*5/27.3]
#长途运输距离（新发地调研比例估算）
meat_trans1_dis = 726.497 
#市内平均距离（Arcgis计算）
meat_trans2_dis = 30
package_emission_meat=0.169
package_percent_meat=0.65

percent_cum_meat=[
    [0.15,1],
    [0,58*0.99,0.99,0.9958,1],
    [0.15,1],
    [0.99,1],
    [0.35,1],
    [0.818,0.155+0.818,0.155+0.818+0.019,1],
    [0.25,0.375,0.5,1],
]

#纵向，不同温度（常温，冷链,新能源常温，新能源冷链）
#（损耗率，单位里程碳排，里程）
trans2_meat=[
    (0.015, 0.0001663, meat_trans2_dis),
    (0.005, 0.0002461, meat_trans2_dis),
    (0.015, 0.0001663*0.576, meat_trans2_dis),
    (0.005, 0.0002461*0.576, meat_trans2_dis),
]

#（常温，冷链）
store1_meat=[
    (0.0533,0,2.5,0),
    (0.0533/3,0.0003,2.5,0.00005644),
]

#纵向，不同温度（常温、冷藏）
#(损耗率（%），单位时间能耗（kWh/k(g*d)），时长（d）,生产（kgCO2e/kg）)
trans1_meat=[
    (0.01,0.0000519,meat_trans1_dis,29.78),
    (0.01,0.0000519*0.576,meat_trans1_dis,29.78),
    (0.01,0.0000519,meat_trans1_dis,24.37),
    (0.01,0.0000519*0.576,meat_trans1_dis,24.37),
    (0.01,0.0000519,meat_trans1_dis,4.66),
    (0.01,0.0000519*0.576,meat_trans1_dis,4.66),
    (0.01,0.0000519,meat_trans1_dis,11.3),
    (0.01,0.0000519*0.576,meat_trans1_dis,11.3)
]



def get_emission_meat(a0,a1,a2,a3,b0,b1,b2,c0,c1,c2,c3,proce,proce_loss,d0,d1,d2,d3,package,en,dis,pack):
    #参数表依次为商店、市内运输、库存、省际运输对应的参数、d3为生产，package为是否包装（0,1），en为单位电能的碳排放，dis为单位废弃物处理碳排放，pack为单位食物包装所对应过的碳排放
    #0.525为经过文献及实地调研对包装效果的预估值，结合JCP2021内线性模型以及保质期在包装前后变化的文献得出
    lr1 = a0*(1-package*0.475)
    lr2 = b0*(1-package*0.475)
    lr3 = c0*(1-package*0.475)
    lr4 = d0*(1-package*0.475)
    m = 1/(1 - lr1)
    e = m * a1*a2*en + a3
    if package == 1:
        e += pack
    m = m/(1 - lr2)
    e += m*b1*b2
    m = m / (1 - lr3)
    e += m * (c1*c2*en + c3)
    m = m / (1-proce_loss)
    e += m * proce * en
    m = m / (1 - lr4)
    e += m * (d1*d2 + d3)
    e += (m-1) * dis
    return e

def js(a,b):
    m=(a+b)/2
    return (st.entropy(a,m))/2+(st.entropy(b,m))/2

import random

import copy

initial=[]

new = [
    ([],[]),
    ([],[],[],[]),
    ([],[]),
    ([],[],[],[]),
    ([],[]),
    ([],[],[],[]),
    ([],[],[],[]),
]

result=[]

for i in range(0,len(name)):
    result.append([])

for i in range(0,30000):
    final_choice = []
    for j in range(0,7):
        decide=random.randint(0,10000)/10000
        for k in range(0,len(percent_cum_fruit[j])):
            if decide <= percent_cum_fruit[j][k]:
                final_choice.append(k)
                break
    a = sell_fruit[final_choice[0]]
    b = trans2_fruit[final_choice[1]]
    c = store1_fruit[final_choice[2]]
    d = trans1_fruit[final_choice[3]]
    initial.append(get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],final_choice[4],energy[final_choice[5]],disposal[final_choice[6]],package_emission_fruit))

initial.sort()
init=np.asarray(initial)

for i in range(0,30000):
    final_choice = []
    for j in range(0,7):
        decide=random.randint(0,10000)/10000
        for k in range(0,len(percent_cum_fruit[j])):
            if decide <= percent_cum_fruit[j][k]:
                final_choice.append(k)
                break
    for test in range(0,len(name)):
        for t in range(0,len(name[test])):
            choice_t = copy.deepcopy(final_choice)
            choice_t[test] = t
            a = sell_fruit[choice_t[0]]
            b = trans2_fruit[choice_t[1]]
            c = store1_fruit[choice_t[2]]
            d = trans1_fruit[choice_t[3]]
            new[test][t].append(get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],choice_t[4],energy[choice_t[5]],disposal[choice_t[6]],package_emission_fruit))

for i in range(0,len(new)):
    for j in range(0,len(new[i])):
        new[i][j].sort()
        result[i].append(np.asarray(new[i][j]))

from numpy import log10

final=[]
for i in range(0,len(result)):
    js_result = []
    chis_result = []
    test=0
    #while test+1 < len(result[i]):
    #    for j in range(test+1,len(result[i])):
    #        js_result.append(10+np.log10(js(result[i][test],result[i][j])))
    #    test += 1
    for j in range(0,len(name[i])):
        final.append((log10(js(result[i][j],init)),name[i][j]))

final.sort(key=lambda x:x[0],reverse=True)
for items in final:
    print(items)
draw_x=[[],[],[]]
draw_y=[[],[],[]]

for i in range(0,len(final)):
    if final[i][0] >= -4:
        k=0
    elif final[i][0] >= -5:
        k=1
    else:
        k=2
    draw_y[k].append(final[i][0])
    draw_x[k].append(final[i][1])

import matplotlib.pyplot as plt

fig,ax=plt.subplots()

colors=["red","orange","blue"]
labels=["-4<log10(初始及条件分布的JS散度)","-5<log10(初始及条件分布的JS散度)<=-4","log10(初始及条件分布的JS散度)<=-5"]
for i in range(0,3):
    if len(draw_x[i]) == 0:
        continue
    else:
        ax.bar(draw_x[i],draw_y[i],color=colors[i],label=labels[i])
ax.legend()
ax.set_title("禽肉 条件分布与初始分布的JS散度")
ax.set_ylabel("log10(初始及条件分布的JS散度)")
ax.set_xlabel("确定条件分布的决策")
ax.set_ylim(-7,-2)
plt.subplots_adjust(bottom=0.28)

#plt.savefig("JS_chicken.png")
plt.show()
