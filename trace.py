with open("build_master_map.py", "r") as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    new_lines.append(line)
    if line.strip().startswith("schools_data = load_geojson"):
        new_lines.append("print('Loaded schools', flush=True)\n")
    elif line.strip().startswith("boreholes_data = load_geojson"):
        new_lines.append("print('Loaded boreholes', flush=True)\n")
    elif line.strip().startswith("tana_buffer = load_geojson"):
        new_lines.append("print('Loaded tana buffer', flush=True)\n")
    elif line.strip().startswith("county_js = json.dumps"):
        new_lines.append("print('Dumping json...', flush=True)\n")
    elif line.strip().startswith("HTML_TEMPLATE ="):
        new_lines.append("print('Got HTML template', flush=True)\n")
    elif line.strip().startswith("HTML = HTML.replace('__GJ_COUNTY__', county_js)"):
        new_lines.append("print('Replacing json inside HTML...', flush=True)\n")
        
with open("build_master_map_trace.py", "w") as f:
    f.writelines(new_lines)
