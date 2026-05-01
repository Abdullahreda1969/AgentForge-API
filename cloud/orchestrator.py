# cloud/orchestrator.py
import os
import logging
from core.templates import Templates

logger = logging.getLogger("CloudOrchestrator")

class CloudOrchestrator:
    def __init__(self):
        self.templates = Templates()
    
    def generate(self, project_name, description, project_type="auto"):
        """توليد مشروع جديد مع إمكانية تحديد النوع (النسخة السحابية)"""
        logger.info(f"☁️ Cloud mode generating: {project_name} (type: {project_type})")
        
        # ✅ إذا كان المستخدم قد حدد نوع المشروع
        if project_type != "auto" and project_type != "general":
            # استخدام النوع المحدد مباشرة
            actual_type = project_type
            item_name = self._get_item_name_for_type(actual_type)
        else:
            # كشف تلقائي من الوصف
            actual_type, item_name = self.templates.detect_type(description)
        
        project_path = os.path.join("projects", project_name)
        os.makedirs(project_path, exist_ok=True)
        
        # اختيار القالب المناسب
        if actual_type == "library":
            helpers_content = self.templates.helpers_library()
            main_content = self.templates.main_library()
        else:
            # القوالب العامة (task, contact, product)
            helpers_content = self.templates.helpers(actual_type, item_name)
            main_content = self.templates.main(actual_type, item_name)
        
        files = {
            "config.py": self.templates.config(),
            "database.py": self.templates.database(),
            "helpers.py": helpers_content,
            "main.py": main_content,
            "start_app.bat": self.templates.start_bat()
        }
        
        for filename, content in files.items():
            with open(os.path.join(project_path, filename), "w", encoding="utf-8") as f:
                f.write(content)
        
        return {"status": "completed", "path": project_path, "files": list(files.keys()), "type_used": actual_type}
    
    def _get_item_name_for_type(self, project_type):
        """تحويل نوع المشروع إلى اسم العنصر"""
        mapping = {
            "task": "task",
            "contact": "contact", 
            "product": "product",
            "library": "book",
            "restaurant": "dish",
            "hotel": "room"
        }
        return mapping.get(project_type, "item")