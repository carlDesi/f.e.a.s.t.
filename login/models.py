from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
def getUsers():
    users = User.objects.all()
    print ("Username : Password : Email")
    for user in users:
        print(user.username + " : " + user.password + " : " + user.email)

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

getRooms()

#to delete items from database:
# # from login.models import Room
# # Room.objects.all().delete()