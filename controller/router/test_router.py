
from fastapi import FastAPI, Request,APIRouter
from pydantic import BaseModel
import random
import json


router = APIRouter()

# 챗봇 요청 본문 모델
class KakaoChatbotRequest(BaseModel):
    userRequest: dict
    action: dict
    bot: dict
    contexts: list = [] # 컨텍스트는 선택 사항일 수 있음

# --------------------
# 1. 문제 제시 스킬 (GET /problem)
# --------------------
@router.post("/problem")
async def generate_problem(request: Request):
    """
    랜덤 2자리 덧셈 문제를 생성하고 챗봇에 응답합니다.
    정답은 컨텍스트에 저장하여 다음 스킬에서 활용할 수 있도록 합니다.
    """
    num1 = random.randint(10, 99) # 10부터 99까지의 두 자리 숫자
    num2 = random.randint(10, 99) # 10부터 99까지의 두 자리 숫자
    correct_answer = num1 + num2
    problem_text = f"다음 문제의 정답은 무엇일까요?\n{num1} + {num2} = ?"

    response_data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": { # simpleText 대신 basicCard를 사용하여 텍스트와 버튼을 함께 표시
                        "title": "산수 문제!",
                        "description": problem_text, # 문제 텍스트를 description에 포함
                        "buttons": [
                            {
                                "label": "정답 입력하기",
                                "action": "block",
                                "blockId": "687d9aa5a380e03dfc79759c" # TODO: 카카오톡 빌더의 '답변 입력 블록' ID로 변경하세요.
                            }
                        ]
                    }
                }
            ],
            "quickReplies": [ # 빠른 답변 버튼 (선택 사항)
                {
                    "label": "포기할래요",
                    "action": "block",
                    "blockId": "블록ID_산수문제시작" # TODO: 카카오톡 빌더의 시작 블록 ID로 변경하세요.
                }
            ]
        },
        "context": {
            "values": [
                {
                    "name": "Question", # 정답을 저장할 컨텍스트 변수 이름
                    "lifeSpan": 5,           # 컨텍스트 유지 시간 (요청 수)
                    "ttl": 300,          # 컨텍스트 유지 시간 (초)
                    "params": {
                    "correct_answer": str(correct_answer),                    
                    }                    
                }
            ]
        }
    }
    return response_data

# --------------------
# 2. 정오답 판별 스킬 (POST /check_answer)
# --------------------
@router.post("/check_answer")
async def check_answer(kakao_request: KakaoChatbotRequest):
    """
    사용자의 답변과 저장된 정답을 비교하여 정오답 여부를 판단합니다.
    """
    user_answer = None
    correct_answer = None

    # 사용자의 입력 값 가져오기
    # 카카오톡 챗봇 빌더에서 '사용자 발화'를 #{user_answer} 변수로 저장하여 전달한다고 가정
    # action.detailParams에서 user_answer를 직접 가져오는 방식 (챗봇 빌더 설정에 따라 다를 수 있음)
    if 'action' in kakao_request.dict() and 'detailParams' in kakao_request.action:
        if 'user_answer' in kakao_request.action['detailParams']:
            user_answer = kakao_request.action['detailParams']['user_answer']['origin']
    
    # 컨텍스트에서 저장된 정답 가져오기
    for context in kakao_request.contexts:
        if context['name'] == 'correct_answer':
            correct_answer = context['value']
            break

    message = ""
    is_correct = False

    if user_answer is None or correct_answer is None:
        message = "문제를 다시 시작해주세요. (오류 발생)"
    else:
        try:
            user_answer_int = int(user_answer)
            correct_answer_int = int(correct_answer)

            if user_answer_int == correct_answer_int:
                message = "정답입니다! 🎉 다음 문제를 풀어볼까요?"
                is_correct = True
            else:
                message = f"아쉽게도 오답입니다. 정답은 {correct_answer} 이었습니다. 😢"
                is_correct = False
        except ValueError:
            message = "숫자를 입력해주세요."
            is_correct = False

    response_data = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": message
                    }
                }
            ],
            "quickReplies": [
                {
                    "label": "새로운 문제",
                    "action": "block",
                    "blockId": "블록ID_문제제시" # TODO: 카카오톡 빌더의 '문제 제시' 블록 ID로 변경하세요.
                },
                {
                    "label": "처음으로",
                    "action": "block",
                    "blockId": "블록ID_산수문제시작" # TODO: 카카오톡 빌더의 시작 블록 ID로 변경하세요.
                }
            ]
        },
        "context": {
            "values": [
                {
                    "name": "is_correct_result", # 정오답 결과 (챗봇 빌더에서 조건 분기용)
                    "lifeSpan": 1,
                    "value": str(is_correct)
                }
            ]
        }
    }
    return response_data
