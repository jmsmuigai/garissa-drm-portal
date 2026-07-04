import json
from pathlib import Path
OUTPUT_DIR = Path('/Users/james/Library/CloudStorage/GoogleDrive-jmsmuigai@gmail.com/My Drive/GARISSADRM/OUTPUT')
def load_geojson(path):
    print("Loading", path)
    if not path.exists(): return None
    with open(path, encoding='utf-8') as f:
        return json.load(f)

load_geojson(OUTPUT_DIR / 'schools_risk_assessed.geojson')
load_geojson(OUTPUT_DIR / 'schools_at_risk.geojson')
load_geojson(OUTPUT_DIR / 'health_facilities_risk_assessed.geojson')
load_geojson(OUTPUT_DIR / 'health_facilities_at_risk.geojson')
load_geojson(OUTPUT_DIR / 'Cleaned_Garissa_Boreholes.geojson')
print("All loaded!")
