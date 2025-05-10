from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from users.models import User
from users.serializers import CustomUserSerializer,CustomUserCreateSerializer
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from sslcommerz_lib import SSLCOMMERZ 
from rest_framework.response import Response
from django.http import HttpResponse
from django.conf import settings as main_settings



class StudentViewSet(ModelViewSet):
    """
    API endpoints for managing students in tuition media platfrom
    - Allows authenticated admin to create,delete and update students
    - Only addmin is allowed to access this API

    """
    queryset = User.objects.filter(role = 'Student')
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]

    
    @swagger_auto_schema(
        operation_summary= 'Retrive the list of Student'
        )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


    @swagger_auto_schema(
            operation_summary= 'Create students by Admin',
            request_body= CustomUserCreateSerializer,
            responses= {
                201: CustomUserSerializer,
                400: 'Bad Request'
            }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    

    @swagger_auto_schema(
            operation_summary= 'Retrive a single Student'
            )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


    @swagger_auto_schema(
            operation_summary= 'Update data of a Student by Admin',
            request_body= CustomUserCreateSerializer,
            responses= {
                201: CustomUserSerializer,
                400: 'Bad Request'
            }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    

    @swagger_auto_schema(
            operation_summary= 'Partially update data of a Student by Admin',
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


    @swagger_auto_schema(
            operation_summary= 'Delete a single instance of Student by Admin'
            )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)




@api_view(['POST',]) 
def PaymentInitiate(request):
    user = request.user
    amount = request.data.get('amount')

    settings = { 
        'store_id': 'homet681c8efac4942', 
        'store_pass': 'homet681c8efac4942@ssl', 
        'issandbox': True 
        }
    sslcz = SSLCOMMERZ(settings)
    
    post_body = {}
    post_body['total_amount'] = amount
    post_body['currency'] = "BDT"
    post_body['tran_id'] = f'tnx_DF3SH4HJ89EC8D{user.id}'
    post_body['success_url'] = f"{main_settings.BACKEND_URL}/api/payment/success/"
    post_body['fail_url'] = f"{main_settings.BACKEND_URL}/api/payment/failed/"
    post_body['cancel_url'] = f"{main_settings.BACKEND_URL}/api/payment/cancel/"
    post_body['emi_option'] = 0
    post_body['cus_name'] = f"{user.first_name} {user.last_name}"
    post_body['cus_email'] = user.email
    post_body['cus_phone'] = user.phone_number
    post_body['cus_add1'] = user.address
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "Online Tuition"
    post_body['product_category'] = "General"
    post_body['product_profile'] = "general"


    response = sslcz.createSession(post_body) 
    
    if response.get('status') == 'SUCCESS':
        return Response({'payment_url' : response.get('GatewayPageURL')})
    else:  
        return Response({'request' : 'Request failed!','response': response})
 


@api_view(['POST',])
def PaymentSuccess(request):
    return HttpResponse(f'{main_settings.FRONTEND_URL}/payment/success/')  


@api_view(['POST',])
def PaymentCancel(request):
    return HttpResponse(f'{main_settings.FRONTEND_URL}/payment/cancel/')  


@api_view(['POST',])
def PaymentFailed(request):
    return HttpResponse(f'{main_settings.FRONTEND_URL}/payment/failed/')