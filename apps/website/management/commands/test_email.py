from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from apps.website.models import Order, OrderTask
from apps.accounts.models import CustomUser


class Command(BaseCommand):
    help = 'Test email notification functionality'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Email address to send test email to')
        parser.add_argument('--type', type=str, choices=['order', 'task', 'user'], help='Type of email to test')

    def handle(self, *args, **options):
        email = options.get('email')
        email_type = options.get('type', 'order')
        
        if not email:
            self.stdout.write(
                self.style.ERROR('Please provide an email address with --email')
            )
            return

        try:
            if email_type == 'order':
                self.test_order_email(email)
            elif email_type == 'task':
                self.test_task_email(email)
            elif email_type == 'user':
                self.test_user_email(email)
                
            self.stdout.write(
                self.style.SUCCESS(f'Test {email_type} email sent successfully to {email}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Failed to send test email: {e}')
            )

    def test_order_email(self, email):
        """Test order created email"""
        # Create a test user if needed
        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={
                'full_name': 'Test User',
                'phone': '+998901234567'
            }
        )
        
        # Create a test order
        order = Order.objects.create(
            user=user,
            order_number='TEST-001',
            start_date='2025-01-15',
            end_date='2025-01-30',
            status='pending'
        )
        
        # Send email
        subject = f'Test: Новый заказ #{order.order_number} создан - ENGLER House'
        html_message = render_to_string('emails/order_created.html', {
            'order': order,
            'site_url': getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
        })
        
        send_mail(
            subject=subject,
            message='',
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

    def test_task_email(self, email):
        """Test task status changed email"""
        # Create a test user if needed
        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={
                'full_name': 'Test User',
                'phone': '+998901234567'
            }
        )
        
        # Create a test order
        order = Order.objects.create(
            user=user,
            order_number='TEST-002',
            start_date='2025-01-15',
            end_date='2025-01-30',
            status='in_progress'
        )
        
        # Create a test task
        task = OrderTask.objects.create(
            order=order,
            title='Test Task',
            description='This is a test task for email notification',
            start_date='2025-01-15',
            end_date='2025-01-20',
            status='completed'
        )
        
        # Send email
        subject = f'Test: Статус этапа "{task.title}" изменен - Заказ #{order.order_number}'
        html_message = render_to_string('emails/task_status_changed.html', {
            'task': task,
            'site_url': getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
        })
        
        send_mail(
            subject=subject,
            message='',
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

    def test_user_email(self, email):
        """Test user created email"""
        # Create a test user
        user = CustomUser.objects.create(
            email=email,
            full_name='Test User',
            phone='+998901234567'
        )
        
        # Send email
        subject = f'Test: Добро пожаловать в ENGLER House - Ваш аккаунт создан'
        html_message = render_to_string('emails/user_created.html', {
            'user': user,
            'password': 'TestPassword123!',
            'site_url': getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
        })
        
        send_mail(
            subject=subject,
            message='',
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
