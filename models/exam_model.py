from typing import List
from pydantic import BaseModel

class QuestionInput(BaseModel):
    question : str
    A : str
    B : str
    C : str
    D : str
    correct : str

class CreateExam(BaseModel):
    recruiterId : str
    examTitle: str
    durationMinutes: int
    questions : List[QuestionInput]


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
