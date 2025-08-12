# 🏥 AI 의사 상담 시스템

Streamlit과 OpenAI GPT를 활용한 의사 상담 시뮬레이션 시스템입니다.

## 🚀 주요 기능

- **의사 페르소나**: 경험 많은 내과 전문의로 설정된 AI와 상담
- **실시간 채팅**: 자연스러운 대화를 통한 증상 상담
- **스크립트 생성**: 대화 내용을 바탕으로 한 상담 준비 스크립트
- **대화 로그 저장**: 상담 내용을 파일로 저장하여 나중에 참고

## 📋 상담 스크립트 구성

### 환자가 꼭 말해야 할 내용
1. **증상 위치** (symptom_location): 어디가 아픈지 구체적인 위치
2. **증상 시기** (symptom_timing): 언제부터 아픈지 시작 시기
3. **증상 강도** (symptom_severity): 증상이 얼마나 심한지 강도
4. **현재 복용 약물** (current_medication): 현재 복용 중인 약물
5. **알레르기 정보** (allergy_info): 알레르기 여부

### 의사가 꼭 말해야 할 내용
6. **진단 정보** (diagnosis_info): 의사의 진단명과 진단 근거
7. **처방 정보** (prescription_info): 처방약의 이름과 복용 방법
8. **부작용** (side_effects): 약의 부작용과 주의사항
9. **후속 계획** (followup_plan): 다음 진료 계획과 재방문 시기
10. **응급 계획** (emergency_plan): 증상 악화 시 언제 다시 와야 하는지

## 🛠️ 설치 및 설정

### 1. 환경 설정
```bash
# conda 환경 활성화
conda activate voice_app

# 필요한 패키지 설치
pip install -r requirements.txt
```

### 2. 실행 방법

#### 🔑 OpenAI API 키 설정
```bash
# 환경 변수로 설정
export OPENAI_API_KEY="your_actual_api_key_here"
```

#### 🚀 로컬 실행
```bash
# 애플리케이션 실행
streamlit run app.py --server.port 8501
```

### 3. Streamlit Cloud 배포

#### 📋 배포 준비
1. GitHub에 코드 업로드
2. [Streamlit Cloud](https://streamlit.io/cloud)에 로그인
3. "New app" 클릭하여 GitHub 저장소 연결

#### 🔐 Secrets 설정
Streamlit Cloud에서 다음 secrets를 설정:
```toml
[openai]
api_key = "your_openai_api_key_here"
```

#### 🎯 배포 설정
- **Main file path**: `app.py`
- **Python version**: 3.11
- **Requirements file**: `requirements.txt`

### 4. 실행 스크립트 사용
```bash
# 실행 권한 부여 (최초 1회)
chmod +x run_app.sh

# 스크립트로 실행
./run_app.sh
```

## 📱 사용법

1. **상담 시작**: 증상이나 궁금한 점을 입력하여 AI 의사와 대화를 시작합니다.
2. **상담 진행**: 의사가 질문하는 내용에 답변하며 상담을 진행합니다.
3. **스크립트 생성**: 상담이 끝나면 "스크립트 생성" 버튼을 눌러 정리된 내용을 확인합니다.
4. **내용 저장**: 생성된 스크립트를 다운로드하거나 대화 로그를 파일로 저장할 수 있습니다.

## 🔍 데모 vs 전체 기능

| 기능 | 데모 버전 | 전체 기능 버전 |
|------|-----------|----------------|
| **API 키** | 불필요 | OpenAI API 키 필요 |
| **응답 품질** | 제한적 (키워드 기반) | GPT-3.5-turbo 기반 고품질 |
| **맞춤형 응답** | 기본 응답 패턴 | 대화 맥락 기반 맞춤형 |
| **스크립트 생성** | 고정된 템플릿 | 대화 내용 기반 동적 생성 |
| **사용 목적** | 테스트 및 데모 | 실제 상담 시뮬레이션 |

## ⚠️ 주의사항

- 이 시스템은 **교육 및 참고용**이며, 실제 의료 진단을 대체할 수 없습니다.
- 진료가 필요한 경우 반드시 전문의를 찾아 상담하시기 바랍니다.
- OpenAI API 사용량에 따른 비용이 발생할 수 있습니다.

## 🔧 기술 스택

- **Frontend**: Streamlit
- **AI Model**: OpenAI GPT-3.5-turbo (전체 기능 버전)
- **Language**: Python 3.11+
- **Environment**: Conda

## 📁 파일 구조

```
chatgpt/
├── app.py                           # 메인 Streamlit 애플리케이션
├── pages/
│   └── 1_script_generator.py      # 상담 스크립트 생성 페이지
├── requirements.txt                 # 필요한 Python 패키지 목록
├── .streamlit/
│   └── config.toml                 # Streamlit 설정 파일
├── run_app.sh                      # 실행 스크립트
└── README.md                       # 이 파일
```

## 🚀 빠른 시작

### 1단계: 로컬에서 테스트
```bash
cd chatgpt
conda activate voice_app

# API 키 설정
export OPENAI_API_KEY="your_key_here"

# 애플리케이션 실행
streamlit run app.py --server.port 8501
```

### 2단계: Streamlit Cloud 배포
1. GitHub에 코드 푸시
2. Streamlit Cloud에서 secrets 설정
3. 자동 배포 완료

### 3단계: 브라우저에서 접속
- 로컬: `http://localhost:8501`
- 클라우드: Streamlit Cloud에서 제공하는 URL

## 💡 팁

- **API 키 설정**: OpenAI 웹사이트에서 API 키를 발급받아 설정하세요
- **Streamlit Cloud**: 무료로 웹 애플리케이션을 배포할 수 있습니다
- **Secrets 관리**: API 키는 Streamlit Cloud의 secrets 기능을 사용하여 안전하게 관리하세요
- **포트 충돌**: 이미 사용 중인 포트가 있다면 `--server.port` 옵션으로 변경하세요
