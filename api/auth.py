# api/auth.py
import secrets
from datetime import datetime
from typing import Optional, Dict

# تخزين بسيط (في الإنتاج استخدم قاعدة بيانات)
API_KEYS: Dict[str, dict] = {}

def generate_api_key(email: str, plan: str = "free", company: str = None) -> str:
    """توليد مفتاح API جديد"""
    api_key = secrets.token_urlsafe(32)
    
    limits = {"free": 100, "pro": 5000, "business": 50000}
    
    API_KEYS[api_key] = {
        "email": email,
        "plan": plan,
        "company": company,
        "monthly_limit": limits.get(plan, 100),
        "used": 0,
        "created_at": datetime.now(),
        "is_active": True
    }
    
    return api_key

def verify_api_key(api_key: str) -> Optional[dict]:
    """التحقق من صحة المفتاح"""
    if api_key not in API_KEYS:
        return None
    
    key_info = API_KEYS[api_key]
    
    if not key_info["is_active"]:
        return None
    
    if key_info["used"] >= key_info["monthly_limit"]:
        return None
    
    return key_info

def record_usage(api_key: str) -> bool:
    """تسجيل استخدام الطلب"""
    if api_key in API_KEYS:
        API_KEYS[api_key]["used"] += 1
        return True
    return False

def get_usage_stats(api_key: str) -> Optional[dict]:
    """الحصول على إحصائيات الاستخدام"""
    if api_key not in API_KEYS:
        return None
    
    key_info = API_KEYS[api_key]
    
    return {
        "email": key_info["email"],
        "plan": key_info["plan"],
        "total_requests": key_info["used"],
        "remaining_requests": key_info["monthly_limit"] - key_info["used"],
        "monthly_limit": key_info["monthly_limit"],
        "created_at": key_info["created_at"]
    }