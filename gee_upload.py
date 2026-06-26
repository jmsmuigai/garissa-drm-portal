#!/usr/bin/env python3
"""Helper to upload local files to GCS and print Earth Engine upload command.

Usage examples:
  python gee_upload.py --bucket my-bucket --source "path/to/file.shp" --asset users/you/asset_name
"""
import argparse
from google.cloud import storage
from pathlib import Path


def upload_to_gcs(bucket_name, source_path, dest_blob_name=None):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    source = Path(source_path)
    if dest_blob_name is None:
        dest_blob_name = source.name
    blob = bucket.blob(dest_blob_name)
    blob.upload_from_filename(str(source))
    print(f'Uploaded gs://{bucket_name}/{dest_blob_name}')
    return f'gs://{bucket_name}/{dest_blob_name}'


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--bucket', required=True, help='GCS bucket name')
    ap.add_argument('--source', required=True, help='Local file to upload')
    ap.add_argument('--asset', required=False, help='Desired Earth Engine asset id (e.g. users/you/asset)')
    args = ap.parse_args()
    gpath = upload_to_gcs(args.bucket, args.source)
    if args.asset:
        print('\nRun the following Earth Engine CLI command to start upload:')
        print(f'  earthengine upload table --asset_id={args.asset} {gpath}')
    else:
        print('No Earth Engine asset id provided; upload done.')
