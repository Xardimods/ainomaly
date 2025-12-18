
import customtkinter as ctk
from .desktop_styles import COLORS

class SidebarButton(ctk.CTkButton):
    def __init__(self, master, text, command=None, is_active=False):
        super().__init__(
            master, 
            text=text, 
            command=command,
            width=200, 
            height=40,
            corner_radius=8,
            anchor="w",
            font=("Inter", 14),
            fg_color="transparent",
            text_color=COLORS["text_secondary"],
            hover_color=COLORS["primary_hover"]
        )
        self.is_active = is_active
        if is_active:
            self.set_active()

    def set_active(self):
        self.configure(
            fg_color=COLORS["primary"], 
            text_color=COLORS["text_inverse"],
            font=("Inter", 14, "bold")
        )

    def set_inactive(self):
        self.configure(
            fg_color="transparent", 
            text_color=COLORS["text_secondary"],
            font=("Inter", 14)
        )

class InfoCard(ctk.CTkFrame):
    def __init__(self, master, title, value, subtext):
        super().__init__(master, corner_radius=12, fg_color=COLORS["card_bg"])
        
        self.grid_columnconfigure(0, weight=1)
        
        self.lbl_title = ctk.CTkLabel(
            self, text=title.upper(), 
            font=("Inter", 12, "bold"), 
            text_color=COLORS["accent_text"]
        )
        self.lbl_title.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 0))
        
        self.lbl_value = ctk.CTkLabel(
            self, text=value, 
            font=("Inter", 24, "bold"), 
            text_color=COLORS["text_primary"]
        )
        self.lbl_value.grid(row=1, column=0, sticky="w", padx=15, pady=(5, 0))
        
        self.lbl_sub = ctk.CTkLabel(
            self, text=subtext, 
            font=("Inter", 11), 
            text_color=COLORS["text_secondary"]
        )
        self.lbl_sub.grid(row=2, column=0, sticky="w", padx=15, pady=(5, 15))

