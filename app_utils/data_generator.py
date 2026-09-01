"""
Générateur de données de démonstration pour le tableau de bord MINSANTE / DLMEP.

IMPORTANT : Ces données sont SIMULÉES à des fins de démonstration visuelle.
Pour un usage réel, remplacez les fonctions ci-dessous par des connecteurs vers :
  - vos exports DHIS2 (API ou fichiers .csv/.xlsx),
  - votre base de surveillance SIMR/SFE,
  - vos seuils épidémiques officiels par maladie.

La structure des DataFrames retournés (noms de colonnes) est conçue pour rester
stable même si vous changez la source de données : il vous suffit de faire en
sorte que vos vraies données respectent le même schéma de colonnes.
"""

import numpy as np
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Référentiel géographique (10 régions du Cameroun + districts de santé simulés)
# ---------------------------------------------------------------------------

REGIONS = {
    "Adamaoua":      (7.3167, 13.5833),
    "Centre":        (3.8667, 11.5167),
    "Est":           (4.5833, 13.6833),
    "Extrême-Nord":  (10.5956, 14.3247),
    "Littoral":      (4.0500, 9.7000),
    "Nord":          (9.3017, 13.3921),
    "Nord-Ouest":    (5.9631, 10.1591),
    "Ouest":         (5.4737, 10.4176),
    "Sud":           (2.9167, 11.1500),
    "Sud-Ouest":     (4.1560, 9.2632),
}

DISEASES = [
    "Rougeole", "Choléra", "Fièvre Jaune", "PFA (Polio)", "MVE (Ebola/Marburg)",
    "Mpox", "Méningite Cérébro-Spinale", "Fièvre Typhoïde", "COVID-19",
    "Diarrhée Sanguinolente (Shigellose)",
]

# Seuils illustratifs (cas/semaine) — À REMPLACER par les seuils officiels SIMR
# par maladie et par district (corridor endémique réel).
DISEASE_THRESHOLDS = {
    "Rougeole":                             {"alerte": 1,  "epidemique": 3},
    "Choléra":                              {"alerte": 1,  "epidemique": 2},
    "Fièvre Jaune":                         {"alerte": 1,  "epidemique": 1},
    "PFA (Polio)":                          {"alerte": 1,  "epidemique": 1},
    "MVE (Ebola/Marburg)":                  {"alerte": 1,  "epidemique": 1},
    "Mpox":                                 {"alerte": 2,  "epidemique": 5},
    "Méningite Cérébro-Spinale":            {"alerte": 2,  "epidemique": 5},
    "Fièvre Typhoïde":                      {"alerte": 5,  "epidemique": 10},
    "COVID-19":                             {"alerte": 5,  "epidemique": 15},
    "Diarrhée Sanguinolente (Shigellose)":  {"alerte": 3,  "epidemique": 8},
}

N_DISTRICTS_PER_REGION = 5


@st.cache_data(show_spinner=False)
def get_districts() -> pd.DataFrame:
    """Référentiel des districts de santé (simulé)."""
    rng = np.random.default_rng(42)
    rows = []
    did = 1
    for region, (lat, lon) in REGIONS.items():
        for i in range(1, N_DISTRICTS_PER_REGION + 1):
            jitter_lat = rng.uniform(-0.6, 0.6)
            jitter_lon = rng.uniform(-0.6, 0.6)
            rows.append({
                "district_id": f"DS{did:03d}",
                "district": f"DS {region} {i}",
                "region": region,
                "lat": round(lat + jitter_lat, 4),
                "lon": round(lon + jitter_lon, 4),
                "population": int(rng.integers(30_000, 250_000)),
            })
            did += 1
    return pd.DataFrame(rows)


@st.cache_data(show_spinner=False)
def get_weekly_surveillance_data(n_weeks: int = 26) -> pd.DataFrame:
    """
    Série hebdomadaire de cas notifiés par district et par maladie.
    Colonnes : semaine, date, district_id, district, region, maladie,
               cas, deces, seuil_alerte, seuil_epidemique, statut
    """
    rng = np.random.default_rng(7)
    districts = get_districts()
    end_date = pd.Timestamp.today().normalize()
    weeks = pd.date_range(end=end_date, periods=n_weeks, freq="W-MON")

    rows = []
    for _, d in districts.iterrows():
        for disease in DISEASES:
            base_rate = rng.choice([0.05, 0.1, 0.3, 0.6, 1.2], p=[0.35, 0.25, 0.2, 0.12, 0.08])
            # une poignée de districts connaissent une flambée récente
            outbreak = rng.random() < 0.06
            for wk_idx, wk in enumerate(weeks):
                lam = base_rate
                if outbreak and wk_idx >= n_weeks - 4:
                    lam = base_rate * rng.uniform(6, 18)
                cas = int(rng.poisson(lam))
                deces = int(rng.binomial(cas, 0.03)) if cas > 0 else 0
                rows.append({
                    "semaine": wk_idx + 1,
                    "date": wk,
                    "district_id": d["district_id"],
                    "district": d["district"],
                    "region": d["region"],
                    "maladie": disease,
                    "cas": cas,
                    "deces": deces,
                })
    df = pd.DataFrame(rows)
    df["seuil_alerte"] = df["maladie"].map(lambda m: DISEASE_THRESHOLDS[m]["alerte"])
    df["seuil_epidemique"] = df["maladie"].map(lambda m: DISEASE_THRESHOLDS[m]["epidemique"])

    def statut(row):
        if row["cas"] >= row["seuil_epidemique"]:
            return "Épidémique"
        elif row["cas"] >= row["seuil_alerte"]:
            return "Alerte"
        return "Normal"

    df["statut"] = df.apply(statut, axis=1)
    return df


@st.cache_data(show_spinner=False)
def get_current_district_status() -> pd.DataFrame:
    """
    Statut courant (dernière semaine dispo) par district : pire statut parmi
    toutes les maladies + liste des maladies concernées. Utilisé pour la carte.
    """
    df = get_weekly_surveillance_data()
    last_week = df["semaine"].max()
    last = df[df["semaine"] == last_week].copy()

    order = {"Épidémique": 2, "Alerte": 1, "Normal": 0}
    last["ordre_statut"] = last["statut"].map(order)

    agg = (
        last.sort_values("ordre_statut", ascending=False)
        .groupby(["district_id", "district", "region"])
        .agg(
            statut_pire=("statut", "first"),
            cas_total=("cas", "sum"),
            deces_total=("deces", "sum"),
            maladies_actives=("maladie", lambda s: ", ".join(
                sorted(set(last.loc[s.index][last.loc[s.index, "statut"] != "Normal"]["maladie"]))
            ) or "Aucune"),
        )
        .reset_index()
    )

    districts = get_districts()[["district_id", "lat", "lon", "population"]]
    agg = agg.merge(districts, on="district_id", how="left")
    return agg
