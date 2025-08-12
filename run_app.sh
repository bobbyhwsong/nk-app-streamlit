#!/bin/bash

# 의사 상담 시스템 실행 스크립트

echo "🏥 AI 의사 상담 시스템을 시작합니다..."

# conda 환경 활성화
echo "📦 conda 환경을 활성화합니다..."
source ~/miniconda3/etc/profile.d/conda.sh
conda activate voice_app

# 현재 디렉토리 확인
echo "📁 현재 디렉토리: $(pwd)"

# 필요한 패키지 설치 확인
echo "🔍 필요한 패키지를 확인합니다..."
pip install -r requirements.txt

# OpenAI API 키 확인
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY 환경 변수가 설정되지 않았습니다."
    echo "📝 .env 파일을 생성하거나 환경 변수를 설정해주세요."
    echo "예시: export OPENAI_API_KEY='your_api_key_here'"
    echo ""
    echo "또는 .env 파일을 생성:"
    echo "echo 'OPENAI_API_KEY=your_api_key_here' > .env"
    exit 1
fi

echo "✅ OpenAI API 키가 설정되었습니다."

# Streamlit 애플리케이션 실행
echo "🚀 Streamlit 애플리케이션을 시작합니다..."
echo "🌐 브라우저에서 http://localhost:8501 로 접속하세요."
echo "⏹️  종료하려면 Ctrl+C를 누르세요."
echo ""

streamlit run app.py
