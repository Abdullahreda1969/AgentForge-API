# agents/corrector.py
"""
وكيل التصحيح (Corrector Agent)
مسؤوليته: تصحيح الأخطاء المكتشفة في كود Streamlit
"""

import re
from typing import Dict, List, Tuple


class CorrectorAgent:
    """يصحح أخطاء Streamlit الشائعة"""

    def __init__(self):
        self.fix_stats = {"fixed": 0, "failed": 0}
    def fix_data_editor_selection(self, code: str) -> Tuple[str, bool]:
        """إزالة selection_mode من st.data_editor (غير مدعوم)"""
        lines = code.split('\n')
        fixed = False
        new_lines = []
        
        for line in lines:
            if 'st.data_editor' in line and 'selection_mode' in line:
                line = re.sub(r',\s*selection_mode\s*=\s*["\'][^"\']*["\']', '', line)
                line = re.sub(r'selection_mode\s*=\s*["\'][^"\']*["\'],?\s*', '', line)
                fixed = True
            new_lines.append(line)
        
        return '\n'.join(new_lines), fixed
    def fix_button_inside_form(self, code: str) -> Tuple[str, bool]:
        """تصحيح: استبدال st.button داخل st.form بـ st.form_submit_button"""
        fixed = False
        lines = code.split('\n')
        inside_form = False
        new_lines = []

        for line in lines:
            if 'with st.form' in line:
                inside_form = True
            if inside_form and 'st.button(' in line and 'st.form_submit_button' not in line:
                line = line.replace('st.button(', 'st.form_submit_button(')
                fixed = True
            if inside_form and line.strip() == '':
                inside_form = False
            new_lines.append(line)

        return '\n'.join(new_lines), fixed

    def fix_dataframe_selection(self, code: str) -> Tuple[str, bool]:
        """تصحيح: استبدال st.dataframe(...)['selection']['rows'] بالطريقة الصحيحة"""
        pattern = r'(\w+)\s*=\s*st\.dataframe\(([^)]*)\)\s*\[\'selection\'\]\[\'rows\'\]'
        replacement = r'event = st.dataframe(\2, selection_mode="single-row", on_select="rerun")\nif event and hasattr(event, "selection") and event.selection:\n    \1 = event.selection.rows\nelse:\n    \1 = []'
        new_code, count = re.subn(pattern, replacement, code, flags=re.DOTALL)
        fixed = count > 0
        return new_code, fixed

    def fix_data_editor_selection(self, code: str) -> Tuple[str, bool]:
        """
        تصحيح: إزالة selection_mode من st.data_editor (غير مدعوم في Streamlit)
        """
        lines = code.split('\n')
        fixed = False
        new_lines = []
        
        for line in lines:
            if 'st.data_editor' in line and 'selection_mode' in line:
                # إزالة selection_mode بكافة أشكالها
                line = re.sub(r',\s*selection_mode\s*=\s*["\'][^"\']*["\']', '', line)
                line = re.sub(r'selection_mode\s*=\s*["\'][^"\']*["\'],?\s*', '', line)
                fixed = True
            new_lines.append(line)
        
        return '\n'.join(new_lines), fixed

    def fix_line_continuation_errors(self, code: str) -> Tuple[str, bool]:
        """
        تصحيح أخطاء أحرف الهروب (\) في منتصف السطر
        """
        lines = code.split('\n')
        new_lines = []
        fixed = False
        
        for line in lines:
            original_line = line
            if '\\' in line and len(line.strip()) > 0:
                line = re.sub(r'\\\s+', ' ', line)
                if original_line.rstrip().endswith('\\'):
                    pass
                else:
                    if line != original_line:
                        fixed = True
            new_lines.append(line)
        
        return '\n'.join(new_lines), fixed

    def ensure_db_initialization(self, code: str) -> Tuple[str, bool]:
        """تأكد من وجود واستدعاء init_db() في database.py"""
        lines = code.split('\n')
        has_init_db = False
        has_call_init_db = False
        fixed = False
        
        for line in lines:
            if 'def init_db()' in line:
                has_init_db = True
            if 'init_db()' in line and 'def' not in line:
                has_call_init_db = True
        
        if has_init_db and not has_call_init_db:
            code += '\n\n# Initialize database\ninit_db()'
            fixed = True
        
        return code, fixed

    def add_missing_submit_button(self, code: str) -> Tuple[str, bool]:
        """إضافة زر إرسال مفقود داخل st.form"""
        lines = code.split('\n')
        new_lines = []
        inside_form = False
        form_indent = 0
        submit_added = False

        for i, line in enumerate(lines):
            if 'with st.form' in line:
                inside_form = True
                form_indent = len(line) - len(line.lstrip())
                new_lines.append(line)
                continue

            if inside_form and not submit_added:
                current_indent = len(line) - len(line.lstrip())
                if current_indent <= form_indent and line.strip():
                    indent = ' ' * (form_indent + 4)
                    new_lines.append(f'{indent}submitted = st.form_submit_button("إرسال")')
                    new_lines.append(f'{indent}if submitted:')
                    new_lines.append(f'{indent}    st.success("تم الإرسال!")')
                    submit_added = True
                    inside_form = False

            new_lines.append(line)

        return '\n'.join(new_lines), submit_added
    def fix_missing_columns(self, code: str, table_name: str = "exercises") -> Tuple[str, bool]:
        """
        تصحيح: إزالة أعمدة غير موجودة من DataFrame
        """
        # الأعمدة القياسية لجدول exercises
        valid_columns = ['id', 'name', 'sets', 'reps', 'weight']
        
        pattern = r'df\s*=\s*df\[\[(.*?)\]\]'
    def ensure_string(self, code) -> Tuple[str, bool]:
            """تأكد من أن الكود من النوع str وليس list أو dict"""
            if isinstance(code, list):
                return '\n'.join(code), True
            elif isinstance(code, dict):
                return str(code), True
            elif code is None:
                return "", True
            return str(code), False
    def replace_columns(match):
        cols = match.group(1)
        # استخراج أسماء الأعمدة
        col_list = [c.strip().strip("'\"") for c in cols.split(',')]
        # تصفية الأعمدة الصحيحة فقط
        valid = [c for c in col_list if c in valid_columns]
        if valid:
            return f"df = df[{valid}]"
        else:
            return "# df column filtering removed - invalid columns"
    
        new_code, count = re.subn(pattern, replace_columns, code)
        fixed = count > 0
        return new_code, fixed
        def fix_selection_access(self, code: str) -> Tuple[str, bool]:
            """
            تصحيح: استبدال st.session_state[...]['selection']['rows'] بالطريقة الآمنة
            """
            pattern = r'st\.session_state\["([^"]+)"\]\["selection"\]\["rows"\]'
            replacement = r'st.session_state.get("\1", {}).get("selection", {}).get("rows", [])'
            new_code, count = re.subn(pattern, replacement, code)
            
            # أيضاً للوصول باستخدام النقاط بدلاً من الأقواس
            pattern2 = r'st\.session_state\["([^"]+)"\]\.selection\.rows'
            replacement2 = r'st.session_state.get("\1", {}).get("selection", {}).get("rows", [])'
            new_code, count2 = re.subn(pattern2, replacement2, new_code)
            
            fixed = count > 0 or count2 > 0
            return new_code, fixed
    def fix_all_errors(self, code: str, errors: List[Dict]) -> Tuple[str, int]:
        """
        تطبيق جميع الإصلاحات المناسبة بناءً على الأخطاء المكتشفة
        """
        fixed_count = 0
        current_code = code

        # إصلاح st.data_editor
        current_code, fixed = self.fix_data_editor_selection(current_code)
        if fixed:
            fixed_count += 1
        
        # إصلاح أخطاء أحرف الهروب
        current_code, fixed = self.fix_line_continuation_errors(current_code)
        if fixed:
            fixed_count += 1

        # إصلاح st.data_editor (قبل معالجة الأخطاء العادية)
        current_code, fixed = self.fix_data_editor_selection(current_code)
        if fixed:
            fixed_count += 1

        for error in errors:
            fix_method = error.get("fix")
            if fix_method == "replace_button_with_submit":
                current_code, fixed = self.fix_button_inside_form(current_code)
                if fixed:
                    fixed_count += 1
            elif fix_method == "fix_dataframe_selection":
                current_code, fixed = self.fix_dataframe_selection(current_code)
                if fixed:
                    fixed_count += 1
            elif fix_method == "add_submit_button":
                current_code, fixed = self.add_missing_submit_button(current_code)
                if fixed:
                    fixed_count += 1

        # إصلاح إضافي لأي أحرف هروب متبقية
        current_code, fixed = self.fix_line_continuation_errors(current_code)
        if fixed:
            fixed_count += 1
            # أولاً: تأكد من أن الكود نصي
        current_code, fixed = self.ensure_string(current_code)
        if fixed:
            fixed_count += 1
        # إصلاح أخطاء الأعمدة غير الموجودة
        current_code, fixed = self.fix_missing_columns(current_code)
        if fixed:
            fixed_count += 1
        # إصلاح أخطاء الوصول إلى selection
        current_code, fixed = self.fix_selection_access(current_code)
        if fixed:
            fixed_count += 1
        # إصلاح أخطاء الوصول إلى selection
        
        def fix_selection_access(self, code: str) -> Tuple[str, bool]:
            """
            تصحيح: استبدال st.session_state[...]['selection']['rows'] بالطريقة الآمنة
            """
            pattern = r'st\.session_state\["([^"]+)"\]\["selection"\]\["rows"\]'
            replacement = r'st.session_state.get("\1", {}).get("selection", {}).get("rows", [])'
            new_code, count = re.subn(pattern, replacement, code)
            
            # أيضاً للوصول باستخدام النقاط بدلاً من الأقواس
            pattern2 = r'st\.session_state\["([^"]+)"\]\.selection\.rows'
            replacement2 = r'st.session_state.get("\1", {}).get("selection", {}).get("rows", [])'
            new_code, count2 = re.subn(pattern2, replacement2, new_code)
            
            fixed = count > 0 or count2 > 0
            return new_code, fixed
        # إصلاح قاعدة البيانات
        current_code, fixed = self.ensure_db_initialization(current_code)
        if fixed:
            fixed_count += 1

        return current_code, fixed_count

    def fix_project_files(self, files: Dict[str, str], all_errors: Dict[str, List[Dict]]) -> Dict[str, str]:
        corrected_files = {}
        total_fixes = 0

        for file_name, code in files.items():
            # تأكد أن الكود نصي
            if isinstance(code, list):
                code = '\n'.join(code)
            elif isinstance(code, dict):
                code = str(code)
            elif code is None:
                code = ""
            
            if file_name in all_errors and all_errors[file_name]:
                corrected_code, fixes = self.fix_all_errors(code, all_errors[file_name])
                corrected_files[file_name] = corrected_code
                total_fixes += fixes
                print(f"🔧 {file_name}: تم إجراء {fixes} إصلاح(ات)")
            else:
                corrected_files[file_name] = code

        self.fix_stats["fixed"] = total_fixes
        print(f"\n📊 إجمالي الإصلاحات: {total_fixes}")
        return corrected_files

    def get_stats(self) -> Dict[str, int]:
        """إحصائيات الإصلاحات"""
        return self.fix_stats

    def get_fix_code_for_error(self, error_name: str) -> str:
        """إرجاع كود التصحيح لخطأ معين"""
        fixes = {
            "st_button_inside_st_form": "استخدم st.form_submit_button بدلاً من st.button داخل st.form",
            "dataframe_selection_subscript": "استخدم on_select='rerun' مع session_state",
            "missing_submit_button": "أضف st.form_submit_button('إرسال') داخل النموذج",
            "line_continuation_error": "قم بإزالة أحرف الهروب (\\) غير الضرورية",
            "data_editor_selection": "قم بإزالة selection_mode من st.data_editor (غير مدعوم)"
        }
        return fixes.get(error_name, "تحقق من الكود يدوياً")