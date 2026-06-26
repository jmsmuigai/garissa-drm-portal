import json

path = "garissa_elnino_flood_risk.ipynb"
with open(path, "r") as f:
    notebook = json.load(f)

for cell in notebook['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        for i, line in enumerate(source):
            if "elif gdf.crs.to_string() != target_crs:" in line:
                # Need to insert code a few lines down
                # Find the line with `print(f"  ✅ {name}: {len(gdf)} features")`
                for j in range(i, len(source)):
                    if "print(f\"  ✅ {name}: {len(gdf)} features\")" in source[j]:
                        source.insert(j, "        # Convert timestamp columns to strings for JSON serialization\n")
                        source.insert(j+1, "        for col in gdf.columns:\n")
                        source.insert(j+2, "            if pd.api.types.is_datetime64_any_dtype(gdf[col]):\n")
                        source.insert(j+3, "                gdf[col] = gdf[col].astype(str)\n")
                        break
                break

with open(path, "w") as f:
    json.dump(notebook, f, indent=1)

print("Notebook updated.")
