import streamlit as st

# ---------------------------------------------------------------------------
# Palette de couleurs
# ---------------------------------------------------------------------------
PRIMARY = "#0B6E4F"       # Vert MINSANTE
PRIMARY_DARK = "#084E38"
PRIMARY_LIGHT = "#12A377"
DANGER = "#D62839"
DANGER_DARK = "#A31D2A"
WARNING = "#E8A324"
ORANGE = "#E8590C"
INFO = "#1E5AA8"
NEUTRAL = "#5B6472"
BG = "#F4F7F9"
CARD_BG = "#FFFFFF"
TEXT_DARK = "#1A1A2E"

FONT_FAMILY = "'Poppins', 'Segoe UI', sans-serif"

SCALE_CAS = ["#E9F7EF", "#A9DFBF", "#52BE80", "#1E8449", "#0B6E4F"]
SCALE_DECES = ["#FDEDEC", "#F5B7B1", "#EC7063", "#C0392B", "#7B241C"]
STATUS_COLORS = {"Épidémique": DANGER, "Alerte": WARNING, "Normal": PRIMARY}

# ---------------------------------------------------------------------------
# Icônes vectorielles (SVG, type Feather Icons) — remplacent les emojis
# ---------------------------------------------------------------------------
ICONS = {
    "hospital": '<rect x="3" y="3" width="18" height="18" rx="2"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/>',
    "chart": '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>',
    "alert": '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    "map": '<polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>',
    "x-circle": '<circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/>',
    "check": '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>',
    "trend-up": '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/>',
    "trend-down": '<polyline points="23 18 13.5 8.5 8.5 13.5 1 6"/><polyline points="17 18 23 18 23 12"/>',
    "trend-flat": '<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>',
    "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "list": '<line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/>',
    "search": '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
    "info": '<circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>',
    "bulb": '<path d="M9 18h6"/><path d="M10 22h4"/><path d="M12 2a7 7 0 0 0-4 12.7V17a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-2.3A7 7 0 0 0 12 2z"/>',
    "building": '<rect x="4" y="2" width="16" height="20" rx="1"/><line x1="9" y1="6" x2="9" y2="6.01"/><line x1="15" y1="6" x2="15" y2="6.01"/><line x1="9" y1="10" x2="9" y2="10.01"/><line x1="15" y1="10" x2="15" y2="10.01"/><line x1="9" y1="14" x2="9" y2="14.01"/><line x1="15" y1="14" x2="15" y2="14.01"/><line x1="9" y1="18" x2="15" y2="18"/>',
}


def icon_svg(name: str, size: int = 18, color: str = "currentColor", stroke_width: float = 2) -> str:
    """Retourne le markup SVG brut d'une icône (aucune dépendance à une police emoji)."""
    inner = ICONS.get(name, ICONS["info"])
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" '
        f'fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" '
        f'stroke-linejoin="round" style="vertical-align:-3px;display:inline-block;">{inner}</svg>'
    )


def icon_tag(name: str, size: int = 16, color: str = "currentColor", margin_right: int = 6) -> str:
    """Icône SVG encapsulée, prête à être insérée devant un texte."""
    return (
        f'<span style="display:inline-flex;align-items:center;margin-right:{margin_right}px;">'
        f'{icon_svg(name, size, color)}</span>'
    )


def flag_cameroun_svg(width: int = 26, height: int = 18) -> str:
    """Petit drapeau vectoriel du Cameroun (remplace l'emoji 🇨🇲)."""
    return f'''<svg width="{width}" height="{height}" viewBox="0 0 3 2" xmlns="http://www.w3.org/2000/svg"
        style="vertical-align:-4px;border-radius:2px;box-shadow:0 0 0 1px rgba(0,0,0,0.08);">
        <rect width="1" height="2" x="0" fill="#007A5E"/>
        <rect width="1" height="2" x="1" fill="#CE1126"/>
        <rect width="1" height="2" x="2" fill="#FCD116"/>
        <polygon points="1.5,0.72 1.58,0.95 1.83,0.95 1.63,1.09 1.71,1.32 1.5,1.18 1.29,1.32 1.37,1.09 1.17,0.95 1.42,0.95"
        fill="#FCD116"/>
    </svg>'''


BASE_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {{
    font-family: {FONT_FAMILY};
}}

#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}

.stApp {{
    background: {BG};
}}

.block-container {{
    padding-top: 1.3rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}}

/* ---------- En-tête de page ---------- */
.dlmep-header {{
    background: linear-gradient(120deg, {PRIMARY_DARK} 0%, {PRIMARY} 55%, {PRIMARY_LIGHT} 100%);
    padding: 1.6rem 2rem;
    border-radius: 16px;
    color: white;
    margin-bottom: 1.6rem;
    box-shadow: 0 8px 24px rgba(11,110,79,0.28);
    position: relative;
    overflow: hidden;
}}
.dlmep-header::after {{
    content: "";
    position: absolute;
    top: -40%; right: -8%;
    width: 260px; height: 260px;
    background: rgba(255,255,255,0.08);
    border-radius: 50%;
}}
.dlmep-header .header-row {{
    display: flex;
    align-items: center;
    gap: 0.7rem;
}}
.dlmep-header .header-icon {{
    background: rgba(255,255,255,0.16);
    border-radius: 12px;
    width: 44px; height: 44px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}}
.dlmep-header h1 {{
    margin: 0;
    font-size: 1.55rem;
    font-weight: 800;
    letter-spacing: -0.01em;
}}
.dlmep-header p {{
    margin: 0.45rem 0 0 0;
    opacity: 0.95;
    font-size: 0.95rem;
    font-weight: 400;
}}

/* ---------- Cartes KPI ---------- */
.kpi-card {{
    background: {CARD_BG};
    border-radius: 16px;
    padding: 1.15rem 1.3rem;
    box-shadow: 0 3px 14px rgba(20,20,40,0.07);
    border-top: 5px solid var(--accent, #0B6E4F);
    height: 100%;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}}
.kpi-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 10px 22px rgba(20,20,40,0.12);
}}
.kpi-card .kpi-top {{
    display: flex;
    align-items: center;
    justify-content: space-between;
}}
.kpi-card .kpi-icon-wrap {{
    background: color-mix(in srgb, var(--accent) 12%, white);
    color: var(--accent);
    border-radius: 10px;
    width: 32px; height: 32px;
    display: flex; align-items: center; justify-content: center;
}}
.kpi-card .kpi-label {{
    font-size: 0.76rem;
    color: {NEUTRAL};
    text-transform: uppercase;
    letter-spacing: 0.04em;
    font-weight: 600;
}}
.kpi-card .kpi-value {{
    font-size: 2rem;
    font-weight: 800;
    color: {TEXT_DARK};
    margin: 0.2rem 0 0.1rem 0;
    line-height: 1.1;
}}
.kpi-card .kpi-delta {{
    font-size: 0.80rem;
    font-weight: 600;
}}

/* ---------- Titres de section ---------- */
.section-title {{
    font-size: 1.15rem;
    font-weight: 700;
    color: {TEXT_DARK};
    margin: 1.6rem 0 0.7rem 0;
    padding-left: 0.7rem;
    border-left: 5px solid {PRIMARY};
}}
.section-sub {{
    font-size: 0.85rem;
    color: {NEUTRAL};
    margin: -0.5rem 0 0.8rem 0.7rem;
}}

/* ---------- Cartes de module (page d'accueil) ---------- */
.module-card {{
    background: {CARD_BG};
    border-radius: 16px;
    padding: 1.2rem 1.3rem;
    box-shadow: 0 3px 14px rgba(20,20,40,0.07);
    height: 100%;
    border-bottom: 4px solid var(--accent, #0B6E4F);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}}
.module-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(20,20,40,0.13);
}}
.module-card .module-icon-wrap {{
    background: color-mix(in srgb, var(--accent) 12%, white);
    color: var(--accent);
    border-radius: 12px;
    width: 42px; height: 42px;
    display: flex; align-items: center; justify-content: center;
    margin-bottom: 0.5rem;
}}
.module-card h4 {{
    margin: 0.2rem 0 0.3rem 0;
    font-size: 1.02rem;
    font-weight: 700;
    color: {TEXT_DARK};
}}
.module-card p {{
    margin: 0;
    font-size: 0.85rem;
    color: {NEUTRAL};
    line-height: 1.4;
}}

/* ---------- Tableaux HTML personnalisés ---------- */
.alert-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88rem;
    border-radius: 10px;
    overflow: hidden;
}}
.alert-table th {{
    background: {PRIMARY};
    color: white;
    text-align: left;
    padding: 0.6rem 0.8rem;
    font-weight: 600;
}}
.alert-table td {{
    padding: 0.5rem 0.8rem;
    border-bottom: 1px solid #E5E7EB;
    color: {TEXT_DARK};
}}
.alert-table tr:nth-child(even) {{
    background: #F7FAF9;
}}
.alert-table tr:hover {{
    background: #EEF6F1;
}}

/* ---------- Badges de statut ---------- */
.badge {{
    display: inline-block;
    padding: 0.22rem 0.7rem;
    border-radius: 999px;
    font-size: 0.76rem;
    font-weight: 700;
    color: white;
    letter-spacing: 0.01em;
}}

/* ---------- Boîtes d'information ---------- */
.info-box {{
    background: #EAF3FF;
    border-left: 5px solid {INFO};
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    font-size: 0.88rem;
    color: {TEXT_DARK};
    display: flex;
    gap: 0.6rem;
    align-items: flex-start;
}}

/* ---------- Légende à puce colorée ---------- */
.color-legend-item {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.85rem;
    color: {TEXT_DARK};
}}
.color-dot {{
    width: 12px; height: 12px;
    border-radius: 4px;
    flex-shrink: 0;
}}

/* ---------- Barre latérale ---------- */
.sidebar-brand {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 700;
    font-size: 1.0rem;
    color: {TEXT_DARK};
    margin-bottom: 0.2rem;
}}
</style>
"""


def inject_base_css():
    st.markdown(BASE_CSS, unsafe_allow_html=True)


def page_header(title: str, subtitle: str = "", icon: str = "hospital"):
    st.markdown(
        f"""
        <div class="dlmep-header">
            <div class="header-row">
                <div class="header-icon">{icon_svg(icon, size=24, color="white")}</div>
                <h1>{title}</h1>
            </div>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value, delta: str = "", accent: str = PRIMARY, delta_color: str = NEUTRAL, icon: str = "info"):
    st.markdown(
        f"""
        <div class="kpi-card" style="--accent:{accent};">
            <div class="kpi-top">
                <div class="kpi-label">{label}</div>
                <div class="kpi-icon-wrap">{icon_svg(icon, size=16, color=accent)}</div>
            </div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-delta" style="color:{delta_color};">{delta}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def module_card(icon: str, title: str, description: str, accent: str = PRIMARY):
    st.markdown(
        f"""
        <div class="module-card" style="--accent:{accent};">
            <div class="module-icon-wrap">{icon_svg(icon, size=20, color=accent)}</div>
            <h4>{title}</h4>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_badge(status: str) -> str:
    color = STATUS_COLORS.get(status, NEUTRAL)
    return f'<span class="badge" style="background:{color};">{status}</span>'


def section_title(text: str, subtitle: str = ""):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="section-sub">{subtitle}</div>', unsafe_allow_html=True)


def info_box(text: str, icon: str = "bulb"):
    st.markdown(
        f'<div class="info-box">{icon_svg(icon, size=18, color="#1E5AA8")}<div>{text}</div></div>',
        unsafe_allow_html=True,
    )


def color_legend(items):
    """items : liste de tuples (couleur, libellé). Affiche une légende à puces colorées (sans emoji)."""
    html = '<div style="display:flex;gap:1.5rem;flex-wrap:wrap;margin:0.4rem 0 0.8rem 0;">'
    for color, label in items:
        html += f'<div class="color-legend-item"><div class="color-dot" style="background:{color};"></div>{label}</div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def fr_number(n) -> str:
    """Formate un nombre à la française : séparateur milliers = espace."""
    try:
        return f"{int(n):,}".replace(",", "\u202f")
    except (ValueError, TypeError):
        return str(n)


def apply_chart_theme(fig, height: int = 420, legend_title: str = None):
    """Applique un thème visuel cohérent à une figure Plotly."""
    fig.update_layout(
        height=height,
        font=dict(family=FONT_FAMILY, size=13, color=TEXT_DARK),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    title_text=legend_title if legend_title else ""),
        hoverlabel=dict(bgcolor="white", font_size=12, font_family=FONT_FAMILY),
    )
    fig.update_xaxes(showgrid=True, gridcolor="#EDF1F3", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#EDF1F3", zeroline=False)
    return fig
