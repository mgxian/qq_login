#coding:utf8

# 使用之前需要先安装chromedriver

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

if len(sys.argv) <2:
    print "Usage: "+ sys.argv[0] + "QQ号 密码"
    sys.exit(1)

qq = sys.argv[1]
password = sys.argv[2]

# 启动浏览器并设置等待超时时间
browser = webdriver.Chrome('D:\chromedriver.exe')
browser.implicitly_wait(10)

# 获取登录面
browser.get('https://ui.ptlogin2.qq.com/cgi-bin/login?style=8&appid=523005422&s_url=https%3A%2F%2Faq.qq.com%2Fcn2%2Fmobile_index&low_login=0&hln_css=https%3A%2F%2Faq.qq.com%2Fv2%2Fimages%2Flogo_new.png&hln_custompage=1')

loginButtonLocator = (By.ID, 'go')
try:
    WebDriverWait(browser, 10, 0.5).until(EC.visibility_of_element_located(loginButtonLocator))
except:
    browser.close()
    sys.exit(-1)

print "登录按钮加载成功：", time.time()

# 获取用户名密码和登录元素
idTextField = browser.find_element_by_id('u')
passwordTextField = browser.find_element_by_id('p')
loginButton = browser.find_element_by_id('go')

# 输入用户名密码并点击登录
idTextField.clear()
passwordTextField.clear()
idTextField.send_keys(qq)
passwordTextField.send_keys(password)
loginButton.click()

# 获取cookie
usernameLocator = (By.CLASS_NAME, 'banner_wording')
try:
    WebDriverWait(browser, 10, 0.5).until(EC.visibility_of_element_located(usernameLocator))
except:
    browser.close()
    sys.exit(-1)
qqCookie = browser.get_cookies()
print "跳转首页,获取cookie", time.time()

# 测试访问tgp接口
browser.get('http://api.pallas.tgp.qq.com/core/get_user_hot_info?area_id=1&qquin=U9943308937238559946')

# 关闭浏览器
time.sleep(2)
browser.close()