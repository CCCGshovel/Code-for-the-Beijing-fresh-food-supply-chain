import matplotlib.pyplot as plt

#后已存入通用框架mass中
consumption_meat=[3.9/27.3,3.1/27.3,15.3/27.3,5/27.3]
consumption_veg = [122.7/(122.7+81.9),81.9/(122.7+81.9)]
for i in range(1,len(consumption_veg)):
    consumption_veg[i] += consumption_veg[i-1]
for i in range(1,len(consumption_meat)):
    consumption_meat[i] += consumption_meat[i-1]

#生成整个碳排放分布表格

#生成图片数据及随机采样结果的两个表格
import xlwt
book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = []
label_sheet = ["Figure Data", "Vegetable Distribution", "Fruit Distribution", "Meat Distribution"]
for i in range(0,len(label_sheet)):
    sheet1 = book.add_sheet(label_sheet[i], cell_overwrite_ok = True)
    sheet.append(sheet1)

from 通用碳排放框架 import choice_veg, choice_meat, sell, store1, trans2, trans1, food, produce, energy, disposal, energyname, disposal_name, package_emission
from 通用碳排放框架 import percent, per_cum

percent_cum = per_cum(percent)

#计算生产的总碳排,因为这里不区分不同排放的来源所以直接使用加和的总数据
#输入：能耗id：n、食物id：f（见通用框架choice[5],food列表）、质量m
#但因为后来不考虑生产采用新能源技术所以显得定义这个函数很可笑
#但懒得改了
def production_emission(f,m,n):
    #f：Food m：mass
    e = 0
    e += produce[f][0]*m
    for t in range(1,len(produce[f])):
        e += m * produce[f][t]
    return e

#输入：标准参数列表（见通用框架）
#输出：指定参数组合下1kg食物所需碳排（不考虑概率）
def get_emissions(f,i,j,k,l,p,n,m):
    #f：Food i：售卖的对应编号 j：市内运输的技术编号 k：存储的技术编号 l：省际运输的编号, p：包装的编号 n：电力的编号 m：废弃物处理的编号
    #通过sell[f][i]/trans2[f][j]/store1[f][k]/trans1[f][l]/package_emission[f][p]/energy[n]/disposal[m]调用该编号的碳排放因子进行计算（具体技术对应参数见定义）
    #0.525为经过文献及实地调研对包装效果的预估值,结合JCP2021内线性模型以及保质期在包装前后变化的文献得出
    #具体的标签列表,表示技术选择
    #final_choice=[choice[0][i],choice[1][j],choice[2][k],choice[3][l],choice[4][p],choice[5][n],choice[6][m]]
    #最终输出结果
    result = []
    a = sell[f][i]
    b = trans2[f][j]
    c = store1[f][k]
    d = trans1[f][l]
    #乘出对应的比例
    percent_line = percent[f][0][i]*percent[f][1][j]*percent[f][2][k]*percent[f][3][l]*percent[f][4][p]*percent[f][5][n]*percent[f][6][m]
    #是否包装,定损耗率
    if p >= 1:
        packaged = 1
    else:
        packaged = 0
    #售卖/市内/存储/省际的损耗率
    lr1 = a[0]*(1-packaged*0.475)
    lr2 = b[0]*(1-packaged*0.475)
    lr3 = c[0]*(1-packaged*0.475)
    lr4 = d[0]*(1-packaged*0.475)
    #不同环节质量变化,用累积质量/（1-当前阶段损耗率）计算。标号与损耗率同阶段
    m1 = 1/(1 - lr1)
    #商店直接碳排
    result.append(m1*a[1]*a[2]*energy[n]+m1*a[3])
    #商店FLW及废弃物处理
    result.append(production_emission(f,m1-1,n))
    result.append(disposal[m]*(m1-1))
    #包装
    result.append(package_emission[f][p])
    m2 = m1/(1 - lr2)
    #市内：直接/FLW/disposal
    result.append( b[1]*b[2]*m2 )
    result.append(production_emission(f,m2-m1,n))
    result.append(disposal[m]*(m2-m1))
    m3 = m2 / (1 - lr3)
    #存储：直接/FLW/disposal
    result.append( m3*c[1]*c[2]*energy[n])
    result.append(production_emission(f,m3-m2,n))
    result.append(disposal[m]*(m3-m2))
    if f >= 2:
        m3 = m3/0.9
        #加工：直接/FLW/disposal
        result.append( m3 * 0.026 * energy[n])
        result.append( production_emission(f,m3*0.1,n))
        result.append( m3 * 0.1 * disposal[m])
    m4 = m3 / (1 - lr4)
    #省际：直接/FLW/disposal
    result.append( d[1] * d[2] * m4)
    result.append(production_emission(f,m4-m3,n))
    result.append(disposal[m]*(m4-m3))
    #生产（1kg）
    #result.append(production_emission(f,1))
    total_e = 0#（计算总计碳排放）
    for data in result:
        total_e += data
    result.append(total_e)
    result.append(percent_line)
    if percent_line >= 1:
        print("发生什么事了")
    i = 0
    #补上标签
    #仅需要不包含生产的比例,因此输出total_e即可
    return total_e

#最终绘图数据堆放处
emissions_joint = []
#i:0~3:肉类水果蔬菜
#j:0~7：七种技术选择
#最终为3*7矩阵
for i in range(0,3):
    a = []
    if i <= 1:
        choice = choice_veg
    else:
        choice = choice_meat
    for j in range(0,7):
        b = []
        for k in range(0,len(percent[i][j])):
            b.append(([],choice[j][k]))
        a.append(b)
    emissions_joint.append(a)


import random


#i：肉食/素食，0蔬菜，1水果，2肉类
for i in range(0, 3):
    #生成随机碳排
    #j：测试次数
    for j in range(0,50000):
        #肉食素食
        test_f = random.random()
        #依据消费量随机测出f,肉食素食分别生成
        if i == 0:
            f = 0
        elif i == 1:
            f = 1
        else:
            f = 2
            #肉类需要随机采样，之后用consumption这一累积分布，采样得到具体为哪一种肉类
            for r in range(0,len(consumption_meat)):
                if test_f <= consumption_meat[r]:
                    f += r
                    break
        #方便看看随机采样到哪了,避免等的太空虚
        if j%2000 == 0:
            print("i:{} j:{}".format(i,j))
        #k：0~6，对应不同技术选择（见choice列表）
        for k in range(0, 7):
            #对每个环节随机采样
            for t in range(0,len(emissions_joint[i][k])):
                #技术环节里不同选择,choice[0]~[6]分别表示顺次的每个环节（顺序见percent定义）
                choice = []
                for l in range(0,7):
                    decide = random.random()
                    for m in range(0,len(percent_cum[f][l])):
                        if decide <= percent_cum[f][l][m]:
                            choice.append(m)
                            break
                #对每个技术的每个选项固定，以衡量其采样结果
                choice[k] = t
                #最终将每个技术选择的采样结果存入同一个列表，用以之后柱状图/箱式图的绘图
                emissions_joint[i][k][t][0].append(get_emissions(f,choice[0],choice[1],choice[2],choice[3],choice[4],choice[5],choice[6]))
                #print(emissions_joint[i][k][t][0][-1])

import numpy
#将数据按照便于存储的方式进行整理：
#3*7矩阵，列为食物种类，行为技术选择的种类，每个内部存入三者数值
#本来是打算为作箱式图准备所以采用了这种随机采样的形式，但由于后来不同种类肉类本身的差异性，遂放弃箱式图
#但由于偷懒最后保留了箱式图匹配matplotlib库的数据源
#毕竟也是最开始随机分布那张图的数据源
#如果只是画现在的图，可以省去随机采样步骤
drawing=[]

for i in range(0,3):
    a = []
    col = 0
    for j in range(0,7):
        b = []
        for list in emissions_joint[i][j]:
            line = 0
            b.append((list[1],numpy.average(list[0]),numpy.std(list[0])))
            sheet[i + 1].write(line, col, list[1])
            for data in list[0]:
                line += 1
                sheet[i + 1].write(line, col, data)
            col += 1
        a.append(b)
    drawing.append(a)

print(drawing)


label_subplots=["销售","二级运输","储存","一级运输","包装","能源","废弃物处理"]
label_food = ["Veg", "Fruit", "Meat"]
total = 0
for f in range(0,3):
    sheet[0].write(total, 0, label_food[f])
    for t in range(0,7):
        cow = 1
        sheet[0].write(total, cow, label_subplots[t])
        for l in range(0,len(drawing[f][t])):
            cow += 1
            sheet[0].write(total, cow, drawing[f][t][l][0])
            sheet[0].write(total, cow + 1, drawing[f][t][l][1])
            cow += 2
        total += 1
    total += 1
book.save("Condition distribution.xls")

for i in range(0,3):
    for list in drawing[i]:
        list.sort(key=lambda x:x[1])

import matplotlib.pyplot as plt
import brewer2mpl
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.rcParams['font.size']=9
fig,axs=plt.subplots(3,7,sharey="row",figsize=(15,9),dpi=300)

colors=["Reds","Oranges","YlOrRd","Greens","Blues","Purples","PuRd"]

#总之就是绘图，这部分应该。。。不是重点？
for i in range(0,3):
    lower = 50
    upper = -50
    for j in range(0,7):
        x=[]
        y=[]
        std=[]
        for item in drawing[i][j]:
            x.append(item[0])
            y.append(item[1])
            std.append(item[2])
            lower = min(lower, item[1])
            upper = max(upper, item[1])
        bmap = brewer2mpl.get_map(colors[j], 'sequential', len(x)+1)
        c=bmap.mpl_colors
        width_devide=8
        font_s = 9
        ha = "center"
        if len(x) == 2:
            axs[i,j].set_xlim(-0.5,1.5)
        elif j == 3:
            if i <= 1:
                width_devide = 12
                ha = "right"
            font_s = 7
        #print("{}: {}".format(x,y))
        axs[i,j].bar(x, y, align='center', color=c[-1*len(x):], width=len(x)/width_devide)
        axs[i,j].set_xticklabels(x, rotation=45,ha = ha, fontsize=font_s)
        for tick in axs[i,j].get_xticklabels():
            tick.set_rotation(45)
        axs[0,j].set_title(label_subplots[j])
        print("f:{} tech:{} high:{} low:{} percent:{}".format(i,label_subplots[j],y[-1],y[0],y[0]/y[-1]))
    axs[i,0].set_ylim(lower*0.95,upper*1.05)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0, hspace=0.5)

axs[0,0].set_ylabel("蔬菜单位碳排放(kgCO2e/kg)")
axs[1,0].set_ylabel("水果单位碳排放(kgCO2e/kg)")
axs[2,0].set_ylabel("肉类单位碳排放(kgCO2e/kg)")



plt.suptitle("技术环节中条件分布下单位质量食品碳排放",fontsize=15)
#plt.savefig("条件分布 柱状图(无标准差,再改版)")
plt.show()