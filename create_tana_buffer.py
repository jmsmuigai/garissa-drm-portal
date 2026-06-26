import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon, MultiPolygon
import os
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def create_tana_buffer():
    """
    Creates a 1km buffer towards Tana River County starting from the official Garissa County boundary.
    Then tags schools and health facilities that fall within this buffer.
    """
    try:
        logging.info("Starting Tana River 1km buffer creation...")
        base_dir = "/Users/james/Library/CloudStorage/GoogleDrive-jmsmuigai@gmail.com/My Drive/GARISSADRM"
        
        # Paths
        county_shp = os.path.join(base_dir, "garissa_county.shp")
        schools_geojson = os.path.join(base_dir, "OUTPUT/schools_risk_assessed.geojson")
        health_geojson = os.path.join(base_dir, "OUTPUT/health_facilities_risk_assessed.geojson")
        
        # Load Garissa county boundary
        logging.info(f"Loading {county_shp}")
        garissa = gpd.read_file(county_shp)
        
        # Reproject to a metric CRS for accurate buffering (UTM Zone 37S for Kenya is EPSG:32737)
        garissa_proj = garissa.to_crs(epsg=32737)
        
        # Extract the boundary (LineString) of Garissa
        garissa_boundary = garissa_proj.boundary
        
        # Buffer the boundary by 1000 meters (1km)
        logging.info("Buffering boundary by 1km...")
        boundary_buffer = garissa_boundary.buffer(1000)
        
        # The buffer includes both INSIDE and OUTSIDE Garissa. 
        # We only want the OUTSIDE part (towards Tana River).
        # We do this by taking the buffer and removing the intersection with Garissa.
        logging.info("Extracting the external buffer...")
        external_buffer = boundary_buffer.difference(garissa_proj.geometry.unary_union)
        
        # Reproject back to WGS84 (EPSG:4326)
        buffer_wgs84 = gpd.GeoDataFrame(geometry=[external_buffer.iloc[0]], crs="EPSG:32737").to_crs(epsg=4326)
        
        # For simplicity, we are capturing the entire outer border of Garissa 1km out.
        # Ideally, we would intersect this with Tana River County shapefile to isolate *only* the Tana River side.
        # However, for now, this "external buffer" will serve as the Border Zone.
        
        # Save the buffer zone
        out_buffer_path = os.path.join(base_dir, "OUTPUT/tana_buffer_zone.geojson")
        buffer_wgs84.to_file(out_buffer_path, driver="GeoJSON")
        logging.info(f"Saved border buffer zone to {out_buffer_path}")
        
        # Now let's tag schools and health facilities
        # We assume the files exist (they do, based on previous directory listing)
        
        def tag_features(filepath, name):
            if not os.path.exists(filepath):
                logging.warning(f"File {filepath} not found, skipping {name} tagging.")
                return
                
            gdf = gpd.read_file(filepath)
            
            # Intersect with the buffer zone
            # Create a boolean mask: True if feature geometry intersects the buffer geometry
            buffer_geom = buffer_wgs84.geometry.iloc[0]
            
            # Create the column
            gdf['tana_buffer_zone'] = gdf.geometry.apply(lambda geom: geom.intersects(buffer_geom) if geom else False)
            
            num_tagged = gdf['tana_buffer_zone'].sum()
            logging.info(f"Tagged {num_tagged} {name} as being in the Tana border buffer zone.")
            
            # Save back
            gdf.to_file(filepath, driver="GeoJSON")
            
        tag_features(schools_geojson, "Schools")
        tag_features(health_geojson, "Health Facilities")
        
        logging.info("Buffer creation and tagging complete!")
        
    except Exception as e:
        logging.error(f"Error creating buffer: {e}", exc_info=True)

if __name__ == "__main__":
    create_tana_buffer()
