from django.contrib import admin
from teachers.models import Tuition,Review,Applicant,StudentsOfTeacher,Progress


admin.site.register(Tuition)
admin.site.register(Review)
admin.site.register(Applicant)
admin.site.register(StudentsOfTeacher)
admin.site.register(Progress)