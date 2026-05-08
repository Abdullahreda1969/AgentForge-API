# cloud/orchestrator.py - نسخة بسيطة مع API Key
import os
import logging
import requests
import json
import re
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("CloudOrchestrator")

class CloudOrchestrator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = "gemini-2.5-flash"
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        
        if self.api_key:
            print(f"✅ API Key loaded: {self.api_key[:20]}...")
        else:
            print("❌ GEMINI_API_KEY not found in .env")
    
    def generate_ai(self, project_name, description):
        if not self.api_key:
            return {"status": "failed", "reason": "GEMINI_API_KEY not found"}
        
        project_path = os.path.join("projects", project_name)
        os.makedirs(project_path, exist_ok=True)
        
        prompt = f"""Create a Streamlit app for: {description}
Project name: {project_name}

Return ONLY valid JSON:
{{"main.py": "import streamlit as st\\nst.title('{project_name}')", "helpers.py": "# helpers", "config.py": "# config", "database.py": "# database", "start_app.bat": "@echo off\\nstreamlit run main.py\\npause"}}
"""
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2, "maxOutputTokens": 2048}
        }
        
        try:
            response = requests.post(self.api_url, json=payload, timeout=60)
            result = response.json()
            
            if "error" in result:
                return {"status": "failed", "reason": result['error'].get('message')}
            
            if "candidates" in result:
                text = result["candidates"][0]["content"]["parts"][0]["text"]
                match = re.search(r'\{.*\}', text, re.DOTALL)
                if match:
                    files = json.loads(match.group())
                    for filename, content in files.items():
                        with open(os.path.join(project_path, filename), "w") as f:
                            f.write(content)
                    return {"status": "completed", "path": project_path, "files": list(files.keys())}
            
            return {"status": "failed", "reason": "No valid JSON"}
            
        except Exception as e:
            return {"status": "failed", "reason": str(e)}