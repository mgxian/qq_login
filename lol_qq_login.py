#coding:utf8

# 使用之前需要先安装phantomjs

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import requests
import random
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

if len(sys.argv) <2:
    print "Usage: "+ sys.argv[0] + "QQ号 密码"
    sys.exit(1)

qq = sys.argv[1]
password = sys.argv[2]

# 设置浏览器标识
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
)

# 启动浏览器并设置等待超时时间
browser = webdriver.PhantomJS(executable_path='C:\\phantomjs\\bin\\phantomjs.exe', desired_capabilities=dcap)
browser.implicitly_wait(10)

# 获取LOL官网页面并点出登录
browser.get('http://lol.qq.com/')

print "获取lol.qq.com：", time.time()
loginButtonLocator = (By.XPATH, '//*[@id="J_topUser"]/div[2]/div[2]/div[1]/em')
try:
    WebDriverWait(browser, 10, 0.5).until(EC.visibility_of_element_located(loginButtonLocator))
except:
    browser.close()
    sys.exit(-1)

print "登录链接已加载：", time.time()
loginButton = browser.find_element_by_xpath('//*[@id="J_topUser"]/div[2]/div[2]/div[1]/em')
loginButton.click()

# 切换到登录的iframe
try:
    WebDriverWait(browser, 10, 0.5).until(EC.frame_to_be_available_and_switch_to_it(0))
except:
    browser.close()
    sys.exit(-1)

print "切换到QQ登录的iframe：", time.time()
#browser.save_screenshot('iframe.png')
#browser.switch_to.frame(0)

# 点击使用QQ号登录
userPasswordLoginButtonLocator = (By.ID, 'switcher_plogin')
try:
    WebDriverWait(browser, 10, 0.5).until(EC.visibility_of_element_located(userPasswordLoginButtonLocator))
except:
    browser.close()
    sys.exit(-1)

userPasswordLoginButton = browser.find_element_by_css_selector('#switcher_plogin')
userPasswordLoginButton.click()

# 获取用户名密码和登录元素
loginButtonLocator = (By.ID, 'login_button')
try:
    WebDriverWait(browser, 10, 0.5).until(EC.visibility_of_element_located(loginButtonLocator))
except:
    browser.close()
    sys.exit(-1)

print "点击使用QQ登录成功：", time.time()
idTextField = browser.find_element_by_id('u')
passwordTextField = browser.find_element_by_id('p')
loginButton = browser.find_element_by_id('login_button')

# 输入用户名密码并点击登录
idTextField.clear()
passwordTextField.clear()
idTextField.send_keys(qq)
passwordTextField.send_keys(password)
#browser.save_screenshot('login_qq.png')
loginButton.click()

# 获取cookie
logoutTextLocator = (By.XPATH, '//*[@id="J_topUser"]/div[3]/div[2]/div[1]/a[2]')
try:
    WebDriverWait(browser, 10, 0.5).until(EC.visibility_of_element_located(logoutTextLocator))
except:
    browser.close()
    sys.exit(-1)
print "登录成功,跳转首页,获取cookie：", time.time()
qqCookie = browser.get_cookies()
#print qqCookie

# 关闭浏览器
browser.save_screenshot('lol_qq.png')
browser.close()

# 测试访问tgp接口
url = 'http://api.pallas.tgp.qq.com/core/get_user_hot_info?area_id=1&qquin=U9943308937238559946'
s = requests.Session()
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
for cookie in qqCookie:
    s.cookies.set(cookie['name'], cookie['value'])

resp = s.get(url, headers=headers)
code = resp.status_code
data = resp.content
jsonData = json.loads(data)
print json.dumps(jsonData, ensure_ascii=False, indent=4, sort_keys=True)
