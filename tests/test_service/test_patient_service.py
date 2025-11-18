"""
Unit tests for patient service
"""

import unittest
from unittest.mock import patch, MagicMock
from app.services.patient_service import PatientService
from app.models.patient import Patient

class TestPatientService(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment before each test"""
        self.patient_service = PatientService()
        
        # Mock database connection
        self.mock_connection = MagicMock()
        self.mock_cursor = MagicMock()
        self.patient_service.connection = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
    
    def tearDown(self):
        """Clean up after each test"""
        self.patient_service.close_connection()
    
    def test_add_patient_success(self):
        """Test successful patient addition"""
        patient = Patient(
            name="John Doe",
            dob="1990-01-15",
            gender="M",
            contact="123-456-7890",
            address="123 Main St"
        )
        
        # Set up mock cursor
        self.mock_cursor.lastrowid = 1
        
        result = self.patient_service.add_patient(patient)
        
        # Verify the patient was added correctly
        self.assertEqual(result.patient_id, 1)
        self.assertEqual(result.name, "John Doe")
        self.mock_cursor.execute.assert_called_once()
        self.mock_connection.commit.assert_called_once()
    
    def test_add_patient_validation_failure(self):
        """Test patient addition with validation failure"""
        # Test with empty name
        patient = Patient(
            name="",
            dob="1990-01-15",
            gender="M",
            contact="123-456-7890",
            address="123 Main St"
        )
        
        with self.assertRaises(ValueError) as context:
            self.patient_service.add_patient(patient)
        self.assertIn("Name is required", str(context.exception))
        
        # Test with empty contact
        patient = Patient(
            name="John Doe",
            dob="1990-01-15",
            gender="M",
            contact="",
            address="123 Main St"
        )
        
        with self.assertRaises(ValueError) as context:
            self.patient_service.add_patient(patient)
        self.assertIn("Contact is required", str(context.exception))
    
    def test_get_all_patients(self):
        """Test getting all patients"""
        # Mock database response
        mock_data = [
            {
                'patient_id': 1,
                'name': 'John Doe',
                'dob': '1990-01-15',
                'gender': 'M',
                'contact': '123-456-7890',
                'address': '123 Main St'
            },
            {
                'patient_id': 2,
                'name': 'Jane Smith',
                'dob': '1985-03-22',
                'gender': 'F',
                'contact': '987-654-3210',
                'address': '456 Elm St'
            }
        ]
        
        self.mock_cursor.fetchall.return_value = mock_data
        
        patients = self.patient_service.get_all_patients()
        
        # Verify results
        self.assertEqual(len(patients), 2)
        self.assertEqual(patients[0].name, "John Doe")
        self.assertEqual(patients[1].name, "Jane Smith")
        self.mock_cursor.execute.assert_called_once_with("SELECT * FROM patients")
    
    def test_get_patient_by_id(self):
        """Test getting patient by ID"""
        # Mock database response
        mock_data = {
            'patient_id': 1,
            'name': 'John Doe',
            'dob': '1990-01-15',
            'gender': 'M',
            'contact': '123-456-7890',
            'address': '123 Main St'
        }
        
        self.mock_cursor.fetchone.return_value = mock_data
        
        patient = self.patient_service.get_patient_by_id(1)
        
        # Verify results
        self.assertIsNotNone(patient)
        self.assertEqual(patient.patient_id, 1)
        self.assertEqual(patient.name, "John Doe")
        self.mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM patients WHERE patient_id = %s", 
            (1,)
        )
    
    def test_update_patient_success(self):
        """Test successful patient update"""
        patient = Patient(
            patient_id=1,
            name="John Doe Updated",
            dob="1990-01-15",
            gender="M",
            contact="123-456-7890",
            address="123 Main St Updated"
        )
        
        self.mock_cursor.rowcount = 1
        
        result = self.patient_service.update_patient(patient)
        
        # Verify update was successful
        self.assertTrue(result)
        self.mock_cursor.execute.assert_called_once()
        self.mock_connection.commit.assert_called_once()
    
    def test_update_patient_validation_failure(self):
        """Test patient update with validation failure"""
        # Test with empty name
        patient = Patient(
            patient_id=1,
            name="",
            dob="1990-01-15",
            gender="M",
            contact="123-456-7890",
            address="123 Main St"
        )
        
        with self.assertRaises(ValueError) as context:
            self.patient_service.update_patient(patient)
        self.assertIn("Name is required", str(context.exception))
    
    def test_delete_patient_success(self):
        """Test successful patient deletion"""
        self.mock_cursor.rowcount = 1
        
        result = self.patient_service.delete_patient(1)
        
        # Verify deletion was successful
        self.assertTrue(result)
        self.mock_cursor.execute.assert_called_once_with(
            "DELETE FROM patients WHERE patient_id = %s", 
            (1,)
        )
        self.mock_connection.commit.assert_called_once()
    
    def test_database_error_handling(self):
        """Test error handling for database operations"""
        # Test add_patient with database error
        patient = Patient(
            name="John Doe",
            dob="1990-01-15",
            gender="M",
            contact="123-456-7890",
            address="123 Main St"
        )
        
        self.mock_cursor.execute.side_effect = Exception