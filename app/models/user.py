"""
User model for authentication and authorization
"""

class User:
    def __init__(self, user_id=None, username=None, password=None, role=None):
        self.user_id = user_id
        self.username = username
        self.password = password  # In real app, this should be hashed
        self.role = role  # 'admin', 'doctor', 'receptionist'
    
    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'role': self.role
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create user object from dictionary"""
        return cls(
            user_id=data.get('user_id'),
            username=data.get('username'),
            password=data.get('password'),
            role=data.get('role')
        )
    
    def is_admin(self):
        """Check if user is admin"""
        return self.role == 'admin'
    
    def is_doctor(self):
        """Check if user is doctor"""
        return self.role == 'doctor'
    
    def is_receptionist(self):
        """Check if user is receptionist"""
        return self.role == 'receptionist'