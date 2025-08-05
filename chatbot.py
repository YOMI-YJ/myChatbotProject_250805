import streamlit as st
import openai
from dotenv import load_dotenv
import os

# ====== CONFIG (.env 사용) ======
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ====== 질문 리스트 ======
questions = [
    "좋아하는 사람이 생기면 어떻게 행동해?",
    "연락은 어떻게 하는 스타일이야?",
    "연애할 때 표현은 어떤 편이야?",
    "다툴 때 어떤 스타일?",
    "이별 후, 너는 어때?"
]

# ====== 세션 상태 초기화 ======
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.answers = []

st.title("💘 나의 연애 스타일은?")
st.markdown("AI가 분석해주는 나의 연애 스타일을 알아보자!(나랑 잘 맞는 스타일 추천은 덤...!)")

# ====== 설문 진행 ======
if st.session_state.step < len(questions):
    with st.chat_message("ai"):
        st.write(questions[st.session_state.step])

    user_input = st.chat_input("여기에 대답을 입력해줘!")

    if user_input:
        st.chat_message("user").write(user_input)
        st.session_state.answers.append(user_input)
        st.session_state.step += 1
        st.rerun()

# ====== 분석 요청 ======
elif st.session_state.step == len(questions):
    with st.chat_message("ai"):
        st.write("✨ 당신의 연애 성향을 분석 중이에요...")

        # 프롬프트 구성
        prompt = """다음은 사용자의 연애 성향 질문과 답변입니다:\n"""
        for i in range(len(questions)):
            prompt += f"{i+1}. {questions[i]}\n→ {st.session_state.answers[i]}\n"

        prompt += """
이 사람의 연애 성향을 분석해줘.\n
- 연애 스타일 이름\n- 성향 설명 (2~3줄)\n- 잘 맞는 연애 상대 스타일\n- 피해야 할 연애 스타일\n- 귀엽거나 감성적인 한마디 조언\n
이모지와 줄바꿈을 적절히 섞어서 따뜻하게 표현해줘.
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "너는 연애상담 전문가이자 감성적인 친구야."},
                    {"role": "user", "content": prompt}
                ]
            )
            result = response.choices[0].message.content
            st.markdown(result)
        except Exception as e:
            st.error(f"GPT 응답 실패: {e}")
