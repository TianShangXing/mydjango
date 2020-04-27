from selenium import webdriver
import time
from selenium.webdriver import ActionChains
import requests
import base64
import urllib

# 建立浏览器对象
browser = webdriver.Chrome('D:/Download/Google下载/chromedriver_win32/chromedriver.exe')

# 打开网页
browser.get('http://localhost:8080/login')

time.sleep(2)

# 使用标签选择器
inputs = browser.find_elements_by_tag_name('input')
# print(inputs)

# 设置用户名
inputs[1].send_keys('xing')

# 设置密码
inputs[2].send_keys('123')

# 定义滑块选择器
button = browser.find_element_by_class_name('dv_handler')

# 建立动作对象
action = ActionChains(browser)

# 按住拖动  点击后拖动           释放
action.click_and_hold(button).perform()

# 动作释放
action.reset_actions()

# 拖动位置
action.move_by_offset(280, 0).perform()

# 获取总长度
mytext = browser.find_element_by_class_name('dv_text')
# print(mytext.size.get('width'))

# 获取拖动物长度
# print(button.size.get('width'))

time.sleep(2)

# 选取验证码图片
# code_img = browser.find_element_by_class_name('imgcode')

# 只截取指定对象
# code_img.screenshot('md.png')

# 截图
# browser.get_screenshot_as_file('md.png')

browser.close()
