from django.urls import path
from .views import Fb_Api, GetCookies_api, Join_grp_api,Join_grp_api, TestSelenium_Api

urlpatterns = [
    path('',Fb_Api.as_view(),name='Fb_Api'),
    path('join',Join_grp_api.as_view(),name='Join_grp_api'),
    path('getcookies',GetCookies_api.as_view(),name='GetCookies_api'),
    path('test',TestSelenium_Api.as_view(),name='TestSelenium_Api'),
]
