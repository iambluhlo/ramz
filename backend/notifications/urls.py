from django.urls import path
from . import views

urlpatterns = [
    # Notifications
    path('', views.UserNotificationsView.as_view(), name='user_notifications'),
    path('stats/', views.notification_stats, name='notification_stats'),
    path('<uuid:notification_id>/read/', views.MarkNotificationReadView.as_view(), name='mark_notification_read'),
    path('mark-all-read/', views.MarkAllNotificationsReadView.as_view(), name='mark_all_notifications_read'),
    path('<uuid:notification_id>/delete/', views.DeleteNotificationView.as_view(), name='delete_notification'),
    path('clear-all/', views.clear_all_notifications, name='clear_all_notifications'),
    path('clear-read/', views.clear_read_notifications, name='clear_read_notifications'),
    
    # Preferences
    path('preferences/', views.NotificationPreferencesView.as_view(), name='notification_preferences'),
]