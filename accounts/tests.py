from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.

class MyTest(TestCase):
    def test_home_page_loads(self):
        response = self.client.get("/")
        
        self.assertEqual(
            response.status_code,
            200
        )
        
    def test_register_page_loads(self):
        response = self.client.get("/accounts/register/")
        
        self.assertEqual(response.status_code, 200)
        
class AccountViewTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user",
            email="test@example.com",
            password="12345678"
        )
        
    def test_user_created(self):
        self.assertEqual(
            self.user.username,
            "test_user"
        )
        
    def test_user_can_login(self):
        
        login_success = self.client.login(
            username="test_user",
            password="12345678"
        )
        
        self.assertTrue(login_success)
        
    def test_dashboard_logged_user(self):
        
        self.client.login(
            username="test_user",
            password="12345678"
        )
        
        response = self.client.get("/accounts/dashboard/") 
        
        self.assertEqual(response.status_code , 200)