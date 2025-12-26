# app.py - 최종 완성형 (RAG + Vision + Tools + Memory + GUI)
import streamlit as st
import ollama
import os
import shutil
from tts_engine import speak
from vision_engine import analyze_image
from function_engine import execute_command, save_to_file
from rag_engine import process_document, query_rag
# [신규] 기억 관리 모듈 가져오기
from db_handler import init_db, save_message, load_messages, clear_db

# 0. DB 초기화 (앱 켤 때 한 번 실행)
init_db()

st.set_page_config(page_title="Jarvis Pro", page_icon="🧠", layout="wide")
st.title("🧠 JARVIS Pro (Memory Edition)")
st.caption("기억력(DB)까지 갖춘 완벽한 로컬 AI 에이전트")

# 2. 사이드바
with st.sidebar:
    st.header("⚙️ 제어 패널")
    voice_on = st.toggle("음성 답변 (TTS)", value=True)
    st.divider()
    
    st.header("📚 지식 주입 (RAG)")
    uploaded_file = st.file_uploader("학습용 문서(PDF)", type=['pdf'])
    
    if uploaded_file is not None:
        save_path = os.path.join(os.getcwd(), uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        if "last_uploaded" not in st.session_state or st.session_state.last_uploaded != uploaded_file.name:
            with st.spinner("문서 학습 중..."):
                result_msg = process_document(save_path)
                st.success(result_msg)
                st.session_state.last_uploaded = uploaded_file.name
                
        if os.path.exists(save_path):
            os.remove(save_path)

    st.divider()
    
    # [수정됨] 기억 삭제 버튼이 DB까지 날리도록 변경
    if st.button("🗑️ 대화 기억 삭제"):
        clear_db() # DB 삭제
        st.session_state.messages = [] # 화면 삭제
        st.rerun()

    st.header("🖼️ 이미지 분석")
    uploaded_image = st.file_uploader("이미지 파일", type=['png', 'jpg', 'jpeg'])

# 3. [중요] 세션 기록 초기화 (DB 연동) ⭐
if "messages" not in st.session_state:
    # DB에서 과거 기록을 불러옵니다.
    db_history = load_messages()
    
    if db_history:
        st.session_state.messages = db_history
        st.info(f"📁 과거 대화 기록 {len(db_history)}건을 불러왔습니다.")
    else:
        # 기록이 없으면 시스템 프롬프트 새로 시작
        # (시스템 프롬프트는 화면에 안 보이므로 DB 저장 안 해도 됨, 하지만 여기선 흐름상 리스트에만 넣음)
        st.session_state.messages = [
            {"role": "system", "content": "너는 유능한 비서 자비스다. 한국어로 명확하게 대답해라."}
        ]

# 4. 대화 출력
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 5. 메인 로직
if prompt := st.chat_input("무엇을 도와드릴까요?"):
    # (1) 사용자 입력 화면 표시
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # (2) 사용자 입력 저장 (Session + DB) ⭐
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_message("user", prompt) # DB 저장

    # (3) 답변 처리
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # A. 명령어 처리
        is_command, result_msg = execute_command(prompt)
        if is_command:
            if result_msg.startswith("REPORT:"):
                # (보고서 로직 생략 - 필요시 이전 코드 참조)
                full_response = result_msg 
            else:
                full_response = result_msg

        # B. 이미지 분석
        elif uploaded_image is not None:
            temp_path = "temp_image.jpg"
            with open(temp_path, "wb") as f:
                f.write(uploaded_image.getbuffer())
            message_placeholder.markdown("👀 이미지 분석 중...")
            analysis_result = analyze_image(temp_path)
            full_response = f"**[이미지 분석]**\n{analysis_result}"

        # C. RAG + 대화
        else:
            try:
                retrieved_context = query_rag(prompt)
            except:
                retrieved_context = ""

            if retrieved_context:
                final_prompt = f"""
                [참고 문서] {retrieved_context}
                [질문] {prompt}
                위 문서를 바탕으로 답변해.
                """
            else:
                final_prompt = prompt

            stream = ollama.chat(model='llama3.1', messages=st.session_state.messages, stream=True)
            for chunk in stream:
                full_response += chunk['message']['content']
                message_placeholder.markdown(full_response + "▌")

        # (4) 최종 출력 및 저장 (Session + DB) ⭐
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        save_message("assistant", full_response) # DB 저장
        
        if voice_on and len(full_response) < 200:
            speak(full_response)