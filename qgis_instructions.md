QGIS Quick Instructions for GARISSADRM

- Open QGIS and use 'Add Vector Layer' to load .shp or .gpkg files from this folder.
- For rasters (.tif), use 'Add Raster Layer'.
- Set project CRS to WGS 84 / UTM zone 37N if most layers use that (or use `Project -> Properties`).
- To prepare a layer for GEE: export the layer to GeoPackage or GeoJSON, upload to GCS, then use `earthengine upload`.
- To keep metadata, use `Layer Properties -> Metadata` and export layer metadata as needed.

Automation tips
- Use `scan_layers.py` to produce a CSV inventory of layers and CRSs.
- Use `gee_upload.py` to push files to GCS before uploading to Earth Engine.
