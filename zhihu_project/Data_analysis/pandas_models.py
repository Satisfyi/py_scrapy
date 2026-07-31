import pandas as pd
hot = pd.Series(
    [12000, 8500, 23000, 5600, 15000],
    index=[
        "AI发展趋势",
        "Python学习路线",
        "大学生就业",
        "新能源汽车",
        "摄影技巧"
    ],name='个人发展方向'
)


"""查看所有热度数据
查看所有标题
查看 Series 数据类型
查看长度"""
# print(hot)
# print(hot.keys().to_list)
# print(hot.dtype)
# print(hot.count())
"""① 获取“大学生就业”的热度
要求使用：
标签索引
② 获取第3个数据
要求使用：
位置索引
③ 获取热度超过10000的话题"""
# print(hot['大学生就业'])
# print(hot.iloc[2])
# print(hot[hot>10000])
"""把：
Python学习路线
8500
修改为：
10000
然后新增一个：
人工智能学习
18000"""
#
# a=hot['Python学习路线']=10000
# print(hot)
#
# b=hot['人工智能学习']=18000
# print(hot)

'''平均热度
最高热度
最低热度
热度最高的话题名称'''
#
# print(hot.mean())
# print(hot.max())
# print(hot.min())
# print(hot.idxmax())
'''热度超过15000属于：

热门

否则：

普通

请生成一个新的 Series：

结果类似：

AI发展趋势       普通
Python学习路线    普通
大学生就业       热门
新能源汽车       普通
摄影技巧        热门
dtype: object'''
"""所有热度数据增加20%。"""
print(type(hot.values))
print(hot*1.2)




