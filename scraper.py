from curl_cffi import requests
from bs4 import BeautifulSoup
import json

def save_tft_data():
    print("데이터 수집 시작...")
    url = "https://lolchess.gg/meta?hl=ko-KR"

    try:
        # 내 컴퓨터에서는 봇 차단 없이 잘 됩니다
        response = requests.get(
            url,
            impersonate="chrome120",
            headers={
                "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
                "Referer": "https://lolchess.gg/"
            }
        )

        if response.status_code != 200:
            print(f"오류 발생: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find('script', id='__NEXT_DATA__')

        if not script_tag:
            print("스크립트 태그를 못 찾았습니다.")
            return

        # 데이터를 JSON 파일로 저장
        data = json.loads(script_tag.string)

        with open("tft_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print("✅ 성공! 'tft_data.json' 파일이 생성되었습니다.")

    except Exception as e:
        print(f"에러 발생: {e}")

if __name__ == "__main__":
    save_tft_data()