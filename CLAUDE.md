# 프로젝트 개요
공공데이터 CSV를 표.그래프.지도로 보여주는 Streamlit 웹앱. 기획서는 PLAN.md 참고.

## 파일 구조
-bike_rental.py : 메인 앱 (UI + 로직)
-ai_helper.py : Claude API를 사용하는 ask_ai() 함수 정의
-data.csv : 공공데이터 파일
-.env : ANTROPIC_API_KEY 보관

## 규칙
-기능을 만들기 전에 PLAN.md를 먼저 확인한다
-모델은 claude-haiku 사용
-API 호출은 ai helper.py에서 ask.ai 함수를 불러 쓴다
-API Key는 .env에서 읽고 코드에 직접 쓰지 않는다
-data.csv를 UTF-8로 먼저, 안 되면 cp949로 읽는다