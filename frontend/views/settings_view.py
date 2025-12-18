
import customtkinter as ctk
from ..desktop_styles import COLORS

class SettingsView(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        self.grid_columnconfigure(0, weight=1)
        
        # Title Helper
        def add_section_title(text, row):
            lbl = ctk.CTkLabel(
                self, text=text, 
                font=("Inter", 18, "bold"), text_color=COLORS["text_primary"]
            )
            lbl.grid(row=row, column=0, sticky="w", pady=(20, 10))
            return row + 1

        # --- General Settings ---
        row = 0
        row = add_section_title("General", row)
        
        self.frame_general = ctk.CTkFrame(self, fg_color=COLORS["card_bg"], corner_radius=10)
        self.frame_general.grid(row=row, column=0, sticky="ew", pady=(0, 10))
        row += 1
        
        # Theme
        lbl_theme = ctk.CTkLabel(self.frame_general, text="Apariencia:", text_color=COLORS["text_primary"])
        lbl_theme.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        self.combo_theme = ctk.CTkComboBox(
            self.frame_general, 
            values=["Oscuro", "Claro", "Sistema"],
            width=200,
            fg_color=COLORS["card_bg"],
            dropdown_fg_color=COLORS["card_bg"]
        )
        self.combo_theme.grid(row=0, column=1, padx=20, pady=20, sticky="e")
        self.combo_theme.set("Oscuro")
        self.combo_theme.configure(command=self.change_theme)
        
    def change_theme(self, choice):
        if choice == "Oscuro":
            ctk.set_appearance_mode("Dark")
        elif choice == "Claro":
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("System")
        
        self.frame_general.grid_columnconfigure(1, weight=1)

        # --- Storage Settings ---
        row = add_section_title("Almacenamiento", row)
        
        self.frame_storage = ctk.CTkFrame(self, fg_color=COLORS["card_bg"], corner_radius=10)
        self.frame_storage.grid(row=row, column=0, sticky="ew", pady=(0, 10))
        row += 1
        
        lbl_path = ctk.CTkLabel(self.frame_storage, text="Ruta de Grabaciones:", text_color=COLORS["text_primary"])
        lbl_path.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        
        self.entry_path = ctk.CTkEntry(
            self.frame_storage, 
            width=300, 
            fg_color=COLORS["window_bg"], 
            border_color=COLORS["card_border"]
        )
        self.entry_path.grid(row=0, column=1, padx=10, pady=15, sticky="ew")
        self.entry_path.insert(0, "C:/Users/marti/Videos/AInomaly_Recs")
        
        btn_browse = ctk.CTkButton(
            self.frame_storage, text="Examinar...", width=100,
            fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"]
        )
        btn_browse.grid(row=0, column=2, padx=20, pady=15)
        
        self.frame_storage.grid_columnconfigure(1, weight=1)
        
        # --- Notifications ---
        row = add_section_title("Notificaciones", row)
        
        self.frame_notif = ctk.CTkFrame(self, fg_color=COLORS["card_bg"], corner_radius=10)
        self.frame_notif.grid(row=row, column=0, sticky="ew", pady=(0, 10))
        row += 1
        
        self.check_motion = ctk.CTkCheckBox(self.frame_notif, text="Alertar al detectar movimiento", text_color=COLORS["text_primary"], onvalue=True, offvalue=False)
        self.check_motion.grid(row=0, column=0, padx=20, pady=15, sticky="w")
        self.check_motion.select()
        
        self.check_sound = ctk.CTkCheckBox(self.frame_notif, text="Reproducir sonido de alarma", text_color=COLORS["text_primary"])
        self.check_sound.grid(row=1, column=0, padx=20, pady=15, sticky="w")
        
        self.check_email = ctk.CTkCheckBox(self.frame_notif, text="Enviar reporte diario por email", text_color=COLORS["text_primary"])
        self.check_email.grid(row=2, column=0, padx=20, pady=15, sticky="w")
        
        # --- About ---
        row = add_section_title("Acerca de", row)
        
        self.frame_about = ctk.CTkFrame(self, fg_color=COLORS["card_bg"], corner_radius=10)
        self.frame_about.grid(row=row, column=0, sticky="ew", pady=(0, 10))
        row += 1
        
        lbl_version = ctk.CTkLabel(self.frame_about, text="AInomaly Desktop v3.1.0", font=("Inter", 14, "bold"), text_color=COLORS["accent_text"])
        lbl_version.pack(pady=(20, 5))
        
        lbl_desc = ctk.CTkLabel(self.frame_about, text="Sistema de Videovigilancia Inteligente con Detección de Anomalías.\nDesarrollado con Python + CustomTkinter + OpenCV.", text_color=COLORS["text_secondary"])
        lbl_desc.pack(pady=(0, 20))
        
        btn_update = ctk.CTkButton(self.frame_about, text="Buscar Actualizaciones", fg_color="transparent", border_width=1, border_color=COLORS["primary"], text_color=COLORS["text_primary"])
        btn_update.pack(pady=(0, 20))

