
"Nutrition Analyst "
import streamlit as st
from PIL import Image
import cv2
import numpy as np

from barcode_extractor import extract_barcode_from_image, validate_barcode
from nutrition_loader import NutritionLoader


# Page config
st.set_page_config(
    page_title="Nutrition Analyst",
    page_icon="🥗",
    layout="wide"
)

# Initialize session state
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'barcode' not in st.session_state:
    st.session_state.barcode = ""

# Initialize nutrition loader
@st.cache_resource
def get_nutrition_loader():
    return NutritionLoader()

nutrition_loader = get_nutrition_loader()


# Header
st.title("🥗 Nutrition Analyst")
st.markdown("**Extract barcode from webcam or enter manually to get WHO/FDA-based health score**")
st.caption("Scoring based on official WHO, FDA, and UK Food Standards Agency guidelines")
st.divider()


# Main layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📸 Input")

    # Input method tabs
    input_tab1, input_tab2, input_tab3 = st.tabs(["📹 Webcam", "📤 Upload Image", "⌨️ Manual Input"])

    with input_tab1:
        st.write("Capture barcode using your webcam")

        # Camera input
        camera_image = st.camera_input("Show barcode to camera")

        if camera_image:
            # Convert to PIL Image
            image = Image.open(camera_image)

            # Extract barcode
            with st.spinner("Extracting barcode..."):
                barcode = extract_barcode_from_image(image)

            if barcode:
                st.success(f"✅ Barcode detected: **{barcode}**")
                st.session_state.barcode = barcode
            else:
                st.error("❌ No barcode detected. Try again or use manual input.")

    with input_tab2:
        st.write("Upload an image containing a barcode")

        # File uploader
        uploaded_file = st.file_uploader(
            "Choose an image",
            type=["png", "jpg", "jpeg"],
            help="Upload a clear image of the product barcode"
        )

        if uploaded_file:
            # Convert to PIL Image
            image = Image.open(uploaded_file)

            # Display uploaded image
            st.image(image, caption="Uploaded Image", use_container_width=True)

            # Extract barcode
            with st.spinner("Extracting barcode..."):
                barcode = extract_barcode_from_image(image)

            if barcode:
                st.success(f"✅ Barcode detected: **{barcode}**")
                st.session_state.barcode = barcode
            else:
                st.error("❌ No barcode detected. Try again with a clearer image or use manual input.")

    with input_tab3:
        st.write("Enter barcode manually")

        manual_barcode = st.text_input(
            "Barcode Number",
            placeholder="e.g., 737628064502",
            help="Enter 8-13 digit barcode"
        )

        if manual_barcode:
            if validate_barcode(manual_barcode):
                st.session_state.barcode = manual_barcode
                st.success(f"✅ Valid barcode: **{manual_barcode}**")
            else:
                st.error("❌ Invalid barcode format. Use 8-13 digits.")

    # Analyze button - Always visible
    st.divider()

    # Show current barcode if available
    if st.session_state.barcode:
        st.info(f"📦 Current Barcode: **{st.session_state.barcode}**")

    # Button is always visible, but disabled if no barcode
    button_disabled = not bool(st.session_state.barcode)

    if st.button(
        "🔍 Analyze Product",
        type="primary",
        use_container_width=True,
        disabled=button_disabled,
        help="Scan or enter a barcode first" if button_disabled else "Click to analyze product"
    ):
        with st.spinner("Fetching product data..."):
            result = nutrition_loader.analyze_product(st.session_state.barcode)

            if result:
                st.session_state.analysis_result = result
                st.success("✅ Analysis complete!")
            else:
                st.error("❌ Product not found in database. Try another barcode.")
                st.session_state.analysis_result = None


with col2:
    st.subheader("📊 Analysis Results")

    if st.session_state.analysis_result:
        result = st.session_state.analysis_result
        nutrition = result["nutrition"]
        score_data = result["score"]

        # Product info
        st.markdown(f"### {nutrition['product_name']}")
        st.markdown(f"**Brand:** {nutrition['brands']}")
        st.markdown(f"**Category:** {nutrition['categories']}")

        # Display product image if available
        if nutrition.get('image_url'):
            try:
                st.image(nutrition['image_url'], width=200)
            except:
                pass

        st.divider()

        # Health Score
        score = score_data['score']
        band = score_data['band']

        # Color coding for bands
        band_colors = {
            'A': '#2E7D32',  # Green
            'B': '#66BB6A',  # Light Green
            'C': '#FDD835',  # Yellow
            'D': '#FB8C00',  # Orange
            'E': '#E53935'   # Red
        }

        color = band_colors.get(band, '#757575')

        st.markdown(f"""
        <div style="background-color: {color}; padding: 20px; border-radius: 10px; text-align: center;">
            <h1 style="color: white; margin: 0;">Health Score: {score}/100</h1>
            <h2 style="color: white; margin: 0;">Band: {band}</h2>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Score breakdown
        col_good, col_concerns = st.columns(2)

        with col_good:
            st.markdown("### ✅ Good Points")
            if score_data['good_points']:
                for point in score_data['good_points']:
                    st.markdown(f"- {point}")
            else:
                st.markdown("_No significant positive points_")

        with col_concerns:
            st.markdown("### ❌ Concerns")
            if score_data['concerns']:
                for concern in score_data['concerns']:
                    st.markdown(f"- {concern}")
            else:
                st.markdown("_No major concerns_")

        st.divider()

        # Ingredients - Show prominently
        st.markdown("### 🧪 Ingredients")
        if nutrition['ingredients_text'] and nutrition['ingredients_text'] != "Not available":
            st.write(nutrition['ingredients_text'])
        else:
            st.warning("Ingredients information not available in database")

        st.divider()

        # Explanation
        st.markdown("### 💡 Explanation")
        st.info(score_data['explanation'])

        st.divider()

        # Scientific Citations
        if 'citations' in score_data and score_data['citations']:
            st.markdown("### 📚 Scientific Citations")
            st.markdown("This score is based on official nutrition guidelines:")
            for citation in score_data['citations']:
                st.markdown(f"- {citation}")
            st.caption("Scoring uses WHO/FDA guidelines, UK Traffic Light System, and EU nutrition regulations")

        st.divider()

        # Nutrition Facts
        with st.expander("📋 Detailed Nutrition Facts (per 100g)"):
            nutrients = nutrition['nutriments']

            col_a, col_b = st.columns(2)

            with col_a:
                st.metric("Energy", f"{nutrients['energy_kcal']} kcal")
                st.metric("Fat", f"{nutrients['fat']}g")
                st.metric("Saturated Fat", f"{nutrients['saturated_fat']}g")
                st.metric("Carbohydrates", f"{nutrients['carbohydrates']}g")

            with col_b:
                st.metric("Sugars", f"{nutrients['sugars']}g")
                st.metric("Fiber", f"{nutrients['fiber']}g")
                st.metric("Protein", f"{nutrients['proteins']}g")
                st.metric("Salt", f"{nutrients['salt']}g")

        # Official Nutriscore
        if nutrition['nutriscore_grade'] != "N/A":
            st.markdown(f"**Official Nutri-Score:** {nutrition['nutriscore_grade'].upper()}")

    else:
        st.info("👈 Scan or enter a barcode to see analysis")


st.divider()

st.markdown("### ℹ️ How It Works")
st.markdown("""
    1. **Scan** barcode via webcam or **enter** manually
    2. System fetches nutrition data from OpenFoodFacts
    3. WHO/FDA guidelines calculate health score (0-100)
    4. Get science-backed insights with official citations
    """)
