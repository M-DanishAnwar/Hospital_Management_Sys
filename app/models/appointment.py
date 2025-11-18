"""
Appointment model class for Hospital Management System
"""

class Appointment:
    def __init__(self, appointment_id=None, patient_id=None, doctor_id=None, 
                 appointment_date=None, status="Scheduled"):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.appointment_date = appointment_date
        self.status = status
    
    def to_dict(self):
        """Convert appointment object to dictionary"""
        return {
            'appointment_id': self.appointment_id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'appointment_date': self.appointment_date,
            'status': self.status
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create appointment object from dictionary"""
        return cls(
            appointment_id=data.get('appointment_id'),
            patient_id=data.get('patient_id'),
            doctor_id=data.get('doctor_id'),
            appointment_date=data.get('appointment_date'),
            status=data.get('status', 'Scheduled')
        )
    
    def validate(self):
        """Validate appointment data"""
        if not self.appointment_date:
            return False, "Appointment date is required"
        if self.status not in ['Scheduled', 'Completed', 'Cancelled']:
            return False, "Invalid status"
        return True, "Valid"