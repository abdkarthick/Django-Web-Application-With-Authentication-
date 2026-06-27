from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home_page(request):
    return render(request, 'home.html')

def register_user(request):
    if request.method == "POST":
        username_input = request.POST.get("username")
        email_input = request.POST.get("email")
        password_input = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password_input != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "register.html")

        if User.objects.filter(username=username_input).exists():
            messages.error(request, "Username is already taken.")
            return render(request, "register.html")

        new_user = User.objects.create_user(
            username=username_input, 
            email=email_input, 
            password=password_input
        )
        
        regular_group, created = Group.objects.get_or_create(name='RegularUser')
        new_user.groups.add(regular_group)
        new_user.save()
        
        messages.success(request, "Account created successfully. Please login now.")
        return redirect("login_user")

    return render(request, "register.html")

def login_user(request):
    if request.method == "POST":
        username_input = request.POST.get("username")
        password_input = request.POST.get("password")
        authenticated_user = authenticate(request, username=username_input, password=password_input)

        if authenticated_user is not None:
            login(request, authenticated_user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password entered.")

    return render(request, "login.html")

def logout_user(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect("login_user")

@login_required
def dashboard(request):
    user_role = "Admin" if request.user.is_superuser else "Regular User"
    context = {
        'user_role': user_role,
        'username': request.user.username
    }
    return render(request, "dashboard.html", context)