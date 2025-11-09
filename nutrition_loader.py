"""
Nutrition Loader Module
Fetches nutrition data from OpenFoodFacts and calculates health score using WHO/FDA guidelines
"""

import requests
import os
from dotenv import load_dotenv
# Keep LangChain imports for future AI features
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from benchmarks import calculate_who_fda_score

load_dotenv()


class NutritionLoader:
    def __init__(self):
        self.api_base = "https://world.openfoodfacts.org/api/v0"
        self.llm = ChatGroq(
            model_name="llama-3.3-70b-versatile",  # Updated to current model
            temperature=0.1,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

    def fetch_product_data(self, barcode):
        """
        Fetch product data from OpenFoodFacts API

        Args:
            barcode: str - Product barcode

        Returns:
            dict: Product data or None if not found
        """
        try:
            url = f"{self.api_base}/product/{barcode}.json"
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()

                if data.get("status") == 1:
                    return data.get("product", {})

            return None

        except Exception as e:
            print(f"Error fetching product data: {e}")
            return None

    def extract_nutrition_info(self, product_data):
        """
        Extract relevant nutrition information

        Args:
            product_data: dict

        Returns:
            dict: Structured nutrition info
        """
        if not product_data:
            return None

        nutrition = {
            "product_name": product_data.get("product_name", "Unknown Product"),
            "brands": product_data.get("brands", "Unknown"),
            "categories": product_data.get("categories", "Unknown"),
            "ingredients_text": product_data.get("ingredients_text", "Not available"),
            "nutriments": {
                "energy_kcal": product_data.get("nutriments", {}).get("energy-kcal_100g", "N/A"),
                "fat": product_data.get("nutriments", {}).get("fat_100g", "N/A"),
                "saturated_fat": product_data.get("nutriments", {}).get("saturated-fat_100g", "N/A"),
                "carbohydrates": product_data.get("nutriments", {}).get("carbohydrates_100g", "N/A"),
                "sugars": product_data.get("nutriments", {}).get("sugars_100g", "N/A"),
                "fiber": product_data.get("nutriments", {}).get("fiber_100g", "N/A"),
                "proteins": product_data.get("nutriments", {}).get("proteins_100g", "N/A"),
                "salt": product_data.get("nutriments", {}).get("salt_100g", "N/A"),
                "sodium": product_data.get("nutriments", {}).get("sodium_100g", "N/A"),
            },
            "nutriscore_grade": product_data.get("nutriscore_grade", "N/A"),
            "image_url": product_data.get("image_url", "")
        }

        return nutrition

    def calculate_health_score(self, nutrition_info):
        """
        Calculate health score using WHO/FDA guidelines

        Args:
            nutrition_info: dict

        Returns:
            dict: {score: int (0-100), band: str (A-E), good_points: list, concerns: list, explanation: str, citations: list}
        """
        if not nutrition_info:
            return None

        # Get nutriments
        nutrients = nutrition_info["nutriments"]

        # Calculate score using WHO/FDA benchmarks
        score_result = calculate_who_fda_score(nutrients)

        # Format good points from bonuses
        good_points = []
        for bonus in score_result["breakdown"]["bonuses"]:
            good_points.append(f"{bonus['factor']}: {bonus['value']}")

        # Format concerns from penalties
        concerns = []
        for penalty in score_result["breakdown"]["penalties"]:
            concerns.append(f"{penalty['factor']}: {penalty['value']} (threshold: {penalty['threshold']})")

        # Generate explanation
        explanation = self._generate_explanation(
            nutrition_info["product_name"],
            score_result["score"],
            score_result["band"],
            len(good_points),
            len(concerns)
        )

        return {
            "score": score_result["score"],
            "band": score_result["band"],
            "good_points": good_points if good_points else ["No significant positive nutritional factors"],
            "concerns": concerns if concerns else ["No major nutritional concerns identified"],
            "explanation": explanation,
            "citations": score_result["citations"],
            "breakdown": score_result["breakdown"]
        }

    def _generate_explanation(self, product_name, score, band, good_count, concern_count):
        """
        Generate a human-readable explanation of the score

        Args:
            product_name: str
            score: int
            band: str
            good_count: int
            concern_count: int

        Returns:
            str: Explanation text
        """
        band_descriptions = {
            "A": "excellent nutritional quality",
            "B": "good nutritional quality",
            "C": "acceptable nutritional quality",
            "D": "poor nutritional quality",
            "E": "very poor nutritional quality"
        }

        description = band_descriptions.get(band, "moderate nutritional quality")

        if concern_count == 0 and good_count > 0:
            return f"{product_name} scores {score}/100 (Band {band}), indicating {description}. This product has {good_count} positive nutritional factor{'s' if good_count != 1 else ''} with no major concerns based on WHO/FDA guidelines."
        elif concern_count > 0 and good_count == 0:
            return f"{product_name} scores {score}/100 (Band {band}), indicating {description}. This product has {concern_count} nutritional concern{'s' if concern_count != 1 else ''} based on WHO/FDA guidelines."
        elif concern_count > 0 and good_count > 0:
            return f"{product_name} scores {score}/100 (Band {band}), indicating {description}. This product has {good_count} positive factor{'s' if good_count != 1 else ''} but also {concern_count} concern{'s' if concern_count != 1 else ''} based on WHO/FDA guidelines."
        else:
            return f"{product_name} scores {score}/100 (Band {band}), indicating {description} based on WHO/FDA nutrition guidelines."

    def analyze_product(self, barcode):
        """
        Complete pipeline: fetch data -> calculate score

        Args:
            barcode: str

        Returns:
            dict: Complete analysis or None
        """
        # Fetch product data
        product_data = self.fetch_product_data(barcode)

        if not product_data:
            return None

        # Extract nutrition info
        nutrition_info = self.extract_nutrition_info(product_data)

        # Calculate score
        score_data = self.calculate_health_score(nutrition_info)

        # Combine results
        return {
            "nutrition": nutrition_info,
            "score": score_data
        }
