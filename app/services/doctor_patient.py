"""
Doctor service class for Hospital Management System
Handles business logic for doctor operations
"""

from app.models.doctor import Doctor
from app.utils.db import create_connection

class DoctorService:
    def __init__(self):
        self.connection = create_connection()
    
    def add_doctor(self, doctor):
        """Add a new doctor to the database"""
        if not isinstance(doctor, Doctor):
            raise ValueError("Invalid doctor object")
        
        valid, message = doctor.validate()
        if not valid:
            raise ValueError(message)
        
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO doctors (name, specialization, contact, email)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (
                doctor.name,
                doctor.specialization,
                doctor.contact,
                doctor.email
            ))
            self.connection.commit()
            doctor.doctor_id = cursor.lastrowid
            return doctor
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Error adding doctor: {str(e)}")
        finally:
            cursor.close()
    
    def get_all_doctors(self):
        """Get all doctors from database"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM doctors")
            rows = cursor.fetchall()
            return [Doctor.from_dict(row) for row in rows]
        except Exception as e:
            raise Exception(f"Error retrieving doctors: {str(e)}")
        finally:
            cursor.close()
    
    def get_doctor_by_id(self, doctor_id):
        """Get doctor by ID"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM doctors WHERE doctor_id = %s", (doctor_id,))
            row = cursor.fetchone()
            return Doctor.from_dict(row) if row else None
        except Exception as e:
            raise Exception(f"Error retrieving doctor: {str(e)}")
        finally:
            cursor.close()
    
    def update_doctor(self, doctor):
        """Update doctor information"""
        if not isinstance(doctor, Doctor):
            raise ValueError("Invalid doctor object")
        
        valid, message = doctor.validate()
        if not valid:
            raise ValueError(message)
        
        try:
            cursor = self.connection.cursor()
            query = """
            UPDATE doctors 
            SET name = %s, specialization = %s, contact = %s, email = %s
            WHERE doctor_id = %s
            """
            cursor.execute(query, (
                doctor.name,
                doctor.specialization,
                doctor.contact,
                doctor.email,
                doctor.doctor_id
            ))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Error updating doctor: {str(e)}")
        finally:
            cursor.close()
    
    def delete_doctor(self, doctor_id):
        """Delete doctor by ID"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM doctors WHERE doctor_id = %s", (doctor_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Error deleting doctor: {str(e)}")
        finally:
            cursor.close()