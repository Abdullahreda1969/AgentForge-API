# api/main.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from local.orchestrator import LocalOrchestrator
from api.models import GenerateRequest, GenerateResponse, APIKeyRequest, APIKeyResponse, UsageStats
from api.auth import generate_api_key, verify_api_key, record_usage, get_usage_stats

# تهيئة التطبيق
app = FastAPI(
    title="AgentForge API",
    description="Generate complete applications from text descriptions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# إضافة CORS (للسماح بالطلبات من أي مكان)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تهيئة المحرك
orchestrator = LocalOrchestrator()

# ============ Endpoints ============

@app.get("/")
async def root():
    """الصفحة الرئيسية للـ API"""
    return {
        "service": "AgentForge API",
        "version": "1.0.0",
        "description": "Generate complete applications from text descriptions",
        "endpoints": {
            "POST /v1/generate": "Generate a new project",
            "POST /v1/api-key": "Request an API key",
            "GET /v1/stats": "Get your usage statistics",
            "GET /health": "Health check"
        },
        "documentation": "/docs"
    }

@app.get("/health")
async def health_check():
    """فحص صحة الخدمة"""
    return {"status": "healthy"}

@app.post("/v1/api-key", response_model=APIKeyResponse)
async def create_api_key(request: APIKeyRequest):
    """إنشاء مفتاح API جديد"""
    api_key = generate_api_key(
        email=request.email,
        plan=request.plan,
        company=request.company
    )
    
    limits = {"free": 100, "pro": 5000, "business": 50000}
    
    return APIKeyResponse(
        api_key=api_key,
        plan=request.plan,
        monthly_limit=limits.get(request.plan, 100),
        created_at=datetime.now(),
        expires_at=None
    )

@app.post("/v1/generate", response_model=GenerateResponse)
async def generate_project(
    request: GenerateRequest,
    x_api_key: str = Header(...)
):
    """توليد مشروع جديد"""
    
    # التحقق من المفتاح
    user = verify_api_key(x_api_key)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired API key")
    
    # تحديد اسم المشروع
    project_name = request.project_name or f"api_project_{user['email'].split('@')[0]}"
    project_name = project_name.replace(" ", "_")
    
    try:
        # توليد المشروع
        result = orchestrator.generate(project_name, request.description)
        
        if result["status"] == "completed":
            # تسجيل الاستخدام
            record_usage(x_api_key)
            
            # رابط التحميل
            download_url = f"/download/{project_name}.zip"
            
            return GenerateResponse(
                success=True,
                project_id=project_name,
                download_url=download_url,
                message=f"Project '{project_name}' generated successfully"
            )
        else:
            return GenerateResponse(
                success=False,
                project_id=project_name,
                message=f"Generation failed: {result.get('reason', 'Unknown error')}"
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
async def download_project(filename: str):
    """تحميل مشروع مولد"""
    file_path = os.path.join("projects", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        file_path,
        media_type="application/zip",
        filename=filename
    )

@app.get("/v1/stats", response_model=UsageStats)
async def get_stats(x_api_key: str = Header(...)):
    """الحصول على إحصائيات الاستخدام"""
    stats = get_usage_stats(x_api_key)
    
    if not stats:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return UsageStats(**stats)