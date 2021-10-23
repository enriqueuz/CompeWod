""" User's views. """

# Django

# REST Framework
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authentication import get_authorization_header
from rest_framework.permissions import AllowAny, IsAuthenticated

# Serializers
from .serializers.users import (
    UserTokenSerializer, 
    UserSignUpSerializer, 
    UserModelSerializer
    )

# Utils
from .utils import delete_user_sessions

class UserViewSet(viewsets.GenericViewSet):
    """ User view set.

    Handle sign up, login and account verification.
    """

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['login', 'signup']:
            permissions = [AllowAny]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]


    @action(detail=False, methods=['post'])
    def login(self, request):
        """ User log in """
        login_serializer = AuthTokenSerializer(
                            data=request.data, 
                            context = {'request': request}
                            )
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            user_serializer = UserTokenSerializer(user)

            if not created:
                delete_user_sessions(user_id=user.id)
                token.delete()
                token = Token.objects.create(user=user)

            return Response({
                            'token': token.key,
                            'user': user_serializer.data,
                            'message': 'Successfully logged in!'
                            }, status=status.HTTP_201_CREATED
                        )
        else:
            return Response({'error':'Wrong email or password'}, 
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User sign up."""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """ User log out. """
        token = request.META.get('HTTP_AUTHORIZATION').split()[-1]
        token = Token.objects.filter(key=token).first()

        if token:
            user = token.user
            delete_user_sessions(user_id=user.id)
            token.delete()

            return Response(
                {'message': 'You have logged out.'}, 
                status=status.HTTP_200_OK
                )

        return Response(
                {'message': 'There is no user with these credentials'}, 
                status=status.HTTP_400_BAD_REQUEST
                )
    
    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User sign up."""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)
