import streamlit as st
import pandas as pd

from app_utils.styling import (
    page_header, kpi_card, module_card, section_title, info_box,
    fr_number, PRIMARY, DANGER, WARNING, INFO,
)
from app_utils.data_generator import get_weekly_surveillance_data, get_current_district_status

page_header(
    "Tableau de Bord de Surveillance Épidémiologique",
    "Système d'Information pour la Surveillance Intégrée de la Maladie et la Riposte (SIMR/SFE) — Cameroun",
    icon="hospital",
)

df = get_weekly_surveillance_data()
status_df = get_current_district_status()
last_week = df["semaine"].max()
last = df[df["semaine"] == last_week]
prev = df[df["semaine"] == last_week - 1]

total_cas = int(last["cas"].sum())
total_cas_prev = int(prev["cas"].sum()) if not prev.empty else 0
delta_cas = total_cas - total_cas_prev
total_deces = int(last["deces"].sum())
nb_epidemie = int((status_df["statut_pire"] == "Épidémique").sum())
nb_alerte = int((status_df["statut_pire"] == "Alerte").sum())
nb_districts = status_df["district_id"].nunique()

section_title("Aperçu global", f"Situation de la semaine épidémiologique en cours — {pd.Timestamp.today().strftime('%d %B %Y')}")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    kpi_card("Cas notifiés", fr_number(total_cas),
             f"{'En hausse de ' if delta_cas >= 0 else 'En baisse de '}{fr_number(abs(delta_cas))} par rapport à S-1",
             accent=INFO, icon="file")
with col2:
    kpi_card("Décès enregistrés", fr_number(total_deces), "Semaine en cours", accent=DANGER, icon="x-circle")
with col3:
    kpi_card("Districts en épidémie", fr_number(nb_epidemie), "Seuil épidémique franchi",
             accent=DANGER, delta_color=DANGER, icon="alert")
with col4:
    kpi_card("Districts en alerte", fr_number(nb_alerte), "Seuil d'alerte franchi",
             accent=WARNING, delta_color=WARNING, icon="shield")
with col5:
    kpi_card("Districts suivis", fr_number(nb_districts), "sur 213 districts (référentiel national)",
             accent=PRIMARY, icon="map")

st.markdown("<br>", unsafe_allow_html=True)
section_title("Modules du tableau de bord", "Accédez à chaque module via le menu de navigation à gauche")

m1, m2, m3, m4 = st.columns(4)
with m1:
    module_card("chart", "Situation Épidémiologique",
                "Courbes épidémiques, cartes des cas et décès, répartition par région et par district.",
                accent=INFO)
with m2:
    module_card("alert", "Alertes de Seuil",
                "Détection automatique des districts ayant dépassé les seuils d'alerte ou épidémique.",
                accent=WARNING)
with m3:
    module_card("shield", "Évaluation des Risques",
                "Matrice de risque interactive : probabilité de survenue × gravité de l'événement.",
                accent=DANGER)
with m4:
    module_card("map", "Districts à Risque",
                "Carte nationale : districts en épidémie (rouge) et districts à risque (bulles).",
                accent=PRIMARY)

st.markdown("<br>", unsafe_allow_html=True)
info_box(
    "Les données affichées dans ce tableau de bord sont <b>simulées</b> à des fins de démonstration visuelle. "
    "Remplacez le fichier <code>utils/data_generator.py</code> par vos connecteurs DHIS2 / SIMR réels "
    "(en conservant les mêmes noms de colonnes) pour un usage opérationnel."
)
