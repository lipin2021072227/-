# 载入包
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns  # 画图

# 画图的主题设计
sns.set_theme()  # 切换到seaborn的默认主题
sns.set_context('notebook')  # 上下文设置绘图元素的比例，用不同的上下文表示适用于较大尺寸绘图或较小尺寸绘图，设置上下文后，相同的绘图函数显示的图形会根据上下问自动缩放。
# 数据的获取
# 读数据
data_user = pd.read_csv("D:\\比赛\\天池淘宝数据可视化\\user_action.csv")
# 观察数据
data_user.head(20)
# print('整体数据的大小为',len(data_user))
# print('数据的集中用户的数量是',len(set(data_user['user_id'])))
# print('数据集中的商品数量',len(set(data_user['item_id'])))
# print('数据的商品类别数量',len(set(data_user['item_category'])))
# 数据集包含了10000个用户在1个月内的1200多万条的购物行为数据，商品总数量2876947，类别8916
# 数据处理
# 查看数据的缺失情况
data_user.isnull().sum()
# 没有空字段
# 处理时间，分割天和小时
data_user['date'] = data_user['time'].map(lambda x: x.split(' ')[0])
data_user['hour'] = data_user['time'].map(lambda x: x.split(' ')[1])
data_user.head()
# 查看数据类型，完成必要的类型转化
data_user.dtypes
data_user['user_id'] = data_user['user_id'].astype('object')
data_user['item_id'] = data_user['item_id'].astype('object')
data_user['item_category'] = data_user['item_category'].astype('object')
data_user['date'] = pd.to_datetime(data_user['date'])  # df[''date]数据类型为“object”，通过pd.to_datetime将该列数据转换为时间类型，即datetime。
data_user['hour'] = data_user['hour'].astype('int64')
# 转变完后的数据类型
data_user.dtypes
# 数据分析和数据可视化
# 1，流量分析 访问量(PV)：全名为P*age *View, 基于用户每次对淘宝页面的刷新次数，用户每刷新一次页面或者打开新的页面就记录就算一次访问。
# 独立访问量(UV)：全名为U*nique *Visitor，一个用户若多次访问淘宝只记录一次，熟悉SQL的小伙伴会知道，本质上是unique操作。
# 计算pv，uv 每天
# df.groupby('key1')['data1']对data1按key1进行聚集，聚集后得到的结果需要以数学计算类方式显示
pv_daily = data_user.groupby('date')['user_id'].count()
pv_daily = pv_daily.reset_index()
pv_daily = pv_daily.rename(columns={'user_id': 'pv_daily'})
uv_daily = data_user.groupby('date')['user_id'].apply(lambda x: len(x.unique()))
uv_daily = uv_daily.reset_index()
uv_daily = uv_daily.rename(columns={'user_id': 'uv_daily'})
# 可视化，使用面向对象的方法，先产生一个Axes对象，再对此对象进行操作，实现绘图
# Figure：画布，Axes容器；
# Axes：坐标系，绘图的区域，绘图总是在坐标系上进行；
# Axis：坐标轴，x轴或y轴。
fig, axes = plt.subplots(2, 1, sharex=True)  # 2行一列的排列图
pv_daily.plot(x='date', y='pv_daily', ax=axes[0], colormap='cividis')
uv_daily.plot(x='date', y='uv_daily', ax=axes[1], colormap='RdGy')
axes[0].set_title('pv_daily')
axes[1].set_title('uv_daily')
# 小时的pv uv的数据分析
# 从上方了解到了双十二的总体流量出现明显峰值，分析双十二的数据
data_user_1212 = data_user.loc[data_user['date'] == '2014-12-12']
print(data_user_1212.dtypes)
# 计算每小时的PV双十二
pv_hour_1212 = data_user_1212.groupby('hour')['user_id'].count().reset_index().rename(
    columns={'user_id': '1212_pv_hour'})
uv_hour_1212 = data_user_1212.groupby('hour')['user_id'].apply(lambda x: len(x.unique())).reset_index().rename(
    columns={'user_id': '1212_uv_hour'})
# 可视化双十二
fig, axes = plt.subplots(2, 1, sharex=True)
pv_hour_1212.plot(x='hour', y='1212_pv_hour', ax=axes[0], colormap='cividis')
uv_hour_1212.plot(x='hour', y='1212_uv_hour', ax=axes[1], colormap='RdGy')
axes[0].set_title('pv_hour_1212')
axes[1].set_title('uv_hour_1212')
# 不同用户的行为流量分析
# 点击、收藏、加购物车、支付四种行为，分别用数字1、2、3、4表示
pv_behavior = data_user.groupby(['behavior_type', 'hour'])['user_id'].count()
pv_behavior = pv_behavior.reset_index()
pv_behavior = pv_behavior.rename(columns={'user_id': 'pv_behavior'})
# 可视化
fig, axes = plt.subplots()
axes = sns.lineplot(x='hour', y='pv_behavior', hue='behavior_type', data=pv_behavior)
# 由于浏览行为1占比太大，去掉重新观察
fig, axes = plt.subplots()
axes = sns.lineplot(x='hour', y='pv_behavior', hue='behavior_type', data=pv_behavior[pv_behavior.behavior_type != 1])
# 转化率的分析
# 分析浏览-收藏/加购-购买的链路的转化漏斗模型
behavior_type = data_user.groupby(['behavior_type'])['user-id'].count()
# 定义价格变量，进行除法
click_num, fav_num, add_num, pay_num = behavior_type[1], behavior_type[2], behavior_type[3], behavior_type[4]
fav_add_num = fav_num + add_num
print('加购/收藏转化率：', 100 * fav_add_num / click_num)
print('点击 到 购买转化率: ', 100 * pay_num / click_num)
print('加购/收藏 到 购买转化率: ', 100 * pay_num / fav_add_num)
# 在和双十二的数据进行比较

# 用户价值分析,用户价值RFM分析模型?
# 项目中我们还是从实际问题出发，站在用户购买行为的角度来探索用户价值，购买频次
data_user_buy = data_user[data_user.behavior_type==4].groupby('user_id')['behavior_type'].count()\

