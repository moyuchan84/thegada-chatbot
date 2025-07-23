from fastapi import APIRouter, Body
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional

from controller.router.test_router import KakaoChatbotRequest

router = APIRouter()

# --- Pydantic Models for Kakao Validation API ---

class ValidationValue(BaseModel):
    origin: str
    value: str
    groupName: str

class ValidationRequest(BaseModel):
    userRequest: dict
    contexts: list
    value: ValidationValue
    action: dict

class ValidationResponse(BaseModel):
    status: str  # "OK" or "FAIL"
    message: Optional[str] = None

# --- Correct Answers ---

ANSWERS = {
    "1": 2,
    "2": 6,
    "3": 81
}
# --- Pydantic Models for Kakao Chatbot Validation Request ---
# 'value' 필드의 상세 구조
class ValidationRequestValue(BaseModel):
    origin: str = Field(..., description="사용자 입력의 원본 문자열")
    resolved: str = Field(..., description="AIU(인공지능 이해) 또는 기타 방법에 의해 해석된 값")

# 'user' 필드의 상세 구조
class ValidationRequestUser(BaseModel):
    id: str = Field(..., description="사용자 ID")
    type: str = Field(..., description="ID의 타입 (예: KAKAO_TALK_V2)")

# 전체 Validation API 요청 본문 구조
class ValidationRequest(BaseModel):
    isInSlotFilling: bool = Field(..., description="슬롯 필링 진행 중인지 여부")
    utterance: str = Field(..., description="현재 요청의 사용자 발화")
    value: ValidationRequestValue
    user: ValidationRequestUser


# --- Response Model for Validation ---
# Validation API의 응답 본문 구조 (새로운 가이드 반영)
class ValidationResponse(BaseModel):
    status: str = Field(..., description="'SUCCESS', 'FAIL', 'ERROR', 'IGNORE' 중 하나")
    value: Optional[str] = Field(None, description="Action에 의해 해석된 값 (선택 사항)")
    data: Optional[Dict[str, Any]] = Field(None, description="클라이언트에 전달하고자 하는 데이터 (선택 사항)")
    message: Optional[str] = Field(None, description="응답 메시지 (선택 사항)")


# --- Validation Logic ---
async def validate_answer(question_id: str, request_data: ValidationRequest):
    """
    사용자 답변을 검증하고 결과를 반환합니다.
    """
    try:
        # 사용자의 답변을 'origin' 필드에서 가져옴
        user_answer_str = request_data.value.origin
        
        if not user_answer_str:
            return ValidationResponse(status="FAIL", message="답변 내용을 찾을 수 없습니다.")

        # 사용자의 답변을 정수로 변환 시도
        try:
            user_answer = int(user_answer_str)
        except ValueError:
            return ValidationResponse(status="FAIL", message="숫자로만 답변해주세요.")
        
        # 문제 ID에 해당하는 정답을 ANSWERS 딕셔너리에서 가져옴
        correct_answer = ANSWERS.get(question_id)

        if correct_answer is None:
            # 존재하지 않는 문제 ID가 요청된 경우
            return ValidationResponse(status="ERROR", message="서버 오류: 유효하지 않은 문제 ID입니다.")

        # 정답 비교
        if user_answer == correct_answer:
            return ValidationResponse(
                status="SUCCESS",
                value=str(user_answer), # 성공 시 해석된 값을 반환
                message="정답입니다! 🎉"
            )
        else:
            return ValidationResponse(
                status="FAIL",
                value=str(user_answer), # 오답이어도 입력된 값은 반환 가능
                message=f"오답입니다. 정답은 {correct_answer}이었습니다. 😢"
            )

    except Exception as e:
        # 그 외 예상치 못한 오류 발생 시
        return ValidationResponse(
            status="ERROR",
            message=f"처리 중 알 수 없는 서버 오류가 발생했습니다: {type(e).__name__} - {e}"
        )


# --- API Endpoints ---
# 각 API 엔드포인트에 새로운 Request 및 Response 모델 적용
@router.post("/1", response_model=ValidationResponse)
async def validate_question_1(request_data: ValidationRequest):
    return await validate_answer("1", request_data)

@router.post("/2", response_model=ValidationResponse)
async def validate_question_2(request_data: ValidationRequest):
    return await validate_answer("2", request_data)

@router.post("/3", response_model=ValidationResponse)
async def validate_question_3(request_data: ValidationRequest):
    return await validate_answer("3", request_data)



import re
# --- Game Code Validation Logic ---
async def validate_game_code_logic(request_data: ValidationRequest):
    """
    '더가다' + 숫자 4자리 형식의 game_code를 검증합니다.
    """
    try:
        # 사용자의 입력(utterance) 또는 value.origin을 game_code로 사용
        # 여기서는 value.origin을 사용하겠습니다.
        game_code_input = request_data.value.origin.strip() # 공백 제거

        if not game_code_input:
            return ValidationResponse(status="FAIL", message="게임 코드를 입력해주세요.")

        # 정규표현식을 사용하여 '더가다' + 숫자 4자리 형식 검증
        # ^: 문자열의 시작
        # 더가다: 리터럴 문자열 "더가다"
        # \d{4}: 정확히 4개의 숫자 (0-9)
        # $: 문자열의 끝
        pattern = re.compile(r"^더가다\d{4}$")

        if pattern.match(game_code_input):
            # 정규표현식에 매치되는 경우 SUCCESS
            return ValidationResponse(
                status="SUCCESS",
                value=game_code_input, # 유효한 게임 코드를 value로 반환
                message=f"'{game_code_input}'은(는) 유효한 게임 코드입니다!"
            )
        else:
            # 매치되지 않는 경우 FAIL
            return ValidationResponse(
                status="FAIL",
                value=game_code_input, # 어떤 코드가 실패했는지 알려줄 수 있음
                message="게임 코드는 '더가다'로 시작하고 뒤에 숫자 4자리가 와야 합니다. (예: 더가다1234)"
            )

    except Exception as e:
        # 예상치 못한 오류 발생 시 ERROR
        return ValidationResponse(
            status="ERROR",
            message=f"게임 코드 검증 중 알 수 없는 서버 오류가 발생했습니다: {type(e).__name__} - {e}"
        )

# --- API Endpoints ---
# 새로운 게임 코드 검증 엔드포인트
@router.post("/validate_game_code", response_model=ValidationResponse)
async def validate_game_code(request_data: ValidationRequest):
    return await validate_game_code_logic(request_data)
