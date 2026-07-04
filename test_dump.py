import json
from pathlib import Path
OUTPUT_DIR = Path('/Users/james/Library/CloudStorage/GoogleDrive-jmsmuigai@gmail.com/My Drive/GARISSADRM/OUTPUT')
def load_geojson(path):
    if not path.exists(): return None
    with open(path, encoding='utf-8') as f:
        return json.load(f)

print("Loading...", flush=True)
camps_data = load_geojson(OUTPUT_DIR / 'idp_camps_risk_assessed.geojson')
dagahaley = load_geojson(OUTPUT_DIR / 'Dagahaley.geojson')
print("Loaded.", flush=True)

print("Dumping...", flush=True)
json.dumps(camps_data)
json.dumps(dagahaley)
print("Dumped.", flush=True)

print("Replacing...", flush=True)
HTML = "A" * 10_000_000
HTML = HTML.replace("A", "B")
print("Replaced.", flush=True)
