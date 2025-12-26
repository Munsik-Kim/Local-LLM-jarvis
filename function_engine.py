# function_engine.py
import os
import subprocess
from duckduckgo_search import DDGS

def execute_command(text):
    cmd = text.strip()
    cmd_lower = cmd.lower()
    
    # ---------------------------------------------------------
    # 1. [신규] 인터넷 조사 & 보고서 기능
    # ---------------------------------------------------------
    if "조사" in cmd and ("해줘" in cmd or "알려줘" in cmd):
        keyword = cmd.replace("조사", "").replace("해서", "").replace("해줘", "").replace("알려줘", "").replace("대해", "").strip()
        
        if not keyword:
            return True, "무엇을 조사할까요?"
            
        print(f"🔎 시스템: 인터넷에서 '{keyword}' 정보를 수집 중입니다...")
        
        try:
            results = DDGS().text(keyword, max_results=3)
            if not results:
                return True, "검색 결과가 없습니다."
                
            search_summary = ""
            for res in results:
                search_summary += f"제목: {res['title']}\n내용: {res['body']}\n링크: {res['href']}\n\n"
            
            return True, f"REPORT:{keyword}\n{search_summary}"
            
        except Exception as e:
            return True, f"검색 중 오류가 발생했습니다: {str(e)}"

    # ---------------------------------------------------------
    # 2. 유튜브 검색
    # ---------------------------------------------------------
    youtube_keywords = ["유튜브", "유투브", "youtube", "너튜브"]
    action_keywords = ["검색", "틀어", "보여", "찾아"]

    if any(k in cmd_lower for k in youtube_keywords) and any(k in cmd_lower for k in action_keywords):
        search_query = cmd
        remove_list = youtube_keywords + action_keywords + ["에서", "해줘", "제발", "좀"]
        for word in remove_list:
            search_query = search_query.replace(word, "")
        search_query = search_query.strip()
        
        if not search_query:
            return True, "검색어를 찾지 못했습니다."

        url = f"https://www.youtube.com/results?search_query={search_query}"
        try: os.startfile(url)
        except: os.system(f'start "" "{url}"')
            
        return True, f"유튜브에서 '{search_query}' 검색 결과를 띄웠습니다."

    # ---------------------------------------------------------
    # 3. 구글 검색
    # ---------------------------------------------------------
    elif "구글" in cmd and ("검색" in cmd or "찾아" in cmd):
        search_query = cmd.replace("구글", "").replace("에서", "").replace("검색해줘", "").replace("찾아줘", "").replace("검색", "").strip()
        url = f"https://www.google.com/search?q={search_query}"
        try: os.startfile(url)
        except: os.system(f'start "" "{url}"')
        return True, f"구글에서 {search_query} 내용을 검색했습니다."

    # ---------------------------------------------------------
    # 4. 윈도우 프로그램 실행
    # ---------------------------------------------------------
    elif "메모장" in cmd and ("켜" in cmd or "실행" in cmd):
        subprocess.Popen("notepad.exe")
        return True, "메모장을 실행했습니다."

    elif "계산기" in cmd and ("켜" in cmd or "실행" in cmd):
        subprocess.Popen("calc.exe")
        return True, "계산기를 실행했습니다."

    elif ("탐색기" in cmd or "내 컴퓨터" in cmd) and ("켜" in cmd or "열어" in cmd):
        subprocess.Popen("explorer.exe")
        return True, "파일 탐색기를 열었습니다."

    return False, ""

# ⭐ 이 부분이 없어서 에러가 났던 겁니다! 꼭 포함되어야 합니다. ⭐
def save_to_file(title, content):
    """
    LLM이 요약한 내용을 파일로 저장하는 함수
    """
    # 파일명에 특수문자가 있으면 에러가 날 수 있으니 간단히 처리
    safe_title = title.replace(" ", "_").replace("/", "_")
    filename = f"{safe_title}_보고서.txt"
    
    # 현재 폴더에 저장
    filepath = os.path.join(os.getcwd(), filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"[{title} 조사 보고서]\n\n")
        f.write(content)
        
    return filepath