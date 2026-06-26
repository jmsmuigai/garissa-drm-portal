/**
 * GARISSA DRM - GOOGLE EARTH ENGINE (GEE) AUTOMATION APP
 * ======================================================
 * 
 * INSTRUCTIONS:
 * 1. Open https://code.earthengine.google.com/
 * 2. Paste this entire code into the center script editor.
 * 3. Click "Run" at the top to preview it.
 * 4. Click "Apps" -> "New App" in the top right to publish this as an interactive web map.
 * 5. Copy the App URL and embed it in your Garissa DRM Dashboard.
 */

// 1. Set the Map Style to Dark/Hybrid for a classic DRM dashboard look
Map.setOptions("HYBRID");
Map.setControlVisibility({all: false, zoomControl: true, mapTypeControl: true});

// 2. Define the Garissa County Boundary
var garissa = ee.FeatureCollection("FAO/GAUL/2015/level1")
  .filter(ee.Filter.eq('ADM1_NAME', 'Garissa'));

Map.centerObject(garissa, 8);

// Add a glowing style boundary for Garissa
var empty = ee.Image().byte();
var garissaOutline = empty.paint({featureCollection: garissa, color: 1, width: 3});
Map.addLayer(garissaOutline, {palette: ['#00f3ff']}, 'Garissa Border', true, 0.8);

// ==============================================================
// AUTOMATED DATA LAYERS
// ==============================================================

// 3. SENTINEL-1 RADAR FLOOD MONITORING (Live data, past 30 days)
var today = ee.Date(Date.now());
var lastMonth = today.advance(-30, 'day');

var sentinel1 = ee.ImageCollection('COPERNICUS/S1_GRD')
  .filterBounds(garissa)
  .filterDate(lastMonth, today)
  .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
  .filter(ee.Filter.eq('instrumentMode', 'IW'))
  .merge(ee.ImageCollection([ee.Image(0).rename('VV')])) // Fallback if no images found
  .select('VV')
  .mosaic()
  .clip(garissa);

// Simple water detection (very low backscatter)
var waterMask = sentinel1.lt(-16);
var floodVis = {min: 0, max: 1, palette: ['000000', 'ff007f']}; 
// Pink/Red for detected water for the futuristic nano-banana style
Map.addLayer(waterMask.updateMask(waterMask), floodVis, '🌊 Sentinel-1 Floods (Live)', false);


// 4. CHIRPS RAINFALL ANOMALY (Live Data)
var chirps = ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY")
  .filterBounds(garissa)
  .filterDate(lastMonth, today)
  .sum()
  .clip(garissa);

var rainVis = {min: 0, max: 200, palette: ['#001a33', '#004080', '#00f3ff', '#39ff14', '#ffd700']};
Map.addLayer(chirps, rainVis, '🌧️ 30-Day Rainfall (CHIRPS)', false);


// 5. MODIS VEGETATION (NDVI)
var ndvi = ee.ImageCollection('MODIS/061/MOD13Q1')
  .filterBounds(garissa)
  .filterDate(today.advance(-60, 'day'), today)
  .select('NDVI')
  .median()
  .clip(garissa);

var ndviVis = {min: 0, max: 8000, palette: ['#303030', '#c800ff', '#10d98c']};
Map.addLayer(ndvi, ndviVis, '🌿 Vegetation Index (NDVI)', false);


// 6. POPULATION DENSITY (WorldPop)
var worldpop = ee.ImageCollection("WorldPop/GP/100m/pop")
  .filter(ee.Filter.eq('country', 'KEN'))
  .mosaic()
  .clip(garissa);

var popVis = {min: 0, max: 50, palette: ['#000000', '#2d004b', '#542788', '#8073ac', '#b2abd2', '#fdb863', '#e08214', '#b35806']};
Map.addLayer(worldpop, popVis, '🏕️ Population Density', false);


// 7. ELEVATION (SRTM)
var elevation = ee.Image("USGS/SRTMGL1_003").clip(garissa);
var eleVis = {min: 0, max: 500, palette: ['blue', 'green', 'yellow', 'red']};
Map.addLayer(elevation, eleVis, '⛰️ Elevation (SRTM)', false);

// 8. RIVER TANA 500m BUFFER (Farm Vulnerability Zone)
// Using HydroSHEDS to get major rivers
var rivers = ee.FeatureCollection("WWF/HydroSHEDS/v1/FreeFlowingRivers")
  .filterBounds(garissa)
  .filter(ee.Filter.gt('RIV_ORD', 3)); // Major rivers
var riverBuffer = rivers.map(function(f) { return f.buffer(500); });
Map.addLayer(riverBuffer, {color: '#ff0000'}, '⚠️ River Tana 500m Farm Buffer', false);

// 9. LAGHAS (Seasonal Rivers Flow Accumulation)
var flowAcc = ee.Image("WWF/HydroSHEDS/15ACC").clip(garissa);
var laghas = flowAcc.gt(100); // threshold for seasonal streams
var laghasMasked = laghas.updateMask(laghas);
Map.addLayer(laghasMasked, {palette: ['#00ffff']}, '💧 Laghas (Seasonal Flood Paths)', false);

// 10. HEALTH RISK HOTSPOTS (Cholera/Malaria probability based on low elevation + stagnant water)
var lowElevation = elevation.lt(150); // Low-lying areas
var stagnantWaterRisk = waterMask.and(lowElevation);
Map.addLayer(stagnantWaterRisk.updateMask(stagnantWaterRisk), {palette: ['#ff00ff']}, '🦠 Health Risk Zones (Waterborne)', false);

// ==============================================================
// UI DASHBOARD WIDGETS
// ==============================================================

// Create an interactive UI Panel
var panel = ui.Panel({
  style: {
    width: '300px',
    padding: '15px',
    backgroundColor: 'rgba(2, 5, 16, 0.9)',
    color: '#00f3ff',
    position: 'bottom-left'
  }
});

var title = ui.Label({
  value: 'GARISSA DRM - LIVE TELEMETRY',
  style: {fontWeight: 'bold', fontSize: '18px', margin: '0 0 10px 0', color: '#ffd700', backgroundColor: '#00000000'}
});

var desc = ui.Label({
  value: 'Toggle layers using the top right "Layers" menu. Click anywhere on the map to get precise satellite data.',
  style: {fontSize: '12px', margin: '0 0 10px 0', color: '#f0f4ff', backgroundColor: '#00000000'}
});

var dataPanel = ui.Panel({style: {backgroundColor: '#00000000'}});

panel.add(title);
panel.add(desc);
panel.add(dataPanel);
Map.add(panel);

// Click handler for inspecting data
Map.onClick(function(coords) {
  dataPanel.clear();
  dataPanel.add(ui.Label('Scanning coordinates...', {color: '#ff007f', backgroundColor: '#00000000'}));
  
  var point = ee.Geometry.Point(coords.lon, coords.lat);
  var dot = ui.Map.Layer(point, {color: '#39ff14'}, 'Clicked Location');
  Map.layers().set(4, dot);
  
  var sampleRain = chirps.sample(point, 30).first();
  var samplePop = worldpop.sample(point, 100).first();
  var sampleEle = elevation.sample(point, 30).first();
  
  ee.Dictionary({
    rain: sampleRain.get('precipitation'),
    pop: samplePop.get('population'),
    ele: sampleEle.get('elevation')
  }).evaluate(function(vals) {
    dataPanel.clear();
    var rainVal = vals.rain ? vals.rain.toFixed(1) + ' mm' : 'No Data';
    var popVal = vals.pop ? Math.round(vals.pop) + ' people/ha' : 'No Data';
    var eleVal = vals.ele ? Math.round(vals.ele) + ' m' : 'No Data';
    
    dataPanel.add(ui.Label({
      value: '📍 Location: ' + coords.lat.toFixed(4) + ', ' + coords.lon.toFixed(4),
      style: {color: '#00f3ff', backgroundColor: '#00000000'}
    }));
    dataPanel.add(ui.Label({
      value: '🌧️ 30-Day Rainfall: ' + rainVal,
      style: {color: '#10d98c', backgroundColor: '#00000000', fontWeight: 'bold'}
    }));
    dataPanel.add(ui.Label({
      value: '🏕️ Population: ' + popVal,
      style: {color: '#fdb863', backgroundColor: '#00000000', fontWeight: 'bold'}
    }));
    dataPanel.add(ui.Label({
      value: '⛰️ Elevation: ' + eleVal,
      style: {color: '#ffd700', backgroundColor: '#00000000', fontWeight: 'bold'}
    }));
  });
});
