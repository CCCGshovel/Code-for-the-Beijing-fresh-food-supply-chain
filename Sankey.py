sell = [0.000109054*122.77*21540,4.55*0.00001*81.9*21540,0.000383355*27.3*21540]
trans2 = [0.00022296*122.77*21540,0.002473*81.9*21540,0.006047657*27.3*21540]
store = [0.00016856*122.77*21540,0.000173*81.9*21540,0.00647*27.3*21540]
process = [0,0,1.891951593*27.3*21540]

loss=[(0.428414-0.3)*122.77*21540,(0.479684-0.32)*81.9*21540,(13.37020247-9.91)*27.3*21540]
produce = [0.3*122.77*21540,0.32*81.9*21540,9.91*27.3*21540]
package = [0.0232*122.77*21540,0.0294*81.9*21540,0.059149152*27.3*21540]
disposal = [0.013773*122.77*21540,0.015115*81.9*21540,0.00576946*27.3*21540]
std=[0.00197*122.77, 0.2272*81.9, 22.05*27.3]
trans1 = [(0.519607-0.428414)*122.77*21540,(0.62683-0.479684)*81.9*21540,(13.41309706-13.37020247)*27.3*21540]

from pyecharts import options as opts
from pyecharts.charts import Sankey

mass=[122.77,81.9]
data=[]



Node_label=[
    ["蔬菜","水果"],
    ["生产","废弃","能耗","制冷剂"],
    ["售卖","市内运输","仓储","省际运输","生产"]
]

nodes=[]

for item in Node_label:
    for data in item:
        nodes.append({"name" : data})

print(nodes)

links=[]

links.append({"source": "Vegetables", "target": "Packaging", "value": 0.116})
links.append({"source": "Vegetables", "target": "Production", "value": 0.3})
links.append({"source": "Vegetables", "target": "Transation", "value": 0.15})
links.append({"source": "Fruits", "target": "Packaging", "value": 0.084})
links.append({"source": "Fruits", "target": "Production", "value": 0.32})
links.append({"source": "Fruits", "target": "Transation", "value": 0.2})

c = (
    Sankey()
    .add(
        "",
        nodes,
        links,
        linestyle_opt=opts.LineStyleOpts(opacity=0.2, curve=0.5, color="source"),
        label_opts=opts.LabelOpts(position="right"),
    )
    .set_global_opts(title_opts=opts.TitleOpts(title="深入强化"))
    .render("Sankey_vegetable.html")    
)
