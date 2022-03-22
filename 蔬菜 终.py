#目的：构建一个计算框架，并把所有的数据标准化，把所有单元存下来
#最终我们可以直接调用不同单元对应的节点，再直接算出来数据
#但最好这个位置可以留一个直接把比例接进来的接口
#实际上我们每个单位所需要访问的只有两个数据，一个是碳排放，一个是损耗率

from turtle import width
import xlwt
import matplotlib.pyplot as plt

#横向，不同包装(有，无)
#纵向，不同温度（常温、冷藏）
#(损耗率（%），单位时间能耗（kWh/k(g*d)），时长（d）,包装碳排放+制冷剂碳排放（kgCO2e/kg）)
sell_veg = [
    (0.08625,0,0.625,0),
    (0.08625/3,0.0003,0.625,0.00005644),
]

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
package_percent=0.68
package_emission=0.116

book=xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet=book.add_sheet('lines', cell_overwrite_ok=True)
sheet_sensitive = book.add_sheet("sensitive", cell_overwrite_ok = True)
sheet_simple=book.add_sheet("simple", cell_overwrite_ok=True)



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




def caculateall():
    emission = 0
    emission_down=[]
    result=[]
    for i in range(0,18):
        emission_down.append(0)
    for m in range(0,len(disposal)):
        for n in range(0,len(energy)):
            i=0
            for a in sell_veg:
                j=0
                for b in trans2_veg:
                    k=0
                    for c in store1_veg:
                        l=0
                        for d in trans1_veg:
                            emission += sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*energy_percent[n]*disposal_percent[m]*((1-package_percent)*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)+package_percent*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission))
                            l+=1
                        k+=1
                    j+=1
                i+=1
    return emission    

#绘图1 以1/3为区分的累积分布（已弃用）
emissions=[]
for m in range(0,len(disposal)):
        for n in range(0,len(energy)):
            i=0
            for a in sell_veg:
                j=0
                for b in trans2_veg:
                    k=0
                    for c in store1_veg:
                        l=0
                        for d in trans1_veg:
                            e1=get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)
                            e2=get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission)
                            emissions.append((e1,package_percent*sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*energy_percent[n]*disposal_percent[m],0))
                            emissions.append((e2,(1-package_percent)*sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*energy_percent[n]*disposal_percent[m],1))
                            l+=1
                        k+=1
                    j+=1
                i+=1
e=caculateall()
emissions.sort(key=lambda x:x[0])
x1=[]
y1=[]
x2=[]
y2=[]
x3=[]
y3=[]

list1_x=[]
list1_y=[]
list2_x=[]
list2_y=[]
cum=0
percent=0

for i in range(0,len(emissions)):
    cum+=emissions[i][1]*emissions[i][0]/e
    percent+=emissions[i][1]
    if cum<=1/3:
        x1.append(percent)
        y1.append(emissions[i][0])
    elif cum<=2/3:
        x2.append(percent)
        y2.append(emissions[i][0])
    else:
        x3.append(percent)
        y3.append(emissions[i][0])
    
x2.insert(0,x1[-1])
y2.insert(0,y1[-1])
x3.insert(0,x2[-1])
y3.insert(0,y2[-1])    
fig, ax1=plt.subplots()
ax1.fill_between(x1,y1,alpha=0.2,step="pre",color="green")
ax1.fill_between(x2,y2,alpha=0.5,step="pre",color="green")
ax1.fill_between(x3,y3,alpha=0.8,step="pre",color="green")
ax1.set_ylabel('emission:kgCO2e/kg')
ax1.set_title("Vegetable cumulative emission")
#plt.show()


#绘图2 绘制以不同阶段抉择为区分的累积分布图
fig, ax1=plt.subplots()
for i in range(0,len(list1_x)):
    ax1.fill_between(list1_x[i],list1_y[i],alpha=0.2,step="pre",color="green")

for i in range(0,len(list2_x)):
    ax1.fill_between(list2_x[i],list2_y[i],alpha=0.2,step="pre",color="red")
#plt.show()

from numpy import log10

#绘图3 计算敏感性，该函数计算降低百分之十对应参数后整体的变化率
def caculateall1():
    emission = 0
    emission_down=[]
    result=[]
    for i in range(0,18):
        emission_down.append(0)
    for m in range(0,len(disposal)):
        for n in range(0,len(energy)):
            i=0
            for a in sell_veg:
                j=0
                for b in trans2_veg:
                    k=0
                    for c in store1_veg:
                        l=0
                        for d in trans1_veg:
                            emission += sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*energy_percent[n]*disposal_percent[m]*((1-package_percent)*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)+package_percent*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission))
                            emission_down[0] += sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*energy_percent[n]*disposal_percent[m]*((1-package_percent)*get_emission(0.9*a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)+package_percent*get_emission(0.9*a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission))
                            emission_down[1] += sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*energy_percent[n]*disposal_percent[m]*((1-package_percent)*get_emission(a[0],0.9*a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)+package_percent*get_emission(a[0],0.9*a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission))
                            emission_down[2] += sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*energy_percent[n]*disposal_percent[m]*((1-package_percent)*get_emission(a[0],a[1],0.9*a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)+package_percent*get_emission(a[0],a[1],0.9*a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission))
                            emission_down[3] += sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*energy_percent[n]*disposal_percent[m]*((1-package_percent)*get_emission(a[0],a[1],a[2],0.9*a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)+package_percent*get_emission(a[0],a[1],a[2],0.9*a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission))
                            emission_down[4] += sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*energy_percent[n]*disposal_percent[m]*((1-package_percent)*get_emission(a[0],a[1],a[2],a[3],0.9*b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)+package_percent*get_emission(a[0],a[1],a[2],a[3],0.9*b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission))
                            emission_down[5] += sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*energy_percent[n]*disposal_percent[m]*((1-package_percent)*get_emission(a[0],a[1],a[2],a[3],b[0],0.9*b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)+package_percent*get_emission(a[0],a[1],a[2],a[3],b[0],0.9*b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission))
                            emission_down[6] += sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*energy_percent[n]*disposal_percent[m]*((1-package_percent)*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],0.9*b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)+package_percent*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],0.9*b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission))
                            emission_down[7] += sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*energy_percent[n]*disposal_percent[m]*((1-package_percent)*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],0.9*c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)+package_percent*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],0.9*c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission))
                            emission_down[8] += sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*energy_percent[n]*disposal_percent[m]*((1-package_percent)*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],0.9*c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)+package_percent*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],0.9*c[1],c[2],c[3],d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission))
                            emission_down[9] += sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*energy_percent[n]*disposal_percent[m]*((1-package_percent)*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],0.9*c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)+package_percent*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],0.9*c[2],c[3],d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission))
                            emission_down[10] += sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*energy_percent[n]*disposal_percent[m]*((1-package_percent)*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],0.9*c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)+package_percent*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],0.9*c[3],d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission))
                            emission_down[11] += sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*energy_percent[n]*disposal_percent[m]*((1-package_percent)*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],0.9*d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)+package_percent*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],0.9*d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission))
                            emission_down[12] += sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*energy_percent[n]*disposal_percent[m]*((1-package_percent)*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],0.9*d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)+package_percent*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],0.9*d[1],d[2],d[3],1,energy[n],disposal[m],package_emission))
                            emission_down[13] += sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*energy_percent[n]*disposal_percent[m]*((1-package_percent)*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],0.9*d[2],d[3],0,energy[n],disposal[m],package_emission)+package_percent*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],0.9*d[2],d[3],1,energy[n],disposal[m],package_emission))
                            emission_down[14] += sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*energy_percent[n]*disposal_percent[m]*((1-package_percent)*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],0.9*d[3],0,energy[n],disposal[m],package_emission)+package_percent*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],0.9*d[3],1,energy[n],disposal[m],package_emission))
                            emission_down[15] += sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*energy_percent[n]*disposal_percent[m]*((1-package_percent)*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,0.9*energy[n],disposal[m],package_emission)+package_percent*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],1,0.9*energy[n],disposal[m],package_emission))
                            emission_down[16] += sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*energy_percent[n]*disposal_percent[m]*((1-package_percent)*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],0.9*disposal[m],package_emission)+package_percent*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],1,energy[n],0.9*disposal[m],package_emission))
                            emission_down[17] += sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*energy_percent[n]*disposal_percent[m]*((1-package_percent)*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.9*package_emission)+package_percent*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.9*package_emission))
                            l+=1
                        k+=1
                    j+=1
                i+=1
    for i in range(0,len(emission_down)):
        result.append(1-emission_down[i]/emission)
    print(result)
    return result    

data=[]
data1=[]
data2=[]
data3=[]
resulttttt=caculateall1()
for i in range(0,len(resulttttt)):
    data.append(log10(resulttttt[i]))

labels=["S2_lr","S2_t","S2_r","S2_e","T2_lr","T2_r","T2_m","S1_lr","S1_t","S1_r","S1_e","T1_lr","T1_r","T1_m","Produce","En_r","Dis_r","Pack_r"]

sorted=[]
for i in range(0,len(labels)):
    sorted.append((labels[i],data[i]))
sorted.sort(key=lambda x:x[1],reverse=True)

m_l=[]
for i in range(0,len(labels)):
    if sorted[i][1]>-2:
        data1.append(sorted[i][1])
        data2.append(0)
        data3.append(0)
    elif sorted[i][1]>-3:
        data1.append(0)
        data2.append(sorted[i][1])
        data3.append(0)
    else:
        data1.append(0)
        data2.append(0)
        data3.append(sorted[i][1])
    m_l.append(sorted[i][0])

print(m_l)
print(data1)

fig, ax = plt.subplots()
ax.bar(m_l, data3 , width=0.3,color="blue",label="Emission Reduction>0.01")
ax.bar(m_l, data2 , width=0.3,color="orange",label="Emission Reduction<=0.01,>0.001")
ax.bar(m_l, data1 , width=0.3,color="red",label="Emission Reduction<0.001")
ax.set_ylabel('lg(1-E_down/E_initial)')
ax.set_xlabel("Parameters")
ax.set_title('Sensitivity of Vegetable')

ax.legend()
plt.show()


#绘图4 区分链条上某环节不同决策下碳排放的贡献
emissions=[]
for m in range(0,len(disposal)):
        for n in range(0,len(energy)):
            i=0
            for a in sell_veg:
                j=0
                for b in trans2_veg:
                    k=0
                    for c in store1_veg:
                        l=0
                        for d in trans1_veg:
                            e1=get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)
                            e2=get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission)
                            #emissions里存储一个元组（排放，占比，对应目标的比例(如0,1位为是否包装，l%2为运输1是否冷链，以此类推)）
                            emissions.append((e1,package_percent*sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*energy_percent[n]*disposal_percent[m],0))
                            emissions.append((e2,(1-package_percent)*sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*energy_percent[n]*disposal_percent[m],1))
                            l+=1
                        k+=1
                    j+=1
                i+=1

e=caculateall()
emissions.sort(key=lambda x:x[0])

list1_x=[]
list1_y=[]
list2_x=[]
list2_y=[]

x_temp=[]
y_temp=[]

import copy

percent=0
for i in range(0,len(emissions)):
    percent+=emissions[i][1]
    x_temp.append(percent)
    y_temp.append(emissions[i][0])
    if i<len(emissions)-1:
        if emissions[i][2] != emissions[i+1][2]:
            x_t = copy.deepcopy(x_temp)
            y_t = copy.deepcopy(y_temp)
            x_t.append(emissions[i+1][1]+percent)
            y_t.append(emissions[i+1][0])
            if emissions[i+1][2]==0:
                list1_x.append(x_t)
                list1_y.append(y_t)
            else:
                list2_x.append(x_t)
                list2_y.append(y_t)
            x_temp.clear()
            y_temp.clear()

import matplotlib.pyplot as plt


percent=0

fig, ax1=plt.subplots()
for i in range(0,len(list1_x)):
    ax1.fill_between(list1_y[i],list1_x[i],alpha=0.5,step="pre",color="grey",linewidth=0)
for i in range(0,len(list2_x)):
    ax1.fill_between(list2_y[i],list2_x[i],alpha=0.5,step="pre",color="red",linewidth=0)

ax1.legend(["Not Packed","Packed"],loc="upper left")
ax1.set_title("Packaging cold chain influencing veg")
ax1.set_xlabel("Percent of consumption")
ax1.set_ylabel("Carbon Emission(kgCO2e/kg)")
plt.show()


#绘图5 绘制该种食物不同链条碳排放的大小
emissions_lines=[]
all=0
i=0
for a in sell_veg:
    j=0
    for b in trans2_veg:
        k=0
        for c in store1_veg:
            l=0
            for d in trans1_veg:
                emission=0
                emissionp=0
                for n in range(0,len(energy)):
                    for m in range(0,len(disposal)):
                        emission += sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*energy_percent[n]*disposal_percent[m]*(1-package_percent)* get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)
                        emissionp += sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*energy_percent[n]*disposal_percent[m]*package_percent* get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission)
                sheet_simple.write(2*all,0,"无包装")
                sheet_simple.write(2*all,1,name[0][i])
                sheet_simple.write(2*all,2,name[1][j])
                sheet_simple.write(2*all,3,name[2][k])
                sheet_simple.write(2*all,4,name[3][l])
                sheet_simple.write(2*all,5,emission)
                sheet_simple.write(2*all+1,0,"包装")
                sheet_simple.write(2*all+1,1,name[0][i])
                sheet_simple.write(2*all+1,2,name[1][j])
                sheet_simple.write(2*all+1,3,name[2][k])
                sheet_simple.write(2*all+1,4,name[3][l])
                sheet_simple.write(2*all+1,5,emissionp)
                emissions_lines.append((emission*sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*(1-package_percent),i%2,j%2,k%2,l%2,0))
                emissions_lines.append((emissionp*sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*package_percent,i%2,j%2,k%2,l%2,1))
                all+=1
                l+=1
            k+=1
        j+=1
    i+=1

label_emission=[]
emissions_fin=[]
emissions_lines.sort(key=lambda x:x[0])

for item in emissions_lines:
    label_emission.append("{}\n{}\n{}\n{}\n{}".format(item[1],item[2],item[3],item[4],item[5]))
    emissions_fin.append(item[0])

fig , ax_emission = plt.subplots()

ax_emission.bar(label_emission,emissions_fin,width=0.3)
ax_emission.set_title("Carbon Emissions for lines")
ax_emission.set_ylabel("kgCO2e/kg food consumption")

#绘图6 绘制不同链条损耗率的对应比例
fig , ax_lr = plt.subplots(2,1,sharex=True)

emissions=[]
loss_rate=[]
loss_amount=[]

for i in range(0,2):
    for j in range(0,2):
        for k in range(0,2):
            for l in range(0,2):
                lr1 = sell_veg[i][0]
                lr2 = 1-(1-lr1)*(1-trans1_veg[j][0])
                lr3 = 1-(1-lr2)*(1-store1_veg[k][0])
                lr4 = 1-(1-lr3)*(1-trans1_veg[l][0])
                lrp1 = sell_veg[i][0]*0.525
                lrp2 = 1-(1-lrp1)*(1-trans2_veg[j][0]*0.525)
                lrp3 = 1-(1-lrp2)*(1-store1_veg[k][0]*0.525)
                lrp4 = 1-(1-lrp3)*(1-trans1_veg[l][0]*0.525)
                loss_rate.append((lr1,lr2,lr3,lr4,i%2,j%2,k%2,l%2,0,(1/(1-lr4)-1)*sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*(1-package_percent)))
                loss_rate.append((lrp1,lrp2,lrp3,lrp4,i%2,j%2,k%2,l%2,1,(1/(1-lrp4)-1)*sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*package_percent))

label_lr=[]
lr_data=[[],[],[],[]]
lr_data_name=["Sell","Trans2","Store","Trans1"]
loss_rate.sort(key = lambda x : x[3])

for item in loss_rate:
    #暂时没想到太好的表示链条的方法，先暂时用01表示是否采用冷链/包装等决策
    label_lr.append("{}\n{}\n{}\n{}\n{}".format(item[4],item[5],item[6],item[7],item[8]))
    for i in range(0,4):
        lr_data[i].append(item[i])
    loss_amount.append(item[-1])


for i in range(0,len(lr_data)):
    ax_lr[0].bar(label_lr, lr_data[3-i], width=0.3, label=lr_data_name[3-i])
ax_lr[1].bar(label_lr,loss_amount, width=0.3)
ax_lr[0].set_title("Vegetable Loss rate")
ax_lr[1].set_title("Vegetable Loss amount")
ax_lr[0].set_ylabel("%")
ax_lr[1].set_ylabel("kg food loss / kg food consumed in society")
ax_lr[0].legend()
plt.show()
 
#计算每条链条的灵敏性，已弃用
"""
def sensitive(a,b,c,d,m,n,total):
    e_basic = get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)
    sheet_sensitive.write(2*total,0,"无包装")
    sheet_sensitive.write(2*total,1,name[0][i])
    sheet_sensitive.write(2*total,2,name[1][j])
    sheet_sensitive.write(2*total,3,name[2][k])
    sheet_sensitive.write(2*total,4,name[3][l])
    sheet_sensitive.write(2*total,5,energyname[n])
    sheet_sensitive.write(2*total,6,disposal_name[m])
    sheet_sensitive.write(2*total, 7, 1-get_emission(0.9*a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total, 8, 1-get_emission(a[0],0.9*a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total, 9, 1-get_emission(a[0],a[1],0.9*a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total, 10, 1-get_emission(a[0],a[1],a[2],0.9*a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total, 11, 1-get_emission(a[0],a[1],a[2],a[3],0.9*b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total, 12, 1-get_emission(a[0],a[1],a[2],a[3],b[0],0.9*b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total, 13, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],0.9*b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total, 14, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],0.9*c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total, 15, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],0.9*c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total, 16, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],0.9*c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total, 17, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],0.9*c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total, 18, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],0.9*d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total, 19, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],0.9*d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total, 20, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],0.9*d[2],d[3],0,energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total, 21, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],0.9*d[3],0,energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total, 22, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,0.9*energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total, 23, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],0.9*disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total, 24, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.9*package_emission)/e_basic)
    e_basic = get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission)
    sheet_sensitive.write(2*total+1,0,"包装")
    sheet_sensitive.write(2*total+1,1,name[0][i])
    sheet_sensitive.write(2*total+1,2,name[1][j])
    sheet_sensitive.write(2*total+1,3,name[2][k])
    sheet_sensitive.write(2*total+1,4,name[3][l])
    sheet_sensitive.write(2*total+1,5,energyname[n])
    sheet_sensitive.write(2*total+1,6,disposal_name[m])
    sheet_sensitive.write(2*total+1, 7, 1-get_emission(0.9*a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total+1, 8, 1-get_emission(a[0],0.9*a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total+1, 9, 1-get_emission(a[0],a[1],0.9*a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total+1, 10, 1-get_emission(a[0],a[1],a[2],0.9*a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total+1, 11, 1-get_emission(a[0],a[1],a[2],a[3],0.9*b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total+1, 12, 1-get_emission(a[0],a[1],a[2],a[3],b[0],0.9*b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total+1, 13, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],0.9*b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total+1, 14, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],0.9*c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total+1, 15, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],0.9*c[1],c[2],c[3],d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total+1, 16, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],0.9*c[2],c[3],d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total+1, 17, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],0.9*c[3],d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total+1, 18, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],0.9*d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total+1, 19, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],0.9*d[1],d[2],d[3],1,energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total+1, 20, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],0.9*d[2],d[3],1,energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total+1, 21, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],0.9*d[3],1,energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total+1, 22, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],1,0.9*energy[n],disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total+1, 23, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],1,energy[n],0.9*disposal[m],package_emission)/e_basic)
    sheet_sensitive.write(2*total+1, 24, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission*0.9)/e_basic)    
"""

#输出每条链对一个的碳排放及损耗率
#输出顺序：前五行为对应的决策，后续依次为：售卖、市内运输、存储、省际运输的累积损耗率；各个阶段分别的碳排放；废弃物处理的方式及碳排放；比例，对应结果；

sheet.write(0,0,"Packaging")
sheet.write(0,1,"Sell")
sheet.write(0,2,"Trans2")
sheet.write(0,3,"Store")
sheet.write(0,4,"Trans1")
sheet.write(0,6,"Sell_lr")
sheet.write(0,7,"Trans2_lr")
sheet.write(0,8,"Store_lr")
sheet.write(0,9,"Trans1_lr")
sheet.write(0,10,"Sell_e")
sheet.write(0,11,"Trans2_e")
sheet.write(0,5,"Energy")
sheet.write(0,12,"Store_e")
sheet.write(0,13,"Trans2_e")
sheet.write(0,14,"Produce_e")
sheet.write(0,15,"Package_e")
sheet.write(0,16,"Disposal")
sheet.write(0,17,"Disposal_e")
sheet.write(0,18,"Percent")
sheet.write(0,19,"Final Emission")

total=1
for m in range(0,len(disposal)):
    for n in range(0,len(energy)):
        i=0
        for a in sell_veg:
            loss_r1 = a[0]
            lossp_r1 = a[0]*0.525
            emission_r1 = 1 / (1-loss_r1) * (a[1]*a[2]*energy[n] + a[3])
            emissionp_r1 = 1 / (1-lossp_r1) * (a[1]*a[2]*energy[n] + a[3])
            j=0
            for b in trans2_veg:
                loss_r2 = 1 - (1 - loss_r1)*(1 - b[0])
                emission_r2 = emission_r1 + 1/(1-loss_r2)*b[1]*b[2]
                lossp_r2 = 1 - (1 - lossp_r1) * (1 - b[0]*0.525)
                emissionp_r2 = emissionp_r1 + 1/(1-lossp_r2)*b[1]*b[2]
                k=0
                for c in store1_veg:
                    loss_r3 = 1 - (1 - loss_r2) * (1 - c[0])
                    emission_r3 = emission_r2 + 1/(1-loss_r3)*(c[1]*c[2]*energy[n] + c[3])
                    lossp_r3 = 1 - (1 - lossp_r2) * (1 - c[0]*0.525) 
                    emissionp_r3 = emissionp_r2 + 1/(1-lossp_r3)*(c[1]*c[2]*energy[n] + c[3])
                    l=0
                    for d in trans1_veg:
                        loss_r4 = 1 - (1 - loss_r3) * (1 - d[0])
                        emission_r4 = emission_r3 + 1/(1-loss_r4)*(d[1]*d[2])
                        lossp_r4 =1 - (1 - lossp_r3) * (1 - d[0]*0.525)
                        emissionp_r4 = emissionp_r3 + 1/(1-lossp_r4)*(d[1]*d[2])
                        emission_r5 = emission_r4 + d[3]*1/(1-loss_r4)
                        emissionp_r5 = emissionp_r4 + d[3]*1/(1-lossp_r4)
                        emission_r6 = emission_r5 + 0
                        emissionp_r6 = emissionp_r5 + package_emission
                        #print("emission:{}".format(emission_r4))
                        #print("loss_r:{}".format(loss_r4))
                        sheet.write(2*total,0,"无包装")
                        sheet.write(2*total,1,name[0][i])
                        sheet.write(2*total,2,name[1][j])
                        sheet.write(2*total,3,name[2][k])
                        sheet.write(2*total,4,name[3][l])
                        sheet.write(2*total,5,energyname[n])
                        sheet.write(2*total,6,loss_r1)
                        sheet.write(2*total,7,loss_r2)
                        sheet.write(2*total,8,loss_r3)
                        sheet.write(2*total,9,loss_r4)
                        sheet.write(2*total,10,emission_r1)
                        sheet.write(2*total,11,emission_r2-emission_r1)
                        sheet.write(2*total,12,emission_r3-emission_r2)
                        sheet.write(2*total,13,emission_r4-emission_r3)
                        sheet.write(2*total,14,emission_r5-emission_r4)
                        sheet.write(2*total,15,emission_r6-emission_r5)
                        sheet.write(2*total,16,disposal_name[m])
                        sheet.write(2*total,17,disposal[m]*loss_r4)
                        sheet.write(2*total,18,sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*energy_percent[n]*disposal_percent[m]*package_percent)
                        sheet.write(2*total,19,emission_r6)
                        sheet.write(2*total+1,0,"包装")
                        sheet.write(2*total+1,1,name[0][i])
                        sheet.write(2*total+1,2,name[1][j])
                        sheet.write(2*total+1,3,name[2][k])
                        sheet.write(2*total+1,4,name[3][l])
                        sheet.write(2*total+1,5,energyname[n])
                        sheet.write(2*total+1,6,lossp_r1)
                        sheet.write(2*total+1,7,lossp_r2)
                        sheet.write(2*total+1,8,lossp_r3)
                        sheet.write(2*total+1,9,lossp_r4)
                        sheet.write(2*total+1,10,emissionp_r1)
                        sheet.write(2*total+1,11,emissionp_r2-emissionp_r1)
                        sheet.write(2*total+1,12,emissionp_r3-emissionp_r2)
                        sheet.write(2*total+1,13,emissionp_r4-emissionp_r3)
                        sheet.write(2*total+1,14,emissionp_r5-emissionp_r4)
                        sheet.write(2*total+1,15,emissionp_r6-emissionp_r5)
                        sheet.write(2*total+1,16,disposal_name[m])
                        sheet.write(2*total+1,17,disposal[m]*lossp_r4)
                        sheet.write(2*total+1,18,sell_veg_percent[i]*trans2_veg_percent[j]*store1_veg_percent[k]*trans1_veg_percent[l]*energy_percent[n]*disposal_percent[m]*(1-package_percent))
                        sheet.write(2*total+1,19,emissionp_r6)
                        #sensitive(a,b,c,d,m,n,total)
                        total+=1
                        #print(total)
                        l+=1
                    k+=1
                j+=1
            i+=1
book.save("蔬菜333.xls")