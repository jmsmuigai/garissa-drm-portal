#!/usr/bin/env python3
"""
Join Borehole Status Data with Safe Grazing Zone Maps
This script performs a spatial join between safe grazing zones and borehole locations.
"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from pathlib import Path

def join_boreholes_to_grazing_zones(boreholes_file, grazing_zones_file, output_file):
    """
    Perform a spatial join between boreholes and safe grazing zones.
    
    Args:
        boreholes_file (str or Path): Path to the borehole CSV or Excel file.
        grazing_zones_file (str or Path): Path to the safe grazing zones GeoJSON/Shapefile.
        output_file (str or Path): Path to save the joined output for dashboards.
    """
    print(f"🔄 Loading safe grazing zones from {grazing_zones_file}...")
    try:
        # Load grazing zones
        grazing_zones = gpd.read_file(grazing_zones_file)
        # Ensure it has a coordinate reference system (CRS) set to WGS84
        if grazing_zones.crs is None:
            grazing_zones = grazing_zones.set_crs(epsg=4326)
        else:
            grazing_zones = grazing_zones.to_crs(epsg=4326)
    except Exception as e:
        print(f"❌ Error loading grazing zones: {e}")
        return

    print(f"🔄 Loading borehole data from {boreholes_file}...")
    try:
        # Check file extension to load CSV or Excel
        file_path_str = str(boreholes_file)
        if file_path_str.endswith('.xlsx') or file_path_str.endswith('.xls'):
            boreholes_df = pd.read_excel(boreholes_file)
        else:
            boreholes_df = pd.read_csv(boreholes_file)
        
        # We assume columns 'longitude' and 'latitude' (or similar) exist.
        # Let's standardize column names for simplicity (convert to lowercase)
        boreholes_df.columns = [c.lower() for c in boreholes_df.columns]
        
        lon_col = 'longitude' if 'longitude' in boreholes_df.columns else 'lon'
        lat_col = 'latitude' if 'latitude' in boreholes_df.columns else 'lat'
        
        if lon_col not in boreholes_df.columns or lat_col not in boreholes_df.columns:
            print("❌ Error: Could not find longitude/latitude columns in borehole data.")
            print(f"   Available columns: {list(boreholes_df.columns)}")
            return
            
        # Convert to GeoDataFrame
        geometry = [Point(xy) for xy in zip(boreholes_df[lon_col], boreholes_df[lat_col])]
        boreholes_gdf = gpd.GeoDataFrame(boreholes_df, geometry=geometry, crs="EPSG:4326")
    except Exception as e:
        print(f"❌ Error loading borehole data: {e}")
        return

    print("🔄 Performing spatial join...")
    try:
        # Spatial join: Find boreholes that intersect with safe grazing zones
        # how='left' keeps all boreholes, how='inner' keeps only those in zones
        joined_data = gpd.sjoin(boreholes_gdf, grazing_zones, how="left", predicate="intersects")
        
        # If 'index_right' is not null, it means the borehole is inside a safe grazing zone
        joined_data['in_safe_zone'] = joined_data['index_right'].notnull()
        
        # Drop the spatial index column
        joined_data = joined_data.drop(columns=['index_right'])
        
        # Export the result
        print(f"💾 Saving joined data to {output_file}...")
        
        # Save to CSV for Looker Studio
        if str(output_file).endswith('.csv'):
            joined_data.drop(columns=['geometry']).to_csv(output_file, index=False)
        else:
            joined_data.to_file(output_file)
            
        print("✅ Spatial join completed successfully!")
        
        # Summary statistics
        total_boreholes = len(joined_data)
        safe_zone_boreholes = joined_data['in_safe_zone'].sum()
        print(f"📊 Summary: {safe_zone_boreholes} out of {total_boreholes} boreholes are within safe grazing zones.")
        
    except Exception as e:
        print(f"❌ Error during spatial join: {e}")

if __name__ == "__main__":
    # Example usage based on the Garissa Sentinel framework structure
    base_dir = Path(__file__).parent
    
    # Paths (adjust as necessary)
    boreholes_input = base_dir / "Boreholes_Export_2026-05-30.xlsx"  # Or .csv
    grazing_zones_input = base_dir / "OUTPUT" / "safe_grazing_zones.geojson" # Or .shp
    output_csv = base_dir / "OUTPUT" / "looker_boreholes_grazing_join.csv"
    
    # Create OUTPUT dir if it doesn't exist
    (base_dir / "OUTPUT").mkdir(exist_ok=True)
    
    print("🚀 Starting Borehole - Grazing Zone Integration...")
    join_boreholes_to_grazing_zones(boreholes_input, grazing_zones_input, output_csv)
