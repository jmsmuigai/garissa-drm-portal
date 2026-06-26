#!/usr/bin/env python3
"""
Enhanced Looker Studio Export Script for Garissa Sentinel
Exports analysis results in formats ready for Looker Studio dashboards
"""
import pandas as pd
from pathlib import Path
import json
from datetime import datetime


def export_for_looker(output_dir='OUTPUT'):
    """
    Export Garissa Sentinel outputs in Looker Studio-ready format
    
    Args:
        output_dir: Directory containing analysis outputs
    """
    output_path = Path(output_dir)
    
    print("="*70)
    print("📊 LOOKER STUDIO EXPORT")
    print("="*70)
    
    # 1. Camp Health Statistics (Primary Dashboard)
    camp_health_file = output_path / 'garissa_camp_health.csv'
    if camp_health_file.exists():
        df_health = pd.read_csv(camp_health_file)
        
        # Add computed columns
        df_health['analysis_date'] = datetime.now().strftime('%Y-%m-%d')
        df_health['degradation_level'] = df_health['mean'].apply(
            lambda x: 'Critical' if x < -0.1 else ('Moderate' if x < -0.05 else ('Stable' if x < 0 else 'Improving'))
        )
        df_health['alert_status'] = df_health['mean'].apply(
            lambda x: '🔴' if x < -0.1 else ('🟡' if x < 0 else '🟢')
        )
        
        # Save enhanced version
        enhanced_file = output_path / 'looker_camp_dashboard.csv'
        df_health.to_csv(enhanced_file, index=False)
        print(f"✅ Exported: {enhanced_file}")
        print(f"   - Rows: {len(df_health)}")
        print(f"   - Columns: {list(df_health.columns)}")
    
    # 2. Safe Grazing Zones Summary
    geojson_file = output_path / 'safe_grazing_zones.geojson'
    if geojson_file.exists():
        with open(geojson_file) as f:
            zones_geojson = json.load(f)
        
        # Extract zone statistics
        zone_records = []
        for i, feat in enumerate(zones_geojson.get('features', [])):
            coords = feat['geometry']['coordinates'][0]
            # Calculate approximate centroid
            avg_lon = sum(c[0] for c in coords) / len(coords)
            avg_lat = sum(c[1] for c in coords) / len(coords)
            
            zone_records.append({
                'zone_id': i + 1,
                'centroid_lat': avg_lat,
                'centroid_lon': avg_lon,
                'num_vertices': len(coords),
                'quality': 'Good',
                'generated_date': datetime.now().strftime('%Y-%m-%d')
            })
        
        df_zones = pd.DataFrame(zone_records)
        zones_file = output_path / 'looker_safe_zones.csv'
        df_zones.to_csv(zones_file, index=False)
        print(f"✅ Exported: {zones_file}")
        print(f"   - Total zones: {len(df_zones)}")
    
    # 3. Combined Summary Statistics
    summary = {
        'analysis_date': datetime.now().strftime('%Y-%m-%d'),
        'total_camps_analyzed': len(df_health) if 'df_health' in locals() else 0,
        'critical_camps': len(df_health[df_health['mean'] < -0.1]) if 'df_health' in locals() else 0,
        'safe_zones_identified': len(zone_records) if 'zone_records' in locals() else 0,
        'avg_ndvi_change': df_health['mean'].mean() if 'df_health' in locals() else 0,
    }
    
    df_summary = pd.DataFrame([summary])
    summary_file = output_path / 'looker_summary.csv'
    df_summary.to_csv(summary_file, index=False)
    print(f"✅ Exported: {summary_file}")
    
    print("\n" + "="*70)
    print("📈 LOOKER STUDIO SETUP INSTRUCTIONS")
    print("="*70)
    print("\n1. Upload CSV files to Google Sheets:")
    print("   - looker_camp_dashboard.csv")
    print("   - looker_safe_zones.csv")
    print("   - looker_summary.csv")
    print("\n2. Open Looker Studio (https://lookerstudio.google.com)")
    print("\n3. Create Data Source → Google Sheets → Select uploaded files")
    print("\n4. Recommended visualizations:")
    print("   - Geo Chart: camp locations with color by degradation_level")
    print("   - Time Series: NDVI trends over time")
    print("   - Scorecard: Total critical camps, avg NDVI change")
    print("   - Table: Detailed camp statistics")
    print("="*70)


def export_to_bigquery(project_id, dataset_id, output_dir='OUTPUT'):
    """
    Optional: Export directly to BigQuery
    
    Args:
        project_id: GCP project ID
        dataset_id: BigQuery dataset ID
        output_dir: Directory containing outputs
    """
    from google.cloud import bigquery
    
    client = bigquery.Client(project=project_id)
    output_path = Path(output_dir)
    
    # Upload camp health data
    camp_health_file = output_path / 'garissa_camp_health.csv'
    if camp_health_file.exists():
        table_id = f"{project_id}.{dataset_id}.camp_health"
        
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=True,
        )
        
        with open(camp_health_file, "rb") as source_file:
            job = client.load_table_from_file(source_file, table_id, job_config=job_config)
        
        job.result()  # Wait for job to complete
        print(f"✅ Uploaded to BigQuery: {table_id}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Export Garissa Sentinel outputs for Looker Studio')
    parser.add_argument('--output-dir', default='OUTPUT', help='Output directory')
    parser.add_argument('--bigquery-project', help='GCP project ID for BigQuery upload (optional)')
    parser.add_argument('--bigquery-dataset', default='garissa_sentinel', help='BigQuery dataset ID')
    
    args = parser.parse_args()
    
    # Always run CSV export
    export_for_looker(args.output_dir)
     
    # Optional BigQuery upload
    if args.bigquery_project:
        print("\n📤 Uploading to BigQuery...")
        export_to_bigquery(args.bigquery_project, args.bigquery_dataset, args.output_dir)
