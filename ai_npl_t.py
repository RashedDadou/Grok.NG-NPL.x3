# ai_npl_t.py

class AiNplT:
    """AI.NPL(T) - Traditional / Organic beings"""

    CAT_BREEDS = {
        "siamese": "elegant Siamese, short glossy fur with dark points, piercing blue eyes",
        "persian": "long-haired Persian, thick luxurious fur, flat expressive face, large round eyes",
        "domestic": "domestic shorthair cat, medium fur, natural realistic look",
        # add more breeds if you want
    }

    def _extract_cat_features(self, prompt: str) -> dict:
        lower = prompt.lower()
        breed_key = None
        for key in self.CAT_BREEDS:
            if key in lower:
                breed_key = key
                break
        if not breed_key and "cat" in lower:
            breed_key = "domestic"

        color = next((w for w in ["black", "white", "gray", "orange", "calico"] if w in lower), None)
        mood = next((w for w in ["curious", "calm", "mischievous", "playful", "sleepy"] if w in lower), "curious")

        return {"breed": breed_key, "color": color, "mood": mood}

    def process(self, enriched_prompt: str):
        features = self._extract_cat_features(enriched_prompt)

        desc = []
        if features["breed"]:
            desc.append(self.CAT_BREEDS[features["breed"]])
        else:
            desc.append("realistic domestic cat with natural fur and proportions")  # default

        if features["color"]:
            desc.append(f"rich realistic {features['color']} coloring")
        else:
            desc.append("natural fur color variation")

        desc.append(f"{features['mood']} expression, lively and expressive eyes")
        desc.append("fine fur details, natural movement, lighting that highlights organic texture")

        return (
            f"Organic and living subject styling based on: {enriched_prompt}\n"
            "– " + "\n– ".join(desc)
        )