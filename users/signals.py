 
from users.views import profiles
from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
from django.contrib.auth.models import User

from .models import Profile

@receiver(post_save, sender=User)
def createProfile(sender,instance,created,**kwargs):
    print("receiver")
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )

@receiver(post_delete, sender=Profile)
def updateUser(sender,instance,created,**kwargs):
    if created == False:
        profile = instance
        user = profile.user

        user.first_name = profile.name
        user.email = profile.email
        user.save()

@receiver(post_delete, sender=Profile)
def deleteUser(sender, **kwargs):
    user = isinstance.user
    user.delete()

