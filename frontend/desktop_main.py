
import customtkinter as ctk
from .desktop_styles import COLORS
from .ui_components import SidebarButton, InfoCard
from .views.dashboard_view import DashboardView
from .views.recordings_view import RecordingsView, FilesView
from .views.camera_test_view import CameraTestView
from .views.settings_view import SettingsView

# Default to Dark Mode
# Default to Dark Mode initially, but allow switching
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AInomalyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AInomaly Desktop")
        self.geometry("1280x720")
        self.minsize(1024, 600)
        
        # Configure Main Layout (Sidebar + Content)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color=COLORS["sidebar_bg"])
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(10, weight=1) # Spacer

        # Logo
        self.logo_label = ctk.CTkLabel(
            self.sidebar, text="🛡️ AINOMALY", 
            font=("Inter", 20, "bold"), 
            text_color=COLORS["primary"]
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # Nav Buttons
        self.nav_buttons = {}
        sections = ["Dashboard", "Grabaciones", "Archivos", "Test Cámara", "Configuración"]
        
        for i, section in enumerate(sections):
            btn = SidebarButton(self.sidebar, text=section, command=lambda s=section: self.show_view(s))
            btn.grid(row=i+1, column=0, padx=10, pady=5, sticky="ew")
            self.nav_buttons[section] = btn
            
        # Status
        self.status_lbl = ctk.CTkLabel(
            self.sidebar, text="🟢 En Línea — v3.1", 
            text_color=COLORS["text_secondary"]
        )
        self.status_lbl.grid(row=11, column=0, padx=20, pady=20, sticky="w")

        # --- Main Content Area ---
        self.content_area = ctk.CTkFrame(self, corner_radius=0, fg_color=COLORS["content_bg"])
        self.content_area.grid(row=0, column=1, sticky="nsew")
        
        # Initialize
        self.current_view = None
        self.show_view("Dashboard")



    def show_view(self, view_name):
        # Update Nav State
        for name, btn in self.nav_buttons.items():
            if name == view_name:
                btn.set_active()
            else:
                btn.set_inactive()
        
        # Clear Content
        for widget in self.content_area.winfo_children():
            widget.destroy()

        # Title
        title = ctk.CTkLabel(
            self.content_area, text=view_name, 
            font=("Inter", 28, "bold"), 
            text_color=COLORS["accent_text"]
        )
        title.pack(pady=(20, 10), padx=30, anchor="w")

        # Render View
        if view_name == "Dashboard":
            view = DashboardView(self.content_area)
            view.pack(fill="both", expand=True)
            
        elif view_name == "Grabaciones":
            view = RecordingsView(self.content_area)
            view.pack(fill="both", expand=True, padx=30, pady=10)
            
        elif view_name == "Archivos":
            view = FilesView(self.content_area)
            view.pack(fill="both", expand=True, padx=30, pady=10)

        elif view_name == "Test Cámara":
            view = CameraTestView(self.content_area)
            view.pack(fill="both", expand=True, padx=30, pady=10)

        elif view_name == "Configuración":
            view = SettingsView(self.content_area)
            view.pack(fill="both", expand=True, padx=30, pady=10)
            
        else:
            self.render_placeholder(f"Vista: {view_name} (En Construcción)")

    def render_placeholder(self, text):
        lbl = ctk.CTkLabel(self.content_area, text=text, font=("Inter", 16), text_color=COLORS["text_secondary"])
        lbl.pack(pady=50)

if __name__ == "__main__":
    app = AInomalyApp()
    app.mainloop()
