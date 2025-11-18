"""
Patient model class for Hospital Management System
"""

class Patient:
    def __init__(self, patient_id=None, name=None, dob=None, gender=None, contact=None, address=None):
        self.patient_id = patient_id
        self.name = name
        self.dob = dob
        self.gender = gender
        self.contact = contact
        self.address = address
    
    def to_dict(self):
        """Convert patient object to dictionary"""
        return {
            'patient_id': self.patient_id,
            'name': self.name,
            'dob': self.dob,
            'gender': self.gender,
            'contact': self.contact,
            'address': self.address
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create patient object from dictionary"""
        return cls(
            patient_id=data.get('patient_id'),
            name=data.get('name'),
            dob=data.get('dob'),
            gender=data.get('gender'),
            contact=data.get('contact'),
            address=data.get('address')
        )
    
    def validate(self):
        """Validate patient data"""
        if not self.name or len(self.name.strip()) == 0:
            return False, "Name is required"
        if not self.contact or len(self.contact.strip()) == 0:
            return False, "Contact is required"
        return True, "Valid"