# 🦾 Jarvis Pro (Local AI Agent)

**RTX 5080 로컬 환경**에서 구동되는 프라이빗 AI 비서 프로젝트입니다.  
대화 생성은 **Ollama의 로컬 LLM(Llama 3.1)**을 사용합니다. 문서 색인과 대화 기록은 로컬에 저장하지만, 인터넷 검색 기능은 외부 서비스에 검색어를 전송합니다. 로컬 추론과 외부 검색의 범위를 나누어 사용하세요.

단순한 챗봇을 넘어, 문서를 이해하고(RAG), 눈으로 보고(Vision), 스스로 인터넷을 검색하여 보고서를 작성하는(Agent) **All-in-One 로컬 에이전트**입니다.

## ✨ 주요 기능 (Key Features)

### 1. 📚 문서 검색과 답변 연결 (RAG)
- **ChromaDB**와 **LangChain**으로 문서를 검색할 수 있는 색인을 만듭니다.
- `ko-sroberta-multitask`로 문서 조각을 숫자 벡터로 바꾸고 관련 조각을 검색합니다.
- PDF 텍스트를 추출·분할해 검색용 색인을 생성합니다. 모델 가중치를 학습하거나 미세조정하는 과정이 아닙니다. 검색 결과가 답변의 정확성을 보장하지는 않습니다.

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

### 1. 필수 프로그램 설치
* [Python 3.10 이상](https://www.python.org/)
* [Ollama](https://ollama.com/) (Local LLM 구동기)

### 2. LLM 모델 다운로드
터미널(PowerShell)에서 아래 명령어로 모델을 다운로드합니다.
```bash
ollama pull llama3.1
```

### 3. 프로젝트 설치
```bash
# 저장소 클론
git clone https://github.com/Munsik-Kim/Local-LLM-jarvis.git
cd Local-LLM-jarvis

# 패키지 설치
pip install -r requirements.txt
```

### 4. 실행
```bash
streamlit run app.py
```

---

## 🔒 보안 및 프라이버시 (Privacy)
- **로컬 경로:** 대화 모델 실행은 Ollama, 문서 검색 색인은 ChromaDB, 대화 기록은 SQLite를 사용합니다. [문서 처리](rag_engine.py)와 [대화 저장](db_handler.py)을 참고하세요.
- **외부 통신:** [검색 도구](function_engine.py)의 `DDGS().text(...)`는 추출한 검색어를 DuckDuckGo로 보냅니다. Google·YouTube 검색도 브라우저에서 외부 URL을 엽니다. 검색을 요청한 문장에 민감한 내용이 들어가면 검색어에 포함될 수 있습니다.
- **최초 준비:** Ollama 모델과 Hugging Face 임베딩 모델을 준비하는 단계에는 다운로드가 필요할 수 있습니다.

따라서 “모든 데이터가 외부로 전송되지 않는다”는 보장은 하지 않습니다. 문서의 ‘학습’이라는 기존 UI 표현은 검색용 색인 생성을 뜻합니다. 이번 안내 수정은 코드를 읽어 확인한 범위이며 새 모델 실행이나 전체 네트워크 보안 감사를 수행한 것은 아닙니다.

---

## 👨‍💻 Developer
* **Name:** Munsik Kim
* **Role:** AI Application Developer
* **Environment:** Windows 11 / RTX 5080 / WSL2
