"""
Unit tests for login view
"""

import unittest
import tkinter as tk
from unittest.mock import patch, MagicMock
from app.views.login import LoginView
from app.services.auth import auth_service

class TestLoginView(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment before each test"""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main window during tests
        
        # Mock auth service methods
        self.original_login = auth_service.login
        self.original_logout = auth_service.logout
        
        # Create login view
        self.login_view = LoginView(self.root)
    
    def tearDown(self):
        """Clean up after each test"""
        # Restore original auth service methods
        auth_service.login = self.original_login
        auth_service.logout = self.original_logout
        
        # Destroy the root window
        self.root.destroy()
    
    def test_login_view_initialization(self):
        """Test that login view initializes correctly"""
        self.assertIsNotNone(self.login_view.root)
        self.assertIsNotNone(self.login_view.username_entry)
        self.assertIsNotNone(self.login_view.password_entry)
        self.assertIsNotNone(self.login_view.login_button)
    
    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    def test_successful_login(self, mock_showerror, mock_showinfo):
        """Test successful login scenario"""
        # Mock auth service to return a user
        mock_user = MagicMock()
        mock_user.role = "admin"
        mock_user.username = "admin"
        
        auth_service.login = MagicMock(return_value=mock_user)
        
        # Set username and password
        self.login_view.username_entry.insert(0, "admin")
        self.login_view.password_entry.insert(0, "admin123")
        
        # Call login handler
        self.login_view.handle_login()
        
        # Verify
        auth_service.login.assert_called_once_with("admin", "admin123")
        mock_showinfo.assert_called_once_with("Success", "Welcome, admin!")
        mock_showerror.assert_not_called()
        
        # Check that current user is set
        self.assertEqual(auth_service.get_current_user().username, "admin")
    
    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    def test_failed_login(self, mock_showerror, mock_showinfo):
        """Test failed login scenario"""
        # Mock auth service to return None
        auth_service.login = MagicMock(return_value=None)
        
        # Set username and password
        self.login_view.username_entry.insert(0, "wronguser")