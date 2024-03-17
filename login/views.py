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

def signup(request):
    if request.method == "POST":
        username = request.POST['email']
        email = request.POST['email']
        password = request.POST['password']
        myuser = User.objects.create_user(username, email, password)
        myuser.save()
        
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

        user = authenticate(username=username, email=email, password=password)
        if user is not None:
            if email == "john@student.edu":
                login(request, user)
                return redirect("student_main")
            elif email == "martha@teacher.edu":
                login(request, user)
                return redirect("teacher_main")

        else:
            return redirect('loginerror')
   
    return render(request, "loginpage.html")

def loginerror(request):
    return render(request, "loginerror.html")

def student_main(request):
    return render(request, "student_main.html")

def teacher_main(request):
        if request.method == "POST":
            title = request.POST['name']
            newroom = Room.create(name=title)
            return redirect("teacher_main")
        else:
            rooms = Room.objects.all()
            return render(request, 'teacher_main.html', {'rooms': rooms})
            

    # template = loader.get_template('login.html')
    # return HttpResponse(template.render())