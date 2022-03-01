from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import pickle , sys

username = sys.argv[1]
fb_password = sys.argv[2]

ip='127.0.0.1:22225'

def get_browser():
    HEADLESS = False
    # HEADLESS = True
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
        chrome_options.add_argument("--proxy-server={}".format(ip))
    except:
        print("Proxy error, may be wrong port")
    chrome_options.add_argument("--disable-notifications")
    # browser = webdriver.Chrome(executable_path= r"/usr/bin/chromedriver" ,options=chrome_options)
    browser = webdriver.Chrome(executable_path= r"C:\Program Files (x86)\chromedriver.exe" ,options=chrome_options)
    return browser
        
def get_cookies(browser):
    url = 'https://www.facebook.com/'
    browser.get(url)
    sleep(10)
    browser.find_element_by_xpath('//*[@data-testid="royal_email"]').send_keys(username)
    sleep(5)
    browser.find_element_by_xpath('//*[@data-testid="royal_pass"]').send_keys(fb_password)
    sleep(4)

    browser.find_element_by_xpath('//*[@data-testid="royal_login_button"]').click()
    sleep(1)
            
    pickle.dump(browser.get_cookies(),open(r"./cookies/zachaiosmyer_cooks.pkl","wb"))
    print("Cookies Captured.......")

if __name__ == '__main__':
    browser = get_browser()
    browser.get('http://lumtest.com/myip.json')
    sleep(4)
    get_cookies(browser)