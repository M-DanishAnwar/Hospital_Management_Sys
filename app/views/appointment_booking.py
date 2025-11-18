"""
Appointment Booking View
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta
from app.utils.style import (
    PRIMARY_COLOR, BACKGROUND_COLOR, TEXT_COLOR,
    TITLE_FONT, NORMAL_FONT, BUTTON_FONT,
    create_button, create_entry, create_label, create_card
)
from app.utils.helpers import validate_required_fields, format_date

class AppointmentBookingView:
    def __init__(self, root):
        self.root = root
        self.root.title("Appointment Booking")
        self.root.geometry("900x700")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header = tk.Label(
            main_frame, 
            text="📅 Appointment Booking", 
            font=TITLE_FONT, 
            fg=PRIMARY_COLOR, 
            bg=BACKGROUND_COLOR
        )
        header.pack(pady=(0, 20))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Book Appointment tab
        book_appointment_frame = tk.Frame(notebook, bg=BACKGROUND_COLOR)
        notebook.add(book_appointment_frame, text="Book Appointment")
        
        # View Appointments tab
        view_appointments_frame = tk.Frame(notebook, bg=BACKGROUND_COLOR)
        notebook.add(view_appointments_frame, text="View Appointments")
        
        # Book Appointment Form
        self.create_booking_form(book_appointment_frame)
        
        # View Appointments Table
        self.create_appointments_table(view_appointments_frame)
    
    def create_booking_form(self, parent):
        # Form card
        form_card = create_card(parent, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Form fields
        form_frame = tk.Frame(form_card, bg="white", padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Patient selection
        create_label(form_frame, "Patient:", font=BUTTON_FONT)
        self.patient_var = tk.StringVar()
        patient_options = ["John Doe (ID: 1)", "Jane Smith (ID: 2)", "Robert Johnson (ID: 3)"]
        patient_dropdown = ttk.Combobox(form_frame, textvariable=self.patient_var, values=patient_options, font=NORMAL_FONT)
        patient_dropdown.pack(fill=tk.X, pady=(0, 10))
        
        # Doctor selection
        create_label(form_frame, "Doctor:", font=BUTTON_FONT)
        self.doctor_var = tk.StringVar()
        doctor_options = ["Dr. Smith - Cardiology", "Dr. Johnson - Neurology", "Dr. Williams - Pediatrics"]
        doctor_dropdown = ttk.Combobox(form_frame, textvariable=self.doctor_var, values=doctor_options, font=NORMAL_FONT)
        doctor_dropdown.pack(fill=tk.X, pady=(0, 10))
        
        # Date selection
        create_label(form_frame, "Appointment Date:", font=BUTTON_FONT)
        self.date_entry = create_entry(form_frame)
        self.date_entry.pack(fill=tk.X, pady=(0, 10))
        self.date_entry.insert(0, (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'))
        
        # Time selection
        create_label(form_frame, "Appointment Time:", font=BUTTON_FONT)
        time_frame = tk.Frame(form_frame, bg="white")
        time_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.time_var = tk.StringVar(value="09:00")
        time_options = ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]
        time_dropdown = ttk.Combobox(time_frame, textvariable=self.time_var, values=time_options, font=NORMAL_FONT, width=10)
        time_dropdown.pack(side=tk.LEFT)
        
        # Status
        create_label(form_frame, "Status:", font=BUTTON_FONT)
        self.status_var = tk.StringVar(value="Scheduled")
        status_options = ["Scheduled", "Completed", "Cancelled"]
        status_dropdown = ttk.Combobox(form_frame, textvariable=self.status_var, values=status_options, font=NORMAL_FONT)
        status_dropdown.pack(fill=tk.X, pady=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg="white")
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        create_button(
            button_frame,
            "Book Appointment",
            command=self.book_appointment,
            bg=PRIMARY_COLOR
        ).pack(side=tk.LEFT, padx=5)
        
        create_button(
            button_frame,
            "Check Doctor Availability",
            command=self.check_availability,
            bg="#17A2B8"
        ).pack(side=tk.LEFT, padx=5)
    
    def create_appointments_table(self, parent):
        # Table card
        table_card = create_card(parent, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview
        columns = ('id', 'patient', 'doctor', 'date', 'time', 'status')
        self.tree = ttk.Treeview(table_card, columns=columns, show='headings')
        
        # Configure columns
        self.tree.heading('id', text='ID')
        self.tree.heading('patient', text='Patient')
        self.tree.heading('doctor', text='Doctor')
        self.tree.heading('date', text='Date')
        self.tree.heading('time', text='Time')
        self.tree.heading('status', text='Status')
        
        self.tree.column('id', width=50)
        self.tree.column('patient', width=150)
        self.tree.column('doctor', width=150)
        self.tree.column('date', width=100)
        self.tree.column('time', width=80)
        self.tree.column('status', width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_card, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add mock data
        self.load_mock_appointments()
        
        # Buttons frame
        button_frame = tk.Frame(table_card, bg=BACKGROUND_COLOR)
        button_frame.pack(fill=tk.X, pady=10)
        
        create_button(
            button_frame,
            "Refresh",
            command=self.load_mock_appointments,
            bg="#17A2B8"
        ).pack(side=tk.LEFT, padx=5)
        
        create_button(
            button_frame,
            "Edit Selected",
            command=self.edit_appointment,
            bg="#FFC107"
        ).pack(side=tk.LEFT, padx=5)
        
        create_button(
            button_frame,
            "Cancel Selected",
            command=self.cancel_appointment,
            bg="#DC3545"
        ).pack(side=tk.LEFT, padx=5)
    
    def book_appointment(self):
        patient = self.patient_var.get()
        doctor = self.doctor_var.get()
        date = self.date_entry.get().strip()
        time = self.time_var.get()
        status = self.status_var.get()
        
        if not validate_required_fields({
            "Patient": patient,
            "Doctor": doctor,
            "Date": date,
            "Time": time
        }):
            return
        
        # Mock booking - in real app this would save to database
        appointment_id = f"A{datetime.now().strftime('%Y%m%d%H%M%S')}"
        messagebox.showinfo("Success", f"Appointment booked successfully!\nAppointment ID: {appointment_id}\nPatient: {patient}\nDoctor: {doctor}\nDate: {date} at {time}")
        
        # Refresh the table
        self.load_mock_appointments()
    
    def check_availability(self):
        doctor = self.doctor_var.get()
        date = self.date_entry.get().strip()
        
        if not doctor or not date:
            messagebox.showwarning("Warning", "Please select doctor and date first")
            return
        
        available_slots = ["09:00", "11:00", "14:00", "16:00"]
        booked_slots = ["10:00", "15:00"]
        
        availability_text = f" Availability for {doctor} on {date}:\n\n"
        availability_text += "✅ Available: " + ", ".join(available_slots) + "\n"
        availability_text += "❌ Booked: " + ", ".join(booked_slots)
        
        messagebox.showinfo("Doctor Availability", availability_text)
    
    def load_mock_appointments(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add mock data
        mock_appointments = [
            (1, "John Doe", "Dr. Smith - Cardiology", "2024-01-16", "09:00", "Scheduled"),
            (2, "Jane Smith", "Dr. Johnson - Neurology", "2024-01-16", "10:00", "Scheduled"),
            (3, "Robert Johnson", "Dr. Williams - Pediatrics", "2024-01-17", "14:00", "Completed"),
            (4, "Mary Williams", "Dr. Smith - Cardiology", "2024-01-18", "11:00", "Scheduled")
        ]
        
        for appt in mock_appointments:
            self.tree.insert('', tk.END, values=appt)
    
    def edit_appointment(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an appointment to edit")
            return
        
        item = self.tree.item(selected_item[0])
        appt_data = item['values']
        messagebox.showinfo("Edit Appointment", f"Editing appointment ID: {appt_data[0]}")
    
    def cancel_appointment(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an appointment to cancel")
            return
        
        if messagebox.askyesno("Confirm Cancel", "Are you sure you want to cancel this appointment?"):
            self.tree.delete(selected_item[0])
            messagebox.showinfo("Success", "Appointment cancelled successfully!")