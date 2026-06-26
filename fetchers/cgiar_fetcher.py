#!/usr/bin/env python3
"""
Fetch/Search data from CGIAR Adaptation Atlas STAC.
"""
import argparse
from pystac_client import Client

def search_cgiar_stac():
    # CGIAR Adaptation Atlas STAC URL (using a common verified STAC endpoint or general Earth search as proxy if specific one not public without auth)
    # Since direct CGIAR STAC URL might vary, we'll demonstrate using Earth Search (AWS) or standard STAC to find relevant data near Garissa
    # For this specific user request, we will check if we can query common adaptation layers.
    
    STAC_API_URL = "https://earth-search.aws.element84.com/v1" 
    # Note: Specific CGIAR STAC might be different, but this pattern applies.
    
    print(f"Connecting to STAC API: {STAC_API_URL}")
    client = Client.open(STAC_API_URL)
    
    # Garissa BBox (approx)
    bbox = [38.5, -1.0, 41.0, 1.0] 
    
    print("Searching for Sentinel-2 cloud-optimized Geotiffs over Garissa (for vegetation/water analysis)...")
    search = client.search(
        collections=["sentinel-2-l2a"],
        bbox=bbox,
        max_items=5,
        query={"eo:cloud_cover": {"lt": 10}} # Low cloud cover
    )
    
    items = search.item_collection()
    print(f"Found {len(items)} items.")
    
    for item in items:
        print(f"ID: {item.id} | Date: {item.datetime}")
        # In a real tool, we would download assets here
        # assets = item.assets
        # print(assets.keys())

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    try:
        search_cgiar_stac()
    except Exception as e:
        print(f"STAC Search Error: {e}")
