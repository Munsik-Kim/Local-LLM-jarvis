# 🦾 Jarvis Pro (Local AI Agent)

**RTX 5080 로컬 환경**에서 구동되는 프라이빗 AI 비서 프로젝트입니다.  
클라우드 API(OpenAI, Gemini 등)에 의존하지 않고, 오직 **로컬 LLM(Llama 3.1)**만을 사용하여 **데이터 보안**과 **비용 절감**을 동시에 실현했습니다.

단순한 챗봇을 넘어, 문서를 이해하고(RAG), 눈으로 보고(Vision), 스스로 인터넷을 검색하여 보고서를 작성하는(Agent) **All-in-One 로컬 에이전트**입니다.

## ✨ 주요 기능 (Key Features)

### 1. 📚 전문가급 문서 분석 (Advanced RAG)
- **벡터 데이터베이스(ChromaDB)**와 **LangChain**을 활용한 고성능 RAG 시스템 구축.
- `ko-sroberta-multitask` 임베딩 모델을 사용하여 한국어 문서 이해도 극대화.
- 수백 페이지의 PDF 문서를 학습하고, 정확한 근거를 찾아 답변.

### 2. 🧠 장기 기억 (Long-term Memory)
- **SQLite** 기반의 영구 기억 저장소 구현.
- 프로그램을 종료해도 사용자와의 과거 대화 내용을 기억하고 문맥을 파악.

### 3. 🛠️ 자율 에이전트 도구 (Function Calling)
- **인터넷 리서치:** DuckDuckGo 검색을 통해 최신 정보를 수집하고 요약.
- **보고서 작성:** 수집한 정보를 바탕으로 체계적인 보고서(.txt) 자동 생성 및 파일 저장.
- **시스템 제어:** 메모장, 계산기 등 윈도우 프로그램 제어.

### 4. 👁️ 시각 지능 (Vision) & 🎙️ 음성 (TTS)
- 이미지를 업로드하면 내용을 분석하고 설명.
- 답변 내용을 음성으로 읽어주는 TTS(Text-to-Speech) 기능 탑재.

### 5. 🖥️ 직관적인 GUI
- **Streamlit**을 활용하여 채팅 앱 형태의 깔끔한 웹 인터페이스 제공.
- 사이드바를 통한 파일 업로드, 설정 제어, 디버깅 모드 지원.

---

## 🛠️ 기술 스택 (Tech Stack)

| 구분 | 기술 / 라이브러리 |
| --- | --- |
| **Core** | Python 3.10+ |
| **LLM Engine** | Ollama (Llama 3.1 8B), LLaVA (Vision) |
| **Web Framework** | Streamlit |
| **RAG Framework** | LangChain, ChromaDB, HuggingFace Embeddings |
| **Search Tool** | DuckDuckGo Search |
| **Document Parsing** | pdfplumber (PDF Text Extraction) |
| **Database** | SQLite3 (Conversation History) |

---

## 📂 프로젝트 구조 (Project Structure)

```bash
📦 Jarvis_Project
 ┣ 📜 app.py              # 메인 실행 파일 (Streamlit GUI & Logic)
 ┣ 📜 rag_engine.py       # RAG 엔진 (문서 청킹, 임베딩, 벡터 DB 관리)
 ┣ 📜 function_engine.py  # 도구 모음 (검색, 파일저장, 앱실행)
 ┣ 📜 vision_engine.py    # 이미지 분석 모듈
 ┣ 📜 db_handler.py       # 대화 기억(SQLite) 관리 모듈
 ┣ 📜 tts_engine.py       # 음성 합성 모듈
 ┗ 📜 requirements.txt    # 의존성 패키지 목록
```
## 🚀 시작하기 (Getting Started)
1. 필수 프로그램 설치
Python 3.10 이상

Ollama (Local LLM 구동기)

2. LLM 모델 다운로드
터미널(PowerShell)에서 아래 명령어로 모델을 다운로드합니다.

Bash

ollama pull llama3.1
3. 프로젝트 설치
Bash

# 저장소 클론 (본인의 GitHub 주소로 변경 필요)
git clone [https://github.com/Munsik-Kim/Local-LLM-jarvis.git](https://github.com/Munsik-Kim/Local-LLM-jarvis.git)

# 패키지 설치
pip install -r requirements.txt
4. 실행
Bash

streamlit run app.py
🔒 보안 및 프라이버시 (Privacy)
이 프로젝트의 모든 데이터 처리는 **사용자의 컴퓨터 내부(Local)**에서만 이루어집니다.

학습시킨 문서 파일

대화 내용 (DB)

카메라/이미지 데이터 위 정보는 외부 서버로 전송되지 않으므로, 회사 기밀 문서나 개인 자료를 안전하게 다룰 수 있습니다.

👨‍💻 Developer
Name: Munsik Kim

Role: AI Application Developer

Environment: Windows 11 / RTX 5080 / WSL2
