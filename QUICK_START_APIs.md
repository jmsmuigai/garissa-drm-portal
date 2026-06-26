# 🚀 QUICK START - Copy-Paste API Keys

## ⚡ 1-MINUTE SETUP

### Your Current API Keys:

```python
# Copy this entire block and paste it in Colab ↓

# ========================================
# 🔑 API CONFIGURATION
# ========================================

# Gemini AI (get yours at: https://makersuite.google.com/app/apikey)
GEMINI_API_KEY = "AIzaSyDDZludrLe0owCB3jFvPWSp8b3ZBx5hBmQ"

# Google Cloud Billing (you have this!)
GCP_BILLING_ACCOUNT = "013D12-524A4C-CBF5AA"

# Google Cloud Project ID (change if you created a different project)
GCP_PROJECT_ID = "garissa-sentinel-drm"
```

---

## 🔄 WHERE TO GET NEW GEMINI KEY (If Needed)

###Option 1: Get Personal Free Key (Recommended)

**🔗 URL:** https://makersuite.google.com/app/apikey

1. Click link above
2. Sign in with `jmsmuigai@gmail.com`
3. Click **"Create API key"** button
4. Select **"Create API key in new project"** (easier)
5. **COPY** the key that appears
6. **PASTE** it in Colab replacing `GEMINI_API_KEY = "..."`

**Looks like:** `AIzaSyABC123...` (40+ characters)

---

## 🏢 WHERE TO VERIFY BILLING ACCOUNT

**🔗 URL:** https://console.cloud.google.com/billing

1. Click link above
2. Sign in
3. Look for billing account ending in: `CBF5AA`
4. **Full ID:** `013D12-524A4C-CBF5AA`

💡 **You already have this - it's correct in the code above!**

---

## 🎯 WHAT TO DO IN COLAB

### Step 1: Open Colab
https://colab.research.google.com

### Step 2: Upload Notebook
- Click `File` → `Open notebook`
- Click `Upload`
- Choose: `GARISSA_SENTINEL_COMPLETE.ipynb`

### Step 3: Find API Cell
Look for cell that says:
```python
# ========================================
# 🔑 YOUR API KEYS - EDIT THESE!
# ========================================
```

### Step 4: Replace Keys
- Click the cell
- Replace `GEMINI_API_KEY` with YOUR new key
- Keep `GCP_BILLING_ACCOUNT` as is (already correct!)
- Keep `GCP_PROJECT_ID` as is (unless you used a different name)

### Step 5: Run Everything
- Click `Runtime` → `Run all`
- Follow authentication prompts when they appear

---

## 📋 AUTHENTICATION FLOW

When you run the notebook, you'll see:

### 1. Google Drive Mount
```
Permit this notebook to access your Google Drive?
```
**Action:** Click "Connect to Google Drive" → Allow

### 2. Earth Engine (First Time Only)
```
To authorize access, open the following URL...
```
**Action:** 
1. Click the URL
2. Click "Generate Token"
3. Sign in
4. Click "Allow"
5. Copy the code
6. Paste it back in Colab
7. Press Enter

### 3. Success!
```
✅ All systems ready!
```

---

## 🆘 QUICK FIXES

### "Invalid API key"
➜ Your Gemini key expired or is wrong  
➜ Get new one: https://makersuite.google.com/app/apikey  
➜ Paste in `GEMINI_API_KEY = "..."`

### "Billing account not found"
➜ Not linked to project  
➜ Go to: https://console.cloud.google.com/billing  
➜ Link account `013D12-524A4C-CBF5AA` to project

### "Earth Engine not enabled"
➜ API not activated  
➜ Go to: https://console.cloud.google.com/apis/library/earthengine.googleapis.com  
➜ Click "ENABLE"

---

## ✅ COPY-PASTE CHECKLIST

Before running:

- [ ] Opened Colab: https://colab.research.google.com
- [ ] Uploaded `GARISSA_SENTINEL_COMPLETE.ipynb`
- [ ] Got Gemini API key from: https://makersuite.google.com/app/apikey
- [ ] Pasted key in `GEMINI_API_KEY` variable
- [ ] Verified billing account: `013D12-524A4C-CBF5AA` is correct
- [ ] Ready to click `Runtime` → `Run all`

**All checked? GO! 🚀**

---

## 📞 Still Stuck?

See detailed guide: `API_SETUP_GUIDE.md`  
Or contact: jmsmuigai@gmail.com
