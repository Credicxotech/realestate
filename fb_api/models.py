from django.db import models

# Create your models here.
class api_params(models.Model):
    password = models.CharField(max_length=50, null=False,default=None) 
    xs = models.CharField(max_length=200,default=None)
    xs_time = models.CharField( max_length=50)
    c_user = models.CharField(max_length=200,default=None)  
    c_user_time = models.CharField( max_length=50)
    uuid=models.UUIDField(default=None)
    post_id = models.CharField(max_length=50)
    port = models.CharField(max_length=50)

class join_grp_api_params(models.Model):
    password = models.CharField(max_length=50, null=False,default=None) 
    xs = models.CharField(max_length=200,default=None)
    xs_time = models.CharField( max_length=50)
    c_user = models.CharField(max_length=200,default=None)  
    c_user_time = models.CharField( max_length=50)
    uuid = models.UUIDField(default=None)
    user_id = models.CharField( max_length=50)
    grp_list = models.CharField(max_length=1000,default=None)
    port = models.CharField(max_length=50)

class get_cookies_api_params(models.Model):
    api_password = models.CharField(max_length=50, null=False,default=None) 
    username = models.CharField(max_length=200,default=None)
    fb_password = models.CharField(max_length=200,default=None)  


    
