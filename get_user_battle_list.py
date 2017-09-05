# coding:utf-8

# 使用之前需要先安装phantomjs

import time
import requests
import json
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

reload(sys)
sys.setdefaultencoding("utf-8")


if len(sys.argv) < 2:
    print "Usage: " + sys.argv[0] + " QQ号 密码"
    sys.exit(1)

QQ = sys.argv[1]
PASSWORD = sys.argv[2]

# 设置浏览器标识
DCAP = dict(DesiredCapabilities.PHANTOMJS)
DCAP["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 \
(KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4"
)

# 启动浏览器并设置等待超时时间
browser = webdriver.PhantomJS(
    executable_path='C:\\phantomjs\\bin\\phantomjs.exe',
    desired_capabilities=DCAP)
browser.implicitly_wait(10)

# 获取登录面
browser.get('https://ui.ptlogin2.qq.com/cgi-bin/login?style=8&appid=523005422&\
s_url=https%3A%2F%2Faq.qq.com%2Fcn2%2Fmobile_index&low_login=0&hln_css=\
https%3A%2F%2Faq.qq.com%2Fv2%2Fimages%2Flogo_new.png&hln_custompage=1')

loginButtonLocator = (By.ID, 'go')
try:
    WebDriverWait(browser, 10, 0.5).until(
        EC.visibility_of_element_located(loginButtonLocator))
except Exception:
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
idTextField.send_keys(QQ)
passwordTextField.send_keys(PASSWORD)
# browser.save_screenshot('loginform.png')
loginButton.click()

# 获取cookie
usernameLocator = (By.CLASS_NAME, 'banner_wording')
try:
    WebDriverWait(browser, 10, 0.5).until(
        EC.visibility_of_element_located(usernameLocator))
except Exception:
    browser.close()
    sys.exit(-1)

browser.get('http://game.qq.com/')
qqCookie = browser.get_cookies()
browser.save_screenshot('index.png')
print "跳转首页,获取cookie", time.time()
print qqCookie

# 关闭浏览器
browser.close()

# 测试访问tgp接口
url = 'http://api.pallas.tgp.qq.com/core/get_player_battle_list'
p = '[[3,{"area_id":1,"qquin":"408183013","bt_num":"0","bt_list":[],\
"champion_id":0,"offset":8,"limit":8,"mvp_flag":-1}]]'

headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) \
AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d \
Safari/600.1.4'}
s = requests.Session()
for cookie in qqCookie:
    s.cookies.set(cookie['name'], cookie['value'])

resp = s.get(url, headers=headers, params={'q': p})
code = resp.status_code
data = resp.content
jsonData = json.loads(data)
# print resp.url
print json.dumps(jsonData, ensure_ascii=False, indent=4, sort_keys=True)
