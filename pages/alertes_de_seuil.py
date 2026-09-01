import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from app_utils.styling import (
    page_header, kpi_card, section_title, status_badge, fr_number, apply_chart_theme,
    PRIMARY, DANGER, WARNING, SCALE_CAS, SCALE_DECES,
)
from app_utils.data_generator import get_weekly_surveillance_data, get_districts, DISEASES, DISEASE_THRESHOLDS

page_header("Alertes de Franchissement de Seuil", "Détection des districts ayant dépassé les seuils d'alerte ou épidémique", icon="alert")

df = get_weekly_surveillance_data()
districts_geo = get_districts()[["district_id", "lat", "lon", "population"]]

with st.sidebar:
    st.markdown("**Filtres**")
    maladie_sel = st.selectbox("Maladie", DISEASES, index=0)
    regions_sel = st.multiselect("Région(s)", sorted(df["region"].unique()), default=[])

th = DISEASE_THRESHOLDS[maladie_sel]
mdf = df[df["maladie"] == maladie_sel].copy()
if regions_sel:
    mdf = mdf[mdf["region"].isin(regions_sel)]

last_week = mdf["semaine"].max()
last = mdf[mdf["semaine"] == last_week]

nb_epid = int((last["statut"] == "Épidémique").sum())
nb_alerte = int((last["statut"] == "Alerte").sum())

c1, c2, c3, c4 = st.columns(4)
with c1:
    kpi_card("Seuil d'alerte", f"{th['alerte']} cas / semaine", maladie_sel, accent=WARNING, icon="shield")
with c2:
    kpi_card("Seuil épidémique", f"{th['epidemique']} cas / semaine", maladie_sel, accent=DANGER, icon="alert")
with c3:
    kpi_card("Districts en épidémie", fr_number(nb_epid), "Semaine en cours", accent=DANGER, delta_color=DANGER, icon="alert")
with c4:
    kpi_card("Districts en alerte", fr_number(nb_alerte), "Semaine en cours", accent=WARNING, delta_color=WARNING, icon="shield")

# ---------------------------------------------------------------------
# Courbe seuils vs observé
# ---------------------------------------------------------------------
section_title("Cas observés vs seuils", f"{maladie_sel} — agrégat national ou des régions filtrées")
agg = mdf.groupby(["semaine", "date"], as_index=False)["cas"].sum()

fig = go.Figure()
fig.add_trace(go.Scatter(x=agg["date"], y=agg["cas"], mode="lines+markers",
                          name="Cas observés", line=dict(color=PRIMARY, width=3), fill="tozeroy",
                          fillcolor="rgba(11,110,79,0.08)"))
fig.add_trace(go.Scatter(x=agg["date"], y=[th["alerte"]] * len(agg), mode="lines",
                          name="Seuil d'alerte", line=dict(color=WARNING, dash="dash", width=2)))
fig.add_trace(go.Scatter(x=agg["date"], y=[th["epidemique"]] * len(agg), mode="lines",
                          name="Seuil épidémique", line=dict(color=DANGER, dash="dash", width=2)))
apply_chart_theme(fig, height=420)
fig.update_layout(hovermode="x unified", yaxis_title="Cas / semaine", xaxis_title="Semaine épidémiologique")
st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------
# Carte des cas et décès (semaine en cours) pour la maladie sélectionnée
# ---------------------------------------------------------------------
section_title("Carte des cas et décès", f"{maladie_sel} — semaine en cours, avec seuils de référence par district")

indicateur = st.radio("Indicateur à cartographier", ["Cas", "Décès"], horizontal=True, key="map_indicateur_alertes")
col_val = "cas" if indicateur == "Cas" else "deces"
scale = SCALE_CAS if indicateur == "Cas" else SCALE_DECES

geo = last.groupby(["district_id", "district", "region", "statut"], as_index=False).agg(
    cas=("cas", "sum"), deces=("deces", "sum")
)
geo = geo.merge(districts_geo, on="district_id", how="left")

fig_map = px.scatter_mapbox(
    geo,
    lat="lat", lon="lon",
    size=col_val,
    color=col_val,
    color_continuous_scale=scale,
    size_max=30,
    hover_name="district",
    hover_data={"region": True, "statut": True, "cas": True, "deces": True, "lat": False, "lon": False},
    zoom=5.2,
    center={"lat": 5.5, "lon": 12.5},
    height=500,
)
fig_map.update_layout(
    mapbox_style="open-street-map",
    margin=dict(l=0, r=0, t=10, b=0),
    coloraxis_colorbar=dict(title=indicateur),
    font=dict(family="Poppins, sans-serif", size=13),
)
st.plotly_chart(fig_map, use_container_width=True)
st.caption(f"Taille et couleur des bulles proportionnelles au nombre de {indicateur.lower()} de {maladie_sel} sur la semaine en cours. Survolez un district pour voir son statut de seuil.")

# ---------------------------------------------------------------------
# Liste des alertes actives
# ---------------------------------------------------------------------
section_title("Districts en alerte ou en épidémie", "Semaine en cours")
alertes = last[last["statut"] != "Normal"].sort_values("cas", ascending=False)[
    ["region", "district", "cas", "deces", "seuil_alerte", "seuil_epidemique", "statut"]
]

if alertes.empty:
    st.success("Aucun district n'a franchi de seuil pour cette maladie sur la semaine en cours.", icon=":material/check_circle:")
else:
    alertes_display = alertes.rename(columns={
        "region": "Région", "district": "District", "cas": "Cas", "deces": "Décès",
        "seuil_alerte": "Seuil d'alerte", "seuil_epidemique": "Seuil épidémique", "statut": "Statut",
    }).copy()
    alertes_display["Statut"] = alertes_display["Statut"].apply(status_badge)
    st.write(
        alertes_display.to_html(escape=False, index=False, classes="alert-table"),
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# Journal des alertes
# ---------------------------------------------------------------------
section_title("Journal des alertes récentes", "Toutes maladies confondues — 8 dernières semaines")
recent = df[df["semaine"] > df["semaine"].max() - 8]
journal = recent[recent["statut"] != "Normal"].sort_values(["date", "cas"], ascending=[False, False])
journal = journal[["date", "region", "district", "maladie", "cas", "statut"]].head(200)

st.dataframe(
    journal,
    use_container_width=True,
    hide_index=True,
    column_config={
        "date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
        "region": "Région",
        "district": "District",
        "maladie": "Maladie",
        "cas": st.column_config.NumberColumn("Cas", format="%d"),
        "statut": "Statut",
    },
)
