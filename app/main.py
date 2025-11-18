"""
Main entry point for the Hospital Management System
"""

import tkinter as tk
from app.views.login import LoginView
from app.utils.style import apply_style

def main():
    # Create main window
    root = tk.Tk()
    root.title("Hospital Management System")
    root.geometry("800x600")
    
    # Apply global styles
    apply_style(root)
    
    # Create login view
    LoginView(root)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()