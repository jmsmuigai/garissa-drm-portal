#!/usr/bin/env python3
"""
Fetch diverse humanitarian datasets for Garissa from HDX using hdx-python-api.
"""
import argparse
import os
from hdx.api.configuration import Configuration
from hdx.data.dataset import Dataset

def fetch_garissa_data(output_dir='OUTPUT/hdx_data'):
    # HDX requires a user_agent but defaults often work. Best practice is to set it.
    Configuration.create(hdx_site='prod', user_agent='GarissaDRM_Bot', hdx_read_only=True)
    
    # Keyword search for Garissa
    query = 'garissa'
    print(f"Searching HDX for: {query}")
    datasets = Dataset.search_in_hdx(query)
    
    print(f"Found {len(datasets)} datasets.")
    
    os.makedirs(output_dir, exist_ok=True)
    
    count = 0
    for dataset in datasets:
        # Filter for relevant file types if needed, or just download resources
        resources = dataset.get_resources()
        for resource in resources:
            # We prefer CSV, SHP, GEOJSON
            fmt = resource.get_file_type().lower()
            if fmt in ['csv', 'shp', 'geojson', 'kml', 'zipped shapefile']:
                print(f"Downloading: {resource['name']} ({fmt}) from dataset: {dataset['title']}")
                try:
                    url, path = resource.download(folder=output_dir)
                    print(f"Saved to: {path}")
                    count += 1
                except Exception as e:
                    print(f"Failed to download {resource['name']}: {e}")
        
        if count >= 10: # Limit for demo purposes
            break
            
    print(f"Downloaded {count} files to {output_dir}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='OUTPUT/hdx_data', help='Output directory')
    args = parser.parse_args()
    
    fetch_garissa_data(args.output)
