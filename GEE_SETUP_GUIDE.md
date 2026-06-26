# 🌍 Google Earth Engine (GEE) Setup Guide
*(Explained Step-by-Step like you're 10 years old)*

Welcome! We are going to connect the Garissa DRM Portal to Google Earth Engine. 

### What is Google Earth Engine?
Imagine you have a giant supercomputer in the sky that takes pictures of the whole Earth every single day. Now imagine you want to look at all those pictures for Garissa County over the last 10 years to see where the rain fell and where the floods happened. If you tried to download all those pictures to your laptop, it would crash! 

Google Earth Engine (GEE) keeps all the pictures on Google's giant computers. Instead of downloading the pictures, you just send a short "script" (like a text message) telling Google what to calculate, and it sends you back just the final map. It's like asking a librarian to read 1,000 books and just give you the one-page summary.

---

## 🚀 Step 1: Register for an Account

You need a special key to use the supercomputer.

1. Open your browser and go to: **[earthengine.google.com/signup](https://earthengine.google.com/signup/)**
2. Sign in with your Google Account (`jmsmuigai@gmail.com`).
3. It will ask what you want to use it for. Select **"Noncommercial / Research / Government"**.
4. Fill in the details (Institution: "Garissa County DRM").
5. Click **Submit**. Google usually approves it instantly, but sometimes it takes a few hours. Check your Gmail for the "Welcome to Earth Engine" email.

---

## 🚀 Step 2: Create a Cloud Project

GEE needs to be connected to a "Project". This is like a folder that tracks your usage.

1. Go to the **[Earth Engine Code Editor](https://code.earthengine.google.com/)**.
2. A popup will say "Choose a Google Cloud Project".
3. Click **"Register a new Cloud Project"**.
4. Name it something like: `garissa-drm-2026`.
5. Click **Continue**. It will take a few seconds to create.
6. Once done, you will see the Code Editor screen. It looks like a map on the bottom and a code box on top.

---

## 🚀 Step 3: Your First Earth Engine Script

Let's test if it works! In the big white box at the top of the Code Editor, copy and paste this text exactly:

> [!WARNING]
> **Syntax Error Warning:** Do NOT copy the markdown code block backticks (the lines that say ` ```javascript ` or ` ``` `). Only copy the raw JavaScript text inside the block!

// This script finds Garissa County and shows its elevation (how high the land is)

// 1. Find Garissa boundary
var garissa = ee.FeatureCollection("FAO/GAUL/2015/level1")
  .filter(ee.Filter.eq('ADM1_NAME', 'Garissa'));

// 2. Center the map on Garissa
Map.centerObject(garissa, 8);

// 3. Get the SRTM Elevation data
var elevation = ee.Image("USGS/SRTMGL1_003");

// 4. Cut the elevation data so it only shows inside Garissa
var garissaElevation = elevation.clip(garissa);

// 5. Add it to the map with some colors! (Blue is low, Red is high)
Map.addLayer(garissaElevation, {min: 0, max: 500, palette: ['blue', 'green', 'yellow', 'red']}, 'Garissa Elevation');

Now, click the **"Run"** button at the very top. Watch the map below — it should magically zoom into Garissa and color it based on how high the ground is! 

---

## 🚀 Step 4: Connecting the Portal (For the Developers)

The Garissa DRM Dashboard uses Python to talk to GEE automatically. Here is how we configure it:

1. Open your terminal on your Mac.
2. Type this command to install the GEE library:
   `pip install earthengine-api`
3. Type this command to log in:
   `earthengine authenticate`
4. A browser window will pop up asking for permission. Click Allow, then copy the special code back into your terminal.
5. In your `.env` file for the portal, make sure you have:
   `EE_PROJECT_ID=garissa-drm-2026`

---

## 🛰️ The Special "Layers" We Use For Garissa

When we ask GEE for maps, we ask for specific "Collections". Here are the exact ones we use for the portal:

* **🌧️ Rainfall (CHIRPS):** `UCSB-CHG/CHIRPS/DAILY` (Shows how much it rained today)
* **🌊 Floods (Sentinel-1):** `COPERNICUS/S1_GRD` (Radar satellite that can see floods through clouds!)
* **🌿 Vegetation (MODIS NDVI):** `MODIS/061/MOD13Q1` (Shows if the grazing land is green or dry)
* **🏕️ Population (WorldPop):** `WorldPop/GP/100m/pop` (Shows exactly where people live)
* **⛰️ Elevation (SRTM):** `USGS/SRTMGL1_003` (Shows where water will flow downhill)

You did it! You have successfully commanded a supercomputer! 🎉
