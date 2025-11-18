"""
Unit tests for authentication service
"""

import unittest
from unittest.mock import patch, MagicMock
from app.services.auth import AuthService, User

class TestAuthService(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment before each test"""
        self.auth_service = AuthService()
    
    def test_login_success(self):
        """Test successful login with valid credentials"""
        # Test admin login
        admin_user = self.auth_service.login("admin", "admin123")
        self.assertIsNotNone(admin_user)
        self.assertEqual(admin_user.username, "admin")
        self.assertEqual(admin_user.role, "admin")
        
        # Test doctor login
        doctor_user = self.auth_service.login("doctor", "doctor123")
        self.assertIsNotNone(doctor_user)
        self.assertEqual(doctor_user.username, "doctor")
        self.assertEqual(doctor_user.role, "doctor")
        
        # Test receptionist login
        receptionist_user = self.auth_service.login("receptionist", "reception123")
        self.assertIsNotNone(receptionist_user)
        self.assertEqual(receptionist_user.username, "receptionist")
        self.assertEqual(receptionist_user.role, "receptionist")
    
    def test_login_failure(self):
        """Test failed login with invalid credentials"""
        # Wrong password
        user = self.auth_service.login("admin", "wrongpassword")
        self.assertIsNone(user)
        
        # Wrong username
        user = self.auth_service.login("wronguser", "admin123")
        self.assertIsNone(user)
        
        # Empty credentials
        user = self.auth_service.login("", "")
        self.assertIsNone(user)
    
    def test_logout(self):
        """Test logout functionality"""
        # Login first
        self.auth_service.login("admin", "admin123")
        self.assertIsNotNone(self.auth_service.get_current_user())
        
        # Logout
        self.auth_service.logout()
        self.assertIsNone(self.auth_service.get_current_user())
    
    def test_authentication_status(self):
        """Test authentication status checks"""
        # Not authenticated initially
        self.assertFalse(self.auth_service.is_authenticated())
        
        # Login
        self.auth_service.login("admin", "admin123")
        self.assertTrue(self.auth_service.is_authenticated())
        
        # Logout
        self.auth_service.logout()
        self.assertFalse(self.auth_service.is_authenticated())
    
    def test_role_checking(self):
        """Test role checking functionality"""
        # Login as admin
        self.auth_service.login("admin", "admin123")
        self.assertTrue(self.auth_service.has_role("admin"))
        self.assertFalse(self.auth_service.has_role("doctor"))
        self.assertFalse(self.auth_service.has_role("receptionist"))
        
        # Login as doctor
        self.auth_service.login("doctor", "doctor123")
        self.assertFalse(self.auth_service.has_role("admin"))
        self.assertTrue(self.auth_service.has_role("doctor"))
        self.assertFalse(self.auth_service.has_role("receptionist"))
        
        # Login as receptionist
        self.auth_service.login("receptionist", "reception123")
        self.assertFalse(self.auth_service.has_role("admin"))
        self.assertFalse(self.auth_service.has_role("doctor"))
        self.assertTrue(self.auth_service.has_role("receptionist"))
    
    def test_has_any_role(self):
        """Test has_any_role functionality"""
        # Login as admin
        self.auth_service.login("admin", "admin123")
        self.assertTrue(self.auth_service.has_any_role(["admin", "doctor"]))
        self.assertFalse(self.auth_service.has_any_role(["doctor", "receptionist"]))
        
        # Login as doctor
        self.auth_service.login("doctor", "doctor123")
        self.assertTrue(self.auth_service.has_any_role(["admin", "doctor", "receptionist"]))
        self.assertFalse(self.auth_service.has_any_role(["admin", "receptionist"]))
    
    def test_user_model(self):
        """Test User model functionality"""
        user = User(user_id=1, username="testuser", role="admin")
        
        # Test to_dict method
        user_dict = user.to_dict()
        self.assertEqual(user_dict['username'], "testuser")
        self.assertEqual(user_dict['role'], "admin")
        
        # Test from_dict method
        new_user = User.from_dict(user_dict)
        self.assertEqual(new_user.username, "testuser")
        self.assertEqual(new_user.role, "admin")
        
        # Test role check methods
        self.assertTrue(user.is_admin())
        self.assertFalse(user.is_doctor())
        self.assertFalse(user.is_receptionist())

if __name__ == '__main__':
    unittest.main()