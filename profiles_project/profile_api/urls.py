from django.urls import path
from profile_api import views

app_name = "profile_api"

urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
]
