import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from app_utils.styling import (
    page_header, kpi_card, section_title, fr_number, apply_chart_theme, color_legend,
    PRIMARY, DANGER, WARNING, ORANGE, INFO,
)
from app_utils.data_generator import DISEASES, get_districts

page_header("Évaluation des Risques", "Matrice de risque — Probabilité de survenue × Gravité de l'événement", icon="shield")

PROB_LEVELS = {1: "Rare", 2: "Peu probable", 3: "Possible", 4: "Probable", 5: "Quasi certain"}
GRAV_LEVELS = {1: "Mineure", 2: "Modérée", 3: "Sérieuse", 4: "Majeure", 5: "Catastrophique"}


def risk_class(score: int):
    if score <= 4:
        return "Faible", PRIMARY
    elif score <= 9:
        return "Modéré", WARNING
    elif score <= 15:
        return "Élevé", ORANGE
    else:
        return "Très élevé", DANGER


if "risk_assessments" not in st.session_state:
    st.session_state.risk_assessments = []

# ---------------------------------------------------------------------
# Formulaire de saisie
# ---------------------------------------------------------------------
section_title("Nouvelle évaluation de risque", "Renseignez la probabilité et la gravité pour un événement donné")

with st.form("risk_form", clear_on_submit=True):
    c1, c2 = st.columns(2)
    with c1:
        evenement = st.selectbox("Maladie / événement de santé publique", DISEASES)
        districts_df = get_districts()
        district = st.selectbox(
            "Localisation (optionnel)",
            ["National"] + sorted(districts_df["district"].unique().tolist()),
        )
    with c2:
        probabilite = st.select_slider(
            "Probabilité de survenue", options=list(PROB_LEVELS.keys()),
            value=3, format_func=lambda x: f"{x} — {PROB_LEVELS[x]}",
        )
        gravite = st.select_slider(
            "Gravité potentielle", options=list(GRAV_LEVELS.keys()),
            value=3, format_func=lambda x: f"{x} — {GRAV_LEVELS[x]}",
        )
    commentaire = st.text_area(
        "Justification / éléments de contexte",
        placeholder="Ex. : rupture de stock vaccinal, mouvement de population, saison des pluies, résultats de laboratoire...",
    )
    submitted = st.form_submit_button("Ajouter l'évaluation", use_container_width=True, icon=":material/add_circle:")

if submitted:
    score = probabilite * gravite
    niveau, couleur = risk_class(score)
    st.session_state.risk_assessments.append({
        "Événement": evenement,
        "Localisation": district,
        "Probabilité": probabilite,
        "Gravité": gravite,
        "Score": score,
        "Niveau de risque": niveau,
        "Commentaire": commentaire,
        "Date": pd.Timestamp.today().strftime("%d/%m/%Y %H:%M"),
    })
    st.success(f"Évaluation ajoutée avec succès — Niveau de risque : **{niveau}** (score {score}/25)",
               icon=":material/check_circle:")

# ---------------------------------------------------------------------
# Matrice de risque visuelle
# ---------------------------------------------------------------------
section_title("Matrice de risque", "Croisement Probabilité × Gravité (échelle 1 à 5)")

col_matrix, col_legend = st.columns([2.2, 1])

with col_matrix:
    z = [[p * g for g in range(1, 6)] for p in range(1, 6)]
    z = z[::-1]

    colorscale = [
        [0.0, "#B7E4C7"], [0.16, PRIMARY],
        [0.16, "#F5D06F"], [0.36, WARNING],
        [0.36, "#F1A26B"], [0.6, ORANGE],
        [0.6, "#F1949E"], [1.0, DANGER],
    ]

    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=[GRAV_LEVELS[g] for g in range(1, 6)],
        y=[PROB_LEVELS[p] for p in range(5, 0, -1)],
        colorscale=colorscale,
        showscale=False,
        text=z,
        texttemplate="%{text}",
        textfont=dict(size=14, family="Poppins, sans-serif"),
        hovertemplate="Probabilité : %{y}<br>Gravité : %{x}<br>Score : %{z}<extra></extra>",
        xgap=3, ygap=3,
    ))

    if st.session_state.risk_assessments:
        hist_df = pd.DataFrame(st.session_state.risk_assessments)
        fig.add_trace(go.Scatter(
            x=[GRAV_LEVELS[g] for g in hist_df["Gravité"]],
            y=[PROB_LEVELS[p] for p in hist_df["Probabilité"]],
            mode="markers+text",
            text=hist_df["Événement"],
            textposition="top center",
            textfont=dict(size=11, family="Poppins, sans-serif", color="#1A1A2E"),
            marker=dict(size=17, color="#1A1A2E", symbol="diamond", line=dict(width=2, color="white")),
            name="Évaluations enregistrées",
            hovertemplate="%{text}<extra></extra>",
        ))

    apply_chart_theme(fig, height=460)
    fig.update_layout(
        xaxis_title="Gravité potentielle",
        yaxis_title="Probabilité de survenue",
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

with col_legend:
    st.markdown("##### Légende des niveaux de risque")
    color_legend([
        (PRIMARY, "<b>Faible (1–4)</b> — Surveillance de routine"),
        (WARNING, "<b>Modéré (5–9)</b> — Vigilance renforcée"),
        (ORANGE, "<b>Élevé (10–15)</b> — Mesures de préparation actives"),
        (DANGER, "<b>Très élevé (16–25)</b> — Réponse immédiate requise"),
    ])

# ---------------------------------------------------------------------
# Registre des évaluations
# ---------------------------------------------------------------------
section_title("Registre des évaluations de risque", "Historique des événements évalués dans cette session")

if not st.session_state.risk_assessments:
    st.info("Aucune évaluation enregistrée pour le moment. Utilisez le formulaire ci-dessus pour commencer.",
             icon=":material/info:")
else:
    reg_df = pd.DataFrame(st.session_state.risk_assessments).sort_values("Score", ascending=False)

    c1, c2, c3 = st.columns(3)
    with c1:
        kpi_card("Évaluations enregistrées", fr_number(len(reg_df)), "", accent=INFO, icon="list")
    with c2:
        kpi_card("Risques élevés / très élevés", fr_number(int((reg_df["Score"] >= 10).sum())), "",
                  accent=DANGER, delta_color=DANGER, icon="alert")
    with c3:
        kpi_card("Score de risque moyen", f"{round(reg_df['Score'].mean(), 1)} / 25", "", accent=WARNING, icon="chart")

    st.dataframe(
        reg_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Score": st.column_config.ProgressColumn("Score", min_value=0, max_value=25, format="%d"),
        },
    )

    if st.button("Réinitialiser le registre", icon=":material/delete:"):
        st.session_state.risk_assessments = []
        st.rerun()
