# vision_engine.py - 2단 엔진 (Vision -> Translation)
import ollama

def analyze_image(image_path):
    print("👀 자비스(Vision): 이미지를 보고 있습니다... (영어 분석 중)")
    
    try:
        # 1. 시각 모델 (Llava or Llama3.2-vision)
        vision_response = ollama.chat(
            model='llava', # 혹은 'llama3.2-vision' 사용 중인 모델명 유지
            messages=[{
                'role': 'user',
                'content': "Describe this image in detail. Focus on appearance, colors, and background.",
                'images': [image_path]
            }]
        )
        english_description = vision_response['message']['content']
        
        print("🧠 자비스(Llama): 한국어로 번역 중입니다...")

        # 2. 번역 모델 (Llama 3.1) - 한자 방지 설정 추가 ⭐
        translate_response = ollama.chat(
            model='llama3.1',
            messages=[{
                'role': 'system',
                # 시스템 프롬프트에 '한자 사용 금지'를 강력하게 박아넣습니다.
                'content': """
                너는 전문 한영 번역가다. 
                주어진 영어 텍스트를 한국어로 번역하되, 다음 규칙을 반드시 지켜라:
                1. 절대로 한자(Chinese Characters)를 사용하지 마라.
                2. 오직 '한글'로만 작성해라.
                3. 번역투가 아닌 자연스러운 구어체로 설명해라.
                """
            },
            {
                'role': 'user',
                'content': f"다음 텍스트를 한국어로 번역해:\n{english_description}"
            }],
            # ⭐ 꿀팁: temperature를 0.1로 낮추면 AI가 '모험'을 하지 않고 시키는 대로만 합니다.
            options={'temperature': 0.1} 
        )
        
        return translate_response['message']['content']
        
    except Exception as e:
        return f"분석 중 오류 발생: {str(e)}"

if __name__ == '__main__':
    print("이 파일은 모듈용입니다.")