from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from extension import proxies
import pickle

def get_browser():
    HEADLESS = True
    sleep(2)
    chrome_options = Options()
    if HEADLESS:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-notifications")
    browser = webdriver.Chrome(executable_path= ChromeDriverManager().install() ,options=chrome_options)
    # browser = webdriver.Chrome(executable_path= r"C:\Program Files (x86)\chromedriver.exe" ,options=chrome_options)
    return browser
                    
def get_cookies(browser):
    try:
        url = 'https://www.facebook.com/'
        browser.get(url)
        print("On FB page")
        sleep(10)
    except:
        print("Page Fb not found")

    accept = browser.find_element_by_xpath('//*[@data-cookiebanner="accept_button"]')
    sleep(2)
    accept.click()
    sleep(4)

    name=browser.find_element_by_xpath('//*[@name="email"]')
    sleep(3)
    name.send_keys("zachaiosmyer@outlook.com")
    sleep(5)
                
    print("Email button not found")
                
    passwword = browser.find_element_by_xpath('//*[@name="pass"]')
    sleep(3)
    passwword.send_keys("plandfr52")
    sleep(4)
                
    print("password button not found")
          
    login = browser.find_element_by_xpath('//*[@name="login"]')
    sleep(2)
    login.click()
    sleep(2)
                
    print("Login not clicked")
          
    pickle.dump(browser.get_cookies(),open(r"./cookies/zachaiosmyer_cooks.pkl","wb"))
    print("Cookies Captured.......")

    sleep(5)
    try:
        browser.find_element_by_xpath('//*[@aria-label="Menu"]')
        sleep(3)
    except:
        print("Menu not found")
        

browser = get_browser()
browser.get('http://lumtest.com/myip.json')
sleep(4)
print(browser.page_source)
sleep(3)
get_cookies(browser)
        
cookies = pickle.load(open(r"./cookies/zachaiosmyer_cooks.pkl","rb"))
xs = cookies[0]['value']
xs_time = cookies[0]['expiry']
c_user = cookies[1]['value']
c_user_time = cookies[1]['expiry']
cookies = {
            'XS':xs,
            'XS_TIME':xs_time,
            'CUSER':c_user,
            'CUSER_TIME':c_user_time
                    }
context = {
            'Status':'Successfull',
            'Cookies':cookies
                   }
print(context)