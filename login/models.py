from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, blank=True)

    rooms = models.CharField(max_length=255, blank=True, help_text='Comma-separated list of room names')
    adminRoom = models.JSONField(default=dict)

    def add_room(self, room_name, student_score=0):
        if not self.rooms:
            self.rooms = room_name
        else:
            self.rooms += ',{}'.format(room_name)

    def remove_room(self, room_name):
        if self.rooms:
            room_names = self.rooms.split(',')
            room_names = [rn.strip() for rn in room_names if rn.strip()]
            room_names = [rn for rn in room_names if rn != room_name]
            self.rooms = ','.join(room_names)

    def get_rooms(self):
        if self.rooms:
            return self.rooms.split(',')
        else:
            return []
        
    def get_admin_room(self):
        return self.adminRoom
    
    def add_admin_room(self, room_name, room_uuid):
        if room_name not in self.adminRoom:
            self.adminRoom[room_uuid] = room_name

def getUsers():
    users = User.objects.all()
    print ("Username : Password : Email : Status")
    # for user in users:
        # print(user.username + " : " + user.password + " : " + user.email + " : " + user.status)
def deleteUsers():
    users = User.objects.all()
    for user in users:
        print(user.username + " : " + user.password + " : " + user.email)
    users.delete()

class Room(models.Model):
    name = models.CharField(max_length=255)
    code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    students = models.JSONField(default=dict)
    subrooms = models.JSONField(default=dict)

    def __str__(self):
        return self.name
    
    def delete_all_rooms():
        rooms = Room.objects.all()
        rooms.delete()
    
    @classmethod
    def create(cls, name, code=None):
        if code is None:
            code = uuid.uuid4()
        room = cls(name=name, code=code)
        room.save()
        return room
    
    def remove_student(self, student_name):
        if student_name in self.students:
            del self.students[student_name]
            self.save()

    def add_student_in_subroom(self, student_name, subroom_name):
        if student_name not in self.subroom_name.values():
            self.subrooms

    def add_subroom(self, subroom_name):
        if subroom_name not in self.subrooms:
            self.subrooms[subroom_name] = []
            self.save()

    def delete_subroom(self, subroom_name):
        if subroom_name in self.subrooms:
            del self.subrooms[subroom_name]
            self.save()
    
def getRooms():
    rooms = Room.objects.all()
    for room in rooms:
        print(room.name + " " + str(room.code) + " " + str(room.students))

def getUserProfiles():
    users = UserProfile.objects.all()
    for user in users:
        print("Username : Password : T/S : Student_Rooms : Teacher_Rooms")
        print(str(user.user.username) + " : " + str(user.user.password) + " : " + str(user.status) + " : " + str(user.get_rooms()) + " : " + str(user.get_admin_room()))

# getUserProfiles()
getRooms()
# deleteUsers()
#to delete items from database:
# # from login.models import Room
# # Room.objects.all().delete()