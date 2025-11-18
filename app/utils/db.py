import mysql.connector
from mysql.connector import Error

def create_connection():
    """Mock database connection - will be replaced with real MySQL connection later"""
    try:
        # This is a mock connection - replace with actual MySQL credentials later
        conn = mysql.connector.connect(
            host='localhost',
            database='hospital_db',
            user='root',
            password='your_password'
        )
        if conn.is_connected():
            print("Connected to MySQL database")
            return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        # Return a mock connection object for now
        return MockConnection()

class MockConnection:
    """Mock connection class to allow UI development without actual database"""
    def cursor(self, dictionary=False):
        return MockCursor()
    
    def commit(self):
        pass
    
    def close(self):
        pass

class MockCursor:
    """Mock cursor class for development"""
    def execute(self, query, params=None):
        pass
    
    def fetchall(self):
        # Return mock data for development
        return [
            {'patient_id': 1, 'name': 'John Doe', 'dob': '1990-01-15', 'gender': 'M'},
            {'patient_id': 2, 'name': 'Jane Smith', 'dob': '1985-03-22', 'gender': 'F'}
        ]
    
    def fetchone(self):
        return {'patient_id': 1, 'name': 'John Doe'}
    
    def close(self):
        pass