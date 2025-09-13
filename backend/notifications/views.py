from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from .models import Notification, NotificationPreference
from .serializers import (
    NotificationSerializer, NotificationPreferenceSerializer, NotificationStatsSerializer
)

class UserNotificationsView(generics.ListAPIView):
    """List user's notifications"""
    
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Notification.objects.filter(user=self.request.user)
        
        # Filter by read status
        is_read = self.request.query_params.get('is_read')
        if is_read is not None:
            queryset = queryset.filter(is_read=is_read.lower() == 'true')
        
        # Filter by notification type
        notification_type = self.request.query_params.get('type')
        if notification_type:
            queryset = queryset.filter(notification_type=notification_type)
        
        # Filter by priority
        priority = self.request.query_params.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        
        return queryset.order_by('-created_at')


class MarkNotificationReadView(generics.UpdateAPIView):
    """Mark notification as read"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def patch(self, request, notification_id):
        try:
            notification = Notification.objects.get(
                id=notification_id, 
                user=request.user
            )
        except Notification.DoesNotExist:
            return Response(
                {'error': 'اطلاع‌رسانی یافت نشد'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if not notification.is_read:
            notification.is_read = True
            notification.read_at = timezone.now()
            notification.save()
        
        return Response(
            NotificationSerializer(notification).data,
            status=status.HTTP_200_OK
        )


class MarkAllNotificationsReadView(generics.UpdateAPIView):
    """Mark all notifications as read"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def patch(self, request):
        updated_count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(
            is_read=True,
            read_at=timezone.now()
        )
        
        return Response({
            'message': f'{updated_count} اطلاع‌رسانی به عنوان خوانده شده علامت‌گذاری شد',
            'updated_count': updated_count
        })


class NotificationPreferencesView(generics.RetrieveUpdateAPIView):
    """Get and update notification preferences"""
    
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        preferences, created = NotificationPreference.objects.get_or_create(
            user=self.request.user
        )
        return preferences


class DeleteNotificationView(generics.DestroyAPIView):
    """Delete a notification"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, notification_id):
        try:
            notification = Notification.objects.get(
                id=notification_id, 
                user=request.user
            )
            notification.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Notification.DoesNotExist:
            return Response(
                {'error': 'اطلاع‌رسانی یافت نشد'},
                status=status.HTTP_404_NOT_FOUND
            )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def notification_stats(request):
    """Get notification statistics"""
    
    user = request.user
    notifications = Notification.objects.filter(user=user)
    
    total_notifications = notifications.count()
    unread_notifications = notifications.filter(is_read=False).count()
    high_priority_unread = notifications.filter(
        is_read=False, 
        priority__in=['high', 'urgent']
    ).count()
    
    # Recent notifications (last 10)
    recent_notifications = notifications.order_by('-created_at')[:10]
    
    data = {
        'total_notifications': total_notifications,
        'unread_notifications': unread_notifications,
        'high_priority_unread': high_priority_unread,
        'recent_notifications': NotificationSerializer(recent_notifications, many=True).data,
    }
    
    return Response(data)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def clear_all_notifications(request):
    """Clear all notifications for user"""
    
    deleted_count = Notification.objects.filter(user=request.user).count()
    Notification.objects.filter(user=request.user).delete()
    
    return Response({
        'message': f'{deleted_count} اطلاع‌رسانی حذف شد',
        'deleted_count': deleted_count
    })


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def clear_read_notifications(request):
    """Clear read notifications for user"""
    
    deleted_count = Notification.objects.filter(
        user=request.user, 
        is_read=True
    ).count()
    
    Notification.objects.filter(
        user=request.user, 
        is_read=True
    ).delete()
    
    return Response({
        'message': f'{deleted_count} اطلاع‌رسانی خوانده شده حذف شد',
        'deleted_count': deleted_count
    })