"""
Mock database utility – NO real MySQL needed for demo
Fully compatible with all views and services using in-memory data
"""

class MockConnection:
    def __init__(self):
        # In-memory "database"
        self.data = {
            'patients': [
                {'patient_id': 1, 'name': 'John Doe', 'dob': '1990-01-15', 'gender': 'M', 'contact': '123-456-7890', 'address': '123 Main St'},
                {'patient_id': 2, 'name': 'Jane Smith', 'dob': '1985-03-22', 'gender': 'F', 'contact': '987-654-3210', 'address': '456 Oak Ave'}
            ],
            'doctors': [
                {'doctor_id': 1, 'name': 'Dr. Alice Johnson', 'specialization': 'Cardiology', 'contact': '555-0101', 'email': 'alice@hospital.com'},
                {'doctor_id': 2, 'name': 'Dr. Bob Wilson', 'specialization': 'Neurology', 'contact': '555-0102', 'email': 'bob@hospital.com'}
            ],
            'appointments': [
                {'appointment_id': 1, 'patient_id': 1, 'doctor_id': 1, 'appointment_date': '2025-01-20 09:00:00', 'status': 'Scheduled'}
            ],
            'billing': [
                {'bill_id': 1, 'patient_id': 1, 'amount': 150.00, 'description': 'Consultation fee', 'payment_status': 'Unpaid', 'date_issued': '2025-01-15'}
            ]
        }

    def cursor(self, dictionary=False):
        return MockCursor(self.data)

    def commit(self):
        pass

    def close(self):
        pass

class MockCursor:
    def __init__(self, data):
        self.data = data
        self.lastrowid = 1

    def execute(self, query, params=None):
        # Parse simple queries for demo
        self.executed_query = query.lower()
        if "insert into patients" in self.executed_query:
            self.lastrowid += 1
        elif "insert into doctors" in self.executed_query:
            self.lastrowid += 1

    def fetchall(self):
        if "select * from patients" in self.executed_query:
            return self.data['patients']
        elif "select * from doctors" in self.executed_query:
            return self.data['doctors']
        elif "billing b join patients p" in self.executed_query.lower():
            # Return joined billing data
            return [
                {
                    'bill_id': 1,
                    'patient_id': 1,
                    'amount': 150.00,
                    'description': 'Consultation fee',
                    'payment_status': 'Unpaid',
                    'date_issued': '2025-01-15',
                    'patient_name': 'John Doe'
                }
            ]
        return []

    def fetchone(self):
        if "select * from patients where patient_id" in self.executed_query:
            return self.data['patients'][0] if self.data['patients'] else None
        return None

    def close(self):
        pass

def create_connection():
    """Returns a fully functional mock database connection for demo"""
    print("✅ Using MOCK database (no MySQL required for demo)")
    return MockConnection()