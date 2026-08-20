from fastapi import HTTPException

def not_found(detail="Không tìm thấy tài nguyên"):
    raise HTTPException(status_code=404, detail=detail)

def bad_request(detail="Dữ liệu không hợp lệ"):
    raise HTTPException(status_code=400, detail=detail)

def forbidden(detail="Bạn không có quyền truy cập"):
    raise HTTPException(status_code=403, detail=detail)
