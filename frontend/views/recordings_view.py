
import customtkinter as ctk
from ..desktop_styles import COLORS

class RecordingsView(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        # Grid Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        
        for i in range(12):
            self.create_video_card(i)
            
    def create_video_card(self, index):
        # Card Container
        card = ctk.CTkFrame(self, fg_color="black", corner_radius=12, border_color=COLORS["text_secondary"], border_width=1)
        row = index // 3
        col = index % 3
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        card.configure(width=300, height=180) # Approx aspect ratio
        
        # "REC" Indicator
        rec_badge = ctk.CTkLabel(
            card, text="● REC", 
            fg_color=COLORS["indigo"], text_color="white",
            corner_radius=4, font=("Inter", 10, "bold"),
            width=50, height=20
        )
        rec_badge.place(x=10, y=10)
        
        # Placeholder Image Text (since we don't assume internet for fetching unsplash in backend-less run easily without blocking, or just solid color)
        # Using a Frame to simulate video content
        video_content = ctk.CTkFrame(card, fg_color="#1a1a2e", corner_radius=0)
        video_content.place(x=0, y=0, relwidth=1, relheight=1)
        video_content.lower() # send to back
        
        lbl_cam = ctk.CTkLabel(card, text=f"CAM-0{index+1}", text_color=COLORS["text_secondary"], font=("JetBrains Mono", 12))
        lbl_cam.place(x=10, rely=0.85)

class FilesView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        # Grid for Folders
        self.grid_columnconfigure((0,1,2,3), weight=1)
        
        folders = ["Rec_2024", "Incidentes", "Logs", "Sistema", "Backup", "Temp", "Export", "Trash"]
        
        for i, name in enumerate(folders):
            self.create_folder_card(name, i)
            
    def create_folder_card(self, name, index):
        card = ctk.CTkButton(
            self, 
            text=f"\n📁\n\n{name}\n{12 + index*5} items",
            font=("Inter", 14),
            fg_color=COLORS["card_bg"],
            hover_color=COLORS["indigo"], 
            corner_radius=12,
            border_width=1,
            border_color=COLORS["sidebar_bg"],
            width=150, height=150
        )
        row = index // 4
        col = index % 4
        card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
