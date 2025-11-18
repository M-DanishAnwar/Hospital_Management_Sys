"""
Login View - Authentication interface for Hospital Management System
"""

import tkinter as tk
from tkinter import messagebox
from app.utils.style import (
    PRIMARY_COLOR, BACKGROUND_COLOR, TEXT_COLOR,
    TITLE_FONT, NORMAL_FONT, BUTTON_FONT,
    create_button, create_entry, create_label
)
from app.services.auth import auth_service

class LoginView:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System - Login")
        self.root.geometry("400x500")
        self.root.configure(bg=BACKGROUND_COLOR)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_label = tk.Label(
            main_frame, 
            text="🏥 Hospital Management System", 
            font=TITLE_FONT, 
            fg=PRIMARY_COLOR, 
            bg=BACKGROUND_COLOR
        )
        header_label.pack(pady=(0, 30))
        
        # Login card
        login_frame = tk.Frame(main_frame, bg="white", padx=30, pady=30, relief=tk.RAISED, borderwidth=1)
        login_frame.pack(fill=tk.BOTH, expand=True)
        
        # Username
        create_label(login_frame, "Username:", font=BUTTON_FONT)
        self.username_entry = create_entry(login_frame)
        self.username_entry.pack(fill=tk.X, pady=(0, 15))
        self.username_entry.focus()
        
        # Password
        create_label(login_frame, "Password:", font=BUTTON_FONT)
        self.password_entry = create_entry(login_frame)
        self.password_entry.pack(fill=tk.X, pady=(0, 20))
        self.password_entry.config(show="*")
        
        # Login button
        self.login_button = create_button(
            login_frame, 
            "Login", 
            command=self.handle_login,
            bg=PRIMARY_COLOR,
            fg="white",
            font=BUTTON_FONT
        )
        self.login_button.pack(fill=tk.X, pady=(0, 15))
        
        # Demo credentials hint
        hint_label = tk.Label(
            login_frame,
            text="Demo credentials:\nAdmin: admin/admin123\nDoctor: doctor/doctor123\nReceptionist: receptionist/reception123",
            font=("Segoe UI", 9),
            fg="gray",
            bg="white",
            justify=tk.LEFT
        )
        hint_label.pack(pady=(10, 0))
        
        # Bind Enter key
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        self.password_entry.bind('<Return>', lambda e: self.handle_login())
    
    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        user = auth_service.login(username, password)
        
        if user:
            messagebox.showinfo("Success", f"Welcome, {username}!")
            self.root.withdraw()  # Hide login window
            
            # Open appropriate dashboard based on role
            self.open_dashboard(user)
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def open_dashboard(self, user):
        dashboard_window = tk.Toplevel(self.root)
        dashboard_window.title(f"Dashboard - {user.username}")
        dashboard_window.geometry("800x600")
        
        if user.is_admin():
            from app.views.admin_dashboard import AdminDashboard
            AdminDashboard(dashboard_window)
        elif user.is_doctor():
            from app.views.doctor_management import DoctorManagementView
            DoctorManagementView(dashboard_window)
        else:  # receptionist
            from app.views.patient_registration import PatientRegistrationView
            PatientRegistrationView(dashboard_window)
        
        # Close login window when dashboard is closed
        dashboard_window.protocol("WM_DELETE_WINDOW", lambda: self.on_dashboard_close(dashboard_window))
    
    def on_dashboard_close(self, dashboard_window):
        dashboard_window.destroy()
        self.root.deiconify()  # Show login window again