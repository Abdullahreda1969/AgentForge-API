# agents/planner.py
"""
وكيل التخطيط (Planner Agent)
مسؤوليته: تحليل الطلب وتحديد نوع المشروع والهيكل المناسب
"""

import json
import re
from typing import Dict, List, Optional


class PlannerAgent:
    def __init__(self):
        self.project_types = {
            "invoice": ["فاتورة", "فواتير", "invoice", "billing", "فواتير"],
            "task": ["مهمة", "مهام", "task", "todo", "to-do"],
            "contact": ["جهة اتصال", "contact", "address", "عنوان", "دفتر عناوين"],
            "product": ["منتج", "products", "inventory", "مخزون"],
            "library": ["مكتبة", "library", "book", "كتاب"],
            "blog": ["blog", "مدونة", "post", "مقال"],
            "calculator": ["آلة حاسبة", "calculator", "حاسبة"],
            "appointment": ["appointment", "booking", "موعد", "حجز", "مواعيد"] ,
            "hotel": ["hotel", "booking", "room", "reservation", "check-in", "check-out", "فندق", "حجز", "غرفة"]# ✅ أضف هذا
        }
    
    def detect_project_type(self, description: str) -> str:
        """تحديد نوع المشروع من الوصف"""
        desc_lower = description.lower()
        for ptype, keywords in self.project_types.items():
            for kw in keywords:
                if kw in desc_lower:
                    return ptype
        return "general"
    
    def plan(self, description: str, project_name: str) -> Dict:
        """
        تحليل الطلب وإنشاء خطة المشروع
        
        Returns:
            Dict: خطة تحتوي على type, features, files_needed
        """
        project_type = self.detect_project_type(description)
        
        # القالب الأساسي للمشروع
        plan = {
            "project_name": project_name,
            "type": project_type,
            "description": description,
            "features": self._extract_features(description, project_type),
            "files": ["main.py", "helpers.py", "config.py", "database.py", "start_app.bat"],
            "database_tables": self._get_tables_for_type(project_type)
        }
        
        return plan
    
    def _extract_features(self, description: str, project_type: str) -> List[str]:
        """استخراج الميزات من الوصف"""
        features = ["create", "read", "delete"]
        
        if "update" in description.lower() or "edit" in description.lower():
            features.append("update")
        if "search" in description.lower():
            features.append("search")
        if "dashboard" in description.lower():
            features.append("dashboard")
        if "chart" in description.lower() or "graph" in description.lower():
            features.append("charts")
            
        return features
    
    def _get_tables_for_type(self, project_type: str) -> List[str]:
        """تحديد الجداول المطلوبة حسب نوع المشروع"""
        tables = {
            "invoice": ["invoices", "line_items"],
            "task": ["tasks"],
            "contact": ["contacts"],
            "product": ["products"],
            "library": ["books"],
            "blog": ["posts"],
            "calculator": [],
            "appointment": ["appointments"],
            "hotel": ["rooms", "reservations", "guests"]
        }
        return tables.get(project_type, ["items"])
    
    def format_plan_for_prompt(self, plan: Dict) -> str:
        """تنسيق الخطة لاستخدامها في prompt Gemini"""
        return f"""
Project Type: {plan['type']}
Features required: {', '.join(plan['features'])}
Database tables: {', '.join(plan['database_tables']) if plan['database_tables'] else 'None needed'}
"""