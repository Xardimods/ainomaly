
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ..desktop_styles import COLORS, PALETTE
from ..ui_components import InfoCard

class DashboardView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        # --- Metrics Row ---
        self.metrics_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.metrics_frame.pack(fill="x", padx=30, pady=(10, 30))
        
        c1 = InfoCard(self.metrics_frame, "Alertas Hoy", "0", "Sin incidentes")
        c1.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        c2 = InfoCard(self.metrics_frame, "Tiempo Activo", "4h 12m", "Monitoreo continuo")
        c2.pack(side="left", fill="both", expand=True, padx=10)
        
        c3 = InfoCard(self.metrics_frame, "Cámaras", "1 / 4", "3 desconectadas")
        c3.pack(side="left", fill="both", expand=True, padx=(10, 0))

        # --- Charts Area ---
        # We use a Grid layout for the charts: Line Chart (Left), Pie + Log (Right)
        self.charts_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.charts_frame.pack(fill="both", expand=True, padx=30, pady=10)
        self.charts_frame.grid_columnconfigure(0, weight=2)
        self.charts_frame.grid_columnconfigure(1, weight=1)
        
        # 1. Line Chart (Matplotlib)
        self.line_chart_frame = ctk.CTkFrame(self.charts_frame, fg_color=COLORS["card_bg"], corner_radius=12)
        self.line_chart_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        self.create_line_chart(self.line_chart_frame)

        # 2. Right Column (Pie Chart)
        self.right_col = ctk.CTkFrame(self.charts_frame, fg_color="transparent")
        self.right_col.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        self.pie_chart_frame = ctk.CTkFrame(self.right_col, fg_color=COLORS["card_bg"], corner_radius=12)
        self.pie_chart_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        self.create_pie_chart(self.pie_chart_frame)
        
        # 3. Mini Logs (Bottom Right - placeholder for now)
        self.logs_frame = ctk.CTkFrame(self.right_col, fg_color=COLORS["card_bg"], corner_radius=12, height=150)
        self.logs_frame.pack(fill="x")
        
        ctk.CTkLabel(self.logs_frame, text="Bitácora Reciente (Logs)", font=("Inter", 12, "bold"), text_color=COLORS["text_secondary"]).pack(pady=10)
        # Simple list
        log_data = [("14:02", "Movimiento Detectado", "INFO"), ("11:30", "Persona (Admin)", "INFO")]
        for time, event, lvl in log_data:
            row = ctk.CTkFrame(self.logs_frame, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=2)
            ctk.CTkLabel(row, text=time, width=50, anchor="w", text_color=COLORS["text_secondary"]).pack(side="left")
            ctk.CTkLabel(row, text=event, anchor="w", text_color=COLORS["text_primary"]).pack(side="left", fill="x", expand=True)
            ctk.CTkLabel(row, text=lvl, width=60, text_color=COLORS["primary"]).pack(side="right")


    def create_line_chart(self, parent):
        # Create Figure
        fig = plt.Figure(figsize=(5, 3), dpi=100)
        fig.patch.set_facecolor(PALETTE["dark_card"]) # Match Card BG
        
        ax = fig.add_subplot(111)
        ax.set_facecolor(PALETTE["dark_card"])
        
        # Data
        x = range(10)
        y = [2, 3, 5, 4, 6, 8, 5, 7, 8, 9]
        
        # Plot
        ax.plot(x, y, color=PALETTE["yellow"], linewidth=2, marker='o', markersize=5)
        
        # Styling
        ax.spines['bottom'].set_color(PALETTE["dark_text_sec"])
        ax.spines['left'].set_color(PALETTE["dark_text_sec"])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(axis='x', colors=PALETTE["dark_text_sec"])
        ax.tick_params(axis='y', colors=PALETTE["dark_text_sec"])
        ax.set_title("Actividad Mensual", color=PALETTE["white"], loc='left', fontsize=10)
        ax.grid(color=PALETTE["dark_text_sec"], linestyle=':', linewidth=0.5, alpha=0.3)

        # Embed
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def create_pie_chart(self, parent):
        fig = plt.Figure(figsize=(3, 3), dpi=100)
        fig.patch.set_facecolor(PALETTE["dark_card"])
        
        ax = fig.add_subplot(111)
        ax.set_facecolor(PALETTE["dark_card"])
        
        labels = ['Normal', 'Alertas']
        sizes = [85, 15]
        colors = [PALETTE["indigo"], PALETTE["yellow"]]
        
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, textprops=dict(color=PALETTE["dark_text_sec"]))
        
        # Hollow center (Donut)
        centre_circle = plt.Circle((0,0),0.70,fc=PALETTE["dark_card"])
        fig.gca().add_artist(centre_circle)
        
        ax.set_title("Distribución", color=PALETTE["white"], fontsize=10)

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
