from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('track/', views.track, name='track'),
    path('search/', views.search, name='search'),
    path('product/<int:id>', views.product, name='product'),
    path('checkout/', views.checkOut, name='checkOut'),
    path('handleRequest/', views.handleRequest, name='handleRequest'),
]