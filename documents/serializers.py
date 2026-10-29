from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Document, QueryLog, UserSession


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'created_at', 'updated_at']


class QueryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueryLog
        fields = ['id', 'query_text', 'results', 'created_at']


class UserSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSession
        fields = ['id', 'user', 'last_active', 'created_at']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user
