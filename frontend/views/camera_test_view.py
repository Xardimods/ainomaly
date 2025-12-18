
import customtkinter as ctk
from ..desktop_styles import COLORS

class CameraTestView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        # Grid Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # Video Area
        self.grid_rowconfigure(1, weight=0) # Controls
        
        # --- Video Placeholder ---
        self.video_frame = ctk.CTkFrame(
            self, 
            fg_color="black", 
            corner_radius=12,
            border_width=2,
            border_color=COLORS["sidebar_bg"]
        )
        self.video_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        # Centered Text in Video Frame
        self.no_signal_lbl = ctk.CTkLabel(
            self.video_frame, 
            text="NO SIGNAL", 
            text_color=COLORS["text_secondary"],
            font=("Inter", 24, "bold")
        )
        self.no_signal_lbl.place(relx=0.5, rely=0.5, anchor="center")
        
        # --- Controls Area ---
        self.controls_frame = ctk.CTkFrame(self, fg_color=COLORS["card_bg"], corner_radius=12)
        self.controls_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        
        # Camera Selection
        self.lbl_source = ctk.CTkLabel(self.controls_frame, text="Fuente de Video:", text_color=COLORS["text_primary"])
        self.lbl_source.pack(side="left", padx=(20, 10), pady=15)
        
        self.combo_source = ctk.CTkComboBox(
            self.controls_frame, 
            values=["Cámara Integrada (Webcam)", "RTSP Stream 1", "RTSP Stream 2", "Archivo de Video"],
            width=250,
            fg_color=COLORS["card_bg"],
            border_color=COLORS["primary"],
            button_color=COLORS["primary"],
            dropdown_fg_color=COLORS["card_bg"]
        )
        self.combo_source.pack(side="left", padx=10, pady=15)
        self.combo_source.set("Cámara Integrada (Webcam)")
        
        # Buttons
        self.btn_start = ctk.CTkButton(
            self.controls_frame, 
            text="▶ Iniciar", 
            fg_color=COLORS["primary"], 
            hover_color=COLORS["primary_hover"],
            width=100,
            command=self.start_camera
        )
        self.btn_start.pack(side="left", padx=20)
        
        self.btn_stop = ctk.CTkButton(
            self.controls_frame, 
            text="⏹ Detener", 
            fg_color=COLORS["red"], # Red
            hover_color=COLORS["red"],
            width=100,
            command=self.stop_camera,
            state="disabled"
        )
        self.btn_stop.pack(side="left", padx=10)
        
        # Status Info (Right aligned)
        self.info_frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        self.info_frame.pack(side="right", padx=20)
        
        self.lbl_fps = ctk.CTkLabel(self.info_frame, text="FPS: --", text_color=COLORS["accent"], font=("Mono", 12))
        self.lbl_fps.pack(side="left", padx=10)
        
        self.lbl_res = ctk.CTkLabel(self.info_frame, text="RES: ----x----", text_color=COLORS["text_secondary"], font=("Mono", 12))
        self.lbl_res.pack(side="left", padx=10)
        
        # State
        self.is_running = False

    def start_camera(self):
        self.is_running = True
        self.no_signal_lbl.configure(text="CONNECTING...", text_color=COLORS["accent"])
        self.btn_start.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        
        # Simulation of connection
        self.after(1000, lambda: self.no_signal_lbl.configure(text="[ LIVE FEED SIMULATION ]\n(OpenCV output would go here)", text_color=COLORS["white"]))
        self.after(1000, lambda: self.lbl_fps.configure(text="FPS: 30"))
        self.after(1000, lambda: self.lbl_res.configure(text="RES: 1920x1080"))

    def stop_camera(self):
        self.is_running = False
        self.no_signal_lbl.configure(text="NO SIGNAL", text_color=COLORS["text_secondary"])
        self.btn_start.configure(state="normal")
        self.btn_stop.configure(state="disabled")
        self.lbl_fps.configure(text="FPS: --")
        self.lbl_res.configure(text="RES: ----x----")
