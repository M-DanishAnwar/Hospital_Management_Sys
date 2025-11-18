"""
Doctor model class for Hospital Management System
"""

class Doctor:
    def __init__(self, doctor_id=None, name=None, specialization=None, contact=None, email=None):
        self.doctor_id = doctor_id
        self.name = name
        self.specialization = specialization
        self.contact = contact
        self.email = email
    
    def to_dict(self):
        """Convert doctor object to dictionary"""
        return {
            'doctor_id': self.doctor_id,
            'name': self.name,
            'specialization': self.specialization,
            'contact': self.contact,
            'email': self.email
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create doctor object from dictionary"""
        return cls(
            doctor_id=data.get('doctor_id'),
            name=data.get('name'),
            specialization=data.get('specialization'),
            contact=data.get('contact'),
            email=data.get('email')
        )
    
    def validate(self):
        """Validate doctor data"""
        if not self.name or len(self.name.strip()) == 0:
            return False, "Name is required"
        if not self.specialization or len(self.specialization.strip()) == 0:
            return False, "Specialization is required"
        if not self.email or len(self.email.strip()) == 0:
            return False, "Email is required"
        return True, "Valid"