import time
import requests
import json

class AiPrompts:
    """
    المشرف - ينسق ويجمع التفاصيل الناقصة
    """
    def __init__(self):
        # قاعدة بيانات افتراضية بسيطة (يمكن توسيعها لاحقاً)
        self.defaults = {
            "cat": "قطة شائعة قصيرة الشعر، لون رمادي مخطط، عيون خضراء، تعبير فضولي",
            "car": "سيارة كلاسيكية أمريكية من السبعينيات، لون أحمر داكن، حالة جيدة",
            "garage": "كراج منزلي قديم، إضاءة فلورسنت صفراء خافتة، أرضية إسمنتية متسخة قليلاً، أدوات معلقة"
        }

    def clarify_and_enrich(self, user_prompt: str, chat_history=None):
        """
        - يحلل الـ prompt
        - يقرر إذا كان يحتاج توضيح
        - يرجع وصفاً محسّناً جاهزاً للمتخصصين
        """
        enriched = user_prompt.strip()

        # ------------------- تحليل بسيط جداً (يمكن تحسينه بـ LLM لاحقاً)
        has_cat_type   = "سيامي" in enriched or "فارسي" in enriched or "ب Bengal" in enriched.lower()
        has_car_type   = "مرسيدس" in enriched or "فورد" in enriched or "تويوتا" in enriched
        has_env_detail = "حديث" in enriched or "مظلم" in enriched or "مشرق" in enriched or "مليء بالغبار" in enriched

        questions = []

        if not has_cat_type:
            questions.append("هل القطة من سلالة معينة أو لون محدد أو تعبير معين؟ (إذا لا، سأستخدم افتراضي)")
        
        if not has_car_type:
            questions.append("هل السيارة من ماركة أو موديل معين أو سنة محددة؟")

        if not has_env_detail:
            questions.append("هل الكراج/البيئة لها طابع معين (قديم، حديث، نظيف، مهجور، إضاءة معينة...)؟")

        # ------------------- منطق التعامل
        if questions and chat_history is None:
            # المرة الأولى → نسأل المستخدم
            return {
                "need_clarification": True,
                "questions": questions,
                "enriched_prompt": None
            }
        else:
            # لدينا إجابات أو لا نحتاج → نكمل الافتراضي
            final_desc = enriched

            if not has_cat_type:
                final_desc += f"، {self.defaults['cat']}"
            if not has_car_type:
                final_desc += f"، {self.defaults['car']}"
            if not has_env_detail:
                final_desc += f"، {self.defaults['garage']}"

            return {
                "need_clarification": False,
                "questions": [],
                "enriched_prompt": final_desc.strip("، ")
            }

    def ask_supervisor(self, what: str):
        """محاكاة طلب من Grok.Supervisor (في الواقع نطبع السؤال)"""
        print(f"[AI.prompts → Grok.Supervisor] أحتاج معلومات عن: {what}")
        # هنا يمكن وضع استدعاء حقيقي لاحقاً
        return f"معلومات افتراضية عن {what} (من Grok)"
    
    def _call_small_llm(self, prompt: str, model: str = "qwen2.5:7b-instruct") -> str:
        """استدعاء Ollama أو أي endpoint محلي مشابه"""
        start_time = time.time()
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.25,          # منخفض جدًا للدقة
                        "top_p": 0.85,
                        "max_tokens": 512
                    }
                },
                timeout=12                        # حد أقصى 12 ثانية
            )
            response.raise_for_status()
            result = response.json().get("response", "").strip()
            print(f"LLM استجاب في {time.time() - start_time:.2f} ثانية")
            return result
        except Exception as e:
            print(f"خطأ في استدعاء LLM: {e} → نستخدم fallback")
            return ""

    def analyze_and_suggest_questions(self, description: str):
        # ────────────────────────────────────────────────
        # System Prompt مع few-shot examples
        # ────────────────────────────────────────────────
        system_prompt = """
أنت مساعد متخصص في تحسين وصف صورة لتوليد AI (مثل Flux أو Grok Imagine).
مهمتك: اقرأ الوصف، وإذا كان فيه غموض مهم → اقترح 2–4 أسئلة توضيحية فقط.
ركز على:
• الكائنات الحية (نوع/سلالة/لون/عمر/حجم/تعبير/وضعية)
• الأشياء الصناعية (ماركة/موديل/سنة/لون/حالة/تصميم)
• البيئة والجو (طابع/إضاءة/طقس/نظافة/عمق/مزاج)

أخرج فقط JSON صالح 100% بدون أي نص إضافي:
{
  "questions": [
    {"question": "...", "options": ["خيار1", "خيار2", ...] أو null إذا لا خيارات},
    ...
  ]
}
إذا الوصف كافٍ تمامًا ولا يحتاج توضيح → أرجع {"questions": []}

أمثلة (few-shot):

مثال 1:
وصف: "قطة على سيارة في كراج"
→ يحتاج توضيح
{
  "questions": [
    {"question": "ما نوع أو سلالة أو لون القطة المطلوبة؟", "options": null},
    {"question": "ما ماركة أو موديل أو لون السيارة؟", "options": ["كلاسيكية", "حديثة", "فورد", "مرسيدس"]},
    {"question": "كيف تبدو البيئة داخل الكراج (قديم، حديث، متسخ، مضيء...)؟", "options": null}
  ]
}

مثال 2:
وصف: "قطة سيامية سوداء على فورد موستانج 1969 حمراء في كراج قديم مليء بالغبار وإضاءة فلورسنت خافتة"
→ كافي
{
  "questions": []
}

مثال 3:
وصف: "فتاة تجلس على كرسي في حديقة"
→ يحتاج توضيح
{
  "questions": [
    {"question": "كم عمر الفتاة تقريبًا وما أسلوب ملابسها أو تعبير وجهها؟", "options": null},
    {"question": "ما نوع الكرسي أو لونه أو خامته؟", "options": null},
    {"question": "كيف تبدو الحديقة (نهار، ليل، مزهرة، خريفية، مطر...)؟", "options": null}
  ]
}
"""

        user_prompt = f"الوصف الحالي: {description}"

        full_prompt = f"{system_prompt}\n\n{user_prompt}"

        # محاولة استدعاء LLM
        raw_response = self._call_small_llm(full_prompt)

        # ────────────────────────────────────────────────
        # محاولة parse الـ JSON
        # ────────────────────────────────────────────────
        try:
            parsed = json.loads(raw_response)
            questions = parsed.get("questions", [])
            if isinstance(questions, list):
                return {"questions": questions}
        except Exception as e:
            print(f"فشل parse JSON من LLM: {e} → fallback")

        # ────────────────────────────────────────────────
        # Fallback: الطريقة القديمة بالكلمات المفتاحية
        # ────────────────────────────────────────────────
        print("استخدام fallback (كلمات مفتاحية)")
        fallback_questions = []

        # مؤشرات بسيطة (يمكن توسيعها)
        if not any(word in description.lower() for word in ["سيامي", "فارسي", "بنگال", "شيرازي", "لون", "أسود", "أبيض", "رمادي", "برتقالي", "صغير", "كبير", "قطيط"]):
            fallback_questions.append({
                "question": "ما نوع/سلالة/لون/حجم/تعبير القطة أو الكائن الحي الرئيسي؟",
                "options": []

            })

        if not any(word in description.lower() for word in ["فورد", "موستنج", "مرسيدس", "تويوتا", "بي ام دبليو", "كلاسيك", "حديث", "1969", "2020", "أحمر", "أسود", "لامع", "مهترئ"]):
            fallback_questions.append({
                "question": "ما ماركة/موديل/سنة/لون/حالة السيارة أو الجسم الرئيسي؟",
                "options": ["كلاسيكية", "رياضية", "فاخرة", "عادية"]
            })

        if not any(word in description.lower() for word in ["قديم", "حديث", "متسخ", "نظيف", "مليء بالغبار", "مظلم", "مشرق", "فلورسنت", "طبيعي", "مطر", "ليل"]):
            fallback_questions.append({
                "question": "ما طابع الكراج أو البيئة (إضاءة، نظافة، جو عام)؟",
                "options": []

            })

        return {"questions": fallback_questions}
    
    def apply_answers(self, current_desc: str, questions: list, answers: list) -> str:
        additions = []
        for q, ans in zip(questions, answers):
            if not ans or not ans.strip():
                continue
            # يمكنك هنا إضافة معالجة خاصة حسب نوع السؤال إذا أردت
            additions.append(ans.strip())

        if not additions:
            return current_desc

        # محاولة جعل الفاصل يتناسب مع اللغة
        if any("،" in current_desc):
            return current_desc + "، " + "، ".join(additions)
        else:
            return current_desc + ", " + ", ".join(additions)
