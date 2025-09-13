from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Profile
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/detail/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('stats/', views.user_stats, name='user_stats'),
    
    # Verification
    path('send-code/', views.SendVerificationCodeView.as_view(), name='send_verification_code'),
    path('verify-code/', views.VerifyCodeView.as_view(), name='verify_code'),
    
    # Security
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('2fa/setup/', views.TwoFactorSetupView.as_view(), name='setup_2fa'),
    path('2fa/disable/', views.DisableTwoFactorView.as_view(), name='disable_2fa'),
]