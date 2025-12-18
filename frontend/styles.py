
def get_css(theme="dark"):
    
    # PALETTES
    if theme == "dark":
        vars = """
        --bg-main: #020205;
        --bg-sidebar: #0a0520;
        --bg-card: rgba(20, 20, 35, 0.7);
        --folder-bg: rgba(255, 255, 255, 0.03);
        
        --text-primary: #f0f0f5;  
        --text-secondary: #a0a0b0; 
        
        --border-color: rgba(255, 255, 255, 0.08);
        --input-bg: rgba(255, 255, 255, 0.05);
        --bg-gradient: radial-gradient(circle at 15% 25%, rgba(24, 0, 173, 0.1) 0%, transparent 50%);
        """
    else: # Light Mode - Fixed
        vars = """
        --bg-main: #ffffff;
        --bg-sidebar: #e2e8f0;     
        --bg-card: #ffffff;
        --folder-bg: #f8fafc;
        
        --text-primary: #0f172a;   
        --text-secondary: #334155; 
        
        --border-color: #cbd5e1;
        --input-bg: #f1f5f9;       
        --bg-gradient: linear-gradient(135deg, #f8fafc 0%, #edf2f7 100%);
        """

    return f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');

    :root {{
        /* BRAND */
        --brand-indigo: #1800ad;
        --brand-indigo-dark: #0f006b;
        --brand-yellow: #ffde59; 
        --brand-yellow-text: #e6c200; 
        
        {vars}
    }}

    /* Base Styling */
    .stApp {{
        background-color: var(--bg-main);
        background-image: var(--bg-gradient);
        color: var(--text-primary);
        font-family: 'Inter', sans-serif;
    }}
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {{
        color: { "var(--brand-indigo)" if theme == "light" else "var(--brand-yellow)" } !important;
        font-weight: 700;
        letter-spacing: -0.01em;
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: var(--bg-sidebar);
        border-right: 1px solid var(--border-color);
    }}
    section[data-testid="stSidebar"] * {{
        color: { "#1e293b" if theme == "light" else "var(--text-primary)" };
    }}

    /* Navigation Radio - CORRECT TARGETING */
    /* Target the option label container specifically */
    label[data-baseweb="radio"] {{
        background: transparent;
        padding: 10px 15px;
        border-radius: 8px;
        margin-bottom: 4px;
        border: 1px solid transparent;
        transition: all 0.2s;
        color: var(--text-secondary) !important;
        cursor: pointer;
        display: flex !important; /* Ensure flex layout */
        align-items: center;
        width: 100%;
    }}
    
    /* Hide the default circle (First DIV child of the label) */
    label[data-baseweb="radio"] > div:first-child {{
        display: none !important;
    }}
    
    /* Ensure the Text Container is Visible */
    label[data-baseweb="radio"] > div:last-child {{
        display: block !important;
        margin-left: 0px !important;
    }}
    
    /* Checked State */
    label[data-baseweb="radio"] input:checked + div + div, 
    div[role="radiogroup"] label[aria-checked="true"] {{
        /* Note: Streamlit structure varies. aria-checked is reliable on the label in some versions, 
           or checking the input inside. We use a broad style for the label itself if possible. 
           But stRadio labels don't always have aria-checked on the LABEL element in older versions. 
           In recent versions (1.30+), label[data-baseweb="radio"] has children.
           We'll assume strict styling via JS checked emulation if CSS fails, but standard active state: */
    }}
    
    /* We trust Streamlit adds data-checked or we target the active one if we can identify it. 
       Usually Streamlit adds a class or attribute. 
       Let's stick to the reliable `div[role="radiogroup"] label[data-checked="true"]` if available, 
       otherwise we rely on the input checked sibling trick if structure permits.
      
       Actually, Streamlit injects `aria-checked="true"` on the label or a wrapper div.
    */
    div[role="radiogroup"] label :checked ~ div:last-child {{ 
        /* This targets the text div when input is checked (if input is inside label) */
        color: #ffffff !important;
        font-weight: 700;
    }}
    
    /* Since we can't easily style the PARENT label based on child input with pure CSS (before :has),
       we rely on Streamlit's internal classes. 
       Workaround: The previous solution `div[role="radiogroup"] > label[aria-checked="true"]` was likely working for the BOX.
       Let's restore that selector specific for the active box. */
       
    div[role="radiogroup"] label[data-checked="true"] {{
        background: var(--brand-indigo) !important;
        color: #ffffff !important;
        border-left: 5px solid var(--brand-yellow);
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(24,0,173,0.3);
    }}
    /* FORCE WHITE TEXT ON CHILDREN OF ACTIVE ELEMENT */
    div[role="radiogroup"] label[data-checked="true"] * {{
        color: #ffffff !important;
    }}
    
    /* Fallback for browsers without :has support (unlikely today but safe) -> 
       We color the TEXT inside. */
       
    label[data-baseweb="radio"]:hover {{
        background: { "rgba(24,0,173,0.1)" if theme=="light" else "rgba(255,255,255,0.05)" };
        color: var(--brand-indigo) !important;
    }}

    /* INPUTS & WIDGETS FORCE STYLING */
    input[type="text"], input[type="password"], input[type="number"], .stSelectbox [data-baseweb="select"] > div {{
        background-color: var(--input-bg) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 6px;
    }}
    li[role="option"] {{
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
    }}
    
    /* SLIDERS - REFINED */
    div[data-baseweb="slider"] div[role="slider"] {{
        background-color: var(--brand-yellow) !important;
        border: 2px solid var(--brand-indigo) !important;
        box-shadow: 0 0 10px rgba(0,0,0,0.2);
    }}
    /* We cannot safely target the track without affecting the container in generic Streamlit versions via CSS only. 
       We will accept the default track color but ensure the labels are readable. */
    
    /* ALERT BOXES (st.info) */
    div[data-baseweb="notification"] {{
        background-color: var(--bg-card) !important;
        border: 1px solid var(--brand-indigo) !important;
        color: var(--text-primary) !important;
    }}
    div[data-baseweb="notification"] svg {{
        color: var(--brand-yellow) !important;
    }}

    /* Cards */
    .custom-card {{
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: { "0 4px 12px rgba(0,0,0,0.05)" if theme == "light" else "0 4px 20px rgba(0,0,0,0.2)" };
    }}
    
    .card-title {{
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: { "var(--brand-indigo)" if theme == "light" else "var(--brand-yellow)" };
        font-weight: 700;
        margin-bottom: 8px;
    }}
    .card-value {{
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
    }}

    /* Folders */
    .folder-container {{
        background: var(--folder-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 20px;
        display: flex; flex-direction: column; align-items: center;
        transition: 0.2s;
        cursor: pointer;
    }}
    .folder-container:hover {{
        border-color: var(--brand-indigo);
        background: { "rgba(24,0,173,0.05)" if theme == "light" else "rgba(24,0,173,0.2)" };
        transform: translateY(-2px);
    }}
    .folder-icon {{
        font-size: 3rem; margin-bottom: 10px;
        color: { "var(--brand-indigo)" if theme == "light" else "var(--brand-yellow)" };
    }}

    /* Video Card */
    .video-card {{
        border-radius: 12px; overflow: hidden;
        border: 1px solid var(--border-color);
        background: #000; position: relative;
    }}
    .rec-indicator {{
        position: absolute; top: 10px; left: 10px;
        background: var(--brand-indigo);
        border: 1px solid var(--brand-yellow);
        color: white; padding: 4px 8px; font-weight: 700; border-radius: 4px; font-size: 0.7rem;
    }}

    /* Buttons */
    div.stButton > button {{
        background-color: var(--brand-indigo);
        color: #fff;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        transition: 0.2s;
    }}
    div.stButton > button:hover {{
        background-color: var(--brand-indigo-dark);
        color: var(--brand-yellow);
        box-shadow: 0 4px 12px rgba(24, 0, 173, 0.3);
    }}

    /* HTML Tables */
    .styled-table {{
        width: 100%;
        border-collapse: collapse;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
    }}
    .styled-table th {{
        text-align: left;
        padding: 12px;
        color: var(--text-secondary);
        font-size: 0.8rem;
        text-transform: uppercase;
        border-bottom: 1px solid var(--border-color);
    }}
    .styled-table td {{
        padding: 12px;
        border-bottom: 1px solid var(--border-color);
        color: var(--text-primary);
    }}
    .styled-table tr:last-child td {{ border-bottom: none; }}
    
    .status-badge {{
        padding: 4px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 600;
    }}
    .bg-info {{ background: rgba(59, 130, 246, 0.2); color: #3b82f6; }}
    .bg-success {{ background: rgba(16, 185, 129, 0.2); color: #10b981; }}
    
</style>
"""
