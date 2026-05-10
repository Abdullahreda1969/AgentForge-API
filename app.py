# app.py
import streamlit as st
import os
import shutil

st.set_page_config(page_title="AgentForge", page_icon="🚀", layout="wide")

st.title("🚀 AgentForge AI Engine")
st.caption("Generate complete applications from text descriptions")

# ========== اختيار المحرك ==========
mode = st.radio(
    "Choose Engine",
    ["💻 Smart Templates", "🦙 Ollama AI", "☁️ Gemini AI"],
    horizontal=True,
    help="Smart Templates: fastest, most stable | Ollama: local AI (requires Ollama) | Gemini: cloud AI (requires API key)"
)

# ========== إدخال بيانات المشروع ==========
col1, col2 = st.columns(2)

with col1:
    project_name = st.text_input("Project Name", placeholder="My_App")

with col2:
    project_type = st.selectbox(
        "Project Type (for Smart Templates only)",
        options=["auto", "task", "contact", "product", "library", "invoice", "appointment", "workout", "meal", "blog"],
        format_func=lambda x: {
            "auto": "🤖 Auto Detect",
            "task": "📝 Task Manager",
            "contact": "📞 Contact Book",
            "product": "📦 Inventory",
            "library": "📚 Library Manager",
            "invoice": "💰 Invoice System",
            "appointment": "📅 Appointment Booking",
            "workout": "🏋️ Workout Tracker",
            "meal": "🍽️ Meal Tracker",
            "blog": "📝 Blog Platform"
        }.get(x, x),
        help="Only used when Smart Templates is selected"
    )

description = st.text_area("Description", placeholder="Describe your app...", height=150)

# ========== معلومات إضافية حسب المحرك ==========
if "Gemini" in mode:
    st.info("☁️ Gemini AI requires an API key. Make sure GEMINI_API_KEY is set in .env file")

if "Ollama" in mode:
    st.info("🦙 Ollama AI requires Ollama to be running locally. Run 'ollama serve' first.")

# ========== زر التوليد ==========
if st.button("🚀 Generate", type="primary"):
    if not project_name or not description:
        st.error("Please enter both name and description")
    else:
        clean_name = project_name.replace(" ", "_")
        
        with st.spinner(f"Generating with {mode}..."):
            
            # ========== Smart Templates ==========
            if "Smart Templates" in mode:
                from local.orchestrator import LocalOrchestrator
                engine = LocalOrchestrator()
                result = engine.generate(clean_name, description, project_type)
            
            # ========== Ollama AI ==========
            elif "Ollama" in mode:
                from ollama.orchestrator import OllamaOrchestrator
                engine = OllamaOrchestrator()
                result = engine.generate_ai(clean_name, description)
            
            # ========== Gemini AI ==========
            elif "Gemini" in mode:
                from cloud.orchestrator import CloudOrchestrator
                engine = CloudOrchestrator()
                result = engine.generate_ai(clean_name, description)
            
            # ========== عرض النتيجة ==========
            if result.get("status") == "completed":
                st.success(f"✅ {clean_name} generated successfully!")
                
                # إنشاء ملف ZIP
                shutil.make_archive(f"projects/{clean_name}", 'zip', result["path"])
                
                with open(f"projects/{clean_name}.zip", "rb") as fp:
                    st.download_button(
                        label="📥 Download Project",
                        data=fp,
                        file_name=f"{clean_name}.zip",
                        mime="application/zip"
                    )
                
                with st.expander("📁 Generated Files"):
                    for file in result.get("files", []):
                        st.code(f"✅ {file}")
                
                if "type_used" in result:
                    st.caption(f"📌 Template used: **{result['type_used']}**")
            else:
                error_msg = result.get("reason", "Unknown error")
                st.error(f"❌ Generation failed: {error_msg}")
                
                # نصائح إضافية حسب الخطأ
                if "Ollama is not running" in error_msg:
                    st.info("💡 Tip: Run 'ollama serve' in a separate terminal window")
                elif "GEMINI_API_KEY" in error_msg:
                    st.info("💡 Tip: Add GEMINI_API_KEY to your .env file")
                elif "No JSON found" in error_msg:
                    st.info("💡 Tip: The AI response was not in the expected format. Try again or use Smart Templates.")

st.markdown("---")
st.caption("Powered by AgentForge - Smart Templates | Ollama AI | Gemini AI")