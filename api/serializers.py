from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Company, Watchlist, WatchlistItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class WatchlistItemSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = WatchlistItem
        fields = ['id', 'company']

class WatchlistSerializer(serializers.ModelSerializer):
    items = WatchlistItemSerializer(many=True, read_only=True)

    class Meta:
        model = Watchlist
        fields = ['id', 'name_watchlist', 'items']
