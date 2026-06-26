import os
import json
import datetime
from pathlib import Path

# Target Output Directory
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "OUTPUT"
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "climate_models.json"

def fetch_climate_models():
    print("🌍 Simulating fetching ECMWF, GFS, and Kenya Met (KMD) El Niño advisory models...")
    
    # In a fully productionized system, you would hit https://meteo.go.ke/ API
    # and the Copernicus ECMWF and NOAA GFS APIs. For now, we simulate the 
    # specific agricultural insight parameters provided by the user.
    
    data = {
        "models": {
            "ECMWF": {
                "forecast": "Heavy catastrophic flooding expected October-January, and March-May.",
                "confidence": "High",
                "precipitation_anomaly": "+1200mm"
            },
            "GFS": {
                "forecast": "Monster El Niño drought globally (affecting Australian/Russian wheat), but localized flooding in East Africa.",
                "confidence": "High"
            },
            "KMD": {
                "source": "Kenya Meteorological Department",
                "advisory": "Extreme river swelling. Laghas to overflow. River Tana communities must evacuate banks."
            }
        },
        "agricultural_advisory": {
            "vegetables": {
                "crops": ["Terere", "Cabbages", "Spinach", "Managu"],
                "prediction": "Flood of relentless supply with low demand. Prices will stay down from Oct to May."
            },
            "tomatoes_potatoes": {
                "crops": ["Tomatoes", "Waru/Potatoes"],
                "prediction": "Prices rise to stratosphere. Waterlogged fields and fungal diseases will decimate fields. Avoid planting in flood-prone farms."
            },
            "beans": {
                "prediction": "Heavy rains and fungal diseases will devastate early plantings. Wait out Oct/Nov rains and plant in December."
            },
            "star_performers": {
                "fruit_trees": "100% uptake if planted early October.",
                "maize": "Plant in high density under irrigation (Sept 5 - 15). 1200mm rain expected. Will produce massive yields to last through La Niña.",
                "wheat": "Local wheat (Nakuru, Narok) will mint millionaires due to global El Niño drought affecting Russian/Australian supply."
            }
        },
        "health_advisory": {
            "diseases": ["Cholera", "Malaria", "Typhoid"],
            "risk_level": "CRITICAL",
            "notes": "Stagnant water in Laghas and Tana floodplains will trigger mosquito breeding and waterborne disease outbreaks."
        },
        "timestamp": datetime.datetime.now().isoformat()
    }

    # Write the data to the JSON file
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)
        
    print(f"✅ Climate models data saved to {OUTPUT_FILE}")
    return data

if __name__ == "__main__":
    fetch_climate_models()
