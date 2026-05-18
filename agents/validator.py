# agents/validator.py
"""
وكيل التحقق (Validator Agent)
مسؤوليته: فحص الكود المُنتَج واكتشاف الأخطاء الشائعة في Streamlit
"""

import re
from typing import List, Dict, Tuple


class ValidatorAgent:
    """يكتشف الأخطاء في كود Streamlit ويبلغ عنها"""

    def __init__(self):
        # قاعدة الأخطاء المعروفة
        self.error_patterns = [
            {
                "name": "st_button_inside_st_form",
                "pattern": r"st\.button\([^)]*\)",
                "context": r"with st\.form",
                "message": "❌ st.button() لا يمكن استخدامها داخل st.form(). استخدم st.form_submit_button() بدلاً من ذلك.",
                "severity": "critical",
                "fix": "replace_button_with_submit"
            },
            {
                "name": "dataframe_selection_subscript",
                "pattern": r"st\.dataframe\([^)]*\)\['selection'\]\['rows'\]",
                "message": "❌ الوصول المباشر st.dataframe(...)['selection']['rows'] غير صحيح. استخدم on_select='rerun' مع session_state.",
                "severity": "critical",
                "fix": "fix_dataframe_selection"
            },
            {
                "name": "missing_submit_button",
                "pattern": r"with st\.form",
                "context": r"st\.form_submit_button",
                "message": "⚠️ النموذج (form) لا يحتوي على زر إرسال. أضف st.form_submit_button().",
                "severity": "warning",
                "fix": "add_submit_button"
            },
            {
                "name": "direct_value_access",
                "pattern": r"st\.(text_input|number_input|selectbox)\([^)]*\)\s*\[",
                "message": "⚠️ الوصول المباشر إلى قيمة widget داخل السطر نفسه قد يسبب أخطاء. استخدم متغير منفصل.",
                "severity": "warning",
                "fix": None
            }
        ]

    def validate(self, code: str, file_name: str = "main.py") -> List[Dict]:
        """
        فحص الكود وإرجاع قائمة بالأخطاء

        Returns:
            List[Dict]: قائمة بالأخطاء، كل خطأ يحتوي على:
                - file: اسم الملف
                - line: رقم السطر (إن أمكن)
                - name: اسم الخطأ
                - message: وصف الخطأ
                - severity: critical / warning / info
                - fix: اسم الإجراء المقترح (إن وجد)
        """
        errors = []
        lines = code.split('\n')

        for i, line in enumerate(lines, 1):
            for pattern in self.error_patterns:
                # فحص النمط في السطر الحالي
                if re.search(pattern["pattern"], line):
                    # إذا كان هناك سياق مطلوب (مثل داخل st.form)
                    if "context" in pattern:
                        # البحث عن السياق في السطور السابقة (حتى 10 أسطر)
                        context_lines = lines[max(0, i-10):i]
                        context_text = '\n'.join(context_lines)
                        if not re.search(pattern["context"], context_text):
                            continue

                    error = {
                        "file": file_name,
                        "line": i,
                        "name": pattern["name"],
                        "message": pattern["message"],
                        "severity": pattern["severity"],
                        "fix": pattern.get("fix"),
                        "code_snippet": line.strip()
                    }
                    errors.append(error)

        return errors

    def validate_all_files(self, files: Dict[str, str]) -> Dict[str, List[Dict]]:
        """
        فحص جميع ملفات المشروع

        Args:
            files: قاموس بأسماء الملفات ومحتوياتها

        Returns:
            Dict[str, List[Dict]]: أخطاء لكل ملف
        """
        all_errors = {}
        for file_name, code in files.items():
            if file_name.endswith('.py'):  # فقط ملفات Python
                errors = self.validate(code, file_name)
                if errors:
                    all_errors[file_name] = errors
        return all_errors

    def has_critical_errors(self, errors: List[Dict]) -> bool:
        """التحقق من وجود أخطاء حرجة (critical)"""
        for error in errors:
            if error.get("severity") == "critical":
                return True
        return False

    def format_report(self, all_errors: Dict[str, List[Dict]]) -> str:
        """تنسيق تقرير الأخطاء بطريقة مقروءة"""

        if not all_errors:
            return "✅ لا توجد أخطاء في الكود!"

        report = "📋 تقرير مراجعة الكود:\n\n"
        for file_name, errors in all_errors.items():
            report += f"📄 {file_name}\n"
            for error in errors:
                emoji = "🔴" if error["severity"] == "critical" else "🟡"
                report += f"  {emoji} سطر {error['line']}: {error['message']}\n"
            report += "\n"
        return report