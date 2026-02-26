# ai_npl_e.py

class AiNplE:
    """AI.NPL(E) - Environment Design"""

    ENV_MOODS = {
        "old": "old garage, accumulated dust, warm dim lighting",
        "dusty": "dusty atmosphere, dust particles floating in light rays",
        "dim": "dim fluorescent or single hanging bulb lighting, long shadows",
        "dark": "dark moody garage, low-key lighting, deep shadows",
        "bright": "bright garage, natural light from windows, clean feel",
        # Add any other environment moods you like
    }

    def _extract_env_features(self, prompt: str) -> str:
        # الدالة القديمة (أو أي منطق استخراج بيئي سابق)
        lower = prompt.lower()
        if "قديم" in lower or "old" in lower:
            return "enclosed old garage, dim industrial lighting, concrete floor with oil stains"
        return "enclosed home garage, industrial dim lighting, concrete floor"

    def process(self, enriched_prompt: str) -> str:
        """
        توليد وصف البيئة مع دمج تأثير الرياح إذا وجدت
        """
        # استخراج سرعة الرياح من الوصف
        wind_speed = 0.0
        lower = enriched_prompt.lower()
        if "رياح" in lower or "wind" in lower:
            for word in lower.split():
                try:
                    # ابحث عن أرقام + "كم" أو "km"
                    if any(unit in word for unit in ["كم", "km", "كم/س", "km/h"]):
                        # استخرج الأرقام فقط
                        num_str = ''.join(c for c in word if c.isdigit() or c == '.')
                        if num_str:
                            wind_speed = float(num_str)
                            break
                except ValueError:
                    pass

        # توليد وصف الرياح
        wind_desc = generate_wind_effect_description(wind_speed)

        # الجزء البيئي الأساسي
        env_base = self._extract_env_features(enriched_prompt)

        # دمج تأثير الرياح إذا كانت موجودة
        if wind_speed > 0:
            env_base += f", {wind_desc}"

        # بناء القائمة النهائية
        desc = [
            env_base,
            "subtle reflections on the car surface",
            "atmospheric depth layers, soft ambient shadows",
            "small environmental details (oil stains, scattered tools)",
            "mixed warm-cool mood, sense of enclosed space"
        ]

        return (
            f"Environmental atmosphere and lighting for: {enriched_prompt}\n"
            "– " + "\n– ".join(desc)
        )
