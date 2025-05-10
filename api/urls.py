from django.urls import path,include
from teachers.views import TeacherViewSet,TuitionViewSet,ReviewViewSet,ApplicantViewSet,StudentOfTeacherViewSet,StudentsProgressViewSet
from users.views import StudentViewSet,PaymentInitiate,PaymentSuccess,PaymentCancel,PaymentFailed
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('students',StudentViewSet,basename= 'student')
router.register('teachers',TeacherViewSet,basename= 'teacher')
router.register('tuitions',TuitionViewSet,basename= 'tuition')

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
    path('payment/success/',PaymentSuccess, name= 'payment-success'),
    path('payment/cancel/',PaymentCancel, name= 'payment-cancel'),
    path('payment/failed/',PaymentFailed, name= 'payment-failed'),
]
