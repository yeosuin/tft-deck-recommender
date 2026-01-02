import json
import time
from curl_cffi import requests
from bs4 import BeautifulSoup

DATA_FILE = "tft_data.json"

def fetch_and_save_data():
    """
    lolchess.gg에서 데이터를 크롤링하여 tft_data.json 파일로 저장합니다.
    """
    print(f"[Scraper] 데이터 수집 시작... ({time.strftime('%Y-%m-%d %H:%M:%S')})")
    
    url = "https://lolchess.gg/meta?hl=ko-KR"
    headers = {
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://lolchess.gg/"
    }

    try:
        # curl_cffi를 사용하여 브라우저처럼 요청
        response = requests.get(url, headers=headers, impersonate="chrome110")
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find('script', id='__NEXT_DATA__')
        
        if not script_tag:
            print("[Scraper] Error: __NEXT_DATA__ 태그를 찾을 수 없습니다.")
            return

        data = json.loads(script_tag.string)
        queries = data.get('props', {}).get('pageProps', {}).get('dehydratedState', {}).get('queries', [])

        champion_map = {}
        item_map = {}
        deck_list = []

        for q in queries:
            query_key = q.get('queryKey', [])
            
            # 아이템 정보
            if 'itemRefs' in query_key:
                items = q.get('state', {}).get('data', {}).get('items', [])
                for item in items:
                    img_url = item.get('imageUrl')
                    if img_url and isinstance(img_url, str):
                        if img_url.startswith('//'):
                            img_url = 'https:' + img_url
                        item_map[item['key']] = img_url

            # 챔피언 정보
            if 'championRefs' in query_key:
                champs = q.get('state', {}).get('data', {}).get('champions', [])
                for c in champs:
                    img_url = c.get('imageUrl')
                    if img_url and isinstance(img_url, str):
                        if img_url.startswith('//'):
                            img_url = 'https:' + img_url
                    else:
                        img_url = ""
                    
                    champion_map[c['key']] = {
                        'name': c['name'],
                        'image_url': img_url
                    }
            
            # 덱 리스트
            if 'getGuideDecks' in query_key:
                deck_list = q.get('state', {}).get('data', {}).get('guideDecks', [])

        if not deck_list:
            print("[Scraper] Error: 덱 리스트가 비어 있습니다.")
            return

        final_decks = []
        all_champions_set = set()

        for deck in deck_list:
            deck_name = deck.get('name', 'Unknown Deck')
            champions = []
            
            slots = deck.get('data', {}).get('slots', [])
            for slot in slots:
                champ_key = slot.get('champion')
                if champ_key in champion_map:
                    champ_info = champion_map[champ_key].copy()
                    
                    # 아이템 처리
                    item_keys = slot.get('items', [])
                    champ_info['items'] = [item_map[k] for k in item_keys if k in item_map]
                    
                    champions.append(champ_info)
                    all_champions_set.add(champ_info['name'])
            
            if champions:
                # 덱 상세 링크
                tb_key = deck.get('teamBuilderKey')
                deck_link = f"https://lolchess.gg/builder?deck={tb_key}" if tb_key else None

                final_decks.append({
                    'name': deck_name,
                    'champions': champions,
                    'champ_names': [c['name'] for c in champions],
                    'link': deck_link
                })

        # 저장할 데이터 구조
        save_data = {
            'updated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'decks': final_decks,
            'all_champions': sorted(list(all_champions_set))
        }

        # JSON 파일로 저장
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        
        print(f"[Scraper] 성공! {len(final_decks)}개의 덱 정보를 '{DATA_FILE}'에 저장했습니다.")

    except Exception as e:
        print(f"[Scraper] 크롤링 중 오류 발생: {e}")

if __name__ == "__main__":
    fetch_and_save_data()
