# 🚀 Quick Start Guide

Get the Nutrition Analyst POC running in 5 minutes!

## ⚡ Fast Setup (Windows)

### Step 1: Install Tesseract OCR (2 minutes)

1. Download: https://github.com/UB-Mannheim/tesseract/wiki
2. Run installer → Use default path: `C:\Program Files\Tesseract-OCR`
3. Done!

### Step 2: Install Python Dependencies (1 minute)

```bash
cd langchain/nutrition_analyst
pip install -r requirements.txt
```

### Step 3: Add Your Groq API Key (30 seconds)

```bash
# Create .env file
copy .env.example .env

# Edit .env and add:
GROQ_API_KEY=your_key_here
```

Get free key: https://console.groq.com/keys

### Step 4: Run! (30 seconds)

```bash
streamlit run app.py
```

Browser opens automatically → Start scanning barcodes! 📹

---

## 🎯 Quick Test

Try this barcode to verify everything works:

**Coca-Cola:** `5449000000996`

1. Click "Manual Input" tab
2. Enter: `5449000000996`
3. Click "Analyze Product"
4. See results in ~5 seconds ✅

---

## 🔧 One-Liner Troubleshoot

**Tesseract not found?**
```bash
tesseract --version
```
If error → Reinstall Tesseract from Step 1

**Python errors?**
```bash
pip install --upgrade -r requirements.txt
```

**Webcam not working?**
→ Use "Manual Input" tab instead

---

## 📖 Full Documentation

- **Detailed Install:** See [INSTALL.md](INSTALL.md)
- **Full README:** See [README.md](README.md)

---

**That's it! Happy scanning! 🥗**
