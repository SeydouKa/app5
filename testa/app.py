# app.py
import streamlit as st
import geopandas as gpd
from shapely.geometry import Point
import geocoder

# Charger le fichier shapefile
Dakar = 'Dakar.shp'
DKR = gpd.read_file(Dakar)
Kaolack = "Kaolack.shp"
KL = gpd.read_file(Kaolack)
inondees = "zone_inondées.shp"
ZI = gpd.read_file(inondees)

def get_device_location():
    location = geocoder.ip('me')
    latitude, longitude = location.latlng
    return latitude, longitude

def main():
    st.title("Application de Géolocalisation")

    # Obtenir la géolocalisation de l'appareil
    coordinates = get_device_location()

    if coordinates:
        st.write(f"Géolocalisation de l'appareil: Latitude {coordinates[0]}, Longitude {coordinates[1]}")
    else:
        st.warning("Impossible de récupérer la géolocalisation de l'appareil.")

    # Widget Streamlit pour entrer manuellement les coordonnées
    st.sidebar.header("Entrer les Coordonnées Manuellement")
    latitude_input = st.sidebar.number_input("Latitude", value=coordinates[0])
    longitude_input = st.sidebar.number_input("Longitude", value=coordinates[1])

    # Créer un point avec les coordonnées entrées
    point = Point(longitude_input, latitude_input)

    # Vérifier si le point est dans la région
    point_in_DKR = DKR.geometry.contains(point).any()
    point_in_KL = KL.geometry.contains(point).any()
    point_in_ZI = ZI.geometry.contains(point).any()

    # Afficher les résultats
    st.subheader("Résultats :")
    if point_in_DKR:
        st.success("Le point est dans la région de Dakar.")
    elif point_in_KL:
        st.success("Le point est dans la région de Kaolack.")
    else:
        st.warning("Le point n'est dans aucune des régions de Dakar et de Kaolack.")

    if point_in_ZI:
        st.error("Le point se trouve dans une zone inondable.")
    else:
        st.success("Le point ne se trouve pas dans une zone inondable.")

if __name__ == "__main__":
    main()
