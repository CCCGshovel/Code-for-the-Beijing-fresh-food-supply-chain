#首先我们需要重构我们的基本数据结构，否则修改起来太恶心人了
#最初的模型框架得改改了

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

import random 
import copy

JS_result=[]
initial_distribution=[]
for i in range(0,6):
    JS_result.append([])
    initial_distribution.append([])

#生成一数组描述随机分布
for i in range(0,6):
    for j in range(0,30000):
        final_choice = []
        for k in range(0,7):
            decide=random.randint(0,10000)/10000
            for l in range(0,len(percent_cum[i][k])):
                if decide <= percent_cum[i][k][l]:
                    final_choice.append(l)
                    break
        a = sell[i][final_choice[0]]
        b = trans2[i][final_choice[1]]
        c = store1[i][final_choice[2]]
        d = trans1[i][final_choice[3]]
        if i <=1:
            initial_distribution[i].append(get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],final_choice[4],energy[final_choice[5]],disposal[final_choice[6]],package_emission[i]))
        else:
            initial_distribution[i].append(get_emission_meat(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],final_choice[4],energy[final_choice[5]],disposal[final_choice[6]],package_emission[i]))

import numpy

init_dis=[]
for i in range(0,6):
    initial_distribution[i].sort()
    init_dis.append(numpy.asarray(initial_distribution[i]))


#test:第一级为6种食物，第二级为七种决策，第三级为每种决策对应的随机数据点组合
#testnp，算js散度输入要求numpy矩阵，存储顺序与test等同
test = []
test_np = []
for i in range(0,6):
    fin=[]
    for j in range(0,len(percent_cum[i])):
        fin1=[]
        for k in range(0,len(percent_cum[i][j])):
            fin1.append([])
        fin.append(fin1)
    test.append(fin)

for i in range(0,6):
    fin=[]
    for j in range(0,len(percent_cum[i])):
        fin.append([])
    test_np.append(fin)

#每组采样计算，用大量随机点描述分布
for i in range(0,6):
    for j in range(0,30000):
        if j%2000 == 0:
            print("i:{} j:{}".format(i,j))
        final_choice=[]
        for k in range(0,7):
            decide=random.randint(0,10000)/10000
            for l in range(0,len(percent_cum[i][k])):
                if decide <= percent_cum[i][k][l]:
                    final_choice.append(l)
                    break
        for m in range(0,len(percent_cum[i])):
            for t in range(0,len(percent_cum[i][m])):
                choice_t = copy.deepcopy(final_choice)
                choice_t[m] = t
                a = sell[i][choice_t[0]]
                b = trans2[i][choice_t[1]]
                c = store1[i][choice_t[2]]
                d = trans1[i][choice_t[3]]
                if i <=1:
                    test[i][m][t].append(get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],choice_t[4],energy[choice_t[5]],disposal[choice_t[6]],package_emission[i]))
                else:
                    test[i][m][t].append(get_emission_meat(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],choice_t[4],energy[choice_t[5]],disposal[choice_t[6]],package_emission[i]))
        
#将生成的test[i][j][k]的万个数据点转换排序，
for i in range(0,len(test)):
    for j in range(0,len(test[i])):
        for k in range(0,len(test[i][j])):
            test[i][j][k].sort()
            test_np[i][j].append(numpy.asarray(test[i][j][k]))

import scipy.stats as st
#js散度计算，输入两等长列表计算
def js(a,b):
    m=(a+b)/2
    return (st.entropy(a,m))/2+(st.entropy(b,m))/2

#存储JS散度的输出结果，因为不考虑排序所以直接一个列表拉通
final_Result=[]
for i in range(0,6):
    final_Result.append([])

for i in range(0,6):
    for j in range(0,len(test_np[i])):
        for k in range(0,len(test_np[i][j])):
            final_Result[i].append(int(1000*numpy.log10(js(init_dis[i],test_np[i][j][k])))/1000)

for i in range(2,6):
    final_Result[i].insert(8,-10)
    final_Result[i].insert(10,-10)

for item in final_Result:
    print(item)
    print(len(item))

import matplotlib.pyplot as plt

#热力图用标签（横坐标）
food = ["蔬菜","水果","牛肉","羊肉","猪肉","禽肉"]

#画热力图用的标签（纵坐标）
choice = [
    "售卖常温","售卖冷链",
    "市内运输常温","市内运输冷链","市内运输常温新能源","市内运输冷链新能源",
    "存储常温","存储新能源",
    "省际运输常温","省际运输冷链","省际运输常温新能源","省际运输冷链新能源",
    "无包装","包装",
    "火电","水电","核电","太阳能",
    "填埋","厌氧消化","堆肥","焚烧 "
]


#画箱式图用的标签，分了列表
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

#js散度的热力图

"""
result = numpy.array(final_Result)
result_t=result.transpose()

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.rcParams['font.size']=9

fig,ax = plt.subplots(figsize=(15,13))
a = ax.imshow(result_t,vmin=-7,vmax=-2,aspect="auto",cmap='Blues')
tickx=[]
ticky=[]
for i in range(0,len(choice)):
    ticky.append(i)
for i in range(0,len(food)):
    tickx.append(i)
for edge, spine in ax.spines.items():
        spine.set_visible(False)
ax.set_yticks(ticky,minor=False)
ax.set_yticklabels(choice,rotation=45)
ax.set_xticks(tickx,minor=False)
ax.set_xticklabels(food)
ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)
fig.colorbar(a)
for i in range(len(food)):
    for j in range(len(choice)):
        data = "Na"
        if result_t[j, i] != -10:
            data = result_t[j, i]
        if result_t[j , i] >= -5:
            text = ax.text(i, j, data,ha="center", va="center", color="w")
        else:
            text = ax.text(i, j, data,ha="center", va="center", color="black")
ax.set_title("不同食物在不同决策下JS散度")
#plt.savefig("JS汇总.png")
#plt.show()
"""

#分不同门类的箱式图
"""
#箱式图的横坐标标签生成用
name=["蔬菜","水果","牛肉","羊肉","猪肉","禽肉"]

fig,axs = plt.subplots(4,2,sharey=True,sharex=False,figsize=(15,15))

color=["green","purple"]
label_subplots=["售卖","市内运输","存储","省际运输","包装","新能源","废弃物处理"]
blots=[]
for i in range(0,len(percent_cum[0])):
    data_box=[]
    label=[]
    print("{}:".format(label_subplots[i]))
    for j in range(0,2):
        label_t=copy.deepcopy(choice_2[i])
        for item in label_t:
            item=name[j]+item
            label.append(item)
        for k in range(0,len(test[j][i])):
            data_box.append(test[j][i][k])
            print("{}:{}".format(label[k+j*len(test[j][i])],numpy.percentile(test[j][i][k], (0,25, 50, 75,100), interpolation='midpoint')))
    blots.append(axs[i%4,int(i/4)].boxplot(data_box, widths=len(data_box)/16, patch_artist=True,
                showmeans=False, showfliers=False,
                whis=(0,100),
                medianprops={"color": "black", "linewidth": 0.3},
                boxprops={"facecolor": "C0", "edgecolor": "black","linewidth": 1},
                whiskerprops={"color": "black", "linewidth": 1.5},
                capprops={"color": "black", "linewidth": 1.5},labels=label))
    for tick in axs[i%4,int(i/4)].get_xticklabels():
        tick.set_rotation(25)
    axs[i%4,int(i/4)].set_title(label_subplots[i])
j=0
sign = -1
for item in blots:
    i=0
    for patch in item["boxes"]:
        if i % len(percent_cum[0][j]) == 0:
            sign+=1
        patch.set_facecolor(color[sign])
        i += 1
    j += 1
    sign = -1


plt.suptitle("不同决策的条件分布下单位质量蔬果类生鲜碳排放",fontsize=15)
plt.savefig("条件分布 箱式图_蔬果.png")
for i in range(0,4):
    axs[i,0].set_ylabel("单位碳排放(kgCO2e/kg)")
#plt.show()



fig,axs_meat = plt.subplots(4, 7, sharex="col", sharey="row", figsize=(10, 8))
blots_meat=[]
color=["red","orange","grey","yellow"]
label_subplots=["售卖","市内运输","存储","省际运输","包装","新能源","废弃物处理"]
blots=[]
for i in range(0,len(percent_cum[0])):
    for j in range(2,6):
        data_box=[]
        for k in range(0,len(test[j][i])):
            data_box.append(test[j][i][k])
            #print("{}:{}".format(label[k+(j-2)*len(test[j][i])],numpy.percentile(test[j][i][k], (0,25, 50, 75,100), interpolation='midpoint')))
        print("i:{} j:{}".format(i,j))
        a = (axs_meat[j-2, i].boxplot(data_box, widths=len(data_box)/16, patch_artist=True,
                showmeans=False, showfliers=False,
                whis=(0,100),
                medianprops={"color": "black", "linewidth": 0.3},
                boxprops={"facecolor": "C0", "edgecolor": "black","linewidth": 1},
                whiskerprops={"color": "black", "linewidth": 1.5},
                capprops={"color": "black", "linewidth": 1.5},labels=choice_3[i]))
        for patch in a["boxes"]:
            patch.set_facecolor(color[j-2])
        for tick in axs_meat[j-2,i].get_xticklabels():
            tick.set_rotation(45)
for i in range(0,4):
    axs_meat[i,0].set_ylabel(name[i+2]+"单位碳排放(kgCO2e/kg)")
for j in range(0,7):
    axs_meat[0,j].set_title(label_subplots[i])

plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.1, hspace=0.2)
plt.suptitle("不同决策的条件分布下单位质量肉类类生鲜碳排放", fontsize=15)
plt.savefig("条件分布 箱式图_肉类.png")
"""

#现在的目标，把这几个分布转成。。。带errorbar的柱状图
#然后
import brewer2mpl
bmap = brewer2mpl.get_map('Set3', 'qualitative', 10)

meat_percent=[3.1/27.3,3.9/27.3,15.3/27.3,5/27.3]
blots=[]
for i in range(0,2):
    a=[]
    for j in range(0,7):
        b=[]
        for k in range(0,len(choice_3[j])):
            b.append(0)
        a.append(b)
    blots.append(a)
for f in range(2,6):
    for i in range(0,7):
        blots[1][i]
