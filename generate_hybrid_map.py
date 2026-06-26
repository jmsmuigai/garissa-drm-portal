import folium
import os
import json
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "OUTPUT"
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "google_hybrid_map.html"

# Garissa Coordinates
GARISSA_LAT = -0.4532
GARISSA_LON = 39.6461

def create_map():
    print("🌍 Generating Google Hybrid Map for Garissa...")
    
    # Create base map
    m = folium.Map(location=[GARISSA_LAT, GARISSA_LON], zoom_start=8, tiles=None)

    # Base Layers
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Hybrid',
        overlay=False,
        control=True
    ).add_to(m)

    folium.TileLayer(
        tiles='OpenStreetMap',
        name='OpenStreetMap',
        overlay=False,
        control=True
    ).add_to(m)

    # 1. Garissa County Boundary (Simulated polygon for demonstration)
    garissa_bounds = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "Garissa County"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[[38.5, 0.5], [41.0, 0.5], [41.0, -2.0], [38.5, -2.0], [38.5, 0.5]]]
                }
            }
        ]
    }
    
    folium.GeoJson(
        garissa_bounds,
        name="Garissa Boundary",
        style_function=lambda x: {'color': 'yellow', 'weight': 2, 'fillOpacity': 0.05},
        tooltip="Garissa County"
    ).add_to(m)

    # 2. Critical Infrastructure: Schools & Hospitals (Mock data based on El Nino context)
    hospitals = folium.FeatureGroup(name="🏥 Health Centers & Hospitals")
    folium.Marker([-0.45, 39.65], popup="Garissa Provincial Hospital<br>Status: Secure", icon=folium.Icon(color='blue', icon='plus')).add_to(hospitals)
    folium.Marker([-0.10, 39.50], popup="Modika Dispensary<br>Status: High Flood Risk", icon=folium.Icon(color='red', icon='plus')).add_to(hospitals)
    folium.Marker([0.05, 39.40], popup="Balambala Health Center<br>Status: Secure", icon=folium.Icon(color='blue', icon='plus')).add_to(hospitals)
    hospitals.add_to(m)

    schools = folium.FeatureGroup(name="🏫 Schools (Evacuation Centers)")
    folium.Marker([-0.46, 39.64], popup="Garissa High School<br>Capacity: 500<br>Stock: Emergency Kits Ready", icon=folium.Icon(color='green', icon='info-sign')).add_to(schools)
    folium.Marker([-0.15, 39.55], popup="Sankuri Secondary<br>Capacity: 300<br>Stock: Need Tents", icon=folium.Icon(color='orange', icon='info-sign')).add_to(schools)
    schools.add_to(m)

    # 3. Flood Risk Zones / River Tana 500m Buffer
    flood_zones = folium.FeatureGroup(name="🌊 River Tana Flood Buffer (500m)")
    # A rough line representing River Tana
    river_coords = [[0.5, 39.0], [0.0, 39.3], [-0.45, 39.64], [-1.0, 40.0], [-1.5, 40.1]]
    folium.PolyLine(river_coords, color="cyan", weight=5, tooltip="River Tana").add_to(flood_zones)
    # Buffer polygon mock
    folium.Polygon([
        [0.55, 38.95], [0.45, 39.05], 
        [-0.05, 39.35], [0.05, 39.25], 
        [-0.40, 39.69], [-0.50, 39.59],
        [-1.05, 40.05], [-0.95, 39.95]
    ], color="red", fill=True, fillOpacity=0.4, tooltip="500m Flood Vulnerability Zone").add_to(flood_zones)
    flood_zones.add_to(m)

    # 4. Laghas (Seasonal Rivers)
    laghas = folium.FeatureGroup(name="💧 Laghas (Seasonal Flood Paths)")
    folium.PolyLine([[-0.2, 40.0], [-0.4, 39.8], [-0.45, 39.64]], color="blue", weight=3, dash_array="5, 5", tooltip="Seasonal River 1").add_to(laghas)
    folium.PolyLine([[-0.8, 39.2], [-0.6, 39.5], [-0.45, 39.64]], color="blue", weight=3, dash_array="5, 5", tooltip="Seasonal River 2").add_to(laghas)
    laghas.add_to(m)

    # Add Layer Control (Checkboxes)
    folium.LayerControl(collapsed=False).add_to(m)

    m.save(str(OUTPUT_FILE))
    print(f"✅ Map saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    create_map()
