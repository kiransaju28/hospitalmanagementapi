from django.test import TestCase
from django.contrib.auth.models import User, Group
from rest_framework.test import APIClient
from rest_framework import status
from apibackendapp.models import Doctor, Specialization

class DoctorRegistrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a specialization for testing
        self.spec = Specialization.objects.create(name="Cardiology", description="Heart stuff")
        
        self.doctor_data = {
            "name": "Dr. Test",
            "contact_info": "1234567890",
            "consultation_fee": 500,
            "specialization": self.spec.id,
            "user": {
                "username": "drtest",
                "password": "strongpassword123",
                "email": "drtest@example.com"
            }
        }

    def test_create_doctor_creates_user_and_group(self):
        """
        Ensure posting to /doctors/ creates a User, a Doctor profile, 
        and assigns the 'Doctor' group.
        """
        response = self.client.post('/api/admins/doctors/', self.doctor_data, format='json')
        
        # 1. Check API Response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        
        # 2. Check Database Integrity
        self.assertTrue(User.objects.filter(username="drtest").exists())
        user = User.objects.get(username="drtest")
        
        self.assertTrue(Doctor.objects.filter(user=user).exists())
        self.assertTrue(user.groups.filter(name='Doctor').exists())

    def test_doctor_permissions(self):
        """
        Ensure a Doctor cannot view another Doctor's profile details
        unless they are Admin.
        """
        # Create Doctor 1 (The one logging in)
        self.client.post('/api/admins/doctors/', self.doctor_data, format='json')
        token = self.client.post('/api/admins/login/', {
            "username": "drtest", 
            "password": "strongpassword123"
        }).data['tokens']['access']
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        # Create Doctor 2 (The one we try to access)
        user2 = User.objects.create_user(username="dr2", password="pwd")
        group, _ = Group.objects.get_or_create(name='Doctor')
        user2.groups.add(group)
        doc2 = Doctor.objects.create(user=user2, name="Dr Two", specialization=self.spec, consultation_fee=500)

        # Try to access Doctor 2's profile as Doctor 1
        response = self.client.get(f'/api/admins/doctors/{doc2.doctor_id}/')
        
        # Should be Forbidden (403) because of DoctorSelfViewPermissions
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)