
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_page, name="home_page"),
    path('create_expense/', views.create_expense, name="create_expense"),
]
