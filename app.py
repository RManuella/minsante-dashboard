import streamlit as st
from app_utils.styling import inject_base_css, flag_cameroun_svg

st.set_page_config(
    page_title="MINSANTE - DLMEP | Surveillance Épidémiologique",
    page_icon=":material/local_hospital:",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_base_css()

with st.sidebar:
    st.markdown(
        f'<div class="sidebar-brand">{flag_cameroun_svg()} MINSANTE — DLMEP</div>',
        unsafe_allow_html=True,
    )
    st.caption("Direction de la Lutte contre la Maladie, les Épidémies et les Pandémies")
    st.markdown("---")

# ---------------------------------------------------------------------------
# Déclaration des pages (icônes Material natives Streamlit — pas d'emoji)
# ---------------------------------------------------------------------------
accueil = st.Page("pages/accueil.py", title="Accueil", icon=":material/home:", default=True)
situation = st.Page("pages/situation_epidemiologique.py", title="Situation Épidémiologique",
                     icon=":material/monitoring:")
alertes = st.Page("pages/alertes_de_seuil.py", title="Alertes de Seuil",
                   icon=":material/warning:")
risques = st.Page("pages/evaluation_des_risques.py", title="Évaluation des Risques",
                   icon=":material/shield_with_heart:")
districts = st.Page("pages/districts_a_risque.py", title="Districts à Risque",
                     icon=":material/map:")

pg = st.navigation([accueil, situation, alertes, risques, districts])

with st.sidebar:
    st.markdown("---")
    st.caption("Données de démonstration — à connecter à DHIS2 / SIMR pour un usage opérationnel.")

pg.run()
