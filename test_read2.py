import pandas as pd
from pathlib import Path
f = Path("GARISSA BORE HOLES/Boreholes_Export_2026-05-30.xlsx")
print("Reading file with calamine...")
df = pd.read_excel(f, engine='calamine')
print(df.head())
