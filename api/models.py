# api/models.py
# api/models.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ProjectType(str, Enum):
    """أنواع المشاريع المتاحة"""
    AUTO = "auto"
    TASK = "task"
    CONTACT = "contact"
    PRODUCT = "product"
    LIBRARY = "library"
    APPOINTMENT = "appointment"
    RESTAURANT = "restaurant"
    HOTEL = "hotel"

class GenerateRequest(BaseModel):
    """طلب توليد مشروع جديد"""
    description: str = Field(..., description="وصف المشروع", min_length=10, max_length=2000)
    project_name: Optional[str] = Field(None, description="اسم المشروع (اختياري)")
    project_type: ProjectType = Field(ProjectType.AUTO, description="نوع المشروع")
    
    class Config:
        json_schema_extra = {
            "example": {
                "description": "Create a contact book app with name and phone number",
                "project_name": "My_Contact_Book",
                "project_type": "contact"
            }
        }

class GenerateResponse(BaseModel):
    """رد خدمة التوليد"""
    success: bool
    project_id: str
    download_url: Optional[str] = None
    message: str
    generated_at: datetime = Field(default_factory=datetime.now)
    used_type: str = Field("auto", description="نوع المشروع الذي تم استخدامه فعلياً")

class APIKeyRequest(BaseModel):
    """طلب إنشاء مفتاح API جديد"""
    email: str = Field(..., description="البريد الإلكتروني")
    plan: str = Field("free", description="نوع الباقة: free, pro, business")
    company: Optional[str] = Field(None, description="اسم الشركة")

class APIKeyResponse(BaseModel):
    """رد إنشاء مفتاح API"""
    api_key: str
    plan: str
    monthly_limit: int
    created_at: datetime
    expires_at: Optional[datetime] = None

class UsageStats(BaseModel):
    """إحصائيات الاستخدام"""
    total_requests: int
    remaining_requests: int
    monthly_limit: int
    plan: str
    email: str