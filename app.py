# app.py
import streamlit as st
import os
import shutil

st.set_page_config(page_title="AgentForge", page_icon="🚀", layout="wide")

st.title("🚀 AgentForge AI Engine")
st.caption("Generate complete applications from text descriptions")

mode = st.radio(
    "Choose Mode:",
    ["🌍 Cloud (Gemini API)", "💻 Local (Ollama)"],
    horizontal=True
)

project_name = st.text_input("Project Name", placeholder="My_App")
description = st.text_area("Description", placeholder="Describe your app...", height=150)

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
            
            result = engine.generate(clean_name, description)
            
            if result["status"] == "completed":
                st.success(f"✅ {clean_name} generated successfully!")
                
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