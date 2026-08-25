from fastapi import HTTPException
from datetime import datetime, timezone


def not_found(
    detail="Không tìm thấy tài nguyên",
    resource_id=None
):
    raise HTTPException(
        status_code=404,
        detail={
            "status": "error",
            "status_code": 404,
            "message": detail,
            "resource_id": resource_id,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    )


def bad_request(
    detail="Dữ liệu không hợp lệ",
    resource_id=None
):
    raise HTTPException(
        status_code=400,
        detail={
            "status": "error",
            "status_code": 400,
            "message": detail,
            "resource_id": resource_id,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    )


def forbidden(
    detail="Bạn không có quyền truy cập",
    resource_id=None
):
    raise HTTPException(
        status_code=403,
        detail={
            "status": "error",
            "status_code": 403,
            "message": detail,
            "resource_id": resource_id,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    )