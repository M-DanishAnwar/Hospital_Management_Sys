"""
Billing View
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from app.utils.style import (
    PRIMARY_COLOR, BACKGROUND_COLOR, TEXT_COLOR,
    TITLE_FONT, NORMAL_FONT, BUTTON_FONT,
    create_button, create_entry, create_label, create_card
)
from app.utils.helpers import validate_required_fields, format_currency, format_date

class BillingView:
    def __init__(self, root):
        self.root = root
        self.root.title("Billing & Payments")
        self.root.geometry("900x700")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header = tk.Label(
            main_frame, 
            text="💰 Billing & Payments", 
            font=TITLE_FONT, 
            fg=PRIMARY_COLOR, 
            bg=BACKGROUND_COLOR
        )
        header.pack(pady=(0, 20))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create Bill tab
        create_bill_frame = tk.Frame(notebook, bg=BACKGROUND_COLOR)
        notebook.add(create_bill_frame, text="Create Bill")
        
        # View Bills tab
        view_bills_frame = tk.Frame(notebook, bg=BACKGROUND_COLOR)
        notebook.add(view_bills_frame, text="View Bills")
        
        # Payments tab
        payments_frame = tk.Frame(notebook, bg=BACKGROUND_COLOR)
        notebook.add(payments_frame, text="Payments")
        
        # Create Bill Form
        self.create_bill_form(create_bill_frame)
        
        # View Bills Table
        self.create_bills_table(view_bills_frame)
        
        # Payments Panel
        self.create_payments_panel(payments_frame)
    
    def create_bill_form(self, parent):
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
        
        # Bill date
        create_label(form_frame, "Bill Date:", font=BUTTON_FONT)
        self.bill_date_entry = create_entry(form_frame)
        self.bill_date_entry.pack(fill=tk.X, pady=(0, 10))
        self.bill_date_entry.insert(0, format_date(datetime.now().strftime('%Y-%m-%d')))
        
        # Amount
        create_label(form_frame, "Amount ($):", font=BUTTON_FONT)
        self.amount_entry = create_entry(form_frame)
        self.amount_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Description
        create_label(form_frame, "Description:", font=BUTTON_FONT)
        self.description_text = tk.Text(form_frame, height=4, font=NORMAL_FONT)
        self.description_text.pack(fill=tk.X, pady=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg="white")
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        create_button(
            button_frame,
            "Generate Bill",
            command=self.generate_bill,
            bg=PRIMARY_COLOR
        ).pack(side=tk.LEFT, padx=5)
        
        create_button(
            button_frame,
            "Clear Form",
            command=self.clear_form,
            bg="#6C757D"
        ).pack(side=tk.LEFT, padx=5)
    
    def create_bills_table(self, parent):
        # Table card
        table_card = create_card(parent, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview
        columns = ('id', 'patient', 'amount', 'date', 'status', 'description')
        self.tree = ttk.Treeview(table_card, columns=columns, show='headings')
        
        # Configure columns
        self.tree.heading('id', text='Bill ID')
        self.tree.heading('patient', text='Patient')
        self.tree.heading('amount', text='Amount')
        self.tree.heading('date', text='Date')
        self.tree.heading('status', text='Status')
        self.tree.heading('description', text='Description')
        
        self.tree.column('id', width=80)
        self.tree.column('patient', width=150)
        self.tree.column('amount', width=100)
        self.tree.column('date', width=100)
        self.tree.column('status', width=80)
        self.tree.column('description', width=200)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_card, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add mock data
        self.load_mock_bills()
        
        # Buttons frame
        button_frame = tk.Frame(table_card, bg=BACKGROUND_COLOR)
        button_frame.pack(fill=tk.X, pady=10)
        
        create_button(
            button_frame,
            "Refresh",
            command=self.load_mock_bills,
            bg="#17A2B8"
        ).pack(side=tk.LEFT, padx=5)
        
        create_button(
            button_frame,
            "View Details",
            command=self.view_bill_details,
            bg="#28A745"
        ).pack(side=tk.LEFT, padx=5)
        
        create_button(
            button_frame,
            "Mark as Paid",
            command=self.mark_as_paid,
            bg="#FFC107"
        ).pack(side=tk.LEFT, padx=5)
    
    def create_payments_panel(self, parent):
        # Summary card
        summary_card = create_card(parent, fill=tk.X, pady=(0, 10))
        
        summary_frame = tk.Frame(summary_card, bg="white", padx=20, pady=20)
        summary_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            summary_frame,
            text="📊 Billing Summary",
            font=BUTTON_FONT,
            fg=PRIMARY_COLOR,
            bg="white"
        ).pack(pady=(0, 10))
        
        # Summary stats
        stats_frame = tk.Frame(summary_frame, bg="white")
        stats_frame.pack(fill=tk.X)
        
        stats = [
            ("Total Revenue", "$24,567.89"),
            ("Unpaid Bills", "$3,456.78"),
            ("Paid Bills", "$21,111.11"),
            ("Avg. Bill Amount", "$153.24")
        ]
        
        for i, (label, value) in enumerate(stats):
            stat_frame = tk.Frame(stats_frame, bg="white")
            stat_frame.grid(row=i//2, column=i%2, padx=10, pady=5, sticky="w")
            
            tk.Label(
                stat_frame,
                text=label,
                font=("Segoe UI", 10),
                fg="#666",
                bg="white"
            ).pack(side=tk.LEFT)
            
            tk.Label(
                stat_frame,
                text=value,
                font=("Segoe UI", 12, "bold"),
                fg=PRIMARY_COLOR,
                bg="white"
            ).pack(side=tk.LEFT, padx=(5, 0))
        
        # Recent payments
        payments_card = create_card(parent, fill=tk.BOTH, expand=True, pady=(10, 0))
        
        payments_frame = tk.Frame(payments_card, bg="white", padx=20, pady=20)
        payments_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            payments_frame,
            text="💸 Recent Payments",
            font=BUTTON_FONT,
            fg=PRIMARY_COLOR,
            bg="white"
        ).pack(pady=(0, 10))
        
        # Payment list
        payment_list = tk.Frame(payments_frame, bg="white")
        payment_list.pack(fill=tk.X)
        
        payments = [
            ("INV-001", "John Doe", "$150.00", "2024-01-15", "Credit Card"),
            ("INV-002", "Jane Smith", "$85.50", "2024-01-14", "Cash"),
            ("INV-003", "Robert Johnson", "$200.00", "2024-01-13", "Insurance")
        ]
        
        for payment in payments:
            payment_frame = tk.Frame(payment_list, bg="#f8f9fa", pady=5)
            payment_frame.pack(fill=tk.X, pady=2)
            
            tk.Label(
                payment_frame,
                text=f"Bill: {payment[0]} | Patient: {payment[1]} | Amount: {payment[2]}",
                font=NORMAL_FONT,
                bg="#f8f9fa"
            ).pack(side=tk.LEFT, padx=10)
            
            tk.Label(
                payment_frame,
                text=f"{payment[3]} ({payment[4]})",
                font=("Segoe UI", 9),
                fg="#6c757d",
                bg="#f8f9fa"
            ).pack(side=tk.RIGHT, padx=10)
    
    def generate_bill(self):
        patient = self.patient_var.get()
        bill_date = self.bill_date_entry.get().strip()
        amount = self.amount_entry.get().strip()
        description = self.description_text.get("1.0", tk.END).strip()
        
        if not validate_required_fields({
            "Patient": patient,
            "Bill Date": bill_date,
            "Amount": amount,
            "Description": description
        }):
            return
        
        try:
            amount_value = float(amount)
            if amount_value <= 0:
                raise ValueError("Amount must be positive")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid amount: {str(e)}")
            return
        
        # Mock generation - in real app this would save to database
        bill_id = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        formatted_amount = format_currency(amount_value)
        
        messagebox.showinfo("Success", f"Bill generated successfully!\nBill ID: {bill_id}\nPatient: {patient}\nAmount: {formatted_amount}\nDate: {bill_date}")
        
        # Clear form
        self.clear_form()
        
        # Refresh the table
        self.load_mock_bills()
    
    def clear_form(self):
        self.patient_var.set("")
        self.bill_date_entry.delete(0, tk.END)
        self.bill_date_entry.insert(0, format_date(datetime.now().strftime('%Y-%m-%d')))
        self.amount_entry.delete(0, tk.END)
        self.description_text.delete("1.0", tk.END)
    
    def load_mock_bills(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add mock data
        mock_bills = [
            (1001, "John Doe", "$150.00", "2024-01-15", "Paid", "Consultation fee"),
            (1002, "Jane Smith", "$85.50", "2024-01-14", "Unpaid", "Medication charges"),
            (1003, "Robert Johnson", "$200.00", "2024-01-13", "Paid", "Follow-up visit"),
            (1004, "Mary Williams", "$350.75", "2024-01-12", "Unpaid", "Lab tests")
        ]
        
        for bill in mock_bills:
            self.tree.insert('', tk.END, values=bill)
    
    def view_bill_details(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a bill to view details")
            return
        
        item = self.tree.item(selected_item[0])
        bill_data = item['values']
        
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Bill Details - ID: {bill_data[0]}")
        details_window.geometry("600x400")
        
        details_frame = tk.Frame(details_window, padx=20, pady=20)
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        details_text = tk.Text(details_frame, wrap=tk.WORD, font=NORMAL_FONT)
        details_text.pack(fill=tk.BOTH, expand=True)
        
        details = f"""
Bill Details
============

Bill ID: {bill_data[0]}
Patient: {bill_data[1]}
Amount: {bill_data[2]}
Date: {bill_data[3]}
Status: {bill_data[4]}

Description:
------------
{bill_data[5]}

Payment Information:
-------------------
Payment Method: Credit Card
Transaction ID: TXN{bill_data[0]}2024
Payment Date: {bill_data[3]}

Notes:
-----
This is an official bill from Hospital Management System.
Please contact billing department for any queries.
        """
        
        details_text.insert(tk.END, details)
        details_text.config(state=tk.DISABLED)
    
    def mark_as_paid(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a bill to mark as paid")
            return
        
        item = self.tree.item(selected_item[0])
        bill_data = item['values']
        
        if bill_data[4] == "Paid":
            messagebox.showinfo("Info", "This bill is already paid")
            return
        
        if messagebox.askyesno("Confirm Payment", f"Mark bill {bill_data[0]} as paid?"):
            # In real app, this would update the database
            new_values = list(bill_data)
            new_values[4] = "Paid"
            self.tree.item(selected_item[0], values=tuple(new_values))
            messagebox.showinfo("Success", f"Bill {bill_data[0]} marked as paid successfully!")