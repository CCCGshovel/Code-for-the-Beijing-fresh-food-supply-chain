#基于链条来进行分析
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

package_emission=[0.116,0.084,0.169,0.169,0.169,0.169]

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
    return [e1, e2-e1, e3-e2, e4-e3, e5-e4, e6-e5, e7-e6, e8-e7]

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
    return [e1, e2-e1, e3-e2, e4-e3, e5-e4, e6-e5, e7-e6, e8-e7]

def emission(food,a0,a1,a2,a3,b0,b1,b2,c0,c1,c2,c3,proce,proce_loss,d0,d1,d2,d3,package,en,dis,pack):
    if food <2 :
        return get_emission(a0,a1,a2,a3,b0,b1,b2,c0,c1,c2,c3,d0,d1,d2,d3,package,en,dis,pack)
    else: 
        return get_emission_meat(a0,a1,a2,a3,b0,b1,b2,c0,c1,c2,c3,proce,proce_loss,d0,d1,d2,d3,package,en,dis,pack)

data=[]
for f in range(0,6):
    data_food = []
    total=0
    for i in range(0,len(percent[f][0])):
        a = sell[f][i]
        for j in range(0,len(percent[f][1])):
            b = trans2[f][j]
            for k in range(0,len(percent[f][2])):
                c = store1[f][k]
                for l in range(0,len(percent[f][3])):
                    d = trans1[f][l]
                    for m in range(0,len(disposal)):
                        for n in range(0,len(energy)):
                            for p in range(0,2):
                                data_unit = emission(f,a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],p,energy[n],disposal[m],package_emission[f])
                                choice = [i,j,k,l,p,n,m]
                                percent_line = 1
                                for t in range(0,len(choice)):
                                    percent_line *= percent[f][t][choice[t]]
                                    #print("{}{}{}{}{}{}{}:{},{}".format(i,j,k,l,p,n,m,t,percent[i][t][choice[t]]))
                                    data_unit.append(choice[t])
                                data_unit.append(percent_line)
                                print(data_unit)
                                data_food.append(data_unit)
    data.append(data_food)
#每个数据单元存储：（售卖，包装，运输2，存储，加工，运输1，生产，废弃物处理，售卖技术，运输2技术，存储技术，运输1技术，包装否，能源，废弃物处理）
labels=["售卖","包装","运输2","存储","加工",'运输1','生产','废弃物处理']
x=[]
y=[]

for data_food in data:
    data_food.sort(key = lambda x:x[7])
    temp_x=[]
    temp_y=[] 
    for i in range(1,len(data_food)):
        data_food[i][-1] += data_food[i-1][-1]
        temp_x.append(data_food[i-1][-1])
    for i in range(0,15):
        t_y=[]
        for j in range(1,len(data_food)):
            t_y.append(data_food[j][i])
        temp_y.append(t_y)
    x.append(temp_x)
    y.append(temp_y)

import xlwt

labels_output=[
    "累积频率",
    "销售 累积碳排",
    "包装 累积碳排",
    "市内运输 累积碳排",
    "存储 累积碳排",
    "省际运输 累积碳排",
    "加工 累积碳排",
    "生产 累积碳排",
    "废弃物处理 累积碳排",
]

book=xlwt.Workbook(encoding='utf-8', style_compression=0)
for i in range(0,len(x)):
    sheet=book.add_sheet('{}'.format(food[i]), cell_overwrite_ok=True)
    for j in range(0,len(labels_output)):
        sheet.write(0,j,labels_output[j])
    for k in range(0,len(x[i])):
        sheet.write(k+1,0,x[i][k])
        for j in range(0,len(y[i])):
            sheet.write(k+1,j+1,y[i][j][k])
book.save("累积碳排放.xls")

import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.rcParams['font.size']=9
fig,axs=plt.subplots(3,2,sharey="row",sharex=True,figsize=(15,15))
for i in range(0,len(x)):
    axs[int(i/2),i%2].fill_between(x[i],y[i][0],step="pre",label=labels[0])  # type: ignore
    for j in range(1,8):
        axs[int(i/2),i%2].fill_between(x[i],y[i][j],y[i][j-1],step="pre",label=labels[j])
    plt.rcParams['font.size']=9
    axs[int(i/2),i%2].set_title(food[i])
    plt.rcParams['font.size']=6
    axs[int(i/2),i%2].legend(loc="upper left")
plt.savefig("Lines.png")
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0, hspace=0.2)
plt.show()