#!/usr/bin/env python3
"""
Deforestation Monitoring using Google Earth Engine (Python API).
Compares NDVI between two time periods.
"""
import ee
import geemap
import argparse

def analyze_deforestation(year_start, year_end, roi_geom=None):
    try:
        ee.Initialize()
    except Exception:
        print("Earth Engine not authenticated. Run `earthengine authenticate` first.")
        return

    print(f"Analyzing Deforestation between {year_start} and {year_end}...")
    
    # Garissa Geometry (Approximate)
    if not roi_geom:
        roi = ee.Geometry.Rectangle([38.5, -2.0, 41.0, 1.0])
    
    def get_annotated_image(year):
        start = f'{year}-01-01'
        end = f'{year}-12-31'
        # Sentinel-2
        img = ee.ImageCollection('COPERNICUS/S2_SR') \
            .filterBounds(roi) \
            .filterDate(start, end) \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
            .median() \
            .clip(roi)
        return img.normalizedDifference(['B8', 'B4']).rename('NDVI')

    ndvi_start = get_annotated_image(year_start)
    ndvi_end = get_annotated_image(year_end)
    
    diff = ndvi_end.subtract(ndvi_start).rename('NDVI_Change')
    
    # Export or visualize
    # For script, we print metadata or export task
    print("Defining export task for NDVI Change map...")
    
    task = ee.batch.Export.image.toDrive(
        image=diff,
        description=f'Garissa_Deforestation_{year_start}_{year_end}',
        folder='GARISSADRM_OUTPUT',
        scale=30,
        region=roi.getInfo()['coordinates']
    )
    task.start()
    print(f"Export task started: Garissa_Deforestation_{year_start}_{year_end}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', type=int, default=2020)
    parser.add_argument('--end', type=int, default=2024)
    args = parser.parse_args()
    
    analyze_deforestation(args.start, args.end)
