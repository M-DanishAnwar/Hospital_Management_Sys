"""
Admin Dashboard View
"""

import tkinter as tk
from tkinter import ttk
from app.utils.style import (
    PRIMARY_COLOR, BACKGROUND_COLOR, TEXT_COLOR,
    TITLE_FONT, NORMAL_FONT, BUTTON_FONT,
    create_button, create_card
)
from app.services.auth import auth_service

class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard - Hospital Management System")
        self.root.geometry("1000x700")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=BACKGROUND_COLOR)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            header_frame,
            text="🏥 Admin Dashboard",
            font=TITLE_FONT,
            fg=PRIMARY_COLOR,
            bg=BACKGROUND_COLOR
        ).pack(side=tk.LEFT)
        
        # Welcome message
        user = auth_service.get_current_user()
        tk.Label(
            header_frame,
            text=f"Welcome, {user.username}! 👋",
            font=BUTTON_FONT,
            fg=TEXT_COLOR,
            bg=BACKGROUND_COLOR
        ).pack(side=tk.RIGHT, padx=20)
        
        # Stats cards
        stats_frame = tk.Frame(main_frame, bg=BACKGROUND_COLOR)
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.create_stats_card(stats_frame, "🏥 Total Patients", "1,245", "#4361ee")
        self.create_stats_card(stats_frame, "👨‍⚕️ Total Doctors", "42", "#3f37c9")
        self.create_stats_card(stats_frame, "📅 Today's Appointments", "28", "#4895ef")
        self.create_stats_card(stats_frame, "💰 Total Revenue", "$245,678", "#4cc9f0")
        
        # Main content area with notebook
        content_frame = tk.Frame(main_frame, bg=BACKGROUND_COLOR)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook
        notebook = ttk.Notebook(content_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Dashboard tab
        dashboard_tab = tk.Frame(notebook, bg=BACKGROUND_COLOR)
        notebook.add(dashboard_tab, text="📊 Dashboard")
        
        # Quick Actions tab
        actions_tab = tk.Frame(notebook, bg=BACKGROUND_COLOR)
        notebook.add(actions_tab, text="⚡ Quick Actions")
        
        # Analytics tab
        analytics_tab = tk.Frame(notebook, bg=BACKGROUND_COLOR)
        notebook.add(analytics_tab, text="📈 Analytics")
        
        # Create dashboard content
        self.create_dashboard_content(dashboard_tab)
        
        # Create quick actions content
        self.create_quick_actions(actions_tab)
    
    def create_stats_card(self, parent, title, value, color):
        """Create a statistics card"""
        card = tk.Frame(parent, bg="white", relief=tk.RAISED, borderwidth=1)
        card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Color bar
        color_bar = tk.Frame(card, bg=color, height=5)
        color_bar.pack(fill=tk.X)
        
        # Content
        content_frame = tk.Frame(card, bg="white", padx=15, pady=15)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            content_frame,
            text=title,
            font=("Segoe UI", 10, "bold"),
            fg="#666",
            bg="white"
        ).pack(anchor=tk.W)
        
        tk.Label(
            content_frame,
            text=value,
            font=("Segoe UI", 20, "bold"),
            fg=color,
            bg="white"
        ).pack(anchor=tk.W, pady=(5, 0))
    
    def create_dashboard_content(self, parent):
        """Create dashboard content with charts and statistics"""
        # Main grid layout
        grid_frame = tk.Frame(parent, bg=BACKGROUND_COLOR)
        grid_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left column - Recent activities
        left_frame = tk.Frame(grid_frame, bg=BACKGROUND_COLOR)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Right column - Quick stats
        right_frame = tk.Frame(grid_frame, bg=BACKGROUND_COLOR)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Recent patients card
        recent_patients_card = create_card(left_frame, fill=tk.BOTH, expand=True, pady=(0, 10))
        
        tk.Label(
            recent_patients_card,
            text="👥 Recent Patients",
            font=BUTTON_FONT,
            fg=PRIMARY_COLOR,
            bg="white"
        ).pack(pady=10, anchor=tk.W, padx=10)
        
        # Patient list
        patient_list = tk.Frame(recent_patients_card, bg="white")
        patient_list.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        patients = [
            ("John Doe", "2024-01-15", "Cardiology"),
            ("Jane Smith", "2024-01-14", "Neurology"),
            ("Robert Johnson", "2024-01-14", "Pediatrics"),
            ("Mary Williams", "2024-01-13", "Orthopedics")
        ]
        
        for i, (name, date, dept) in enumerate(patients):
            patient_frame = tk.Frame(patient_list, bg="#f8f9fa" if i % 2 == 0 else "white")
            patient_frame.pack(fill=tk.X, pady=2)
            
            tk.Label(
                patient_frame,
                text=f"• {name}",
                font=NORMAL_FONT,
                bg=patient_frame["bg"]
            ).pack(side=tk.LEFT, padx=10, pady=5)
            
            tk.Label(
                patient_frame,
                text=date,
                font=("Segoe UI", 9),
                fg="#6c757d",
                bg=patient_frame["bg"]
            ).pack(side=tk.RIGHT, padx=10, pady=5)
        
        # System status card
        status_card = create_card(right_frame, fill=tk.BOTH, expand=True, pady=(0, 10))
        
        tk.Label(
            status_card,
            text="⚙️ System Status",
            font=BUTTON_FONT,
            fg=PRIMARY_COLOR,
            bg="white"
        ).pack(pady=10, anchor=tk.W, padx=10)
        
        status_items = [
            ("Database", "✅ Online", "green"),
            ("Backup", "✅ Last: 2024-01-15 02:00", "green"),
            ("API Services", "✅ Running", "green"),
            ("Storage", "⚠️ 85% used", "orange")
        ]
        
        for item in status_items:
            item_frame = tk.Frame(status_card, bg="white")
            item_frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(
                item_frame,
                text=item[0],
                font=NORMAL_FONT,
                bg="white"
            ).pack(side=tk.LEFT)
            
            tk.Label(
                item_frame,
                text=item[1],
                font=NORMAL_FONT,
                fg=item[2],
                bg="white"
            ).pack(side=tk.RIGHT)
    
    def create_quick_actions(self, parent):
        """Create quick actions panel"""
        actions_frame = tk.Frame(parent, bg=BACKGROUND_COLOR, padx=20, pady=20)
        actions_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            actions_frame,
            text="⚡ Quick Actions",
            font=TITLE_FONT,
            fg=PRIMARY_COLOR,
            bg=BACKGROUND_COLOR
        ).pack(pady=(0, 20))
        
        # Action buttons grid
        buttons_frame = tk.Frame(actions_frame, bg=BACKGROUND_COLOR)
        buttons_frame.pack(fill=tk.BOTH, expand=True)
        
        # Row 1
        row1 = tk.Frame(buttons_frame, bg=BACKGROUND_COLOR)
        row1.pack(fill=tk.X, pady=10)
        
        self.create_action_button(row1, "🏥 Register Patient", "#4CC9F0")
        self.create_action_button(row1, "👨‍⚕️ Add Doctor", "#4361EE")
        self.create_action_button(row1, "📅 Schedule Appointment", "#3F37C9")
        
        # Row 2
        row2 = tk.Frame(buttons_frame, bg=BACKGROUND_COLOR)
        row2.pack(fill=tk.X, pady=10)
        
        self.create_action_button(row2, "📋 View Medical Records", "#4895EF")
        self.create_action_button(row2, "💰 Process Billing", "#F72585")
        self.create_action_button(row2, "📊 Generate Reports", "#7209B7")
        
        # Row 3
        row3 = tk.Frame(buttons_frame, bg=BACKGROUND_COLOR)
        row3.pack(fill=tk.X, pady=10)
        
        self.create_action_button(row3, "👥 Manage Users", "#4CC9F0")
        self.create_action_button(row3, "🔒 System Settings", "#3F37C9")
        self.create_action_button(row3, "🚪 Logout", "#DC3545")
    
    def create_action_button(self, parent, text, color):
        """Create a styled action button"""
        button = tk.Button(
            parent,
            text=text,
            font=BUTTON_FONT,
            bg=color,
            fg="white",
            relief=tk.RAISED,
            borderwidth=1,
            padx=20,
            pady=15,
            cursor="hand2"
        )
        button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Add hover effect
        button.bind('<Enter>', lambda e: button.config(bg=self.darken_color(color)))
        button.bind('<Leave>', lambda e: button.config(bg=color))
        
        return button
    
    def darken_color(self, color):
        """Darken a hex color for hover effect"""
        if color.startswith('#'):
            color = color[1:]
        r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
        r, g, b = max(0, r-30), max(0, g-30), max(0, b-30)
        return f'#{r:02x}{g:02x}{b:02x}'