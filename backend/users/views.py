""" User's views. """

# Django
from django.contrib.sessions.models import Session

# REST Framework
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer

# Serializers
from .serializers import UserTokenSerializer

# Utils
from datetime import datetime

# class Login(ObtainAuthToken):
#     """ Login view."""

#     def post(self, request, *args, **kwargs):
#         login_serializer = self.serializer_class(
#                             data=request.data, 
#                             context = {'request': request}
#                             )
#         if login_serializer.is_valid():
#             user = login_serializer.validated_data['user']
#             token, created = Token.objects.get_or_create(user=user)
#             user_serializer = UserTokenSerializer(user)

#             if not created:
#                 # If user logs in again delete previous session
#                 all_sessions = Session.objects.filter(
#                                 expire_date__gte=datetime.now()
#                                 )
#                 if all_sessions.exists():
#                     for session in all_sessions:
#                         session_data = session.get_decoded()
#                         if user.id == int(session_data.get('_auth_user_id')):
#                             session.delete()
                            
#                 token.delete()
#                 token = Token.objects.create(user=user)

#             return Response({
#                             'token': token.key,
#                             'user': user_serializer.data,
#                             'message': 'Successfully logged in!'
#                             }, status=status.HTTP_201_CREATED
#                         )
#         else:
#             return Response({'error':'Wrong email or password'}, 
#                             status=status.HTTP_400_BAD_REQUEST)
        
        # return Response({'message':'Hola desde response'}, status=status.HTTP_200_OK)

class UserViewSet(viewsets.GenericViewSet):
    """ User view set.

    Handle sign up, login and account verification.
    """
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
                # If user logs in again delete previous session
                all_sessions = Session.objects.filter(
                                expire_date__gte=datetime.now()
                                )
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()
                            
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
