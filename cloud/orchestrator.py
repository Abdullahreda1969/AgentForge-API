# cloud/orchestrator.py
import os
import logging
from core.templates import Templates

logger = logging.getLogger("CloudOrchestrator")

class CloudOrchestrator:
    def __init__(self):
        self.templates = Templates()
    
    def generate(self, project_name, description):
        logger.info(f"☁️ Cloud mode generating: {project_name}")
        
        project_type, item_name = self.templates.detect_type(description)
        
        project_path = os.path.join("projects", project_name)
        os.makedirs(project_path, exist_ok=True)
        
        files = {
            "config.py": self.templates.config(),
            "database.py": self.templates.database(),
            "helpers.py": self.templates.helpers(project_type, item_name),
            "main.py": self.templates.main(project_type, item_name),
            "start_app.bat": self.templates.start_bat()
        }
        
        for filename, content in files.items():
            with open(os.path.join(project_path, filename), "w", encoding="utf-8") as f:
                f.write(content)
        
        return {"status": "completed", "path": project_path, "files": list(files.keys())}