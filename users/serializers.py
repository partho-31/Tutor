from rest_framework import serializers
from djoser.serializers import UserCreateSerializer,UserSerializer
from users.models import User
from teachers.models import Applicant,StudentsOfTeacher
from teachers.serializers import ForProfileTuitionSerializer



class CustomUserCreateSerializer(UserCreateSerializer):
    image= serializers.ImageField(required=False, allow_null=True)
    class Meta(UserCreateSerializer.Meta):
        fields = ['first_name','last_name','password','email','address','phone_number','role','image']



class CustomUserSerializer(UserSerializer):
    applied_tuition = serializers.SerializerMethodField(method_name= 'check_applied_tuition')
    approved_tuition = serializers.SerializerMethodField(method_name= 'check_approved_tuition')

    class Meta:
        model = User
        fields = ['id','first_name','last_name','email','address','phone_number','image','applied_tuition','approved_tuition']

    def check_applied_tuition(self, obj):
        applicants = Applicant.objects.select_related('tuition').filter(user=obj) 
        return ThirdPartySerializer(applicants,many=True).data
    
    def check_approved_tuition(self,obj):
        student_of_particular_tuition = StudentsOfTeacher.objects.select_related('tuition').filter(user=obj)
        return ThirdPartySerializer(student_of_particular_tuition, many=True).data



class ThirdPartySerializer(serializers.Serializer):
    details = serializers.SerializerMethodField(method_name= 'get_details')
    class Meta:
        fields = ['details']

    def get_details(self,obj):
        return ForProfileTuitionSerializer(obj.tuition).data






