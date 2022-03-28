import pandas
from pymongo import MongoClient
import matplotlib.pyplot as plt


client = MongoClient("mongodb://admin:admin123@192.168.50.103:27017/")
db = client['weibo']
collection = db.comment_user_info
df = pandas.DataFrame(list(collection.find()))
del df['_id']
data = df[['fans_count', 'follows_count', 'weibos_count']]

data.insert(loc=3, column='Activity', value=df['fans_count'] * 0.4 + df['follows_count'] * 0.3 + df['weibos_count'] * 0.3)

bins = [0, 100, 500, 1000, 10000, 100000, 100000000]
labels = ['Too Low', 'Low', 'Normal', 'High', 'Too High', 'Not Personal']
colors = ['#7986CA', '#AFD7F7', '#C8B4E1', '#E6C9E1', '#F4E6BA', '#EABECA']
explode = [0, 0, 0, 0.4, 0.4, 0.4]

group = data.groupby(pandas.cut(data['Activity'], bins=bins, labels=labels)).count()

font = 'Microsoft Yahei'

plt.axis('equal')

group = group['Activity']

plt.gca().spines['right'].set_color('none')
plt.gca().spines['top'].set_color('none')
plt.gca().spines['left'].set_color('none')
plt.gca().spines['bottom'].set_color('none')

plt.xlim(0, 8)
plt.ylim(0, 8)
plt.xticks(())
plt.yticks(())

plt.title('微博评论用户活跃度', fontproperties=font, fontsize=12)

plt.pie(x=group, labels=labels,
        autopct='%.3f%%',  # 设置百分比的格式,保留3位小数
        pctdistance=0.7,  # 设置百分比标签和圆心的距离
        colors=colors,  # 设置百分比颜色
        explode=explode,  # 突出显示
        labeldistance=1.2,  # 设置标签和圆心的距离
        startangle=180,  # 设置饼图的初始角度
        center=(4, 4),  # 设置饼图的圆心(相当于X轴和Y轴的范围)
        radius=4,  # 设置饼图的半径(相当于X轴和Y轴的范围)
        counterclock=False,  # 是否为逆时针方向,False表示顺时针方向
        textprops={'fontsize': 9, 'color': 'black', 'fontproperties': font}, #设置文本标签的属性值
        frame=1)  # 是否显示饼图的圆圈,1为显示

plt.legend(loc='upper right', bbox_to_anchor=(1.12, 1.12))
plt.savefig(r'C:\Users\Astria\Pictures\Camera Roll\dataAnalysis.jpg',
            dpi=2000, bbox_inches='tight')

plt.show()
