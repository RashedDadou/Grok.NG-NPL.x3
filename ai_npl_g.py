# ai_npl_g.py

class AiNplG:
    """AI.NPL(G) - Geometric Design"""

    CAR_TYPES = {
        "mustang": "Ford Mustang classic, strong muscular lines, long hood, distinctive front grille",
        "classic": "American classic car, balanced design, smooth curves with sharp edges",
        "ford": "Ford car, strong American design, prominent metal details",
        "mercedes": "Elegant Mercedes, smooth lines, prominent star emblem",
        # Add any other brands you like here
    }

    def _extract_car_features(self, prompt: str) -> dict:
        lower = prompt.lower()
        model = next((k for k in self.CAR_TYPES if k in lower), None)
        color = next((w for w in ["red", "black", "white", "blue", "silver", "gold"] if w in lower), "dark glossy")
        return {"model": model, "color": color}

    def process(self, enriched_prompt: str):
        features = self._extract_car_features(enriched_prompt)

        desc = [
            "Strong visual composition, low or 3/4 angle to highlight the car",
            "Rule of thirds or golden ratio for balanced elements",
            "Balanced negative space around the car and cat",
        ]

        if features["model"]:
            desc.append(f"Precise geometry for {self.CAR_TYPES[features['model']]}, realistic proportions, sharp metal details")
        if features["color"]:
            desc.append(f"{features['color']} surface with accurate environmental reflections")

        desc.append("Clean geometric shapes for the garage: walls, floor, hanging tools")

        return (
            f"Geometric composition and layout for: {enriched_prompt}\n"
            "– " + "\n– ".join(desc)
        )