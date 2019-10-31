from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

from .serializers import UserSerializer


class Registration(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer