from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from users.models import User
from cloudinary.models import CloudinaryField

  
class Tuition(models.Model):
    Yes = 'Yes'
    No = 'No'
    STATUS_CHOICES = [
        (Yes,'Yes'),
        (No,'No')
    ]

    
    title = models.CharField(max_length=150, blank=False, null=False)
    sub_title = models.CharField(max_length=150, blank=False, null=False)
    description = models.TextField()
    course_content = models.TextField()
    classes = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    duration = models.CharField(max_length=100, blank=True, null=True)
    subjects = models.CharField(max_length= 150)
    availability = models.CharField(max_length= 5, choices=STATUS_CHOICES, default= Yes)
    Enrolled = models.PositiveIntegerField(default=0)
    teacher = models.ForeignKey(User, on_delete= models.CASCADE, related_name= 'tuition')
    fee = models.PositiveBigIntegerField(default= 499, blank=False, null=False)
    outcomes = models.TextField()
    image = CloudinaryField('image')


    def __str__(self):
        return self.title
    

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='review')
    comment = models.CharField(max_length=200, blank=True, null=True)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    tuition = models.ForeignKey(Tuition, on_delete=models.CASCADE, related_name='review')

    def __str__(self):
        return self.comment
    

class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'applicant')
    tuition = models.ForeignKey(Tuition, on_delete=models.CASCADE, related_name= 'applicant')

    def __str__(self):
        return self.user.first_name


class StudentsOfTeacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'student')
    tuition = models.ForeignKey(Tuition, on_delete=models.CASCADE, related_name= 'student')
    teacher = models.ForeignKey(User, on_delete= models.CASCADE, related_name= 'studentOfTeacher')

    def __str__(self):
        return self.user.first_name
    

class Progress(models.Model):
    STARTED = 'Started'
    FIRST_PHASE = '25% Completed'
    SECOND_PHASE = '50% Completed'
    THIRD_PHASE = '75% Completed'
    COMPELETED = '100% Completed'
    STATUS_CHOICES = [
        (STARTED, 'Started'),
        (FIRST_PHASE, '25% Completed'),
        (SECOND_PHASE, '50% Completed'),
        (THIRD_PHASE, '75% Completed'),
        (COMPELETED, '100% Completed'),
    ]

    STATUS_ChOICES2 = [
        ('Doing Well', 'Doing Well'),
        ('Need More Hardwork', 'Need More Hardwork'),
        ('Greate', 'Greate'),
        ('Not So Well', 'Not So Well')
    ]

    topics_for_this_week = models.CharField(max_length=200, blank=False, null=False)
    topics = models.CharField(max_length=15, choices=STATUS_CHOICES, default= 'Started')
    assignment = models.CharField(max_length= 150, default='Coming Soon')
    topics_completed = models.PositiveIntegerField(default=0)
    student_progress = models.CharField(max_length=20, choices=STATUS_ChOICES2, default= 'Doing Well')

    user = models.OneToOneField(User, on_delete= models.CASCADE, related_name= 'progress')
    tuition = models.ForeignKey(Tuition, on_delete= models.CASCADE, related_name= 'progress')