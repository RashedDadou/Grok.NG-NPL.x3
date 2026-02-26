# test.py  (نسخة تفاعلية + توضيح أذكى)

from ai_prompts import AiPrompts
from ai_npl_g import AiNplG
from ai_npl_e import AiNplE
from ai_npl_t import AiNplT
from ai_rl_supervisor import AIRLSupervisor
from renderer import RenderingWindow

def interactive_enrich(supervisor: AiPrompts, initial_prompt: str) -> str:
    current_description = initial_prompt.strip()
    print("\nالوصف الأولي:", current_description)
    print("-" * 60)

    clarification_round = 0
    max_rounds = 4  # حماية من حلقة لا نهائية

    while clarification_round < max_rounds:
        clarification_round += 1
        
        result = supervisor.analyze_and_suggest_questions(current_description)
        
        if not result["questions"]:
            print("\n→ الوصف كافٍ الآن (لا أسئلة إضافية)")
            break
        
        print(f"\nجولة التوضيح {clarification_round}:")
        for i, q in enumerate(result["questions"], 1):
            print(f"  {i}. {q['question']}")
            if 'options' in q:
                options = q.get('options')
                if options and isinstance(options, (list, tuple)):
                    print("     خيارات ممكنة:", ", ".join(str(opt) for opt in options))
                else:
                    print("     خيارات ممكنة: (مفتوح – أجب بحرية)")
    
        # أخذ إجابة المستخدم
        user_answers = []
        for i in range(len(result["questions"])):
            ans = input(f"إجابتك على السؤال {i+1} (أو اضغط Enter لتخطي): ").strip()
            user_answers.append(ans if ans else None)
        
        # تحديث الوصف بناءً على الإجابات
        updated = supervisor.apply_answers(current_description, result["questions"], user_answers)
        if updated == current_description and all(a is None for a in user_answers):
            print("→ لم تضف تفاصيل جديدة، نكمل بالمتوفر...")
            break
        
        current_description = updated
        print("\nالوصف بعد تحديث:", current_description)
    
    return current_description


def main():
    supervisor = AiPrompts()
    
    user_input = input("اكتب وصف الصورة المطلوبة: ").strip()
    if not user_input:
        user_input = "قطة على سيارة مركونة داخل كراج منزل"  # fallback
    
    enriched_prompt = interactive_enrich(supervisor, user_input)
    
    rl_supervisor = AIRLSupervisor(prompts_supervisor=supervisor)
    rl_part = rl_supervisor.generate_behavior(enriched_prompt, output_type="image")

    
    print("\n" + "═" * 70)
    print("الوصف النهائي بعد التوضيح:")
    print(enriched_prompt)
    print("═" * 70 + "\n")
    
def main():
    supervisor = AiPrompts()
    
    # ────────────────────── اختيار نوع الإخراج من المستخدم ──────────────────────
    print("اختر نوع الإخراج:")
    print("1. صورة ثابتة (Image)")
    print("2. فيديو قصير (Video)")
    choice = input("أدخل 1 أو 2: ").strip()
    
    if choice == "2":
        output_type = "video"
        style_suffix = "photorealistic, cinematic lighting, ultra detailed, 8k, sharp focus, smooth motion --ar 16:9"
    else:
        output_type = "image"
        style_suffix = "photorealistic, cinematic lighting, ultra detailed, 8k, sharp focus --ar 4:3"

    user_input = input("\nاكتب وصف الصورة/الفيديو المطلوبة: ").strip()
    if not user_input:
        user_input = "قطة سيامية سوداء على سيارة موستانج حمراء في كراج قديم"

    enriched_prompt = interactive_enrich(supervisor, user_input)
    
    print("\n" + "═" * 80)
    print(f"الوصف النهائي بعد التوضيح ({output_type.upper()}):")
    print(enriched_prompt)
    print("═" * 80 + "\n")

    # توليد الأجزاء
    g_part = AiNplG().process(enriched_prompt)
    e_part = AiNplE().process(enriched_prompt)
    t_part = AiNplT().process(enriched_prompt)

    # AI.RL - السلوك والحركة
    rl_supervisor = AIRLSupervisor()
    rl_part = rl_supervisor.generate_behavior(enriched_prompt, output_type=output_type)

    # الدمج
    renderer = RenderingWindow()
    renderer.add_part("G", g_part, weight=1.0)
    renderer.add_part("E", e_part, weight=0.9)
    renderer.add_part("T", t_part, weight=1.3)
    
    if rl_part and rl_part.strip():
        renderer.add_part("RL", rl_part, weight=1.5)   # وزن عالي للحركة والسلوك

    final = renderer.render(
        base_prompt=enriched_prompt,
        style_suffix=style_suffix
    )

    print("الـ Final Prompt الجاهز:")
    print(final)
    print("-" * 90)
if __name__ == "__main__":
    main()
