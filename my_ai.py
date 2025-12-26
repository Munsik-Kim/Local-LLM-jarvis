import ollama

# 1. 자비스의 자아(Persona) 설정 - 여기가 핵심입니다!
system_instruction = """
너는 나의 유능한 개인 비서 '자비스(Jarvis)'다.
너는 클라우드가 아니라, 내 로컬 컴퓨터의 강력한 RTX 5080 GPU 위에서 실행되고 있다.
항상 예의 바르고, 명확하고, 한국어로 대답해라.
"""

user_input = "안녕! 너는 누구니? 그리고 넌 지금 어디에서 실행되고 있어?"

print("--------------------------------------------------")
print(f"사용자: {user_input}")
print("--------------------------------------------------")
print("Jarvis(생각중...): ", end="", flush=True)

# 2. Ollama에게 '설정(System)'과 '질문(User)'을 같이 전달
stream = ollama.chat(
    model='llama3.1',
    messages=[
        {'role': 'system', 'content': system_instruction}, # 최면 걸기
        {'role': 'user', 'content': user_input}
    ],
    stream=True,
)

# 3. 답변 출력하기
for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)

print("\n--------------------------------------------------")