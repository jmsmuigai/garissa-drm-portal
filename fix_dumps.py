with open("build_master_map.py", "r") as f:
    text = f.read()

dumps_block = """
schools_js = json.dumps(schools_data) if schools_data else "null"
health_js = json.dumps(health_data) if health_data else "null"
schools_risk_js = json.dumps(schools_at_risk_data) if schools_at_risk_data else "null"
health_risk_js = json.dumps(health_at_risk_data) if health_at_risk_data else "null"
boreholes_js = json.dumps(boreholes_data) if boreholes_data else "null"
rivers_js = json.dumps(rivers_data) if rivers_data else "null"
county_js = json.dumps(county_data) if county_data else "null"
subcounties_js = json.dumps(subcounties_data) if subcounties_data else "null"
wards_js = json.dumps(wards_data) if wards_data else "null"
dams_js = json.dumps(dams_data) if dams_data else "null"
cascade_js = json.dumps(cascade_data) if cascade_data else "null"
evac_js = json.dumps(evac_data) if evac_data else "null"
elnino_js = json.dumps(elnino_data) if elnino_data else "null"
tana_buffer_js = json.dumps(tana_buffer) if tana_buffer else "null"
laghas_js = json.dumps(laghas_geojson) if laghas_geojson else "null"
towns_js = json.dumps(towns_data) if towns_data else "null"
camps_js = json.dumps(camps_data) if camps_data else "null"
dagahaley_js = json.dumps(dagahaley) if dagahaley else "null"
hagadera_js = json.dumps(hagadera) if hagadera else "null"
ifo_js = json.dumps(ifo_camp) if ifo_camp else "null"
high_risk_js = json.dumps(high_risk) if high_risk else "null"
medium_risk_js = json.dumps(medium_risk) if medium_risk else "null"
extreme_risk_js = json.dumps(extreme_risk) if extreme_risk else "null"
disease_js = json.dumps(disease_data) if disease_data else "null"
subcounty_summary_js = json.dumps(subcounty_summary) if subcounty_summary else "null"

"""

idx = text.find("HTML = HTML_TEMPLATE.replace('__TOTAL_SCHOOLS__', str(total_schools))")
if idx != -1:
    new_text = text[:idx] + dumps_block + text[idx:]
    with open("build_master_map.py", "w") as f:
        f.write(new_text)
    print("Fixed!")
