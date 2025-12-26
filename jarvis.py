import ollama
import sys
import os
from tts_engine import speak 
from vision_engine import analyze_image
from function_engine import execute_command, save_to_file # save_to_file 추가됨

messages = [
    {
        'role': 'system', 
        'content': """
        너는 유능한 비서 '자비스'다.
        1. 한국어로 명확하게 대답해라.
        2. 한자는 쓰지 마라.
        3. 만약 사용자가 제공한 '검색 결과'가 있다면, 그것을 바탕으로 아주 상세하게 요약해라.
        """
    }
]

print("==================================================")
print("🦾 자비스(Jarvis) 에이전트 모드 가동")
print("==================================================")
speak("업그레이드 완료. 인터넷 조사 및 보고서 작성이 가능합니다.")

while True:
    try:
        user_input = input("\n👤 사용자: ")
        clean_input = user_input.strip()
        
        if clean_input.lower() in ["exit", "종료"]:
            break
        if not clean_input:
            continue

        # 1. 명령어 실행 확인
        is_command, result_msg = execute_command(clean_input)
        
        if is_command:
            # ------------------------------------------------------------
            # ⭐ 핵심 로직: 검색 결과가 돌아왔을 때 (REPORT: 표식 확인)
            # ------------------------------------------------------------
            if result_msg.startswith("REPORT:"):
                # "REPORT:키워드" 와 "내용"을 분리
                lines = result_msg.split("\n", 1)
                keyword = lines[0].replace("REPORT:", "")
                search_data = lines[1]
                
                print(f"🧠 자비스: 검색된 정보를 읽고 보고서를 작성 중입니다... (키워드: {keyword})")
                speak(f"{keyword}에 대한 정보를 찾았습니다. 내용을 요약해 드릴게요.")
                
                # LLM에게 검색 내용 던져주고 요약시키기
                prompt = f"""
                다음은 인터넷에서 검색된 '{keyword}' 관련 정보다.
                이 내용을 바탕으로 체계적인 보고서를 작성해줘.
                서론, 본론, 결론으로 나누고 핵심 내용을 글머리 기호로 정리해.
                
                [검색 데이터]
                {search_data}
                """
                
                # LLM 생성 시작
                stream = ollama.chat(model='llama3.1', messages=[{'role': 'user', 'content': prompt}], stream=True)
                
                full_report = ""
                print(f"\n📄 [{keyword} 보고서 생성 중...]\n")
                for chunk in stream:
                    part = chunk['message']['content']
                    print(part, end='', flush=True)
                    full_report += part
                print("\n")
                
                # ⭐ 파일로 저장하기
                saved_path = save_to_file(keyword, full_report)
                print(f"💾 보고서 저장 완료: {saved_path}")
                speak("보고서 작성을 완료하고 파일로 저장했습니다.")
                
                # 기억에 추가
                messages.append({'role': 'assistant', 'content': f"{keyword} 조사 보고서를 작성했습니다."})
                continue

            # 일반 명령어(메모장, 유튜브 등)인 경우
            else:
                print(f"🤖 자비스: {result_msg}")
                speak(result_msg)
                continue

        # 2. 이미지 처리
        if os.path.isfile(clean_input):
            # ... (기존 이미지 처리 코드) ...
            pass 
            
        # 3. 일반 대화
        messages.append({'role': 'user', 'content': clean_input})
        # ... (기존 대화 코드) ...
        # 여기서는 생략했지만 기존 코드 그대로 유지하면 됩니다.
        
        # (편의를 위해 일반 대화 부분 코드를 간략히 적습니다. 실제 파일엔 기존 내용을 유지하세요)
        print("🤖 자비스: ", end="")
        stream = ollama.chat(model='llama3.1', messages=messages, stream=True)
        full_res = ""
        for chunk in stream:
            part = chunk['message']['content']
            print(part, end="", flush=True)
            full_res += part
        print()
        speak(full_res)
        messages.append({'role': 'assistant', 'content': full_res})

    except KeyboardInterrupt:
        break