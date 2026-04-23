# local/orchestrator.py
import os
import logging
import shutil
from core.templates import Templates

logger = logging.getLogger("LocalOrchestrator")

class LocalOrchestrator:
    def __init__(self):
        self.templates = Templates()
    
    def generate(self, project_name, description):
        logger.info(f"🚀 Local mode generating: {project_name}")
        
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
        # بعد حفظ الملفات، أنشئ ZIP
        zip_path = os.path.join("projects", f"{project_name}.zip")
        if not os.path.exists(zip_path):
            shutil.make_archive(
                os.path.join("projects", project_name), 
                'zip', 
                project_path
            )
        return {"status": "completed", "path": project_path, "files": list(files.keys())}