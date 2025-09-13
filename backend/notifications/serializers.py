from rest_framework import serializers
from .models import Notification, NotificationPreference

class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for notifications"""
    
    class Meta:
        model = Notification
        fields = [
            'id', 'notification_type', 'priority', 'title', 'message',
            'data', 'action_url', 'is_read', 'created_at', 'read_at'
        ]
        read_only_fields = [
            'id', 'notification_type', 'priority', 'title', 'message',
            'data', 'action_url', 'created_at'
        ]


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """Serializer for notification preferences"""
    
    class Meta:
        model = NotificationPreference
        fields = [
            'email_trade_notifications', 'email_security_alerts', 'email_price_alerts',
            'email_news_updates', 'email_system_updates',
            'sms_trade_notifications', 'sms_security_alerts', 'sms_price_alerts',
            'sms_withdrawal_confirmations',
            'push_trade_notifications', 'push_security_alerts', 'push_price_alerts',
            'push_news_updates', 'push_system_updates',
            'do_not_disturb_start', 'do_not_disturb_end', 'timezone'
        ]


class NotificationStatsSerializer(serializers.Serializer):
    """Serializer for notification statistics"""
    
    total_notifications = serializers.IntegerField()
    unread_notifications = serializers.IntegerField()
    high_priority_unread = serializers.IntegerField()
    recent_notifications = NotificationSerializer(many=True)