from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone
from .models import Notification, NotificationPreference, EmailTemplate, SMSTemplate, NotificationLog
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    """Service for handling notifications"""
    
    def create_notification(self, user, notification_type, title, message, 
                          priority='medium', data=None, action_url=None):
        """Create a new notification"""
        
        notification = Notification.objects.create(
            user=user,
            notification_type=notification_type,
            priority=priority,
            title=title,
            message=message,
            data=data or {},
            action_url=action_url
        )
        
        # Send notification based on user preferences
        self.send_notification(notification)
        
        return notification
    
    def send_notification(self, notification):
        """Send notification via configured channels"""
        
        user = notification.user
        preferences = self.get_user_preferences(user)
        
        # Check if we should send based on notification type and user preferences
        should_send_email = self._should_send_email(notification, preferences)
        should_send_sms = self._should_send_sms(notification, preferences)
        should_send_push = self._should_send_push(notification, preferences)
        
        # Send via different channels
        if should_send_email:
            self.send_email_notification(notification)
        
        if should_send_sms:
            self.send_sms_notification(notification)
        
        if should_send_push:
            self.send_push_notification(notification)
        
        # Mark as sent
        notification.is_sent = True
        notification.sent_at = timezone.now()
        notification.save()
    
    def send_email_notification(self, notification):
        """Send email notification"""
        
        try:
            user = notification.user
            
            # Get email template
            template = self._get_email_template(notification.notification_type)
            if not template:
                logger.warning(f"No email template found for {notification.notification_type}")
                return
            
            # Prepare context
            context = {
                'user': user,
                'notification': notification,
                'site_name': 'بیت‌کوین پلاس',
                **notification.data
            }
            
            # Render email content
            subject = self._render_template_string(template.subject, context)
            html_message = self._render_template_string(template.html_content, context)
            plain_message = self._render_template_string(template.text_content, context)
            
            # Send email
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False
            )
            
            # Log successful send
            NotificationLog.objects.create(
                notification=notification,
                delivery_method='email',
                recipient=user.email,
                status='sent'
            )
            
            notification.sent_email = True
            notification.save()
            
        except Exception as e:
            logger.error(f"Failed to send email notification: {str(e)}")
            
            # Log failed send
            NotificationLog.objects.create(
                notification=notification,
                delivery_method='email',
                recipient=user.email,
                status='failed',
                error_message=str(e)
            )
    
    def send_sms_notification(self, notification):
        """Send SMS notification"""
        
        try:
            user = notification.user
            
            # Get SMS template
            template = self._get_sms_template(notification.notification_type)
            if not template:
                logger.warning(f"No SMS template found for {notification.notification_type}")
                return
            
            # Prepare context
            context = {
                'user': user,
                'notification': notification,
                **notification.data
            }
            
            # Render SMS content
            message = self._render_template_string(template.content, context)
            
            # Here you would integrate with SMS provider (e.g., Kavenegar, etc.)
            # For now, we'll just log it
            logger.info(f"SMS to {user.phone_number}: {message}")
            
            # Log successful send
            NotificationLog.objects.create(
                notification=notification,
                delivery_method='sms',
                recipient=user.phone_number,
                status='sent'
            )
            
            notification.sent_sms = True
            notification.save()
            
        except Exception as e:
            logger.error(f"Failed to send SMS notification: {str(e)}")
            
            # Log failed send
            NotificationLog.objects.create(
                notification=notification,
                delivery_method='sms',
                recipient=user.phone_number,
                status='failed',
                error_message=str(e)
            )
    
    def send_push_notification(self, notification):
        """Send push notification"""
        
        try:
            user = notification.user
            
            # Here you would integrate with push notification service
            # (Firebase, OneSignal, etc.)
            logger.info(f"Push notification to {user.email}: {notification.title}")
            
            # Log successful send
            NotificationLog.objects.create(
                notification=notification,
                delivery_method='push',
                recipient=user.email,
                status='sent'
            )
            
            notification.sent_push = True
            notification.save()
            
        except Exception as e:
            logger.error(f"Failed to send push notification: {str(e)}")
            
            # Log failed send
            NotificationLog.objects.create(
                notification=notification,
                delivery_method='push',
                recipient=user.email,
                status='failed',
                error_message=str(e)
            )
    
    def get_user_preferences(self, user):
        """Get user notification preferences"""
        preferences, created = NotificationPreference.objects.get_or_create(user=user)
        return preferences
    
    def _should_send_email(self, notification, preferences):
        """Check if email should be sent based on preferences"""
        
        type_mapping = {
            'trade_executed': preferences.email_trade_notifications,
            'order_filled': preferences.email_trade_notifications,
            'security_alert': preferences.email_security_alerts,
            'price_alert': preferences.email_price_alerts,
            'news_update': preferences.email_news_updates,
            'system_maintenance': preferences.email_system_updates,
        }
        
        return type_mapping.get(notification.notification_type, True)
    
    def _should_send_sms(self, notification, preferences):
        """Check if SMS should be sent based on preferences"""
        
        type_mapping = {
            'trade_executed': preferences.sms_trade_notifications,
            'order_filled': preferences.sms_trade_notifications,
            'security_alert': preferences.sms_security_alerts,
            'price_alert': preferences.sms_price_alerts,
            'withdrawal_approved': preferences.sms_withdrawal_confirmations,
            'withdrawal_completed': preferences.sms_withdrawal_confirmations,
        }
        
        return type_mapping.get(notification.notification_type, False)
    
    def _should_send_push(self, notification, preferences):
        """Check if push notification should be sent based on preferences"""
        
        type_mapping = {
            'trade_executed': preferences.push_trade_notifications,
            'order_filled': preferences.push_trade_notifications,
            'security_alert': preferences.push_security_alerts,
            'price_alert': preferences.push_price_alerts,
            'news_update': preferences.push_news_updates,
            'system_maintenance': preferences.push_system_updates,
        }
        
        return type_mapping.get(notification.notification_type, True)
    
    def _get_email_template(self, notification_type):
        """Get email template for notification type"""
        try:
            return EmailTemplate.objects.get(
                template_type=notification_type,
                is_active=True
            )
        except EmailTemplate.DoesNotExist:
            return None
    
    def _get_sms_template(self, notification_type):
        """Get SMS template for notification type"""
        try:
            return SMSTemplate.objects.get(
                template_type=notification_type,
                is_active=True
            )
        except SMSTemplate.DoesNotExist:
            return None
    
    def _render_template_string(self, template_string, context):
        """Render template string with context"""
        from django.template import Template, Context
        
        template = Template(template_string)
        return template.render(Context(context))
    
    # Convenience methods for common notifications
    
    def notify_trade_executed(self, user, trade):
        """Notify user about executed trade"""
        
        self.create_notification(
            user=user,
            notification_type='trade_executed',
            title='معامله اجرا شد',
            message=f'معامله {trade.quantity} {trade.trading_pair.base_currency.symbol} به قیمت {trade.price} اجرا شد',
            priority='medium',
            data={
                'trade_id': str(trade.id),
                'trading_pair': trade.trading_pair.symbol,
                'quantity': str(trade.quantity),
                'price': str(trade.price),
            }
        )
    
    def notify_order_filled(self, user, order):
        """Notify user about filled order"""
        
        self.create_notification(
            user=user,
            notification_type='order_filled',
            title='سفارش اجرا شد',
            message=f'سفارش {order.side} {order.quantity} {order.trading_pair.base_currency.symbol} به طور کامل اجرا شد',
            priority='medium',
            data={
                'order_id': str(order.id),
                'trading_pair': order.trading_pair.symbol,
                'side': order.side,
                'quantity': str(order.quantity),
                'price': str(order.price) if order.price else 'بازار',
            }
        )
    
    def notify_deposit_confirmed(self, user, transaction):
        """Notify user about confirmed deposit"""
        
        self.create_notification(
            user=user,
            notification_type='deposit_confirmed',
            title='واریز تایید شد',
            message=f'واریز {transaction.amount} {transaction.wallet.cryptocurrency.symbol} تایید شد',
            priority='medium',
            data={
                'transaction_id': str(transaction.id),
                'amount': str(transaction.amount),
                'cryptocurrency': transaction.wallet.cryptocurrency.symbol,
            }
        )
    
    def notify_withdrawal_approved(self, user, withdrawal_request):
        """Notify user about approved withdrawal"""
        
        self.create_notification(
            user=user,
            notification_type='withdrawal_approved',
            title='برداشت تایید شد',
            message=f'درخواست برداشت {withdrawal_request.amount} {withdrawal_request.cryptocurrency.symbol} تایید شد',
            priority='high',
            data={
                'withdrawal_id': str(withdrawal_request.id),
                'amount': str(withdrawal_request.amount),
                'cryptocurrency': withdrawal_request.cryptocurrency.symbol,
                'to_address': withdrawal_request.to_address,
            }
        )
    
    def notify_security_alert(self, user, alert_type, details):
        """Notify user about security alert"""
        
        self.create_notification(
            user=user,
            notification_type='security_alert',
            title='هشدار امنیتی',
            message=f'فعالیت مشکوک در حساب شما: {details}',
            priority='urgent',
            data={
                'alert_type': alert_type,
                'details': details,
            }
        )
    
    def notify_price_alert(self, user, market_alert, current_price):
        """Notify user about triggered price alert"""
        
        self.create_notification(
            user=user,
            notification_type='price_alert',
            title='هشدار قیمت',
            message=f'{market_alert.trading_pair.symbol} به قیمت {current_price} رسید',
            priority='medium',
            data={
                'alert_id': str(market_alert.id),
                'trading_pair': market_alert.trading_pair.symbol,
                'target_value': str(market_alert.target_value),
                'current_price': str(current_price),
                'alert_type': market_alert.alert_type,
            }
        )