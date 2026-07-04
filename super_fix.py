import re

with open('build_master_map.py', 'r') as f:
    text = f.read()

# We need to find exactly where the bad stuff starts.
# We'll look for `    {data:GJ_HEALTH, nameKey:'name_healt', color:'#06b6d4', icon:'🏥'},`
marker = "    {data:GJ_HEALTH, nameKey:'name_healt', color:'#06b6d4', icon:'🏥'},"
idx = text.find(marker)

if idx != -1:
    good_text = text[:idx + len(marker)] + "\n"
    
    missing_part = """    {data:GJ_BORES, nameKey:'Borehole_N', color:'#0ea5e9', icon:'💧'}
  ];
  datasets.forEach(ds => {
    if (!ds.data) return;
    ds.data.features.forEach(f => {
      const p = f.properties;
      const name = (p[ds.nameKey] || p.name || '').toLowerCase();
      if (name.includes(q) && found < 10) {
        found++;
        const c = f.geometry.coordinates;
        const m = L.circleMarker([c[1],c[0]], {radius:12, fillColor:ds.color, color:'white', weight:3, fillOpacity:0.9});
        m.bindPopup(buildPopup(p, p[ds.nameKey]||'Feature', ds.color, ds.icon)).openPopup();
        m.addTo(map);
        searchMarkers.push(m);
        if (found===1) map.setView([c[1],c[0]], 12);
      }
    });
  });
  results.textContent = found>0 ? `✅ ${found} results found` : '❌ No features found';
}
function clearSearch() {
  document.getElementById('searchInput').value = '';
  searchMarkers.forEach(m => map.removeLayer(m));
  searchMarkers = [];
  document.getElementById('searchResults').textContent='';
}

// ══════════════════════════════════════════════════════════════════
// INIT ALL COMPONENTS
// ══════════════════════════════════════════════════════════════════
buildDiseaseCards();
buildDiseaseChart();
buildCascadeTimeline();

// Animate/highlight Garissa boundary on load
setTimeout(() => {
  if (layers.countyBoundary) {
    layers.countyBoundary.setStyle({color:'#0ea5e9',weight:4,dashArray:'none'});
  }
}, 1000);

// Auto-fit to Garissa County
if (layers.countyBoundary) {
  const bounds = layers.countyBoundary.getBounds();
  if (bounds.isValid()) map.fitBounds(bounds, {padding:[20,20]});
}

console.log('🌊 Garissa DRM Master Map loaded!');
console.log('  📊 Schools:', GJ_SCHOOLS?.features?.length, '| Health:', GJ_HEALTH?.features?.length, '| Boreholes:', GJ_BORES?.features?.length);
</script>
</body>
</html>\"\"\"

HTML = HTML_TEMPLATE.replace('__TOTAL_SCHOOLS__', str(total_schools))
HTML = HTML.replace('__AT_RISK_SCHOOLS__', str(at_risk_schools))
HTML = HTML.replace('__TOTAL_HEALTH__', str(total_health))
HTML = HTML.replace('__AT_RISK_HEALTH__', str(at_risk_health))
HTML = HTML.replace('__BH_COUNT__', str(bh_count))

HTML = HTML.replace('__WASH_CLEAN_WATER__', str(wash_needs["clean_water"]))
HTML = HTML.replace('__PCT_CLEAN_WATER__', str(int(wash_needs["clean_water"]/max(total_health,1)*100)))
HTML = HTML.replace('__WASH_SANITATION__', str(wash_needs["sanitation"]))
HTML = HTML.replace('__PCT_SANITATION__', str(int(wash_needs["sanitation"]/max(total_health,1)*100)))
HTML = HTML.replace('__WASH_HANDWASHING__', str(wash_needs["handwashing"]))
HTML = HTML.replace('__PCT_HANDWASHING__', str(int(wash_needs["handwashing"]/max(total_health,1)*100)))

HTML = HTML.replace('__HLT_WATERBORNE__', str(hlt_stats["waterborne"]))
HTML = HTML.replace('__PCT_WATERBORNE__', str(int(hlt_stats["waterborne"]/max(total_health,1)*100)))
HTML = HTML.replace('__HLT_NO_WATER__', str(hlt_stats["no_water"]))
HTML = HTML.replace('__PCT_NO_WATER__', str(int(hlt_stats["no_water"]/max(total_health,1)*100)))
HTML = HTML.replace('__HLT_FLOODING__', str(hlt_stats["flooding_issues"]))
HTML = HTML.replace('__PCT_FLOODING__', str(int(hlt_stats["flooding_issues"]/max(total_health,1)*100)))

facility_levels_html = "".join(f'<div class="wash-bar-row"><div class="wash-bar-label"><span>{k}</span><span>{v}</span></div><div class="wash-bar-bg"><div class="wash-bar-fill" style="width:{int(v/max(total_health,1)*100)}%;background:#0d9488"></div></div></div>' for k,v in sorted(hlt_stats["level"].items(), key=lambda x:-x[1])[:6])
HTML = HTML.replace('__FACILITY_LEVELS__', facility_levels_html)

HTML = HTML.replace('__GJ_SCHOOLS__', schools_js)
HTML = HTML.replace('__GJ_HEALTH__', health_js)
HTML = HTML.replace('__GJ_SCH_RISK__', schools_risk_js)
HTML = HTML.replace('__GJ_HLT_RISK__', health_risk_js)
HTML = HTML.replace('__GJ_BORES__', boreholes_js)
HTML = HTML.replace('__GJ_RIVERS__', rivers_js)
HTML = HTML.replace('__GJ_COUNTY__', county_js)
HTML = HTML.replace('__GJ_SUBCTY__', subcounties_js)
HTML = HTML.replace('__GJ_WARDS__', wards_js)
HTML = HTML.replace('__GJ_DAMS__', dams_js)
HTML = HTML.replace('__GJ_CASCADE__', cascade_js)
HTML = HTML.replace('__GJ_EVAC__', evac_js)
HTML = HTML.replace('__GJ_ELNINO__', elnino_js)
HTML = HTML.replace('__GJ_TANA__', tana_buffer_js)
HTML = HTML.replace('__GJ_LAGHAS__', laghas_js)
HTML = HTML.replace('__GJ_TOWNS__', towns_js)
HTML = HTML.replace('__GJ_CAMPS__', camps_js)
HTML = HTML.replace('__GJ_DAGAH__', dagahaley_js)
HTML = HTML.replace('__GJ_HAGA__', hagadera_js)
HTML = HTML.replace('__GJ_IFO__', ifo_js)
HTML = HTML.replace('__GJ_HIGHZ__', high_risk_js)
HTML = HTML.replace('__GJ_MEDZ__', medium_risk_js)
HTML = HTML.replace('__GJ_EXTREMEZ__', extreme_risk_js)
HTML = HTML.replace('__DISEASE_DATA__', disease_js)
HTML = HTML.replace('__SUBCTY_STATS__', subcounty_summary_js)

print(f"  📄 HTML size: {len(HTML)/1024:.0f} KB")
output_path = OUTPUT_DIR / 'garissa_master_interactive_map.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(HTML)
print(f"\\n✅ Master Interactive Map → {output_path.name}")
print(f"   Size: {output_path.stat().st_size/1024:.0f} KB")
print("\\n" + "=" * 70)
print("🎉 ALL DONE! Open garissa_master_interactive_map.html in your browser")
print("=" * 70)
"""
    
    with open('build_master_map.py', 'w') as f:
        f.write(good_text + missing_part)
        
    print("Super fixed applied.")
else:
    print("Marker not found.")
