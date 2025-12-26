# tts_engine.py - 한국어 목소리 자동 감지 버전
import pyttsx3
import threading

# TTS 엔진 초기화
engine = pyttsx3.init()

# 1. 설치된 목소리 리스트를 가져옵니다.
voices = engine.getProperty('voices')

# 2. 한국어 목소리(Microsoft Heami 등) 찾기
korean_voice_found = False
for voice in voices:
    # 목소리 이름에 'Korea' 또는 'Heami'가 들어간 걸 찾습니다.
    if 'Korea' in voice.name or 'Heami' in voice.name:
        engine.setProperty('voice', voice.id)
        korean_voice_found = True
        print(f"🎤 한국어 음성 설정 완료: {voice.name}")
        break

# 한국어가 없으면 경고 메시지 출력
if not korean_voice_found:
    print("⚠️ 한국어 음성을 찾지 못했습니다. 기본 음성으로 출력합니다.")
    print("   (윈도우 설정 -> 시간 및 언어 -> 음성 에서 '한국어' 팩을 설치해주세요.)")

# 말하기 속도 조절 (기본 200은 너무 빠를 수 있어서 150 정도로 추천)
engine.setProperty('rate', 200) 

def speak(text):
    """
    주어진 텍스트를 음성으로 읽어주는 함수 (스레드 처리)
    """
    def _run_tts():
        try:
            if engine._inLoop:
                engine.endLoop()
            engine.say(text)
            engine.runAndWait()
        except Exception:
            pass

    threading.Thread(target=_run_tts, daemon=True).start()

# 테스트
if __name__ == '__main__':
    speak("안녕하세요. 자비스의 목소리가 바뀌었나요?")
    input("테스트 종료하려면 엔터...")