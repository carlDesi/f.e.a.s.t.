from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.http import JsonResponse
# Create your views here.
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Room
from .models import UserProfile
from django.contrib.auth.decorators import login_required


def signup(request):
    if request.method == "POST":
        username = request.POST['email']
        email = request.POST['email']
        password = request.POST['password']
        status = request.POST['status']

        myuser = User.objects.create_user(username, email, password)

        myprofile = UserProfile.objects.create(user=myuser)
        myprofile.status = status

        myprofile.save()

        # myuser.save()
        
        messages.success(request, "Account successfully created")
    
        return redirect('loginpage')
    
    return render(request, "signup.html")
    # template = loader.get_template('signup.html')
    # return HttpResponse(template.render())

def loginpage(request):
    if request.method == "POST":
        username = request.POST['email']
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            try:
                user_profile = UserProfile.objects.get(user=user)
                if user_profile.status == 'student':
                    login(request, user)
                    return redirect("student_main")
                elif user_profile.status == 'teacher':
                    login(request, user)
                    return redirect("teacher_main")
            except UserProfile.DoesNotExist:
                return render(request, "loginpage.html", {"error": "User profile not found."})

        else:
            return render(request, "loginpage.html", {"error": "Invalid email or password."})

    return render(request, "loginpage.html")

def loginerror(request):
    return render(request, "loginerror.html")

@login_required
def student_main(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user, status='student')
        return render(request, "student_main.html")
        pass
    except UserProfile.DoesNotExist:
        return redirect("loginpage")

@login_required
def teacher_main(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user, status='teacher')
        if request.method == "POST":
            title = request.POST['name']
            newroom = Room.create(name=title)
            return redirect("teacher_main")
        else:
            rooms = Room.objects.all()
            return render(request, 'teacher_main.html', {'rooms': rooms})
        pass
    except UserProfile.DoesNotExist:
        return redirect("loginpage")

    # template = loader.get_template('login.html')
    # return HttpResponse(template.render())