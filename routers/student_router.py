from fastapi import APIRouter
from models.exam_model import ExamJoin
from models.exam_model import SubmitExam
from supabase_client import supabase

router = APIRouter()

fake_answers = {}

@router.get("/isokay")
def isOkay():
    return {"message": "Is okay"}

@router.post("/join-exam")
def join_exam(input: ExamJoin):
    roll = input.roll_no
    code = input.exam_code

    student_res = (
        supabase.table("students")
        .select("*")
        .eq("roll_no", roll)
        .single()
        .execute()
    )

    exam_res = (
        supabase.table("exams")
        .select("*")
        .eq("exam_code", code)
        .single()
        .execute()
    )

   # questions_res = (
   #     supabase.table("questions")
   #     .select("*")
   #     .eq("exam_code", code)
   #     .execute()
   # )

    student = student_res.data
    exam = exam_res.data
   # questions = questions_res.data
    # 1. Student exists?
    if student is None:
        return {"error": "Student not found"}

    # 2. Exam exists?
    if exam is None:
        return {"error": "Invalid exam code"}

   # student = fake_students[roll]
  #  exam = fake_exams[code]

    return {
        "status": "OK",
        "student_name": student["name"],
        "exam_title": exam["title"],
        "duration": exam["duration"],
     #   "questions": questions
     #   "total_questions": exam["total_questions"]
    }


@router.post("/submit-exam")
def submit_exam(data: SubmitExam):
    code = data.exam_code
    questions_res = (
        supabase.table("questions")
        .select("*")
        .eq("exam_code", code)
        .execute()
    )
    # 1. Check if exam exists
  #  if code not in fake_exams:
    #    return {"error": "Invalid exam code"}

    # 2. Get questions for this exam
    questions = questions_res.data

    score = 0   
    for i, question in enumerate(questions):
        student_ans = data.answers[i]

        if( student_ans == question["correct_option"]):
            score += 1

    # 3. Score calculation
    
    supabase.table("student_score").insert({
        "exam_code" : code,
        "roll_no": data.roll_no,
        "score": score,
    }).execute()

    # 4. Return results
    return {
        "score": score,
        "total_questions": len(questions)
    }
