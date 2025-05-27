from django.urls import path,include
from teachers.views import TeacherViewSet,TuitionViewSet,ReviewViewSet,ApplicantViewSet,StudentOfTeacherViewSet,StudentsProgressViewSet,BlogsViewSet
from users.views import StudentViewSet,ContactViewSet,PaymentInitiate,PaymentSuccess,PaymentCancel,PaymentFailed,update_profile,PaymentHistory
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('students', StudentViewSet, basename= 'student')
router.register('teachers', TeacherViewSet, basename= 'teacher')
router.register('tuitions', TuitionViewSet, basename= 'tuition')
router.register('blogs', BlogsViewSet, basename='blog')
router.register('contact', ContactViewSet, basename='contact')

tuition_router = routers.NestedDefaultRouter(router, 'tuitions', lookup='tuition')
tuition_router.register('reviews',ReviewViewSet,basename= 'tuition-review')

applicant_router = routers.NestedDefaultRouter(router,'tuitions',lookup= 'tuition')
applicant_router.register('applicants',ApplicantViewSet,basename='tuition-applicant')

progress_router = routers.NestedDefaultRouter(router,'tuitions',lookup= 'tuition')
progress_router.register('progress',StudentsProgressViewSet,basename='tuition-progress')

student_router = routers.NestedDefaultRouter(router, 'teachers', lookup='teacher')
student_router.register('students', StudentOfTeacherViewSet, basename='teacher-student')

urlpatterns = [
    path('',include(router.urls)),
    path('',include(tuition_router.urls)),
    path('',include(applicant_router.urls)),
    path('',include(student_router.urls)),
    path('',include(progress_router.urls)),
    path('payment/initiate',PaymentInitiate, name= 'payment-initiate'),
    path('payment/success/<int:id>/',PaymentSuccess, name= 'payment-success'),
    path('payment/cancel/',PaymentCancel, name= 'payment-cancel'),
    path('payment/failed/',PaymentFailed, name= 'payment-failed'),
    path('profile/update/',update_profile,name= 'profile-update'), 
    path('payment_history/',PaymentHistory,name= 'payment-history'), 
    
]
