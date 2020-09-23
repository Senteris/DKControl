from rest_framework import permissions
from rest_framework.routers import APIRootView
from rest_framework.viewsets import ModelViewSet, ViewSet

from main.models import User
from api.serializers import UserSerializer


class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class OverviewView(APIRootView):
    pass


