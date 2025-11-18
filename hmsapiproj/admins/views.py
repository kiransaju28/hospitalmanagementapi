from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# --- CORRECT IMPORT: Import models from apibackendapp ---
from apibackendapp.models import Staff, Specialization, Doctor

from .serializers import (
    StaffSerializer, 
    SpecializationSerializer, 
    DoctorSerializer,
    UserSerializer,
    SignupSerializer,
    LoginSerializer
)

from .permissions import (
    AdminOnlyPermissions,
    StaffManagementPermissions,
    DoctorSelfViewPermissions
)

# --- Helper Function to Generate Tokens ---
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    
    def get_permissions(self):
        """
        Allow any user to POST (Sign up as Staff).
        Restrict other actions based on StaffManagementPermissions.
        """
        if self.action == 'create':
            return [AllowAny()]
        return [StaffManagementPermissions()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save the Staff instance (which also creates the User via serializer logic)
        staff_instance = serializer.save()
        
        # Generate Tokens for the newly created user
        user = staff_instance.user
        tokens = get_tokens_for_user(user)
        
        # Prepare custom response
        response_data = serializer.data
        response_data['tokens'] = tokens
        response_data['role'] = "Staff"
        
        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    permission_classes = [StaffManagementPermissions]

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def get_permissions(self):
        """
        Allow any user to POST (Sign up as Doctor).
        Restrict other actions based on DoctorSelfViewPermissions.
        """
        if self.action == 'create':
            return [AllowAny()]
        return [DoctorSelfViewPermissions()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save the Doctor instance
        doctor_instance = serializer.save()
        
        # Generate Tokens
        user = doctor_instance.user
        tokens = get_tokens_for_user(user)
        
        # Prepare custom response
        response_data = serializer.data
        response_data['tokens'] = tokens
        response_data['role'] = "Doctor"
        
        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminOnlyPermissions] 

# Generic Signup (for simple users, if needed)
class SignupApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            group_name = user.groups.first().name if user.groups.exists() else None
            
            return Response({
                "user_id": user.id,
                "username": user.username,
                "role": group_name,
                **tokens
            }, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            # authenticate checks username/password
            user = authenticate(
                request, 
                username=serializer.validated_data["username"], 
                password=serializer.validated_data["password"]
            )
            
            if user:
                tokens = get_tokens_for_user(user)
                group_name = user.groups.first().name if user.groups.exists() else None
                
                return Response({
                    "status": status.HTTP_200_OK,
                    "message": "Login successful",
                    "username": user.username,
                    "role": group_name, 
                    "tokens": tokens
                }, status=status.HTTP_200_OK)
            
            return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)