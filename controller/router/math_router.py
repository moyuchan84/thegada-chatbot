
from fastapi import APIRouter, Body
from application.service.math_service import MathService
from domain.model.request import Request
from domain.model.response import Response

router = APIRouter()
math_service = MathService()

@router.post("/question", response_model=Response)
async def generate_question():
    return math_service.generate_question()

@router.post("/question/text", response_model=Response)
async def generate_question_simple_text():
    return math_service.generate_question_simple_text()


@router.post("/solve", response_model=Response)
async def solve_question(request: Request = Body(...)):
    return math_service.solve_question(request.userRequest.utterance, request.contexts)
