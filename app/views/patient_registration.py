"""
Patient Registration View
"""

import tkinter as tk
from tkinter import ttk, messagebox
from app.utils.style import (
    PRIMARY_COLOR, BACKGROUND_COLOR, TEXT_COLOR,
    TITLE_FONT, NORMAL_FONT, BUTTON_FONT,
    create_button, create_entry, create_label, create_card
)
from app.utils.helpers import validate_required_fields, format_date

class PatientRegistrationView:
    def __init__(self, root):
        self.root = root
        self.root.title("Patient Registration")
        self.root.geometry("800x600")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header = tk.Label(
            main_frame, 
            text="🏥 Patient Registration", 
            font=TITLE_FONT, 
            fg=PRIMARY_COLOR, 
            bg=BACKGROUND_COLOR
        )
        header.pack(pady=(0, 20))
        
        # Registration form card
        form_card = create_card(main_frame, fill=tk.X)
        
        # Form fields
        form_frame = tk.Frame(form_card, bg="white", padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Name
        create_label(form_frame, "Patient Name:", font=BUTTON_FONT)
        self.name_entry = create_entry(form_frame)
        self.name_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Date of Birth
        dob_frame = tk.Frame(form_frame, bg="white")
        dob_frame.pack(fill=tk.X, pady=(0, 10))
        
        create_label(dob_frame, "Date of Birth (YYYY-MM-DD):", font=BUTTON_FONT)
        self.dob_entry = create_entry(dob_frame)
        
        # Gender
        gender_frame = tk.Frame(form_frame, bg="white")
        gender_frame.pack(fill=tk.X, pady=(0, 10))
        
        create_label(gender_frame, "Gender:", font=BUTTON_FONT)
        self.gender_var = tk.StringVar(value="M")
        gender_frame_inner = tk.Frame(gender_frame, bg="white")
        gender_frame_inner.pack(fill=tk.X)
        
        tk.Radiobutton(gender_frame_inner, text="Male", variable=self.gender_var, value="M", bg="white").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(gender_frame_inner, text="Female", variable=self.gender_var, value="F", bg="white").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(gender_frame_inner, text="Other", variable=self.gender_var, value="Other", bg="white").pack(side=tk.LEFT, padx=5)
        
        # Contact
        create_label(form_frame, "Contact Number:", font=BUTTON_FONT)
        self.contact_entry = create_entry(form_frame)
        self.contact_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Address
        create_label(form_frame, "Address:", font=BUTTON_FONT)
        self.address_text = tk.Text(form_frame, height=3, font=NORMAL_FONT)
        self.address_text.pack(fill=tk.X, pady=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg="white")
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        create_button(
            button_frame,
            "Register Patient",
            command=self.register_patient,
            bg=PRIMARY_COLOR
        ).pack(side=tk.LEFT, padx=5)
        
        create_button(
            button_frame,
            "Clear Form",
            command=self.clear_form,
            bg="#6C757D"
        ).pack(side=tk.LEFT, padx=5)
        
        create_button(
            button_frame,
            "Back to Dashboard",
            command=self.back_to_dashboard,
            bg="#DC3545"
        ).pack(side=tk.RIGHT, padx=5)
    
    def register_patient(self):
        # Get form data
        name = self.name_entry.get().strip()
        dob = self.dob_entry.get().strip()
        gender = self.gender_var.get()
        contact = self.contact_entry.get().strip()
        address = self.address_text.get("1.0", tk.END).strip()
        
        # Validate required fields
        if not validate_required_fields({
            "Patient Name": name,
            "Date of Birth": dob,
            "Contact Number": contact,
            "Address": address
        }):
            return
        
        # Format date
        formatted_dob = format_date(dob)
        if not formatted_dob:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD")
            return
        
        # Mock registration - in real app this would save to database
        messagebox.showinfo("Success", f"Patient {name} registered successfully!")
        
        # Clear form after successful registration
        self.clear_form()
    
    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.dob_entry.delete(0, tk.END)
        self.gender_var.set("M")
        self.contact_entry.delete(0, tk.END)
        self.address_text.delete("1.0", tk.END)
    
    def back_to_dashboard(self):
        self.root.destroy()