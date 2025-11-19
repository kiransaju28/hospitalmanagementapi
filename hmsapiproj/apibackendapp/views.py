from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView
from .serializers import SignupSerializer
from rest_framework.permissions import AllowAny

class SignupView(CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]   # important
