from django.contrib import admin
from .models import Testing_api, api_params, get_cookies_api_params,join_grp_api_params
# Register your models here.
admin.site.register(api_params)
admin.site.register(join_grp_api_params)
admin.site.register(get_cookies_api_params)
admin.site.register(Testing_api)