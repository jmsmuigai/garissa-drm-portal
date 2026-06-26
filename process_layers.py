import geopandas as gpd
from pathlib import Path
import json

# Output paths
OUT_DIR = Path("/Users/james/Library/CloudStorage/GoogleDrive-jmsmuigai@gmail.com/My Drive/GARISSADRM/OUTPUT")
OUT_DIR.mkdir(parents=True, exist_ok=True)
IN_DIR = Path("/Users/james/garissa_local_workdir")

print("Loading shapefiles...")
try:
    gdf_county = gpd.read_file(IN_DIR / "garissa_county.shp")
    # Simplify if too large, but 59KB is very small
    gdf_county.to_crs(epsg=4326).to_file(OUT_DIR / "garissa_county.geojson", driver="GeoJSON")
    print("Exported garissa_county.geojson")
except Exception as e:
    print(f"Error converting garissa_county: {e}")

try:
    gdf_flood = gpd.read_file(IN_DIR / "flood_extents.shp")
    gdf_flood = gdf_flood.to_crs(epsg=4326)
    # Give it some attributes for popup
    gdf_flood['Risk_Level'] = 'Extreme'
    gdf_flood['Name'] = 'Inundated Area'
    gdf_flood.to_file(OUT_DIR / "flood_extents.geojson", driver="GeoJSON")
    print("Exported flood_extents.geojson")
except Exception as e:
    print(f"Error converting flood_extents: {e}")

# Create mock River Buffers based on a line
from shapely.geometry import LineString, Polygon
# Approximate Tana River path through Garissa
tana_line = LineString([(38.9, -0.1), (39.2, -0.3), (39.6, -0.45), (40.0, -0.8), (40.2, -1.2)])
gdf_river = gpd.GeoDataFrame(geometry=[tana_line], crs="EPSG:4326")
# Project to a metric CRS to buffer in km (e.g. 3857 or local UTM)
gdf_river_proj = gdf_river.to_crs(epsg=3857)

# Buffer 1km and 3km
buffer_1km = gdf_river_proj.buffer(1000)
buffer_3km = gdf_river_proj.buffer(3000)

gdf_buf_1 = gpd.GeoDataFrame({'Name': ['Tana River 1km Buffer'], 'Risk_Level': ['High Risk']}, geometry=buffer_1km, crs="EPSG:3857").to_crs(epsg=4326)
gdf_buf_3 = gpd.GeoDataFrame({'Name': ['Tana River 3km Buffer'], 'Risk_Level': ['Medium Risk']}, geometry=buffer_3km, crs="EPSG:3857").to_crs(epsg=4326)

gdf_buf_1.to_file(OUT_DIR / "tana_buffer_1km.geojson", driver="GeoJSON")
gdf_buf_3.to_file(OUT_DIR / "tana_buffer_3km.geojson", driver="GeoJSON")
print("Exported buffers")

# Create mock farms
# Just put a few polygons near the river
farm1 = Polygon([(39.5, -0.4), (39.52, -0.4), (39.52, -0.42), (39.5, -0.42)])
farm2 = Polygon([(39.6, -0.46), (39.62, -0.46), (39.62, -0.48), (39.6, -0.48)])
farm3 = Polygon([(39.7, -0.5), (39.72, -0.5), (39.72, -0.52), (39.7, -0.52)])

gdf_farms = gpd.GeoDataFrame({
    'Name': ['Tana Delta Farm A', 'Garissa Irrigation Scheme B', 'Mororo Agro Farm'],
    'Crop_Type': ['Maize/Sorghum', 'Mangoes/Bananas', 'Watermelons'],
    'Risk_Level': ['Extreme', 'High Risk', 'Extreme']
}, geometry=[farm1, farm2, farm3], crs="EPSG:4326")

gdf_farms.to_file(OUT_DIR / "farms_at_risk.geojson", driver="GeoJSON")
print("Exported farms_at_risk.geojson")
