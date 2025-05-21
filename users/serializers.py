from rest_framework import serializers
from djoser.serializers import UserCreateSerializer,UserSerializer
from users.models import User,ProfileInfo,Payment
from teachers.models import Applicant,StudentsOfTeacher
from teachers.serializers import ForProfileTuitionSerializer



class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ['first_name','last_name','password','email','address','phone_number','role','institute','profession','bio','qualifications','experience']

    def create(self, validated_data):
        user = super().create(validated_data)
        ProfileInfo.objects.create(user=user)
        return user


class CustomUserSerializer(UserSerializer):
    applied_tuition = serializers.SerializerMethodField(method_name= 'check_applied_tuition')
    approved_tuition = serializers.SerializerMethodField(method_name= 'check_approved_tuition')

    profile_info = serializers.SerializerMethodField(method_name='get_profile_info')

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'profile_info','applied_tuition','approved_tuition','institute','profession','bio','qualifications','experience','role')
    
    def get_profile_info(self, obj):
        profile = ProfileInfo.objects.get(user=obj)
        return {
            'image': profile.image.url if profile.image else None
        }

   
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


class ProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required = False, allow_null=True)
    class Meta:
        model = ProfileInfo
        fields = ['image']

        

class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name= 'get_user')
    class Meta:
        model = Payment
        fields = ['user','tran_id','amount','created_at' ]

    def get_user(self,obj):
        return CustomUserSerializer(obj.user).data




 