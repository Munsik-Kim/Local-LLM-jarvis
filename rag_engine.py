# rag_engine.py - 최신 LangChain 버전 대응 완료
import os
import pdfplumber

# [수정됨 1] 텍스트 스플리터 경로 변경
# 기존: from langchain.text_splitter import RecursiveCharacterTextSplitter (삭제)
# 최신: langchain_text_splitters 패키지 사용
from langchain_text_splitters import RecursiveCharacterTextSplitter

# [수정됨 2] 임베딩 모델 경로 (그대로 유지)
from langchain_huggingface import HuggingFaceEmbeddings

# [수정됨 3] 벡터 DB 경로 (그대로 유지)
from langchain_community.vectorstores import Chroma

# [수정됨 4] Document 객체 경로 변경
from langchain_core.documents import Document 

# 1. 벡터 DB 저장 경로
PERSIST_DIRECTORY = os.path.join(os.getcwd(), "db_storage")

# 2. 임베딩 모델 설정
embedding_model = HuggingFaceEmbeddings(
    model_name="jhgan/ko-sroberta-multitask"
)

def process_document(file_path):
    """
    문서를 읽어서 -> 쪼개고 -> 벡터 DB에 저장하는 함수
    """
    print(f"🔄 문서 처리 시작: {file_path}")
    
    # (1) PDF 텍스트 추출
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    
    if not text:
        return "문서에서 텍스트를 추출하지 못했습니다."

    # (2) 텍스트 쪼개기 (Chunking)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    
    # LangChain용 문서 객체로 변환
    docs = [Document(page_content=x) for x in text_splitter.split_text(text)]
    
    # (3) 벡터 DB 생성 및 저장
    vector_db = Chroma.from_documents(
        documents=docs,
        embedding=embedding_model,
        persist_directory=PERSIST_DIRECTORY,
        collection_name="jarvis_docs"
    )
    
    print(f"✅ 문서 저장 완료! 총 {len(docs)}개의 조각으로 나뉘어 저장됨.")
    return f"문서 학습 완료! 총 {len(docs)}개의 조각으로 데이터베이스에 저장되었습니다."

def query_rag(question):
    """
    질문을 받아서 -> 관련된 문서 조각을 찾아서 -> 리턴하는 함수
    """
    # 저장된 DB 불러오기
    vector_db = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embedding_model,
        collection_name="jarvis_docs"
    )
    
    # (1) 질문과 가장 유사한 조각 3개 검색 (k=3)
    docs = vector_db.similarity_search(question, k=3)
    
    # (2) 찾은 조각들의 내용을 합침
    context = "\n\n".join([doc.page_content for doc in docs])
    
    return context