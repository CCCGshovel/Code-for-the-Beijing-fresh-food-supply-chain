#目的：用箱式图？柱状图？表现不同情景下的排放状况
from 通用碳排放框架 import choice_veg, choice_meat, sell, store1, trans2, trans1, food, produce, energy, disposal, energyname, disposal_name, package_emission
from 通用碳排放框架 import percent, per_cum, mass

from 情景模拟 import percent_ecommerce, percent_market, percent_supermarket, distance_short, distance_long

percentcum_supermarket = per_cum(percent_supermarket)
percentcum_ecommerce = per_cum(percent_ecommerce)
percentcum_market = per_cum(percent_market)
#由于要绘制琵琶图，因此要进行随机采样，现将情景模拟里的基础比例数据转化为累积比例
#存储在percent_init里，便于一个参数直接调用（后续mode0~2）
percent_init = [percent_supermarket,percent_ecommerce,percent_market]

percent_cum = [percentcum_supermarket,percentcum_ecommerce,percentcum_market]

for m in range(0,3):
    for f in range(0,6):
        for l in range(0,7):
            print("m:{} f:{} l:{} {}".format(m,f,l,percent_cum[m][f][l]))

def production_emission(f,mass,n):
    e = produce[f][0] * mass
    for i in range(1,len(produce[f])):
        e += produce[f][i] * mass
    return e
    
#输入：8个标准参数（见通用框架表头），及mode0~2，返回当前技术组合下1kg的碳排放（不含比例）
#mode见开头percent_init的顺序
def get_emissions(f,i,j,k,l,p,n,m,mode):
    #a\b\c\d\e分别为销售市内库存省际生产对应的元组,p:是否包装,energy:能耗，dis：废弃物处理方式
    #0.525为经过文献及实地调研对包装效果的预估值，结合JCP2021内线性模型以及保质期在包装前后变化的文献得出
    a = sell[f][i]
    b = trans2[f][j]
    c = store1[f][k]
    d = trans1[f][l]
    percent_line = percent_init[mode][f][0][i]*percent_init[mode][f][1][j]*percent_init[mode][f][2][k]*percent_init[mode][f][3][l]*percent_init[mode][f][4][p]*percent_init[mode][f][5][n]*percent_init[mode][f][6][m]
    if p >= 1:
        packaged = 1
    else:
        packaged = 0
    if f >= 2:
        length = 2
    else:
        length = 4
    if l >= length:
        dis = distance_short[f][mode]
    else:
        dis = distance_long[f][mode]     
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
        e_total += m3 * 0.026 * energy[n]
        e_total += m3 * 0.1 * disposal[m]
        e_total += production_emission(f,m3*0.1,n)
    m4 = m3 / (1 - lr4)
    e_total += d[1]*dis*m4
    e_total += (m4-m3) * disposal[m]
    e_total += production_emission(f,m4-m3,n)
    #返回1kg的完整碳排放
    return e_total

import random

BoxplotData = [
    #超市(6种f,同food顺序，下同)
    [[],[],[],[],[],[]],
    #生鲜电商（6种）
    [[],[],[],[],[],[]],
    #菜市场（6种）
    [[],[],[],[],[],[]]
]

#对消费量进行累积
consumption_meat=[3.9/27.3,3.1/27.3,15.3/27.3,5/27.3]
consumption_veg = [122.7/(122.7+81.9),81.9/(122.7+81.9)]
for i in range(1,len(consumption_veg)):
    consumption_veg[i] += consumption_veg[i-1]
for i in range(1,len(consumption_meat)):
    consumption_meat[i] += consumption_meat[i-1]

#这俩函数是直接抄的官网案例代码，用来调整琵琶图的格式，忽略即可
def adjacent_values(vals, q1, q3):
    upper_adjacent_value = q3 + (q3 - q1) * 1.5
    upper_adjacent_value = np.clip(upper_adjacent_value, q3, vals[-1])

    lower_adjacent_value = q1 - (q3 - q1) * 1.5
    lower_adjacent_value = np.clip(lower_adjacent_value, vals[0], q1)
    return lower_adjacent_value, upper_adjacent_value


def set_axis_style(ax, labels):
    ax.xaxis.set_tick_params(direction='out')
    ax.xaxis.set_ticks_position('bottom')
    ax.set_xticks(np.arange(1, len(labels) + 1))
    ax.set_xlim(0.25, len(labels) + 0.75)

#输出表格，但这里只定义了表格以及写表头
import xlwt
book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = []
label_sheet = ["Supermarket", "E-commerse", "Market"]
label_title = ["Veg", "Fruit", "Beef", "Lamb", "Pork", "Chicken"]
for i in range(0,len(label_sheet)):
    sheet1 = book.add_sheet(label_sheet[i], cell_overwrite_ok = True)
    for j in range(0,len(label_title)):
        sheet1.write(0, 2*j, label_title[j])
    sheet.append(sheet1)

sheet.append(book.add_sheet("Emission", cell_overwrite_ok=True))
#mode0~3：顺序依照percent_init
for mode in range(0,3):
    for f in range(0,6):
        #test为循环次数，随机采样次数
        for test in range(0,20000):
            if test%2000 == 0:
                print("f:{} test:{}".format(f,test))
            choice = []
                #技术环节里不同选择,choice[0]~[6]分别表示顺次的每个环节（顺序见percent定义）
            for l in range(0,7):
                decide = random.random()
                for m in range(0,len(percent_cum[mode][f][l])):
                    if decide <= percent_cum[mode][f][l][m]:
                        choice.append(m)
                        break
                #对每个技术的每个选项固定，以衡量其采样结果
            emission = get_emissions(f,choice[0],choice[1],choice[2],choice[3],choice[4],choice[5],choice[6],mode)
            BoxplotData[mode][f].append(emission)
                #print(emissions_joint[i][k][t][0][-1])
            sheet[mode].write(test+1, 2*f, emission)

from numpy import mean
for f in range(0,6):
    print("{} {} {}".format(mean(BoxplotData[0][f]),mean(BoxplotData[1][f]),mean(BoxplotData[2][f]),))

for m in range(0,3):
    for f in range(0,6):
        BoxplotData[m][f].sort()

from matplotlib import pyplot as plt 
import numpy as np

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.rcParams['font.size']=9

fig, axs = plt.subplots(nrows=3, ncols=2 ,sharex="all" ,dpi = 300)

label = ["超市","生鲜电商","菜市场"]
#绘制琵琶图
for f in range(0,6):
    data = []
    for mode in range(0,3):
        data.append(BoxplotData[mode][f])
    quartile1, medians, quartile3 = np.percentile(data, [25, 50, 75], axis=1)
    parts = axs[int(f/2),f%2].violinplot(data,showmeans=False, showmedians=False,showextrema=False)
    parts["bodies"][0].set_facecolor('#D43F3A')
    parts["bodies"][1].set_facecolor('#6BA21C')
    parts["bodies"][2].set_facecolor('#5A432B')
    for pc in parts['bodies']:
        pc.set_edgecolor('black')
        pc.set_alpha(0.8)
    whiskers = np.array([
    adjacent_values(sorted_array, q1, q3)
    for sorted_array, q1, q3 in zip(data, quartile1, quartile3)])
    whiskers_min, whiskers_max = whiskers[:, 0], whiskers[:, 1] 
    inds = np.arange(1, len(medians) + 1)
    axs[int(f/2),f%2].scatter(inds, medians, marker='o', color='white', s=5, zorder=3)
    axs[int(f/2),f%2].vlines(inds, quartile1, quartile3, color='k', linestyle='-', lw=5)
    axs[int(f/2),f%2].vlines(inds, whiskers_min, whiskers_max, color='k', linestyle='-', lw=1)
    axs[int(f/2),f%2].set_title(food[f])
    set_axis_style(axs[int(f/2),f%2], label)
    plt.xticks(ticks=[1,2,3], labels=label)
for m in range(0,3):
    axs[m,0].set_ylabel("碳排放kgCO2e/kg")

plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.5, hspace=0.5)
plt.suptitle("不同供应模式的碳排放")
#plt.savefig("作图\\同供应模式碳排放比较.png")
plt.show()

average_e = [
    [],[],[]
]

for f in range(0,6):
    for mode in range(0,3):
        average_e[mode].append(np.mean(BoxplotData[mode][f]))
print(average_e)
#输出疫情前中后的比例
#每行代表疫情前中后
#每列代表不同供应模式
percent = [
    [0.4034,0.1612,0.4355],
    [0.3699,0.3570,0.2731],
    [0.4453,0.2397,0.3150]
]

#疫情前中后输出位表格
label_time = ["Pre", "During", "Post"]

for f in range(0,6):
    sheet[-1].write(0, f + 1, food[f])
    for mode in range(0,3):
        e = 0
        for j in range(0,3):
            e += percent[j][mode] * average_e[j][f]
        sheet[-1].write(mode + 1, f + 1, e)
    for mode in range(0,3):
        sheet[-1].write(mode + 1, 0, label_time[mode])


book.save("Mode_distribution.xls")
