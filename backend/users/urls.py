# """ Users URL's. """

# # Django
# from django.urls import path

# # Views
# from .views import Login

# urlpatterns = [
#     path('login/', Login.as_view(), name='login'),
# ]

""" Users URL's """

# Django
from django.urls import include, path

# Views
from . import views as user_views

# Django REST Framework
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', user_views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls))

]
# urlpatterns = router.urls