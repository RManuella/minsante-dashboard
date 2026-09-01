import streamlit as st
import pandas as pd
import plotly.express as px

from app_utils.styling import (
    page_header, kpi_card, section_title, status_badge, fr_number, apply_chart_theme, color_legend,
    PRIMARY, DANGER, WARNING, INFO, STATUS_COLORS,
)
from app_utils.data_generator import get_current_district_status

page_header("Districts à Risque", "Cartographie nationale des districts en épidémie et des districts à risque", icon="map")

status_df = get_current_district_status()

with st.sidebar:
    st.markdown("**Filtres**")
    regions_sel = st.multiselect("Région(s)", sorted(status_df["region"].unique()), default=[])
    statuts_sel = st.multiselect(
        "Statut", ["Épidémique", "Alerte", "Normal"], default=["Épidémique", "Alerte", "Normal"]
    )

fdf = status_df.copy()
if regions_sel:
    fdf = fdf[fdf["region"].isin(regions_sel)]
if statuts_sel:
    fdf = fdf[fdf["statut_pire"].isin(statuts_sel)]

nb_epid = int((fdf["statut_pire"] == "Épidémique").sum())
nb_alerte = int((fdf["statut_pire"] == "Alerte").sum())
nb_normal = int((fdf["statut_pire"] == "Normal").sum())
pop_a_risque = int(fdf.loc[fdf["statut_pire"] != "Normal", "population"].sum())

c1, c2, c3, c4 = st.columns(4)
with c1:
    kpi_card("Districts en épidémie", fr_number(nb_epid), "Visibles en rouge sur la carte", accent=DANGER, delta_color=DANGER, icon="alert")
with c2:
    kpi_card("Districts en alerte", fr_number(nb_alerte), "Visibles en orange sur la carte", accent=WARNING, delta_color=WARNING, icon="shield")
with c3:
    kpi_card("Districts en situation normale", fr_number(nb_normal), "Visibles en vert sur la carte", accent=PRIMARY, icon="check")
with c4:
    kpi_card("Population à risque", fr_number(pop_a_risque), "Cumul districts alerte + épidémie", accent=INFO, icon="users")

# ---------------------------------------------------------------------
# Carte
# ---------------------------------------------------------------------
section_title("Carte des districts", "Statut épidémiologique courant par district de santé")

color_map = STATUS_COLORS
size_map = {"Épidémique": 24, "Alerte": 16, "Normal": 8}
fdf["taille"] = fdf["statut_pire"].map(size_map)

fig_map = px.scatter_map(
    fdf,
    lat="lat", lon="lon",
    color="statut_pire",
    size="taille",
    size_max=26,
    color_discrete_map=color_map,
    hover_name="district",
    hover_data={"region": True, "statut_pire": True, "cas_total": True, "deces_total": True,
                "maladies_actives": True, "lat": False, "lon": False, "taille": False},
    zoom=5.3,
    center={"lat": 5.5, "lon": 12.5},
    height=560,
    labels={"statut_pire": "Statut"},
)
fig_map.update_layout(
    map_style="open-street-map",
    margin=dict(l=0, r=0, t=10, b=0),
    legend_title_text="Statut",
    font=dict(family="Poppins, sans-serif", size=13),
)
st.plotly_chart(fig_map, use_container_width=True)

color_legend([
    (DANGER, "Rouge — district en épidémie (seuil épidémique franchi)"),
    (WARNING, "Orange — district à risque / en alerte (taille proportionnelle à la sévérité)"),
    (PRIMARY, "Vert — situation normale"),
])

# ---------------------------------------------------------------------
# Répartitions
# ---------------------------------------------------------------------
col_a, col_b = st.columns([1.3, 1])
with col_a:
    section_title("Districts par statut et par région", "Répartition régionale des statuts épidémiologiques")
    reg_status = fdf.groupby(["region", "statut_pire"], as_index=False).size()
    fig_bar = px.bar(
        reg_status, x="region", y="size", color="statut_pire",
        color_discrete_map=color_map, barmode="stack",
        labels={"size": "Nombre de districts", "region": "Région", "statut_pire": "Statut"},
    )
    apply_chart_theme(fig_bar, height=380)
    st.plotly_chart(fig_bar, use_container_width=True)

with col_b:
    section_title("Répartition globale", "Part des districts par statut")
    pie_df = fdf["statut_pire"].value_counts().reset_index()
    pie_df.columns = ["statut", "nombre"]
    fig_pie = px.pie(pie_df, names="statut", values="nombre", color="statut",
                      color_discrete_map=color_map, hole=0.55)
    apply_chart_theme(fig_pie, height=380)
    st.plotly_chart(fig_pie, use_container_width=True)

# ---------------------------------------------------------------------
# Tableau détaillé
# ---------------------------------------------------------------------
section_title("Tableau détaillé des districts", "Liste complète avec cas, décès et maladies actives")

table = fdf.sort_values(["statut_pire", "cas_total"], ascending=[True, False]).copy()
table_display = table[[
    "region", "district", "statut_pire", "cas_total", "deces_total", "population", "maladies_actives"
]].rename(columns={
    "region": "Région", "district": "District", "statut_pire": "Statut",
    "cas_total": "Cas (semaine en cours)", "deces_total": "Décès (semaine en cours)",
    "population": "Population", "maladies_actives": "Maladies actives",
})
table_display["Statut"] = table_display["Statut"].apply(status_badge)

st.write(table_display.to_html(escape=False, index=False, classes="alert-table"), unsafe_allow_html=True)

st.download_button(
    "Exporter le tableau (CSV)",
    data=table.drop(columns=["taille"], errors="ignore").to_csv(index=False).encode("utf-8-sig"),
    file_name="districts_a_risque.csv",
    mime="text/csv",
    icon=":material/download:",
)
