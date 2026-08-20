from fastapi import FastAPI,Request
from app.db.database import Base,engine
from app.models  import user,event,event_task
from app.core.response import success
app = FastAPI(
    title="EVENT MANAGEMENT API"
)

Base.metadata.create_all(bind = engine)

@app.get("/")
def get_root():
    return {
        "message": "CHAO MUNG DEN VOI EVENT MANAGEMENT API"
    }

@app.get("/health")
def health_check(request:Request):
    return success(request,None,"API ĐANG HOẠT ĐỘNG")