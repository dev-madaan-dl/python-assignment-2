from django.db import models
from django.contrib.auth.models import User


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class QueryLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='queries')
    query_text = models.CharField(max_length=500)
    results = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.query_text}"


class UserSession(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='session')
    last_active = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} session"
