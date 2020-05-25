# 读库
from math import *
content = []
with open('test1.txt', encoding="utf-8") as fp:
    content = fp.readlines()

print(content)

# 写入hash
data = {}

# {'1': {'华为mate60': '5.0', '小米10': '3.0', 'Oppo': '4.0'}, '2': {'小米10': '4.0', 'iphone11': '4.5'}, '3': {'vivo': '4.0'}}

for line in content:

    line = line.replace("\n", "").split(",")

    if not line[0] in data.keys():
        data[line[0]] = {line[1]: line[2]}
    else:
        data[line[0]][line[1]] = line[2]

# 计算相似值
def Euclid(user1, user2):
    # 取出两位用户购买过的手机和评分
    user1_data = data[user1]
    user2_data = data[user2]
    distance = 0
    # 找到两位用户都购买过的手机，并计算欧式距离
    for key in user1_data.keys():
        if key in user2_data.keys():
            distance += pow(float(user1_data[key])-float(user2_data[key]), 2)
            print(distance)

    return 1 / (1+sqrt(distance))  # 这里返回值越小，相似度越大


print(Euclid("1", "1"))
