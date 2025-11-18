from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from apibackendapp.models import Staff, Specialization, Doctor

# Basic User Serializer for nested display
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Helper serializer to accept registration data inside Doctor/Staff payloads
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

class StaffSerializer(serializers.ModelSerializer):
    # Nest the registration serializer for creating; use UserSerializer for reading if needed
    user = UserRegistrationSerializer(write_only=True)
    user_details = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Staff
        fields = ['staff_id', 'fullname', 'gender', 'joining_date', 'mail_id', 'mobileno', 'user', 'user_details']

    def create(self, validated_data):
        # 1. Extract user data
        user_data = validated_data.pop('user')
        
        # 2. Create the User
        user = User.objects.create_user(**user_data)
        
        # 3. Assign to 'Staff' Group
        group, _ = Group.objects.get_or_create(name='Staff')
        user.groups.add(group)
        
        # 4. Create the Staff profile linked to the new user
        staff_instance = Staff.objects.create(user=user, **validated_data)
        
        return staff_instance

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer(write_only=True)
    user_details = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = Doctor
        fields = ['doctor_id', 'name', 'contact_info', 'consultation_fee', 'specialization', 'user', 'user_details']

    def create(self, validated_data):
        # 1. Extract user data
        user_data = validated_data.pop('user')
        
        # 2. Create the User
        user = User.objects.create_user(**user_data)
        
        # 3. Assign to 'Doctor' Group
        group, _ = Group.objects.get_or_create(name='Doctor')
        user.groups.add(group)
        
        # 4. Create the Doctor profile linked to the new user
        doctor_instance = Doctor.objects.create(user=user, **validated_data)
        
        return doctor_instance

# --- AUTH SERIALIZERS ---

class SignupSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'group_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        group_name = validated_data.pop("group_name", None)
        
        # Create user using the helper method which hashes password
        user = User.objects.create_user(**validated_data)

        if group_name:
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
        
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)