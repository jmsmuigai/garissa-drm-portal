#!/usr/bin/env python3
"""
Simple Water Analysis Module for Garissa.
Identifies potential water pan sites based on mock slope and soil data.
"""
import numpy as np
import pandas as pd # In real life, use geopandas
import argparse

def find_water_pan_sites(dem_path=None):
    print("Loading Digital Elevation Model (DEM)...")
    # Simulation of raster analysis
    # Criteria: Slope < 5 degrees, Soil = Clay/Loam
    
    print("Calculating Slope...")
    # Mock result
    potential_sites = [
        {'lat': -0.45, 'lon': 39.65, 'score': 0.9, 'note': 'Excellent drainage, clay soil'},
        {'lat': -0.42, 'lon': 39.68, 'score': 0.85, 'note': 'Good catchment area'},
        {'lat': -0.50, 'lon': 39.60, 'score': 0.7, 'note': 'Sandy loam, requires lining'}
    ]
    
    print("Potential Water Pan Sites Identified:")
    df = pd.DataFrame(potential_sites)
    print(df)
    
    output = 'OUTPUT/water_pan_sites.csv'
    df.to_csv(output, index=False)
    print(f"Saved sites to {output}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dem', help='Path to DEM file')
    args = parser.parse_args()
    
    find_water_pan_sites(args.dem)
