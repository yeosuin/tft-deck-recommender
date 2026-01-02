import streamlit as st
from curl_cffi import requests # 강력한 봇 탐지 우회
from bs4 import BeautifulSoup
import json
import time
import random

# -----------------------------------------------------------------------------
# 1. 백엔드 로직 (데이터 크롤링 및 처리)
# -----------------------------------------------------------------------------

@st.cache_data(ttl=3600)
def fetch_tft_data():
    # 1. 세션 생성 (쿠키 유지를 위해)
    session = requests.Session()

    # 2. 헤더 설정 (더 사람처럼 보이게)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://lolchess.gg/",
        "Upgrade-Insecure-Requests": "1"
    }

    try:
        # 3. 홈 화면 먼저 방문 (쿠키 획득용)
        # impersonate="chrome120" : 최신 브라우저 흉내
        session.get("https://lolchess.gg/", headers=headers, impersonate="chrome120")

        # 아주 짧은 대기 (사람인 척)
        time.sleep(random.uniform(0.5, 1.5))

        # 4. 실제 데이터 페이지 요청
        url = "https://lolchess.gg/meta?hl=ko-KR"
        response = session.get(
            url,
            headers=headers,
            impersonate="chrome120"
        )

        # 403 오류 체크
        if response.status_code == 403:
            return None, "서버에서 봇으로 인식하여 차단했습니다 (403 Error). 잠시 후 다시 시도하거나 로컬 환경에서 실행해주세요."

        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find('script', id='__NEXT_DATA__')

        if not script_tag:
            return None, "데이터 스크립트를 찾을 수 없습니다."

        data = json.loads(script_tag.string)
        queries = data.get('props', {}).get('pageProps', {}).get('dehydratedState', {}).get('queries', [])

        champion_map = {}
        item_map = {}
        deck_list = []

        for q in queries:
            query_key = q.get('queryKey', [])

            # 아이템 정보 매핑
            if 'itemRefs' in query_key:
                items = q.get('state', {}).get('data', {}).get('items', [])
                for item in items:
                    img_url = item.get('imageUrl')
                    if img_url and isinstance(img_url, str):
                        if img_url.startswith('//'):
                            img_url = 'https:' + img_url
                        item_map[item['key']] = img_url

            # 챔피언 정보 매핑
            if 'championRefs' in query_key:
                champs = q.get('state', {}).get('data', {}).get('champions', [])
                for c in champs:
                    img_url = c.get('imageUrl')
                    if img_url and isinstance(img_url, str):
                        if img_url.startswith('//'):
                            img_url = 'https:' + img_url
                    else:
                        img_url = ''

                    champion_map[c['key']] = {
                        'name': c['name'],
                        'image_url': img_url
                    }

            # 덱 리스트
            if 'getGuideDecks' in query_key:
                deck_list = q.get('state', {}).get('data', {}).get('guideDecks', [])

        if not deck_list:
            return None, "덱 리스트를 찾을 수 없습니다."

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

                    # 해당 챔피언의 추천 아이템 이미지 URL 추출
                    item_keys = slot.get('items', [])
                    champ_info['items'] = [item_map[k] for k in item_keys if k in item_map]

                    champions.append(champ_info)
                    all_champions_set.add(champ_info['name'])

            if champions:
                # 덱 상세 링크 생성
                tb_key = deck.get('teamBuilderKey')
                deck_link = f"https://lolchess.gg/builder?deck={tb_key}" if tb_key else None

                final_decks.append({
                    'name': deck_name,
                    'champions': champions,
                    'champ_names': [c['name'] for c in champions],
                    'link': deck_link
                })

        return {
            'decks': final_decks,
            'all_champions': sorted(list(all_champions_set))
        }, None

    except Exception as e:
        return None, f"크롤링 오류: {str(e)}"

# -----------------------------------------------------------------------------
# 2. 프론트엔드 UI (Streamlit)
# -----------------------------------------------------------------------------

def main():
    st.set_page_config(page_title="TFT 덱 추천기", page_icon="♟️", layout="wide")

    # CSS 설정 (헤더 액션 숨김, 버튼 스타일, 아이템 표시 등)
    st.markdown("""
    <style>
        /* 우측 상단 기본 메뉴 숨김 */
        [data-testid="stHeaderActionElements"] {
            display: none;
        }
        
        /* 덱 헤더 레이아웃 (타이틀 + 버튼) */
        .deck-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px; /* 아래 일치 정보와의 간격 */
        }
        
        /* 공략 더보기 버튼 (a 태그 직접 스타일링) */
        .guide-btn {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 110px; /* 너비 고정 */
            height: 32px; /* 높이 고정 */
            background-color: transparent;
            border: 1px solid #555;
            border-radius: 4px;
            color: #ccc !important;
            text-decoration: none !important;
            font-size: 12px;
            transition: all 0.2s ease;
            white-space: nowrap;
        }
        .guide-btn:hover {
            border-color: #ff4b4b;
            color: #ff4b4b !important;
            background-color: rgba(255, 75, 75, 0.1);
            transform: translateY(-1px);
        }

        /* 챔피언 카드 스타일 */
        .champ-container { display: flex; flex-wrap: wrap; gap: 12px; padding-bottom: 20px; }
        .champ-card { 
            width: 70px; display: flex; flex-direction: column; 
            align-items: center; vertical-align: top; margin-bottom: 5px;
        }
        .champ-img { 
            width: 60px; height: 60px; object-fit: cover; 
            border-radius: 6px; border: 2px solid #444; 
        }
        .champ-img.mine { border-color: #ff4b4b; box-shadow: 0 0 8px rgba(255, 75, 75, 0.6); }
        .champ-name { 
            font-size: 11px; text-align: center; margin-top: 4px; 
            color: #aaaaaa; width: 100%; white-space: nowrap; 
            overflow: hidden; text-overflow: ellipsis;
        }
        .champ-name.mine { color: #ff4b4b; font-weight: bold; }
        .item-container { display: flex; gap: 2px; margin-top: 3px; justify-content: center; flex-wrap: wrap; min-height: 18px; }
        .item-img { width: 16px; height: 16px; border-radius: 2px; border: 1px solid #222; }
    </style>
    """, unsafe_allow_html=True)

    # 상단 레이아웃: 타이틀과 새로고침 버튼
    col1, col2 = st.columns([8, 2])
    with col1:
        st.title("♟️ TFT 실시간 메타 덱 추천")
    with col2:
        st.write("") # 줄맞춤용 여백
        if st.button("🔄 데이터 새로고침"):
            fetch_tft_data.clear()
            st.rerun()

    st.markdown("""
    보유하고 있는 챔피언을 선택하면, **lolchess.gg**의 실시간 메타 데이터를 분석하여 
    가장 적합한 덱을 추천해 드립니다.
    """)

    # 데이터 로드
    with st.spinner("최신 메타 데이터를 불러오는 중입니다..."):
        data, error = fetch_tft_data()

    if error:
        st.error(error)
        return

    all_decks = data['decks']
    all_champions = data['all_champions']

    st.subheader("나의 챔피언 선택")
    selected_champs = st.multiselect(
        "현재 보유 중이거나 핵심으로 사용할 챔피언을 선택하세요:",
        options=all_champions,
        placeholder="챔피언 검색 또는 선택..."
    )

    if selected_champs:
        recommendations = []
        for deck in all_decks:
            matched = set(selected_champs).intersection(set(deck['champ_names']))
            count = len(matched)
            if count > 0:
                recommendations.append({
                    'deck': deck,
                    'match_count': count,
                    'matched_names': matched
                })

        recommendations.sort(key=lambda x: x['match_count'], reverse=True)

        st.divider()
        st.subheader(f"🔍 추천 결과 ({len(recommendations)}개)")

        for rank, rec in enumerate(recommendations, 1):
            deck = rec['deck']
            match_count = rec['match_count']
            matched_names = rec['matched_names']

            if rank == 1:
                rank_badge, title_color = "🥇", "red"
            elif rank == 2:
                rank_badge, title_color = "🥈", "orange"
            elif rank == 3:
                rank_badge, title_color = "🥉", "green"
            else:
                rank_badge, title_color = "🏅", "blue"

            with st.container(border=True):
                # 헤더 (타이틀 + 버튼) HTML 생성
                button_html = ""
                if deck.get('link'):
                    button_html = f'<a href="{deck["link"]}" target="_blank" class="guide-btn">공략 더보기 🔗</a>'

                header_html = f"""
                <div class="deck-header">
                    <h4 style="margin: 0; padding: 0;">{rank_badge} Rank {rank} &nbsp;|&nbsp; <span style="color:{title_color}">{deck['name']}</span></h4>
                    {button_html}
                </div>
                """
                st.markdown(header_html, unsafe_allow_html=True)

                # 일치 정보는 타이틀 아래에 배치
                st.markdown(f"✅&nbsp;&nbsp;**{match_count}명 일치** :gray[({', '.join(matched_names)})]")

                st.write("") # 간격

                # HTML로 챔피언 카드 나열 (CSS Flexbox 적용)
                champ_html = '<div class="champ-container">'
                for champ in deck['champions']:
                    is_mine = "mine" if champ['name'] in selected_champs else ""

                    # 아이템 HTML 생성
                    items_html = ""
                    if 'items' in champ and champ['items']:
                        items_html = '<div class="item-container">'
                        for item_url in champ['items']:
                            items_html += f'<img src="{item_url}" class="item-img">'
                        items_html += '</div>'

                    champ_html += f"""<div class="champ-card"><img src="{champ['image_url']}" class="champ-img {is_mine}"><div class="champ-name {is_mine}">{champ['name']}</div>{items_html}</div>"""
                champ_html += '</div>'

                st.markdown(champ_html, unsafe_allow_html=True)

    else:
        st.info("챔피언을 선택하면 덱 추천이 시작됩니다.")

if __name__ == "__main__":
    main()