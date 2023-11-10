from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import timedelta
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import update_last_login
from django.utils import timezone
from .serializers import UserSerializer
import re

@api_view(['POST'])
def register(request):

    if request.method == 'POST':

        serializer = UserSerializer(data=request.data)

        # Validate the data
        if serializer.is_valid():

            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            # verify data
            if not username or not email or not password:
                return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
            
            if not checkData(username, email, password):
                return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

            # create user
            user = serializer.save()

            refresh = TokenObtainPairSerializer.get_token(user)
            reg_token = str(refresh.access_token)
            reg_token = AccessToken.for_user(user)
            reg_token.set_exp(lifetime=timedelta(minutes=2))
            reg_token_str = str(reg_token)
            #print(reg_token_str)

            return Response({

                'registration_complete': True,
                'reg_token': reg_token_str
                
            }, status=status.HTTP_201_CREATED)
        
        else:

            print(serializer.errors)

            if 'username' in serializer.errors:
                
                return Response({'error': "Username is already taken"}, status=status.HTTP_400_BAD_REQUEST)
            
            elif 'email' in serializer.errors:

                return Response({'error': "Email is already taken"}, status=status.HTTP_400_BAD_REQUEST)

def checkData(username, email, password):
    return is_valid_username(username) and is_valid_email(email) and is_valid_password(password)

def is_valid_username(username):
    return 3 <= len(username) <= 25

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[a-zA-Z0-9\.-]+\.[a-zA-Z]{2,}$'
    return bool(re.fullmatch(pattern, email))

def is_valid_password(password):
    return 6 <= len(password) <= 25

@api_view(['POST'])
def login(request):

    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:

        update_last_login(None, user)
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        try:

            user_data = {

                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'email': user.email
            }

        except AttributeError as e:

            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # The user is authenticated
        refresh = TokenObtainPairSerializer.get_token(user)
        access = str(refresh.access_token)

        serializer = UserSerializer(user)
        
        return Response({

            'refresh': str(refresh),
            'access': access,
            'user': serializer.data

        }, status=status.HTTP_200_OK)
    
    else:
        # Authentication failed
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_auth(request):

    if request.user.is_authenticated:
        
        return Response({"message": "You are authenticated!", 
                         "username": request.user.username, 
                         "email":request.user.email,
                         "user_id": request.user.id}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "You are not authenticated!"}, status=status.HTTP_401_UNAUTHORIZED)
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_account_data(request):

    try:

        user = request.user
        # Use the serializer
        serializer = UserSerializer(user)

        # print(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)