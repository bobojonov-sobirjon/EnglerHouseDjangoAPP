from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from apps.website.models import Order

User = get_user_model()


@csrf_protect
def login_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect('profile')
    
    # Check for logout message in session
    if 'logout_message' in request.session:
        messages.success(request, request.session['logout_message'])
        del request.session['logout_message']
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, 'Пожалуйста, заполните все поля')
            return render(request, 'pages/login.html', {'email': email})
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.first_name}!')
                return redirect('profile')
            else:
                messages.error(request, 'Ваш аккаунт деактивирован')
        else:
            messages.error(request, 'Неверный email или пароль')
    
    return render(request, 'pages/login.html', {'email': request.POST.get('email', '')})

@login_required
def logout_view(request):
    logout(request)
    # Use session to store message after logout
    request.session['logout_message'] = 'Вы успешно вышли из системы'
    return redirect('login')

@login_required
def profile_view(request):
    if request.method == 'POST':
        # Handle profile update
        user = request.user
        
        # Update basic profile information
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        user.patronymic = request.POST.get('patronymic', '').strip()
        
        # Save user profile
        try:
            user.save()
            messages.success(request, 'Профиль успешно обновлен')
        except Exception as e:
            messages.error(request, f'Ошибка при обновлении профиля: {str(e)}')
            return render(request, 'pages/profile.html', {'user': user})
    
        return render(request, 'pages/profile.html', {'user': request.user})
    
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
    
    # GET request - just show the profile page
    return render(request, 'pages/profile.html', {'user': request.user, 'orders': orders})
