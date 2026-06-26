import json

path = "garissa_elnino_flood_risk.ipynb"
with open(path, "r") as f:
    notebook = json.load(f)

for cell in notebook['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        for i, line in enumerate(source):
            if "ee.Initialize(project='garissadrm')" in line:
                source[i] = "    try:\n"
                source.insert(i+1, "        ee.Initialize(project='garissadrm')\n")
                source.insert(i+2, "    except Exception:\n")
                source.insert(i+3, "        print('\\n⚠️ WARNING: Project garissadrm is not registered for Earth Engine. Visit https://console.cloud.google.com/earth-engine/configuration?project=garissadrm to register it.')\n")
                source.insert(i+4, "        print('Falling back to default project...\\n')\n")
                source.insert(i+5, "        ee.Initialize()\n")
                break

with open(path, "w") as f:
    json.dump(notebook, f, indent=1)

print("Notebook updated.")
