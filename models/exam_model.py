from pydantic import BaseModel

class CreateExam(BaseModel):
    title: str
    duration: int
    recruiter_id : str

class AddQuestion(BaseModel):
    exam_code: str
    question: str
    options: list
    correct_option: int


class ExamJoin(BaseModel):
    roll_no: str
    exam_code: str

class ExamStart(BaseModel):
    exam_code: str
    

class SubmitExam(BaseModel):
    exam_code: int
    roll_no : str
    answers: list[int]
