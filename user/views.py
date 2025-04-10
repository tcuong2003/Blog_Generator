from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import CustomUser

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)    
            # return redirect('blog_generator:blog_generator_form')
            return redirect('/')
        else:
            error_message = "Invalid username or password"
            return render(request, 'login.html', {'error_message': error_message})
        
    return render(request, 'login.html')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        repeatPassword = request.POST['repeatPassword']

        # Kiểm tra username đã tồn tại hay chưa
        if CustomUser.objects.filter(username=username).exists():
            error_message = 'Username already exists'
            return render(request, 'signup.html', {'error_message': error_message})

        # Kiểm tra password có khớp không
        if password != repeatPassword:
            error_message = 'Passwords do not match'
            return render(request, 'signup.html', {'error_message': error_message})

        try:
            # Tạo user mới
            user = CustomUser.objects.create_user(username=username, password=password)
            user.save()
            login(request, user)
            # return redirect('blog_generator:blog_generator_form')
            return redirect('/')
        except Exception as e:
            error_message = f'Error creating account: {str(e)}'
            return render(request, 'signup.html', {'error_message': error_message})

    return render(request, 'signup.html')

def user_logout(request):
    logout(request)
    return redirect('/')