"""
Patient service class for Hospital Management System
Handles business logic for patient operations
"""

from app.models.patient import Patient
from app.utils.db import create_connection

class PatientService:
    def __init__(self):
        self.connection = create_connection()
    
    def add_patient(self, patient):
        """Add a new patient to the database"""
        if not isinstance(patient, Patient):
            raise ValueError("Invalid patient object")
        
        valid, message = patient.validate()
        if not valid:
            raise ValueError(message)
        
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO patients (name, dob, gender, contact, address)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                patient.name,
                patient.dob,
                patient.gender,
                patient.contact,
                patient.address
            ))
            self.connection.commit()
            patient.patient_id = cursor.lastrowid
            return patient
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Error adding patient: {str(e)}")
        finally:
            cursor.close()
    
    def get_all_patients(self):
        """Get all patients from database"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM patients")
            rows = cursor.fetchall()
            return [Patient.from_dict(row) for row in rows]
        except Exception as e:
            raise Exception(f"Error retrieving patients: {str(e)}")
        finally:
            cursor.close()
    
    def get_patient_by_id(self, patient_id):
        """Get patient by ID"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
            row = cursor.fetchone()
            return Patient.from_dict(row) if row else None
        except Exception as e:
            raise Exception(f"Error retrieving patient: {str(e)}")
        finally:
            cursor.close()
    
    def update_patient(self, patient):
        """Update patient information"""
        if not isinstance(patient, Patient):
            raise ValueError("Invalid patient object")
        
        valid, message = patient.validate()
        if not valid:
            raise ValueError(message)
        
        try:
            cursor = self.connection.cursor()
            query = """
            UPDATE patients 
            SET name = %s, dob = %s, gender = %s, contact = %s, address = %s
            WHERE patient_id = %s
            """
            cursor.execute(query, (
                patient.name,
                patient.dob,
                patient.gender,
                patient.contact,
                patient.address,
                patient.patient_id
            ))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Error updating patient: {str(e)}")
        finally:
            cursor.close()
    
    def delete_patient(self, patient_id):
        """Delete patient by ID"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM patients WHERE patient_id = %s", (patient_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Error deleting patient: {str(e)}")
        finally:
            cursor.close()
    
    def close_connection(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()