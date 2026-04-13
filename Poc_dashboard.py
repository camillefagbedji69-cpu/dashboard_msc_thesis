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
m = folium.Map(location=[shape.centroid.y.mean(), shape.centroid.x.mean()], zoom_start=10)
# Add Shapefile to Map
folium.GeoJson(shape).add_to(m)

# Display in Streamlit
st_folium(m, width=700, height=500)

## Configuration 
st.sidebar.header("Configuration")
bassin_choisi = st.sidebar.selectbox(
    "Choose a sub-watershed:",
    options=df['ws_id'].unique()
)

# 3. FILTRAGE : On récupère uniquement la ligne du bassin sélectionné
data_bassin = data[data['ws_id'] == bassin_choisi].iloc[0]

# 4. AFFICHAGE DES MÉTRIQUES
st.title(f"📍 Metrics of the sub-watershed N°: {bassin_choisi}")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Carbon strorage", value=f"{data_bassin['carbon_ha']:.3f} t/ha", border = True)

with col2:
    st.metric(label="Annual Runoff", value=f"{data_bassin['awy_ha']:.3f} m³", border = True)

with col3:
    score = data_bassin['R_nexus']
    st.metric(
        label="Nexus resilience index", 
        value=f"{score:.2f}",
        delta="Critical" if score < 0.6 else "Stable",
        delta_color="inverse" if score < 0.4 else "normal", border = True)

with col4: 
    st.metric(label = "Area of sub-watershed", value = f"{data_bassin['area']:.3f} ha", border = True)

