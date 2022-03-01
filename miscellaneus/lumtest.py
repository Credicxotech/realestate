from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

ip = IP = '127.0.0.1:24000'

def get_browser():
    # HEADLESS = False
    HEADLESS = True
    sleep(2)
    chrome_options = Options()
    if HEADLESS:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    try:
        chrome_options.add_argument("--proxy-server=%s" % ip)
    except:
        print("Proxy error, may be wrong port")
    chrome_options.add_argument("--disable-notifications")
    browser = webdriver.Chrome(executable_path= r"/usr/bin/chromedriver" ,options=chrome_options)
    # browser = webdriver.Chrome(executable_path= r"C:\Program Files (x86)\chromedriver.exe" ,options=chrome_options)
    return browser

def lumtest(browser):
    browser.get('http://lumtest.com/myip.json')
    sleep(5)
    print(browser.page_source)
    sleep(3)
    
if __name__ == '__main__':
    browser = get_browser()
    lumtest(browser)

browser.quit()    