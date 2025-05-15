from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import CustomUserManager
from cloudinary.models import CloudinaryField
from django.conf import settings

class User(AbstractUser):
    Teacher = 'Teacher'
    Student = 'Student'
    STATUS_CHOICES = [
        (Teacher,'Teacher'),
        (Student,'Student')
    ]

    username = None
    email = models.EmailField( unique= True)
    address = models.CharField(max_length= 200, blank= True, null= True)
    phone_number = models.CharField(max_length= 15, blank= True, null= True)
    role = models.CharField(max_length=8, choices= STATUS_CHOICES, default= 'Student')
    institute = models.CharField(max_length=200, blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)
    experience = models.CharField(max_length=200,default="Student" ,blank=True, null=True)
    image= CloudinaryField('image',default='profile_pozuuv',blank=True,null=True)
   
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.get_full_name()
    


    

