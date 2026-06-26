"""
GARISSA DRM - QGIS GEE AUTO-LOADER SCRIPT
=========================================

INSTRUCTIONS:
1. Open QGIS.
2. Make sure the "Earth Engine Data Catalog" Plugin is installed and authenticated.
3. Open the Python Console in QGIS (Plugins -> Python Console).
4. Click the "Show Editor" button (looks like a notepad icon).
5. Paste this script into the editor and click the Green "Run" arrow.

This script will automatically:
- Connect to Google Earth Engine.
- Zoom to Garissa County.
- Load the Live Sentinel-1 Flood Radar Layer.
- Load the CHIRPS Rainfall layer.
- Apply standard color ramps so you don't have to style them manually.
"""

import ee
from ee_plugin import Map

def auto_load_garissa_layers():
    try:
        # Initialize EE
        # Note: The QGIS plugin handles authentication automatically if already logged in via plugin settings
        print("Initializing Google Earth Engine in QGIS...")
        
        # 1. Load Garissa Boundary
        print("Loading Garissa Boundary...")
        garissa = ee.FeatureCollection("FAO/GAUL/2015/level1") \
            .filter(ee.Filter.eq('ADM1_NAME', 'Garissa'))
            
        Map.centerObject(garissa, 8)
        
        empty = ee.Image().byte()
        garissa_outline = empty.paint(garissa, 1, 3)
        Map.addLayer(garissa_outline, {'palette': ['00f3ff']}, 'Garissa Border', True)

        # 2. Load CHIRPS Rainfall (Last 30 Days)
        print("Loading CHIRPS Rainfall (30-day cumulative)...")
        today = ee.Date(ee.Date.now())
        last_month = today.advance(-30, 'day')

        chirps = ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY") \
            .filterBounds(garissa) \
            .filterDate(last_month, today) \
            .sum() \
            .clip(garissa)

        rain_vis = {'min': 0, 'max': 200, 'palette': ['#001a33', '#004080', '#00f3ff', '#39ff14', '#ffd700']}
        Map.addLayer(chirps, rain_vis, '30-Day Rainfall (CHIRPS)', False)

        # 3. Load Sentinel-1 Floods (Live Radar)
        print("Loading Sentinel-1 Flood Extents...")
        sentinel1 = ee.ImageCollection('COPERNICUS/S1_GRD') \
            .filterBounds(garissa) \
            .filterDate(last_month, today) \
            .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV')) \
            .filter(ee.Filter.eq('instrumentMode', 'IW')) \
            .select('VV') \
            .mosaic() \
            .clip(garissa)

        # Mask out very low backscatter (water)
        water_mask = sentinel1.lt(-16)
        flood_vis = {'min': 0, 'max': 1, 'palette': ['000000', 'ff007f']}
        
        Map.addLayer(water_mask.updateMask(water_mask), flood_vis, 'Sentinel-1 Floods (Live)', False)

        # 4. Load Population Density (WorldPop)
        print("Loading Population Density...")
        worldpop = ee.ImageCollection("WorldPop/GP/100m/pop") \
            .filter(ee.Filter.eq('country', 'KEN')) \
            .mosaic() \
            .clip(garissa)
        pop_vis = {'min': 0, 'max': 50, 'palette': ['#000000', '#2d004b', '#542788', '#8073ac', '#b2abd2', '#fdb863', '#e08214', '#b35806']}
        Map.addLayer(worldpop, pop_vis, 'Population Density', False)

        # 5. Load Elevation (SRTM)
        print("Loading Elevation Data...")
        elevation = ee.Image("USGS/SRTMGL1_003").clip(garissa)
        ele_vis = {'min': 0, 'max': 500, 'palette': ['blue', 'green', 'yellow', 'red']}
        Map.addLayer(elevation, ele_vis, 'Elevation (SRTM)', False)

        print("✅ SUCCESS! All GEE layers loaded successfully.")

    except Exception as e:
        print(f"❌ ERROR: Failed to load layers. Details: {e}")

# Run the function
auto_load_garissa_layers()
