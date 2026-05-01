# app.py
import streamlit as st
import os
import shutil

st.set_page_config(page_title="AgentForge", page_icon="🚀", layout="wide")

st.title("🚀 AgentForge AI Engine")
st.caption("Generate complete applications from text descriptions")

# ========== اختيار وضع التشغيل ==========
mode = st.radio(
    "Choose Mode:",
    ["🌍 Cloud (Gemini API)", "💻 Local (Ollama)"],
    horizontal=True
)

# ========== إدخال بيانات المشروع ==========
col1, col2 = st.columns(2)

with col1:
    project_name = st.text_input("Project Name", placeholder="My_App")

with col2:
    # ✅ القائمة المنسدلة لاختيار نوع المشروع
    project_type = st.selectbox(
        "Project Type",
        options=["auto", "task", "contact", "product", "library"],
        format_func=lambda x: {
            "auto": "🤖 Auto Detect (Recommended)",
            "task": "📝 Task Manager",
            "contact": "📞 Contact Book",
            "product": "📦 Inventory Management",
            "library": "📚 Library Manager"
        }.get(x, x),
        help="Auto Detect will analyze your description to choose the best template"
    )

# عرض معلومات إضافية حسب الاختيار
if project_type != "auto":
    st.info(f"ℹ️ Using template: **{project_type}**. The AI will generate this specific application type.")

description = st.text_area("Description", placeholder="Describe your app...", height=150)

# ========== زر التوليد ==========
if st.button("🚀 Generate", type="primary"):
    if not project_name or not description:
        st.error("Please enter both name and description")
    else:
        clean_name = project_name.replace(" ", "_")
        
        with st.spinner(f"Generating in {mode} mode..."):
            if "Cloud" in mode:
                from cloud.orchestrator import CloudOrchestrator
                engine = CloudOrchestrator()
            else:
                from local.orchestrator import LocalOrchestrator
                engine = LocalOrchestrator()
            
            # ✅ تمرير project_type إلى المحرك
            result = engine.generate(clean_name, description, project_type=project_type)
            
            if result["status"] == "completed":
                st.success(f"✅ {clean_name} generated successfully!")
                
                # إنشاء ملف ZIP للتحميل
                shutil.make_archive(f"projects/{clean_name}", 'zip', result["path"])
                
                with open(f"projects/{clean_name}.zip", "rb") as fp:
                    st.download_button(
                        label="📥 Download Project",
                        data=fp,
                        file_name=f"{clean_name}.zip",
                        mime="application/zip"
                    )
                
                with st.expander("📁 Generated Files"):
                    for file in result["files"]:
                        st.code(f"✅ {file}")
                
                # عرض النوع الذي تم استخدامه فعلياً
                if "type_used" in result:
                    st.caption(f"📌 Template used: **{result['type_used']}**")
            else:
                st.error(f"❌ Generation failed: {result.get('message', 'Unknown error')}")