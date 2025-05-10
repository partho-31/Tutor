from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from api.permissions import IsAdminOrTeacherOrReadOnly,IsAdminOrReadOnly,OnlyForTeacher,StudentCanReadOnly,ReviewAuthorOrAdmin
from api.paginations import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from users.models import User
from teachers.models import Tuition,Review,Applicant,StudentsOfTeacher,Progress
from teachers.serializers import TeacherSerializer,TuitionSerializer,CreateTuitionSerializer,ReviewSerializer,ApplicantSerializer,StudentofTeacherSerializer,ProgressOfStudentSerializer


class TeacherViewSet(ModelViewSet):
    """
    API endpoints for managing teacher in tuition media platfrom
    - Allows authenticated admin to create,delete and update teachers
    - Allows users to view teachers list and details

    """
    queryset = User.objects.filter(role= 'Teacher').all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = CustomPagination

    @swagger_auto_schema(
            operation_summary= 'Retrive the list of Teachers'
            )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
            operation_summary= 'Create a Teachers by Admin',
            request_body= TeacherSerializer,
            responses= {
                201: TeacherSerializer,
                400: 'Bad Request'
            }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
            operation_summary= 'Retrive a single Teacher'
            )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
            operation_summary= 'Update data of a Teacher by Admin',
            request_body= TeacherSerializer,
            responses= {
                201: TeacherSerializer,
                400: 'Bad Request'
            }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
            operation_summary= 'Partially update data of a Teacher by Admin',
            request_body= TeacherSerializer,
            responses= {
                201: TeacherSerializer,
                400: 'Bad Request'
            }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
            operation_summary= 'Delete a single instance of Teacher'
            )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)



class TuitionViewSet(ModelViewSet):
    """
    API endpoints for managing tuition's in tuition media platfrom
    - Allows authenticated admin and teacher to create,delete and update tuitions
    - Allows users to view tuition list and details
    - Allows authenticated users to apply for a tuition
    - Allows authenticated users to see progress in their particular enrolled tuition
    - Support filtering by subjects,classes and teacher

    """
    queryset = Tuition.objects.prefetch_related('teacher').all()
    serializer_class = TuitionSerializer
    permission_classes = [IsAdminOrTeacherOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['subjects','classes','teacher']
    pagination_class = CustomPagination


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateTuitionSerializer
        return TuitionSerializer

    def perform_create(self, serializer):
        serializer.save(teacher = self.request.user)


    @swagger_auto_schema(
            operation_summary= 'Create applications for Tuition',
    )
    @action(methods=['get'], detail=True)
    def apply_for_tuition(self, request, pk=None):
        tuition = Tuition.objects.get(id= pk)
        user = self.request.user

        applicant, created = Applicant.objects.get_or_create(user=user, tuition=tuition)
        if not created:
            return Response({'message':'You have already taken this tuition'}, status= status.HTTP_208_ALREADY_REPORTED)
        
        serializer = ApplicantSerializer(applicant)
        return Response(serializer.data, status= status.HTTP_201_CREATED) 
    

    @swagger_auto_schema(
            operation_summary= 'Progress of student in enrolled tuition',
    )
    @action(methods=['get'],detail=True)
    def see_progress(self,request,pk=None):
        user = self.request.user
        tuition = Tuition.objects.get(id= pk)

        progress, created = Progress.objects.get_or_create(user= user, tuition=tuition)
        if not created:
            return Response({'message': 'Applicant is already taken'}, status= status.HTTP_208_ALREADY_REPORTED)
        
        serializer = ProgressOfStudentSerializer(progress)
        return Response(serializer.data, status= status.HTTP_201_CREATED)


    @swagger_auto_schema(
        operation_summary= 'Retrive the list of Tuitions'
        )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
            operation_summary= 'Create a Tuition by Teacher/Admin',
            request_body= CreateTuitionSerializer,
            responses= {
                201: TuitionSerializer,
                400: 'Bad Request'
            }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
            operation_summary= 'Retrive a single Tuition'
            )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
            operation_summary= 'Update data of a Tuition by Teacher/Admin',
            request_body= CreateTuitionSerializer,
            responses= {
                201: TuitionSerializer,
                400: 'Bad Request'
            }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
            operation_summary= 'Partially update data of a Tuition by Teacher/Admin',
            request_body= CreateTuitionSerializer,
            responses= {
                201: TuitionSerializer,
                400: 'Bad Request'
            }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
            operation_summary= 'Delete a single instance of Tuition by Teacher/Admin'
            )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)



class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [ReviewAuthorOrAdmin]

    def get_queryset(self):
        return Review.objects.filter(tuition_id= self.kwargs.get('tuition_pk'))
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def get_serializer_context(self):
        tuition_id = self.kwargs.get('tuition_pk')
        return {'tuition_id': tuition_id}
    


class ApplicantViewSet(ModelViewSet):
    http_method_names = ['get','delete']
    serializer_class = ApplicantSerializer
    permission_classes = [OnlyForTeacher]

    def get_queryset(self):
        return Applicant.objects.filter(tuition_id= self.kwargs.get('tuition_pk'))
    
    @action(methods=['get'],detail=True)
    def select_student(self,request, tuition_pk=None, pk=None):
        applicant = Applicant.objects.get(id= self.kwargs.get('pk'))
        tuition = Tuition.objects.get(id= self.kwargs.get('tuition_pk'))

        student, created = StudentsOfTeacher.objects.get_or_create(user=applicant.user, tuition=tuition, teacher=self.request.user)
        if not created:
            return Response({'message': 'Applicant is already taken'}, status=status.HTTP_208_ALREADY_REPORTED)

        serializer = StudentofTeacherSerializer(student)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        



class StudentOfTeacherViewSet(ModelViewSet):
    """
    API endpoints for managing student of a Teacher in tuition media platfrom
    - Allows authenticated admin and teacher to update and delete
    - Allows teacher to mark topics and give assignment to student

    """
    http_method_names = ['get','delete']
    serializer_class = StudentofTeacherSerializer
    permission_classes = [OnlyForTeacher]

    def get_queryset(self):
        teacher = User.objects.get(id= self.kwargs.get('teacher_pk'))
        return StudentsOfTeacher.objects.filter(teacher= teacher)

    @swagger_auto_schema(
        operation_summary= 'Retrive the list of student under a Teacher'
        )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
            operation_summary= 'Retrive a single student under a Teacher'
            )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
            operation_summary= 'Delete a single instance of Student '
            )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    



class StudentsProgressViewSet(ModelViewSet):
    serializer_class = ProgressOfStudentSerializer
    permission_classes = [StudentCanReadOnly]

    def get_queryset(self):
        tuition = Tuition.objects.get(id = self.kwargs.get('tuition_pk'))
        return Progress.objects.filter(tuition = tuition)