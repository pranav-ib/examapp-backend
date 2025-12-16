import time
from fastapi import APIRouter
from models.exam_model import CreateExam, AddQuestion, SubmitExam
import random

from supabase_client import supabase

router = APIRouter()

@router.post("/create-exam")
def create_exam(data: CreateExam):


    MAX_ATTEMPTS = 5

    for attempts in range(MAX_ATTEMPTS):
        code = str(random.randint(100000, 999999))

        try:
            supabase.table("exams").insert({
                "exam_code" : code,
                "title" : data.examTitle,
                "duration" : data.durationMinutes,
                "recruiter_id" : data.recruiterId
            }).execute()

            for q in data.questions:
                supabase.table("questions").insert({
                    "exam_code" : code,
                    "question": q.question,
                    "options": [q.A, q.B, q.C, q.D],
                    "correct_option": q.correct
                }).execute()

            return {"message": "Exam created",
                    "exam_code": code
            }
        
        except Exception as e:
            if "duplicate key" in str(e):
                print(f"Duplicate exam code : {code}. Retrying...")
                continue

            raise e
    return {
        "error": "Unable to generate unique exam code. Try again."
    }


@router.post("/add-question")
def add_question(data: AddQuestion):
    exam = supabase.table("exams").select("*").eq("exam_code", data.exam_code).single().execute()

    if exam.data is None:
        return {"error": "Invalid exam code"}

  

    exam_id = exam.data["id"]

    supabase.table("questions").insert({
        "exam_code" : exam_id,
        "question": data.question,
        "options": data.options,
        "correct_option": data.correct_option
    }).execute()

  #  fake_exams[data.exam_code]["total_questions"] += 1

    return {"status": "Question added"}

@router.get("/get-questions/{exam_code}")
def get_questions(exam_code: str):
    exam = supabase.table("exams").select("*").eq("exam_code",exam_code).single().execute()

    if exam.data is None:
        return {"error": "Invalid exam code"}
    
    return fake_exams[exam_code]["questions"]

@router.get("/start-exam/{exam_code}")
def start_exam(exam_code: str):
    questions_res = (
        supabase.table("questions")
        .select("*")
        .eq("exam_code", exam_code)
        .execute()
    )

    questions = questions_res.data
    server_time = time.time()
    return {
        "exam_code" : exam_code,
        "server_time" : server_time,
        "questions" : questions        
    }

@router.get("/get-my-exam")
def get_exams(recruiter_id: str):
    exams = (
        supabase.table("exams")
        .select("id, title, exam_code, attended_count")
        .eq("recruiter_id", recruiter_id)
        .execute()
    )
    return {"exams" : exams.data}