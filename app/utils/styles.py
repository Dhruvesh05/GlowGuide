"""Master CSS design system for GlowGuide Professional Edition."""

MASTER_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --primary: #6366F1;
    --primary-dark: #4F46E5;
    --secondary: #8B5CF6;
    --accent: #EC4899;
    --bg-light: #FFFFFF;
    --bg-dark: #0F172A;
    --bg-gray: #F8FAFC;
    --bg-gray-2: #F1F5F9;
    --border-light: #E2E8F0;
    --text-primary: #0F172A;
    --text-secondary: #64748B;
    --text-tertiary: #94A3B8;
}

/* Dark mode variables */
[data-theme="dark"] {
    --primary: #818CF8;
    --primary-dark: #6366F1;
    --secondary: #A78BFA;
    --accent: #F472B6;
    --bg-light: #1E293B;
    --bg-dark: #0F172A;
    --bg-gray: #1A1F35;
    --bg-gray-2: #15202B;
    --border-light: #334155;
    --text-primary: #F1F5F9;
    --text-secondary: #CBD5E1;
    --text-tertiary: #94A3B8;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg-light);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    color: var(--text-primary);
    transition: background-color 0.3s ease, color 0.3s ease;
}

[data-testid="stHeader"] { display: none; }
[data-testid="stDecoration"] { display: none; }

/* ========== NAVBAR (Cloud Style Rectangle) ========== */
.navbar-container {
    position: sticky;
    top: 0;
    z-index: 1000;
    width: 100%;
    padding: 20px 40px;
    background: rgba(255, 255, 255, 0.98);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(226, 232, 240, 0.4);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
}

[data-theme="dark"] .navbar-container {
    background: rgba(15, 23, 42, 0.98);
    border-bottom-color: rgba(51, 65, 85, 0.4);
}

.navbar-content {
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.navbar-brand {
    font-family: 'Poppins', sans-serif;
    font-size: 26px;
    font-weight: 800;
    background: linear-gradient(135deg, #6366F1, #8B5CF6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.8px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.navbar-brand:hover {
    letter-spacing: -0.5px;
}

.navbar-nav {
    display: flex;
    gap: 48px;
    align-items: center;
    margin-left: 100px;
}

.nav-item {
    color: var(--text-secondary);
    font-weight: 500;
    cursor: pointer;
    padding: 10px 0;
    border-bottom: 3px solid transparent;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    font-size: 15px;
    position: relative;
}

.nav-item::after {
    content: '';
    position: absolute;
    bottom: -3px;
    left: 0;
    width: 0;
    height: 3px;
    background: linear-gradient(135deg, #6366F1, #8B5CF6);
    transition: width 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.nav-item:hover::after {
    width: 100%;
}

.nav-item:hover {
    color: var(--primary);
}

.nav-item.active {
    color: var(--primary);
    border-bottom-color: var(--primary);
}

.nav-controls {
    display: flex;
    gap: 16px;
    align-items: center;
}

.theme-toggle {
    width: 50px;
    height: 50px;
    border-radius: 14px;
    border: 1px solid var(--border-light);
    background: var(--bg-gray);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    color: var(--text-primary);
}

.theme-toggle:hover {
    background: var(--primary);
    color: white;
    border-color: var(--primary);
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(99, 102, 241, 0.3);
}

.theme-toggle:active {
    transform: translateY(-1px);
}

/* ========== MAIN HERO SECTION ========== */
.hero-section {
    text-align: center;
    padding: 100px 32px 80px;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(139, 92, 246, 0.08) 50%, rgba(236, 72, 153, 0.04) 100%);
    border-radius: 32px;
    margin: 40px auto;
    max-width: 1200px;
    position: relative;
    overflow: hidden;
}

.hero-section::before {
    content: '';
    position: absolute;
    top: -40%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(99, 102, 241, 0.1) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}

.hero-section::after {
    content: '';
    position: absolute;
    bottom: -20%;
    left: -5%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(139, 92, 246, 0.08) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}

[data-theme="dark"] .hero-section {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.15) 50%, rgba(236, 72, 153, 0.08) 100%);
}

.hero-content {
    position: relative;
    z-index: 1;
}

.hero-title {
    font-family: 'Poppins', sans-serif;
    font-size: 120px;
    font-weight: 800;
    background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #EC4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -3px;
    margin-bottom: 20px;
    line-height: 1;
    animation: fadeInDown 0.8s ease-out;
}

.hero-subtitle {
    font-size: 20px;
    color: var(--text-secondary);
    margin-bottom: 48px;
    font-weight: 400;
    letter-spacing: 0.5px;
    animation: fadeInUp 0.8s ease-out 0.2s backwards;
}

.hero-cta {
    display: flex;
    gap: 16px;
    justify-content: center;
    animation: fadeInUp 0.8s ease-out 0.4s backwards;
}

/* ========== ANIMATIONS ========== */
@keyframes fadeInDown {
    from {
        opacity: 0;
        transform: translateY(-30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

/* ========== SIDEBAR ========== */
[data-testid="stSidebar"] {
    background: var(--bg-light);
    border-right: 1px solid var(--border-light);
}

[data-testid="stSidebarNav"] button {
    border: none;
    padding: 14px 18px;
    border-radius: 12px;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    color: var(--text-secondary);
    font-weight: 500;
    font-size: 15px;
}

[data-testid="stSidebarNav"] button:hover {
    background: var(--bg-gray);
    color: var(--primary);
    transform: translateX(4px);
}

[data-testid="stSidebarNav"] button[aria-selected="true"] {
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    color: white;
    font-weight: 600;
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.3);
}

/* ========== BUTTONS ========== */
.stButton > button {
    background: linear-gradient(135deg, #6366F1, #7C3AED);
    color: white !important;
    border: none;
    border-radius: 12px;
    padding: 14px 32px;
    font-weight: 600;
    font-size: 15px;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.25);
    text-transform: uppercase;
    letter-spacing: 0.6px;
    font-family: 'Inter', sans-serif;
    position: relative;
    overflow: hidden;
}

.stButton > button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: rgba(255, 255, 255, 0.2);
    transition: left 0.3s ease;
}

.stButton > button:hover::before {
    left: 100%;
}

.stButton > button:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(99, 102, 241, 0.4);
}

.stButton > button:active {
    transform: translateY(-2px);
}

/* ========== TABS ========== */
.stTabs [data-baseweb="tab-list"] {
    border-bottom: 2px solid var(--border-light);
    background: transparent;
    border-radius: 0;
    padding: 0;
}

.stTabs [data-baseweb="tab"] {
    padding: 16px 24px;
    color: var(--text-secondary);
    font-weight: 500;
    border-radius: 0;
    border: none;
    transition: all 0.3s ease;
    margin-right: 0;
    position: relative;
    font-size: 15px;
}

.stTabs [data-baseweb="tab"]::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 0;
    height: 2px;
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    transition: width 0.3s ease;
}

.stTabs [aria-selected="true"]::after {
    width: 100%;
}

.stTabs [aria-selected="true"] {
    color: var(--primary) !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: var(--primary);
}

/* ========== METRICS ========== */
.stMetric {
    background: var(--bg-gray);
    padding: 28px;
    border-radius: 18px;
    border: 1px solid var(--border-light);
    border-left: 5px solid var(--primary);
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    position: relative;
    overflow: hidden;
}

.stMetric::before {
    content: '';
    position: absolute;
    top: 0;
    right: -50%;
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, rgba(99, 102, 241, 0.1) 0%, transparent 70%);
    border-radius: 50%;
}

.stMetric:hover {
    border-left-color: var(--secondary);
    box-shadow: 0 16px 40px rgba(99, 102, 241, 0.18);
    transform: translateY(-6px);
    border-color: var(--primary);
}

/* ========== TEXT ========== */
h1 {
    font-family: 'Poppins', sans-serif;
    font-size: 48px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -2px;
    margin-bottom: 12px;
}

h2 {
    font-family: 'Poppins', sans-serif;
    font-size: 36px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 14px;
}

h3 {
    font-family: 'Poppins', sans-serif;
    font-size: 22px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 12px;
}

/* ========== CARDS ========== */
.stContainer {
    background: var(--bg-light);
    border-radius: 18px;
    border: 1px solid var(--border-light);
    padding: 32px;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.stContainer:hover {
    border-color: var(--primary);
    box-shadow: 0 12px 40px rgba(99, 102, 241, 0.15);
    transform: translateY(-6px);
}

/* ========== DATAFRAME ========== */
.stDataFrame {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid var(--border-light);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.stDataFrame table {
    font-size: 14px;
}

/* ========== INPUTS ========== */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] select {
    border-radius: 12px;
    border: 1px solid var(--border-light);
    font-size: 15px;
    padding: 12px 16px;
    transition: all 0.3s ease;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus,
[data-testid="stSelectbox"] select:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
}

/* ========== RESPONSIVE ========== */
@media (max-width: 768px) {
    .navbar-nav {
        gap: 24px;
        margin-left: 0;
    }
    
    .hero-title {
        font-size: 64px;
    }
    
    h1 {
        font-size: 36px;
    }
    
    h2 {
        font-size: 28px;
    }
}
"""

# HTML Component Snippets
CARD_OPEN = '<div style="background: var(--bg-light); border: 1px solid var(--border-light); border-radius: 18px; padding: 28px; margin-bottom: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); transition: all 0.3s ease;" onmouseover="this.style.boxShadow=\'0 12px 40px rgba(99, 102, 241, 0.15)\'; this.style.borderColor=\'#6366F1\'; this.style.transform=\'translateY(-6px)\';" onmouseout="this.style.boxShadow=\'0 4px 12px rgba(0,0,0,0.05)\'; this.style.borderColor=\'#E2E8F0\'; this.style.transform=\'translateY(0)\';">'
CARD_CLOSE = '</div>'

SECTION_HEADER = '<div style="margin-top: 40px; margin-bottom: 28px; padding-bottom: 16px; border-bottom: 2px solid var(--border-light);"><h2 style="margin: 0; font-size: 32px; font-weight: 700; color: var(--text-primary); letter-spacing: -0.5px;">%s</h2></div>'

BADGE_SAFE = '<span style="display: inline-block; background: #D1FAE5; color: #065F46; padding: 8px 16px; border-radius: 24px; font-size: 13px; font-weight: 600; letter-spacing: 0.3px; border: 1px solid #6EE7B7;">✓ Safe</span>'
BADGE_CAUTION = '<span style="display: inline-block; background: #FEF3C7; color: #92400E; padding: 8px 16px; border-radius: 24px; font-size: 13px; font-weight: 600; letter-spacing: 0.3px; border: 1px solid #FCD34D;">⚠ Caution</span>'
BADGE_RISK = '<span style="display: inline-block; background: #FEE2E2; color: #7F1D1D; padding: 8px 16px; border-radius: 24px; font-size: 13px; font-weight: 600; letter-spacing: 0.3px; border: 1px solid #FECACA;">✕ High Risk</span>'
