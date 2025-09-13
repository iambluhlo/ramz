from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, UserProfile, VerificationCode
import random
import string

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'email', 'username', 'phone_number', 'first_name', 'last_name',
            'password', 'password_confirm'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("رمزهای عبور مطابقت ندارند")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        # Create user profile
        UserProfile.objects.create(user=user)
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError('اطلاعات ورود نامعتبر است')
            if not user.is_active:
                raise serializers.ValidationError('حساب کاربری غیرفعال است')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('ایمیل و رمز عبور الزامی است')
        
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user information"""
    
    profile = UserProfileSerializer(read_only=True)
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'phone_number', 'first_name', 'last_name',
            'full_name', 'is_phone_verified', 'is_email_verified', 
            'is_identity_verified', 'two_factor_enabled', 'is_trading_enabled',
            'is_withdrawal_enabled', 'date_joined', 'last_login', 'profile'
        ]
        read_only_fields = [
            'id', 'is_phone_verified', 'is_email_verified', 'is_identity_verified',
            'two_factor_enabled', 'date_joined', 'last_login'
        ]


class VerificationCodeSerializer(serializers.ModelSerializer):
    """Serializer for verification codes"""
    
    class Meta:
        model = VerificationCode
        fields = ['code_type', 'created_at', 'expires_at']
        read_only_fields = ['created_at', 'expires_at']


class VerifyCodeSerializer(serializers.Serializer):
    """Serializer for code verification"""
    
    code = serializers.CharField(max_length=6, min_length=6)
    code_type = serializers.ChoiceField(choices=VerificationCode.CODE_TYPES)


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change"""
    
    old_password = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
    new_password_confirm = serializers.CharField()
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("رمزهای عبور جدید مطابقت ندارند")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("رمز عبور فعلی اشتباه است")
        return value


class TwoFactorSetupSerializer(serializers.Serializer):
    """Serializer for 2FA setup"""
    
    verification_code = serializers.CharField(max_length=6, min_length=6)
    
    def validate_verification_code(self, value):
        # Here you would validate the 2FA code with the secret
        # This is a simplified version
        if not value.isdigit():
            raise serializers.ValidationError("کد تایید باید عددی باشد")
        return value