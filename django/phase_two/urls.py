from django.urls import path
from . import views

urlpatterns = [
    path('create-item/', views.create_item, name='create-item'),
    path('search/', views.search, name='search'),
    path('create-comment/', views.create_comment, name='create-comment'),
    path('create-item-test/', views.create_item_test, name='create-item-test'),
    path('init-db/', views.init_db, name='init-db'),
]