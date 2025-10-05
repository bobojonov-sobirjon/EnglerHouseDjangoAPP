from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Order, OrderTask
from apps.accounts.models import CustomUser


@receiver(post_save, sender=Order)
def send_order_created_email(sender, instance, created, **kwargs):
    """Send email notification when a new order is created"""
    if created and instance.user and instance.user.email:
        try:
            # Prepare email data
            subject = f'Новый заказ #{instance.order_number} создан - ENGLER House'
            
            # Render email template
            html_message = render_to_string('emails/order_created.html', {
                'order': instance,
                'site_url': getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
            })
            
            # Send email
            send_mail(
                subject=subject,
                message='',  # Plain text version (empty since we're using HTML)
                html_message=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.user.email],
                fail_silently=False,
            )
            
            print(f"Order created email sent to {instance.user.email}")
            
        except Exception as e:
            print(f"Failed to send order created email: {e}")


@receiver(pre_save, sender=OrderTask)
def track_task_status_change(sender, instance, **kwargs):
    """Track when task status changes"""
    if instance.pk:  # Only for existing instances
        try:
            old_instance = OrderTask.objects.get(pk=instance.pk)
            instance._old_status = old_instance.status
        except OrderTask.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None


@receiver(post_save, sender=OrderTask)
def send_task_status_changed_email(sender, instance, created, **kwargs):
    """Send email notification when task status changes"""
    # Only send email if status actually changed and user has email
    if (hasattr(instance, '_old_status') and 
        instance._old_status != instance.status and 
        instance.order.user and 
        instance.order.user.email):
        
        try:
            # Prepare email data
            subject = f'Статус этапа "{instance.title}" изменен - Заказ #{instance.order.order_number}'
            
            # Render email template
            html_message = render_to_string('emails/task_status_changed.html', {
                'task': instance,
                'site_url': getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
            })
            
            # Send email
            send_mail(
                subject=subject,
                message='',  # Plain text version (empty since we're using HTML)
                html_message=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.order.user.email],
                fail_silently=False,
            )
            
            print(f"Task status changed email sent to {instance.order.user.email}")
            
        except Exception as e:
            print(f"Failed to send task status changed email: {e}")


@receiver(pre_save, sender=CustomUser)
def store_user_password(sender, instance, **kwargs):
    """Store the password before saving to send in email"""
    if not instance.pk:  # Only for new instances
        instance._original_password = instance.password
    else:
        # For existing instances, check if password was changed
        try:
            old_instance = CustomUser.objects.get(pk=instance.pk)
            if old_instance.password != instance.password:
                instance._original_password = instance.password
            else:
                instance._original_password = None
        except CustomUser.DoesNotExist:
            instance._original_password = None


@receiver(post_save, sender=CustomUser)
def send_user_created_email(sender, instance, created, **kwargs):
    """Send email notification when a new user is created"""
    if created and instance.email and hasattr(instance, '_original_password') and instance._original_password:
        try:
            # Use the actual password that was set
            actual_password = instance._original_password
            
            # Prepare email data
            subject = f'Добро пожаловать в ENGLER House - Ваш аккаунт создан'
            
            # Render email template
            html_message = render_to_string('emails/user_created.html', {
                'user': instance,
                'password': actual_password,
                'site_url': getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
            })
            
            # Send email
            send_mail(
                subject=subject,
                message='',  # Plain text version (empty since we're using HTML)
                html_message=html_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email],
                fail_silently=False,
            )
            
            print(f"User created email sent to {instance.email} with password: {actual_password}")
            
        except Exception as e:
            print(f"Failed to send user created email: {e}")
