# renderer.py    ← ممكن تضعها في ملف منفصل أو في نهاية أي ملف

class RenderingWindow:
    """
    نافذة Rendering موحدة
    تجمع الأجزاء من AI.NPL(G), AI.NPL(E), AI.NPL(T)
    مع إمكانية إعطاء وزن (تكرار أو أولوية) لكل جزء
    """
    
    def __init__(self):
        self.parts = {}
        self.weights = {}   # وزن افتراضي = 1 لكل جزء
    
    def add_part(self, name: str, text: str, weight: float = 1.0):
        """إضافة جزء + وزنه (weight)"""
        self.parts[name] = text.strip()
        self.weights[name] = max(0.0, weight)   # لا وزن سالب
    
    def render(self, base_prompt: str, style_suffix: str = "") -> str:
        """
        Generate the Final Master Prompt
        
        Args:
            base_prompt: The core user description
            style_suffix: General style additions (e.g. --ar 3:2, very detailed, 8k ...)
        
        Returns:
            str: Clean, combined prompt ready for image generation models
        """
        if not self.parts:
            return (base_prompt.strip() + " " + style_suffix.strip()).strip()

        # Start with the base description once
        lines = [base_prompt.strip()]

        # Preferred order: subject → geometry → environment
        order = ["T", "RL", "G", "E"]  # T first (living subjects), then G (structure), then E (atmosphere)

        for key in order:
            if key in self.parts and self.parts[key]:
                part_text = self.parts[key].strip()
                if not part_text:
                    continue

                weight = self.weights.get(key, 1.0)
                if weight <= 0:
                    continue

                # Repeat the part according to weight
                repeat_count = max(1, int(round(weight)))
                for _ in range(repeat_count):
                    lines.append(part_text)

                # Optional: if fractional weight (e.g. 1.5), you can add emphasis later
                # if weight % 1 != 0:
                #     lines[-1] += ", highly emphasized"

        if style_suffix:
            lines.append(style_suffix.strip())

        # Join with double newlines for readability in prompt
        final_prompt = "\n\n".join(lines).strip()

        return final_prompt

# ────────────────────────────────────────────────
# مثال استخدام كامل (copy-paste جاهز)
# ────────────────────────────────────────────────

if __name__ == "__main__":

    # افتراض أن لديك الثلاث كلاسات السابقة
    from ai_npl_g import AiNplG
    from ai_npl_e import AiNplE
    from ai_npl_t import AiNplT

    user_prompt = "قطة على سيارة مركونة داخل كراج منزل"

    g = AiNplG()
    e = AiNplE()
    t = AiNplT()

    renderer = RenderingWindow()

    # أوزان اختيارية (مثال: نريد نبرز الكائن أكثر من البيئة)
    renderer.add_part("G", g.process(user_prompt), weight=1.0)
    renderer.add_part("E", e.process(user_prompt), weight=0.8)
    renderer.add_part("T", t.process(user_prompt), weight=1.4)

    final_prompt = renderer.render(
        base_prompt=user_prompt,
        style_suffix="cinematic lighting, ultra detailed, photorealistic, 8k, sharp focus"
    )

    print("━ Final Master Prompt ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(final_prompt)
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")