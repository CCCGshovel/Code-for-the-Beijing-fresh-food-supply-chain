import matplotlib.pyplot as plt
import numpy

import scipy.stats

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.rcParams['font.size']=9
#基础数据库  不变
sell_veg = [
    (0.08625,0,0.625,0),
    (0.08625/3,0.0003,0.625,0.00005644),
]

food_name=["蔬菜","水果","牛肉","羊肉","猪肉","禽肉"]

name_store_veg=["包装常温","无包装常温","包装冷链","无包装冷链"]

name=[
    ["常温","冷链"],
    ["常温","冷链","常温新能源","冷链新能源"],
    ["常温","冷链"],
    ["常温","冷链","常温新能源","冷链新能源"],
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
    ["常温","冷链"],
    ["常温","冷链","常温新能源","冷链新能源"],
    ["常温","冷链"],
    ["牛肉","牛肉新能源","羊肉","牛肉新能源","猪肉","猪肉新能源","禽肉","禽肉新能源"],
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
    [0.58*0.99,0.99,0.9958,1],
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


#绘图1：整体箱型图
import random


veg_Data=[]
fruit_Data=[]
meat_Data=([],[],[],[])
for i in range(0,10000):
    final_choice = []
    for j in range(0,7):
        decide=random.randint(0,10000)/10000
        for k in range(0,len(percent_cum_veg[j])):
            if decide <= percent_cum_veg[j][k]:
                final_choice.append(k)
                break
    a = sell_veg[final_choice[0]]
    b = trans2_veg[final_choice[1]]
    c = store1_veg[final_choice[2]]
    d = trans1_veg[final_choice[3]]
    veg_Data.append(get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],final_choice[4],energy[final_choice[5]],disposal[final_choice[6]],package_emission_veg))
    final_choice.clear()
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
    fruit_Data.append(get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],final_choice[4],energy[final_choice[5]],disposal[final_choice[6]],package_emission_fruit))
for m in range(0,4):
    for i in range(0,10000):
        final_choice=[]
        for j in range(0,7):
            decide=random.randint(0,10000)/10000
            for k in range(0,len(percent_cum_meat[j])):
                if decide <= percent_cum_meat[j][k]:
                    final_choice.append(k)
                    break
        final_choice[3]+=2*m
        a = sell_meat[final_choice[0]]
        b = trans2_meat[final_choice[1]]
        c = store1_meat[final_choice[2]]
        d = trans1_meat[final_choice[3]]
        meat_Data[m].append(get_emission_meat(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],final_choice[4],energy[final_choice[5]],disposal[final_choice[6]],package_emission_meat))


fig, (ax_Veg,ax_Meat) = plt.subplots(1,2)
ax_Veg.boxplot([veg_Data,fruit_Data], widths=0.25, patch_artist=True,
                showmeans=False, showfliers=False,
                whis=(0,100),
                medianprops={"color": "black", "linewidth": 0.3},
                boxprops={"facecolor": "C0", "edgecolor": "black","linewidth": 1},
                whiskerprops={"color": "black", "linewidth": 1.5},
                capprops={"color": "black", "linewidth": 1.5},labels=["蔬菜","水果"])
ax_Veg.set(ylim=(0,1))
ax_Veg.set_ylabel("单位食物碳排放/(kgCO2e/kg)")
ax_Meat.set_ylabel("单位食物碳排放/(kgCO2e/kg)")
ax_Meat.set(ylim=(0,40))
ax_Meat.boxplot(meat_Data, widths=0.5, patch_artist=True,
                showmeans=False, showfliers=False,
                whis=(0,100),
                medianprops={"color": "black", "linewidth": 0.5},
                boxprops={"facecolor": "C1", "edgecolor": "black","linewidth": 1},
                whiskerprops={"color": "black", "linewidth": 1.5},
                capprops={"color": "black", "linewidth": 1.5},labels=["牛肉","羊肉","猪肉","禽肉"])
plt.suptitle("单位质量不同食品碳排放情况概述")
plt.savefig("单位碳排放概述.png",fontsize=12)
#plt.show()

import xlwt
book=xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet=book.add_sheet('boxblots', cell_overwrite_ok=True)
sheet_sensitive = book.add_sheet("sensitive", cell_overwrite_ok = True)


a=[]
table_label=["0",".25",".5",".75","1"]
for i in range(0,5):
    sheet.write(0,i+1,table_label[i])
a.append(numpy.percentile(veg_Data, (0,25, 50, 75,100), interpolation='midpoint'))
a.append(numpy.percentile(fruit_Data, (0,25, 50, 75,100), interpolation='midpoint'))
a.append(numpy.percentile(meat_Data[0], (0,25, 50, 75,100), interpolation='midpoint'))
a.append(numpy.percentile(meat_Data[1], (0,25, 50, 75,100), interpolation='midpoint'))
a.append(numpy.percentile(meat_Data[2], (0,25, 50, 75,100), interpolation='midpoint'))
a.append(numpy.percentile(meat_Data[3], (0,25, 50, 75,100), interpolation='midpoint'))

for i in range(0,len(a)):
    sheet.write(i+1,0,food_name[i])
    for j in range(0,len(table_label)):
        sheet.write(i+1,j+1,a[i][j])
book.save("Boxplots.xls")


#绘图2 每种食物不同技术单元

emissions_veg=[]
emissions_fruit=[]
emissions_meat=[]
for m in range(0,len(disposal_percent)):
        for n in range(0,len(energy)):
            i=0
            for a in sell_veg:
                j=0
                for b in trans2_veg:
                    k=0
                    for c in store1_veg:
                        l=0
                        for d in trans1_veg:
                            e1=get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission_veg)
                            e2=get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission_veg)
                            emissions_veg.append((e1,(1-package_percent_veg)*sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*energy_percent[n]*disposal_percent[m],i,j,k,l,0,n,m))
                            emissions_veg.append((e2,package_percent_veg*sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*energy_percent[n]*disposal_percent[m],i,j,k,l,1,n,m))
                            l+=1
                        k+=1
                    j+=1
                i+=1
            i=0
            for a in sell_fruit:
                j=0
                for b in trans2_fruit:
                    k=0
                    for c in store1_fruit:
                        l=0
                        for d in trans1_fruit:
                            e1=get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission_fruit)
                            e2=get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission_fruit)
                            emissions_fruit.append((e1,(1-package_percent_fruit)*sell_fruit_percent[i]*trans2_fruit_percent[j]*store1_fruit_percent[k]*trans1_fruit_percent[l]*energy_percent[n]*disposal_percent[m],i%2,j%2,k%2,l%2,0,n,m))
                            emissions_fruit.append((e2,package_percent_fruit*sell_fruit_percent[i]*trans2_fruit_percent[j]*store1_fruit_percent[k]*trans1_fruit_percent[l]*energy_percent[n]*disposal_percent[m],i%2,j%2,k%2,l%2,1,n,m))
                            l+=1
                        k+=1
                    j+=1
                i+=1
            i=0
            for a in sell_meat:
                j=0
                for b in trans2_meat:
                    k=0
                    for c in store1_meat:
                        l=0
                        for d in trans1_meat:
                            e1=get_emission_meat(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission_meat)
                            e2=get_emission_meat(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission_meat)
                            emissions_meat.append((e1,(1-package_percent_meat)*sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*energy_percent[n]*disposal_percent[m],i,j,k,l,0,n,m))
                            emissions_meat.append((e2,package_percent_meat*sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*energy_percent[n]*disposal_percent[m],i,j,k,l,1,n,m))
                            l+=1
                        k+=1
                    j+=1
                i+=1

emissions_veg.sort(key=lambda x:x[0])
emissions_fruit.sort(key=lambda x:x[0])
emissions_meat.sort(key=lambda x:x[0])


import copy

veg_x =[
    [[],[]],
    [[],[],[],[]],
    [[],[]],
    [[],[],[],[]],
    [[],[]],
    [[],[],[],[]],
    [[],[],[],[]],
]

veg_data2_ranged =[
    ([],[]),
    ([],[],[],[]),
    ([],[]),
    ([],[],[],[]),
    ([],[]),
    ([],[],[],[]),
    ([],[],[],[]),
]

fruit_data2_ranged =[
    ([],[]),
    ([],[],[],[]),
    ([],[]),
    ([],[],[],[]),
    ([],[]),
    ([],[],[],[]),
    ([],[],[],[]),
]

meat_base=[
    ([],[]),
    ([],[],[],[]),
    ([],[]),
    ([],[]),
    ([],[]),
    ([],[],[],[]),
    ([],[],[],[]),
]

meat_x=[]
for i in range(0,4):
    meat_x.append(copy.deepcopy(meat_base))
meat_y=copy.deepcopy(meat_x)

fruit_x=copy.deepcopy(veg_x)
fruit_y=copy.deepcopy(veg_x)
veg_y=copy.deepcopy(veg_x)

labels_veg=[]
labels_meat=[]
for item in name:
    labels_veg.append(item)
for item in name_meat:
    labels_meat.append(item)
labels_meat.append(["包装","无包装"])
labels_meat.append(energyname)
labels_meat.append(disposal_name)
labels_veg.append(["包装","无包装"])
labels_veg.append(energyname)
labels_veg.append(disposal_name)
labels_fruit=copy.deepcopy(labels_veg)

labels_meat_fin=[]
for i in range(0,4):
    labels_meat_fin.append(copy.deepcopy(labels_meat))
labels_meat=["牛肉","羊肉","猪肉","禽肉"]

for j in range(0,len(labels_meat_fin)):
    for a in labels_meat_fin[j]:
        for i in range(0,len(a)):
            a[i]=labels_meat[j]+a[i]

for a in labels_veg:
    for i in range(0,len(a)):
        a[i]="蔬菜"+a[i]
for a in labels_fruit:
    for i in range(0,len(a)):
        a[i]="水果"+a[i]


for data in emissions_veg:
    for i in range(0,len(veg_x)):
        #print("{}:sign={},max={}".format(i,data[i+2],len(v eg_x[i])))
        veg_x[i][data[i+2]].append(data[0])
        veg_y[i][data[i+2]].append(data[1])

for data in emissions_fruit:
    for i in range(0,len(veg_x)):
        #print("{}:sign={},max={}".format(i,data[i+2],len(veg_x[i])))
        fruit_x[i][data[i+2]].append(data[0])
        fruit_y[i][data[i+2]].append(data[1])

for data in emissions_meat:
    for i in range(0,len(meat_x[0])):
        meat_x[int(data[5]/2)][i][data[i+2]%len(meat_x[int(data[5]/2)][i])].append(data[0])
        meat_y[int(data[5]/2)][i][data[i+2]%len(meat_x[int(data[5]/2)][i])].append(data[1])

for category in veg_y:
    for sequence in category:
        if len(sequence) == 0:
            break
        for i in range(1,len(sequence)):
            sequence[i]+=sequence[i-1]
        final=sequence[-1]
        for i in range(1,len(sequence)):   
            sequence[i]/=final

for category in fruit_y:
    for sequence in category:
        if len(sequence) == 0:
            break
        for i in range(1,len(sequence)):
            sequence[i]+=sequence[i-1]
        final=sequence[-1]
        for i in range(1,len(sequence)):   
            sequence[i]/=final

for kind in meat_y:
    for category in kind:
        for sequence in category:
            if len(sequence) == 0:
                break
            for i in range(1,len(sequence)):
                sequence[i] += sequence[i-1]
            final=sequence[-1]
            for i in range(1,len(sequence)):
                sequence[i]/=final 

colors=["blue","red","green","grey","purple","brown","orange"]
styles=["--","-.",":"]
label_subplots=["售卖","市内运输","存储","省际运输","包装","新能源","废弃物处理"]


fig,axs = plt.subplots(4,2,sharey=True,sharex=True,figsize=(15,15))
for i in range(0,len(veg_x)):
    axs[i%4,int(i/4)].plot(veg_x[i][0],veg_y[i][0],color=colors[2],label=labels_veg[i][0])
    axs[i%4,int(i/4)].plot(fruit_x[i][0],fruit_y[i][0],color=colors[4],label=labels_fruit[i][0])
    for j in range(1,len(veg_x[i])):
        axs[i%4,int(i/4)].plot(veg_x[i][j],veg_y[i][j],color=colors[2],linestyle=styles[j-1],label=labels_veg[i][j])
        axs[i%4,int(i/4)].plot(fruit_x[i][j],fruit_y[i][j],color=colors[4],linestyle=styles[j-1],label=labels_fruit[i][j])
    axs[i%4,int(i/4)].legend(loc="upper left")
    axs[i%4,int(i/4)].set_title(label_subplots[i])

axs[0,0].set(ylim=(0,1))
for i in range(0,4):
    axs[i,0].set_ylabel("累积频率")
for i in range(0,2):
    axs[3,i].set_xlabel("单位碳排放(kgCO2e/kg)")
plt.suptitle("蔬果类每环节不同决策下碳排放的条件累积分布",fontsize=15)
plt.subplots_adjust(wspace =0)
plt.savefig('蔬果 条件分布的累积分布.png')
plt.show()

fig,axs_meat = plt.subplots(4,2,sharey=True,sharex=True,figsize=(15,15))
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.rcParams['font.size']=6
for k in range(0,len(meat_x)):
    for i in range(0,len(meat_x[k])):
        axs_meat[i%4,int(i/4)].plot(meat_x[k][i][0],meat_y[k][i][0],color=colors[k+3],label=labels_meat_fin[k][i][0])
        axs_meat[i%4,int(i/4)].set_title(label_subplots[i])
        for j in range(1,len(meat_x[k][i])):
            axs_meat[i%4,int(i/4)].plot(meat_x[k][i][j],meat_y[k][i][j],color=colors[k+3],linestyle=styles[j-1],label=labels_meat_fin[k][i][j])
        axs_meat[i%4,int(i/4)].legend(loc="upper left")

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.rcParams['font.size']=9
axs_meat[0,0].set(ylim=(0,1))
for i in range(0,4):
    axs_meat[i,0].set_ylabel("累积频率")
for i in range(0,2):
    axs_meat[3,i].set_xlabel("单位碳排放(kgCO2e/kg)")
plt.subplots_adjust(wspace =0)
plt.suptitle("肉类每环节不同决策下碳排放的条件累积分布",fontsize=12)
plt.savefig('肉类 条件分布的累积分布.png')
plt.show()