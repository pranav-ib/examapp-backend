from fastapi import FastAPI
from routers.exam_router import router as exam_router
from routers.recruiter_auth import router as recruiter_router
from models.exam_model import ExamJoin
from routers.exam_router import router as exam_router
from routers.student_router import router as student_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "FastAPI backend running"}

# Include exam routes
app.include_router(exam_router)
app.include_router(student_router)
app.include_router(recruiter_router)
