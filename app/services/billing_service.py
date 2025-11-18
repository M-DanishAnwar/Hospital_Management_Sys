"""
Billing service class for Hospital Management System
Handles business logic for billing operations
"""

from app.utils.db import create_connection
from app.utils.helpers import format_currency

class BillingService:
    def __init__(self):
        self.connection = create_connection()
    
    def create_bill(self, patient_id, amount, description, date_issued=None):
        """Create a new bill"""
        try:
            cursor = self.connection.cursor()
            if not date_issued:
                date_issued = datetime.now().strftime('%Y-%m-%d')
            
            query = """
            INSERT INTO billing (patient_id, amount, description, payment_status, date_issued)
            VALUES (%s, %s, %s, 'Unpaid', %s)
            """
            cursor.execute(query, (patient_id, amount, description, date_issued))
            self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Error creating bill: {str(e)}")
        finally:
            cursor.close()
    
    def get_patient_bills(self, patient_id):
        """Get all bills for a patient"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT b.*, p.name as patient_name 
                FROM billing b
                JOIN patients p ON b.patient_id = p.patient_id
                WHERE b.patient_id = %s
                ORDER BY b.date_issued DESC
            """, (patient_id,))
            return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Error retrieving bills: {str(e)}")
        finally:
            cursor.close()
    
    def mark_as_paid(self, bill_id):
        """Mark a bill as paid"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE billing 
                SET payment_status = 'Paid', payment_date = %s
                WHERE bill_id = %s
            """, (datetime.now().strftime('%Y-%m-%d'), bill_id))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Error updating bill: {str(e)}")
        finally:
            cursor.close()
    
    def get_unpaid_bills(self):
        """Get all unpaid bills"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT b.*, p.name as patient_name 
                FROM billing b
                JOIN patients p ON b.patient_id = p.patient_id
                WHERE b.payment_status = 'Unpaid'
                ORDER BY b.date_issued ASC
            """)
            return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Error retrieving unpaid bills: {str(e)}")
        finally:
            cursor.close()