from django.urls import path
from . import views

urlpatterns = [
    path('part3/send-list-of-users-excluding-admin-and-current-user/', views.send_list_of_users_excluding_admin_and_current_user, name='send_list_of_users_excluding_admin_and_current_user'),
    path('part3/add-favorite/', views.add_favorite, name='add_favorite'),
    path('part3/q10/', views.q10, name='q10'),
    path('part3/q9/', views.q9, name='q9'),
    path('part3/q8/', views.q8, name='q8'),
    path('part3/q7/', views.q7, name='q7'),
    path('part3/q6/', views.q6, name='q6'),
    path('part3/q5/', views.q5, name='q5'),
    path('part3/q4/', views.q4, name='q4'),
    path('part3/q3/', views.q3, name='q3'),
    path('part3/q2/', views.q2, name='q2'),
    path('part3/q1/', views.q1, name='q1'),
]