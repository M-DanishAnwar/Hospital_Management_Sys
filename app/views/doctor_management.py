"""
Doctor Management View
"""

import tkinter as tk
from tkinter import ttk, messagebox
from app.utils.style import (
    PRIMARY_COLOR, BACKGROUND_COLOR, TEXT_COLOR,
    TITLE_FONT, NORMAL_FONT, BUTTON_FONT,
    create_button, create_entry, create_label, create_card
)
from app.utils.helpers import validate_required_fields, validate_email

class DoctorManagementView:
    def __init__(self, root):
        self.root = root
        self.root.title("Doctor Management")
        self.root.geometry("800x600")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header = tk.Label(
            main_frame, 
            text="👨‍⚕️ Doctor Management", 
            font=TITLE_FONT, 
            fg=PRIMARY_COLOR, 
            bg=BACKGROUND_COLOR
        )
        header.pack(pady=(0, 20))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Add Doctor tab
        add_doctor_frame = tk.Frame(notebook, bg=BACKGROUND_COLOR)
        notebook.add(add_doctor_frame, text="Add Doctor")
        
        # View Doctors tab
        view_doctors_frame = tk.Frame(notebook, bg=BACKGROUND_COLOR)
        notebook.add(view_doctors_frame, text="View Doctors")
        
        # Add Doctor Form
        self.create_add_doctor_form(add_doctor_frame)
        
        # View Doctors Table
        self.create_view_doctors_table(view_doctors_frame)
    
    def create_add_doctor_form(self, parent):
        # Form card
        form_card = create_card(parent, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Form fields
        form_frame = tk.Frame(form_card, bg="white", padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Name
        create_label(form_frame, "Doctor Name:", font=BUTTON_FONT)
        self.name_entry = create_entry(form_frame)
        self.name_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Specialization
        create_label(form_frame, "Specialization:", font=BUTTON_FONT)
        self.specialization_entry = create_entry(form_frame)
        self.specialization_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Contact
        create_label(form_frame, "Contact Number:", font=BUTTON_FONT)
        self.contact_entry = create_entry(form_frame)
        self.contact_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Email
        create_label(form_frame, "Email:", font=BUTTON_FONT)
        self.email_entry = create_entry(form_frame)
        self.email_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg="white")
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        create_button(
            button_frame,
            "Add Doctor",
            command=self.add_doctor,
            bg=PRIMARY_COLOR
        ).pack(side=tk.LEFT, padx=5)
        
        create_button(
            button_frame,
            "Clear Form",
            command=self.clear_form,
            bg="#6C757D"
        ).pack(side=tk.LEFT, padx=5)
    
    def create_view_doctors_table(self, parent):
        # Table card
        table_card = create_card(parent, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview
        columns = ('id', 'name', 'specialization', 'contact', 'email')
        self.tree = ttk.Treeview(table_card, columns=columns, show='headings')
        
        # Configure columns
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='Name')
        self.tree.heading('specialization', text='Specialization')
        self.tree.heading('contact', text='Contact')
        self.tree.heading('email', text='Email')
        
        self.tree.column('id', width=50)
        self.tree.column('name', width=150)
        self.tree.column('specialization', width=150)
        self.tree.column('contact', width=100)
        self.tree.column('email', width=200)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_card, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add mock data
        self.load_mock_doctors()
        
        # Buttons frame
        button_frame = tk.Frame(table_card, bg=BACKGROUND_COLOR)
        button_frame.pack(fill=tk.X, pady=10)
        
        create_button(
            button_frame,
            "Refresh",
            command=self.load_mock_doctors,
            bg="#17A2B8"
        ).pack(side=tk.LEFT, padx=5)
        
        create_button(
            button_frame,
            "Edit Selected",
            command=self.edit_doctor,
            bg="#FFC107"
        ).pack(side=tk.LEFT, padx=5)
        
        create_button(
            button_frame,
            "Delete Selected",
            command=self.delete_doctor,
            bg="#DC3545"
        ).pack(side=tk.LEFT, padx=5)
    
    def add_doctor(self):
        name = self.name_entry.get().strip()
        specialization = self.specialization_entry.get().strip()
        contact = self.contact_entry.get().strip()
        email = self.email_entry.get().strip()
        
        if not validate_required_fields({
            "Doctor Name": name,
            "Specialization": specialization,
            "Contact Number": contact,
            "Email": email
        }):
            return
        
        if not validate_email(email):
            messagebox.showerror("Error", "Invalid email format")
            return
        
        # Mock add doctor - in real app this would save to database
        messagebox.showinfo("Success", f"Doctor {name} added successfully!")
        
        # Clear form
        self.clear_form()
        
        # Refresh the table
        self.load_mock_doctors()
    
    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.specialization_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
    
    def load_mock_doctors(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add mock data
        mock_doctors = [
            (1, "Dr. John Smith", "Cardiology", "123-456-7890", "john.smith@hospital.com"),
            (2, "Dr. Sarah Johnson", "Neurology", "234-567-8901", "sarah.j@hospital.com"),
            (3, "Dr. Michael Chen", "Pediatrics", "345-678-9012", "mchen@hospital.com")
        ]
        
        for doctor in mock_doctors:
            self.tree.insert('', tk.END, values=doctor)
    
    def edit_doctor(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a doctor to edit")
            return
        
        # In real app, this would open an edit form
        item = self.tree.item(selected_item[0])
        doctor_data = item['values']
        messagebox.showinfo("Edit Doctor", f"Editing doctor: {doctor_data[1]}")
    
    def delete_doctor(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a doctor to delete")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this doctor?"):
            self.tree.delete(selected_item[0])
            messagebox.showinfo("Success", "Doctor deleted successfully!")