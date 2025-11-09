"""
Barcode Extractor Module
Extracts barcodes from webcam images using pyzbar (preferred) or Tesseract OCR (fallback)
"""

import cv2
from PIL import Image
import numpy as np
import re
import os
import platform

# Try to import pyzbar (recommended for barcode scanning)
try:
    from pyzbar.pyzbar import decode as pyzbar_decode
    PYZBAR_AVAILABLE = True
    print("[OK] pyzbar available - using dedicated barcode scanner")
except ImportError:
    PYZBAR_AVAILABLE = False
    print("[WARNING] pyzbar not available - falling back to Tesseract OCR")
    print("   For better barcode detection, install ZBar: https://github.com/UB-Mannheim/tesseract/wiki")

# Import Tesseract as fallback
try:
    import pytesseract
    TESSERACT_AVAILABLE = True

    # Auto-configure Tesseract path for Windows
    if platform.system() == "Windows":
        possible_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            r"C:\Tesseract-OCR\tesseract.exe",
        ]
        for path in possible_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                break
except ImportError:
    TESSERACT_AVAILABLE = False
    print("[WARNING] Tesseract not available")


def extract_barcode_with_pyzbar(image):
    """
    Extract barcode using pyzbar (RECOMMENDED - fast and accurate)

    Args:
        image: numpy array

    Returns:
        str: Barcode number if found, None otherwise
    """
    if not PYZBAR_AVAILABLE:
        return None

    # pyzbar works on grayscale or color images
    decoded_objects = pyzbar_decode(image)

    if decoded_objects:
        # Return the first barcode found
        barcode_data = decoded_objects[0].data.decode('utf-8')
        return barcode_data

    return None


def preprocess_image_for_ocr(image):
    """
    Preprocess image to improve OCR accuracy for barcodes

    Args:
        image: numpy array

    Returns:
        numpy array: Preprocessed image
    """
    # Convert to grayscale
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image

    # Apply thresholding to make barcode numbers clearer
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Denoise
    denoised = cv2.fastNlMeansDenoising(thresh)

    return denoised


def extract_barcode_with_ocr(image):
    """
    Extract barcode using Tesseract OCR (FALLBACK - slower and less accurate)

    Args:
        image: numpy array

    Returns:
        str: Barcode number if found, None otherwise
    """
    if not TESSERACT_AVAILABLE:
        return None

    # Preprocess image
    processed = preprocess_image_for_ocr(image)

    # Try OCR with digit-only configuration
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
    text = pytesseract.image_to_string(processed, config=custom_config)

    # Clean extracted text
    cleaned = re.sub(r'\D', '', text)  # Remove non-digits

    # Look for barcode-like sequences (8-13 consecutive digits)
    barcode_pattern = re.findall(r'\d{8,13}', cleaned)

    if barcode_pattern:
        # Return the longest sequence found (most likely the barcode)
        return max(barcode_pattern, key=len)

    # If no match, try again with original image (sometimes preprocessing hurts)
    text = pytesseract.image_to_string(image, config=custom_config)
    cleaned = re.sub(r'\D', '', text)
    barcode_pattern = re.findall(r'\d{8,13}', cleaned)

    if barcode_pattern:
        return max(barcode_pattern, key=len)

    return None


def extract_barcode_from_image(image):
    """
    Extract barcode from an image using pyzbar (preferred) or OCR (fallback)

    Args:
        image: PIL Image or numpy array

    Returns:
        str: Barcode number if found, None otherwise
    """
    # Convert PIL Image to numpy array if needed
    if isinstance(image, Image.Image):
        image = np.array(image)

    # Method 1: Try pyzbar first (MUCH better for barcodes)
    if PYZBAR_AVAILABLE:
        barcode = extract_barcode_with_pyzbar(image)
        if barcode:
            return barcode

    # Method 2: Fallback to OCR (slower, less reliable)
    if TESSERACT_AVAILABLE:
        barcode = extract_barcode_with_ocr(image)
        if barcode:
            return barcode

    return None


def extract_barcode_from_webcam():
    """
    Capture image from webcam and extract barcode

    Returns:
        tuple: (barcode_number, captured_image) or (None, None)
    """
    # Open webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return None, None

    # Capture frame
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return None, None

    # Convert BGR to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Extract barcode
    barcode = extract_barcode_from_image(frame_rgb)

    return barcode, frame_rgb


def validate_barcode(barcode):
    """
    Basic barcode validation

    Args:
        barcode: str

    Returns:
        bool: True if valid barcode format
    """
    if not barcode:
        return False

    # Check if numeric and reasonable length (8-13 digits for most barcodes)
    if barcode.isdigit() and 8 <= len(barcode) <= 13:
        return True

    return False
