# Tableau de Bord de Surveillance Épidémiologique — MINSANTE / DLMEP

Application Streamlit multi-pages pour la surveillance intégrée de la maladie (SIMR/SFE).

## 📦 Contenu

```
minsante_dashboard/
├── app.py                                    # Routeur principal (navigation + config)
├── pages/
│   ├── accueil.py                            # Page d'accueil (KPI globaux)
│   ├── situation_epidemiologique.py          # Courbes épidémiques, carte cas/décès
│   ├── alertes_de_seuil.py                   # Détection des seuils franchis, carte
│   ├── evaluation_des_risques.py             # Matrice de risque interactive
│   └── districts_a_risque.py                 # Carte nationale des districts
├── app_utils/
│   ├── data_generator.py                     # Données simulées (À REMPLACER)
│   └── styling.py                            # CSS, icônes SVG, cartes KPI réutilisables
├── .streamlit/config.toml                    # Thème visuel
└── requirements.txt
```

Tous les noms de fichiers sont en ASCII pur (aucun emoji) pour éviter les problèmes
d'encodage lors du transfert entre systèmes (Windows notamment). La navigation entre
pages et ses icônes sont gérées par code dans `app.py` via `st.navigation`, avec des
icônes Material natives de Streamlit (`:material/...:`) plutôt que des emojis. Le
contenu visuel (cartes KPI, en-têtes, cartes de modules) utilise un jeu d'icônes
SVG vectorielles défini dans `app_utils/styling.py`.

## 🚀 Installation et lancement

```bash
cd minsante_dashboard
pip install -r requirements.txt
streamlit run app.py
```

L'application s'ouvre automatiquement dans votre navigateur (http://localhost:8501).

## 🔌 Connecter vos vraies données (DHIS2 / SIMR)

Toutes les données affichées sont **simulées** dans `app_utils/data_generator.py` afin que
vous puissiez tester le rendu visuel immédiatement. Pour brancher vos vraies données :

1. **Référentiel des districts** (`get_districts`) : remplacez par votre liste des
   213 districts de santé avec leurs coordonnées géographiques (lat/lon) —
   colonnes attendues : `district_id, district, region, lat, lon, population`.

2. **Données hebdomadaires de surveillance** (`get_weekly_surveillance_data`) :
   remplacez par un export DHIS2 (API `analytics` ou fichier `.csv`) avec les
   colonnes : `semaine, date, district_id, district, region, maladie, cas, deces,
   seuil_alerte, seuil_epidemique, statut`.

   - Vous pouvez calculer `seuil_alerte` / `seuil_epidemique` à partir de votre
     corridor endémique réel (moyenne + 2 écarts-types des années précédentes),
     et `statut` par comparaison `cas` vs seuils.

3. **Seuils par maladie** (`DISEASE_THRESHOLDS`) : à ajuster avec les seuils
   officiels validés par la DLMEP pour chaque maladie prioritaire.

Tant que le **schéma de colonnes** est respecté, les 4 pages fonctionnent sans
aucune modification supplémentaire.

## 🧩 Fonctionnalités par page

- **Situation Épidémiologique** : courbe épidémique multi-maladies, répartition
  régionale, part des maladies, tableau détaillé filtrable.
- **Alertes de Seuil** : comparaison cas observés vs seuil d'alerte / épidémique,
  liste des districts en alerte, journal historique des alertes (8 semaines).
- **Évaluation des Risques** : formulaire de saisie (probabilité × gravité),
  matrice de risque 5×5 interactive, registre exportable des évaluations.
- **Districts à Risque** : carte interactive (rouge = épidémie, bulles = risque),
  répartition par région, tableau détaillé exportable en CSV.

## 🎨 Personnalisation

- Couleurs et logo : modifiez `app_utils/styling.py` (variables `PRIMARY`, `DANGER`, etc.)
  et `.streamlit/config.toml`.
- Pour ajouter le logo officiel MINSANTE, placez un fichier image dans le dossier
  et ajoutez `st.image("logo.png")` dans la barre latérale de `app.py`.
