import pandas as pd
from pathlib import Path
f = Path("GARISSA BORE HOLES/Boreholes_Export_2026-05-30.xlsx")
print("Reading file...")
df = pd.read_excel(f, engine='openpyxl')
print(df.head())
