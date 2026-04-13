import streamlit as st 
import pandas as pd 
import folium 
import streamlit_folium as st_folium 
import geopandas as gpd 
### Interface 

st.header("Monitoring tool of Wari-Maro - Monts Kouffé National Park")

## Data importations 
shape = gpd.read_file("bassins.shp")
data = pd.read_csv("Water.csv")

## Transformation to GeoJSON file 
m = folium.Map(location=[9.345062821272252, 2.612680777718885], zoom_start=10)
# Add Shapefile to Map
folium.GeoJson(shape).add_to(m)

# ... tes imports ...

# 1. On affiche la carte et on capture l'interaction
map_data = st_folium.st_folium(m, width=700, height = 400, key="map")

# 2. On détermine quel bassin est sélectionné
# Priorité : le clic sur la carte, sinon la sélection dans la sidebar
id_clique = None
if map_data['last_active_drawing']:
    # On récupère l'ID (assure-toi que 'ws_id' est bien dans les propriétés du shapefile)
    id_clique = map_data['last_active_drawing']['properties'].get('ws_id')

# 3. Synchronisation entre Sidebar et Carte
if id_clique:
    bassin_choisi = st.sidebar.selectbox(
        "Choose a sub-watershed:",
        options=data['ws_id'].unique(),
        index=list(data['ws_id'].unique()).index(id_clique)
    )
else:
    bassin_choisi = st.sidebar.selectbox(
        "Choose a sub-watershed:",
        options=data['ws_id'].unique()
    )

# 3. FILTRAGE : On récupère uniquement la ligne du bassin sélectionné
data_bassin = data[data['ws_id'] == bassin_choisi].iloc[0]

# 4. AFFICHAGE DES MÉTRIQUES
st.title(f"📍 Metrics of the sub-watershed N°: {bassin_choisi}")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Carbon strorage", value=f"{data_bassin['carbon_ha']:.1f} t/ha", border = True)

with col2:
    st.metric(label="Annual Runoff", value=f"{data_bassin['awy_ha']:.1f} m³", border = True)

with col3:
    score = data_bassin['R_nexus']
    st.metric(
        label="Nexus resilience index", 
        value=f"{score:.2f}",
        delta="Critical" if score < 0.6 else "Stable",
        delta_color="inverse" if score < 0.4 else "normal", border = True)
with col4: 
    st.metric(label = "Area of sub-watershed", value = f"{data_bassin['area']:.1f} ha", border = True)

