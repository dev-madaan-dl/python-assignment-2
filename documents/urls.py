from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    DocumentListCreateView,
    DocumentDetailView,
    QueryView,
    QueryHistoryView,
)

urlpatterns = [
    path('auth/register', RegisterView.as_view()),
    path('auth/login', LoginView.as_view()),
    path('documents', DocumentListCreateView.as_view()),
    path('documents/<int:pk>', DocumentDetailView.as_view()),
    path('query', QueryView.as_view()),
    path('queries', QueryHistoryView.as_view()),
]
