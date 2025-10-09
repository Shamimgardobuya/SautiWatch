from django.shortcuts import render
from .forms import UsersForm, LoginForm
from .models import CustomUser
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
# Create your views here.

def create_user(request):
    if request.method == 'POST':
        form = UsersForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            # Auto-generate username from first and last name
            username = f"{first_name.lower()}_{last_name.lower()}"

            CustomUser.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )          
            return render(request, 'users/landing_page.html')
    else:
        form = UsersForm()
    return render(request, 'users/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                customuser = CustomUser.objects.get(email=email)
                if check_password(password, customuser.password):
                    # Successful login
                    return render(request, 'users/landing_page.html')
                else:
                    form.add_error('password', 'Invalid password')
            except CustomUser.DoesNotExist:
                form.add_error('email', 'No user found with that email')
    else:
        form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form})

    
def logout_user(request):
    logout(request)
    return redirect('login_user')
    