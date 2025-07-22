import random
from domain.model.response import (
    Response, SkillTemplate, Component, BasicCard, Thumbnail, QuickReply, ContextControl, ContextValue
)

class MathService:
    def generate_question(self) -> Response:
        num1 = random.randint(10, 99)
        num2 = random.randint(10, 99)
        question = f"{num1} + {num2} = ?"
        answer = str(num1 + num2)

        response = Response(
            template=SkillTemplate(
                outputs=[
                    Component(
                        basicCard=BasicCard(
                            title="두뇌 풀가동! 수학 퀴즈",
                            description=question,
                            thumbnail=Thumbnail(
                                imageUrl="https://img.hankyung.com/photo/202401/AA.35389870.1.jpg"),
                            quickReplies=[
                                QuickReply(label="포기", action="message", messageText="포기")
                            ]
                        )
                    )
                ]
            ),
            context=ContextControl(
                values=[
                    ContextValue(key="answer", value=answer)
                ]
            )
        )
        return response

    def solve_question(self, utterance: str, contexts: list) -> Response:
        try:
            user_answer = int(utterance)
            # Extract the answer from the context
            # The context is a list of dictionaries, we need to find the one with the name 'answer'
            answer_context = next((ctx for ctx in contexts if ctx.get('name') == 'answer'), None)
            if answer_context:
                correct_answer = int(answer_context['params']['answer']['value'])
                if user_answer == correct_answer:
                    text = "정답입니다!"
                else:
                    text = f"아쉽지만 오답입니다. 정답은 {correct_answer} 입니다."
            else:
                text = "정답을 찾을 수 없습니다. 다시 시도해주세요."

        except (ValueError, IndexError):
            text = "정답을 다시 입력해주세요."

        response = Response(
            template=SkillTemplate(
                outputs=[
                    Component(
                        basicCard=BasicCard(
                            description=text
                        )
                    )
                ]
            )
        )
        return response