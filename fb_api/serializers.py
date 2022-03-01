from django.db.models.base import Model
from rest_framework import serializers

from .models import api_params, get_cookies_api_params , join_grp_api_params

class MyInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_params
        fields = '__all__'

class JoinGrpSerializer(serializers.ModelSerializer):
    class Meta:
        model = join_grp_api_params
        fields = '__all__'

class GetCookiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_cookies_api_params
        fields = '__all__'