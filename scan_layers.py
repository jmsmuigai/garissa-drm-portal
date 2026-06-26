#!/usr/bin/env python3
"""Scan the repository for common GIS files and produce a CSV summary.

Usage: python scan_layers.py -i /path/to/root -o /path/to/output.csv
"""
import argparse
import csv
import os
from pathlib import Path

try:
    import fiona
except Exception:
    fiona = None

try:
    import rasterio
except Exception:
    rasterio = None


def scan(root):
    exts_vector = {'.shp', '.gpkg', '.geojson'}
    exts_raster = {'.tif', '.tiff'}
    rows = []
    root = Path(root)
    for i, p in enumerate(root.rglob('*')):
        if i % 10 == 0:
            print(f'Scanning {i}: {p}', flush=True)
        if p.suffix.lower() in exts_vector:
            info = {'path': str(p), 'type': 'vector', 'format': p.suffix.lower(), 'crs': '', 'features': '', 'bounds': ''}
            if fiona:
                try:
                    with fiona.open(p) as src:
                        crs = src.crs_wkt or src.crs
                        info['crs'] = str(crs)
                        count = 0
                        for _ in src:
                            count += 1
                        info['features'] = str(count)
                        info['bounds'] = str(src.bounds)
                except Exception as e:
                    info['crs'] = f'error: {e}'
            rows.append(info)
        elif p.suffix.lower() in exts_raster:
            info = {'path': str(p), 'type': 'raster', 'format': p.suffix.lower(), 'crs': '', 'features': '', 'bounds': ''}
            if rasterio:
                try:
                    with rasterio.open(p) as src:
                        info['crs'] = str(src.crs)
                        info['bounds'] = str(src.bounds)
                        info['features'] = f'w={src.width},h={src.height},count={src.count},dtype={src.dtypes[0] if src.dtypes else ""}'
                except Exception as e:
                    info['crs'] = f'error: {e}'
            rows.append(info)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--input', required=True, help='Root folder to scan')
    ap.add_argument('-o', '--output', required=True, help='CSV output path')
    args = ap.parse_args()
    rows = scan(args.input)
    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
    with open(args.output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['path', 'type', 'format', 'crs', 'features', 'bounds'])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    print(f'Wrote {len(rows)} rows to {args.output}')

if __name__ == '__main__':
    main()
