# agents/memory.py
"""
وكيل الذاكرة (Memory Agent)
مسؤوليته: تخزين الأخطاء والحلول السابقة لتسريع التصحيح مستقبلاً
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime


class MemoryAgent:
    def __init__(self, knowledge_file: str = "knowledge/errors.json"):
        self.knowledge_file = knowledge_file
        self.knowledge = self._load_knowledge()
    
    def _load_knowledge(self) -> Dict:
        """تحميل قاعدة المعرفة من ملف JSON"""
        if os.path.exists(self.knowledge_file):
            try:
                with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {"errors": [], "fixes": [], "stats": {"total_errors": 0, "total_fixes": 0}}
        return {"errors": [], "fixes": [], "stats": {"total_errors": 0, "total_fixes": 0}}
    
    def _save_knowledge(self):
        """حفظ قاعدة المعرفة"""
        os.makedirs(os.path.dirname(self.knowledge_file), exist_ok=True)
        with open(self.knowledge_file, 'w', encoding='utf-8') as f:
            json.dump(self.knowledge, f, ensure_ascii=False, indent=2)
    
    def learn_from_error(self, error: Dict, fix_applied: str):
        """تسجيل خطأ وحله في قاعدة المعرفة"""
        error_info = {
            "name": error.get("name"),
            "message": error.get("message"),
            "file": error.get("file"),
            "severity": error.get("severity"),
            "fix_applied": fix_applied,
            "timestamp": datetime.now().isoformat()
        }
        
        self.knowledge["errors"].append(error_info)
        self.knowledge["stats"]["total_errors"] += 1
        self._save_knowledge()
    
    def learn_from_fix(self, error_name: str, fix_code: str):
        """تسجيل حل لخطأ معين"""
        fix_info = {
            "error_name": error_name,
            "fix_code": fix_code,
            "success_count": 1,
            "timestamp": datetime.now().isoformat()
        }
        
        # البحث عن حل موجود مسبقاً
        for existing in self.knowledge["fixes"]:
            if existing["error_name"] == error_name:
                existing["success_count"] += 1
                existing["timestamp"] = datetime.now().isoformat()
                self._save_knowledge()
                return
        
        self.knowledge["fixes"].append(fix_info)
        self.knowledge["stats"]["total_fixes"] += 1
        self._save_knowledge()
    
    def suggest_fix(self, error_name: str) -> Optional[str]:
        """اقتراح حل لخطأ معين بناءً على التجارب السابقة"""
        for fix in self.knowledge["fixes"]:
            if fix["error_name"] == error_name:
                return fix["fix_code"]
        return None
    
    def get_statistics(self) -> Dict:
        """إحصائيات قاعدة المعرفة"""
        return {
            "total_errors_learned": self.knowledge["stats"]["total_errors"],
            "total_fixes_learned": self.knowledge["stats"]["total_fixes"],
            "recent_errors": self.knowledge["errors"][-5:] if self.knowledge["errors"] else []
        }
    
    def print_statistics(self):
        """طباعة الإحصائيات بشكل مقروء"""
        stats = self.get_statistics()
        print("\n📚 Memory Agent Statistics:")
        print(f"   Total errors learned: {stats['total_errors_learned']}")
        print(f"   Total fixes learned: {stats['total_fixes_learned']}")
        if stats['recent_errors']:
            print(f"   Recent errors: {len(stats['recent_errors'])} in last session")