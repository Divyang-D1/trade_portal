from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Company, Watchlist

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'company_name', 'symbol', 'scripcode']

class WatchlistSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = Watchlist
        fields = ['company']
