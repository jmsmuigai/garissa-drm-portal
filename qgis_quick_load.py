#!/usr/bin/env python3
"""
Garissa DRM — QGIS Quick Loader
================================
Run this script from the QGIS Python Console to instantly load
the enhanced workspace including Seven Forks dams, at-risk schools
and hospitals, El Nino overlay, and evacuation zones.

HOW TO RUN IN QGIS:
  1. Open QGIS
  2. Plugins > Python Console (or Ctrl+Alt+P)
  3. In the console, type:
     exec(open(r'/Users/james/Library/CloudStorage/GoogleDrive-jmsmuigai@gmail.com/My Drive/GARISSADRM/qgis_quick_load.py').read())
  4. Press Enter

The complete workspace will load automatically with:
  - All risk layers
  - Seven Forks dam markers with live-like status
  - Schools & hospitals color-coded by risk
  - Hover pop-ups showing all attributes
  - El Nino 2026 predicted inundation zone
  - Evacuation assembly points
"""
import sys
from pathlib import Path

SCRIPT_PATH = Path('/Users/james/Library/CloudStorage/GoogleDrive-jmsmuigai@gmail.com/My Drive/GARISSADRM/4_qgis_enhanced_workspace.py')

if SCRIPT_PATH.exists():
    exec(open(str(SCRIPT_PATH)).read())
else:
    print("ERROR: Could not find 4_qgis_enhanced_workspace.py")
    print(f"Expected at: {SCRIPT_PATH}")
