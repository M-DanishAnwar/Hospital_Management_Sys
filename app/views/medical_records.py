"""
Medical Records View
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from app.utils.style import (
    PRIMARY_COLOR, BACKGROUND_COLOR, TEXT_COLOR,
    TITLE_FONT, NORMAL_FONT, BUTTON_FONT,
    create_button, create_entry, create_label, create_card
)
from app.utils.helpers import validate_required_fields, format_date

class MedicalRecordsView:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Records")
        self.root.geometry("900x700")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header = tk.Label(
            main_frame, 
            text="📋 Medical Records", 
            font=TITLE_FONT, 
            fg=PRIMARY_COLOR, 
            bg=BACKGROUND_COLOR
        )
        header.pack(pady=(0, 20))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Add Record tab
        add_record_frame = tk.Frame(notebook, bg=BACKGROUND_COLOR)
        notebook.add(add_record_frame, text="Add Medical Record")
        
        # View Records tab
        view_records_frame = tk.Frame(notebook, bg=BACKGROUND_COLOR)
        notebook.add(view_records_frame, text="View Medical Records")
        
        # Add Record Form
        self.create_record_form(add_record_frame)
        
        # View Records Table
        self.create_records_table(view_records_frame)
    
    def create_record_form(self, parent):
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
        
        # Visit date
        create_label(form_frame, "Visit Date:", font=BUTTON_FONT)
        self.visit_date_entry = create_entry(form_frame)
        self.visit_date_entry.pack(fill=tk.X, pady=(0, 10))
        self.visit_date_entry.insert(0, format_date(datetime.now().strftime('%Y-%m-%d')))
        
        # Diagnosis
        create_label(form_frame, "Diagnosis:", font=BUTTON_FONT)
        self.diagnosis_text = scrolledtext.ScrolledText(form_frame, height=4, font=NORMAL_FONT)
        self.diagnosis_text.pack(fill=tk.X, pady=(0, 10))
        
        # Prescription
        create_label(form_frame, "Prescription:", font=BUTTON_FONT)
        self.prescription_text = scrolledtext.ScrolledText(form_frame, height=4, font=NORMAL_FONT)
        self.prescription_text.pack(fill=tk.X, pady=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg="white")
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        create_button(
            button_frame,
            "Save Medical Record",
            command=self.save_medical_record,
            bg=PRIMARY_COLOR
        ).pack(side=tk.LEFT, padx=5)
        
        create_button(
            button_frame,
            "Clear Form",
            command=self.clear_form,
            bg="#6C757D"
        ).pack(side=tk.LEFT, padx=5)
    
    def create_records_table(self, parent):
        # Table card
        table_card = create_card(parent, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview
        columns = ('id', 'patient', 'doctor', 'diagnosis', 'date')
        self.tree = ttk.Treeview(table_card, columns=columns, show='headings')
        
        # Configure columns
        self.tree.heading('id', text='Record ID')
        self.tree.heading('patient', text='Patient')
        self.tree.heading('doctor', text='Doctor')
        self.tree.heading('diagnosis', text='Diagnosis')
        self.tree.heading('date', text='Visit Date')
        
        self.tree.column('id', width=80)
        self.tree.column('patient', width=150)
        self.tree.column('doctor', width=150)
        self.tree.column('diagnosis', width=200)
        self.tree.column('date', width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_card, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add mock data
        self.load_mock_records()
        
        # Buttons frame
        button_frame = tk.Frame(table_card, bg=BACKGROUND_COLOR)
        button_frame.pack(fill=tk.X, pady=10)
        
        create_button(
            button_frame,
            "Refresh",
            command=self.load_mock_records,
            bg="#17A2B8"
        ).pack(side=tk.LEFT, padx=5)
        
        create_button(
            button_frame,
            "View Details",
            command=self.view_record_details,
            bg="#28A745"
        ).pack(side=tk.LEFT, padx=5)
        
        create_button(
            button_frame,
            "Delete Selected",
            command=self.delete_record,
            bg="#DC3545"
        ).pack(side=tk.LEFT, padx=5)
    
    def save_medical_record(self):
        patient = self.patient_var.get()
        doctor = self.doctor_var.get()
        visit_date = self.visit_date_entry.get().strip()
        diagnosis = self.diagnosis_text.get("1.0", tk.END).strip()
        prescription = self.prescription_text.get("1.0", tk.END).strip()
        
        if not validate_required_fields({
            "Patient": patient,
            "Doctor": doctor,
            "Visit Date": visit_date,
            "Diagnosis": diagnosis
        }):
            return
        
        # Mock save - in real app this would save to database
        record_id = f"MR{datetime.now().strftime('%Y%m%d%H%M%S')}"
        messagebox.showinfo("Success", f"Medical record saved successfully!\nRecord ID: {record_id}\nPatient: {patient}\nDoctor: {doctor}")
        
        # Clear form
        self.clear_form()
        
        # Refresh the table
        self.load_mock_records()
    
    def clear_form(self):
        self.patient_var.set("")
        self.doctor_var.set("")
        self.visit_date_entry.delete(0, tk.END)
        self.visit_date_entry.insert(0, format_date(datetime.now().strftime('%Y-%m-%d')))
        self.diagnosis_text.delete("1.0", tk.END)
        self.prescription_text.delete("1.0", tk.END)
    
    def load_mock_records(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add mock data
        mock_records = [
            (101, "John Doe", "Dr. Smith - Cardiology", "Hypertension", "2024-01-15"),
            (102, "Jane Smith", "Dr. Johnson - Neurology", "Migraine", "2024-01-14"),
            (103, "Robert Johnson", "Dr. Williams - Pediatrics", "Common cold", "2024-01-13"),
            (104, "Mary Williams", "Dr. Smith - Cardiology", "Diabetes", "2024-01-12")
        ]
        
        for record in mock_records:
            self.tree.insert('', tk.END, values=record)
    
    def view_record_details(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record to view details")
            return
        
        item = self.tree.item(selected_item[0])
        record_data = item['values']
        
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Medical Record Details - ID: {record_data[0]}")
        details_window.geometry("600x400")
        
        details_frame = tk.Frame(details_window, padx=20, pady=20)
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        details_text = tk.Text(details_frame, wrap=tk.WORD, font=NORMAL_FONT)
        details_text.pack(fill=tk.BOTH, expand=True)
        
        details = f"""
Medical Record Details
========================

Record ID: {record_data[0]}
Patient: {record_data[1]}
Doctor: {record_data[2]}
Visit Date: {record_data[4]}

Diagnosis:
----------
{record_data[3]}

Prescription:
------------
- Paracetamol 500mg (3 times daily)
- Rest and plenty of fluids
- Follow up in 7 days

Notes:
-----
Patient is responding well to treatment. Blood pressure is stable.
Next appointment scheduled for next week.
        """
        
        details_text.insert(tk.END, details)
        details_text.config(state=tk.DISABLED)
    
    def delete_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record to delete")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this medical record?"):
            self.tree.delete(selected_item[0])
            messagebox.showinfo("Success", "Medical record deleted successfully!")