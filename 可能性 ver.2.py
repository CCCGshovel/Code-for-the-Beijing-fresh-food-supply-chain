#通用碳排框架：第一版存储的数据，以引用的形式分别使用
from 通用碳排放框架 import choice_veg, choice_meat, sell, store1, trans2, trans1, produce, energy, disposal, energyname, disposal_name, package_emission
from 通用碳排放框架 import percent, per_cum, mass
from 通用碳排放框架 import food as fname

#计算生产的总碳排,因为这里不区分不同排放的来源所以直接使用加和的总数据
#输入：为初版计算时涉及到的f：食物种类；m：终端消费1kg的质量；n:能源种类
#但因为最后不考虑生产的能源排放所以这个借口其实废掉了
def production_emission(f,m,n):
    #f：Food m：mass
    e = 0
    e += produce[f][0]*m
    for t in range(1,len(produce[f])):
        e += m * produce[f][t]
    return e

#计算生产1kg食物的碳排放
#输入：各参数编码（详见通用框架抬头）
#输出1kg食物的总碳排，不涉及概率
def get_emissions(f,i,j,k,l,p,n,m):
    #f：Food i：售卖的对应编号 j：市内运输的技术编号 k：存储的技术编号 l：省际运输的编号, p：包装的编号 n：电力的编号 m：废弃物处理的编号
    #通过sell[f][i]/trans2[f][j]/store1[f][k]/trans1[f][l]/package_emission[f][p]/energy[n]/disposal[m]调用该编号的碳排放因子进行计算（具体技术对应参数见定义）
    #0.525为经过文献及实地调研对包装效果的预估值,结合JCP2021内线性模型以及保质期在包装前后变化的文献得出
    #具体的标签列表,表示技术选择
    #final_choice=[choice[0][i],choice[1][j],choice[2][k],choice[3][l],choice[4][p],choice[5][n],choice[6][m]]
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
    i = 0
    #补上标签
    # 有部分冗余代码，毕竟是当时赶时间写的，最初是作为列表形式输出给每种flw、直接碳排、废弃物处理三个部门。现在已不需要
    return total_e

#将基础频率转化为累积频率，详细定义见通用框架
percent_cum = per_cum(percent)

#引入随机采样包，计算绘图数据
import random
#初始化possibility列表，用于存储数据
#其格式为6*7的矩阵，矩阵每一元记录另一个列表，列表值为[大于原始分布的概率,技术名称]
#事物顺序见通用food列表，label顺序见通用choice列表
posibility=[]
for f in range(0, 6):
    test = []
    #label：由于涉及带着排序，因此
    if f <= 1:
        label = choice_veg
    else:
        label = choice_meat
    for i in range(0, 7):
        for j in range(0,len(percent_cum[f][i])):
            test.append([0, label[i][j]])
    posibility.append(test)

#随机采样：依次遍历6种f，test_time次采样
test_time=2000
result = []
for f in range(0,6):
    for j in range(0,test_time):
        if j%2000 == 0:
            print("f:{} j:{}".format(f,j))
        final_choice = []
        for k in range(0,7):
            decide=random.random()
            for l in range(0,len(percent_cum[f][k])):
                if decide <= percent_cum[f][k][l]:
                    final_choice.append(l)
                    break
        #随机采样得到初始分布的技术选择，并作为一次比较的基准值（对应的技术见通用choice列表）
        e_init=get_emissions(f,final_choice[0],final_choice[1],final_choice[2],final_choice[3],final_choice[4],final_choice[5],final_choice[6])
        try_zoom = 0
        #遍历之前生成的6*7矩阵，将基础选择中的一个参数改为指定技术（见choice），每组进行比较，比较后对列表中的每一个概率值进行累加
        for i in range(0, len(final_choice)):
            for t in range(0, len(percent_cum[f][i])):
                choice = []
                for k in range(0,7):
                    decide = random.random()
                    for l in range(0,len(percent_cum[f][k])):
                        if decide <= percent_cum[f][k][l]:
                            choice.append(l)
                            break
                choice[i] = t
                e_test = get_emissions(f,choice[0],choice[1],choice[2],choice[3],choice[4],choice[5],choice[6],)
                if e_test >= e_init:
                    posibility[f][try_zoom][0] += 1 / test_time
                try_zoom += 1


import matplotlib.pyplot as plt
import numpy

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.rcParams['font.size']=9

#排序，便于绘图
for f in range(0,len(posibility)):
    posibility[f].sort(key=lambda x:x[0])
    print(posibility[f])


fig, axs = plt.subplots(3, 2, sharey = True, figsize=(10,6))
#此处i指代f，即食物种类
#理论上我应该继续用f，前后统一
for i in range(0,6):
    #x轴列表
    if i <= 1:
        label = choice_veg
    else:
        label = choice_meat
    total = 0
    #back为底板，统一数值为1
    #在我们possibility列表中输出参数覆盖在back图层后，剩余部分即可表示条件分布小于初始分布的概率
    back = []
    for j in range(0,len(label)):
        for k in range(0,len(label[j])):
            back.append(1)
    #x、y为最终绘图的k值及y值
    x=[]
    y=[]
    #由于我们需要访问排序后的x及y，因此最初以这种行事定义数据格式
    for item in posibility[i]:
        x.append(item[1])
        y.append(item[0])
    total+=1
    #分别绘制back及y的数据，以达成累积分布图的效果
    axs[int(i/2),i%2].bar(x,back,color="lightsteelblue")
    axs[int(i/2),i%2].bar(x,y,color="lightsalmon")
    axs[int(i/2),i%2].set_xticklabels(x,rotation=45)
    axs[int(i/2),i%2].set_title(fname[i])
    axs[int(i/2),i%2].set_xticklabels(x, rotation=45,ha = "right",fontsize = 7)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0, hspace=0.7)
plt.suptitle("不同条件分布与原分布概率比较",fontsize=15)

axs[0,0].set_ylabel("大于初始分布的概率")
axs[1,0].set_ylabel("大于初始分布的概率")
axs[2,0].set_ylabel("大于初始分布的概率")
plt.savefig("概率 与原始分布比较.png")
plt.show()
#plt.show()
