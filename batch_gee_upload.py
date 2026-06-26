#!/usr/bin/env python3
"""
Batch Upload Script for Google Earth Engine Assets
Automatically uploads all shapefiles to GEE with organized naming
"""
import ee
from pathlib import Path
import subprocess
import time
import json
from google.cloud import storage


class GEEBatchUploader:
    """Automated batch uploader for GEE assets"""
    
    def __init__(self, project_root, gcs_bucket=None):
        """
        Initialize batch uploader
        
        Args:
            project_root: Root directory containing shapefiles
            gcs_bucket: Google Cloud Storage bucket for staging (optional)
        """
        self.project_root = Path(project_root)
        self.gcs_bucket = gcs_bucket
        self.asset_mapping = {}
        
        # Initialize EE
        try:
            ee.Initialize()
            print("✅ Earth Engine initialized")
        except:
            print("⚠️  Authenticating Earth Engine...")
            ee.Authenticate()
            ee.Initialize()
            print("✅ Earth Engine authenticated")
    
    def discover_shapefiles(self):
        """Discover all shapefiles in the project directory"""
        shapefiles = []
        
        # Find all .shp files
        for shp_file in self.project_root.rglob("*.shp"):
            # Skip if it's in a hidden directory or temp directory
            if any(part.startswith('.') for part in shp_file.parts):
                continue
            
            # Get required shapefile components
            base_path = shp_file.with_suffix('')
            required_files = [
                shp_file,  # .shp
                base_path.with_suffix('.shx'),  # .shx
                base_path.with_suffix('.dbf'),  # .dbf
            ]
            
            # Check if all required files exist
            if all(f.exists() for f in required_files):
                shapefiles.append({
                    'shp': shp_file,
                    'base': base_path,
                    'name': shp_file.stem,
                    'relative_path': shp_file.relative_to(self.project_root)
                })
        
        print(f"📁 Discovered {len(shapefiles)} complete shapefiles")
        return shapefiles
    
    def generate_asset_id(self, shapefile_info, username="jmsmuigai"):
        """
        Generate GEE asset ID with organized naming
        
        Args:
            shapefile_info: Dictionary with shapefile metadata
            username: GEE username
            
        Returns:
            Asset ID string
        """
        # Create organized folder structure
        relative_path = shapefile_info['relative_path']
        parent_folder = relative_path.parent.name if relative_path.parent.name != '.' else 'root'
        
        # Clean folder name
        folder_clean = parent_folder.lower().replace(' ', '_').replace('-', '_')
        
        # Clean filename
        name_clean = shapefile_info['name'].lower().replace(' ', '_').replace('-', '_')
        
        asset_id = f"users/{username}/garissa/{folder_clean}/{name_clean}"
        
        return asset_id
    
    def upload_to_gee_cli(self, shapefile_info, asset_id):
        """
        Upload shapefile to GEE using command line tool
        
        Args:
            shapefile_info: Dictionary with shapefile metadata
            asset_id: GEE asset ID
            
        Returns:
            Boolean success status
        """
        shp_path = shapefile_info['shp']
        
        print(f"\n📤 Uploading: {shapefile_info['name']}")
        print(f"   Asset ID: {asset_id}")
        
        # Build earthengine upload command
        cmd = [
            'earthengine', 'upload', 'table',
            '--asset_id', asset_id,
            str(shp_path)
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                print(f"   ✅ Upload initiated successfully")
                return True
            else:
                print(f"   ❌ Upload failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"   ⏱️  Upload timed out")
            return False
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
    
    def batch_upload_all(self, dry_run=False):
        """
        Upload all discovered shapefiles to GEE
        
        Args:
            dry_run: If True, only print what would be uploaded
        """
        print("\n" + "="*70)
        print("🚀 BATCH GEE ASSET UPLOAD")
        print("="*70)
        
        shapefiles = self.discover_shapefiles()
        
        if not shapefiles:
            print("❌ No shapefiles found")
            return
        
        # Priority shapefiles (upload first)
        priority_names = ['garissa_county', 'dadaab', 'hagadera', 'dagahaley', 'ifo', 'schools', 'health']
        
        # Sort: priority first, then alphabetically
        shapefiles.sort(key=lambda x: (
            not any(p in x['name'].lower() for p in priority_names),
            x['name'].lower()
        ))
        
        results = {'success': [], 'failed': [], 'skipped': []}
        
        print(f"\n📋 Upload Plan ({len(shapefiles)} files):")
        for i, shp_info in enumerate(shapefiles, 1):
            asset_id = self.generate_asset_id(shp_info)
            print(f"   {i}. {shp_info['name']} → {asset_id}")
            self.asset_mapping[shp_info['name']] = asset_id
        
        if dry_run:
            print("\n🔍 DRY RUN - No uploads performed")
            return results
        
        # Confirm upload
        print("\n⚠️  This will upload all files to Google Earth Engine")
        confirm = input("Continue? (yes/no): ").strip().lower()
        
        if confirm != 'yes':
            print("❌ Upload cancelled")
            return results
        
        # Perform uploads
        print("\n🚀 Starting uploads...\n")
        for i, shp_info in enumerate(shapefiles, 1):
            asset_id = self.generate_asset_id(shp_info)
            
            print(f"[{i}/{len(shapefiles)}] ", end='')
            success = self.upload_to_gee_cli(shp_info, asset_id)
            
            if success:
                results['success'].append(shp_info['name'])
            else:
                results['failed'].append(shp_info['name'])
            
            # Rate limiting - wait between uploads
            if i < len(shapefiles):
                time.sleep(2)
        
        # Save asset mapping
        mapping_file = self.project_root / "gee_asset_mapping.json"
        with open(mapping_file, 'w') as f:
            json.dump(self.asset_mapping, f, indent=2)
        
        print("\n" + "="*70)
        print("📊 UPLOAD SUMMARY")
        print("="*70)
        print(f"✅ Successful: {len(results['success'])}")
        print(f"❌ Failed: {len(results['failed'])}")
        print(f"📋 Asset mapping saved to: {mapping_file}")
        print("="*70)
        
        if results['failed']:
            print("\n❌ Failed uploads:")
            for name in results['failed']:
                print(f"   - {name}")
        
        return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Batch upload shapefiles to Google Earth Engine')
    parser.add_argument('--project-root', type=str, default='.',
                       help='Project root directory containing shapefiles')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show upload plan without actually uploading')
    parser.add_argument('--bucket', type=str, help='GCS bucket for staging (optional)')
    
    args = parser.parse_args()
    
    uploader = GEEBatchUploader(
        project_root=args.project_root,
        gcs_bucket=args.bucket
    )
    
    uploader.batch_upload_all(dry_run=args.dry_run)
