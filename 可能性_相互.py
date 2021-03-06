choice_2=[
    ["售卖常温","售卖冷链"],
    ["市内运输常温","市内运输冷链","市内运输常温新能源","市内运输冷链新能源",],
    ["存储常温","存储新能源",],
    ["省际运输常温","省际运输冷链","省际运输常温新能源","省际运输冷链新能源",],
    ["无包装","包装",],
    ["火电","水电","核电","太阳能",],
    ["填埋","厌氧消化","堆肥","焚烧"]
]

choice_3=[
    ["售卖常温","售卖冷链"],
    ["市内常温","市内冷链","常温新能源","冷链新能源",],
    ["存储常温","存储新能源",],
    ["活畜","活畜新能源"],
    ["无包装","包装",],
    ["火电","水电","核电","太阳能",],
    ["填埋","厌氧消化","堆肥","焚烧"]
]


sell=[
    #蔬菜
    [(0.08625,0,0.625,0,"常温"),
    (0.08625/3,0.0003,0.625,0.00005644,'冷链')],
    #水果
    [(0.2*0.9,0,0.625,0,"常温"),
    (0.2*0.9/3,0.0003,0.625,0.00005644,"冷链")],
    #肉类(四种)
    [(0.013325,0,0.625,0,"常温"),
    (0.013325/3,0.0006,0.625,0.00005644,"冷链")],
    [(0.013325,0,0.625,0,"常温"),
    (0.013325/3,0.0006,0.625,0.00005644,"冷链")],
    [(0.013325,0,0.625,0,"常温"),
    (0.013325/3,0.0006,0.625,0.00005644,"冷链")],
    [(0.013325,0,0.625,0,"常温"),
    (0.013325/3,0.0006,0.625,0.00005644,"冷链")],
]


food = ["蔬菜","水果","牛肉","羊肉","猪肉","禽肉"]

trans2_dis = 30
veg_trans1_dis = 935.87
fruit_trans1_dis = 1443.0488
meat_trans1_dis = 726.497 

trans2=[
    #蔬菜
    [(0.17*trans2_dis/veg_trans1_dis, 0.0000519, trans2_dis),
    (0.09*trans2_dis/veg_trans1_dis, 0.000186, trans2_dis),
    (0.17*trans2_dis/veg_trans1_dis, 0.0000519*0.576, trans2_dis),
    (0.09*trans2_dis/veg_trans1_dis, 0.000186*0.576, trans2_dis)],
    #水果
    [(0.20*trans2_dis/fruit_trans1_dis, 0.0000519, trans2_dis),
    (0.10*trans2_dis/fruit_trans1_dis, 0.000186, trans2_dis),
    (0.20*trans2_dis/fruit_trans1_dis, 0.0000519*0.576, trans2_dis),
    (0.10*trans2_dis/fruit_trans1_dis, 0.000186*0.576, trans2_dis)],
    #肉类
    [(0.015, 0.0001663, trans2_dis),
    (0.005, 0.0002461, trans2_dis),
    (0.015, 0.0001663*0.576, trans2_dis),
    (0.005, 0.0002461*0.576, trans2_dis)],
    [(0.015, 0.0001663, trans2_dis),
    (0.005, 0.0002461, trans2_dis),
    (0.015, 0.0001663*0.576, trans2_dis),
    (0.005, 0.0002461*0.576, trans2_dis)],
    [(0.015, 0.0001663, trans2_dis),
    (0.005, 0.0002461, trans2_dis),
    (0.015, 0.0001663*0.576, trans2_dis),
    (0.005, 0.0002461*0.576, trans2_dis)],
    [(0.015, 0.0001663, trans2_dis),
    (0.005, 0.0002461, trans2_dis),
    (0.015, 0.0001663*0.576, trans2_dis),
    (0.005, 0.0002461*0.576, trans2_dis)],
]

store1=[
    #蔬菜
    [(0.15,0,2.5,0),
    (0.05,0.0003,2.5,0.00005644)],
    #水果
    [(0.075,0,2.5,0),
    (0.025,0.0003,2.5,0.00005644)],
    #肉类
    [(0.0533,0,2.5,0),
    (0.0533/3,0.0003,2.5,0.00005644)],
    [(0.0533,0,2.5,0),
    (0.0533/3,0.0003,2.5,0.00005644)],
    [(0.0533,0,2.5,0),
    (0.0533/3,0.0003,2.5,0.00005644)],
    [(0.0533,0,2.5,0),
    (0.0533/3,0.0003,2.5,0.00005644)],
]

trans1=[
    #蔬菜
    [(0.17,0.0000519,veg_trans1_dis,0.3),
    (0.09,0.000186,veg_trans1_dis,0.307144),
    (0.17,0.0000519*0.576,veg_trans1_dis,0.3),
    (0.09,0.000186*0.576,veg_trans1_dis,0.307144)],
    #水果
    [(0.20,0.0000519,fruit_trans1_dis,0.32),
    (0.10,0.000186,fruit_trans1_dis,0.327144),
    (0.20,0.0000519*0.576,fruit_trans1_dis,0.32),
    (0.10,0.000186*0.576,fruit_trans1_dis,0.327144)],
    #肉类
    [(0.01,0.0000519,meat_trans1_dis,29.78),
    (0.01,0.0000519*0.576,meat_trans1_dis,29.78)],
    [(0.01,0.0000519,meat_trans1_dis,24.37),
    (0.01,0.0000519*0.576,meat_trans1_dis,24.37)],
    [(0.01,0.0000519,meat_trans1_dis,4.66),
    (0.01,0.0000519*0.576,meat_trans1_dis,4.66)],
    [(0.01,0.0000519,meat_trans1_dis,11.3),
    (0.01,0.0000519*0.576,meat_trans1_dis,11.3)]
]

percent_cum=[
    #蔬菜
    [
        [0.58,1],
        [0.865*0.99, 0.865*0.99+0.135*0.99, 0.99+0.865*0.01,1],
        [0.83,1],
        [0.865*0.99, 0.865*0.99+0.135*0.99, 0.99+0.865*0.01,1],
        [1-0.68,1],
        [0.818,0.155+0.818,0.155+0.818+0.019,1],
        [0.25,0.375,0.5,1]
    ],
    #水果
    [
        [0.83,1],
        [0.865*0.99, 0.865*0.99+0.135*0.99, 0.99+0.865*0.01,1],
        [0.83,1],
        [0.865*0.99, 0.99, 0.99+0.865*0.01,1],
        [1-0.608,1],
        [0.818,0.155+0.818,0.155+0.818+0.019,1],
        [0.25,0.375,0.5,1]
    ],
    #肉类
    [
        [0.15,1],
        [0.58*0.99,0.99,0.9958,1],
        [0.15,1],
        [0.99,1],
        [0.35,1],
        [0.818,0.155+0.818,0.155+0.818+0.019,1],
        [0.25,0.375,0.5,1],
    ],
    [
        [0.15,1],
        [0.58*0.99,0.99,0.9958,1],
        [0.15,1],
        [0.99,1],
        [0.35,1],
        [0.818,0.155+0.818,0.155+0.818+0.019,1],
        [0.25,0.375,0.5,1],
    ],
    [
        [0.15,1],
        [0.58*0.99,0.99,0.9958,1],
        [0.15,1],
        [0.99,1],
        [0.35,1],
        [0.818,0.155+0.818,0.155+0.818+0.019,1],
        [0.25,0.375,0.5,1],
    ],
    [
        [0.15,1],
        [0.58*0.99,0.99,0.9958,1],
        [0.15,1],
        [0.99,1],
        [0.35,1],
        [0.818,0.155+0.818,0.155+0.818+0.019,1],
        [0.25,0.375,0.5,1],
    ],
]

percent=[
    [
        [0.58,0.42],
        [0.865*0.99, 0.135*0.99, 0.865*0.01,0.135*0.01],
        [0.83,0.17],
        [0.865*0.99, 0.135*0.99, 0.865*0.01,0.135*0.01],
        [1-0.68,0.68],
        [0.818,0.155,0.019,0.008],
        [0.25,0.125,0.125,0.5]
    ],
    #水果
    [
        [0.83,0.17],
        [0.865*0.99, 0.135*0.99, 0.865*0.01, 0.135*0.01],
        [0.83,0.17],
        [0.865*0.99, 0.135*0.99, 0.865*0.01, 0.135*0.01],
        [1-0.608,0.608],
        [0.818,0.155,0.019,0.008],
        [0.25,0.125,0.125,0.5]
    ],
    #肉类
    [
        [0.15,0.85],
        [0.58*0.99,0.99*0.42,0.58*0.01,0.42*0.01],
        [0.15,0.85],
        [0.99,0.01],
        [0.35,0.65],
        [0.818,0.155,0.019,0.008],
        [0.25,0.125,0.125,0.5]
    ],
    [
        [0.15,0.85],
        [0.58*0.99,0.99*0.42,0.58*0.01,0.42*0.01],
        [0.15,0.85],
        [0.99,0.01],
        [0.35,0.65],
        [0.818,0.155,0.019,0.008],
        [0.25,0.125,0.125,0.5]
    ],
    [
        [0.15,0.85],
        [0.58*0.99,0.99*0.42,0.58*0.01,0.42*0.01],
        [0.15,0.85],
        [0.99,0.01],
        [0.35,0.65],
        [0.818,0.155,0.019,0.008],
        [0.25,0.125,0.125,0.5]
    ],
    [
        [0.15,0.85],
        [0.58*0.99,0.99*0.42,0.58*0.01,0.42*0.01],
        [0.15,0.85],
        [0.99,0.01],
        [0.35,0.65],
        [0.818,0.155,0.019,0.008],
        [0.25,0.125,0.125,0.5]
    ],
]


energy=[1.28,0.00339,0.00779,0.00112]
energyname=["火电","水电","核电","太阳能"]

disposal=[0.625*0.02582/0.466,-0.02754,0.165,0.02582]
disposal_name=["填埋","厌氧消化","堆肥","焚烧"]

package_emission=[0.084,0.116,0.169,0.169,0.169,0.169]

def get_emission_meat(a0,a1,a2,a3,b0,b1,b2,c0,c1,c2,c3,proce,proce_loss,d0,d1,d2,d3,package,en,dis,pack):
    #参数表依次为商店、市内运输、库存、省际运输对应的参数、d3为生产，package为是否包装（0,1），en为单位电能的碳排放，dis为单位废弃物处理碳排放，pack为单位食物包装所对应过的碳排放
    #0.525为经过文献及实地调研对包装效果的预估值，结合JCP2021内线性模型以及保质期在包装前后变化的文献得出
    lr1 = a0*(1-package*0.475)
    lr2 = b0*(1-package*0.475)
    lr3 = c0*(1-package*0.475)
    lr4 = d0*(1-package*0.475)
    m = 1/(1 - lr1)
    e2 = 0
    e1 = m * a1*a2*en + a3
    if package == 1:
        e2 = e1 + pack
    else: 
        e2 = e1
    m = m/(1 - lr2)
    e3 = e2 + m*b1*b2
    m = m / (1 - lr3)
    e4 = e3 + m * (c1*c2*en + c3)
    m = m / (1-proce_loss)
    e5 = e4 + m * proce * en
    m = m / (1 - lr4)
    e6 = e5 + m * (d1*d2) 
    e7 = e6 + m * d3
    e8 = e7 + (m-1) * dis
    return e8

def get_emission(a0,a1,a2,a3,b0,b1,b2,c0,c1,c2,c3,d0,d1,d2,d3,package,en,dis,pack):
    #参数表依次为商店、市内运输、库存、省际运输、d3为生产，package为是否包装（0,1），en为单位电能的碳排放，dis为单位废弃物处理碳排放，pack为单位食物包装所对应过的碳排放
    #包装使得食物浪费降低损耗→0.525
    lr1 = a0*(1-package*0.475)
    lr2 = b0*(1-package*0.475)
    lr3 = c0*(1-package*0.475)
    lr4 = d0*(1-package*0.475)
    m = 1/(1 - lr1)
    e1 = m * a1*a2*en + a3
    if package == 1:
        e2 = e1 + pack
    else:
        e2 = e1
    m = m/(1 - lr2)
    e3 = e2 + m*b1*b2
    m = m / (1 - lr3)
    e4 = e3 + m * (c1*c2*en + c3)
    m = m / (1 - lr4)
    e5 = e4
    e6 = e5 + m * (d1*d2) 
    e7 = e6 + m * d3
    e8 = e7 + (m-1) * dis
    return e8

def emission(food,a0,a1,a2,a3,b0,b1,b2,c0,c1,c2,c3,proce,proce_loss,d0,d1,d2,d3,package,en,dis,pack):
    if food <2 :
        return get_emission(a0,a1,a2,a3,b0,b1,b2,c0,c1,c2,c3,d0,d1,d2,d3,package,en,dis,pack)
    else: 
        return get_emission_meat(a0,a1,a2,a3,b0,b1,b2,c0,c1,c2,c3,proce,proce_loss,d0,d1,d2,d3,package,en,dis,pack)

import random
import copy
from tkinter import ttk

posibility=[]
for f in range(0, 6):
    test = []
    if f <= 1:
        label = choice_2
    else:
        label = choice_3
    for i in range(0, 7):
        test1=[]
        for j in range(0,len(percent_cum[f][i])):
            for k in range(j+1,len(percent_cum[f][i])):
                test1.append([0, "{}>{}".format(label[i][j],label[i][k])])
        test.append(test1)
    posibility.append(test)

for item in posibility:
    print(item)

test_time=10000

for f in range(0,6):
    for j in range(0,test_time):
        if j%2000 == 0:
            print("f:{} j:{}".format(f,j))
        #其实可以做的：每个选项分别生成一组，
        for i in range(0, 7):
            comparing=[]
            for t in range(0, len(percent_cum[f][i])):
                choice = []
                for k in range(0,7):
                    decide = random.random()
                    for l in range(0,len(percent_cum[f][k])):
                        if decide <= percent_cum[f][k][l]:
                            choice.append(l)
                            break
                choice[i] = t
                a = sell[f][choice[0]]
                b = trans2[f][choice[1]]
                c = store1[f][choice[2]]
                d = trans1[f][choice[3]]
                e_test = emission(f,a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],choice[4],energy[choice[5]],disposal[choice[6]],package_emission[f])
                comparing.append(e_test)
            store_id = 0
            for m in range(0,len(comparing)):
                for n in range(m+1,len(comparing)):
                    if comparing[m] > comparing[n]:
                        posibility[f][i][store_id][0] += 1/test_time
                    store_id += 1
for food in posibility:
    for tech in food:
        print(tech)

import matplotlib.pyplot as plt
import numpy

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.rcParams['font.size']=9


for f in range(0,len(posibility)):
    posibility[f].sort(key=lambda x:x[0])

choice = [
    "售卖常温","售卖冷链",
    "市内运输常温","市内运输冷链","市内运输常温新能源","市内运输冷链新能源",
    "存储常温","存储新能源",
    "省际运输常温","省际运输冷链","省际运输常温新能源","省际运输冷链新能源",
    "无包装","包装",
    "火电","水电","核电","太阳能",
    "填埋","厌氧消化","堆肥","焚烧 "
]

fig, axs = plt.subplots(3, 2, sharey = True, figsize=(10,6))

for i in range(0,6):
    if i <= 1:
        label = choice_2
    else:
        label = choice_3
    total = 0
    for j in range(0,len(label)):
        for k in range(0,len(label[j])):
            back=[]
            back.append(1)
        x=[]
        y=[]
        for item in posibility[i]:
            x.append(item[1])
            y.append(item[0])
        total+=1
        axs[i%3,int(i/3)].bar(x,back,color="lightsteelblue")
        axs[i%3,int(i/3)].bar(x,y,color="lightsalmon")
        axs[i%3,int(i/3)].set_xticklabels(x,rotation=45)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0, hspace=0.5)
plt.savefig("概率 与原始分布比较.png")
#plt.show()
