"""
Style constants for the Hospital Management System UI
Uses lemon yellow and sky blue color scheme as requested
"""

import tkinter as tk 

# Color Scheme
PRIMARY_COLOR = "#4CC9F0"      # Sky Blue (primary buttons, headers)
SECONDARY_COLOR = "#72EFDD"    # Teal accent
BACKGROUND_COLOR = "#F8F9FA"   # Light background
CARD_COLOR = "#FFFFFF"         # White cards
TEXT_COLOR = "#212529"         # Dark text
TEXT_LIGHT = "#6C757D"         # Light text (secondary)
DANGER_COLOR = "#EF4444"       # Red (delete, errors)
SUCCESS_COLOR = "#10B981"      # Green (success messages)
WARNING_COLOR = "#F59E0B"      # Amber (warnings)

# Lemon Yellow accent colors
ACCENT_YELLOW = "#F9C74F"      # Lemon Yellow
ACCENT_YELLOW_LIGHT = "#FDF8E3" # Light yellow background

# Fonts
FONT_FAMILY = "Segoe UI"
HEADER_FONT = (FONT_FAMILY, 16, "bold")
TITLE_FONT = (FONT_FAMILY, 24, "bold")
NORMAL_FONT = (FONT_FAMILY, 12)
SMALL_FONT = (FONT_FAMILY, 10)
BUTTON_FONT = (FONT_FAMILY, 12, "bold")

# Spacing and sizing
PADDING_SMALL = 5
PADDING_MEDIUM = 10
PADDING_LARGE = 20
BUTTON_WIDTH = 15
INPUT_WIDTH = 30

def apply_style(root):
    """Apply global style settings to the root window"""
    root.configure(bg=BACKGROUND_COLOR)
    
def create_card(parent, **kwargs):
    """Create a styled card/frame with consistent appearance"""
    frame = tk.Frame(parent, bg=CARD_COLOR, relief=tk.RAISED, borderwidth=1)
    if 'padx' not in kwargs:
        kwargs['padx'] = PADDING_MEDIUM
    if 'pady' not in kwargs:
        kwargs['pady'] = PADDING_MEDIUM
    frame.pack(**kwargs)
    return frame

def create_header(parent, text, **kwargs):
    """Create a styled header"""
    label = tk.Label(parent, text=text, font=TITLE_FONT, fg=PRIMARY_COLOR, bg=BACKGROUND_COLOR)
    if 'pady' not in kwargs:
        kwargs['pady'] = PADDING_LARGE
    label.pack(**kwargs)
    return label

def create_button(parent, text, command=None, **kwargs):
    """Create a styled button"""
    if 'bg' not in kwargs:
        kwargs['bg'] = PRIMARY_COLOR
    if 'fg' not in kwargs:
        kwargs['fg'] = "white"
    if 'font' not in kwargs:
        kwargs['font'] = BUTTON_FONT
    if 'width' not in kwargs:
        kwargs['width'] = BUTTON_WIDTH
    
    button = tk.Button(parent, text=text, command=command, **kwargs)
    button.pack(pady=PADDING_SMALL)
    return button

def create_entry(parent, **kwargs):
    """Create a styled entry field"""
    entry = tk.Entry(parent, font=NORMAL_FONT, width=INPUT_WIDTH)
    entry.pack(pady=PADDING_SMALL, padx=PADDING_SMALL)
    return entry

def create_label(parent, text, **kwargs):
    """Create a styled label"""
    if 'font' not in kwargs:
        kwargs['font'] = NORMAL_FONT
    if 'bg' not in kwargs:
        kwargs['bg'] = BACKGROUND_COLOR
    
    label = tk.Label(parent, text=text, **kwargs)
    label.pack(pady=PADDING_SMALL, anchor=tk.W)
    return label