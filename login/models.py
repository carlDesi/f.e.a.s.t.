from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, blank=True)

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

    def __str__(self):
        return self.name
    
    @classmethod
    def create(cls, name, code=None):
        if code is None:
            code = uuid.uuid4()
        room = cls(name=name, code=code)
        room.save()
        return room
    
def getRooms():
    rooms = Room.objects.all()
    for room in rooms:
        print(room.name + str(room.code))

def getUserProfiles():
    users = UserProfile.objects.all()
    for user in users:
        print("Username : Password : T/S")
        print(str(user.user.username) + " : " + str(user.user.password) + " : " + str(user.status))


getUserProfiles()
# deleteUsers()
#to delete items from database:
# # from login.models import Room
# # Room.objects.all().delete()