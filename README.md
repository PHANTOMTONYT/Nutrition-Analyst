# Nutrition Analyst

A comprehensive nutrition analysis application that scans product barcodes and provides detailed health scores based on official nutrition guidelines.

## Features

- **Multi-input Barcode Scanning** - Webcam capture, image upload, or manual entry
- **Real Nutrition Data** - Fetches from OpenFoodFacts database (2M+ products)
- **WHO/FDA Rule-Based Scoring** - Transparent, scientifically-validated health scores (0-100)
- **Official Citations** - Every score backed by WHO, FDA, and UK FSA guidelines
- **Health Insights** - Clear breakdown of positive factors and concerns
- **Official Nutri-Score** - Displays official EU Nutri-Score when available
- **Rich Visualizations** - Color-coded health bands, nutrition facts, and ingredient lists
- **Offline Capable** - No API costs for scoring (only for data fetching)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                      (Streamlit - app.py)                       │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Webcam     │  │ Upload Image │  │ Manual Input │         │
│  │   Scanner    │  │              │  │   Barcode    │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                  │                  │                 │
│         └──────────────────┴──────────────────┘                 │
│                            │                                    │
└────────────────────────────┼────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BARCODE EXTRACTION                           │
│                 (barcode_extractor.py)                          │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐      │
│  │  Method 1: pyzbar (Preferred)                        │      │
│  │  - Dedicated barcode scanner library                 │      │
│  │  - Fast & accurate                                   │      │
│  │  - Supports: EAN-13, UPC-A, UPC-E, Code128, etc.    │      │
│  └──────────────────────────────────────────────────────┘      │
│                             │                                   │
│                             ▼ (if fails)                        │
│  ┌──────────────────────────────────────────────────────┐      │
│  │  Method 2: Tesseract OCR (Fallback)                 │      │
│  │  - Image preprocessing (grayscale, threshold)        │      │
│  │  - OCR text extraction                               │      │
│  │  - Pattern matching (8-13 digit sequences)          │      │
│  └──────────────────────────────────────────────────────┘      │
│                             │                                   │
│                             ▼                                   │
│                    Validated Barcode                            │
└────────────────────────────┼────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   NUTRITION DATA LOADING                        │
│                   (nutrition_loader.py)                         │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐      │
│  │  Step 1: Fetch Product Data                         │      │
│  │  API: OpenFoodFacts                                  │      │
│  │  URL: https://world.openfoodfacts.org/api/v0        │      │
│  │  Endpoint: /product/{barcode}.json                  │      │
│  └──────────────────────────────────────────────────────┘      │
│                             │                                   │
│                             ▼                                   │
│  ┌──────────────────────────────────────────────────────┐      │
│  │  OpenFoodFacts Response:                             │      │
│  │  - Product name, brand, category                     │      │
│  │  - Nutrition facts (per 100g)                        │      │
│  │  - Ingredients list                                  │      │
│  │  - Official Nutri-Score                              │      │
│  │  - Product images                                    │      │
│  └──────────────────────────────────────────────────────┘      │
│                             │                                   │
│                             ▼                                   │
│  ┌──────────────────────────────────────────────────────┐      │
│  │  Step 2: Extract & Structure Data                   │      │
│  │  - Parse nutriments (per 100g):                      │      │
│  │    • Energy (kcal)                                   │      │
│  │    • Fat & Saturated Fat                             │      │
│  │    • Carbs & Sugars                                  │      │
│  │    • Fiber & Protein                                 │      │
│  │    • Salt & Sodium                                   │      │
│  └──────────────────────────────────────────────────────┘      │
└────────────────────────────┼────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     HEALTH SCORE CALCULATION                    │
│                    (nutrition_loader.py)                        │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐      │
│  │  WHO/FDA Rule-Based Scoring (benchmarks.py)         │      │
│  │  Method: Transparent penalty/bonus system           │      │
│  │                                                       │      │
│  │  Input: Nutrition data (per 100g)                   │      │
│  │  Processing:                                          │      │
│  │  - Starts with 100 points                            │      │
│  │  - Applies penalties for high sugar, sat fat, sodium│      │
│  │  - Adds bonuses for high fiber, protein             │      │
│  │  - Uses official WHO/FDA/UK FSA thresholds          │      │
│  │                                                       │      │
│  │  Output:                                              │      │
│  │  - Health Score (0-100)                               │      │
│  │  - Grade Band (A/B/C/D/E)                            │      │
│  │  - Good Points with values                           │      │
│  │  - Concerns with thresholds                          │      │
│  │  - Scientific Citations                              │      │
│  │  - Detailed Explanation                              │      │
│  └──────────────────────────────────────────────────────┘      │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐      │
│  │  Reference: WHO/FDA Benchmarks (benchmarks.py)       │      │
│  │  - WHO Sugar Guidelines (2015)                       │      │
│  │  - FDA Daily Reference Values (2016)                 │      │
│  │  - UK Traffic Light System (2013)                    │      │
│  │  - EU Fiber Standards (2006)                         │      │
│  │  - Nutri-Score System (2017)                         │      │
│  └──────────────────────────────────────────────────────┘      │
└────────────────────────────┼────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      RESULTS DISPLAY                            │
│                      (Streamlit UI)                             │
│                                                                 │
│  ┌────────────────────────────────────────────────────┐        │
│  │  Product Information                               │        │
│  │  - Name, Brand, Category                           │        │
│  │  - Product Image                                   │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                 │
│  ┌────────────────────────────────────────────────────┐        │
│  │  Health Score Card                                 │        │
│  │  ┌──────────────────────────────────┐              │        │
│  │  │  Health Score: 75/100            │              │        │
│  │  │  Band: B                          │              │        │
│  │  └──────────────────────────────────┘              │        │
│  │  Color-coded by band (A=Green → E=Red)             │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                 │
│  ┌─────────────────────┐  ┌─────────────────────────┐         │
│  │  ✅ Good Points     │  │  ❌ Concerns            │         │
│  │  - High fiber       │  │  - High sugar content   │         │
│  │  - Good protein     │  │  - Processed ingredients│         │
│  └─────────────────────┘  └─────────────────────────┘         │
│                                                                 │
│  ┌────────────────────────────────────────────────────┐        │
│  │  Ingredients List                                  │        │
│  │  Full ingredient breakdown                         │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                 │
│  ┌────────────────────────────────────────────────────┐        │
│  │  Detailed Explanation                              │        │
│  │  AI-generated health insights                      │        │
│  └────────────────────────────────────────────────────┘        │
│                                                                 │
│  ┌────────────────────────────────────────────────────┐        │
│  │  Nutrition Facts (per 100g)                        │        │
│  │  - Energy, Fat, Carbs, Sugar, Fiber, Protein, Salt │        │
│  │  - Official Nutri-Score                            │        │
│  └────────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Sequence

1. **User Input** → Barcode (via webcam/upload/manual)
2. **Barcode Extraction** → Validated barcode number
3. **API Call** → OpenFoodFacts database
4. **Data Retrieval** → Nutrition facts + product info
5. **WHO/FDA Scoring** → Rule-based analysis with official thresholds
6. **Score Calculation** → 0-100 score + A-E band + citations
7. **Results Display** → Comprehensive health report with scientific backing

---

## Technology Stack

### Frontend
- **Streamlit** - Web UI framework
- **Pillow (PIL)** - Image processing
- **OpenCV** - Computer vision operations

### Barcode Processing
- **pyzbar** - Primary barcode scanner
- **pytesseract** - Fallback OCR engine

### Backend
- **Requests** - HTTP client for API calls
- **LangChain** - (Reserved for future AI features)
- **Python** - Rule-based scoring algorithms

### Data Sources
- **OpenFoodFacts API** - Nutrition database (2M+ products)
- **WHO/FDA Guidelines** - Scientific benchmarks for scoring

---

## Module Breakdown

### 1. `app.py` (Main Application)
**Responsibilities:**
- Streamlit UI rendering
- User input handling (webcam/upload/manual)
- Session state management
- Results visualization
- Color-coded health score display

**Key Features:**
- Three input methods (webcam, file upload, manual)
- Real-time barcode scanning
- Interactive analysis button
- Detailed nutrition facts display
- Expandable sections for detailed info

### 2. `barcode_extractor.py` (Barcode Detection)
**Responsibilities:**
- Extract barcodes from images
- Two-tier detection system
- Barcode validation

**Functions:**
- `extract_barcode_with_pyzbar()` - Primary detection
- `extract_barcode_with_ocr()` - Fallback detection
- `extract_barcode_from_image()` - Main interface
- `validate_barcode()` - Format validation (8-13 digits)

**Supported Formats:**
- EAN-13, EAN-8
- UPC-A, UPC-E
- Code128, Code39
- ISBN-10, ISBN-13

### 3. `nutrition_loader.py` (Data & Analysis)
**Responsibilities:**
- Fetch product data from OpenFoodFacts
- Extract and structure nutrition info
- Calculate health scores using WHO/FDA benchmarks
- Format results with citations

**Functions:**
- `fetch_product_data()` - API communication
- `extract_nutrition_info()` - Data structuring
- `calculate_health_score()` - WHO/FDA rule-based scoring
- `_generate_explanation()` - Human-readable summary
- `analyze_product()` - Complete pipeline

**API Integration:**
- Endpoint: `https://world.openfoodfacts.org/api/v0/product/{barcode}.json`
- Response parsing and error handling
- Nutriment extraction (per 100g standardization)

### 4. `benchmarks.py` (Scientific References)
**Responsibilities:**
- Store WHO/FDA reference values
- Define scoring thresholds
- Provide citations and explanations
- **PRIMARY SCORING ENGINE** - Rule-based algorithms

**Key References:**
- WHO Sugar Guidelines (2015)
- FDA Daily Reference Values (2016)
- UK Food Standards Agency Traffic Light Labelling (2013)
- EU Nutrition Claims Regulation (2006)
- Nutri-Score System (2017)
- NOVA Food Classification (2019)

**Functions:**
- `calculate_who_fda_score()` - **PRIMARY** rule-based scoring with penalties/bonuses
- `get_all_citations()` - Reference documentation

---

## Scoring Methodology

### Current System (WHO/FDA Rule-Based)
The system uses transparent, scientifically-validated scoring:

**Algorithm:**
1. **Starts with 100 points**
2. **Applies penalties** for nutrients to limit:
   - High sugar (>22.5g per 100g): up to -30 points
   - High saturated fat (>5g per 100g): up to -25 points
   - High sodium (>600mg per 100g): up to -25 points
   - High calorie density (>400 kcal per 100g): up to -10 points
3. **Adds bonuses** for beneficial nutrients:
   - Very high fiber (≥12g per 100g): +15 points
   - High fiber (≥6g per 100g): +8 points
   - Good protein (≥10g per 100g): +10 points
4. **Clamps score** to 0-100 range
5. **Assigns band** based on final score

**Score Bands:**
- **A (80-100):** Excellent nutritional quality
- **B (60-79):** Good nutritional quality
- **C (40-59):** Acceptable nutritional quality
- **D (20-39):** Poor nutritional quality
- **E (0-19):** Very poor nutritional quality

**Scientific Basis:**
- WHO Sugar Guidelines (2015)
- FDA Daily Reference Values (2016)
- UK Traffic Light Labelling System (2013)
- EU Nutrition Claims Regulation (2006)

**Advantages:**
- ✅ Transparent and reproducible
- ✅ No API costs
- ✅ Works offline
- ✅ Backed by official citations
- ✅ Consistent scoring

---

## API Dependencies

### OpenFoodFacts API
- **Free & Open Source**
- **No API Key Required**
- **Coverage:** 2M+ products worldwide
- **Data Quality:** Community-maintained, varies by product
- **Rate Limits:** None specified (reasonable use)

### Scoring
- **No API Required** - Rule-based scoring runs locally
- **Cost:** FREE
- **Speed:** Instant (<0.1 seconds)
- **Offline:** Works without internet (after data is fetched)

### Future AI Features (Optional)
- **Groq API** - Reserved for future AI enhancements
- **LangChain** - Integrated for potential AI features
- Currently not used for scoring

---

## Setup

### 1. Install Barcode Scanner (Choose One)

#### Option A: Install ZBar (RECOMMENDED for webcam barcode detection)

For best webcam barcode detection, install ZBar library:

**Windows (Easiest with Conda):**
```bash
conda install -c conda-forge pyzbar
```

**Windows (Manual):** See [INSTALL_ZBAR.md](INSTALL_ZBAR.md) for detailed instructions

**Linux:**
```bash
sudo apt-get install libzbar0
pip install pyzbar
```

**macOS:**
```bash
brew install zbar
pip install pyzbar
```

#### Option B: Use Tesseract OCR (Fallback - less reliable for webcam)

If you can't install ZBar, the app will fall back to Tesseract OCR:

**Windows:**
1. Download Tesseract installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer (recommended path: `C:\Program Files\Tesseract-OCR`)
3. Add Tesseract to PATH or set it in code:
   ```python
   # If needed, add this line to barcode_extractor.py
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

### 2. Install Python Dependencies

```bash
cd langchain/nutrition_analyst
pip install -r requirements.txt
```

### 3. Set up Environment Variables (Optional)

**Note:** Not required for basic functionality. Scoring works without any API keys.

If you want to enable future AI features, create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your Groq API key:

```
GROQ_API_KEY=your_actual_groq_api_key
```

**Note:** Groq API is optional and only needed for future AI features. The WHO/FDA scoring works without it.

### 4. Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## How to Use

### Method 1: Webcam Scan
1. Click on the "Webcam" tab
2. Allow camera access
3. Show a product barcode to your camera
4. The barcode will be automatically detected
5. Click "Analyze Product"

### Method 2: Manual Input
1. Click on the "Manual Input" tab
2. Type the barcode number (8-13 digits)
3. Click "Analyze Product"

### Test Barcodes

Try these sample barcodes:
- **Coca-Cola:** `5449000000996`
- **Nutella:** `3017620422003`
- **Almonds:** `737628064502`
- **Yogurt:** `3229820787015`

## Project Structure

```
nutrition_analyst/
├── app.py                    # Main Streamlit UI
├── barcode_extractor.py      # Barcode detection (pyzbar + OCR)
├── nutrition_loader.py       # API calls + WHO/FDA scoring
├── benchmarks.py            # WHO/FDA guidelines & rule-based scoring
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (optional)
└── README.md               # This documentation
```

---

## Scientific References

All scoring is based on official guidelines:

### 1. **WHO (World Health Organization)**
- Sugar intake guidelines (2015)
- Sodium intake guidelines (2012)
- Diet and chronic disease prevention (2003)

### 2. **FDA (Food and Drug Administration)**
- Daily Reference Values (2016)
- Nutrition Facts Label standards

### 3. **UK Food Standards Agency**
- Traffic Light Labelling System (2013)

### 4. **European Union**
- Nutrition and Health Claims Regulation (2006)
- Nutri-Score System (Santé Publique France, 2017)

### 5. **NOVA Food Classification**
- Monteiro et al. (2019)
- UN FAO/WHO recognized processing classification

---

## Future Enhancements

### Potential Improvements:
1. **AI-Powered Personalization**
   - Use LangChain + Groq for dietary recommendations
   - Personalized health insights based on user goals
   - Allergen detection and warnings

2. **Multi-Score Dashboard**
   - Show official Nutri-Score prominently
   - Add UK Traffic Light indicators
   - Display NOVA classification
   - WHO/FDA compliance badges

3. **Offline Mode**
   - Cache product data locally
   - Pre-download common products database
   - Reduce API dependencies

4. **Export Features**
   - PDF report generation
   - Product comparison mode
   - History tracking

5. **Enhanced Barcode Support**
   - QR code scanning
   - Batch product scanning
   - Product recommendations

## Troubleshooting

### Camera not working?
- Make sure your browser has camera permissions
- Try refreshing the page
- Use manual input as fallback

### Barcode not detected?
- Ensure good lighting
- Hold barcode steady and centered
- Try manual input instead

### Product not found?
- Not all products are in OpenFoodFacts database
- Try a different product
- Check barcode number is correct

### Scoring not working?
- WHO/FDA scoring works offline and doesn't need API keys
- Ensure product has valid nutrition data in OpenFoodFacts
- Check that nutriments are available (not "N/A")

---

## License & Credits

- **OpenFoodFacts:** Open Database License (ODbL)
- **WHO/FDA Guidelines:** Public domain (official government guidelines)
- **pyzbar:** MIT License
- **Streamlit:** Apache License 2.0
- **LangChain:** MIT License

---

## Support

For issues or questions:
- Check OpenFoodFacts database: https://world.openfoodfacts.org
- Verify barcode is valid and in database
- Review WHO/FDA scoring methodology in `benchmarks.py`

---

Made with Streamlit, LangChain, and WHO/FDA Guidelines
