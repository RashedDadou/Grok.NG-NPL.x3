# supervisor_helper.py

import json
import os
from typing import Dict, Any, Optional

class SuperVisorHelper:
    """
    SuperVisor.Helper - المخزن الاستراتيجي للمعلومات السلوكية والعلمية
    يخدم AI.RL بشكل رئيسي، ويمكن الوصول إليه من أجزاء أخرى إذا لزم
    """

    STORAGE_FILE = "supervisor_helper_knowledge.json"

    def __init__(self):
        self.knowledge: Dict[str, Dict[str, Any]] = {}
        self._load()

    def _load(self):
        """تحميل البيانات من الملف إذا وُجد"""
        if os.path.exists(self.STORAGE_FILE):
            try:
                with open(self.STORAGE_FILE, "r", encoding="utf-8") as f:
                    self.knowledge = json.load(f)
                print(f"[SuperVisor.Helper] Loaded {len(self.knowledge)} entries from storage")
            except Exception as e:
                print(f"[SuperVisor.Helper] Failed to load storage: {e}")

    def _save(self):
        """حفظ التغييرات إلى الملف"""
        try:
            with open(self.STORAGE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.knowledge, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[SuperVisor.Helper] Failed to save: {e}")

    def get(self, entity: str, aspect: str, default: Any = None) -> Any:
        """
        جلب معلومة محددة
        مثال: helper.get("cat", "hunting_style")
        """
        entity = entity.lower()
        aspect = aspect.lower()
        
        if entity in self.knowledge and aspect in self.knowledge[entity]:
            return self.knowledge[entity][aspect]
        
        return default

    def store(self, entity: str, aspect: str, value: Any):
        """
        حفظ معلومة جديدة أو تحديث موجودة
        """
        entity = entity.lower()
        aspect = aspect.lower()
        
        if entity not in self.knowledge:
            self.knowledge[entity] = {}
        
        self.knowledge[entity][aspect] = value
        self._save()

    def search_or_query(self, entity: str, aspect: str) -> str:
        """
        - يبحث أولاً في المخزن الداخلي
        - إذا ما لقاش → يحاكي بحث خارجي (يمكن استبداله بـ web_search حقيقي)
        - يخزن النتيجة ويرجعها
        """
        cached = self.get(entity, aspect)
        if cached is not None:
            return cached

        # محاكاة بحث خارجي (في الواقع استبدل بـ web_search أو x_keyword_search)
        external_info = self._simulate_external_query(entity, aspect)
        
        # حفظ النتيجة للمرات القادمة
        self.store(entity, aspect, external_info)
        
        return external_info

    def _simulate_external_query(self, entity: str, aspect: str) -> str:
        """محاكاة فقط — هنا يجي مكان استدعاء أدوات البحث الحقيقية"""
        sim_data = {
            ("cat", "hunting_style"): "stalking with low body, slow tail tip twitching, sudden pounce",
            ("plant", "wind_response"): "leaves flutter and oscillate, thin stems bend elastically, thicker stems resist",
            ("human", "nervous_gestures"): "fidgeting hands, foot tapping, avoiding eye contact, increased blink rate",
        }
        return sim_data.get((entity.lower(), aspect.lower()), "No specific information found")
    
    