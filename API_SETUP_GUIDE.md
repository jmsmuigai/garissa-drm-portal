# 🔑 API SETUP GUIDE - Complete Instructions

This guide shows you **exactly where to get** all the API keys needed for Garissa Sentinel.

---

## 📋 APIs You Need

| API | Purpose | Cost | Required? |
|-----|---------|------|-----------|
| Google Earth Engine | Satellite data | **FREE** | ✅ YES |
| Gemini AI | Environmental reports | **FREE** | ✅ YES |
| Google Cloud Billing | Enable GEE services | **FREE** (no charges) | ✅ YES |

---

## 1️⃣ Google Earth Engine Setup

### Step 1: Sign Up for Earth Engine

**🔗 Go to:** https://earthengine.google.com/signup

1. Click **"Sign Up"** button
2. Sign in with your Google account (jmsmuigai@gmail.com)
3. Select **"Academia & Research"** or **"Non-commercial"**
4. Fill in:
   - Organization: Garissa County Government
   - Country: Kenya
   - Purpose: Environmental monitoring and disaster risk management
5. Click **"Submit"**
6. **Wait for approval email** (usually 1-2 days, but can be instant)

### Step 2: Enable Cloud Project

**🔗 Go to:** https://console.cloud.google.com

1. Click **"Select a project"** at the top
2. Click **"NEW PROJECT"**
3. Enter project name: `garissa-sentinel-drm`
4. Click **"Create"**
5. **Copy the Project ID** that appears (looks like: `garissa-sentinel-drm-xxxxx`)

### Step 3: Link Billing Account

**You already have:** `013D12-524A4C-CBF5AA`

**🔗 In Cloud Console:** https://console.cloud.google.com/billing

1. Click **"Link a billing account"**
2. Select your account: `013D12-524A4C-CBF5AA`
3. Click **"Set account"**

> ⚠️ **Don't worry:** Earth Engine is FREE. The billing account is just for identity verification. You won't be charged!

### Step 4: Enable Earth Engine API

**🔗 Go to:** https://console.cloud.google.com/apis/library/earthengine.googleapis.com

1. Make sure your project `garissa-sentinel-drm` is selected (top bar)
2. Click **"ENABLE"** button
3. Wait for confirmation

### ✅ What to Copy:

```plaintext
GCP_PROJECT_ID = "garissa-sentinel-drm"  # Or whatever ID was created
GCP_BILLING_ACCOUNT = "013D12-524A4C-CBF5AA"  # You already have this
```

---

## 2️⃣ Gemini AI API Key

### Step 1: Get Your API Key

**🔗 Go to:** https://makersuite.google.com/app/apikey

1. Sign in with your Google account
2. Click **"Create API key"** button
3. Select your project: `garissa-sentinel-drm` (or create a new one)
4. Click **"Create API key in existing project"**
5. **COPY the key** that appears (starts with `AIza...`)

### Step 2: Test Your Key

**🔗 Go to:** https://makersuite.google.com/app/prompts/new

1. Type: "Say hello"
2. Click **"Run"**
3. If you get a response, your key works!

### ✅ What to Copy:

```plaintext
GEMINI_API_KEY = "AIzaSy..." # Your actual key (40+ characters)
```

> ⚠️ **Keep it secret!** Don't share this key publicly.

---

## 3️⃣ Update the Colab Notebook

### Find the API Configuration Cell

In `GARISSA_SENTINEL_COMPLETE.ipynb`, look for this cell (near the top):

```python
# ========================================
# 🔑 YOUR API KEYS - EDIT THESE!
# ========================================

GEMINI_API_KEY = "AIzaSyDDZludrLe0owCB3jFvPWSp8b3ZBx5hBmQ"  # ← REPLACE
GCP_BILLING_ACCOUNT = "013D12-524A4C-CBF5AA"  # ← Already correct!
GCP_PROJECT_ID = "garissa-sentinel-drm"  # ← REPLACE if different
```

### How to Edit:

1. **Click** the cell in Colab
2. **Replace** the values with YOUR keys
3. **Run** the cell (click ▶️ button)

---

## 🎯 QUICK REFERENCE CARD

**Copy these values into your notebook:**

```python
# === EDIT THESE IN COLAB ===

# 1. Gemini AI Key (from https://makersuite.google.com/app/apikey)
GEMINI_API_KEY = "YOUR_KEY_HERE"  # Starts with AIza...

# 2. Google Cloud Billing Account (you have this!)
GCP_BILLING_ACCOUNT = "013D12-524A4C-CBF5AA"  # ✅ Correct

# 3. Google Cloud Project ID (from https://console.cloud.google.com)
GCP_PROJECT_ID = "garissa-sentinel-drm"  # Or your actual project ID
```

---

## 🆘 Troubleshooting

### Problem: "Earth Engine authentication failed"

**Solution:**
1. Make sure you've been approved for Earth Engine (check email)
2. Make sure billing account is linked to project
3. Make sure Earth Engine API is enabled

**Check approval:** Go to https://code.earthengine.google.com
- If you can access it, you're approved!
- If not, wait for approval email

### Problem: "Invalid API key" (Gemini)

**Solution:**
1. Go to https://makersuite.google.com/app/apikey
2. Check if the key is still active
3. If not, create a new one
4. Make sure you copied the FULL key (40+ characters)

### Problem: "Billing account not found"

**Solution:**
1. Go to https://console.cloud.google.com/billing
2. Make sure `013D12-524A4C-CBF5AA` is listed
3. Make sure it's linked to your project
4. Check with your organization's billing admin

### Problem: "Project not found"

**Solution:**
1. Go to https://console.cloud.google.com
2. Click project dropdown (top bar)
3. Copy the EXACT Project ID shown
4. Paste that ID into `GCP_PROJECT_ID`

---

## 📊 Usage Limits & Quotas

### Google Earth Engine (FREE Tier)
- **Requests:** Unlimited for non-commercial use
- **Computation:** 100 concurrent requests
- **Storage:** 250 GB of assets
- **Exports:** Unlimited

> ✅ **Your usage:** Well within free limits!

### Gemini AI (FREE Tier)
- **Requests:** 60 per minute
- **Tokens:** 1,500,000 per month
- **Models:** gemini-pro (text)

> ✅ **Your usage:** ~10 requests per analysis = plenty!

---

## 🔒 Security Best Practices

### DO ✅
- Keep API keys in Colab only (not in GitHub)
- Use separate keys for testing vs production
- Monitor usage at https://console.cloud.google.com

### DON'T ❌
- Share API keys in emails or messages
- Commit keys to public repositories
- Use the same key across multiple projects

---

## 📞 Getting Help

### Earth Engine Issues:
- Forum: https://groups.google.com/g/google-earth-engine-developers
- Documentation: https://developers.google.com/earth-engine

### Gemini AI Issues:
- Support: https://makersuite.google.com/help
- Documentation: https://ai.google.dev/docs

### Billing Issues:
- GCP Support: https://console.cloud.google.com/support

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Can access https://code.earthengine.google.com
- [ ] Billing account `013D12-524A4C-CBF5AA` is linked
- [ ] Project `garissa-sentinel-drm` is created
- [ ] Earth Engine API is enabled
- [ ] Gemini API key is created
- [ ] Gemini test prompt works
- [ ] All keys are copied into Colab notebook

**If all checked: You're ready to go! 🎉**

---

## 🎓 Video Tutorials (Recommended)

### Earth Engine Setup
https://www.youtube.com/watch?v=oAGfY7gM7Ms

### Colab Basics
https://www.youtube.com/watch?v=inN8seMm7UI

### Gemini AI Setup
https://ai.google.dev/tutorials/get_started_web

---

**🌍 Once all APIs are configured, you're ready to monitor Garissa from space!**
