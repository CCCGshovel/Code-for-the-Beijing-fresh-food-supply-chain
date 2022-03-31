#这个的目标是用热力图的框架把灵敏性分析给做出来

from 通用碳排放框架 import choice_veg, choice_meat, sell, store1, trans2, trans1, food, produce, energy, disposal, energyname, disposal_name, package_emission
from 通用碳排放框架 import percent, per_cum, mass

import matplotlib.pyplot as plt
import numpy
from numpy import log10

percent_cum = per_cum(percent)

#计算生产的总碳排,因为这里不区分不同排放的来源所以直接使用加和的总数据
def production_emission(f,m,en,production_else):
    #f：Food m：mass
    e = 0
    e += produce[f][0]*m
    e += production_else*m
    return e

def get_emission(f,parameters):
    #f,食物;parameters:长度为{}的列表,其内容为：
    #蔬果类：[a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],produce_noenergy,package_emission,energy[n],disposal[m]]
    #肉类：[a[0],a[1],a[2],a[3],b[0],b[1],b[2],c[0],c[1],c[2],c[3],d[0],d[1],d[2],produce_noenergy,package_emission,energy[n],disposal[m],1.6(能耗),0.1(损耗率)]
    if parameters[15] != 0:
        packaged = 1
    else: 
        packaged = 0
    result = []
    lr1 = parameters[0] * (1 - packaged*0.475)
    lr2 = parameters[4] * (1 - packaged*0.475)
    lr3 = parameters[7] * (1 - packaged*0.475)
    lr4 = parameters[11] * (1 - packaged*0.475)
    m1 = 1/(1 - lr1)
    #商店直接碳排
    result.append(m1*parameters[1]*parameters[2]*parameters[16]+m1*parameters[3])
    #商店FLW及废弃物处理
    #print("{} {}".format(parameters[17],parameters[14]))
    #包装
    result.append(parameters[15])
    m2 = m1/(1 - lr2)
    #市内：直接/FLW/disposal
    result.append( parameters[5]*parameters[6]*m2 )
    m3 = m2 / (1 - lr3)
    #存储：直接/FLW/disposal
    result.append( m3*parameters[8]*parameters[9]*parameters[16] + parameters[10])
    if f >= 2:
        m3 = m3/(1-parameters[19])
        #加工：直接/FLW/disposal
        #print(parameters[18]*parameters[16]*m3)
        result.append( m3 * parameters[18] * parameters[16])
    m4 = m3 / (1 - lr4)
    #省际：直接/FLW/disposal
    result.append( parameters[12] * parameters[13] * m4)
    result.append((parameters[14] + parameters[17])*(m4-1))
    #生产（1kg）
    #result.append(production_emission(f,1))
    total_e = 0#（计算总计碳排放）
    for data in result:
        total_e += data
    result.append(total_e)
    #仅需要不包含生产的比例,因此输出total_e即可
    return total_e

def get_emissions_all(f, parameter_id):
    #返回第i个列表的参数优化10%时的变化率
    e = 0
    e_produce_else = 0
    for i in range(1,len(produce[f])):
        e_produce_else += produce[f][i]
    for i in range(0,len(sell[f])):
        for j in range(0,len(trans2[f])):
            for k in range(0,len(store1[f])):
                for l in range(0,len(trans1[f])):
                    for p in range(0,len(package_emission[f])):
                        for n in range(0,len(energy)):
                            for m in range(0,len(disposal)):
                                parameters = []
                                percent_line = percent[f][0][i]*percent[f][1][j]*percent[f][2][k]*percent[f][3][l]*percent[f][4][p]*percent[f][5][n]*percent[f][6][m]
                                for para in range(0,4):
                                    parameters.append(sell[f][i][para])
                                for para in range(0,3):
                                    parameters.append(trans2[f][j][para])
                                for para in range(0,4):
                                    parameters.append(store1[f][k][para])
                                for para in range(0,3):
                                    parameters.append(trans1[f][k][para])
                                parameters.append(e_produce_else)
                                parameters.append(package_emission[f][p])
                                parameters.append(energy[n])
                                parameters.append(disposal[m])
                                if f >= 2:
                                    parameters.append(1.6)
                                    parameters.append(0.1)
                                if parameter_id >= 0:
                                    parameters[parameter_id] *= 0.9
                                e += get_emission(f,parameters) * percent_line
    return e

basic = []
for f in range(0,6):
    basic.append(get_emissions_all(f,-1))

label_paras = [
    "销售损耗率","销售电耗","销售存储时间","销售制冷剂泄漏",
    "二级运输损耗","二级运输排放因子","二级运输里程",
    "存储损耗率","存储电耗","存储时间","存储制冷剂泄漏",
    "一级运输损耗","一级运输排放因子","一级运输里程",
    "生产","包装碳排放","发电排放因子","废弃物处理碳排放","加工能耗","加工损耗率",
]

draw = [[],[],[],[],[],[]]
for f in range(0,6):
    length = len(label_paras)
    if f < 2:
        length -= 2
    for i in range(0,length):
        draw[f].append(numpy.log10(1-get_emissions_all(f, i)/basic[f])) 
    if f < 2:
        draw[f].append(-100)
        draw[f].append(-100)
    print(draw[f])


result = numpy.array(draw)
result_t=result.transpose()

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.rcParams['font.size']=9

fig,ax = plt.subplots(figsize=(12,8),dpi = 300)
a = ax.imshow(result_t,vmin=-6,vmax=-1,aspect="auto",cmap='coolwarm')
tickx=[]
ticky=[]
for i in range(0,len(label_paras)):
    ticky.append(i)
for i in range(0,len(food)):
    tickx.append(i)
for edge, spine in ax.spines.items():
        spine.set_visible(False)
ax.set_yticks(ticky,minor=False)
ax.set_yticklabels(label_paras,rotation=45)
ax.set_xticks(tickx,minor=False)
ax.set_xticklabels(food)
ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)
fig.colorbar(a)
for i in range(len(food)):
    for j in range(len(label_paras)):
        data = "Na"
        if result_t[j, i] != -100:
            data = int(result_t[j, i]*1000)/1000
        text = ax.text(i, j, data,ha="center", va="center", color="black")
ax.set_title("不同参数灵敏性分析结果")
plt.savefig("灵敏性汇总(改，彩色).png")
plt.show()