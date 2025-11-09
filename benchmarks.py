"""
Nutrition Benchmarks and Citations Module
Contains scientifically validated benchmarks and references for nutrition scoring
"""

# WHO/FDA Daily Reference Values
# Source: WHO Guideline: Sugars intake for adults and children (2015)
# Source: FDA Daily Reference Values (2016)
DAILY_REFERENCE_VALUES = {
    "energy_kcal": {
        "reference": 2000,
        "unit": "kcal",
        "citation": "FDA Daily Reference Values (2016)",
        "url": "https://www.fda.gov/food/nutrition-facts-label/daily-value-nutrition-and-supplement-facts-labels"
    },
    "sugar": {
        "max_daily": 50,  # grams
        "max_percent_calories": 10,
        "unit": "g",
        "citation": "WHO Guideline: Sugars intake for adults and children (2015)",
        "url": "https://www.who.int/publications/i/item/9789241549028",
        "explanation": "WHO strongly recommends reducing free sugars to less than 10% of total energy intake"
    },
    "saturated_fat": {
        "max_daily": 20,  # grams (for 2000 kcal diet)
        "max_percent_calories": 10,
        "unit": "g",
        "citation": "WHO Diet, nutrition and the prevention of chronic diseases (2003)",
        "url": "https://www.who.int/publications/i/item/924120916X",
        "explanation": "Saturated fat intake should be less than 10% of total energy intake"
    },
    "sodium": {
        "max_daily": 2000,  # mg
        "unit": "mg",
        "citation": "WHO Guideline: Sodium intake for adults and children (2012)",
        "url": "https://www.who.int/publications/i/item/9789241504836",
        "explanation": "WHO recommends reducing sodium intake to less than 2000 mg/day (5g salt)"
    },
    "fiber": {
        "min_daily": 25,  # grams
        "unit": "g",
        "citation": "FDA Daily Reference Values (2016)",
        "url": "https://www.fda.gov/food/nutrition-facts-label/daily-value-nutrition-and-supplement-facts-labels",
        "explanation": "Adequate fiber intake is associated with reduced risk of chronic diseases"
    },
    "protein": {
        "reference_daily": 50,  # grams
        "unit": "g",
        "citation": "FDA Daily Reference Values (2016)",
        "url": "https://www.fda.gov/food/nutrition-facts-label/daily-value-nutrition-and-supplement-facts-labels",
        "explanation": "Daily reference value for protein based on a 2000 kcal diet"
    }
}

# Nutri-Score Official Bands
# Source: Santé Publique France
NUTRISCORE_INFO = {
    "name": "Nutri-Score",
    "citation": "Santé Publique France - Nutri-Score (2017)",
    "url": "https://www.santepubliquefrance.fr/en/nutri-score",
    "explanation": """The Nutri-Score is a front-of-pack nutrition label that converts the nutritional value
    of products into a simple code consisting of 5 letters (A to E) and 5 colors (dark green to red).
    Each product is awarded a score based on a scientific algorithm. This formula takes into account
    nutrients to favor (fiber, protein, fruits, vegetables, legumes, nuts, rapeseed, walnut and olive oils)
    and nutrients to limit (energy, saturated fatty acids, sugars, salt).""",
    "bands": {
        "A": {"color": "Dark Green", "description": "Best nutritional quality"},
        "B": {"color": "Light Green", "description": "Good nutritional quality"},
        "C": {"color": "Yellow", "description": "Acceptable nutritional quality"},
        "D": {"color": "Orange", "description": "Poor nutritional quality"},
        "E": {"color": "Red", "description": "Lowest nutritional quality"}
    }
}

# NOVA Food Classification
# Source: Monteiro et al. (2019)
NOVA_CLASSIFICATION = {
    "name": "NOVA Food Classification",
    "citation": "Monteiro CA, et al. Ultra-processed foods: what they are and how to identify them. Public Health Nutrition (2019)",
    "url": "https://www.fao.org/3/ca5644en/ca5644en.pdf",
    "explanation": """NOVA is a food classification system that categorizes food by the extent and purpose
    of industrial processing. Studies show ultra-processed foods (Group 4) are associated with increased
    risk of obesity, type 2 diabetes, and cardiovascular disease.""",
    "groups": {
        1: "Unprocessed or minimally processed foods",
        2: "Processed culinary ingredients",
        3: "Processed foods",
        4: "Ultra-processed food and drink products"
    }
}

# Scoring Thresholds per 100g
SCORING_THRESHOLDS = {
    "sugar": {
        "low": 5,      # ≤5g = low
        "medium": 22.5,  # >5g and ≤22.5g = medium
        "high": 22.5,    # >22.5g = high
        "citation": "UK Food Standards Agency Traffic Light Labelling (2013)",
        "explanation": "Traffic light criteria for sugar content per 100g"
    },
    "saturated_fat": {
        "low": 1.5,    # ≤1.5g = low
        "medium": 5,   # >1.5g and ≤5g = medium
        "high": 5,     # >5g = high
        "citation": "UK Food Standards Agency Traffic Light Labelling (2013)",
        "explanation": "Traffic light criteria for saturated fat content per 100g"
    },
    "sodium": {
        "low": 0.3,    # ≤0.3g = low (equivalent to 0.75g salt)
        "medium": 1.5,   # >0.3g and ≤1.5g = medium
        "high": 1.5,     # >1.5g = high
        "citation": "UK Food Standards Agency Traffic Light Labelling (2013)",
        "explanation": "Traffic light criteria for sodium/salt content per 100g"
    },
    "fiber": {
        "high": 6,     # ≥6g = high (source of fiber)
        "very_high": 12,  # ≥12g = very high (high in fiber)
        "citation": "EU Nutrition and Health Claims Regulation (2006)",
        "explanation": "EU criteria for 'source of fiber' and 'high in fiber' claims"
    }
}


def calculate_who_fda_score(nutrients):
    """
    Calculate a rule-based health score using WHO/FDA guidelines

    Args:
        nutrients: dict - Nutrition data per 100g

    Returns:
        dict: {
            'score': int (0-100),
            'band': str (A-E),
            'breakdown': dict,
            'citations': list
        }
    """
    score = 100  # Start with perfect score
    breakdown = {
        "penalties": [],
        "bonuses": []
    }
    citations_used = []

    # Extract values (handle "N/A")
    def get_value(key):
        val = nutrients.get(key, 0)
        return float(val) if val != "N/A" and val != "" else 0

    sugar = get_value("sugars")
    sat_fat = get_value("saturated_fat")
    sodium = get_value("sodium") * 1000  # Convert g to mg
    fiber = get_value("fiber")
    protein = get_value("proteins")
    energy = get_value("energy_kcal")

    # PENALTY: High Sugar (per 100g)
    if sugar > SCORING_THRESHOLDS["sugar"]["high"]:
        penalty = min(30, (sugar - SCORING_THRESHOLDS["sugar"]["high"]) * 2)
        score -= penalty
        breakdown["penalties"].append({
            "factor": "High Sugar",
            "value": f"{sugar}g per 100g",
            "penalty": penalty,
            "threshold": f">{SCORING_THRESHOLDS['sugar']['high']}g",
            "citation": SCORING_THRESHOLDS["sugar"]["citation"]
        })
        citations_used.append(SCORING_THRESHOLDS["sugar"]["citation"])
    elif sugar <= SCORING_THRESHOLDS["sugar"]["low"]:
        breakdown["bonuses"].append({
            "factor": "Low Sugar",
            "value": f"{sugar}g per 100g",
            "bonus": 0,
            "threshold": f"≤{SCORING_THRESHOLDS['sugar']['low']}g"
        })

    # PENALTY: High Saturated Fat
    if sat_fat > SCORING_THRESHOLDS["saturated_fat"]["high"]:
        penalty = min(25, (sat_fat - SCORING_THRESHOLDS["saturated_fat"]["high"]) * 3)
        score -= penalty
        breakdown["penalties"].append({
            "factor": "High Saturated Fat",
            "value": f"{sat_fat}g per 100g",
            "penalty": penalty,
            "threshold": f">{SCORING_THRESHOLDS['saturated_fat']['high']}g",
            "citation": SCORING_THRESHOLDS["saturated_fat"]["citation"]
        })
        citations_used.append(SCORING_THRESHOLDS["saturated_fat"]["citation"])

    # PENALTY: High Sodium
    if sodium > 600:  # 600mg per 100g = high
        penalty = min(25, (sodium - 600) / 50)
        score -= penalty
        breakdown["penalties"].append({
            "factor": "High Sodium",
            "value": f"{sodium}mg per 100g",
            "penalty": penalty,
            "threshold": ">600mg per 100g",
            "citation": SCORING_THRESHOLDS["sodium"]["citation"]
        })
        citations_used.append(SCORING_THRESHOLDS["sodium"]["citation"])

    # BONUS: High Fiber
    if fiber >= SCORING_THRESHOLDS["fiber"]["very_high"]:
        bonus = 15
        score += bonus
        breakdown["bonuses"].append({
            "factor": "Very High Fiber",
            "value": f"{fiber}g per 100g",
            "bonus": bonus,
            "threshold": f"≥{SCORING_THRESHOLDS['fiber']['very_high']}g",
            "citation": SCORING_THRESHOLDS["fiber"]["citation"]
        })
        citations_used.append(SCORING_THRESHOLDS["fiber"]["citation"])
    elif fiber >= SCORING_THRESHOLDS["fiber"]["high"]:
        bonus = 8
        score += bonus
        breakdown["bonuses"].append({
            "factor": "High Fiber",
            "value": f"{fiber}g per 100g",
            "bonus": bonus,
            "threshold": f"≥{SCORING_THRESHOLDS['fiber']['high']}g",
            "citation": SCORING_THRESHOLDS["fiber"]["citation"]
        })
        citations_used.append(SCORING_THRESHOLDS["fiber"]["citation"])

    # BONUS: Good Protein Content
    if protein >= 10:  # 10g per 100g is significant
        bonus = 10
        score += bonus
        breakdown["bonuses"].append({
            "factor": "Good Protein Content",
            "value": f"{protein}g per 100g",
            "bonus": bonus,
            "threshold": "≥10g per 100g",
            "citation": DAILY_REFERENCE_VALUES["protein"]["citation"]
        })
        citations_used.append(DAILY_REFERENCE_VALUES["protein"]["citation"])

    # PENALTY: High Calorie Density
    if energy > 400:  # High energy per 100g
        penalty = min(10, (energy - 400) / 50)
        score -= penalty
        breakdown["penalties"].append({
            "factor": "High Calorie Density",
            "value": f"{energy} kcal per 100g",
            "penalty": penalty,
            "threshold": ">400 kcal per 100g"
        })

    # Clamp score to 0-100
    score = max(0, min(100, round(score)))

    # Determine band
    if score >= 80:
        band = "A"
    elif score >= 60:
        band = "B"
    elif score >= 40:
        band = "C"
    elif score >= 20:
        band = "D"
    else:
        band = "E"

    return {
        "score": score,
        "band": band,
        "breakdown": breakdown,
        "citations": list(set(citations_used))  # Remove duplicates
    }


def get_all_citations():
    """
    Return all citations used in the scoring system

    Returns:
        list: List of citation dictionaries
    """
    citations = []

    # Add WHO/FDA citations
    for nutrient, data in DAILY_REFERENCE_VALUES.items():
        if "citation" in data:
            citations.append({
                "title": data["citation"],
                "url": data.get("url", ""),
                "explanation": data.get("explanation", "")
            })

    # Add Nutri-Score citation
    citations.append({
        "title": NUTRISCORE_INFO["citation"],
        "url": NUTRISCORE_INFO["url"],
        "explanation": NUTRISCORE_INFO["explanation"]
    })

    # Add threshold citations
    for nutrient, data in SCORING_THRESHOLDS.items():
        if "citation" in data:
            citations.append({
                "title": data["citation"],
                "url": data.get("url", ""),
                "explanation": data.get("explanation", "")
            })

    # Remove duplicates
    seen = set()
    unique_citations = []
    for citation in citations:
        title = citation["title"]
        if title not in seen:
            seen.add(title)
            unique_citations.append(citation)

    return unique_citations
