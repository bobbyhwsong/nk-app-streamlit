import streamlit as st
import openai
import json
from datetime import datetime

# OpenAI API 키 설정 (Streamlit secrets 사용)
def get_openai_api_key():
    """OpenAI API 키를 안전하게 가져오기"""
    # Streamlit Cloud에서 실행 중인 경우
    if hasattr(st, 'secrets') and 'openai' in st.secrets:
        return st.secrets['openai']['api_key']
    
    # 로컬에서 실행 중인 경우 환경 변수 사용
    import os
    return os.getenv("OPENAI_API_KEY")

# API 키 설정
api_key = get_openai_api_key()
if not api_key:
    st.error("⚠️ OpenAI API 키가 설정되지 않았습니다. Streamlit Cloud에서 secrets를 설정하거나 로컬에서 환경 변수를 설정해주세요.")
    st.stop()

# 페이지 설정
st.set_page_config(
    page_title="의사 상담 시스템",
    page_icon="🏥",
    layout="wide"
)

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
    # 의사의 초기 인사 메시지 추가
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "안녕하세요! 어떻게 오셨나요?"
    })
if "conversation_log" not in st.session_state:
    st.session_state.conversation_log = []

# 의사 페르소나 설정
DOCTOR_SYSTEM_PROMPT = """당신은 50대 남성의 경험 많은 내과 의사입니다. 환자와의 대화에서 다음 사항을 지켜주세요:

1. 무심한 말투로 대화하세요.
2. 의학용어는 쉽게 설명하되, 간결하게 하세요.
3. 환자의 메시지에 대해 간결하게, 적절한 응답을 해주세요.
4. 길게 말하지 말고, 존대말로 하세요.

환자는 다음의 사항 중에 하나 또는 여러 개를 물어볼거야.
환자의 메시지에 따라 적절한 응답을 해주세요.

환자 입장에서 꼭 말해야 하는 것:
1. symptom_location: 어디가 아픈지 구체적인 위치
2. symptom_timing: 언제부터 아픈지 시작 시기  
3. symptom_severity: 증상이 얼마나 심한지 강도
4. current_medication: 현재 복용 중인 약물
5. allergy_info: 알레르기 여부

진료과정 중에 의사한테 꼭 들어야 하는 것:
6. diagnosis_info: 의사의 진단명과 진단 근거
7. prescription_info: 처방약의 이름과 복용 방법
8. side_effects: 약의 부작용과 주의사항
9. followup_plan: 다음 진료 계획과 재방문 시기
10. emergency_plan: 증상 악화 시 언제 다시 와야 하는지"""

def generate_doctor_response(user_message):
    """의사 페르소나로 GPT 응답 생성"""
    try:
        # 대화 히스토리 구성
        messages = [
            {"role": "system", "content": DOCTOR_SYSTEM_PROMPT},
        ]
        
        # 이전 대화 내용 추가
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                messages.append({"role": "user", "content": msg["content"]})
            elif msg["role"] == "assistant":
                messages.append({"role": "assistant", "content": msg["content"]})
        
        # 현재 사용자 메시지 추가
        messages.append({"role": "user", "content": user_message})
        
        # OpenAI API 호출 (새로운 형식)
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"죄송합니다. 오류가 발생했습니다: {str(e)}"





# 메인 UI
st.title("🏥 AI 의사 상담 시스템")
st.markdown("---")

# 사이드바
with st.sidebar:
    st.header("📋 설정")
    
    # 사용자 ID 입력
    st.markdown("### 👤 사용자 정보")
    user_id = st.text_input("사용자 ID를 입력하세요", placeholder="예: user001", key="user_id_input")
    
    if user_id:
        st.session_state.user_id = user_id
        st.success(f"✅ {user_id}님 환영합니다!")
    else:
        st.warning("⚠️ 사용자 ID를 입력해주세요.")
    
    st.markdown("---")
    
    if st.button("🗑️ 대화 초기화"):
        st.session_state.messages = []
        st.session_state.conversation_log = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📋 스크립트 생성")
    if st.button("🔄 상담 스크립트 생성하기", type="primary", use_container_width=True, disabled=not user_id):
        if st.session_state.messages:
            # 스크립트 페이지로 이동
            st.switch_page("pages/1_script_generator.py")
        else:
            st.warning("먼저 의사와 대화를 나누어주세요.")

# 메인 채팅 영역
st.subheader("💬 의사와 상담하기")

# 채팅 메시지 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
if prompt := st.chat_input("증상이나 궁금한 점을 말씀해주세요..."):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 의사 응답 생성
    with st.chat_message("assistant"):
        with st.spinner("의사가 응답을 준비하고 있습니다..."):
            response = generate_doctor_response(prompt)
            st.markdown(response)
    
    # 의사 응답을 메시지에 추가
    st.session_state.messages.append({"role": "assistant", "content": response})
