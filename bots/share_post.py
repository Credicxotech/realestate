from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from .extension import proxies

import random
import sys 
import os
from logging import *
import json
import configparser
from datetime import datetime,date
import requests

import sentry_sdk

# takings arguments
xs_time = sys.argv[1]
c_user_time = sys.argv[2]
xs = sys.argv[3]
c_user = sys.argv[4]
post_id = sys.argv[5]
password = sys.argv[6]
uuid = sys.argv[7]
ip = sys.argv[8]
port = sys.argv[9]

#snetry-sdk work
sentry_sdk.init("https://d61c7a6830b44dd9ae627e01d2c6d695@o425995.ingest.sentry.io/6138760", traces_sample_rate=1.0)

#starting the flow, recording the time
start_flow = datetime.now().isoformat(' ','seconds')

# reading config file and using attributes
config = configparser.ConfigParser()
config.read(r"./config_files/config_share_post.ini")
time_sleep = config['time']
att1 = time_sleep['att1']
att2 = time_sleep['att2']
print("### Att1={}, Att2={}".format(att1,att2))
callback_url = config['callback_url']
cb_url = callback_url['cb_url']
print(cb_url)

# making directory as per dates
p_dir= './log_files/share_post'
directory = "LOG-{}".format(date.today())
path = os.path.join(p_dir,directory)
try:
    os.mkdir(path)
except:
    pass

# creaing log file using uuid and writing onto them
path_logging = './log_files/share_post/LOG-{}/{}.log'.format(date.today(),uuid)
log_format = '%(lineno)d -- %(asctime)s -- %(levelname)s -- %(message)s'
basicConfig(filename=path_logging , level=DEBUG, filemode='w', format=log_format)

# verifying password
try:   
    if password != '12345asdf':
        critical("Entered Password is Wrong")
        sleep(3)  
        data_ = {"Error":"Wrong password"}
        r = requests.post(cb_url, json=data_)
        info("Wrong password")
        print("Wrong password")
        print("Data is",data_,"\n")  
except: 
    pass

   

# initiating callback json
data = {}
with open(r"./callback_json/share_post_callback.json",'w') as cb:
    json.dump(data,cb)

with open(r"./callback_json/share_post_callback.json",'w') as cb:
    data["flow"] = {
        "uuid": uuid,
        "start_time": start_flow,
        "end_time": "",
        "used_ip": ip,
        "error": "none"
        }
    json.dump(data,cb)

print("### Api Call , Starting task.")
info("API Call , Starting task. \n")
with open(r"./callback_json/share_post_callback.json",'w') as cb:
    data["trace"]={"steps":[
                { 
                'start_time':datetime.now().isoformat(' ','seconds'),
                'end_time': datetime.now().isoformat(' ','seconds'),  
                'action' : 'API Call , Starting task.',
                'status' : True
                }
                ]} 
    json.dump(data,cb)
sleep(3)

username = 'blubee'
password = '13467913'
endpoint = 'il.smartproxy.com'
port = port
proxies_extension = proxies(username, password, endpoint, port)

def get_browser():
    # HEADLESS = False
    HEADLESS = True
    ("Initiating Browser")
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
    chrome_options.add_extension(proxies_extension)
    browser = webdriver.Chrome(executable_path= ChromeDriverManager().install() ,options=chrome_options)
    # browser = webdriver.Chrome(executable_path= r"C:\Program Files (x86)\chromedriver.exe" ,options=chrome_options)
    return browser

def post_the_post(browser): 
    # get FB home page 
    try:
        browser.get('https://www.facebook.com/')
        print("### On Facebook Page....###")
        info("On Facebook Page.")
        data['trace']['steps'].append({
                'start_time':datetime.now().isoformat(' ','seconds'),
                'end_time': datetime.now().isoformat(' ','seconds'), 
                'action' : 'Open FB home page',
                'status' : True
        })
    except:
        end_flow = datetime.now().isoformat(' ','seconds')
        print("### Didn't get the url, may be IP port is not working")
        warning("### Didn't get the url, may be IP port is not working")
        with open(r"./callback_json/share_post_callback.json",'w') as cb:
            data['trace']['steps'].append({
                'start_time':datetime.now().isoformat(' ','seconds'),
                'end_time': datetime.now().isoformat(' ','seconds'), 
                'action' : 'Open FB home page',
                'status' : False
                                         })
            data.update({"flow": {
                        "uuid": uuid,
                        "start_time": start_flow,
                        "end_time": end_flow,
                        "used_ip": ip,
                        "error": "1001 - Din't get Facebook URL, may be proxy not working"
                        }})
            json.dump(data,cb)
        browser.quit()
        cb = open(r"./callback_json/share_post_callback.json",'r') 
        send_data = cb.read()
        r = requests.post(cb_url, json=send_data)
        print("Callback given with error description")
        exit()
    

    info("Sleeping for 10 secs")
    sleep(10)

    print("### Adding Cookies ### \n")
    info("Adding Cookies ")
    
    sleep(2)
   
    xs_cuser=[
                {'domain': '.facebook.com', 'expiry': int(xs_time), 'httpOnly': True, 'name': 'xs', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': xs},
                {'domain': '.facebook.com', 'expiry': int(c_user_time), 'httpOnly': False, 'name': 'c_user', 'path': '/', 'sameSite': 'None', 'secure': True, 'value': c_user}
                 ]
                 
    # render cookies
    try:
        cookie_list = xs_cuser
    except:
        end_flow = datetime.now().isoformat(' ','seconds')
        critical("Didn't get cookies, might have in a wrong way.")
        with open(r"./callback_json/share_post_callback.json",'w') as cb:
            data['trace']['steps'].append({
                'start_time':datetime.now().isoformat(' ','seconds'),
                'end_time': datetime.now().isoformat(' ','seconds'), 
                'action' : '703-Render cookies',
                'status' : False
            })
            data.update({"flow": {
                    "uuid": uuid,
                    "start_time": start_flow,
                    "end_time": end_flow,
                    "used_ip": ip,
                    "error": "Render Cookies failed"
                    }})
            json.dump(data,cb) 
        browser.quit() 
        cb = open(r"./callback_json/share_post_callback.json",'r') 
        send_data = cb.read()
        r = requests.post(cb_url, json=send_data)
        print("Callback given with error description")  
        exit()

    for cookie in cookie_list:
        print(cookie)
    
    # add cookies to browser
    try:
        for cookie in cookie_list:
            browser.add_cookie(cookie)
            print("### Succesfully added cookie ### ")  
            info("Succesfully added cookie ") 
        data['trace']['steps'].append(
            {'start_time':datetime.now().isoformat(' ','seconds'),
              'end_time': datetime.now().isoformat(' ','seconds'), 
              'action' : 'Adding cookies',
            'status' : True
            })      
    except:    
        end_flow = datetime.now().isoformat(' ','seconds')
        print("### Could not add cookies , login failed..... ###") 
        critical("Could not add cookies , login failed.....")
        with open(r"./callback_json/share_post_callback.json",'w') as cb:
            json.dump(data,cb)
        data['trace']['steps'].append({
              'start_time':datetime.now().isoformat(' ','seconds'),
              'end_time': datetime.now().isoformat(' ','seconds'), 
              'action' : 'Adding cookies',
              'status' : False })
        data.update({"flow": {
                "uuid": uuid,
                "start_time": start_flow,
                "end_time": end_flow,
                "used_ip": ip,
                "error": "702 - Adding cookies failed"
                }}) 
        with open(r"./callback_json/share_post_callback.json",'w') as cb:
            json.dump(data,cb)
        browser.quit()
        cb = open(r"./callback_json/share_post_callback.json",'r') 
        send_data = cb.read()
        r = requests.post(cb_url, json=send_data)
        print("Callback given with error description")
        exit()

    info("All cookies added succesfully...")
    sleep(1)
    info("Login was successfull")
    data['trace']['steps'].append({
              'start_time':datetime.now().isoformat(' ','seconds'),
              'end_time': datetime.now().isoformat(' ','seconds'), 
              'action' : 'Login',
              'status' : True})

    # refresh page
    try:
        info("Refreshing Page")
        print("Browser Refreshing")
        browser.refresh()
        sleep(8)
    except:
        end_flow = datetime.now().isoformat(' ','seconds')
        warning("Could not refresh browser")
        data.update({"flow": {
                "uuid": uuid,
                "start_time": start_flow,
                "end_time": end_flow,
                "used_ip": ip,
                "error": "Browser Refresh failed"
                }}) 
        with open(r"./callback_json/share_post_callback.json",'w') as cb:
            json.dump(data,cb)
        browser.quit()
        cb = open(r"./callback_json/share_post_callback.json",'r') 
        send_data = cb.read()
        r = requests.post(cb_url, json=send_data)
        print("Callback given with error description")
        exit()

    info("Sleeping for 8 secs")
    print("Sleeping for 8 secs")
    sleep(8)

    # get post URL
    try:  
        start_time_first = datetime.now().isoformat(' ','seconds')
        url = 'https://www.facebook.com/{}'.format(post_id)      
        browser.get(url)
        sleep(3)
        print("### Got the Post ID...###")
        info("Got the Post ID")
        data['trace']['steps'].append({
              'start_time':start_time_first,
              'end_time': datetime.now().isoformat(' ','seconds'), 
              'action' : 'Open Post',
              'status' : True})
    except:
        end_flow = datetime.now().isoformat(' ','seconds')
        error("Couldn't fetch url from Post ID")  
        critical("Couldn't fetch url from Post ID") 
        browser.quit() 
        data['trace']['steps'].append({
              'start_time':start_time_first,
              'end_time':datetime.now().isoformat(' ','seconds') , 
              'action' : 'Open post.',
              'status' : False })
        data.update({"flow": {
                "uuid": uuid,
                "start_time": start_flow,
                "end_time": end_flow,
                "used_ip": ip,
                "error": "404-Post page not found."
                }})
        with open(r"./callback_json/share_post_callback.json",'w') as cb:
            json.dump(data,cb) 
        browser.quit()
        cb = open(r"./callback_json/share_post_callback.json",'r') 
        send_data = cb.read()
        r = requests.post(cb_url, json=send_data)
        print("Callback given with error description")
        exit()
        
    j = random.randint(3,8)
    print("*** Sleeping for {} secs ***".format(j))
    info("Sleeping for {} secs ".format(j))
    sleep(j)
    
    # find share button
    try:
        share = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH,"//span[contains(text(),'Share')]")))
        print("### Share_button found ###")
        info("Share_button found ")
        data['trace']['steps'].append({
              'start_time':start_time_first,
              'end_time': datetime.now().isoformat(' ','seconds'), 
              'action' : 'Find share button',
              'status' : True })
        sleep(4)
    except:
        end_flow = datetime.now().isoformat(' ','seconds')
        warning("Couldn't find share button")
        data['trace']['steps'].append({
              'start_time':start_time_first,
              'end_time': datetime.now().isoformat(' ','seconds'), 
              'action' : 'Find share button',
              'status' : False })
        data.update({"flow": {
                "uuid": uuid,
                "start_time": start_flow,
                "end_time": end_flow,
                "used_ip": ip,
                "error": "601-Find Share button failed"
                }}) 
        with open(r"./callback_json/share_post_callback.json",'w') as cb:
            json.dump(data,cb)
        browser.quit()
        cb = open(r"./callback_json/share_post_callback.json",'r') 
        send_data = cb.read()
        r = requests.post(cb_url, json=send_data)
        print("Callback given with error description")
        exit()

    # click share button
    try:    
        browser.execute_script("arguments[0].click();", WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Share')]"))))
        # share.click()
        print("### Share_button clicked ###")
        info("Share_button clicked ")
        data['trace']['steps'].append({
              'start_time':start_time_first,
              'end_time': datetime.now().isoformat(' ','seconds'), 
              'action' : 'Click share button',
              'status' : True })
         
        sleep(5)
    except:
        end_flow = datetime.now().isoformat(' ','seconds')
        warning("Couldn't click share button") 
        print("Couldn't click share button") 
        data['trace']['steps'].append({
              'start_time':start_time_first,
              'end_time': datetime.now().isoformat(' ','seconds'), 
              'action' : 'Click share button',
              'status' : False })
        data.update({"flow": {
                "uuid": uuid,
                "start_time": start_flow,
                "end_time": end_flow,
                "used_ip": ip,
                "error": "602-Click share button failed"
                }})
        with open(r"./callback_json/share_post_callback.json",'w') as cb:
            json.dump(data,cb)
        browser.quit() 
        cb = open(r"./callback_json/share_post_callback.json",'r') 
        send_data = cb.read()
        r = requests.post(cb_url, json=send_data)
        print("Callback given with error description")  
        exit()
    
    # find share to group button
    try:
        share_to_grp = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH,"//span[contains(text(),'Share to a group')]")))
        info("Share_to_a_Group button found")
        print("Share_to_a_Group button found")
        data['trace']['steps'].append({
              'start_time':start_time_first,
              'end_time': datetime.now().isoformat(' ','seconds'), 
              'action' : 'Find Share_to_a_group button',
              'status' : True })
    except:
        info("Share_to_a_Group button not found")
        print("Share_to_a_Group button not found")
        end_flow = datetime.now().isoformat(' ','seconds')
        data['trace']['steps'].append({
              'start_time':start_time_first,
              'end_time': datetime.now().isoformat(' ','seconds'), 
              'action' : 'Click Share_to_a_group button',
              'status' : False })
        data.update({"flow": {
                "uuid": uuid,
                "start_time": start_flow,
                "end_time": end_flow,
                "used_ip": ip,
                "error": "601-Share_to_a_group button not found "
                }})
        with open(r"./callback_json/share_post_callback.json",'w') as cb:
            json.dump(data,cb)
        browser.quit()
        cb = open(r"./callback_json/share_post_callback.json",'r') 
        send_data = cb.read()
        r = requests.post(cb_url, json=send_data)
        print("Callback given with error description")
        exit()

    # click share to grp button 
    try:
        sleep(2)
        share_to_grp.click()
        print("### Share_to_group_button clicked###")
        info("Share_to_group_button clicked")
        data['trace']['steps'].append({
              'start_time':start_time_first,
              'end_time': datetime.now().isoformat(' ','seconds'), 
              'action' : 'Click Share_to_a_group button',
              'status' : True })
        sleep(random.randint(2,5)) 
    except:
        end_flow = datetime.now().isoformat(' ','seconds')
        error("Couldn't click the share_to_a_group button")
        critical("Might not have logged in with cookies")
        print("Share_to_a_group button not clicked")
        data['trace']['steps'].append({
              'start_time':start_time_first,
              'end_time': datetime.now().isoformat(' ','seconds'), 
              'action' : 'Click Share_to_a_group button',
              'status' : False })
        data.update({"flow": {
                "uuid": uuid,
                "start_time": start_flow,
                "end_time": end_flow,
                "used_ip": ip,
                "error": "602/701-Share_to_a_group button not clicked , May be Wrong cookies , could not login"
                }})
        with open(r"./callback_json/share_post_callback.json",'w') as cb:
            json.dump(data,cb)
        browser.quit()
        cb = open(r"./callback_json/share_post_callback.json",'r') 
        send_data = cb.read()
        r = requests.post(cb_url, json=send_data)
        print("Callback given with error description") 
        exit()     
    
    # find group list
    try:
        which_groups_box = browser.find_element_by_xpath("//div[contains(@class,'b20td4e0 muag1w35')]")
        sleep(3)
        which_groups = which_groups_box.find_elements_by_xpath("//div[contains(@class,'oajrlxb2 gs1a9yip g5ia77u1 mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv nhd2j8a9 mg4g778l pfnyh3mw p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x tgvbjcpo hpfvmrgz jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h esuyzwwr f1sip0of du4w35lb btwxx1t3 abiwlrkh p8dawk7l lzcic4wl ue3kfks5 pw54ja7n uo3d90p7 l82x9zwi a8c37x1j')]")
        sleep(4)
        data['trace']['steps'].append({
              'start_time':start_time_first,
              'end_time': datetime.now().isoformat(' ','seconds'), 
              'action' : 'Find Group List',
              'status' : True })
    except:
        end_flow = datetime.now().isoformat(' ','seconds')
        warning("Couldn't get the list of groups,Login with cookies failed or Wrong cookies ")
        print("Couldn't get the list of groups,Login with cookies failed or Wrong cookies ")
        data['trace']['steps'].append({
              'start_time':start_time_first,
              'end_time': datetime.now().isoformat(' ','seconds'), 
              'action' : 'Find Group List',
              'status' : False })
        data.update({"flow": {
                "uuid": uuid,
                "start_time": start_flow,
                "end_time": end_flow,
                "used_ip": ip,
                "error": "601/701-Group list not found, Login with cookies failed or Wrong cookies"
                }})
        with open(r"./callback_json/share_post_callback.json",'w') as cb:
            json.dump(data,cb)
        browser.quit()
        cb = open(r"./callback_json/share_post_callback.json",'r') 
        send_data = cb.read()
        r = requests.post(cb_url, json=send_data)
        print("Callback given with error description")
        exit()

    sleep(5)

    # print length before scrolling
    try:
        print("Length before scrolling is {}".format(len(which_groups)))
    except:
        print("Group list not found, Login with cookies failed or Wrong cookies")
        info("Group list not found, Login with cookies failed or Wrong cookies")
        data.update({"flow": {
                "uuid": uuid,
                "start_time": start_flow,
                "end_time": end_flow,
                "used_ip": ip,
                "error": "601/701-Group list not found, Login with cookies failed or Wrong cookies"
                }})
        with open(r"./callback_json/share_post_callback.json",'w') as cb:
            json.dump(data,cb)
        cb = open(r"./callback_json/share_post_callback.json",'r') 
        send_data = cb.read()
        r = requests.post(cb_url, json=send_data)
        print("Callback given with error description")
        exit()
    
    print("### Starting scrolling ###")
    info("Starting scrolling for all groups")
    start_time = datetime.now().isoformat(' ','seconds')
    sleep(2)
    
    # scroll to find all groups
    scroll = int(len(which_groups)/3)
    try:
        for i in range(scroll):
            browser.execute_script("arguments[0].scrollIntoView();", which_groups[-1] )
            sleep(5)
            which_groups = which_groups_box.find_elements_by_xpath("//div[contains(@class,'oajrlxb2 gs1a9yip g5ia77u1 mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv nhd2j8a9 mg4g778l pfnyh3mw p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x tgvbjcpo hpfvmrgz jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h esuyzwwr f1sip0of du4w35lb btwxx1t3 abiwlrkh p8dawk7l lzcic4wl ue3kfks5 pw54ja7n uo3d90p7 l82x9zwi a8c37x1j')]")
    except:
        end_flow = datetime.now().isoformat(' ','seconds')
        end_time2 = datetime.now().isoformat(' ','seconds')
        warning("Couldn't scroll the groups")
        data['trace']['steps'].append({
        'start_time':start_time,
        'end_time': end_time2, 
        'action' : 'Scrolling',
        'status' : False
                    })
        data.update({"flow": {
                "uuid": uuid,
                "start_time": start_flow,
                "end_time": end_flow,
                "used_ip": ip,
                "error": "Scrolling error, unexpected error"
                }})
        with open(r"./callback_json/share_post_callback.json",'w') as cb:
            json.dump(data,cb)
        browser.quit()
        cb = open(r"./callback_json/share_post_callback.json",'r') 
        send_data = cb.read()
        r = requests.post(cb_url, json=send_data)
        print("Callback given with error description")
        exit()
        
    print(" ### Scrolling finished ###")
    print("### Length after scrolling is",len(which_groups))
    info("Scrolling finished")
    info("{} groups found, that are: ".format(len(which_groups)))
    end_time = datetime.now().isoformat(' ','seconds')
    data['trace']['steps'].append({
        'start_time':start_time,
        'end_time': end_time, 
        'action' : 'Scrolling',
        'status' : True
           })
    sleep(5)

    # finding URLs for the group
    grp_urls=[]
    try:
        find_urls = which_groups_box.find_elements_by_xpath("//a[contains(@class,'oajrlxb2 gs1a9yip g5ia77u1 mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv nhd2j8a9 mg4g778l pfnyh3mw p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x tgvbjcpo hpfvmrgz jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h esuyzwwr f1sip0of du4w35lb n00je7tq arfg74bv qs9ysxi8 k77z8yql btwxx1t3 abiwlrkh p8dawk7l lzcic4wl oo9gr5id q9uorilb')]")
        data['trace']['steps'].append({
        'start_time':datetime.now().isoformat(' ','seconds'),
        'end_time': datetime.now().isoformat(' ','seconds'), 
        'action' : 'Find URLs button',
        'status' : True
                    })
        print("Button found to find URLs")
        info("Button found to find URLs")
    except:
        print("Button not found to find URLs") 
        info("Button not found to find URLs")
        end_flow = datetime.now().isoformat(' ','seconds')
        end_time2 = datetime.now().isoformat(' ','seconds')
        data['trace']['steps'].append({
        'start_time':datetime.now().isoformat(' ','seconds'),
        'end_time': datetime.now().isoformat(' ','seconds'), 
        'action' : 'Find URLs button',
        'status' : False
                    })
        data.update({"flow": {
                "uuid": uuid,
                "start_time": start_flow,
                "end_time": end_flow,
                "used_ip": ip,
                "error": "601-Find URLs button not found"
                }})
        with open(r"./callback_json/share_post_callback.json",'w') as cb:
            json.dump(data,cb)
        browser.quit() 
        cb = open(r"./callback_json/share_post_callback.json",'r') 
        send_data = cb.read()
        r = requests.post(cb_url, json=send_data)
        print("Callback given with error description")
        exit()

    sleep(3)  
    # fetch urls 
    try:
        for get_url in find_urls:
            url = get_url.get_attribute('href')
            grp_urls.append(url)
        print("### Group URLs found")
        info("Group URLs found")
        data['trace']['steps'].append({
        'start_time':datetime.now().isoformat(' ','seconds'),
        'end_time': datetime.now().isoformat(' ','seconds'), 
        'action' : "Fetch Groups' URLs ",
        'status' : True
                    })
    except:
        print("### Did not find urls for the groups")
        info("Did not find urls for the groups")
        end_flow = datetime.now().isoformat(' ','seconds')
        data['trace']['steps'].append({
        'start_time':datetime.now().isoformat(' ','seconds'),
        'end_time': datetime.now().isoformat(' ','seconds'), 
        'action' : "Fetch Groups' URLs",
        'status' : False
                    })
        data.update({"flow": {
                "uuid": uuid,
                "start_time": start_flow,
                "end_time": end_flow,
                "used_ip": ip,
                "error": "601/602-Fetching Groups's URLs failed"
                }})
        with open(r"./callback_json/share_post_callback.json",'w') as cb:
            json.dump(data,cb)
        browser.quit()
        cb = open(r"./callback_json/share_post_callback.json",'r') 
        send_data = cb.read()
        r = requests.post(cb_url, json=send_data)
        print("Callback given with error description")
        exit()

    # Dump URLS into a file in case of emergencies
    grp_url_str = '{}'.format(grp_urls)
    with open('./miscellaneus/url_list/url_list.txt','w') as file:
        file.write(grp_url_str)

    # formating group names
    grps=[]
    for i in which_groups:
        grps.append(i.text[:-13])

    # print("### Groups found are")
    info("### Groups found are")
    
    for i in range(len(grps)):
        # print(grps[i])
        info(grps[i])  
    
    # click on first group to share
    try:
        which_groups[0].click()
        print("Clicking First Group ")
        info("Clicking First Group ")
        data['trace']['steps'].append({
        'start_time':start_time ,
        'end_time': datetime.now().isoformat(' ','seconds') , 
        'action' : 'Clicking first group',
        'status' : True})
    except:
        end_flow = datetime.now().isoformat(' ','seconds')
        error("Couldn't click on first group, might get blocked")  
        print("Couldn't click on first group, might get blocked")  
        data['trace']['steps'].append({
        'start_time':start_time,
        'end_time': datetime.now().isoformat(' ','seconds') , 
        'action' : 'Clicking first group',
        'status' : False
        })              
        data.update({"flow": {
                "uuid": uuid,
                "start_time": start_flow,
                "end_time": end_flow,
                "used_ip": ip,
                "error": "602First group not clicked, Might get blocked"
                }})
        with open(r"./callback_json/share_post_callback.json",'w') as cb:
            json.dump(data,cb)
        browser.quit()
        cb = open(r"./callback_json/share_post_callback.json",'r') 
        send_data = cb.read()
        r = requests.post(cb_url, json=send_data)
        print("Callback given with error description")
        exit() 

    d = random.randint(2,5)
    print("***Sleeping for {} secs***".format(d))
    info("Sleeping for {} secs ".format(d))
    sleep(d)

    # find post button
    try:    
        post = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH,"//span[contains(text(),'Post')]")))
        sleep(random.randint(2,6))
        data['trace']['steps'].append({
        'start_time':start_time ,
        'end_time': datetime.now().isoformat(' ','seconds') , 
        'action' : 'Find post button',
        'status' : True
        })
    except:
        info("Couldn't find Post button ")
        print("Couldn't find Post button ")
        end_flow = datetime.now().isoformat(' ','seconds')
        error("Could not share post, may be button not found")
        data['trace']['steps'].append({
        'start_time':start_time ,
        'end_time': datetime.now().isoformat(' ','seconds') , 
        'action' : 'Find post button',
        'status' : False
        })
        data.update({"flow": {
                "uuid": uuid,
                "start_time": start_flow,
                "end_time": end_flow,
                "used_ip": ip,
                "error": "601-Post button not found, might get blocked"
                }})  
        with open(r"./callback_json/share_post_callback.json",'w') as cb:
            json.dump(data,cb)
        browser.quit()
        cb = open(r"./callback_json/share_post_callback.json",'r') 
        send_data = cb.read()
        r = requests.post(cb_url, json=send_data)
        print("Callback given with error description")
        exit()
       
    # click post button  
    try:    
        post.click()
        print("***Post shared to group '{}'***".format(grps[0]))
        info("Post shared to group '{}'".format(grps[0]))
        info("Groups shared in count is 1")
        print("Groups shared in count is 1")

        print("***Sleeping for 4 secs***")
        data['trace']['steps'].append({
        'start_time':start_time,
        'end_time': datetime.now().isoformat(' ','seconds') , 
        'action' : 'Sharing Post',
        'status' : True
        })
        info("Sleeping for 4 secs ")
        sleep(4)
        data["groups"] = {'group':[{
               'name': grps[0],
               'url' : grp_urls[1],
               'info': 'Groups shared in count is 1'
                }]}
        with open(r"./callback_json/share_post_callback.json",'w') as cb:
            json.dump(data,cb)
    except:
        end_flow = datetime.now().isoformat(' ','seconds')
        error("Could not share post, may be blocked by facebook")
        print("Could not share post, may be blocked by facebook")
        data['trace']['steps'].append({
        'start_time':start_time ,
        'end_time': datetime.now().isoformat(' ','seconds') , 
        'action' : 'Sharing post',
        'status' : False
        })
        data.update({"flow": {
                "uuid": uuid,
                "start_time": start_flow,
                "end_time": end_flow,
                "used_ip": ip,
                "error": "602-Sharing post, may be blocked by Facebook"
                }})  
        with open(r"./callback_json/share_post_callback.json",'w') as cb:
            json.dump(data,cb)
        browser.quit()
        cb = open(r"./callback_json/share_post_callback.json",'r') 
        send_data = cb.read()
        r = requests.post(cb_url, json=send_data)
        print("Callback given with error description")
        exit()


    with open(r"./callback_json/share_post_callback.json",'w') as cb:
        json.dump(data,cb)


    # fetch callback data
    try:
        cb = open(r"./callback_json/share_post_callback.json",'r') 
        send_data = cb.read()
        r = requests.post(cb_url, json=send_data)
        print("Callback given with error description")
        info("Callback data fetched")
        print("Callback data fetched")
        print("Data is",send_data,"\n")  
    except:
        info("Callback data not fetched")    
        print("Callback data not fetched")  
        data_ = {"Error":"Data was not fetched, please see callback file"}
        r = requests.post(cb_url, json=data_)
        exit()  
    
    r = random.randint(int(att1),int(att2)) 
    r_min = int(r/60)
    print("***Sleeping for {} mins***".format(r_min))
    info("Sleeping for {} mins".format(r_min))
    data['trace']['steps'].append({
        'start_time':start_time,
        'end_time': datetime.now().isoformat(' ','seconds') , 
        'action' : 'Sleeping for {} mins'.format(r_min),
        'status' : True
        })

    # send data to callback url   
    
    # if r.status_code == 200:
    #     info("Callback sent")
    #     print("Callback sent")
    # else:
    #     info("Callback url responded abnormally")
    #     print("Callback url responded abnormally")

    r_sleep=r_min*60
    # sleep(r_min)
    sleep(r_sleep)
    
    print("### Starting to share in multiple groups......###")
    debug("Starting to share in multiple groups......")
    data['trace']['steps'].append({
        'start_time':datetime.now().isoformat(' ','seconds') ,
        'end_time': datetime.now().isoformat(' ','seconds') , 
        'action' : 'Share in other groups',
        'status' : True
                          })
    sleep(2)
    
    for i in range(1,len(which_groups)):
        sleep(2)
        start_time_sec = datetime.now().isoformat(' ','seconds')
        # find and click button 
        try:
            share = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH,"//span[contains(text(),'Share')]")))
            share.click()
            info("Share button found and clicked")
            data['trace']['steps'].append({
              'start_time':start_time_sec,
              'end_time': datetime.now().isoformat(' ','seconds'), 
              'action' : 'Find and click share button',
              'status' : True
            })
        except:
            end_flow = datetime.now().isoformat(' ','seconds')
            error("Share button not clicked") 
            data['trace']['steps'].append({
              'start_time':start_time_sec,
              'end_time': datetime.now().isoformat(' ','seconds'), 
              'action' : '601/602-Find and click share button',
              'status' : False
            })
            data.update({"flow": {
                "uuid": uuid,
                "start_time": start_flow,
                "end_time": end_flow,
                "used_ip": ip,
                "error": "601/602-Find and click share button failed"
                }})
            with open(r"./callback_json/share_post_callback.json",'w') as cb:
                json.dump(data,cb)
            browser.quit() 
            cb = open(r"./callback_json/share_post_callback.json",'r') 
            send_data = cb.read()
            r = requests.post(cb_url, json=send_data)
            print("Callback given with error description")  
            exit()

        c = random.randint(2,7)
        print("***Sleeping for {} secs***".format(c))
        info("Sleeping for {} secs ".format(c))
        sleep(c)
        
        # share to a group
        try:
            share_to_grp = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH,"//span[contains(text(),'Share to a group')]")))
            share_to_grp.click()
            info("Share_to_a_group button found and clicked")
            data['trace']['steps'].append({
              'start_time':start_time_sec,
              'end_time': datetime.now().isoformat(' ','seconds'), 
              'action' : 'Find and click share_to_group button',
              'status' : True
            })
        except:
            end_flow = datetime.now().isoformat(' ','seconds')
            error("Share_to_group button not found")
            data['trace']['steps'].append({
              'start_time':start_time_sec,
              'end_time': datetime.now().isoformat(' ','seconds'), 
              'action' : 'Find and click share_to_group button',
              'status' : False  
              })
            data.update({"flow": {
                "uuid": uuid,
                "start_time": start_flow,
                "end_time": end_flow,
                "used_ip": ip,
                "error": "601/602-Find and click share_to_group button failed"
                }})
            with open(r"./callback_json/share_post_callback.json",'w') as cb:
                json.dump(data,cb)
            browser.quit()
            cb = open(r"./callback_json/share_post_callback.json",'r') 
            send_data = cb.read()
            r = requests.post(cb_url, json=send_data)
            print("Callback given with error description")
            exit()

        b = random.randint(3,6)
        print("***Sleeping for {} secs***".format(b))
        info("Sleeping for {} secs ".format(b))
        sleep(b)

        # find groups again
        try:        
            which_groups_box = browser.find_element_by_xpath("//div[contains(@class,'b20td4e0 muag1w35')]")
            sleep(5)
            which_groups_sec = which_groups_box.find_elements_by_xpath("//div[contains(@class,'oajrlxb2 gs1a9yip g5ia77u1 mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv nhd2j8a9 mg4g778l pfnyh3mw p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x tgvbjcpo hpfvmrgz jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h esuyzwwr f1sip0of du4w35lb btwxx1t3 abiwlrkh p8dawk7l lzcic4wl ue3kfks5 pw54ja7n uo3d90p7 l82x9zwi a8c37x1j')]")
            info("Finding group list")
            data['trace']['steps'].append({
              'start_time':start_time_sec,
              'end_time': datetime.now().isoformat(' ','seconds'), 
              'action' : 'Find group list',
              'status' : True
            })
        except:
            end_flow = datetime.now().isoformat(' ','seconds')
            error("Groups not found")
            print("Groups not found")
            data['trace']['steps'].append({
                'start_time':start_time_sec,
              'end_time': datetime.now().isoformat(' ','seconds'), 
              'action' : 'Find group list',
              'status' : False
            })
            data.update({"flow": {
                "uuid": uuid,
                "start_time": start_flow,
                "end_time": end_flow,
                "used_ip": ip,
                "error": "601-Find group list failed"
                }})
            with open("./callback_json/share_post_callback.json",'w') as cb:
                json.dump(data,cb)
            browser.quit()
            cb = open(r"./callback_json/share_post_callback.json",'r') 
            send_data = cb.read()
            r = requests.post(cb_url, json=send_data)
            print("Callback given with error description")
            exit()

        a = random.randint(3,6)
        print("***Sleeping for {} secs***".format(a))
        info("Sleeping for {} secs".format(a))
        sleep(a)

        # scroll again
        try:
            start_time_sec = datetime.now().isoformat(' ','seconds')
            info("Starting to scroll") 
            print("Starting to scroll") 
            for j in range(scroll):
                browser.execute_script("arguments[0].scrollIntoView();", which_groups_sec[-1] )
                sleep(4)
                which_groups_sec.extend(browser.find_elements_by_xpath("//div[contains(@class,'oajrlxb2 gs1a9yip g5ia77u1 mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv nhd2j8a9 mg4g778l pfnyh3mw p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x tgvbjcpo hpfvmrgz jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h esuyzwwr f1sip0of du4w35lb btwxx1t3 abiwlrkh p8dawk7l lzcic4wl ue3kfks5 pw54ja7n uo3d90p7 l82x9zwi a8c37x1j')]"))
        except:
            end_flow = datetime.now().isoformat(' ','seconds')
            warning("Couldn't scroll for more groups")
            print("Couldn't scroll for more groups")
            data.update({"flow": {
                "uuid": uuid,
                "start_time": start_flow,
                "end_time": end_flow,
                "used_ip": ip,
                "error": "Scroll to share in other groups"
                }})
            with open(r"./callback_json/share_post_callback.json",'w') as cb:
                json.dump(data,cb)
            browser.quit()
            cb = open(r"./callback_json/share_post_callback.json",'r') 
            send_data = cb.read()
            r = requests.post(cb_url, json=send_data)
            print("Callback given with error description")
            exit()
        
        end_time_sec = datetime.now().isoformat(' ','seconds')
        info("Scrolling finished")
        print("Scrolling finished")   
        data['trace']['steps'].append({
              'start_time':start_time_sec,
              'end_time': end_time_sec, 
              'action' : 'Scrolling finished',
              'status' : False})

 
        # clciking on other groups 
        try:    
            which_groups_sec[i].click()
            data['trace']['steps'].append({
              'start_time':start_time_sec,
              'end_time': datetime.now().isoformat(' ','seconds'), 
              'action' : 'Clicking on group "{}"'.format(grps[i]),
              'status' : True
            })
        except:
            end_flow = datetime.now().isoformat(' ','seconds')
            error("Could not click on group '{}'".format(grps[i]))  
            print("Could not click on group '{}' , might get blocked".format(grps[i]))  
            data['trace']['steps'].append({
                'start_time':start_time_sec,
              'end_time': datetime.now().isoformat(' ','seconds'), 
              'action' : 'Could not click on group "{}"'.format(grps[i]),
              'status' : False
            })
            data.update({"flow": {
                "uuid": uuid,
                "start_time": start_flow,
                "end_time": end_flow,
                "used_ip": ip,
                "error": "602-Could not click on group '{}', might get blocked".format(grps[i])
                }})
            with open(r"./callback_json/share_post_callback.json",'w') as cb:
                json.dump(data,cb)
            browser.quit()
            cb = open(r"./callback_json/share_post_callback.json",'r') 
            send_data = cb.read()
            r = requests.post(cb_url, json=send_data)
            print("Callback given with error description")
            exit()
             
        sleep(3) 
        

        # posting in other groups
        try:   
            post = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH,"//span[contains(text(),'Post')]")))
            post.click()    
            print("### Post shared to group {}".format(grps[i]))
            info("Post shared to group {}".format(grps[i]))
            try:
                data['trace']['steps'].append({
                'start_time':datetime.now().isoformat(' ','seconds'),
                'end_time': datetime.now().isoformat(' ','seconds'), 
                'action' : 'Posting',
                'status' : True
                })
            except:
                print("Posting callback error***")
            try:
                sleep(4)
                data["groups"]['group'].append({
                'name': grps[i],
                'url' : grp_urls[i+1],
                'info': "Groups count is {}".format(i+1)
                })
                info("Groups shared in count is {}").format(i+1)
                print("Group shared in count is {}").format(i+1)
            except:
                print("Group callback error***")
        except:
            end_flow = datetime.now().isoformat(' ','seconds')
            error("Could not share the post")
            data['trace']['steps'].append({
              'start_time':start_time_sec,
              'end_time': datetime.now().isoformat(' ','seconds'), 
              'action' : 'Posting',
              'status' : False
            })
            data.update({"flow": {
                "uuid": uuid,
                "start_time": start_flow,
                "end_time": end_flow,
                "used_ip": ip,
                "error": "601/602-Post not shared, might get blocked"
                }})
            with open(r"./callback_json/share_post_callback.json",'w') as cb:
                json.dump(data,cb)
            browser.quit()
            cb = open(r"./callback_json/share_post_callback.json",'r') 
            send_data = cb.read()
            r = requests.post(cb_url, json=send_data)
            print("Callback given with error description")
            exit()
                                                    

        s = random.randint(int(att1),int(att2))
        s_mins = int(s/60)
        print("***Sleeping for {} mins***".format(s_mins))
        info("***Sleeping for {} mins***".format(s_mins))
        data['trace']['steps'].append({
              'start_time':start_time_sec,
              'end_time': datetime.now().isoformat(' ','seconds'), 
              'action' : 'Sleeping for {} mins'.format(s_mins),
              'status' : True
            })
        
        with open(r"./callback_json/share_post_callback.json",'w') as cb:
            json.dump(data,cb)
    
        # fetch callback data
        try:
            cb = open(r"./callback_json/share_post_callback.json",'r') 
            send_data = json.load(cb)
            r = requests.post(cb_url, data=send_data)
            info("Callback data fetched")
            print("Callback data fetched")
            print("Data is->",send_data,"\n")
        except:
            info("Callback data not fetched")    
            print("Callback data not fetched")  
            data_ = {"Error":"Data was not fetched , could not send data"}
            r = requests.post(cb_url, json=data_) 
            exit()

        # send data to callback url   
        # if r.status_code == 200:
        #     info("Callback sent")
        #     print("Callback sent")
        # else:
        #     info("Callback url responded abnormally")
        #     print("Callback url responded abnormally")
        s_sleep=s_mins*60
        # sleep(s_mins)
        sleep(s_sleep)

end_flow =  datetime.now().isoformat(' ','seconds') 

if __name__ == '__main__':
   
    browser = get_browser()

    browser.get("http://lumtest.com/myip.json")  
    sleep(4)
    print(browser.page_source)
    sleep(3)

    post_the_post(browser)

    print("Task was successfull")
    info("Task was successfull")

    # data.update({"flow": {
    #   "uuid": uuid,
    #   "start_time": start_flow,
    #   "end_time": end_flow,
    #   "used_ip": ip,
    #   "error": "None, Task Done !"
    # }})

    with open(r"./callback_json/share_post_callback.json",'w') as cb:
        json.dump(data,cb) 
    print("Callback file dumped") 
    info("Callback file dumped")
    
# fetch data
    try:
        send_data = {'Message': 'Task was successfull !'}  
        r = requests.post(cb_url, json=send_data)
        info("Task Done message sent")
        print("Task Done message sent")     
    except:
        info("Unexpected error.")
        print("Unexpected error.")

# send data
    # if r.status_code == 200:
    #     info("Callback sent")
    #     print("Callback sent")
    #     print("Response json data is ",r.json(),"\n")
    # else:
    #     info("Callback url responded abnormally")
    #     print("Callback url responded abnormally")
    
    info("Done with the task !!!")
    print("Done with the task !!!")
browser.quit()