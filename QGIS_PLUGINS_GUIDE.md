# 🔌 QGIS Configuration & Plugin Guide for Garissa DRM

To fully replicate the processing pipelines used to generate the Garissa DRM maps and analyze flood risk locally, you will need a specific setup in QGIS (Quantum GIS). 

This guide outlines exactly which plugins to install and how to configure them for disaster risk management analysis.

## 📥 How to Install Plugins in QGIS
1. Open QGIS.
2. On the top menu bar, click **Plugins** > **Manage and Install Plugins...**
3. Ensure you have an active internet connection. QGIS will fetch the plugin repository.
4. Search for the plugin names listed below in the search bar.
5. Click **Install Plugin** in the bottom right corner.

---

## 🛠️ Mandatory Plugins

### 1. Google Earth Engine (GEE) Plugin
* **Search Name:** `Earth Engine Data Catalog` / `qgis-earthengine-plugin`
* **Why you need it:** Allows you to load Google Earth Engine datasets directly into QGIS without downloading massive files. You can visualize the live Sentinel-1 flood extents over your local Garissa shapefiles.
* **Setup:** Requires you to authenticate your Google Account once installed.

### 2. QuickMapServices
* **Search Name:** `QuickMapServices`
* **Why you need it:** The best plugin for adding high-resolution satellite imagery basemaps.
* **Setup:** After installing, go to *Web > QuickMapServices > Settings > More services*, and click **"Get contributed pack"**. This will unlock Google Hybrid, Google Satellite, Esri, and Bing maps.

### 3. qgis2web
* **Search Name:** `qgis2web`
* **Why you need it:** This is the tool used to export QGIS map compositions into the interactive HTML/Leaflet maps used on the web dashboard (like `garissa_master_drm_map.html`). It converts your styles and layers into web code instantly.

### 4. Data Plotly
* **Search Name:** `Data Plotly`
* **Why you need it:** Creates interactive D3 charts directly inside QGIS. Used to generate the histograms of flood vulnerability (e.g., how many schools fall within the 0-1km flood radius).

---

## 🔬 Advanced Analysis Plugins

### 5. Profile Tool
* **Search Name:** `Profile Tool`
* **Why you need it:** Draws a line across the River Tana and generates an elevation cross-section. Extremely useful for visualizing the river basin topology and understanding where water will spill over first.

### 6. SAGA Next Gen (SAGANG)
* **Search Name:** Usually pre-installed in the Processing Toolbox, or search `SAGA`.
* **Why you need it:** Contains advanced hydrological algorithms. Used for generating "Catchment Area", "Flow Accumulation", and "Topographic Wetness Index" from the SRTM Elevation model.

### 7. HCMGIS
* **Search Name:** `HCMGIS`
* **Why you need it:** Excellent for bulk processing and downloading OpenStreetMap data. Useful for fetching the latest building footprints in Garissa town or Dadaab camp.

### 8. TimeManager / Temporal Controller
* **Search Name:** Built into modern QGIS (QGIS 3.14+). Look for the "clock" icon in the Map Navigation toolbar.
* **Why you need it:** Used to animate the progression of floods over time. If you have daily flood extents from Oct to Dec, this tool creates a video animation of the flood spreading.

---

## ⚙️ Recommended Project Settings for Garissa
Before starting analysis, ensure your project is set up with the correct Coordinate Reference Systems (CRS):

1. **Project CRS (for viewing):** `EPSG:4326` (WGS 84 - Lat/Lon). Good for web maps and GPS coordinates.
2. **Processing CRS (for measuring distance/area):** `EPSG:32737` (WGS 84 / UTM zone 37S). **CRITICAL.** If you measure the area of a flood, or buffer a river by 1km while in EPSG:4326, your measurements will be wrong. Always reproject vector layers to UTM Zone 37S before buffering or calculating area.
