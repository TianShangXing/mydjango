import re

ret = re.match(r"^1[356789]\d{9}$", '15647419067')

if ret:
    print('手机号合法')

else:
    print('手机号有误')


year = 2020
month = 5
day = 21

days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# 判断闰年
def ifleapyear(year):
    return (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0)

if ifleapyear(year):
    days[1] = 29

# 默认天数
count = 0

for i in range(month - 1):
    count += days[i]

count += day

print(count)