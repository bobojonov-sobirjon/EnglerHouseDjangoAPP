from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.core.exceptions import ValidationError

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
    
    # GET request - just show the profile page
    return render(request, 'pages/profile.html', {'user': request.user})
