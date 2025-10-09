from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
import json
from .models import HeroSection, Service, Project, ProjectCarousel, ProjectDetails, GalleryImage, Press, PressItem, Architect, Review, ContactInfo, Zayavka, Order, OrderTask


def home(request):
    """Home page view with all dynamic content"""
    # Get active hero section
    hero = HeroSection.objects.filter(is_active=True).first()
    
    # Get gallery images - only show if we have exactly 10 images
    gallery_count = GalleryImage.objects.filter(is_active=True).count()
    show_gallery = gallery_count >= 10
    
    context = {
        'hero': hero,
        'services': Service.objects.filter(is_active=True)[:4],
        'projects': Project.objects.filter(is_active=True)[:3],
        'show_gallery': show_gallery,
        'gallery_1': GalleryImage.objects.filter(is_active=True, order=1).first() if show_gallery else None,
        'gallery_2': GalleryImage.objects.filter(is_active=True, order=2).first() if show_gallery else None,
        'gallery_3': GalleryImage.objects.filter(is_active=True, order=3).first() if show_gallery else None,
        'gallery_4': GalleryImage.objects.filter(is_active=True, order=4).first() if show_gallery else None,
        'gallery_5': GalleryImage.objects.filter(is_active=True, order=5).first() if show_gallery else None,
        'gallery_6': GalleryImage.objects.filter(is_active=True, order=6).first() if show_gallery else None,
        'gallery_7': GalleryImage.objects.filter(is_active=True, order=7).first() if show_gallery else None,
        'gallery_8': GalleryImage.objects.filter(is_active=True, order=8).first() if show_gallery else None,
        'gallery_9': GalleryImage.objects.filter(is_active=True, order=9).first() if show_gallery else None,
        'gallery_10': GalleryImage.objects.filter(is_active=True, order=10).first() if show_gallery else None,
        'press': Press.objects.filter(is_active=True).first(),
        'press_items': PressItem.objects.filter(is_active=True)[:4],
        'architects': Architect.objects.filter(is_active=True)[:4],
    }
    return render(request, 'index.html', context)


def services(request):
    """Services page view"""
    context = {
        'services': Service.objects.filter(is_active=True),
    }
    return render(request, 'pages/services.html', context)


def projects(request):
    """Projects page view"""
    # Get gallery images - only show if we have at least 10 images
    gallery_count = GalleryImage.objects.filter(is_active=True).count()
    show_gallery = gallery_count >= 10
    
    context = {
        'projects': Project.objects.filter(is_active=True),
        'show_gallery': show_gallery,
        'gallery_1': GalleryImage.objects.filter(is_active=True, order=1).first() if show_gallery else None,
        'gallery_2': GalleryImage.objects.filter(is_active=True, order=2).first() if show_gallery else None,
        'gallery_3': GalleryImage.objects.filter(is_active=True, order=3).first() if show_gallery else None,
        'gallery_4': GalleryImage.objects.filter(is_active=True, order=4).first() if show_gallery else None,
        'gallery_5': GalleryImage.objects.filter(is_active=True, order=5).first() if show_gallery else None,
        'gallery_6': GalleryImage.objects.filter(is_active=True, order=6).first() if show_gallery else None,
        'gallery_7': GalleryImage.objects.filter(is_active=True, order=7).first() if show_gallery else None,
        'gallery_8': GalleryImage.objects.filter(is_active=True, order=8).first() if show_gallery else None,
        'gallery_9': GalleryImage.objects.filter(is_active=True, order=9).first() if show_gallery else None,
        'gallery_10': GalleryImage.objects.filter(is_active=True, order=10).first() if show_gallery else None,
    }
    return render(request, 'pages/projects.html', context)


def architects(request):
    """Architects page view"""
    # Get gallery images - only show if we have at least 10 images
    gallery_count = GalleryImage.objects.filter(is_active=True).count()
    show_gallery = gallery_count >= 10
    
    context = {
        'architects': Architect.objects.filter(is_active=True),
        'show_gallery': show_gallery,
        'gallery_1': GalleryImage.objects.filter(is_active=True, order=1).first() if show_gallery else None,
        'gallery_2': GalleryImage.objects.filter(is_active=True, order=2).first() if show_gallery else None,
        'gallery_3': GalleryImage.objects.filter(is_active=True, order=3).first() if show_gallery else None,
        'gallery_4': GalleryImage.objects.filter(is_active=True, order=4).first() if show_gallery else None,
        'gallery_5': GalleryImage.objects.filter(is_active=True, order=5).first() if show_gallery else None,
        'gallery_6': GalleryImage.objects.filter(is_active=True, order=6).first() if show_gallery else None,
        'gallery_7': GalleryImage.objects.filter(is_active=True, order=7).first() if show_gallery else None,
        'gallery_8': GalleryImage.objects.filter(is_active=True, order=8).first() if show_gallery else None,
        'gallery_9': GalleryImage.objects.filter(is_active=True, order=9).first() if show_gallery else None,
        'gallery_10': GalleryImage.objects.filter(is_active=True, order=10).first() if show_gallery else None,
    }
    return render(request, 'pages/architects.html', context)


def works_progress(request, project_id):
    """Works progress page view"""
    project = get_object_or_404(Project, id=project_id, is_active=True)
    print(project.model_3d_file)
    carousel_images = ProjectCarousel.objects.filter(project=project, is_active=True)
    project_details = ProjectDetails.objects.filter(project=project, is_active=True)
    
    # Handle review submission
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        comment = request.POST.get('comment', '').strip()
        
        if first_name and last_name and comment:
            Review.objects.create(
                project=project,
                first_name=first_name,
                last_name=last_name,
                comment=comment,
                is_active=False  # Requires admin approval
            )
            messages.success(request, 'Спасибо за ваш отзыв! Он будет опубликован после модерации.')
            return redirect('works_progress', project_id=project_id)
        else:
            messages.error(request, 'Пожалуйста, заполните все поля.')
    
    context = {
        'project': project,
        'carousel_images': carousel_images,
        'project_details': project_details,
    }
    return render(request, 'pages/works-progress.html', context)


def about(request):
    """About/Press page view"""
    context = {
        'press': Press.objects.filter(is_active=True).first(),
        'press_items': PressItem.objects.filter(is_active=True),
        'reviews': Review.objects.filter(is_active=True)[:4],
    }
    return render(request, 'pages/about.html', context)


def contact(request):
    """Contact page view"""
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    context = {
        'contact_info': contact_info,
    }
    return render(request, 'pages/contact.html', context)


@csrf_exempt
def submit_zayavka(request):
    """Handle feedback form submission"""
    if request.method == 'POST':
        try:
            # Parse JSON data
            data = json.loads(request.body)
            name = data.get('name', '').strip()
            email = data.get('email', '').strip()
            phone = data.get('phone', '').strip()
            
            # Validate data
            if not name or not email or not phone:
                return JsonResponse({
                    'success': False,
                    'message': 'Пожалуйста, заполните все поля.'
                }, status=400)
            
            # Create zayavka
            zayavka = Zayavka.objects.create(
                name=name,
                email=email,
                phone=phone
            )
            
            # Send email notification
            try:
                subject = '🔔 Новая заявка на ENGLER House'
                message = f"""
Здравствуйте!

Вам поступила новая заявка на обратную связь:

👤 Имя: {name}
📧 Почта: {email}
📱 Телефон: {phone}
🕐 Дата: {zayavka.created_at.strftime('%d.%m.%Y в %H:%M')}

---
Перейдите в админ-панель для просмотра и обработки заявки.
                """
                
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Error sending email: {e}")
                # Don't fail the request if email fails
            
            return JsonResponse({
                'success': True,
                'message': 'Спасибо! Ваша заявка принята. Мы свяжемся с вами в ближайшее время.'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Неверный формат данных.'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Произошла ошибка: {str(e)}'
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'message': 'Метод не разрешен.'
    }, status=405)


def tour_3d(request):
    """3D tour page view"""
    return render(request, '3d_tour/tour.html')


def my_projects(request):
    """My projects page with order tracking and Gantt chart"""
    # Filter orders by current user
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
    else:
        # For demo purposes show all if not authenticated
        # In production you should redirect to login
        orders = Order.objects.all().order_by('-created_at')
    
    # Prepare Gantt chart data for each order
    for order in orders:
        tasks = order.tasks.all()
        
        # Calculate timeline
        if tasks.exists():
            min_date = min(task.start_date for task in tasks)
            max_date = max(task.end_date for task in tasks)
            total_days = (max_date - min_date).days + 1
            
            for task in tasks:
                # Calculate position and width for Gantt bar
                days_from_start = (task.start_date - min_date).days
                task_duration = (task.end_date - task.start_date).days + 1
                
                task.position_percent = (days_from_start / total_days) * 100
                task.width_percent = (task_duration / total_days) * 100
            
            order.task_list = tasks
            order.timeline_start = min_date
            order.timeline_end = max_date
            order.total_duration_days = total_days
        else:
            order.task_list = []
            order.timeline_start = order.start_date
            order.timeline_end = order.end_date
            order.total_duration_days = (order.end_date - order.start_date).days + 1
    
    context = {
        'orders': orders,
    }
    return render(request, 'pages/my-projects.html', context)