from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import *


@api_view(['POST'])
def signup(request):
    data = request.data
    user = UserSerializer(data=data)

    if not user.is_valid(raise_exception=True):
        return Response({'status': 400, 'message': "Something went wrong"}, status=400)

    user.save()
    auth_user = AuthUserSerializer(data={'username': user.data['email'], 'password': user.data['password']})
    if not auth_user.is_valid(raise_exception=True):
        return Response({'status': 400, 'message': "Something went wrong"}, status=400)

    auth_user.save()
    return Response({'status': 201, 'message': "User signed up"}, status=201)


@api_view(['POST'])
def login(request):
    data = request.data
    credentials = LoginSerializer(data=data)
    if not credentials.is_valid(raise_exception=True):
        return Response({'status': 400, 'message': "Something went wrong"}, status=400)

    auth_user = AuthUser.objects.filter(username=credentials.data['email'], password=credentials.data['password'], is_active=True).first()
    if not auth_user:
        return Response({'status': 400, 'message': "Email or Password  is not valid"}, status=400)

    token = RefreshToken.for_user(auth_user)

    return Response({'status': 200, 'message': 'Login Successful', 'token': {'refresh': str(token), 'access': str(token.access_token)}})
