url = 'https://blubee.app/api/execution-info'
import requests
load = {'data':'this is from server and code'}
r= requests.post(url,data=load)
print(r.status_code)
print(r.content)
print(r.json())
