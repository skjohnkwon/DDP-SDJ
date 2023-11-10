from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from userauth import views
        
urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('check-auth/', views.check_auth, name='check-auth'),
    path('get-account-data/', views.get_account_data, name='get-account-data'),
]
