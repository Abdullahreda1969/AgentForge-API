# run_api.py - نسخة بسيطة ومضمونة
import uvicorn
print("AgentForge API - Version 2.0 with SQLite")
if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )