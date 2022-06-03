#生成整个碳排放分布表格
import xlwt
book = xlwt.Workbook(encoding='utf-8', style_compression=0)


choice_veg=[
    ["常温","冷链"],
    ["常温","冷链","常温混动","冷链混动",],
    ["常温","冷链",],
    ["常温短途","冷链短途","常温新能源短途","冷链新能源短途","常温长途","冷链长途","常温混动长途","冷链混动长途",],
    ["无包装","塑料袋装","纸箱包装","塑料盒装"],
    ["火电","新能源"],
    ["填埋","厌氧消化","堆肥","焚烧"]
]

choice_meat=[
    ["常温","冷链"],
    ["常温","冷链","常温混动","冷链混动",],
    ["常温","冷链",],
    ["活畜短途","活畜新能源短途","活畜长途","活畜混动长途",],
    ["无包装","塑料袋装","纸箱包装","塑料盒装"],
    ["火电","新能源"],
    ["填埋","厌氧消化","堆肥","焚烧"]
]

consumption=[
    [122.7/(122.7+81.9),81.9/(122.7+81.9)],
    [3.9/27.3,3.1/27.3,15.3/27.3,5/27.3]
]


for item in consumption:
    for i in range(1,len(item)):
        item[i] += item[i - 1]
#(损耗率/能耗/时间/制冷剂泄漏/名称)
sell=[
    #蔬菜
    [(0.08625,0.0034/1000,0.625,0,"常温"),
    (0.08625/3,0.017/1000,0.625,0.00005644,'冷链')],
    #水果
    [(0.2*0.9,0.0034/1000,0.625,0,"常温"),
    (0.2*0.9/3,0.017/1000,0.625,0.00005644,"冷链")],
    #肉类(四种)
    [(0.013325,0.027/1000,0.625,0,"常温"),
    (0.013325/3,0.64/1000,0.625,0.00005644,"冷链")],
    [(0.013325,0.027/1000,0.625,0,"常温"),
    (0.013325/3,0.64/1000,0.625,0.00005644,"冷链")],
    [(0.013325,0.027/1000,0.625,0,"常温"),
    (0.013325/3,0.64/1000,0.625,0.00005644,"冷链")],
    [(0.013325,0.027/1000,0.625,0,"常温"),
    (0.013325/3,0.64/1000,0.625,0.00005644,"冷链")],
]


food = ["蔬菜","水果","牛肉","羊肉","猪肉","禽肉"]

trans2_dis = 30
veg_trans1_dis = 975.38
veg_trans1_dis_short = 232.37
fruit_trans1_dis = 1634.59
fruit_trans1_dis_short = 251.28
meat_trans1_dis = 972.42
meat_trans1_dis_short = 98.94

#(损耗率,碳排因子kgCO2e/kmkg, 距离)
#名称见trans2[f][j]的名称列表见choice[1]
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

#同sell
#种类见choice[2]
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

#同trans1
#种类见choice[3]或label
trans1=[
    #蔬菜
    [(0.17,0.0000519,veg_trans1_dis_short),
    (0.09,0.000186,veg_trans1_dis_short),
    (0.17,0.0000519*0.576,veg_trans1_dis_short),
    (0.09,0.000186*0.576,veg_trans1_dis_short),
    (0.17,0.0000519,veg_trans1_dis),
    (0.09,0.000186,veg_trans1_dis),
    (0.17,0.0000519*0.576,veg_trans1_dis),
    (0.09,0.000186*0.576,veg_trans1_dis),
    ],
    #水果
    [
    (0.20,0.0000519,fruit_trans1_dis_short),
    (0.10,0.000186,fruit_trans1_dis_short),
    (0.20,0.0000519*0.576,fruit_trans1_dis_short),
    (0.10,0.000186*0.576,fruit_trans1_dis_short),
    (0.20,0.0000519,fruit_trans1_dis),
    (0.10,0.000186,fruit_trans1_dis),
    (0.20,0.0000519*0.576,fruit_trans1_dis),
    (0.10,0.000186*0.576,fruit_trans1_dis)
    ],
    #肉类
    [(0.01,0.0000519,meat_trans1_dis_short),
    (0.01,0.0000519*0.576,meat_trans1_dis_short),
    (0.01,0.0000519,meat_trans1_dis),
    (0.01,0.0000519*0.576,meat_trans1_dis)
    ],
    [(0.01,0.0000519,meat_trans1_dis_short),
    (0.01,0.0000519*0.576,meat_trans1_dis_short),
    (0.01,0.0000519,meat_trans1_dis),
    (0.01,0.0000519*0.576,meat_trans1_dis)
    ],
    [(0.01,0.0000519,meat_trans1_dis_short),
    (0.01,0.0000519*0.576,meat_trans1_dis_short),
    (0.01,0.0000519,meat_trans1_dis),
    (0.01,0.0000519*0.576,meat_trans1_dis)
    ],
    [(0.01,0.0000519,meat_trans1_dis_short),
    (0.01,0.0000519*0.576,meat_trans1_dis_short),
    (0.01,0.0000519,meat_trans1_dis),
    (0.01,0.0000519*0.576,meat_trans1_dis)
    ],
]

#累积频率，随机采样用，本代码中不采用，主要画箱式图/分布图/概率等随机采样的时候需要用
percent_cum=[]


#数据来源：目压文献的图(JCP2015中国食品1979~2009)，什么吊文献居然只有图没有数据啊（半恼）
#能耗，施肥，车辆/农机，废弃物处理、肠胃发酵，粪便处理、包装生产、饲料生产、化肥生产、农膜生产、农药生产
#我们现在需要改什么？把produce的结构改一下以适应新模型
produce=[
    #蔬
    (0.2613*1.35/8.5,0.2613*1.5/8.3,0.2613*0.5/8.3,0,0,0,0,0,0,0.2613*5.4/11,0.2613*0.6/11,0.2613*0.9/11),
    #果
    (0.8931*1.25/6.5,0.8931*2/6.5,0.8931/13.8,0,0,0,0,0,0.8931*4/13.9,0,0.8931*2.5/13.9),
    #肉
    (21.71*(0.25/10.5),0,21.71*0.017,0,21.71*4.6/7.8,21.71*1/7.8,0,21.71*1.8/7.8,0,0,0),
    (20.82*0.3/9.9,0,20.82*0.055,0,20.82*0.728,20.82*0.151,0,20.82*0.063,0,0,0),
    (2.89*0.1,0,2.89*0.124,0,2.89*0.077,2.89*0.466,0,2.89*0.333,0,0,0),
    (11.37*0.1,0,11.37*0.124,0,11.37*0.077,11.37*0.466,0,11.37*0.333,0,0,0),
]

#每种技术单元的比例，第一层为6种食物，第二层为7个技术单元的选择（也许应该把长短途分开），最内层为每种的不同概率
percent=[
    #蔬菜
    [
        #售卖（常温/冷链）
        [0.58,0.42],
        #市内运输（常温/冷链）普通，及对应新能源
        [0.865*0.99, 0.135*0.99, 0.865*0.01,0.135*0.01],
        #存储常温/冷链
        [0.83,0.17],
        #省际：前四个短途，后四个长途；奇数为常温，偶数为冷链，每隔2个依次为常规、混动
        [0.865*0.99*0.28, 0.135*0.99*0.28, 0.865*0.01*0.28,0.135*0.01*0.28, 0.865*0.99*0.72, 0.135*0.99*0.72, 0.865*0.01*0.72,0.135*0.01*0.72],
        #无包装、塑料袋、纸盒、塑料盒（爬虫数据解决的具体比例）
        [1-0.68,0.68*175/(175+23+109),0.68*23/(175+23+109),0.68*109/(175+23+109),],
        #常温/新能源
        [0.818,1-0.818],
        #废弃物处理
        [0.25,0.125,0.125,0.5]
        #下同
    ],
    #水果
    [
        [0.83,0.17],
        [0.865*0.99, 0.135*0.99, 0.865*0.01, 0.135*0.01],
        [0.83,0.17],
        [0.865*0.99*0.14, 0.135*0.99*0.14, 0.865*0.01*0.14, 0.135*0.01*0.14,0.865*0.99*0.86, 0.135*0.99*0.86, 0.865*0.01*0.86, 0.135*0.01*0.,],
        [1-0.608,0.608*47/(147+85+47),0.608*85/(147+85+47),0.608*147/(147+85+47),],
        [0.818,0.155,0.019,0.008],
        [0.25,0.125,0.125,0.5]
    ],
    #肉类
    [
        [0.15,0.85],
        [0.58*0.99,0.99*0.42,0.58*0.01,0.42*0.01],
        [0.15,0.85],
        #肉类与前有区别的是省际运输，奇数常规偶数新能源，每2个一组分别长途/短途，其他与水果的模式相同
        [0.99*0.28,0.01*0.28,0.99*0.72,0.01*0.72,],
        [0.35,0.65*445/(445+9+309),0.65*9/(445+9+309),0.65*309/(445+9+309)],
        [0.818,1-0.818],
        [0.25,0.125,0.125,0.5]
    ],
    [
        [0.15,0.85],
        [0.58*0.99,0.99*0.42,0.58*0.01,0.42*0.01],
        [0.15,0.85],
        [0.99*0.28,0.01*0.28,0.99*0.72,0.01*0.72,],
        [0.35,0.65*445/(445+9+309),0.65*9/(445+9+309),0.65*309/(445+9+309)],
        [0.818,0.155,0.019,0.008],
        [0.25,0.125,0.125,0.5]
    ],
    [
        [0.15,0.85],
        [0.58*0.99,0.99*0.42,0.58*0.01,0.42*0.01],
        [0.15,0.85],
        [0.99*0.28,0.01*0.28,0.99*0.72,0.01*0.72,],
        [0.35,0.65*445/(445+9+309),0.65*9/(445+9+309),0.65*309/(445+9+309)],
        [0.818,1-0.818],
        [0.25,0.125,0.125,0.5]
    ],
    [
        [0.15,0.85],
        [0.58*0.99,0.99*0.42,0.58*0.01,0.42*0.01],
        [0.15,0.85],
        [0.99*0.28,0.01*0.28,0.99*0.72,0.01*0.72,],
        [0.35,0.65*445/(445+9+309),0.65*9/(445+9+309),0.65*309/(445+9+309)],
        [0.818,1-0.818],
        [0.25,0.125,0.125,0.5]
    ],
]


#使用已有数据直接生成percent_cum,避免自己算整错了啥
for f in range(0,6):
    final = []
    for i in range(0,len(percent[f])):
        data = 0
        tech = []
        for count in percent[f][i]:
            data += count
            tech.append(data)
        tech[-1] = 1
        final.append(tech)
        #print(tech)
    percent_cum.append(final)

#每种食物的消费量，1~6依次为蔬、果、四种肉
mass=[122.77,81.9,3.1,3.9,15.3,5]

energy=[1.28,0.00339]
energyname=["火电","新能源"]

disposal=[0.625*0.02582/0.466,-0.02754,0.165,0.02582]
disposal_name=["填埋","厌氧消化","堆肥","焚烧"]

#包装
package_emission=[
    #每个列表蔬菜、水果、肉类的四种食物
    #每个列表内分别为：无包装、塑料袋、纸箱、塑料盒（份）
    #在get_emissions 函数调用，直接加对应数值
    #蔬菜
    [0,3.71*8.21/500,0.449*7.1*34.5/1000,3.671*8.21/500],
    #水果
    [0,1.624*8.21/500,0.403*7.1*34.5/1000,2.632*8.21/500],
    #肉类
    [0,3.287*8.21/500,1.05*7.1*34.5/1000,4.3*8.21/500],
    [0,3.287*8.21/500,1.05*7.1*34.5/1000,4.3*8.21/500],
    [0,3.287*8.21/500,1.05*7.1*34.5/1000,4.3*8.21/500],
    [0,3.287*8.21/500,1.05*7.1*34.5/1000,4.3*8.21/500],
    ]


#计算生产的总碳排，因为这里不区分不同排放的来源所以直接使用加和的总数据
def production_emission(f,m,n):
    #f：Food m：mass
    e = 0
    e += produce[f][0]*m/energy[0]
    for t in range(1,len(produce[f])):
        e += m * produce[f][t]
    return e

def get_emissions(f,i,j,k,l,p,n,m):
    #f：Food i：售卖的对应编号 j：市内运输的技术编号 k：存储的技术编号 l：省际运输的编号， p：包装的编号 n：电力的编号 m：废弃物处理的编号
    #通过sell[f][i]/trans2[f][j]/store1[f][k]/trans1[f][l]/package_emission[f][p]/energy[n]/disposal[m]调用该编号的碳排放因子进行计算（具体技术对应参数见定义）
    #0.525为经过文献及实地调研对包装效果的预估值，结合JCP2021内线性模型以及保质期在包装前后变化的文献得出
    #具体的标签列表，表示技术选择
    if f <= 1:
        choice = choice_veg
    else:
        choice = choice_meat
    final_choice=[choice[0][i],choice[1][j],choice[2][k],choice[3][l],choice[4][p],choice[5][n],choice[6][m]]
    #最终输出结果
    result = []
    a = sell[f][i]
    b = trans2[f][j]
    c = store1[f][k]
    d = trans1[f][l]
    #乘出对应的比例
    percent_line = percent[f][0][i]*percent[f][1][j]*percent[f][2][k]*percent[f][3][l]*percent[f][4][p]*percent[f][5][n]*percent[f][6][m]
    #是否包装，定损耗率
    if p >= 1:
        packaged = 1
    else:
        packaged = 0
    #售卖/市内/存储/省际的损耗率
    lr1 = a[0]*(1-packaged*0.475)
    lr2 = b[0]*(1-packaged*0.475)
    lr3 = c[0]*(1-packaged*0.475)
    lr4 = d[0]*(1-packaged*0.475)
    #不同环节质量变化，用累积质量/（1-当前阶段损耗率）计算。标号与损耗率同阶段
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
    result.append(production_emission(f,1,n))
    total_e = 0#（计算总计碳排放）
    for data in result:
        total_e += data
    result.append(total_e)
    result.append(percent_line)
    i = 0
    #补上标签
    while i < len(final_choice):
        result.insert(i,final_choice[i])
        i += 1
    #最终返回一个列表：[7个标签，4(蔬果)/5(肉)*3分阶段碳排放,1kg生产碳排放，总计碳排放，所有链条汇总后的比例]
    return result

stage_data=[
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
    ]

def get_emissions_stage(f,i,j,k,l,p,n,m):
    if f <= 1:
        choice = choice_veg
    else:
        choice = choice_meat
    final_choice=[choice[0][i],choice[1][j],choice[2][k],choice[3][l],choice[4][p],choice[5][n],choice[6][m]]
    #最终输出结果
    result = []
    a = sell[f][i]
    b = trans2[f][j]
    c = store1[f][k]
    d = trans1[f][l]
    #乘出对应的比例
    percent_line = percent[f][0][i]*percent[f][1][j]*percent[f][2][k]*percent[f][3][l]*percent[f][4][p]*percent[f][5][n]*percent[f][6][m]
    #是否包装，定损耗率
    if p >= 1:
        packaged = 1
    else:
        packaged = 0
    #售卖/市内/存储/省际的损耗率
    lr1 = a[0]*(1-packaged*0.475)
    lr2 = b[0]*(1-packaged*0.475)
    lr3 = c[0]*(1-packaged*0.475)
    lr4 = d[0]*(1-packaged*0.475)
    #不同环节质量变化，用累积质量/（1-当前阶段损耗率）计算。标号与损耗率同阶段
    m1 = 1/(1 - lr1)
    #商店直接碳排
    stage_data[f][0]+=percent_line*(m1*a[1]*a[2]*energy[n]+m1*a[3]+production_emission(f,m1-1,n)+disposal[m]*(m1-1))
    #商店FLW及废弃物处理
    #包装
    result.append(package_emission[f][p])
    m2 = m1/(1 - lr2)
    #市内：直接/FLW/disposal
    stage_data[f][1]+=percent_line*( b[1]*b[2]*m2 + production_emission(f,m2-m1,n)+disposal[m]*(m2-m1))
    m3 = m2 / (1 - lr3)
    #存储：直接/FLW/disposal
    stage_data[f][2] += percent_line*(m3*c[1]*c[2]*energy[n]+production_emission(f,m3-m2,n)+disposal[m]*(m3-m2))
    if f >= 2:
        m3 = m3/0.9
        #加工：直接/FLW/disposal
        stage_data[f][3] +=percent_line * (m3 * 0.026 * energy[n]+ production_emission(f,m3*0.1,n)+ m3 * 0.1 * disposal[m])
    m4 = m3 / (1 - lr4)
    #省际：直接/FLW/disposal
    stage_data[f][4] += percent_line*(d[1] * d[2] * m4+production_emission(f,m4-m3,n)+disposal[m]*(m4-m3))
    #生产（1kg）
    stage_data[f][5] += package_emission[f][p]*percent_line

#表头
label_veg=[
        "售卖技术","市内运输技术","存储技术","省际运输技术","包装","发电技术","废弃物处理技术",
        "售卖 直接碳排","售卖 FLW","售卖 废弃物处理","包装",
        "市内运输 直接碳排","市内运输 FLW","市内运输，废弃物处理",
        "存储 直接碳排","存储 FLW","存储 废弃物处理",
        "省际 直接碳排","省际 FLW","省际 废弃物处理",
        "生产","总计","比例"
    ]

label_meat=[
        "售卖技术","市内运输技术","存储技术","省际运输技术","包装","发电技术","废弃物处理技术",
        "售卖 直接碳排","售卖 FLW","售卖 废弃物处理","包装",
        "市内运输 直接碳排","市内运输 FLW","市内运输，废弃物处理",
        "存储 直接碳排","存储 FLW","存储 废弃物处理",
        "加工 直接碳排","加工 FLW","加工 废弃物处理",
        "省际 直接碳排","省际 FLW","省际 废弃物处理",
        "生产","总计","比例"
]

sheet1 = book.add_sheet("不同环节占比")

for f in range(0,len(food)):
    #xlwt库定义表
    sheet = book.add_sheet(food[f], cell_overwrite_ok=True)
    #输出行/列数
    line = 0
    col = 0
    if f <= 1:
        label = label_veg
    else:
        label = label_meat
    for item in label:
        sheet.write(line, col, item)
        col += 1
    total_data=[]
    #计算所有表格后返回上述定义数据（定义见getemissions）
    for i in range(0,len(sell[f])):#2
        for j in range(0,len(trans2[f])):#4
            for k in range(0,len(store1[f])):#2
                for l in range(0,len(trans1[f])):#8（蔬果）/4（肉）
                    for p in range(0,len(choice_veg[4])):#4，通过最上面的名称定义
                        for m in range(0,len(disposal)):#4,四种废弃物处理
                            for n in range(0,len(energy)):#2
                                result_temp = get_emissions(f,i,j,k,l,p,n,m)
                                get_emissions_stage(f,i,j,k,l,p,n,m)
                                total_data.append(result_temp)
    total_data.sort(key=lambda x:x[-2])#每种食物所有数据依照总计碳排放（倒数第二个数据）
    #写入对应的数据
    for line_data in total_data:
        col = 0
        line += 1 
        for data in line_data:
            sheet.write(line, col, data)
            col += 1

for i in range(0,6):
    for j in range(0,6):
        sheet1.write(i+1,j+1,stage_data[i][j])

book.save("碳排放汇总ver3(修改屠宰碳排放).xls") 