import streamlit as st
import pandas as pd
import plotly.express as px

from app_utils.styling import (
    page_header, kpi_card, section_title, fr_number, apply_chart_theme, color_legend,
    PRIMARY, DANGER, INFO, SCALE_CAS, SCALE_DECES,
)
from app_utils.data_generator import get_weekly_surveillance_data, get_districts, DISEASES

page_header("Situation Épidémiologique", "Suivi des tendances de cas et de décès par maladie sous surveillance", icon="chart")

df = get_weekly_surveillance_data()
districts_geo = get_districts()[["district_id", "lat", "lon", "population"]]

# ---------------------------------------------------------------------
# Filtres
# ---------------------------------------------------------------------
with st.sidebar:
    st.markdown("**Filtres**")
    regions_sel = st.multiselect("Région(s)", sorted(df["region"].unique()), default=[])
    maladies_sel = st.multiselect("Maladie(s)", DISEASES, default=["Rougeole", "Choléra", "Mpox"])
    n_semaines = st.slider("Nombre de semaines à afficher", 4, int(df["semaine"].max()), 12)

fdf = df.copy()
if regions_sel:
    fdf = fdf[fdf["region"].isin(regions_sel)]
if maladies_sel:
    fdf = fdf[fdf["maladie"].isin(maladies_sel)]
fdf = fdf[fdf["semaine"] > fdf["semaine"].max() - n_semaines]

last_week = fdf["semaine"].max()
last = fdf[fdf["semaine"] == last_week]
prev = fdf[fdf["semaine"] == last_week - 1]

# ---------------------------------------------------------------------
# Indicateurs clés
# ---------------------------------------------------------------------
total_cas = int(fdf["cas"].sum())
total_deces = int(fdf["deces"].sum())
letalite = round((total_deces / total_cas * 100), 2) if total_cas else 0.0
cas_sem = int(last["cas"].sum())
cas_sem_prev = int(prev["cas"].sum()) if not prev.empty else 0
if cas_sem > cas_sem_prev:
    tendance, tendance_couleur, tendance_icone = "En hausse", DANGER, "trend-up"
elif cas_sem < cas_sem_prev:
    tendance, tendance_couleur, tendance_icone = "En baisse", PRIMARY, "trend-down"
else:
    tendance, tendance_couleur, tendance_icone = "Stable", INFO, "trend-flat"

c1, c2, c3, c4 = st.columns(4)
with c1:
    kpi_card("Total des cas", fr_number(total_cas), f"Sur les {n_semaines} dernières semaines", accent=INFO, icon="file")
with c2:
    kpi_card("Total des décès", fr_number(total_deces), f"Sur les {n_semaines} dernières semaines", accent=DANGER, icon="x-circle")
with c3:
    kpi_card("Létalité (CFR)", f"{letalite} %", "Décès / cas notifiés", accent=DANGER if letalite > 3 else PRIMARY, icon="chart")
with c4:
    kpi_card("Tendance (semaine en cours)", tendance, f"{fr_number(cas_sem)} cas vs {fr_number(cas_sem_prev)} en S-1",
             accent=tendance_couleur, delta_color=tendance_couleur, icon=tendance_icone)

# ---------------------------------------------------------------------
# Courbe épidémique
# ---------------------------------------------------------------------
section_title("Courbe épidémique", "Évolution hebdomadaire du nombre de cas notifiés")
curve = fdf.groupby(["date", "maladie"], as_index=False)["cas"].sum()
fig_curve = px.line(
    curve, x="date", y="cas", color="maladie", markers=True,
    labels={"date": "Semaine épidémiologique", "cas": "Nombre de cas", "maladie": "Maladie"},
    color_discrete_sequence=px.colors.qualitative.Bold,
)
fig_curve.update_traces(line=dict(width=2.5), marker=dict(size=6))
apply_chart_theme(fig_curve, height=430)
fig_curve.update_layout(hovermode="x unified")
st.plotly_chart(fig_curve, use_container_width=True)

# ---------------------------------------------------------------------
# Carte des cas et décès par district
# ---------------------------------------------------------------------
section_title("Carte des cas et décès", "Répartition géographique cumulée sur la période sélectionnée, par district")

indicateur = st.radio("Indicateur à cartographier", ["Cas", "Décès"], horizontal=True, key="map_indicateur_situation")
col_val = "cas" if indicateur == "Cas" else "deces"
scale = SCALE_CAS if indicateur == "Cas" else SCALE_DECES

geo_agg = fdf.groupby(["district_id", "district", "region"], as_index=False).agg(
    cas=("cas", "sum"), deces=("deces", "sum")
)
geo_agg = geo_agg.merge(districts_geo, on="district_id", how="left")
geo_agg = geo_agg[geo_agg[col_val] >= 0]

fig_map = px.scatter_map(
    geo_agg,
    lat="lat", lon="lon",
    size=col_val,
    color=col_val,
    color_continuous_scale=scale,
    size_max=32,
    hover_name="district",
    hover_data={"region": True, "cas": True, "deces": True, "lat": False, "lon": False},
    zoom=5.2,
    center={"lat": 5.5, "lon": 12.5},
    height=520,
)
fig_map.update_layout(
    map_style="open-street-map",
    margin=dict(l=0, r=0, t=10, b=0),
    coloraxis_colorbar=dict(title=indicateur),
    font=dict(family="Poppins, sans-serif", size=13),
)
st.plotly_chart(fig_map, use_container_width=True)
st.caption(f"Taille et couleur des bulles proportionnelles au nombre de {indicateur.lower()} cumulés par district sur la période affichée.")

# ---------------------------------------------------------------------
# Répartitions
# ---------------------------------------------------------------------
col_a, col_b = st.columns(2)

with col_a:
    section_title("Répartition régionale", "Cas cumulés par région sur la période")
    reg = fdf.groupby("region", as_index=False)["cas"].sum().sort_values("cas", ascending=True)
    fig_reg = px.bar(reg, x="cas", y="region", orientation="h", color="cas",
                      color_continuous_scale=SCALE_CAS,
                      labels={"cas": "Nombre de cas", "region": ""})
    apply_chart_theme(fig_reg, height=380)
    fig_reg.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_reg, use_container_width=True)

with col_b:
    section_title("Répartition par maladie", "Part de chaque maladie dans le total des cas")
    mal = fdf.groupby("maladie", as_index=False)["cas"].sum()
    fig_mal = px.pie(mal, names="maladie", values="cas", hole=0.55,
                      color_discrete_sequence=px.colors.qualitative.Bold)
    apply_chart_theme(fig_mal, height=380)
    st.plotly_chart(fig_mal, use_container_width=True)

# ---------------------------------------------------------------------
# Table détaillée
# ---------------------------------------------------------------------
section_title("Détail par district", "Cas et décès notifiés au cours de la semaine en cours")
detail = (
    last.groupby(["region", "district", "maladie"], as_index=False)
    .agg(cas=("cas", "sum"), deces=("deces", "sum"))
    .sort_values("cas", ascending=False)
)
detail = detail[detail["cas"] > 0]
st.dataframe(
    detail,
    use_container_width=True,
    hide_index=True,
    column_config={
        "region": "Région",
        "district": "District",
        "maladie": "Maladie",
        "cas": st.column_config.NumberColumn("Cas", format="%d"),
        "deces": st.column_config.NumberColumn("Décès", format="%d"),
    },
)
