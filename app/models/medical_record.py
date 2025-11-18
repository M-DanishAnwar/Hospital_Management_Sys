"""
Medical Record model class for Hospital Management System
"""

class MedicalRecord:
    def __init__(self, record_id=None, patient_id=None, doctor_id=None, 
                 diagnosis=None, prescription=None, visit_date=None):
        self.record_id = record_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.diagnosis = diagnosis
        self.prescription = prescription
        self.visit_date = visit_date
    
    def to_dict(self):
        """Convert medical record object to dictionary"""
        return {
            'record_id': self.record_id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'diagnosis': self.diagnosis,
            'prescription': self.prescription,
            'visit_date': self.visit_date
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create medical record object from dictionary"""
        return cls(
            record_id=data.get('record_id'),
            patient_id=data.get('patient_id'),
            doctor_id=data.get('doctor_id'),
            diagnosis=data.get('diagnosis'),
            prescription=data.get('prescription'),
            visit_date=data.get('visit_date')
        )
    
    def validate(self):
        """Validate medical record data"""
        if not self.diagnosis or len(self.diagnosis.strip()) == 0:
            return False, "Diagnosis is required"
        if not self.visit_date:
            return False, "Visit date is required"
        return True, "Valid"