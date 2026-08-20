from fastapi import Request
from datetime import datetime

def success(request: Request, data=None, message="Thành công"):
    return {
        "status": "success",
        "message": message,
        "data": data,
        "error": None,
        "timestamp": datetime.utcnow().isoformat(),
        "path": request.url.path
    }

def error(request: Request, message="Có lỗi xảy ra", code=400, detail=None):
    return {
        "status": "error",
        "message": message,
        "data": None,
        "error": {
            "code": code,
            "detail": detail
        },
        "timestamp": datetime.utcnow().isoformat(),
        "path": request.url.path
    }
