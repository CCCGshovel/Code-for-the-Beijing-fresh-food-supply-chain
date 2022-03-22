#目的：构建一个计算框架，并把所有的数据标准化，把所有单元存下来
#最终我们可以直接调用不同单元对应的节点，再直接算出来数据
#但最好这个位置可以留一个直接把比例接进来的接口
#实际上我们每个单位所需要访问的只有两个数据，一个是碳排放，一个是损耗率

import xlwt


#不同温度（常温、冷藏）
#(损耗率（%），单位时间能耗（kWh/k(g*d)），时长（d）,包装碳排放+制冷剂碳排放（kgCO2e/kg）)
#包装的碳排加在这一级
sell_meat = [
    (0.013325,0,0.625,0),
    (0.013325/3,0.0006,0.625,0.00005644),
]

#输出表格时使用的注解
name=[
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
#火电，水电，核能，风能
energy_percent=[0.818,0.155,0.019,0.008]
#废弃物处理比例：焚烧/堆肥/厌氧消化
disposal_percent=[0.5,0.25,0.25]
#长途运输距离（新发地调研比例估算）
meat_trans1_dis = 726.497 
#市内平均距离（Arcgis计算）
meat_trans2_dis = 30


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

#kgCO2e/kwh
energy=[1.28,0.00339,0.00779,0.00112]
energyname=["火电","水电","核电","太阳能"]

#kgCO2e/kg
disposal=[0.02582,-0.02754,0.165]
disposal_name=["焚烧","厌氧消化","堆肥"]

book=xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet=book.add_sheet('lines', cell_overwrite_ok=True)
sheet_sensitive = book.add_sheet("sensitive", cell_overwrite_ok = True)

def get_emission(a0,a1,a2,a3,b0,b1,b2,c0,c1,c2,c3,proce,proce_loss,d0,d1,d2,d3,package,en,dis,pack):
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

#返回初始组合的碳排放期望
def caculateall():
    emission = 0
    for m in range(0,len(disposal)):
        for n in range(0,len(energy)):
            i=0
            for a in sell_meat:
                j=0
                for b in trans2_meat:
                    k=0
                    for c in store1_meat:
                        l=0
                        for d in trans1_meat:
                            emission += sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*energy_percent[n]*disposal_percent[m]*(0.35*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.116)+0.65*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169))
                            l+=1
                        k+=1
                    j+=1
                i+=1
    return emission    


#绘图1：初始以1/3累积碳排为分界的累积分布逆函数
emissions=[]
for m in range(0,len(disposal)):
        for n in range(0,len(energy)):
            i=0
            for a in sell_meat:
                j=0
                for b in trans2_meat:
                    k=0
                    for c in store1_meat:
                        l=0
                        for d in trans1_meat:
                            e1=get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169)
                            e2=get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169)
                            emissions.append((e1,0.35*sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*energy_percent[n]*disposal_percent[m]))
                            emissions.append((e2,0.65*sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*energy_percent[n]*disposal_percent[m]))
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


import matplotlib.pyplot as plt

x2.insert(0,x1[-1])
y2.insert(0,y1[-1])
x3.insert(0,x2[-1])
y3.insert(0,y2[-1])    
fig, ax1=plt.subplots()
ax1.fill_between(x1,y1,alpha=0.2,step="pre",color="red")
ax1.fill_between(x2,y2,alpha=0.5,step="pre",color="red")
ax1.fill_between(x3,y3,alpha=0.8,step="pre",color="red")
ax1.set_ylabel('emission:kgCO2e/kg')
ax1.set_title("meat cumulative emission")
plt.show()

#灵敏性分析 计算每条链条在对应参数下调10%的情况下碳排放的变化率，返回一个列表
def caculateall1():
    emission = 0
    emission_down=[]
    result=[]
    for i in range(0,20):
        emission_down.append(0)
    for m in range(0,len(disposal)):
        for n in range(0,len(energy)):
            i=0
            for a in sell_meat:
                j=0
                for b in trans2_meat:
                    k=0
                    for c in store1_meat:
                        l=0
                        for d in trans1_meat:
                            emission += sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*energy_percent[n]*disposal_percent[m]*(0.35*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169)+0.65*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169))
                            emission_down[0] += sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*energy_percent[n]*disposal_percent[m]*(0.35*get_emission(0.9*a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169)+0.65*get_emission(0.9*a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169))
                            emission_down[1] += sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*energy_percent[n]*disposal_percent[m]*(0.35*get_emission(a[0],0.9*a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169)+0.65*get_emission(a[0],0.9*a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169))
                            emission_down[2] += sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*energy_percent[n]*disposal_percent[m]*(0.35*get_emission(a[0],a[1],0.9*a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169)+0.65*get_emission(a[0],a[1],0.9*a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169))
                            emission_down[3] += sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*energy_percent[n]*disposal_percent[m]*(0.35*get_emission(a[0],a[1],a[2],0.9*a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169)+0.65*get_emission(a[0],a[1],a[2],0.9*a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169))
                            emission_down[4] += sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*energy_percent[n]*disposal_percent[m]*(0.35*get_emission(a[0],a[1],a[2],a[3],0.9*b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169)+0.65*get_emission(a[0],a[1],a[2],a[3],0.9*b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169))
                            emission_down[5] += sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*energy_percent[n]*disposal_percent[m]*(0.35*get_emission(a[0],a[1],a[2],a[3],b[0],0.9*b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169)+0.65*get_emission(a[0],a[1],a[2],a[3],b[0],0.9*b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169))
                            emission_down[6] += sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*energy_percent[n]*disposal_percent[m]*(0.35*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],0.9*b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169)+0.65*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],0.9*b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169))
                            emission_down[7] += sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*energy_percent[n]*disposal_percent[m]*(0.35*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],0.9*c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169)+0.65*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],0.9*c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169))
                            emission_down[8] += sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*energy_percent[n]*disposal_percent[m]*(0.35*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],0.9*c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169)+0.65*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],0.9*c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169))
                            emission_down[9] += sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*energy_percent[n]*disposal_percent[m]*(0.35*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],0.9*c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169)+0.65*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],0.9*c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169))
                            emission_down[10] += sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*energy_percent[n]*disposal_percent[m]*(0.35*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],0.9*c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169)+0.65*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],0.9*c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169))
                            emission_down[11] += sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*energy_percent[n]*disposal_percent[m]*(0.35*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,0.9*d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169)+0.65*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,0.9*d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169))
                            emission_down[12] += sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*energy_percent[n]*disposal_percent[m]*(0.35*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],0.9*d[1],d[2],d[3],0,energy[n],disposal[m],0.169)+0.65*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],0.9*d[1],d[2],d[3],1,energy[n],disposal[m],0.169))
                            emission_down[13] += sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*energy_percent[n]*disposal_percent[m]*(0.35*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],0.9*d[2],d[3],0,energy[n],disposal[m],0.169)+0.65*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],0.9*d[2],d[3],1,energy[n],disposal[m],0.169))
                            emission_down[14] += sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*energy_percent[n]*disposal_percent[m]*(0.35*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],0.9*d[3],0,energy[n],disposal[m],0.169)+0.65*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],0.9*d[3],1,energy[n],disposal[m],0.169))
                            emission_down[15] += sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*energy_percent[n]*disposal_percent[m]*(0.35*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,0.9*energy[n],disposal[m],0.169)+0.65*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,0.9*energy[n],disposal[m],0.169))
                            emission_down[16] += sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*energy_percent[n]*disposal_percent[m]*(0.35*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],0.9*disposal[m],0.169)+0.65*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],0.9*disposal[m],0.169))
                            emission_down[17] += sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*energy_percent[n]*disposal_percent[m]*(0.35*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.9*0.169)+0.65*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.9*0.169))
                            emission_down[18] += sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*energy_percent[n]*disposal_percent[m]*(0.35*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169)+0.65*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6*0.9,0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169))
                            emission_down[19] += sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*energy_percent[n]*disposal_percent[m]*(0.35*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169)+0.65*get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1*0.9,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169))
                            l+=1
                        k+=1
                    j+=1
                i+=1
    for i in range(0,len(emission_down)):
        result.append(1-emission_down[i]/emission)
    print(result)
    return result    

from numpy import log10

#绘图2：不同参数的灵敏性柱状图，最后使用其对数进行表征
data1=[]
data2=[]
data3=[]
resulttttt=caculateall1()

labels=["S2_lr","S2_t","S2_r","S2_e","T2_lr","T2_r","T2_m","S1_lr","S1_t","S1_r","S1_e","T1_lr","T1_r","T1_m","Produce","En_r","Dis_r","Pack_r","Pro_r","Pro_lr"]
data=[]
data1=[]
data2=[]
data3=[]
resulttttt=caculateall1()
for i in range(0,len(resulttttt)):
    data.append(log10(resulttttt[i]))

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
ax.set_title('Sensitivity of meat')

ax.legend()
plt.show()

package_emission=0.169
package_percent=0.65

emissions_lines=[]
all=0
i=0
for a in sell_meat:
    j=0
    for b in trans2_meat:
        k=0
        for c in store1_meat:
            l=0
            emission=0
            emissionp=0
            for d in trans1_meat:
                for n in range(0,len(energy)):
                    for m in range(0,len(disposal)):
                        emission += sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*energy_percent[n]*disposal_percent[m]*(1-package_percent)* get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],package_emission)
                        emissionp += sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*energy_percent[n]*disposal_percent[m]*package_percent* get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],package_emission)
                l+=1
            emissions_lines.append((emission*sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*(1-package_percent),i%2,j%2,k%2,0))
            emissions_lines.append((emissionp*sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*package_percent,i%2,j%2,k%2,1))
            k+=1
        j+=1
    i+=1

label_emission=[]
emissions_fin=[]
emissions_lines.sort(key=lambda x:x[0])

for item in emissions_lines:
    label_emission.append("{}\n{}\n{}\n{}".format(item[1],item[2],item[3],item[4]))
    emissions_fin.append(item[0])

fig , ax_emission = plt.subplots()

ax_emission.bar(label_emission,emissions_fin,width=0.3)
ax_emission.set_title("Carbon Emissions for lines")
ax_emission.set_ylabel("kgCO2e/kg food consumption")

#绘图5 绘制不同链条损耗率的对应比例
fig , ax_lr = plt.subplots(2,1,sharex=True)

emissions=[]
loss_rate=[]
loss_amount=[]

for i in range(0,2):
    for j in range(0,2):
        for k in range(0,2):
            for l in range(0,2):
                lr1 = sell_meat[i][0]
                lr2 = 1-(1-lr1)*(1-trans1_meat[j][0])
                lr3 = 1-(1-lr2)*(1-store1_meat[k][0])
                lr4 = 1-(1-lr3)*0.9
                lr5 = 1-(1-lr4)*(1-trans1_meat[l][0])
                lrp1 = sell_meat[i][0]*0.525
                lrp2 = 1-(1-lrp1)*(1-trans2_meat[j][0]*0.525)
                lrp3 = 1-(1-lrp2)*(1-store1_meat[k][0]*0.525)
                lrp4 = 1-(1-lrp3)*0.9
                lrp5 = 1-(1-lrp4)*(1-trans1_meat[l][0]*0.525)
                loss_rate.append((lr1,lr2,lr3,lr4,lr5,i%2,j%2,k%2,l%2,0,(1/(1-lr4)-1)*sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*(1-package_percent)))
                loss_rate.append((lrp1,lrp2,lrp3,lrp4,lrp5,i%2,j%2,k%2,l%2,1,(1/(1-lrp4)-1)*sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*package_percent))

label_lr=[]
lr_data=[[],[],[],[],[]]
lr_data_name=["Sell","Trans2","Store","Process","Trans1"]
loss_rate.sort(key = lambda x : x[4])

for item in loss_rate:
    label_lr.append("{}\n{}\n{}\n{}".format(item[5],item[6],item[7],item[8]))
    for i in range(0,len(lr_data)):
        lr_data[i].append(item[i])
    loss_amount.append(item[-1])


for i in range(0,len(lr_data)):
    ax_lr[0].bar(label_lr, lr_data[len(lr_data)-i-1], width=0.3, label=lr_data_name[len(lr_data)-i-1])
ax_lr[1].bar(label_lr,loss_amount, width=0.3)
ax_lr[0].set_title("meat Loss rate")
ax_lr[1].set_title("meat Loss amount")
ax_lr[0].set_ylabel("%")
ax_lr[1].set_ylabel("kg food loss / kg food consumed in society")
ax_lr[0].legend()
plt.show()
#输出每条链灵敏性分析的前置计算（已弃用）
def sensitive(a,b,c,d,m,n,total):
    e_basic = get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169)
    sheet_sensitive.write(2*total,0,"无包装")
    sheet_sensitive.write(2*total,1,name[0][i])
    sheet_sensitive.write(2*total,2,name[1][j])
    sheet_sensitive.write(2*total,3,name[2][k])
    sheet_sensitive.write(2*total,4,name[3][l])
    sheet_sensitive.write(2*total,5,energyname[n])
    sheet_sensitive.write(2*total,6,disposal_name[m])
    sheet_sensitive.write(2*total, 7, 1-get_emission(0.9*a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total, 8, 1-get_emission(a[0],0.9*a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total, 9, 1-get_emission(a[0],a[1],0.9*a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total, 10, 1-get_emission(a[0],a[1],a[2],0.9*a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total, 11, 1-get_emission(a[0],a[1],a[2],a[3],0.9*b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total, 12, 1-get_emission(a[0],a[1],a[2],a[3],b[0],0.9*b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total, 13, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],0.9*b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total, 14, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],0.9*c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total, 15, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],0.9*c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total, 16, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],0.9*c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total, 17, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],0.9*c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total, 18, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],0.9*1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total, 19, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.9*0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total, 20, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,0.9*d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total, 21, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],0.9*d[1],d[2],d[3],0,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total, 22, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],0.9*d[2],d[3],0,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total, 23, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],0.9*d[3],0,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total, 24, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,0.9*energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total, 25, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],0.9*disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total, 26, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.9*0.169)/e_basic)
    e_basic = get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169)
    sheet_sensitive.write(2*total+1,0,"包装")
    sheet_sensitive.write(2*total+1,1,name[0][i])
    sheet_sensitive.write(2*total+1,2,name[1][j])
    sheet_sensitive.write(2*total+1,3,name[2][k])
    sheet_sensitive.write(2*total+1,4,name[3][l])
    sheet_sensitive.write(2*total+1,5,energyname[n])
    sheet_sensitive.write(2*total+1,6,disposal_name[m])
    sheet_sensitive.write(2*total+1, 7, 1-get_emission(0.9*a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total+1, 8, 1-get_emission(a[0],0.9*a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total+1, 9, 1-get_emission(a[0],a[1],0.9*a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total+1, 10, 1-get_emission(a[0],a[1],a[2],0.9*a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total+1, 11, 1-get_emission(a[0],a[1],a[2],a[3],0.9*b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total+1, 12, 1-get_emission(a[0],a[1],a[2],a[3],b[0],0.9*b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total+1, 13, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],0.9*b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total+1, 14, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],0.9*c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total+1, 15, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],0.9*c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total+1, 16, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],0.9*c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total+1, 17, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],0.9*c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total+1, 18, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],0.9*1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total+1, 19, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.9*0.1,d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total+1, 20, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,0.9*d[0],d[1],d[2],d[3],1,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total+1, 21, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],0.9*d[1],d[2],d[3],1,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total+1, 22, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],0.9*d[2],d[3],1,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total+1, 23, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],0.9*d[3],1,energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total+1, 24, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,0.9*energy[n],disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total+1, 25, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],1,energy[n],0.9*disposal[m],0.169)/e_basic)
    sheet_sensitive.write(2*total+1, 26, 1-get_emission(a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],1.6,0.1,d[0],d[1],d[2],d[3],0,energy[n],disposal[m],0.169*0.9)/e_basic)    

#输出每张链条的对应参数
total=0
for m in range(0,len(disposal)):
    for n in range(0,len(energy)):
        i=0
        for a in sell_meat:
            loss_r1 = a[0]
            lossp_r1 = a[0]*0.525
            emission_r1 = 1 / (1-loss_r1) * (a[1]*a[2]*energy[n] + a[3])
            emissionp_r1 = 1 / (1-lossp_r1) * (a[1]*a[2]*energy[n] + a[3])
            j=0
            for b in trans2_meat:
                loss_r2 = 1 - (1 - loss_r1) * (1 - b[0])
                emission_r2 = emission_r1 + 1/(1-loss_r2)*b[1]*b[2]
                lossp_r2 = 1 - (1 - lossp_r1) * (1 - b[0]*0.525)
                emissionp_r2 = emissionp_r1 + 1/(1-lossp_r2)*b[1]*b[2]
                k=0
                for c in store1_meat:
                    loss_r3 = 1 - (1 - loss_r2) * (1 - c[0])
                    emission_r3 = emission_r2 + 1/(1-loss_r3)*(c[1]*c[2]*energy[n] + c[3])
                    lossp_r3 = 1 - (1 - lossp_r2) * (1 - c[0]*0.525)
                    emissionp_r3 = emissionp_r2 + 1/(1-lossp_r3)*(c[1]*c[2]*energy[n] + c[3])
                    loss_r4 = 1-(1-loss_r3) * 0.9 
                    lossp_r4 = 1-(1+lossp_r3)* 0.9 
                    emission_r4 = 1.6 * 1/(1-loss_r4)*energy[n]
                    emissionp_r4 = 1.6 * 1/(1-lossp_r4)*energy[n]
                    l=0
                    for d in trans1_meat:
                        loss_r5 = 1- (1 - loss_r4) * (1 - d[0]) 
                        emission_r5 = emission_r4 + 1/(1-loss_r5)*(d[1]*d[2])
                        lossp_r5 = 1-(1 - lossp_r4) * (1 - d[0]*0.525) 
                        emissionp_r5 = emissionp_r4 + 1/(1-lossp_r5)*(d[1]*d[2])
                        emission_r6 = emission_r5 + d[3]*1/(1-loss_r5)
                        emissionp_r6 = emissionp_r5 + d[3]*1/(1-lossp_r5)
                        emission_r7 = emission_r6 + 0
                        emissionp_r7 = emissionp_r6 + 0.169
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
                        sheet.write(2*total,10,loss_r5)
                        sheet.write(2*total,11,emission_r1)
                        sheet.write(2*total,12,emission_r2-emission_r1)
                        sheet.write(2*total,13,emission_r3-emission_r2)
                        sheet.write(2*total,14,emission_r4-emission_r3)
                        sheet.write(2*total,15,emission_r5-emission_r4)
                        sheet.write(2*total,16,emission_r6-emission_r5)
                        sheet.write(2*total,17,emission_r7-emission_r6)
                        sheet.write(2*total,18,disposal_name[m])
                        sheet.write(2*total,19,disposal[m]*loss_r5)
                        sheet.write(2*total,20,sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*energy_percent[n]*disposal_percent[m]*0.65)
                        sheet.write(2*total,21,emission_r7)
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
                        sheet.write(2*total+1,10,lossp_r5)
                        sheet.write(2*total+1,11,emissionp_r1)
                        sheet.write(2*total+1,12,emissionp_r2-emissionp_r1)
                        sheet.write(2*total+1,13,emissionp_r3-emissionp_r2)
                        sheet.write(2*total+1,14,emissionp_r4-emissionp_r3)
                        sheet.write(2*total+1,15,emissionp_r5-emissionp_r4)
                        sheet.write(2*total+1,16,emissionp_r6-emissionp_r5)
                        sheet.write(2*total+1,17,emissionp_r7-emissionp_r6)
                        sheet.write(2*total+1,18,disposal_name[m])
                        sheet.write(2*total+1,19,disposal[m]*lossp_r4)
                        sheet.write(2*total+1,20,sell_meat_percent[i]*trans2_meat_percent[j]*store1_meat_percent[k]*trans1_meat_percent[l]*energy_percent[n]*disposal_percent[m]*0.35)
                        sheet.write(2*total+1,21,emissionp_r7)
                        sensitive(a,b,c,d,m,n,total)
                        total += 1
                        l+=1
                    k+=1
                j+=1
            i+=1
book.save("肉类2.xls")