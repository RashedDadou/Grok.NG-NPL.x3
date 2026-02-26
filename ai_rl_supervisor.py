# ai_rl_supervisor.py

import os
import json
from typing import Dict, Optional

from supervisor_helper import SuperVisorHelper

class AIRLSupervisor:
    def __init__(self):
        self.helper = SuperVisorHelper()

        # مكتبة داخلية أساسية (يمكن أن تُحدث من المخزن أو البحث)
        self.behavior_patterns = {
            "cat": "slow blinking, tail curling or swishing, ear twitching, soft paw placement, subtle weight shift",
            "dog": "panting rhythm, tail wag intensity based on mood, alert ear rotation, sniffing head movement",
            "bird": "feather ruffling, head bobbing, quick eye darts, balanced perching, wing adjustment",
            "human": "subtle breathing, eye blinks, natural weight transfer, micro hand gestures, lifelike posture",
            "plant": "gentle phototropism, leaf flutter in breeze, stem flex under weight, dew droplet movement",
        }
            
    def _load_knowledge(self):
        """تحميل المخزن من ملف json إذا وُجد"""
        if os.path.exists(self.KNOWLEDGE_FILE):
            try:
                with open(self.KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    self.knowledge.update(loaded)
                print(f"[AI.RL] Loaded {len(loaded)} additional entries from {self.KNOWLEDGE_FILE}")
            except Exception as e:
                print(f"[AI.RL] Failed to load knowledge file: {e}")

    def _save_knowledge(self):
        """حفظ التغييرات في المخزن (اختياري حاليًا)"""
        try:
            with open(self.KNOWLEDGE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.knowledge, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[AI.RL] Failed to save knowledge: {e}")

    def external_search(self, entity: str, aspect: str) -> Optional[str]:
        """
        محاكاة بحث خارجي بسيط (في المستقبل يمكن استبداله بـ web_search أو x_keyword_search)
        """
        # مثال محاكاة فقط — في الواقع استبدل هنا باستدعاء أداة بحث حقيقية
        simulated_responses = {
            ("cat", "hunting"): "Cats stalk prey with low crouch, slow tail tip twitching, sudden pounce with claws extended",
            ("plant", "wind"): "Leaves and thin stems show oscillatory movement in wind; stronger stems resist but flex slightly",
        }

        key = (entity.lower(), aspect.lower())
        return simulated_responses.get(key)
            
    def enrich_with_knowledge(self, enriched_prompt: str) -> str:
        """يبحث في المكتبة الداخلية أو يحاكي بحث خارجي"""
        lower = enriched_prompt.lower()
        additions = []

        if "cat" in lower or "قطة" in lower:
            additions.append(self.knowledge_base["cat"]["movement"])
        
        if "human" in lower or "إنسان" in lower or "person" in lower:
            additions.append(self.knowledge_base["human"]["movement"])

        if not additions:
            return ""

        return "Realistic motion & behavior:\n• " + "\n• ".join(additions)

    def coordinate_npls(self, enriched_prompt: str):
        """محاكاة التواصل مع NPLs (في الإصدار الأول نرجع نص إضافي فقط)"""
        behavior = self.enrich_with_knowledge(enriched_prompt)
        if behavior:
            return behavior + "\n(Supervised by AI.RL for natural dynamics)"
        return ""

    def _ask_npl(self, npl_type: str, desc: str, motion_level: str) -> str:
        """محاكاة طلب من NPL مع إضافة سياق الحركة"""
        prefix = f"[Motion level: {motion_level}] "
        if npl_type == "T":
            return f"{prefix}Natural living subject pose & subtle movement: realistic micro-expressions, breathing, tail/ear/fur motion"
        elif npl_type == "G":
            return f"{prefix}Camera & composition motion: smooth pan or slight zoom, perspective consistent with subject movement"
        elif npl_type == "E":
            return f"{prefix}Environmental dynamics: gentle wind on leaves, dust particles drifting, light flicker"
        return ""

    def process(self, enriched_prompt: str) -> str:
        """
        Takes the enriched prompt and returns behavior description 
        ready to be added to the final master prompt.
        """
        behavior_parts = []

        # Detect which living entities exist in the prompt
        lower = enriched_prompt.lower()

        if any(word in lower for word in ["human", "man", "woman", "person", "girl", "boy", "child"]):
            behavior_parts.append(self.rooms["human"].get_behavior(enriched_prompt))
        
        if any(word in lower for word in ["cat", "dog", "bird", "animal", "horse", "lion"]):
            behavior_parts.append(self.rooms["animal"].get_behavior(enriched_prompt))
        
        if any(word in lower for word in ["plant", "tree", "flower", "grass", "bush"]):
            behavior_parts.append(self.rooms["plant"].get_behavior(enriched_prompt))

        # Social interactions between different types
        social = self._generate_social_interactions(enriched_prompt)
        if social:
            behavior_parts.append(social)

        return "\n".join(behavior_parts)

    def _generate_social_interactions(self, prompt: str) -> str:
        """Simulates social habits and interactions between different life forms"""
        lower = prompt.lower()
        if "cat" in lower and ("human" in lower or "person" in lower):
            return "natural human-animal bond: cat showing affection by rubbing against leg or watching curiously from distance, subtle mutual trust"
        if "bird" in lower and "tree" in lower:
            return "bird perched naturally on branch, gentle interaction with plant life, realistic weight distribution on leaves"
        return ""
    
    def generate_behavior(self, enriched_prompt: str, output_type: str = "image") -> str:
        """
        توليد وصف سلوك وحركة طبيعية مع كشف كيانات أذكى
        """
        lower = enriched_prompt.lower()
        behavior_sections = {}
        lines = []

        # كشف الكيانات (مثال بسيط)
        if "نسر" in lower or "eagle" in lower:
            eagle_params = {
                "mass": 4.5,
                "area": 1.1,
                "lift_coeff": 1.6,
                "drag_coeff": 0.35
            }

            if output_type == "image":
                # حساب خطوة واحدة فقط
                instance = EntityPhysicsInstance(PhysicsCore(), "eagle", eagle_params)
                result = instance.step(wind_speed_kmh=20)
                monitor = PhysicsMonitor().check(instance, result)
                lines.append(physics_to_prompt_text(result["forces"], monitor, "eagle", 20))
            else:
                # محاكاة فيديو قصير (1 ثانية)
                frames = simulate_over_time(eagle_params, wind_speed_kmh=20, duration_sec=1.0)
                lines.append("Dynamic animation sequence:")
                for f in frames[::5]:  # كل 5 فريمات عشان ما يطولش
                    lines.append(f"  Frame {f['frame']} ({f['time']}s): {f['prompt_snippet']}")

        # ... باقي الكود للكائنات الأخرى ...

        if not lines:
            return ""

        return "\n".join(lines)
    
        # قاموس كشف الكيانات (أكثر ذكاءً ومرونة)
        entity_keywords = {
            "cat":    ["cat", "قطة", "سيامي", "kitten", "قطيط"],
            "dog":    ["dog", "كلب", "puppy"],
            "bird":   ["bird", "طائر", "عصفور"],
            "human":  ["human", "person", "man", "woman", "girl", "boy", "إنسان", "رجل", "امرأة"],
            "plant":  ["plant", "tree", "flower", "grass", "شجرة", "وردة", "نبات"]
        }

        detected = []
        for entity, keywords in entity_keywords.items():
            if any(kw in lower for kw in keywords):
                detected.append(entity)

        # توليد السلوك لكل كيان مكتشف
        for entity in detected:
            lines = []

            # حركة أساسية
            pattern = self.behavior_patterns.get(entity)
            if pattern:
                lines.append(pattern)

            # سلوك اجتماعي إذا وُجد تفاعل
            if any(w in lower for w in ["with", "and", "near", "together", "مع", "بجانب", "يلعب"]):
                social = self.helper.search_or_query(entity, "social")
                if social and social != "Simulated external info":
                    lines.append(social)

            if lines:
                behavior_sections[entity] = lines

        # حركة الكاميرا للفيديو
        if output_type == "video":
            behavior_sections["camera"] = [
                "smooth cinematic camera movement: gentle push-in, slow tracking pan, natural motion blur"
            ]

        if not behavior_sections:
            return ""

        # تجميع النتيجة بشكل منظم وجميل
        result = ["Natural behavior & realistic motion layer (AI.RL supervised):"]
        
        for entity, lines in behavior_sections.items():
            title = "Camera & overall motion" if entity == "camera" else f"{entity.capitalize()} behavior & motion"
            result.append(title)
            result.extend([f"  • {line}" for line in lines])

        return "\n".join(result)
    
# ====================== الغرف الثلاث ======================

class HumanRoom:
    """Room for human natural behavior & social habits"""
    
    def get_behavior(self, prompt: str) -> str:
        return (
            "Natural human behavior and micro-movements: realistic weight shift, "
            "subtle breathing, natural eye direction, micro-expressions, "
            "lifelike posture and gesture according to context and emotion"
        )


class AnimalRoom:
    """Room for animals (especially cats, dogs, birds...)"""
    
    ANIMAL_BEHAVIORS = {
        "cat": "cat-specific natural behavior: slow blinking, tail movement, ear twitching, "
               "weight balanced on paws, curious head tilt, realistic fur flow when moving",
        "dog": "dog-specific: panting rhythm, tail wag speed according to mood, "
               "alert ear position, natural sniffing motion",
        "bird": "bird-specific: feather ruffling, head bob, realistic wing fold, "
                "perching balance, quick eye movements"
    }

    def get_behavior(self, prompt: str) -> str:
        lower = prompt.lower()
        for key, behavior in self.ANIMAL_BEHAVIORS.items():
            if key in lower:
                return behavior
        # Default for any animal
        return (
            "animal-specific natural behavior: realistic muscle movement, "
            "weight distribution on limbs, natural breathing rhythm, "
            "species-accurate micro-movements and instincts"
        )


class PlantRoom:
    """Room for plants - growth and natural response"""
    
    def get_behavior(self, prompt: str) -> str:
        return (
            "Natural plant behavior: phototropism (gentle lean toward light source), "
            "subtle leaf movement with air current, realistic growth direction, "
            "delicate stem bending under weight of flowers or dew, organic texture flow"
        )