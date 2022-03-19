from distutils import extension
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView 
import datetime  
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from .serializers import GetCookiesSerializer, MyInputSerializer,JoinGrpSerializer, TestApiSerializer

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
from time import sleep
# from webdriver_manager.chrome import ChromeDriverManager

import os
import configparser 

class Fb_Api(CreateAPIView):
    serializer_class = MyInputSerializer
    def post(self, request, *args, **kwargs):
        password = self.request.POST['password']
        xs = self.request.POST['xs']
        xs_time = self.request.POST['xs_time']
        c_user = self.request.POST['c_user']
        c_user_time = self.request.POST['c_user_time']
        uuid = self.request.POST['uuid']
        post_id = self.request.POST['post_id']
        port = self.request.POST['port']          
        
        config = configparser.ConfigParser()
        config.read(r"./config_files/config_share_post.ini")
        ip_port = config['ip_port']
        config_port = ip_port['port']

        if port=='':
            IP_proxy = 'il.smartproxy.com:{}'.format(config_port)
        else:
            IP_proxy = 'il.smartproxy.com:{}'.format(port)

        context = {
            'Status':'Successfull',
            'Uuid' : uuid,
                   }
        try:
            def post_share_via_url(): 
                os.system("python " + "./bots/share_post.py " + xs_time + " " +  c_user_time + " " + xs + " " + c_user + " " + post_id + " " + password + " " + uuid + " " + IP_proxy )
                # os.system("python3 " + "./bots/share_post.py " + xs_time + " " +  c_user_time + " " + xs + " " + c_user + " " + post_id + " " + password + " " + uuid + " " + IP_proxy)
            post_share_via_url()

        except:
            context2 = {'Status':'Failure', 'UUID': uuid}
            return Response( context2, status=status.HTTP_400_BAD_REQUEST)
        
        return Response( context, status=status.HTTP_200_OK)

class TestSelenium_Api(CreateAPIView):
    serializer_class = TestApiSerializer
    def post(self, request, *args, **kwargs):
        url = self.request.POST['url']

        ip = 'il.smartproxy.com:30002'

        try:
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
                chrome_options.add_argument("--proxy-server={}".format(ip))               
                # browser = webdriver.Chrome(executable_path= r"C:\Program Files (x86)\chromedriver.exe" ,options=chrome_options,desired_capabilities=capabilities)
                browser = webdriver.Chrome(executable_path= r"/usr/bin/chromedriver" ,options=chrome_options)
                return browser

            browser = get_browser()
               
            browser.get(url)
            sleep(5)
            pagesource = browser.page_source
            print(pagesource)

            context = {
                    'Status':'Successfull',
                    'Result': pagesource
                        }
        except:
            context = {
                'Status':'Successfull',
                'Result': "Chromedriver was not found"
                    }

        return Response( context, status=status.HTTP_200_OK)

class Join_grp_api(CreateAPIView):
    serializer_class = JoinGrpSerializer
    def post(self, request, *args, **kwargs):
        password = self.request.POST['password']
        xs = self.request.POST['xs']
        xs_time = self.request.POST['xs_time']
        c_user = self.request.POST['c_user']
        c_user_time = self.request.POST['c_user_time']
        uuid = self.request.POST['uuid']
        user_id = self.request.POST['user_id']
        grp_list_str = self.request.POST['grp_list']
        port = self.request.POST['port']

        config = configparser.ConfigParser()
        config.read(r"./config_files/config_join_grp.ini")
        ip_port = config['ip_port']
        config_port = ip_port['port']

        if port=='':
            IP_proxy = 'il.smartproxy.com:{}'.format(config_port)
        else:
            IP_proxy = 'il.smartproxy.com:{}'.format(port)

        def join_groups():
            os.system("python " + "./bots/join_grp.py " + xs_time + " " +  c_user_time + " " + xs + " " + c_user + " " + grp_list_str + " " + password + " " + uuid + " " + IP_proxy + " " + user_id )
            # os.system("python3 " + "./bots/join_grp.py " + xs_time + " " +  c_user_time + " " + xs + " " + c_user + " " + grp_list_str + " " + password + " " + uuid + " " + IP_proxy + " " + user_id)

        join_groups()

        context = {
            'Status':'Successfull',
            'Uuid' : uuid,
            'User ID' : user_id
                   }
        return Response( context, status=status.HTTP_200_OK)

import requests

class GetCookies_api(CreateAPIView):
    serializer_class = GetCookiesSerializer
    def post(self, request, *args, **kwargs):
        api_password = self.request.POST['api_password']
        username = self.request.POST['username']
        fb_password = self.request.POST['fb_password']
        
        ip = 'il.smartproxy.com:30002'

        if api_password != '12345asdf':
            print("Wrong password")
            ("Wrong password")
            data_ = {"Error":"Wrong password"}
            r = requests.post('https://blubee.app/api/execution-info', json=data_)
            print("Wrong password")
            print("Data is",data_,"\n")

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
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--proxy-server={}".format(ip))
            browser = webdriver.Chrome(executable_path= r"/usr/bin/chromedriver",options=chrome_options)
            # browser = webdriver.Chrome(executable_path= r"C:\Program Files (x86)\chromedriver.exe" ,options=chrome_options)
            return browser
                    
        def get_cookies(browser):
            try:
                url = 'https://www.facebook.com/'
                browser.get(url)
                print("On FB page")
                sleep(8)
                # print(browser.page_source)
            except:
                print("Page Fb not found")

            try:
                accept = browser.find_element_by_xpath('//*[@title="Allow essential and optional cookies"]')
                sleep(2)
                accept.click()
                sleep(4)
                print("Accept button found")
            except:
                print("No accept button")
                return Response({'Message':'Login was failed'}, status=status.HTTP_404_NOT_FOUND)

            try:
                name=browser.find_element_by_xpath('//*[@name="email"]')
                sleep(3)
                name.send_keys(username)
                sleep(5)
                print("Name found")
            except:
                print("Name not found")
                return Response({'Message':'Email button not found '}, status=status.HTTP_404_NOT_FOUND)
                
            try:  
                passwword = browser.find_element_by_xpath('//*[@name="pass"]')
                sleep(3)
                passwword.send_keys(fb_password)
                sleep(4)
                print("password found")
            except:
                print("Password not found")
                return Response({'Message':'Password button not found'}, status=status.HTTP_404_NOT_FOUND)
                
      
            try:
                login = browser.find_element_by_xpath('//*[@name="login"]')
                sleep(2)
                login.click()
                sleep(2)
                print("Login clicked")
            except:
                print("Login not clicked")
                return Response({'Message':'Login was not clicked'}, status=status.HTTP_404_NOT_FOUND)
                
            print("Login  clicked")

            cookies = browser.get_cookies()
            print("Cookies Captured.......")
          
            sleep(5)
            try:
                browser.find_element_by_xpath('//*[@aria-label="Menu"]')
                sleep(3)
            except:
                print("Menu not found")
                return Response({'Message':'Login was failed'}, status=status.HTTP_404_NOT_FOUND)
            return cookies

        browser = get_browser()
        browser.get('http://lumtest.com/myip.json')
        sleep(4)
        print(browser.page_source)
        sleep(3)
        cookies = get_cookies(browser)

        for cooks in cookies:
            if cooks['name'] =='xs':
                xs = cooks['value']
                xs_time = cooks['expiry']
            elif cooks['name'] == 'c_user':
                c_user = cooks['value']
                c_user_time = cooks['expiry']
            else:
                pass
        
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
        return Response(context,status=status.HTTP_200_OK)
      

