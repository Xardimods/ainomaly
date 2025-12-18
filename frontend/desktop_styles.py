
# Brand Colors & Dynamic Theme Support

# Helper for (Light, Dark) tuples
def dynamic(light, dark):
    return (light, dark)

# Raw Palette
PALETTE = {
    "indigo": "#1800ad",
    "indigo_dark": "#0f006b",
    "yellow": "#ffde59",
    "yellow_dark": "#e6c200",
    "white": "#ffffff",
    "black": "#000000",
    
    # Dark Mode Base
    "dark_bg": "#020205",
    "dark_sidebar": "#0a0520",
    "dark_card": "#141423",
    "dark_text": "#f0f0f5",
    "dark_text_sec": "#a0a0b0",
    
    # Light Mode Base
    "light_bg": "#f1f5f9",
    "light_sidebar": "#ffffff",
    "light_card": "#ffffff", 
    "light_text": "#0f172a",
    "light_text_sec": "#64748b"
}

# Semantic Dynamic Colors (Light, Dark)
COLORS = {
    # Main Layout
    "window_bg": dynamic(PALETTE["light_bg"], PALETTE["dark_bg"]),
    "sidebar_bg": dynamic(PALETTE["light_sidebar"], PALETTE["dark_sidebar"]),
    "content_bg": dynamic(PALETTE["light_bg"], PALETTE["dark_bg"]),
    
    # Cards & Content
    "card_bg": dynamic(PALETTE["light_card"], PALETTE["dark_card"]),
    "card_border": dynamic("#e2e8f0", PALETTE["dark_sidebar"]),
    
    # Text
    "text_primary": dynamic(PALETTE["light_text"], PALETTE["dark_text"]),
    "text_secondary": dynamic(PALETTE["light_text_sec"], PALETTE["dark_text_sec"]),
    "text_inverse": dynamic(PALETTE["white"], PALETTE["light_text"]), # Text on dark buttons
    
    # Accents
    "primary": dynamic(PALETTE["indigo"], PALETTE["indigo"]),
    "primary_hover": dynamic(PALETTE["indigo_dark"], PALETTE["indigo_dark"]),
    "accent": dynamic("#d97706", PALETTE["yellow"]), # Darker yellow for light mode? Or just same.
    "accent_text": dynamic("#b45309", PALETTE["yellow"]),
    
    # Specifics
    "red": dynamic("#ef4444", "#ef4444"),
    "green": dynamic("#22c55e", "#22c55e"),
    
    # Keep strictly raw generic refs if needed (though discouraged)
    "indigo": PALETTE["indigo"],
    "yellow": PALETTE["yellow"],
    "white": PALETTE["white"]
}
