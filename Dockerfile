# syntax=docker/dockerfile:1

FROM python:3.12

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

# 6. 포트 노출 (선택 사항이지만 권장)
# 이 포트는 Dockerfile 정보용이며, 실제 Render에서는 $PORT를 사용합니다.
EXPOSE 8000

# 7. 애플리케이션 실행 명령어
# CMD 명령어는 컨테이너가 시작될 때 실행됩니다.
# main.py 파일에 app이라는 FastAPI 인스턴스가 있다고 가정합니다.
# --host 0.0.0.0: 모든 네트워크 인터페이스에서 수신
# --port $PORT: Render가 할당하는 동적 포트 환경 변수 사용
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
