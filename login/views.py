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

@login_required(login_url='/login/')
def student_main(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user, status='student')
        if request.method == "POST":
            if 'class_code' in request.POST:
                class_code = request.POST['class_code']
                if Room.objects.filter(code=class_code).exists():
                    room = Room.objects.get(code=class_code)
                    if room.name not in user_profile.get_rooms():
                        user_profile.add_room(room.name)
                        user_profile.save()

                        if not room.students:
                            room.students = {}
                        room.students[user_profile.user.email] = [0, []]
                        room.save()

                        # messages.success(request, "Room added successfully.")
                        print("Room added successfully")
                    else:
                        messages.error(request, "Room with code '{}' is already in your list of rooms.".format(class_code))
                        print("Room with code '{}' is already in your list of rooms.".format(class_code))
                else:
                    messages.error(request, "Room with code '{}' does not exist.".format(class_code))
            elif 'remove_all_rooms' in request.POST:
                #Roomname = request.POST['room_name_for_removal']
                #theroom = Room.objects.get(code="ca94c44b-4dc0-43e8-864d-0a35c52395d8")
                #theroom.remove_student(user_profile.user.email)
                #theroom.save()
                #print(theroom.students)
                #user_profile.remove_room(Roomname)
                #user_profile.save()
                # Room.remove_student(Roomname, user_profile)
                messages.success(request, "All rooms removed.")

        user_rooms = user_profile.get_rooms()
        user_rooms = list(set(user_rooms))
        class_options = [('', '-- Select a class --')] + [(room, room) for room in user_rooms]

        return render(request, "student_main.html", {'user_profile': user_profile, 'class_options': class_options})
        pass
    except UserProfile.DoesNotExist:
        return redirect("loginpage")

@login_required(login_url='/login/')
def teacher_main(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user, status='teacher')
        if request.method == "POST":
            if 'delete_all_rooms' in request.POST:
                print('Hello World')
                user_profile.adminRoom = {}
                user_profile.save()
                Room.objects.all().delete()
            elif 'get_info' in request.POST:
                room_code = request.POST['get_info']
                room = Room.objects.get(code=room_code)
                students = room.students.items()
                allsubrooms = room.subrooms.items()
                rooms = Room.objects.filter(code__in=[str(code) for code in user_profile.get_admin_room().keys()])
                return render(request, 'teacher_main.html', {'rooms':rooms, 'students': students, 'room':room, 'subrooms':allsubrooms})
            elif 'room_name' in request.POST:
                room_name = request.POST['room_name']
                newroom = Room.create(name=room_name)
                user_profile.add_admin_room(room_name, str(newroom.code))
                user_profile.save()
            elif 'add-sub-room-btn' in request.POST:
                subroom_name = request.POST['subroom-name-input']
                activeroomcode = request.POST['active-room-code']
                activeroom = Room.objects.get(code=activeroomcode)
                Room.add_subroom(activeroom, subroom_name)
                allsubrooms = activeroom.subrooms.items()
                room = Room.objects.get(code=activeroomcode)
                students = room.students.items()
                rooms = Room.objects.filter(code__in=[str(code) for code in user_profile.get_admin_room().keys()])
                return render(request, 'teacher_main.html', {'rooms':rooms, 'students': students, 'room':room, 'subrooms':allsubrooms})
            elif 'delete-sub-room-button' in request.POST:
                if 'subroomname' in request.POST:    
                    subroom_name = request.POST['subroomname']
                    activeroomcode = request.POST['active-room-code']
                    activeroom = Room.objects.get(code=activeroomcode)
                    Room.delete_subroom(activeroom, subroom_name)
                    allsubrooms = activeroom.subrooms.items()
                    room = Room.objects.get(code=activeroomcode)
                    students = room.students.items()
                    rooms = Room.objects.filter(code__in=[str(code) for code in user_profile.get_admin_room().keys()])
                    return render(request, 'teacher_main.html', {'rooms':rooms, 'students': students, 'room':room, 'subrooms':allsubrooms})
            elif 'student-add-button' in request.POST:
                if "student-name-input" in request.POST:
                    student_name = request.POST['student-name-input']
                    subroom_name = request.POST['subroomname']
                    activeroomcode = request.POST['active-room-code']
                    activeroom = Room.objects.get(code=activeroomcode)
                    allsubrooms = activeroom.subrooms.items()
                    room = Room.objects.get(code=activeroomcode)
                    students = room.students.items()
                    studentsinsubroom = room.subrooms[subroom_name]
                    if student_name in room.students.keys():
                        if room.students[student_name][1] == []:
                            room.students[student_name][1].append(subroom_name)
                            studentsinsubroom.append(student_name)
                            room.save()
                            activeroom = Room.objects.get(code=activeroomcode)
                            allsubrooms = activeroom.subrooms.items()
                    rooms = Room.objects.filter(code__in=[str(code) for code in user_profile.get_admin_room().keys()])
                    return render(request, 'teacher_main.html', {'rooms':rooms, 'students': students, 'room':room, 'subrooms':allsubrooms})
            elif 'student-remove-button' in request.POST:
                student_name = request.POST['student_subroom_name']
                subroom_name = request.POST['subroomname']
                activeroomcode = request.POST['active-room-code']
                activeroom = Room.objects.get(code=activeroomcode)
                allsubrooms = activeroom.subrooms.items()
                room = Room.objects.get(code=activeroomcode)
                students = room.students.items()
                studentsinsubroom = room.subrooms[subroom_name]
                room.students[student_name][1].remove(subroom_name)
                studentsinsubroom.remove(student_name)
                room.save()
                activeroom = Room.objects.get(code=activeroomcode)
                allsubrooms = activeroom.subrooms.items()
                rooms = Room.objects.filter(code__in=[str(code) for code in user_profile.get_admin_room().keys()])
                return render(request, 'teacher_main.html', {'rooms':rooms, 'students': students, 'room':room, 'subrooms':allsubrooms})
        rooms = Room.objects.filter(code__in=[str(code) for code in user_profile.get_admin_room().keys()])
        return render(request, 'teacher_main.html', {'rooms':rooms})
    except UserProfile.DoesNotExist:
        return redirect("loginpage")
    # template = loader.get_template('login.html')
    # return HttpResponse(template.render())