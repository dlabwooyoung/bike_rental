import streamlit as st
import pandas as pd
from ai_helper import ask_ai

# 페이지 설정
st.set_page_config(page_title="자전거 대여소 추천", layout="wide")
st.title("🚲 자전거 대여소 추천 앱")

# 데이터 로드 함수
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('bike rental.py/data.csv', encoding='cp949')
    except:
        df = pd.read_csv('bike rental.py/data.csv', encoding='utf-8')
    return df

# 데이터 로드
df = load_data()

# 사이드바 설정
st.sidebar.header("🔍 검색 설정")

# 입력: 지역 입력
region = st.sidebar.text_input("지역을 입력하세요", value="강남역")

# 스타일 선택 (처리)
style = st.sidebar.radio(
    "자신의 스타일을 정하세요",
    ["🏃 빠른 이동", "🚴 여유로운 산책", "🎒 관광 투어"],
    index=0
)

# 검색 버튼
search_btn = st.sidebar.button("🔎 자전거 대여소 추천받기")

# 추천 로직
if search_btn:
    if region.strip():
        # Claude API를 활용한 추천
        prompt = f"""
        사용자가 '{region}' 지역에서 자전거 대여소 추천을 요청했습니다.
        사용자의 스타일: {style}

        아래는 서울시 자전거 대여소 ID 목록입니다:
        {', '.join(df['대여소ID'].unique()[:30])}

        '{region}' 지역과 가장 유사한 자전거 대여소 3개를 추천해주세요.
        응답 형식: "ST-123, ST-456, ST-789" (쉼표로 구분된 ID만)
        """

        with st.spinner("추천을 받고 있습니다..."):
            try:
                response = ask_ai(prompt)
                st.session_state.recommendations = response.strip()
                st.success("✅ 추천 완료!")
            except Exception as e:
                st.error(f"오류 발생: {e}")
    else:
        st.warning("지역을 입력해주세요.")

# 추천 결과 표시 (출력)
if 'recommendations' in st.session_state and st.session_state.recommendations:
    st.header(f"📍 '{region}' 지역의 추천 대여소 (스타일: {style})")

    # 추천된 대여소 파싱
    rental_ids = [id.strip() for id in st.session_state.recommendations.split(',')]

    # 추천 대여소 표시
    cols = st.columns(3)
    for i, rental_id in enumerate(rental_ids[:3]):
        with cols[i]:
            if st.button(f"📌 {rental_id}", key=f"rental_{i}"):
                st.session_state.selected_rental = rental_id

# 선택된 대여소의 자전거 상태 표시 (처리 - 대여소 클릭)
if 'selected_rental' in st.session_state:
    selected = st.session_state.selected_rental
    st.header(f"🚲 '{selected}' 자전거 상태")

    # 해당 대여소의 데이터 필터링
    rental_data = df[df['대여소ID'] == selected]

    if not rental_data.empty:
        # 최신 데이터 가져오기
        latest_data = rental_data.iloc[-1]

        # 주요 정보 표시
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("대여소 번호", latest_data['대여소번호'])
        with col2:
            st.metric("현재 자전거 수", latest_data['거치수량'])
        with col3:
            st.metric("마지막 업데이트", latest_data['일시'])

        # 자전거 상태 시각화
        st.subheader("📊 자전거 거치 현황")

        # 시간대별 변화 차트
        time_series = rental_data.copy()
        time_series['일시'] = pd.to_datetime(time_series['일시'])
        time_series = time_series.sort_values('일시')

        st.line_chart(
            time_series.set_index('일시')['거치수량'],
            title="시간대별 자전거 거치 수량 변화"
        )

        # 상세 데이터 테이블
        st.subheader("📋 상세 정보")
        st.dataframe(rental_data[['일시', '대여소번호', '거치수량']])
    else:
        st.error(f"'{selected}' 대여소의 데이터를 찾을 수 없습니다.")

# 사이드바 - 데이터 정보
st.sidebar.divider()
st.sidebar.info(
    f"""
    📊 **데이터 정보**
    - 전체 대여소: {df['대여소ID'].nunique()}개
    - 데이터 기간: {df['일시'].min()} ~ {df['일시'].max()}
    - 총 레코드: {len(df):,}개
    """
)
