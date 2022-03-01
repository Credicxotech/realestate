from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

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
grp_list_str = sys.argv[5]
password = sys.argv[6]
uuid = sys.argv[7]
ip = sys.argv[8]
user_id = sys.argv[9]

#snetry-sdk work
sentry_sdk.init("https://d61c7a6830b44dd9ae627e01d2c6d695@o425995.ingest.sentry.io/6138760", traces_sample_rate=1.0)

#starting the flow, recording the time
start_flow = datetime.now().isoformat(' ','seconds')

# reading config file and using attributes
config = configparser.ConfigParser()
config.read(r"./config_files/config_join_grp.ini")
time_sleep = config['time']
att1 = time_sleep['att1']
att2 = time_sleep['att2']
print("### Att1={}, Att2={}".format(att1,att2))
callback_url = config['callback_url']
cb_url = callback_url['cb_url']
print(cb_url)

# making directory as per dates
p_dir= './log_files/join_grp'
directory = "LOG-{}".format(date.today())
path = os.path.join(p_dir,directory)
try:
    os.mkdir(path)
except:
    pass

# creating log file using uuid and writing onto them
path_logging = './log_files/join_grp/LOG-{}/{}.log'.format(date.today(),uuid)
log_format = '%(lineno)d -- %(asctime)s -- %(levelname)s -- %(message)s'
basicConfig(filename=path_logging , level=DEBUG, filemode='w', format=log_format)

# check password
try:   
    if password != '12345asdf':
        critical("Entered Password is Wrong")
        print("Entered password is wrong")
        sleep(3) 
        data_ = {"Error":"Wrong password"}
        r = requests.post(cb_url, json=data_)
        info("Wrong password")
        print("Wrong password")
        print("Data is",data_,"\n")  
except: 
    pass    

# initiate callback
data = {}
with open(r"./callback/join_group_callback.json",'w') as cb:
    json.dump(data,cb)

with open(r"./callback/join_group_callback.json",'w') as cb:
    data["flow"] = {
        "uuid": uuid,
        "user_id": user_id,
        "start_time": start_flow,
        "end_time": "",
        "used_ip": ip,
        "error": "none",
        "info": "none"
        }
    json.dump(data,cb)

print("### Api Call , Starting task.")
info("API Call , Starting task. \n")
with open(r"./callback/join_group_callback.json",'w') as cb:
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

def get_browser():
    HEADLESS = True
    info("Initiating Browser")
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
        critical("Proxy error, may be wrong port")
        print("Proxy error, may be wrong port")
    chrome_options.add_argument("--disable-notifications")
    browser = webdriver.Chrome(executable_path= r"/usr/bin/chromedriver" ,options=chrome_options)
    # browser = webdriver.Chrome(executable_path= r"C:\Program Files (x86)\chromedriver.exe" ,options=chrome_options)
    return browser

def post_the_post(browser):  
    # get facebook page
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
        end_flow =  datetime.now().isoformat(' ','seconds') 
        print("### Didn't get the url, may be IP port is not working")
        warning("Didn't get the url, may be IP port is not working")
        data.update({"flow": {
                    "uuid": uuid,
                    "user_id": user_id,
                    "start_time": start_flow,
                    "end_time": end_flow,
                    "used_ip": ip,
                    "error": "1001 - Din't get Facebook URL, may be proxy not working"
                    }})
        with open(r"./callback/join_group_callback.json",'w') as cb:
            json.dump(data,cb)
        browser.quit()
        cb = open(r"./callback_json/join_group_callback.json",'r') 
        send_data = cb.read()
        r = requests.post(cb_url, json=send_data)
        print("Callback given with error description")
        
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
        end_flow =  datetime.now().isoformat(' ','seconds') 
        critical("Didn't get cookies, might have in a wrong way.") 
        with open(r"./callback/join_group_callback.json",'w') as cb:
            data['trace']['steps'].append({
              'start_time':datetime.now().isoformat(' ','seconds'),
              'end_time': datetime.now().isoformat(' ','seconds'), 
              'action' : '703 - Render cookies',
              'status' : False
        })
            data.update({"flow": {
                    "uuid": uuid,
                    "user_id": user_id,
                    "start_time": start_flow,
                    "end_time": end_flow,
                    "used_ip": ip,
                    "error": "703 - Render cookies failed"
                    }})
            json.dump(data,cb)
        browser.quit()   
        cb = open(r"./callback_json/join_group_callback.json",'r') 
        send_data = cb.read()
        r = requests.post(cb_url, json=send_data)
        print("Callback given with error description")

    for cookie in cookie_list:
        print(cookie)

    # adding cookies 
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
        end_flow =  datetime.now().isoformat(' ','seconds') 
        print("### Could not add cookies , login failed..... ###") 
        critical("Could not add cookies , login failed.....")
        with open(r"./callback/join_group_callback.json",'w') as cb:
            data['trace']['steps'].append({
              'start_time':datetime.now().isoformat(' ','seconds'),
              'end_time': datetime.now().isoformat(' ','seconds'), 
              'action' : 'Adding cookies',
              'status' : False })
            data.update({"flow": {
                    "uuid": uuid,
                    "user_id": user_id,
                    "start_time": start_flow,
                    "end_time": end_flow,
                    "used_ip": ip,
                    "error": "702 - Adding cookies failed"
                    }})
            json.dump(data,cb)
        browser.quit()

    info(" All cookies added succesfully...")
    print("### All cookies added succesfully...")
    info(3)
    debug("Login was successfull")
    print("### Login was successfull")
    
    data['trace']['steps'].append({
                'start_time':datetime.now().isoformat(' ','seconds'),
                'end_time': datetime.now().isoformat(' ','seconds'), 
                'action' : 'Login',
                'status' : True})

    # refresh browser
    try:
        info("Refreshing Page")
        print("### Browser Refreshing")
        browser.refresh()
        sleep(3)
    except:
        end_flow =  datetime.now().isoformat(' ','seconds')
        warning("Could not refresh browser")
        with open(r"./callback/join_group_callback.json",'w') as cb:
            data['trace']['steps'].append({
                    'start_time':datetime.now().isoformat(' ','seconds'),
                    'end_time': datetime.now().isoformat(' ','seconds'), 
                    'action' : 'Browser Refresh',
                    'status' : False })
            data.update({"flow": {
                    "uuid": uuid,
                    "user_id": user_id,
                    "start_time": start_flow,
                    "end_time": end_flow,
                    "used_ip": ip,
                    "error": "Browser Refresh failed"
                    }})
            json.dump(data,cb)
        browser.quit()
        cb = open(r"./callback_json/join_group_callback.json",'r') 
        send_data = cb.read()
        r = requests.post(cb_url, json=send_data)
        print("Callback given with error description")

    info("Sleeping for 8 secs")
    sleep(8)

    grp_list = grp_list_str.split(",")

    start_time = datetime.now().isoformat(' ','seconds')
    for grp_id in grp_list:
        browser.get('https://www.facebook.com/')
        sleep(5)
        print("### Some scrolling")
        info("Some scrolling")
        browser.execute_script("window.scrollTo(0,200)")  
        sleep(2)
        browser.execute_script("window.scrollTo(200,400)") 
        sleep(4) 
        browser.execute_script("window.scrollTo(400,700)")  
        sleep(3)

        # get url by id
        try:
            url = 'https://www.facebook.com/groups/{}'.format(grp_id)      
            browser.get(url)
            sleep(3)
            print("### Got the url from Group ID.. id={}".format(grp_id))
            info("### Got the url from Group ID.. id={}".format(grp_id))
            
            data['trace']['steps'].append({
                    'start_time':datetime.now().isoformat(' ','seconds'),
                    'end_time': datetime.now().isoformat(' ','seconds'), 
                    'action' : 'Get group page',
                    'status' : True})
            sleep(2)
            browser.execute_script("window.scrollTo(0,100)")    
            sleep(3)
            browser.execute_script("window.scrollTo(200,300)")    
            sleep(5)
            browser.execute_script("window.scrollTo(300,500)")    
            sleep(4)
        except:
            end_flow =  datetime.now().isoformat(' ','seconds') 
            error("### Couldn't fetch url from Group ID")  
            critical("Couldn't fetch url from Group ID") 
            browser.quit() 
            with open(r"./callback/join_group_callback.json",'w') as cb:
                data['trace']['steps'].append({
                    'start_time':datetime.now().isoformat(' ','seconds'),
                    'end_time':datetime.now().isoformat(' ','seconds') , 
                    'action' : 'Get Group page',
                    'status' : False })
                data.update({"flow": {
                    "uuid": uuid,
                    "user_id": user_id,
                    "start_time": start_flow,
                    "end_time": end_flow,
                    "used_ip": ip,
                    "error": "404 - Group page not found"
                    }})
                json.dump(data,cb)
            browser.quit()
            cb = open(r"./callback_json/join_group_callback.json",'r') 
            send_data = cb.read()
            r = requests.post(cb_url, json=send_data)
            print("Callback given with error description")

        j = random.randint(3,8)
        print("*** Sleeping for {} secs ***".format(j))
        info("Sleeping for {} secs ".format(j))
        sleep(j)

        # find join button
        try:
            join_grp = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH,"//span[contains(text(),'Join Group')]")))
            print("### Join_Group found ###")
            info("Join_Group found ")
            
            data['trace']['steps'].append({
                    'start_time':datetime.now().isoformat(' ','seconds'),
                    'end_time': datetime.now().isoformat(' ','seconds'), 
                    'action' : 'Find Join_Group button',
                    'status' : True })
            sleep(1)
        except:
            end_flow =  datetime.now().isoformat(' ','seconds') 
            print("### Couldn't find Join_Group button")
            error("Couldn't find Join_Group button")
            data['trace']['steps'].append({
                    'start_time':datetime.now().isoformat(' ','seconds'),
                    'end_time': datetime.now().isoformat(' ','seconds'), 
                    'action' : 'Find Join_Group button',
                    'status' : False })
            data.update({"flow": {
                    "uuid": uuid,
                    "user_id": user_id,
                    "start_time": start_flow,
                    "end_time": end_flow,
                    "used_ip": ip,
                    "error": "601 - Join_group button not found"
                    }})
            with open(r"./callback/join_group_callback.json",'w') as cb:
                json.dump(data,cb)
            browser.quit()
            cb = open(r"./callback_json/join_group_callback.json",'r') 
            send_data = cb.read()
            r = requests.post(cb_url, json=send_data)
            print("Callback given with error description")

        # click join group
        try:    
            join_grp.click()
            print("### Join_Group clicked ###")
            info("Join_Group clicked ")
            
            data['trace']['steps'].append({
                    'start_time':datetime.now().isoformat(' ','seconds'),
                    'end_time': datetime.now().isoformat(' ','seconds'), 
                    'action' : 'Click Join_Group button',
                    'status' : "success" })
            sleep(5)
        except:
            end_time = datetime.now().isoformat(' ','seconds')
            end_flow =  datetime.now().isoformat(' ','seconds')
            error("Couldn't click Join_Group button") 
            print("### Couldn't click Join_Group button")
            with open(r"./callback/join_group_callback.json",'w') as cb:
                data['trace']['steps'].append({
                    'group_id' : grp_id,
                    'user_id' : user_id,
                    'start_time':start_time,
                    'end_time': end_time, 
                    'action' : 'Click Join_Group button',
                    'status' : "blocked or failed_error" })
                data.update({"flow": {
                    "uuid": uuid,
                    "user_id": user_id,
                    "start_time": start_flow,
                    "end_time": end_flow,
                    "used_ip": ip,
                    "error": "602 - Click Join_Group button"
                    }})
                json.dump(data,cb) 
            browser.quit()
            cb = open(r"./callback_json/join_group_callback.json",'r') 
            send_data = cb.read()
            r = requests.post(cb_url, json=send_data)
            print("Callback given with error description")

        # failed questions check
        try:
            end_flow =  datetime.now().isoformat(' ','seconds')
            ans_que = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH,"//span[contains(text(),'Answer questions')]")))
            if ans_que.text == 'Answer questions':
                print("### Failed Questions ###")
                info("Failed Questions")
                
                data['trace']['steps'].append({
                            'group_id': grp_id, 
                            'user_id': user_id,
                            'start_time':datetime.now().isoformat(' ','seconds'),
                            'end_time': datetime.now().isoformat(' ','seconds'),
                            'action' : 'Group joined',
                            'status' : 'failed_question' })
                data.update({"flow": {
                    "uuid": uuid,
                    "user_id": user_id,
                    "start_time": start_flow,
                    "end_time": end_flow,
                    "used_ip": ip,
                    "error": "801 - failed_questions"
                    }})
            with open(r"./callback/join_group_callback.json",'w') as cb:
                json.dump(data,cb)
            cb = open(r"./callback_json/join_group_callback.json",'r') 
            send_data = cb.read()
            r = requests.post(cb_url, json=send_data)
            print("Callback given with error description")
                
        except:
            end_time = datetime.now().isoformat(' ','seconds') 
            end_flow =  datetime.now().isoformat(' ','seconds')       
            print("### Group joined ###,id={}".format(grp_id))
            info("Group joined, id={}".format(grp_id))
            data['trace']['steps'].append({
                            'group_id' : grp_id,
                            'user_id' : user_id,
                            'start_time':start_time,
                            'end_time': end_time, 
                            'action' : 'Group joined',
                            'status' : 'success' })
            data.update({"flow": {
                    "uuid": uuid,
                    "user_id": user_id,
                    "start_time": start_flow,
                    "end_time": end_flow,
                    "used_ip": ip,
                    "error": "None -  Group joined, id={}".format(grp_id)
                    }})
            with open(r"./callback/join_group_callback.json",'w') as cb:
                json.dump(data,cb)

            s = random.randint(int(att1),int(att2))
            s_mins = int(s/60)
            print("***Sleeping for {} mins***".format(s_mins))
            info("***Sleeping for {} mins***".format(s_mins))

            # fetch callback data
            try:
                cb = open(r"./callback_json/join_group_callback.json",'r') 
                send_data = cb.read()  
                r = requests.post(cb_url, json=send_data)
                info("Callback data fetched")
                print("Callback data fetched")
                print("Data is->",send_data)
            except:
                info("Cannot fetch callback data")
                print("Cannot fetch callback data")
                data_ = {"Error":"Data was not fetched , please see callback file"}
                r = requests.post(cb_url, json=data_) 
            
            # send data
            try:
                if r.status_code == 200:
                    info("Callback sent")
                    print("Callback sent")
                    print("Response json data is ",r.json(),"\n")
                else:
                    info("Callback url responded abnormally")
                    print("Callback url responded abnormally")
            except:
                info("Error in callback")
                print("Error in callback")
                data_ = {"Error":"Callback url responded abnormally before"} 
                r = requests.post(cb_url, json=data_)

        sleep(s) 

end_flow =  datetime.now().isoformat(' ','seconds') 

if __name__ == '__main__':
    try:
        browser = get_browser()
        debug("Browser Initiated")
    except:
        critical("Could not initiate browser")   

    post_the_post(browser)

    data.update({"flow": {
      "uuid": uuid,
      "start_time": start_flow,
      "end_time": end_flow,
      "used_ip": ip,
      "error": "none"
    }})

    info("Done with the task !!!")

    with open(r"./callback/join_group_callback.json",'w') as cb:
        json.dump(data,cb)
    print("Callback file dumped") 
    info("Callback file dumped")

    # fetch data
    try:
        cb = open(r"./callback_json/join_group_callback.json",'r') 
        send_data = cb.read()  
        r = requests.post(cb_url, json=send_data)
        info("Callback data fetched")
        print("Callback data fetched")
        print("Data is->",send_data)
    except:
        info("Cannot fetch callback data")
        print("Cannot fetch callback data")
        data_ = {"Error":"Data was not fetched , please see callback file"}
        r = requests.post(cb_url, json=data_) 

    # send data
    try:
        if r.status_code == 200:
            info("Callback sent")
            print("Callback sent")
            print("Response json data is ",r.json(),"\n")
        else:
            info("Callback url responded abnormally")
            print("Callback url responded abnormally")
    except:
        info("Error in callback")
        print("Error in callback")
        data_ = {"Error":"Callback url responded abnormally before"} 
        r = requests.post(cb_url, json=data_)
    
    info("Done with the task !!!")
    print("Done with the task !!!") 

browser.quit()
   
