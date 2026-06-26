#!/usr/bin/env python3
"""
Verification Test Suite for Garissa Sentinel
Tests all components to ensure they work correctly
"""
import sys
from pathlib import Path
import subprocess


def test_imports():
    """Test that all required libraries can be imported"""
    print("="*70)
    print("TEST 1: Python Library Imports")
    print("="*70)
    
    required_modules = [
        ('ee', 'earthengine-api'),
        ('geemap', 'geemap'),
        ('geopandas', 'geopandas'),
        ('pandas', 'pandas'),
        ('google.generativeai', 'google-generativeai'),
        ('shapefile', 'pyshp'),
        ('simplekml', 'simplekml'),
    ]
    
    failures = []
    for module_name, package_name in required_modules:
        try:
            __import__(module_name)
            print(f"✅ {module_name:30} - OK")
        except ImportError:
            print(f"❌ {module_name:30} - MISSING (install: pip install {package_name})")
            failures.append(package_name)
    
    if failures:
        print(f"\n⚠️  Missing packages: {', '.join(failures)}")
        print(f"   Run: pip install {' '.join(failures)}")
        return False
    else:
        print("\n✅ All imports successful")
        return True


def test_gee_auth():
    """Test Google Earth Engine authentication"""
    print("\n" + "="*70)
    print("TEST 2: Google Earth Engine Authentication")
    print("="*70)
    
    try:
        import ee
        ee.Initialize()
        print("✅ GEE authenticated successfully")
        
        # Test a simple operation
        point = ee.Geometry.Point([40.0, 0.5])
        print(f"✅ GEE operations working (test point: {point.getInfo()})")
        return True
        
    except Exception as e:
        print(f"❌ GEE authentication failed: {e}")
        print("   Run: earthengine authenticate")
        return False


def test_gemini_api():
    """Test Gemini AI API"""
    print("\n" + "="*70)
    print("TEST 3: Gemini AI API")
    print("="*70)
    
    try:
        import google.generativeai as genai
        
        # Use API key from user's profile
        api_key = "AIzaSyDDZludrLe0owCB3jFvPWSp8b3ZBx5hBmQ"
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Say hello in exactly 3 words.")
        
        print(f"✅ Gemini API working")
        print(f"   Response: {response.text[:100]}")
        return True
        
    except Exception as e:
        print(f"❌ Gemini API failed: {e}")
        print("   Check your API key at: https://makersuite.google.com/app/apikey")
        return False


def test_shapefiles(project_root):
    """Test shapefile loading"""
    print("\n" + "="*70)
    print("TEST 4: Shapefile Loading")
    print("="*70)
    
    try:
        import geopandas as gpd
        
        test_files = [
            'garissa_county.shp',
            'Daadab_camp_blocks/Hagadera.shp',
            'Garissa Schools/garissa_schools.shp',
        ]
        
        for shp_file in test_files:
            full_path = Path(project_root) / shp_file
            if full_path.exists():
                gdf = gpd.read_file(full_path)
                print(f"✅ {shp_file:40} - {len(gdf)} features")
            else:
                print(f"⚠️  {shp_file:40} - FILE NOT FOUND")
        
        return True
        
    except Exception as e:
        print(f"❌ Shapefile loading failed: {e}")
        return False


def test_geofencing_engine():
    """Test geofencing export functions"""
    print("\n" + "="*70)
    print("TEST 5: Geofencing Engine")
    print("="*70)
    
    try:
        from geofencing_engine import GeofencingEngine
        
        # Create test data
        test_data = {
            'type': 'FeatureCollection',
            'features': [{
                'type': 'Feature',
                'geometry': {
                    'type': 'Polygon',
                    'coordinates': [[
                        [40.5, 0.5], [40.6, 0.5], 
                        [40.6, 0.6], [40.5, 0.6], [40.5, 0.5]
                    ]]
                }
            }]
        }
        
        # Test exports
        engine = GeofencingEngine(Path(__file__).parent / "OUTPUT" / "test")
        results = engine.export_all_formats(test_data, 'test_zone')
        
        print("✅ All geofencing export formats working:")
        for format_type, filepath in results.items():
            print(f"   - {format_type}: {filepath.name}")
        
        # Cleanup test files
        for filepath in results.values():
            if filepath.exists():
                filepath.unlink()
        
        return True
        
    except Exception as e:
        print(f"❌ Geofencing engine failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_main_script_syntax():
    """Test main script for syntax errors"""
    print("\n" + "="*70)
    print("TEST 6: Main Script Syntax")
    print("="*70)
    
    try:
        import garissa_sentinel_main
        print("✅ garissa_sentinel_main.py - No syntax errors")
        
        import gemini_advisor
        print("✅ gemini_advisor.py - No syntax errors")
        
        import geofencing_engine
        print("✅ geofencing_engine.py - No syntax errors")
        
        import batch_gee_upload
        print("✅ batch_gee_upload.py - No syntax errors")
        
        return True
        
    except Exception as e:
        print(f"❌ Script syntax check failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests(project_root=None):
    """Run complete test suite"""
    if project_root is None:
        project_root = Path(__file__).parent
    
    print("\n" + "="*70)
    print("🧪 GARISSA SENTINEL - VERIFICATION TEST SUITE")
    print("="*70)
    print(f"Project root: {project_root}\n")
    
    # Add project root to Python path
    sys.path.insert(0, str(project_root))
    
    results = {
        'Python Imports': test_imports(),
        'GEE Authentication': test_gee_auth(),
        'Gemini API': test_gemini_api(),
        'Shapefile Loading': test_shapefiles(project_root),
        'Geofencing Engine': test_geofencing_engine(),
        'Script Syntax': test_main_script_syntax(),
    }
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:30} - {status}")
    
    print("="*70)
    print(f"Results: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED - System ready to run!")
        print("\nNext step: Run the full pipeline:")
        print("   ./run_full_pipeline.sh")
        return 0
    else:
        print("\n⚠️  Some tests failed - please fix issues before running")
        return 1


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Garissa Sentinel Verification Tests')
    parser.add_argument('--project-root', type=str, 
                       default=str(Path(__file__).parent),
                       help='Project root directory')
    
    args = parser.parse_args()
    
    exit_code = run_all_tests(args.project_root)
    sys.exit(exit_code)
