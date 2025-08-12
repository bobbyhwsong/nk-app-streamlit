import streamlit as st
import openai
import json
from datetime import datetime
import os

# OpenAI API 키 설정 (Streamlit secrets 사용)
def get_openai_api_key():
    """OpenAI API 키를 안전하게 가져오기"""
    # Streamlit Cloud에서 실행 중인 경우
    if hasattr(st, 'secrets') and 'openai' in st.secrets:
        return st.secrets['openai']['api_key']
    
    # 로컬에서 실행 중인 경우 환경 변수 사용
    return os.getenv("OPENAI_API_KEY")

# API 키 설정
api_key = get_openai_api_key()
if not api_key:
    st.error("⚠️ OpenAI API 키가 설정되지 않았습니다. Streamlit Cloud에서 secrets를 설정하거나 로컬에서 환경 변수를 설정해주세요.")
    st.stop()

# 페이지 설정
st.set_page_config(
    page_title="상담 스크립트 생성",
    page_icon="📋",
    layout="wide"
)

# 세션 상태 확인
if "messages" not in st.session_state or not st.session_state.messages:
    st.error("대화 내용이 없습니다. 먼저 의사와 상담을 진행해주세요.")
    if st.button("🏥 상담 페이지로 돌아가기"):
        st.switch_page("app.py")
    st.stop()

# 사용자 ID 확인
if "user_id" not in st.session_state or not st.session_state.user_id:
    st.error("사용자 ID가 설정되지 않았습니다. 상담 페이지에서 사용자 ID를 입력해주세요.")
    if st.button("🏥 상담 페이지로 돌아가기"):
        st.switch_page("app.py")
    st.stop()

def generate_consultation_script():
    """대화 내용을 바탕으로 상담 스크립트 생성"""
    try:
        # 대화 내용 요약
        conversation_summary = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in st.session_state.messages
        ])
        
        script_prompt = f"""다음은 환자와 의사의 상담 내용입니다:

{conversation_summary}

이 대화 내용을 바탕으로, 환자가 실제 의사를 만났을 때 준비해야 할 내용을 정리해주세요.

다음 형식으로 JSON 형태로 응답해주세요:

{{
    "patient_must_tell": {{
        "symptom_location": "어디가 아픈지 구체적인 위치",
        "symptom_timing": "언제부터 아픈지 시작 시기",
        "symptom_severity": "증상이 얼마나 심한지 강도",
        "current_medication": "현재 복용 중인 약물",
        "allergy_info": "알레르기 여부"
    }},
    "doctor_must_tell": {{
        "diagnosis_info": "의사의 진단명과 진단 근거",
        "prescription_info": "처방약의 이름과 복용 방법",
        "side_effects": "약의 부작용과 주의사항",
        "followup_plan": "다음 진료 계획과 재방문 시기",
        "emergency_plan": "증상 악화 시 언제 다시 와야 하는지"
    }}
}}"""

        # OpenAI API 호출 (새로운 형식)
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 의료 상담 전문가입니다. 환자와 의사가 준비해야 할 내용을 체계적으로 정리해주세요."},
                {"role": "user", "content": script_prompt}
            ],
            max_tokens=800,
            temperature=0.3
        )
        
        # JSON 파싱 시도
        try:
            script_data = json.loads(response.choices[0].message.content)
            return script_data
        except json.JSONDecodeError:
            # JSON 파싱 실패 시 텍스트로 반환
            return {"error": "스크립트 생성 중 오류가 발생했습니다.", "raw_response": response.choices[0].message.content}
            
    except Exception as e:
        return {"error": f"스크립트 생성 중 오류가 발생했습니다: {str(e)}"}



# 메인 UI
st.title("📋 상담 스크립트 생성")
st.markdown("---")

# 사이드바
with st.sidebar:
    st.header("📋 설정")
    
    if st.button("🏥 상담 페이지로 돌아가기"):
        st.switch_page("app.py")
    
    if st.button("🗑️ 대화 초기화"):
        st.session_state.messages = []
        st.rerun()

# 메인 콘텐츠
st.subheader("💬 대화 기록 보기")

# 대화 내용을 토글로 표시
with st.expander("📝 전체 대화 내용 보기", expanded=False):
    for i, msg in enumerate(st.session_state.messages):
        role = "환자" if msg["role"] == "user" else "의사"
        st.markdown(f"**{i+1}. {role}**")
        st.markdown(f"{msg['content']}")
        st.markdown("---")

st.markdown("---")
st.subheader("📋 스크립트 생성")

if st.button("🔄 스크립트 생성하기", type="primary", use_container_width=True):
    with st.spinner("상담 스크립트를 생성하고 있습니다..."):
        script = generate_consultation_script()
        
        if "error" not in script:
            st.success("✅ 스크립트가 성공적으로 생성되었습니다!")
            
            # 스크립트 데이터를 세션에 저장
            st.session_state.generated_script = script
            st.rerun()
        else:
            st.error(f"❌ 스크립트 생성 실패: {script['error']}")

# 생성된 스크립트 표시
if "generated_script" in st.session_state:
    script = st.session_state.generated_script
    
    st.markdown("---")
    st.subheader("🎯 생성된 상담 스크립트")
    
    # 환자가 꼭 말해야 할 내용
    st.markdown("### 🗣️ 환자가 꼭 말해야 할 내용")
    patient_info = script["patient_must_tell"]
    for key, value in patient_info.items():
        with st.expander(f"**{key.replace('_', ' ').title()}**", expanded=False):
            st.markdown(value)
    
    st.markdown("---")
    
    # 의사가 꼭 말해야 할 내용
    st.markdown("### 👨‍⚕️ 의사가 꼭 말해야 할 내용")
    doctor_info = script["doctor_must_tell"]
    for key, value in doctor_info.items():
        with st.expander(f"**{key.replace('_', ' ').title()}**", expanded=False):
            st.markdown(value)
    
    # 스크립트 다운로드
    st.markdown("---")
    st.subheader("📥 스크립트 다운로드")
    
    # 마크다운 형식으로 스크립트 생성
    script_text = f"""# 의사 상담 스크립트

생성일시: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M:%S')}

## 환자가 꼭 말해야 할 내용
"""
    for key, value in patient_info.items():
        script_text += f"### {key.replace('_', ' ').title()}\n{value}\n\n"
    
    script_text += f"""## 의사가 꼭 말해야 할 내용
"""
    for key, value in doctor_info.items():
        script_text += f"### {key.replace('_', ' ').title()}\n{value}\n\n"
    
    # 다운로드 버튼들
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="📥 마크다운 파일로 다운로드",
            data=script_text,
            file_name=f"consultation_script_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True
        )
    
    with col2:
        st.download_button(
            label="📊 JSON 파일로 다운로드",
            data=json.dumps(script, ensure_ascii=False, indent=2),
            file_name=f"consultation_script_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    # 완료 및 저장 버튼
    st.markdown("---")
    st.subheader("✅ 상담 완료")
    
    if st.button("🎯 상담 완료 및 저장", type="primary", use_container_width=True):
        # 사용자 폴더 생성 및 파일 저장
        user_folder = f"user_data/{st.session_state.user_id}"
        os.makedirs(user_folder, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 대화 기록 저장
        conversation_file = f"{user_folder}/conversation_{timestamp}.txt"
        with open(conversation_file, "w", encoding="utf-8") as f:
            f.write(f"의사 상담 대화 기록 - {st.session_state.user_id}\n")
            f.write(f"생성일시: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            
            for i, msg in enumerate(st.session_state.messages, 1):
                role = "환자" if msg["role"] == "user" else "의사"
                f.write(f"{i}. {role}: {msg['content']}\n\n")
        
        # 스크립트 저장
        script_file = f"{user_folder}/script_{timestamp}.md"
        with open(script_file, "w", encoding="utf-8") as f:
            f.write(script_text)
        
        # JSON 스크립트도 저장
        json_script_file = f"{user_folder}/script_{timestamp}.json"
        with open(json_script_file, "w", encoding="utf-8") as f:
            json.dump(script, f, ensure_ascii=False, indent=2)
        
        st.success(f"✅ 상담이 완료되었습니다!")
        st.success(f"📁 저장 위치: {user_folder}/")
        st.success(f"📝 대화 기록: conversation_{timestamp}.txt")
        st.success(f"📋 스크립트: script_{timestamp}.md")
        st.success(f"📊 JSON: script_{timestamp}.json")
        
        # 완료 후 상담 페이지로 돌아가기
        if st.button("🏥 새로운 상담 시작하기"):
            st.session_state.messages = []
            st.switch_page("app.py")

# 하단 정보
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>⚠️ 이 시스템은 교육 및 참고용이며, 실제 의료 진단을 대체할 수 없습니다.</p>
    <p>진료가 필요한 경우 반드시 전문의를 찾아 상담하시기 바랍니다.</p>
</div>
""", unsafe_allow_html=True)