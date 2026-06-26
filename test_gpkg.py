import geopandas as gpd
from pathlib import Path
b = gpd.read_file("OUTPUT/Buffered Disolved Floods.gpkg")
l = gpd.read_file("OUTPUT/LOW RISK FLOODS AREA.gpkg")
print("Buffered:", len(b))
print("Low:", len(l))
