# Quick Installation Guide

## Step-by-Step Setup (Windows)

### 1. Install Tesseract OCR

**Required for barcode detection from webcam**

1. Download Tesseract installer:
   - Go to: https://github.com/UB-Mannheim/tesseract/wiki
   - Download the latest Windows installer (e.g., `tesseract-ocr-w64-setup-5.3.3.20231005.exe`)

2. Run the installer:
   - Use default installation path: `C:\Program Files\Tesseract-OCR`
   - Complete installation

3. Verify installation:
   ```bash
   tesseract --version
   ```
   If this works, you're good! If not, add to PATH manually.

### 2. Navigate to Project Directory
```bash
cd "C:\Users\Suggala Sai Preetham\resume roaster\langchain\nutrition_analyst"
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up Groq API Key

Create a `.env` file in this directory:

```bash
# Copy the template
copy .env.example .env
```

Then edit `.env` and add your Groq API key:
```
GROQ_API_KEY=your_actual_groq_api_key_here
```

**Get your free Groq API key:** https://console.groq.com/keys

### 5. Run the App
```bash
streamlit run app.py
```

The browser should automatically open to `http://localhost:8501`

---

## Troubleshooting

### ❌ Tesseract Not Found Error
**Solution:**
1. Make sure Tesseract is installed (see Step 1 above)
2. Verify it's in the correct path: `C:\Program Files\Tesseract-OCR\tesseract.exe`
3. If installed elsewhere, update the path in `barcode_extractor.py`:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'YOUR_PATH\tesseract.exe'
   ```

### ❌ Barcode not detected from webcam
**Solution:**
- Ensure good lighting
- Hold barcode steady and clear
- Make sure numbers below barcode are visible
- Try using manual input instead

### ❌ Camera not working in Streamlit
**Solution:**
- Allow camera permissions in your browser
- Refresh the page
- Use manual barcode input as alternative

### ❌ Groq API Error
**Solution:**
- Check your `.env` file has the correct API key
- Verify you haven't exceeded free tier limits
- Check internet connection

### ❌ Product not found
**Solution:**
- Not all products are in OpenFoodFacts database
- Try the sample barcodes in the sidebar
- Try a different product

---

## Quick Test

After installation, try this barcode to verify everything works:

**Coca-Cola:** `5449000000996`

1. Go to "Manual Input" tab
2. Enter: `5449000000996`
3. Click "Analyze Product"
4. You should see results within 5-10 seconds

---

## System Requirements

- **Python:** 3.8 or higher
- **RAM:** 2GB minimum (4GB recommended for EasyOCR)
- **Disk:** 500MB for dependencies
- **Internet:** Required for OpenFoodFacts API and Groq API

---

## What Gets Installed?

The main dependencies are:

1. **Tesseract OCR** - System-level OCR engine
2. **streamlit** - Web UI framework
3. **langchain-groq** - Groq LLM integration
4. **opencv-python** - Image processing
5. **pytesseract** - Python wrapper for Tesseract
6. **requests** - API calls to OpenFoodFacts

Total install size: ~200-300MB

---

## Next Steps

Once the app is running:

1. Try the webcam feature
2. Test manual barcode input
3. Check the sample barcodes in sidebar
4. View detailed nutrition facts
5. Compare different products

Enjoy! 🥗
