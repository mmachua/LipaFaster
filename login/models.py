from django.db import models
#from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
#from home.forms import UserProfile
User = settings.AUTH_USER_MODEL


#class UserProfileManager(models.Manager):
#    pass
# Create your models here.
class UserProfile(models.Model):
    User =models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    description = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100,  blank=True)
    website = models.URLField(max_length=100, blank=True)
    phone = models.IntegerField(default=0, blank=True)
    image = models.ImageField(upload_to='profile_image', blank=True)

    def __str__(self):
        return self.User.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        User_Profile = UserProfile.objects.create(User=kwargs['instance'])
        #User_profile=UserProfile.objects.create(user=kwargs['instance'])



post_save.connect(create_profile, sender=User)

