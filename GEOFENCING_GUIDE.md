# 🗺️ Geofencing Guide - Safe Grazing Zones for Pastoralist Communities

## What is Geofencing?

**Geofencing** creates invisible digital boundaries (like virtual fences) around specific geographic areas. For Garissa Sentinel, we identify "Safe Grazing Zones" based on:

1. **Good Vegetation Health** (NDVI > 0.3)
2. **Low Population Density** (< 10 people/km²)

These zones tell pastoralists: *"This area has good grass and few people → it's safe to graze your livestock here."*

---

## 📊 How Safe Zones Are Calculated

### Step 1: Satellite Vegetation Analysis
```python
# We get recent satellite images showing plant health
ndvi = satellite.calculate_vegetation_health()

# Filter areas with healthy grass (NDVI > 0.3)
good_grass = ndvi > 0.3
```

**NDVI Scale:**
- `-1 to 0`: Water, roads, bare rock
- `0 to 0.2`: Very sparse vegetation (poor grazing)
- `0.2 to 0.4`: Moderate vegetation (acceptable grazing)
- `0.4 to 0.6`: Good vegetation ✅ (good grazing)
- `0.6 to 1.0`: Dense forests (may have tsetse flies)

### Step 2: Population Density Check
```python
# Get human population data
population = worldpop.get_density()

# Filter areas with few people (< 10 people/km²)
low_population = population < 10
```

### Step 3: Combine Both Criteria
```python
# Safe zones = Good grass AND Low population
safe_zones = good_grass AND low_population
```

---

## 📁 Output Formats

Garissa Sentinel exports safe zones in **4 different formats** for different uses:

### 1. GeoJSON (Web Maps & JavaScript)

**File:** `safe_grazing_zones.geojson`

**Use Case:** Web applications, mobile apps, online maps

**Example Usage:**
```javascript
// Load in Leaflet.js
fetch('OUTPUT/safe_grazing_zones.geojson')
  .then(r => r.json())
  .then(data => {
    L.geoJSON(data, {
      style: {color: 'green', fillOpacity: 0.3}
    }).addTo(map);
  });
```

**Data Structure:**
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [[40.5, 0.5], [40.6, 0.5], [40.6, 0.6], [40.5, 0.6], [40.5, 0.5]]
        ]
      }
    }
  ]
}
```

---

### 2. KML (Google Earth)

**File:** `safe_grazing_zones.kml`

**Use Case:** Viewing on mobile phones (Google Earth app), community presentations

**How to Use:**
1. Download **Google Earth** on your phone (free from Play Store/App Store)
2. Open the app
3. Menu → Import KML file
4. Navigate to `safe_grazing_zones.kml`
5. Green zones = Safe for grazing!

**Features:**
- Color-coded polygons (green = safe)
- Click on zone to see details
- Works offline once loaded
- Share via WhatsApp/Bluetooth

---

### 3. Shapefile (QGIS & ArcGIS)

**Files:**
- `safe_grazing_zones.shp` (geometry)
- `safe_grazing_zones.shx` (index)
- `safe_grazing_zones.dbf` (attributes)
- `safe_grazing_zones.prj` (projection: WGS84)

**Use Case:** GIS analysis, overlaying with other maps, printing

**How to Use in QGIS:**
```
1. Open QGIS
2. Layer → Add Layer → Add Vector Layer
3. Browse to: OUTPUT/safe_grazing_zones.shp
4. Click "Add"
5. Style the layer (green fill, 50% transparency)
```

**Attribute Table:**
| Field | Type | Description |
|-------|------|-------------|
| zone_id | Number | Unique zone identifier (1, 2, 3...) |
| quality | Text | Quality rating ("Good", "Excellent") |
| generated | Date | When this analysis was run |

---

### 4. CSV Coordinates (SMS & Mobile Apps)

**File:** `safe_grazing_zones_coordinates.csv`

**Use Case:** Bulk SMS systems, WhatsApp broadcasts, mobile apps without internet

**Format:**
```csv
zone_id,centroid_lat,centroid_lon,boundary_points,quality,area_approx_km2
1,0.554321,40.612345,"0.55,40.61;0.56,40.62;...",Good,12.5
2,0.423456,40.789012,"0.42,40.78;0.43,40.79;...",Good,8.3
```

**Columns Explained:**
- `zone_id`: Zone number (1, 2, 3...)
- `centroid_lat`: Center latitude (North-South position)
- `centroid_lon`: Center longitude (East-West position)
- `boundary_points`: Semicolon-separated boundary coordinates
- `quality`: Vegetation quality
- `area_approx_km2`: Approximate area in square kilometers

**SMS Message Example:**
```
SAFE ZONE 3: Center at 0.55°N, 40.61°E. 
Good grazing. Area: 12.5 km². 
Avoid camps to north.
```

---

## 🔧 Customizing Safe Zone Criteria

### Making Criteria More Strict
Edit `garissa_sentinel_main.py`:

```python
# Original (default)
safe_zones = ndvi_recent.gt(0.3).And(pop_density.lt(10))

# More strict (higher quality grass needed)
safe_zones = ndvi_recent.gt(0.4).And(pop_density.lt(5))
```

### Making Criteria More Relaxed
```python
# More relaxed (allows lower quality grass)
safe_zones = ndvi_recent.gt(0.2).And(pop_density.lt(15))
```

### Adding Additional Criteria

```python
# Example: Exclude flood-prone areas
from ee import FeatureCollection

# Load flood extents
flood_zones = FeatureCollection('users/jmsmuigai/garissa/flood_extents')

# Safe zones = Good grass AND Low population AND Not flooded
safe_zones = ndvi_recent.gt(0.3) \
             .And(pop_density.lt(10)) \
             .And(not_in_flood_zone)
```

---

## 📱 Integration with Mobile Applications

### Option 1: Offline Mobile App (Android/iOS)

**Technology:** Flutter + local SQLite database

1. **Export CSV coordinates** to app database
2. **Use device GPS** to find user location
3. **Calculate distance** to nearest safe zone
4. **Show direction** with arrow/compass
5. **Works offline** (no internet needed)

**Sample Code (Flutter):**
```dart
// Load safe zones from CSV
List<SafeZone> zones = await loadFromCSV();

// Get user location
Position position = await Geolocator.getCurrentPosition();

// Find nearest zone
SafeZone nearest = findNearest(position, zones);

// Show distance
print('Nearest safe zone: ${nearest.distance} km away');
```

### Option 2: SMS Alert System

**Service:** Africa's Talking, Twilio, or similar

```python
# Example: Send SMS with nearest zone
import africastalking

africastalking.initialize(username='sandbox', api_key='YOUR_KEY')
sms = africastalking.SMS

# Read zones from CSV
zones_df = pd.read_csv('OUTPUT/safe_grazing_zones_coordinates.csv')

# Send to herders
for phone in herder_phones:
    zone = zones_df.iloc[0]  # First zone
    message = f"SAFE ZONE {zone['zone_id']}: {zone['centroid_lat']:.4f}N, {zone['centroid_lon']:.4f}E. Good grazing."
    sms.send(message, [phone])
```

### Option 3: WhatsApp Sharing

1. Load KML file on your phone
2. Open Google Earth app
3. Tap on safe zone
4. Tap "Share"
5. Send via WhatsApp to community groups

---

## 🌍 Understanding Coordinates

### Decimal Degrees Format
Garissa Sentinel uses **Decimal Degrees (DD)** format:

```
Latitude:  0.554321°N  (North of equator)
Longitude: 40.612345°E (East of prime meridian)
```

**Garissa County Bounds:**
- Latitude: -1.5° to 1.5° (spans equator)
- Longitude: 38.5° to 41.5°

### Converting to Degrees-Minutes-Seconds (DMS)

Some herders may prefer traditional DMS format:

```python
# Decimal: 0.554321°N
# DMS: 0° 33' 15.6" N

# Conversion formula
degrees = int(0.554321)          # 0
minutes = int((0.554321 - 0) * 60)  # 33
seconds = ((0.554321 - 0) * 60 - 33) * 60  # 15.6
```

---

## ⚠️ Important Limitations

### 1. Satellite Resolution
- **Minimum detectable area**: ~30m × 30m (0.0009 km²)
- **Small patches** < 1 hectare may be missed

### 2. Cloud Cover
- **Cloud-free images** needed for accurate NDVI
- **Rainy seasons** may have fewer usable images
- **Solution**: Use median composite over 3 months

### 3. Seasonal Variations
- **Dry season** (Jan-Mar): Lower NDVI everywhere
- **Wet season** (Apr-Jun): Higher NDVI everywhere
- **Solution**: Compare same seasons across years

### 4. Ground Truth Needed
- **Satellite data ≠ Reality always**
- **Field verification** recommended
- **Community knowledge** essential

**Best Practice:**
```
✅ Use geofencing as a STARTING POINT
✅ Send scouts to verify before moving whole herd
✅ Consult elders familiar with the area
✅ Check for security/wildlife issues (satellites can't see lions!)
```

---

## 📈 Monitoring Zone Changes Over Time

### Monthly Tracking
```bash
# Run analysis each month
cd /path/to/GARISSADRM

# January run
python garissa_sentinel_main.py --output-suffix jan2025

# February run
python garissa_sentinel_main.py --output-suffix feb2025

# Compare
diff OUTPUT/safe_grazing_zones_jan2025.csv OUTPUT/safe_grazing_zones_feb2025.csv
```

### Trend Analysis
```python
import pandas as pd
import matplotlib.pyplot as plt

# Load multiple months
jan = pd.read_csv('OUTPUT/zones_jan2025.csv')
feb = pd.read_csv('OUTPUT/zones_feb2025.csv')
mar = pd.read_csv('OUTPUT/zones_mar2025.csv')

# Plot total safe area over time
months = ['Jan', 'Feb', 'Mar']
total_areas = [jan['area_approx_km2'].sum(), 
               feb['area_approx_km2'].sum(),
               mar['area_approx_km2'].sum()]

plt.plot(months, total_areas)
plt.title('Total Safe Grazing Area - Trend')
plt.ylabel('Area (km²)')
plt.show()
```

---

## 🤝 Community Best Practices

### 1. Inform Before Implementing
- **Community meeting** to explain the system
- **Visual aids** (print KML on maps)
- **Trial period** with volunteer herders

### 2. Combine with Traditional Knowledge
```
Digital Zones + Elder Wisdom = Best Results

Example:
✅ Digital says Zone 3 is safe
✅ Elder confirms no wild animals recently
→ Proceed to Zone 3
```

### 3. Update Regularly
- **Re-run analysis** monthly during dry season
- **Weekly updates** during drought emergencies
- **Share updates** via SMS/WhatsApp

### 4. Feedback Loop
- **Herders report** if zone actually had good grass
- **Adjust criteria** based on feedback
- **Improve accuracy** over time

---

## 📞 Support

For geofencing questions:
- **Technical Issues**: Check `README.md` troubleshooting section
- **Customization**: Edit `geofencing_engine.py`
- **Training**: Contact jmsmuigai@gmail.com

---

**Remember:** Geofencing is a tool to help, not replace, traditional pastoralist knowledge!

🌱 Good Grass + 🤖 Smart Technology + 👴 Elder Wisdom = **Sustainable Grazing**
