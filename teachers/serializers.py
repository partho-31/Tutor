from rest_framework import serializers
from teachers.models import Tuition,Review,Applicant,StudentsOfTeacher,Progress
from users.models import User



class TeacherSerializer(serializers.ModelSerializer):
    provided_tuitions = serializers.SerializerMethodField(method_name= 'get_all_tuitions')
    class Meta:
        model = User
        fields = ['id','first_name','last_name','email','address','phone_number','provided_tuitions']

    def get_all_tuitions(self,obj):
        tuition = Tuition.objects.filter(teacher_id= obj.id)
        return ForProfileTuitionSerializer(tuition, many=True).data



class ForProfileTuitionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    subjects = serializers.CharField()
    class Meta:
        fields = ['id','title','subjects']



class CreateTuitionSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = Tuition
        fields = ['title','teacher','description','classes','subjects','availability','image','sub_title','duration','course_content','fee','outcomes']
        read_only_fields = ['teacher']



class TuitionSerializer(serializers.ModelSerializer):
    teacher = serializers.SerializerMethodField(method_name='get_teacher_details')
    
    class Meta:
        model = Tuition
        fields = ['id','teacher','title','description','classes','subjects','availability','image','sub_title','duration','course_content','fee','outcomes']

    def get_teacher_details(self,obj):
        return obj.teacher.first_name



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','user','comment','rating']
        read_only_fields = ['user']

    def create(self, validated_data):
        tuition = Tuition.objects.get(id = self.context.get('tuition_id'))
        return Review.objects.create(tuition= tuition,**validated_data)



class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = ['id','user','tuition']



class StudentofTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentsOfTeacher
        fields = ['id','user','tuition']



class ProgressOfStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ['id','topics_for_this_week','topics','assignment','topics_completed','student_progress','user']