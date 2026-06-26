#!/usr/bin/env python3
"""
Garissa Sentinel - Digital Twin for Ecological Security
Main analysis engine for satellite-based environmental monitoring
"""
import ee
import geemap
import pandas as pd
import geopandas as gpd
from datetime import datetime
from pathlib import Path
import json
import sys
from tqdm import tqdm

# Import local modules
from geofencing_engine import GeofencingEngine
from gemini_advisor import GeminiAdvisor

class GarissaSentinel:
    """Main orchestration class for Garissa environmental monitoring"""
    
    def __init__(self, project_root=None, test_mode=False):
        """
        Initialize the Garissa Sentinel system
        
        Args:
            project_root: Root directory of the project
            test_mode: If True, uses smaller date ranges for testing
        """
        self.project_root = Path(project_root) if project_root else Path(__file__).parent
        self.test_mode = test_mode
        self.output_dir = self.project_root / "OUTPUT"
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize Earth Engine
        self._initialize_gee()
        
        # Load local shapefiles
        self.local_assets = self._load_local_assets()
        
        print("✅ Garissa Sentinel initialized successfully")
    
    def _initialize_gee(self):
        """Initialize Google Earth Engine with proper authentication"""
        try:
            ee.Initialize()
            print("✅ Google Earth Engine authenticated")
        except Exception as e:
            print(f"⚠️  GEE not authenticated. Attempting authentication...")
            try:
                ee.Authenticate()
                ee.Initialize()
                print("✅ GEE authentication successful")
            except Exception as auth_error:
                print(f"❌ GEE authentication failed: {auth_error}")
                print("Please run: earthengine authenticate")
                if not self.test_mode:
                    sys.exit(1)
    
    def _load_local_assets(self):
        """Load local shapefiles from the project directory"""
        assets = {}
        
        try:
            # Load Dadaab camp blocks
            camp_blocks = []
            camp_dir = self.project_root / "Daadab_camp_blocks"
            for shp_file in camp_dir.glob("*.shp"):
                gdf = gpd.read_file(shp_file)
                gdf['camp_name'] = shp_file.stem
                camp_blocks.append(gdf)
            
            if camp_blocks:
                assets['refugee_camps'] = pd.concat(camp_blocks, ignore_index=True)
                print(f"✅ Loaded {len(camp_blocks)} camp block shapefiles")
            
            # Load Garissa County boundary
            county_file = self.project_root / "garissa_county.shp"
            if county_file.exists():
                assets['garissa_boundary'] = gpd.read_file(county_file)
                print("✅ Loaded Garissa County boundary")
            
            # Load Schools
            schools_file = self.project_root / "Garissa Schools" / "garissa_schools.shp"
            if schools_file.exists():
                assets['schools'] = gpd.read_file(schools_file)
                print("✅ Loaded Garissa Schools")
            
            # Load Health Facilities
            health_file = self.project_root / "Garissa Health Facilities" / "garissa_health_facilities.shp"
            if health_file.exists():
                assets['health_facilities'] = gpd.read_file(health_file)
                print("✅ Loaded Health Facilities")
                
        except Exception as e:
            print(f"⚠️  Warning loading local assets: {e}")
        
        return assets
    
    def get_greenness(self, geometry, start_date, end_date, name="region"):
        """
        Calculate NDVI (Normalized Difference Vegetation Index) for a region
        
        Args:
            geometry: GEE geometry or GeoDataFrame
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            name: Region name for logging
            
        Returns:
            NDVI image clipped to geometry
        """
        # Convert GeoDataFrame to GEE geometry if needed
        if isinstance(geometry, gpd.GeoDataFrame):
            geometry = geemap.geopandas_to_ee(geometry)
        
        print(f"📡 Fetching Sentinel-2 imagery for {name} ({start_date} to {end_date})...")
        
        # Fetch Sentinel-2 data
        dataset = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
                  .filterDate(start_date, end_date) \
                  .filterBounds(geometry) \
                  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
                  .median()
        
        # Calculate NDVI: (NIR - Red) / (NIR + Red)
        # Band 8 = NIR, Band 4 = Red
        ndvi = dataset.normalizedDifference(['B8', 'B4']).rename('NDVI')
        
        return ndvi.clip(geometry)
    
    def analyze_deforestation(self):
        """
        Detect deforestation and land degradation around refugee camps
        Compares vegetation health between two time periods
        """
        print("\n" + "="*60)
        print("🌳 DEFORESTATION ANALYSIS")
        print("="*60)
        
        if 'refugee_camps' not in self.local_assets:
            print("❌ No refugee camp data loaded")
            return None
        
        camps_gdf = self.local_assets['refugee_camps']
        
        # Define time periods
        if self.test_mode:
            start_date_old = '2024-11-01'
            end_date_old = '2024-12-31'
            start_date_new = '2025-01-01'
            end_date_new = datetime.now().strftime('%Y-%m-%d')
        else:
            start_date_old = '2024-01-01'
            end_date_old = '2024-12-31'
            start_date_new = '2025-01-01'
            end_date_new = datetime.now().strftime('%Y-%m-%d')
        
        # Create 5km buffer around camps
        camps_buffered = camps_gdf.copy()
        camps_buffered['geometry'] = camps_buffered.geometry.buffer(0.05)  # ~5km in degrees
        
        # Convert to EE FeatureCollection
        camps_ee = geemap.geopandas_to_ee(camps_buffered)
        camps_geometry = camps_ee.geometry()
        
        # Calculate NDVI for both periods
        ndvi_old = self.get_greenness(camps_geometry, start_date_old, end_date_old, "Camps 2024")
        ndvi_new = self.get_greenness(camps_geometry, start_date_new, end_date_new, "Camps 2025")
        
        # Calculate change (negative = vegetation loss)
        ndvi_change = ndvi_new.subtract(ndvi_old).rename('NDVI_Change')
        
        print("📊 Extracting statistics per camp block...")
        
        # Extract statistics for each camp block
        stats = ndvi_change.reduceRegions(
            collection=camps_ee,
            reducer=ee.Reducer.mean().combine(
                reducer2=ee.Reducer.stdDev(),
                sharedInputs=True
            ).combine(
                reducer2=ee.Reducer.min(),
                sharedInputs=True
            ).combine(
                reducer2=ee.Reducer.max(),
                sharedInputs=True
            ),
            scale=30
        ).getInfo()
        
        # Convert to DataFrame
        features = stats['features']
        records = []
        for feat in features:
            props = feat['properties']
            props['geometry_type'] = feat.get('geometry', {}).get('type', '')
            records.append(props)
        
        df = pd.DataFrame(records)
        
        # Save results
        output_file = self.output_dir / "garissa_camp_health.csv"
        df.to_csv(output_file, index=False)
        print(f"💾 Saved results to {output_file}")
        
        # Summary statistics
        if 'mean' in df.columns:
            avg_change = df['mean'].mean()
            print(f"\n📈 Average NDVI Change: {avg_change:.4f}")
            if avg_change < -0.05:
                print("⚠️  WARNING: Significant vegetation loss detected!")
            elif avg_change < 0:
                print("⚠️  Moderate vegetation decline")
            else:
                print("✅ Vegetation stable or improving")
        
        return df
    
    def identify_safe_grazing_zones(self):
        """
        Identify safe grazing zones based on:
        1. Good vegetation health (NDVI > 0.3)
        2. Low population density (< 10 people/km²)
        """
        print("\n" + "="*60)
        print("🐄 SAFE GRAZING ZONE IDENTIFICATION")
        print("="*60)
        
        if 'garissa_boundary' not in self.local_assets:
            print("❌ No Garissa boundary data loaded")
            return None
        
        boundary_gdf = self.local_assets['garissa_boundary']
        boundary_ee = geemap.geopandas_to_ee(boundary_gdf)
        boundary_geom = boundary_ee.geometry()
        
        # Get recent NDVI
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now().replace(month=max(1, datetime.now().month-3))).strftime('%Y-%m-%d')
        
        print(f"📡 Analyzing vegetation for {start_date} to {end_date}...")
        ndvi_recent = self.get_greenness(boundary_geom, start_date, end_date, "Garissa County")
        
        # Get population density from WorldPop
        print("📡 Fetching population density data...")
        pop_density = ee.ImageCollection("WorldPop/GP/100m/pop") \
                       .filterDate('2020-01-01', '2021-01-01') \
                       .first() \
                       .clip(boundary_geom)
        
        # Identify safe zones: NDVI > 0.3 AND population < 10
        safe_zones = ndvi_recent.gt(0.3).And(pop_density.unmask(0).lt(10))
        
        # Convert to vectors for export
        print("🗺️  Converting raster to vector polygons...")
        safe_zones_vectors = safe_zones.selfMask().reduceToVectors(
            geometry=boundary_geom,
            scale=100,
            geometryType='polygon',
            maxPixels=1e9
        )
        
        # Initialize geofencing engine for multi-format export
        print("📦 Generating geofencing exports...")
        geofencing = GeofencingEngine(self.output_dir)
        
        # Export in multiple formats
        zone_data = safe_zones_vectors.getInfo()
        geofencing.export_all_formats(zone_data, 'safe_grazing_zones')
        
        return safe_zones_vectors
    
    def generate_ai_advisory(self, camp_health_df):
        """
        Generate AI-powered environmental advisory using Gemini
        
        Args:
            camp_health_df: DataFrame with camp health statistics
        """
        print("\n" + "="*60)
        print("🤖 GEMINI AI ADVISORY")
        print("="*60)
        
        if camp_health_df is None or camp_health_df.empty:
            print("❌ No data available for AI analysis")
            return
        
        advisor = GeminiAdvisor(api_key="AIzaSyDDZludrLe0owCB3jFvPWSp8b3ZBx5hBmQ")
        
        # Generate comprehensive report
        report = advisor.generate_advisory_report(camp_health_df)
        
        # Save report
        report_file = self.output_dir / "AI_ADVISORY_REPORT.md"
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(f"💾 AI Advisory saved to {report_file}")
        
        # Generate SMS alerts
        sms_alerts = advisor.generate_sms_alerts(camp_health_df)
        
        if sms_alerts:
            sms_file = self.output_dir / "SMS_ALERTS.txt"
            with open(sms_file, 'w') as f:
                for alert in sms_alerts:
                    f.write(alert + "\n\n")
            print(f"📱 SMS Alerts saved to {sms_file}")
    
    def run_full_pipeline(self):
        """Execute the complete analysis pipeline"""
        print("\n" + "="*70)
        print("🌍 GARISSA SENTINEL - DIGITAL TWIN FOR ECOLOGICAL SECURITY")
        print("="*70)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Mode: {'TEST' if self.test_mode else 'PRODUCTION'}")
        print("="*70 + "\n")
        
        try:
            # Step 1: Deforestation Analysis
            camp_health = self.analyze_deforestation()
            
            # Step 2: Safe Grazing Zones
            safe_zones = self.identify_safe_grazing_zones()
            
            # Step 3: AI Advisory
            if camp_health is not None:
                self.generate_ai_advisory(camp_health)
            
            print("\n" + "="*70)
            print("✅ PIPELINE COMPLETED SUCCESSFULLY")
            print("="*70)
            print(f"Outputs saved to: {self.output_dir}")
            print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        except Exception as e:
            print(f"\n❌ Pipeline failed: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Garissa Sentinel - Environmental Monitoring System')
    parser.add_argument('--test-mode', action='store_true', help='Run in test mode with smaller date ranges')
    parser.add_argument('--project-root', type=str, help='Project root directory', default=None)
    
    args = parser.parse_args()
    
    sentinel = GarissaSentinel(project_root=args.project_root, test_mode=args.test_mode)
    sentinel.run_full_pipeline()
