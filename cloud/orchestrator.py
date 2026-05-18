# cloud/orchestrator.py
import os
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai

from agents.validator import ValidatorAgent
from agents.corrector import CorrectorAgent
from agents.planner import PlannerAgent
from agents.memory import MemoryAgent

load_dotenv()


def clean_json_response(text: str) -> str:
    """إزالة أحرف التحكم غير المسموح بها في JSON"""
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*$', '', text)
    text = re.sub(r'^```\s*', '', text)
    text = re.sub(r'[\x00-\x1f\x7f]', '', text)

    def replace_newlines(match):
        inside = match.group(0)
        return inside.replace('\n', '\\n').replace('\r', '\\r')

    text = re.sub(r'"(?:[^"\\]|\\.)*"', replace_newlines, text, flags=re.DOTALL)
    return text


class CloudOrchestrator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print("❌ GEMINI_API_KEY not found in .env file")
            self.model = None
            return

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        print("✅ Gemini client initialized successfully")
        
        self.planner = PlannerAgent()
        self.validator = ValidatorAgent()
        self.corrector = CorrectorAgent()
        self.memory = MemoryAgent()
        
        print("✅ All 5 agents initialized successfully")

    def generate_ai(self, project_name, description):
        if not self.model:
            return {"status": "failed", "reason": "Gemini model not initialized"}

        project_path = os.path.join("projects", project_name)
        os.makedirs(project_path, exist_ok=True)

        # ========== 1. Planner Agent ==========
        print("\n" + "="*50)
        print("🧠 STEP 1: Planning Agent")
        print("="*50)
        plan = self.planner.plan(description, project_name)
        print(f"📋 Project Type: {plan['type']}")
        print(f"📋 Features: {', '.join(plan['features'])}")
        print(f"📋 Tables: {', '.join(plan['database_tables']) if plan['database_tables'] else 'None'}")

        # ========== تعريف type_hints خارج f-string ==========
        type_hints = {
            "restaurant": "menu items (name, price, category) and orders (customer, items, total)",
            "gym": "exercises (name, sets, reps, weight) and workouts (date, duration)",
            "school": "students (name, grade, email) and teachers (name, subject, email)",
            "hospital": "doctors (name, specialty, phone) and patients (name, condition, doctor_id)",
            "event": "events (name, date, location) and attendees (name, email, event_id)",
            "hotel": "rooms (room_number, type, price) and reservations (guest_name, room_id, check_in, check_out)",
            "invoice": "invoices (customer_name, amount, due_date, status) and line_items (description, quantity, unit_price)",
            "appointment": "appointments (customer_name, service, date, time, status)"
        }

        # ========== 2. بناء الـ prompt ==========
        plan_text = self.planner.format_plan_for_prompt(plan)
        
        # إضافة تلميحات إضافية إذا كان النوع معروفاً
        if plan['type'] in type_hints:
            plan_text += f"\nSPECIFIC FIELDS: {type_hints[plan['type']]}"

        prompt = f"""You are an expert Python developer. Build a COMPLETE WORKING Streamlit application.

PROJECT NAME: {project_name}
USER REQUEST: {description}

PLANNED STRUCTURE:
{plan_text}

================================================================================
CRITICAL STREAMLIT RULES - FOLLOW EXACTLY:
================================================================================
1. NEVER use st.button() inside st.form(). Use st.form_submit_button() instead.
2. NEVER use st.dataframe(...)['selection']['rows'] - THIS DOES NOT WORK.
3. ALWAYS add a submit button to every form using st.form_submit_button().
4. Use st.rerun() after data modification operations.
5. For dataframe row selection, use event.selection.rows pattern.

================================================================================
REQUIREMENTS:
================================================================================
1. SQLite database with tables: {', '.join(plan['database_tables']) if plan['database_tables'] else 'items'}
2. Features: {', '.join(plan['features'])}

3. Generate these 5 files:
   - main.py (Streamlit UI)
   - helpers.py (database functions)
   - config.py (constants)
   - database.py (SQLite setup)
   - start_app.bat

================================================================================
RETURN ONLY VALID JSON. NO EXTRA TEXT.
================================================================================
"""

        print(f"\n📤 Sending prompt of length: {len(prompt)} characters")

        try:
            # ========== 3. Generator Agent ==========
            print("\n" + "="*50)
            print("💻 STEP 2: Generator Agent (Gemini)")
            print("="*50)
            response = self.model.generate_content(prompt)
            txt = response.text

            # استخراج JSON
            match = re.search(r'\{.*\}', txt, re.DOTALL)
            if not match:
                print("❌ No JSON found in response")
                return {"status": "failed", "reason": "No JSON found"}

            json_str = clean_json_response(match.group())

            try:
                files = json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error: {e}")
                return {"status": "failed", "reason": f"Invalid JSON: {e}"}

            # التأكد من وجود جميع الملفات
            required = ["main.py", "helpers.py", "config.py", "database.py", "start_app.bat"]
            for key in required:
                if key not in files:
                    files[key] = f"# {key}\nprint('{key} generated')"

            # ========== 4. Validator & Corrector ==========
            print("\n" + "="*50)
            print("🔍 STEP 3: Validator & Corrector Agents")
            print("="*50)
            all_errors = self.validator.validate_all_files(files)
            
            if all_errors:
                print(self.validator.format_report(all_errors))
                if self.validator.has_critical_errors(all_errors):
                    print("🔧 Attempting automatic correction...")
                    files = self.corrector.fix_project_files(files, all_errors)
                    
                    # التحقق مرة أخرى
                    all_errors = self.validator.validate_all_files(files)
                    if all_errors:
                        print("⚠️ Some errors remain:")
                        print(self.validator.format_report(all_errors))
                    else:
                        print("✅ All errors fixed!")
            else:
                print("✅ No errors found!")

            # ========== 5. حفظ الملفات ==========
            print("\n" + "="*50)
            print("💾 STEP 4: Saving Files")
            print("="*50)
            for name, code in files.items():
                filepath = os.path.join(project_path, name)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(code)
                print(f"✅ Created: {name}")

            # ========== 6. Memory Agent ==========
            self.memory.print_statistics()

            return {
                "status": "completed",
                "path": project_path,
                "files": list(files.keys()),
                "plan": plan
            }

        except Exception as e:
            print(f"❌ Error: {e}")
            return {"status": "failed", "reason": str(e)}