#新的sankey图
#我们一直以来的努力，全部都白费了

from 通用碳排放框架 import choice_veg, choice_meat, sell, store1, trans2, trans1, food, produce, energy, disposal, energyname, disposal_name, package_emission
from 通用碳排放框架 import percent, per_cum, mass


#现在需要多少个种类？
#能耗、FLW能耗、FLW其他、废弃物处理、机器、包装生产
#FLW的能耗和其他碳排放怎么分？#我觉得原来那种分法其实蛮离大谱的
emission=[
    #6个种类排放的综合
    [0,0,0,0,0,0],
    #第二阶段，7个环节，加加工、包装,刨掉1kg生产
    [0,0,0,0,0,0],
    #每个环节的排放
    [    
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
    ]
]

from copy import deepcopy

emission_sankey=[]
for i in range(0,len(food)):
    emission_sankey.append(deepcopy((emission)))

def production_emission(f,m,percent,stage,n):
    emission_sankey[f][2][stage][1] += m * produce[f][0] * energy[n] / energy[0] * mass[f] * percent
    for t in range(1,len(emission_sankey[0][0])):
        emission_sankey[f][2][stage][2] += m * produce[f][t] * mass[f] * percent

def get_emissions(f,i,j,k,l,p,n,m):
    #a\b\c\d\e分别为销售市内库存省际生产对应的元组,p:是否包装,energy:能耗，dis：废弃物处理方式
    #0.525为经过文献及实地调研对包装效果的预估值，结合JCP2021内线性模型以及保质期在包装前后变化的文献得出
    global emission_sankey
    a = sell[f][i]
    b = trans2[f][j]
    c = store1[f][k]
    d = trans1[f][l]
    percent_line = percent[f][0][i]*percent[f][1][j]*percent[f][2][k]*percent[f][3][l]*percent[f][4][p]*percent[f][5][n]*percent[f][6][m]
    if p >= 1:
        packaged = 1
    else:
        packaged = 0
    lr1 = a[0]*(1-packaged*0.475)
    lr2 = b[0]*(1-packaged*0.475)
    lr3 = c[0]*(1-packaged*0.475)
    lr4 = d[0]*(1-packaged*0.475)
    m1 = 1/(1 - lr1)
    emission_sankey[f][2][0][0] += m1*a[1]*a[2]*energy[n]*percent_line*mass[f]
    emission_sankey[f][2][0][3] += (m1-1)*disposal[m]*percent_line*mass[f]
    production_emission(f,m1-1,percent_line,0,n)
    emission_sankey[f][2][5][5] += package_emission[f][p]*percent_line*mass[f]
    m2 = m1/(1 - lr2)
    emission_sankey[f][2][1][4] += b[1]*b[2]*m2*percent_line*mass[f]
    emission_sankey[f][2][1][3] += (m2-m1)*disposal[m]*percent_line*mass[f]
    production_emission(f,m2-m1,percent_line,1,n)
    m3 = m2 / (1 - lr3)
    emission_sankey[f][2][2][0] += m3*c[1]*c[2]*energy[n]*percent_line*mass[f]
    emission_sankey[f][2][0][3] += (m3-m2)*disposal[m]*percent_line*mass[f]
    production_emission(f,m3-m2,percent_line,2,n)
    if f >= 2:
        m3 = m3/0.9
        emission_sankey[f][2][3][0] += m3 * 1.6 * energy[n]*percent_line*mass[f]
        emission_sankey[f][2][3][3] += m3 * 0.1 * disposal[m]*percent_line*mass[f]
        production_emission(f,m3*0.1,percent_line,3,n)
    m4 = m3 / (1 - lr4)
    emission_sankey[f][2][4][4] += d[1]*d[2]*m4*percent_line*mass[f]
    emission_sankey[f][2][4][3] += (m4-m3) * disposal[m]*percent_line*mass[f]
    production_emission(f,m4-m3,percent_line,4,n)

for f in range(0,6):
    for i in range(0,len(sell[f])):
        for j in range(0,len(trans2[f])):
            for k in range(0,len(store1[f])):
                for l in range(0,len(trans1[f])):
                    for p in range(0,2):
                        for m in range(0,len(disposal)):
                            for n in range(0,len(energy)):
                                get_emissions(f,i,j,k,l,p,n,m)

for f in range(0,6):
    for i in range(0,len(emission_sankey[0][0])):
        for j in range(0,len(emission_sankey[0][1])):
            emission_sankey[f][0][i] += emission_sankey[f][2][j][i]
            emission_sankey[f][1][j] += emission_sankey[f][2][j][i]

for f in range(0,6):
    print(emission_sankey[f][0])
    print(emission_sankey[f][1])

from pyecharts import options as opts
from pyecharts.charts import Sankey
#能耗,施肥,器械设备,其他固定碳排放（饲料化肥生产等）,废弃物处理,肠胃发酵
Node_label=[
    ["蔬菜 ","水果 ","牛肉 ","羊肉 ","猪肉 ","禽肉 "],
    ["售卖","市内运输","存储","加工","省际运输","包装"],
    ["直接能耗","FLW能耗","FLW其他","废弃物处理","车辆直接碳排","包装生产"]
]

nodes=[]


colors = [
    "#67001f",
    "#b2182b",
    "#d6604d",
    "#f4a582",
    "#fddbc7",
    "#a3001f",
    "#d1e5f0",
    "#9325de",
    "#4356c3",
    "#2444ac",
    "#0533a6",
    "#d6e3f2",
    "#95c2df",
    "#5294c1",
    "#d266ac",
    "#053061",
    "#96e1da",
    "#ee3343",
    "#21733d",
    "#053061",
    "#43e3f2",
    "#95c22f",
    "#51a9cd",
    "#d326ac",
    "#0554ee",
]
import xlwt
book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet("stages", cell_overwrite_ok = True)
for i in range(0,6):
    sheet.write(1+i,0,Node_label[0][i])
    sheet.write(0,1+i,Node_label[1][i])

i=0
for item in Node_label:
    for data in item:
        if i <6:
            nodes.append({"name" : data, "itemStyle":{"color": colors[i]}})
        else:
            nodes.append({"name" : data})
        i+=1

i = 0
for item in food:
    nodes.append({"name" : item,"itemStyle":{"color": colors[i]}})
    i+=1

links=[]

emission_type=[
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
]

for f in range(0,6):
    for i in range(0,len(emission_sankey[0][0])):
        for j in range(0,len(emission_sankey[0][1])):
            emission_type[j][i] += emission_sankey[f][2][j][i]


print(emission_type)

for f in range(0,6):
    for i in range(0,6):
        if emission_sankey[f][1][i] != 0:
            links.append({"source": food[f], "target": Node_label[1][i], "value": emission_sankey[f][1][i]})
        sheet.write(f+1,i+1,emission_sankey[f][1][i])
book.save("不同食物 不同环节的碳排放.xls")
for f in range(0,6):
    for i in range(0,len(emission_sankey[0][0])):
        if emission_sankey[f][0][i] >0:
            links.append({"source": Node_label[2][i], "target": Node_label[0][f], "value": emission_sankey[f][0][i]})
for i in range(0,len(emission_sankey[0][0])):
    for j in range(0,len(emission_sankey[0][1])):
        if emission_type[j][i]>0:
            links.append({"source": Node_label[1][j], "target": Node_label[2][i], "value": emission_type[j][i]})
    

c = (
    Sankey()
    .add(
        "",
        nodes,
        links,
        linestyle_opt=opts.LineStyleOpts(opacity=0.2, curve=0.5, color="source"),
        label_opts=opts.LabelOpts(position="right"),
    )
    .set_global_opts(title_opts=opts.TitleOpts(title="整体碳排放"))
    .render("Sankey_total_ver2.html")    
)
