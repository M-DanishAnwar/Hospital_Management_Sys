"""
Authentication service for user login and session management
"""

from app.models.user import User
from app.utils.db import create_connection

class AuthService:
    def __init__(self):
        self.current_user = None
    
    def login(self, username, password):
        """
        Authenticate user with username and password
        Returns User object if successful, None otherwise
        """
        # For demo purposes, use hardcoded credentials
        # In real app, this would query the database
        mock_users = {
            'admin': {'password': 'admin123', 'role': 'admin'},
            'doctor': {'password': 'doctor123', 'role': 'doctor'},
            'receptionist': {'password': 'reception123', 'role': 'receptionist'}
        }
        
        if username in mock_users and mock_users[username]['password'] == password:
            self.current_user = User(
                username=username,
                role=mock_users[username]['role']
            )
            return self.current_user
        
        return None
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
    
    def get_current_user(self):
        """Get current logged in user"""
        return self.current_user
    
    def is_authenticated(self):
        """Check if user is authenticated"""
        return self.current_user is not None
    
    def has_role(self, role):
        """Check if current user has specific role"""
        if not self.is_authenticated():
            return False
        return self.current_user.role == role
    
    def has_any_role(self, roles):
        """Check if current user has any of the specified roles"""
        if not self.is_authenticated():
            return False
        return self.current_user.role in roles

# Global auth service instance
auth_service = AuthService()