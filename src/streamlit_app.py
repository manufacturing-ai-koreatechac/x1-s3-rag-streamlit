"""
X1-S3: 제조 지식 RAG 챗봇 Streamlit UI
실행: streamlit run src/streamlit_app.py
"""
import streamlit as st

st.set_page_config(page_title="제조 AI 챗봇", page_icon="🏭", layout="wide")

st.title("🏭 제조 지식 RAG 챗봇")
st.caption("KAMP 데이터 기반 제조 도메인 Q&A 시스템")

# 신호등 상태 표시
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🟢 시스템 상태", "정상", "ChromaDB 연결됨")
with col2:
    st.metric("📚 인덱싱 문서 수", "4개", "KAMP 문서")
with col3:
    st.metric("🔍 마지막 검색", "방금 전", "응답 시간: 0.3s")

st.divider()

# 사이드바: RAG 설정
with st.sidebar:
    st.header("⚙️ RAG 설정")
    top_k = st.slider("검색 문서 수 (Top-K)", min_value=1, max_value=5, value=2)
    st.caption("검색할 유사 문서 개수입니다.")

    st.divider()
    st.header("📋 예시 질문")
    example_questions = [
        "베어링 이상 진동 기준은?",
        "스마트공장 ROI 얼마나 돼?",
        "AutoEncoder 이상탐지 원리는?",
        "용접 품질 검사 주기는?",
    ]
    for q in example_questions:
        if st.button(q, use_container_width=True):
            st.session_state["preset_query"] = q

# 채팅 UI
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사이드바 버튼으로 질문 설정
preset = st.session_state.pop("preset_query", None)

if prompt := (st.chat_input("제조 현장 질문을 입력하세요... (예: 베어링 이상 기준은?)") or preset):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # RAG 파이프라인 (mock 응답 — 실제 운영 시 아래 블록을 실제 RAG 파이프라인으로 교체)
    with st.chat_message("assistant"):
        with st.spinner("문서 검색 중..."):
            # 실제 RAG 연동 위치 (현재는 mock 응답)
            # 실제 운영: from rag_engine import rag_pipeline; result = rag_pipeline(prompt, ...)
            mock_contexts = [
                {"topic": "베어링", "source": "설비매뉴얼", "text": "진동값 3mm/s 초과 시 위험 신호..."},
                {"topic": "이상탐지", "source": "AI가이드", "text": "재구성 오차가 임계값 초과 시 이상 판정..."},
            ]

            response = f"""**[RAG 검색 결과]**

"{prompt}"와 관련된 문서 {top_k}건을 검색했습니다.

**검색된 컨텍스트:**
"""
            for i, ctx in enumerate(mock_contexts[:top_k], 1):
                response += f"\n> [{i}] **{ctx['source']}** ({ctx['topic']}): {ctx['text']}"

            response += f"""

**현장 조치 권고:**
위 문서를 기반으로 즉각 점검 스케줄을 수립하세요.

---
*실제 운영 시 OpenAI/Claude API 연동 필요. `.env` 파일에 API 키 설정.*"""

            st.markdown(response)

            # 검색 품질 표시
            with st.expander("🔍 검색 상세 정보"):
                st.json({
                    "query": prompt,
                    "top_k": top_k,
                    "retrieved_docs": [{"source": c["source"], "topic": c["topic"]} for c in mock_contexts[:top_k]],
                    "mode": "mock (실제 운영 시 LLM API 연동)"
                })

    st.session_state.messages.append({"role": "assistant", "content": response})
