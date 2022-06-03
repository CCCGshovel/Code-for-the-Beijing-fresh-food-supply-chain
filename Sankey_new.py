#新的sankey图
#目的：绘制食物种类-产生碳排放阶段-产生碳排放种类-食物种类的sankey图
from 通用碳排放框架 import choice_veg, choice_meat, sell, store1, trans2, trans1, food, produce, energy, disposal, energyname, disposal_name, package_emission
from 通用碳排放框架 import percent, per_cum, mass


#emissions：sankey图绘图数据存储的地方，为每种食物建立如下列表，出入上级列表emission_sankey中
emission=[
    #6个种类排放的综合（Node_labels[1]即第二排的内容）
    [0,0,0,0,0,0],
    #第二阶段，更新后为6个环节（Node_labels[2]即第二排的内容）
    [0,0,0,0,0,0],
    #每个环节的排放（用以表征sankey图产生碳排放阶段及产生碳排放种类的对应关系，为6*6）
    [    
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
        [0,0,0,0,0,0],
    ]
]

#上述框架复制六次得到每种食物的数据存储结构
from copy import deepcopy
emission_sankey=[]
for i in range(0,len(food)):
    emission_sankey.append(deepcopy((emission)))

#计算生产碳排放，因为生产的碳排需要多次反复调用且涉及不同参数的改变，所以可以多次调用这个函数
#由于我们是直接维护emission_sankey这个数组，因此遍历过程中不设置返回值
#此处m指需要生产的质量，用以计算不同环节造成损耗率造成不同碳排放的比较
def production_emission(f,m,percent,stage,n):
    emission_sankey[f][2][stage][2] += m * produce[f][0] * energy[n] / energy[0] * mass[f] * percent
    for t in range(1,len(emission_sankey[0][0])):
        emission_sankey[f][2][stage][2] += m * produce[f][t] * mass[f] * percent

#输入：标准参数列表（见标准框架）
#无输出，直接维护emission_sankey
def get_emissions(f,i,j,k,l,p,n,m):
    #a\b\c\d\e分别为销售市内库存省际生产对应的元组,p:是否包装,energy:能耗，dis：废弃物处理方式
    #0.525为经过文献及实地调研对包装效果的预估值，结合JCP2021内线性模型以及保质期在包装前后变化的文献得出
    global emission_sankey
    a = sell[f][i]
    b = trans2[f][j]
    c = store1[f][k]
    d = trans1[f][l]
    percent_line = percent[f][0][i]*percent[f][1][j]*percent[f][2][k]*percent[f][3][l]*percent[f][4][p]*percent[f][5][n]*percent[f][6][m]
    #判断是否有包装，正如之前讨论的结果，我们忽视不同包装对于损耗率的差异
    if p >= 1:
        packaged = 1
    else:
        packaged = 0
    #调整损耗率
    lr1 = a[0]*(1-packaged*0.475)
    lr2 = b[0]*(1-packaged*0.475)
    lr3 = c[0]*(1-packaged*0.475)
    lr4 = d[0]*(1-packaged*0.475)
    m1 = 1/(1 - lr1)
    #emissions_sankey[f]:访问某种食物的框架组合，由于我们分阶段逐渐累加，因此我们直接对emissions_sankey[f][2]的6*6矩阵进行维护
    #emissions_sankey[f][1]emissions_sankey[f][0]则在对2的数据维护完毕后直接没行/每列求和轻松得到
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
    #屠宰，跳过蔬果
    if f >= 2:
        m3 = m3/0.9
        emission_sankey[f][2][3][0] += m3 * 0.026 * energy[n]*percent_line*mass[f]
        emission_sankey[f][2][3][3] += m3 * 0.1 * disposal[m]*percent_line*mass[f]
        production_emission(f,m3*0.1,percent_line,3,n)
    m4 = m3 / (1 - lr4)
    emission_sankey[f][2][4][4] += d[1]*d[2]*m4*percent_line*mass[f]
    emission_sankey[f][2][4][3] += (m4-m3) * disposal[m]*percent_line*mass[f]
    production_emission(f,m4-m3,percent_line,4,n)

#依照参数顺序（见标准框架）调用上述函数进行维护操作
for f in range(0,6):
    for i in range(0,len(sell[f])):
        for j in range(0,len(trans2[f])):
            for k in range(0,len(store1[f])):
                for l in range(0,len(trans1[f])):
                    for p in range(0,2):
                        for m in range(0,len(disposal)):
                            for n in range(0,len(energy)):
                                get_emissions(f,i,j,k,l,p,n,m)

#累加完成绘图数据
for f in range(0,6):
    for i in range(0,len(emission_sankey[0][0])):
        for j in range(0,len(emission_sankey[0][1])):
            emission_sankey[f][0][i] += emission_sankey[f][2][j][i]
            emission_sankey[f][1][j] += emission_sankey[f][2][j][i]

#只是个检查，可以无视
for f in range(0,6):
    print(emission_sankey[f][0])
    print(emission_sankey[f][1])

from pyecharts import options as opts
from pyecharts.charts import Sankey
#能耗,施肥,器械设备,其他固定碳排放（饲料化肥生产等）,废弃物处理,肠胃发酵
#绘制sankey图所用标签
Node_label=[
    ["蔬菜 ","水果 ","牛肉 ","羊肉 ","猪肉 ","禽肉 "],
    ["售卖","市内运输","存储","加工","省际运输","包装"],
    ["直接能耗","FLW能耗","FLW","废弃物处理","车辆直接碳排","包装生产"]
]

#Nodes列表以及links列表，作为pyecharts库生成sankey图的输入及输出使用，Nodes定义所有数据节点（见NodesLabels列表）内容为字典
#Links完善所有数据关系，内容为字典
nodes=[]

#一些随机生成的颜色编码，手动指定网上扒拉的一个配色方案，避免随机生成
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


i=0
for item in Node_label:
    for data in item:
        #只是兼容早期版本所以没删能耗这个节点，当时赶时间做的比较粗暴
        if i <6 and data != "FLW能耗":
            nodes.append({"name" : data, "itemStyle":{"color": colors[i]}})
        else:
            nodes.append({"name" : data})
        i+=1

i = 0
for item in food:
    nodes.append({"name" : item,"itemStyle":{"color": colors[i]}})
    i+=1

links=[]

#输出表格用的，Stage（六阶段，销售等）到Type（FLW、废弃物处理等）的转化过程
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
            emission_type[i][j] += emission_sankey[f][2][j][i]
#分别依据三个不同规则输出表格
sheet_labels = ["Food-Stages", "Stages-Type", "Type-Food"]
data = []
sheet = []
for i in range(0,3):
    sheet1 = book.add_sheet(sheet_labels[i], cell_overwrite_ok = True)
    for j in range(0,len(Node_label[i%3])):
        sheet1.write(j+1, 0, Node_label[i%3][j])
        for k in range(0,len(Node_label[(i+1)%3])):
            sheet1.write(0, k+1, Node_label[(i+1)%3][k])
            if i == 0:
                data_source = emission_sankey[j][1]
            elif i == 2:
                data_source = emission_sankey[j][0]
            else:
                data_source = emission_type[j]
            sheet1.write(j+1, k+1, data_source[k])

book.save("Sankey Data.xls")

print(emission_type)
#依照之前规定方式，分别依照三组循环设定链接方式
for f in range(0,6):
    for i in range(0,6):
        if emission_sankey[f][1][i] != 0:
            links.append({"source": food[f], "target": Node_label[1][i], "value": emission_sankey[f][1][i]})
#        sheet.write(f+1,i+1,emission_sankey[f][1][i])
book.save("不同食物 不同环节的碳排放.xls")
for f in range(0,6):
    for i in range(0,len(emission_sankey[0][0])):
        if emission_sankey[f][0][i] >0:
            links.append({"source": Node_label[2][i], "target": Node_label[0][f], "value": emission_sankey[f][0][i]})
for i in range(0,len(emission_sankey[0][0])):
    for j in range(0,len(emission_sankey[0][1])):
        if emission_type[j][i]>0:
            links.append({"source": Node_label[1][j], "target": Node_label[2][i], "value": emission_type[j][i]})
    
#绘制sankey图
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
