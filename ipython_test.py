from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
"Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4"
)


browser = webdriver.PhantomJS(executable_path='C:\\phantomjs\\bin\\phantomjs.exe', desired_capabilities=dcap)
browser.get('https://ui.ptlogin2.qq.com/cgi-bin/login?style=8&appid=523005422&s_url=https%3A%2F%2Faq.qq.com%2Fcn2%2Fmobile_index&low_login=0&hln_css=https%3A%2F%2Faq.qq.com%2Fv2%2Fimages%2Flogo_new.png&hln_custompage=1')
time.sleep(1)

idTextField = browser.find_element_by_id('u')
passwordTextField = browser.find_element_by_id('p')
loginButton = browser.find_element_by_id('go')