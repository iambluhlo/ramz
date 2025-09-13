from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from django.utils import timezone
from datetime import timedelta
import random
import string

from .models import User, UserProfile, VerificationCode, LoginAttempt
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserSerializer,
    UserProfileSerializer, VerificationCodeSerializer, VerifyCodeSerializer,
    ChangePasswordSerializer, TwoFactorSetupSerializer
)


class RegisterView(generics.CreateAPIView):
    """User registration endpoint"""
    
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        # Send verification code for phone
        self.send_verification_code(user, 'phone')
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'message': 'ثبت نام با موفقیت انجام شد. کد تایید به شماره تلفن شما ارسال شد.'
        }, status=status.HTTP_201_CREATED)
    
    def send_verification_code(self, user, code_type):
        """Generate and send verification code"""
        code = ''.join(random.choices(string.digits, k=6))
        expires_at = timezone.now() + timedelta(minutes=10)
        
        VerificationCode.objects.create(
            user=user,
            code=code,
            code_type=code_type,
            expires_at=expires_at
        )
        
        # Here you would integrate with SMS/Email service
        # For now, we'll just log it
        print(f"Verification code for {user.email}: {code}")


class LoginView(APIView):
    """User login endpoint"""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        # Log login attempt
        LoginAttempt.objects.create(
            user=user,
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            success=True
        )
        
        # Update last login IP
        user.last_login_ip = self.get_client_ip(request)
        user.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'requires_2fa': user.two_factor_enabled,
            'message': 'ورود با موفقیت انجام شد'
        })
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class ProfileView(generics.RetrieveUpdateAPIView):
    """User profile view"""
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """User profile detail view"""
    
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


class SendVerificationCodeView(APIView):
    """Send verification code endpoint"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        code_type = request.data.get('code_type')
        
        if code_type not in dict(VerificationCode.CODE_TYPES):
            return Response(
                {'error': 'نوع کد تایید نامعتبر است'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user already has a recent code
        recent_code = VerificationCode.objects.filter(
            user=request.user,
            code_type=code_type,
            created_at__gte=timezone.now() - timedelta(minutes=2),
            is_used=False
        ).first()
        
        if recent_code:
            return Response(
                {'error': 'کد تایید اخیراً ارسال شده است. لطفاً 2 دقیقه صبر کنید.'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        
        # Generate new code
        code = ''.join(random.choices(string.digits, k=6))
        expires_at = timezone.now() + timedelta(minutes=10)
        
        VerificationCode.objects.create(
            user=request.user,
            code=code,
            code_type=code_type,
            expires_at=expires_at
        )
        
        # Here you would send the actual SMS/Email
        print(f"Verification code for {request.user.email}: {code}")
        
        return Response({
            'message': 'کد تایید ارسال شد',
            'expires_in': 600  # 10 minutes
        })


class VerifyCodeView(APIView):
    """Verify code endpoint"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        code = serializer.validated_data['code']
        code_type = serializer.validated_data['code_type']
        
        # Find valid code
        verification_code = VerificationCode.objects.filter(
            user=request.user,
            code=code,
            code_type=code_type,
            is_used=False,
            expires_at__gt=timezone.now()
        ).first()
        
        if not verification_code:
            return Response(
                {'error': 'کد تایید نامعتبر یا منقضی شده است'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Mark code as used
        verification_code.is_used = True
        verification_code.save()
        
        # Update user verification status
        user = request.user
        if code_type == 'phone':
            user.is_phone_verified = True
        elif code_type == 'email':
            user.is_email_verified = True
        
        user.save()
        
        return Response({
            'message': 'تایید با موفقیت انجام شد',
            'user': UserSerializer(user).data
        })


class ChangePasswordView(APIView):
    """Change password endpoint"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({'message': 'رمز عبور با موفقیت تغییر یافت'})


class TwoFactorSetupView(APIView):
    """2FA setup endpoint"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        if request.user.two_factor_enabled:
            return Response(
                {'error': 'احراز هویت دو مرحله‌ای قبلاً فعال شده است'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = TwoFactorSetupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Here you would verify the 2FA code with the generated secret
        # For simplicity, we'll just enable it
        user = request.user
        user.two_factor_enabled = True
        user.two_factor_secret = ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))
        user.save()
        
        return Response({
            'message': 'احراز هویت دو مرحله‌ای با موفقیت فعال شد',
            'user': UserSerializer(user).data
        })


class DisableTwoFactorView(APIView):
    """Disable 2FA endpoint"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        user = request.user
        if not user.two_factor_enabled:
            return Response(
                {'error': 'احراز هویت دو مرحله‌ای فعال نیست'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.two_factor_enabled = False
        user.two_factor_secret = None
        user.save()
        
        return Response({
            'message': 'احراز هویت دو مرحله‌ای غیرفعال شد',
            'user': UserSerializer(user).data
        })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats(request):
    """Get user statistics"""
    user = request.user
    
    # Get login attempts in last 30 days
    recent_logins = LoginAttempt.objects.filter(
        user=user,
        timestamp__gte=timezone.now() - timedelta(days=30)
    ).count()
    
    # Get failed login attempts
    failed_logins = LoginAttempt.objects.filter(
        user=user,
        success=False,
        timestamp__gte=timezone.now() - timedelta(days=30)
    ).count()
    
    return Response({
        'recent_logins': recent_logins,
        'failed_logins': failed_logins,
        'account_age_days': (timezone.now() - user.date_joined).days,
        'verification_status': {
            'phone': user.is_phone_verified,
            'email': user.is_email_verified,
            'identity': user.is_identity_verified,
        },
        'security_features': {
            'two_factor': user.two_factor_enabled,
            'trading_enabled': user.is_trading_enabled,
            'withdrawal_enabled': user.is_withdrawal_enabled,
        }
    })