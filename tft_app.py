import streamlit as st
import json
import os

DATA_FILE = "/Users/iwmedia/개발/tft_data.json"

def load_data():
    """
    저장된 tft_data.json 파일을 읽어옵니다.
    """
    if not os.path.exists(DATA_FILE):
        return None, "데이터 파일이 없습니다. scraper.py를 먼저 실행해 주세요."
    
    if os.path.getsize(DATA_FILE) == 0:
        return None, "데이터 파일이 비어있습니다. scraper.py를 다시 실행해 주세요."

    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data, None
    except Exception as e:
        return None, f"데이터 로드 중 오류: {e}"

def main():
    st.set_page_config(page_title="TFT 덱 추천기", page_icon="♟️", layout="wide")

    # CSS 설정 (헤더 액션 숨김, 버튼 스타일, 아이템 표시 등)
    st.markdown("""
    <style>
        [data-testid="stHeaderActionElements"] { display: none; }
        
        .deck-header {
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 8px;
        }
        .guide-btn {
            display: flex; align-items: center; justify-content: center;
            width: 110px; height: 32px; background-color: transparent;
            border: 1px solid #555; border-radius: 4px; color: #ccc !important;
            text-decoration: none !important; font-size: 12px; transition: all 0.2s ease;
        }
        .guide-btn:hover {
            border-color: #ff4b4b; color: #ff4b4b !important;
            background-color: rgba(255, 75, 75, 0.1); transform: translateY(-1px);
        }
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

    col1, col2 = st.columns([8, 2])
    with col1:
        st.title("♟️ TFT 실시간 메타 덱 추천")
    with col2:
        st.write("")
        # JSON 파일 다시 읽기 버튼
        if st.button("🔄 화면 새로고침"):
            st.rerun()

    data, error = load_data()

    if error:
        st.error(error)
        st.warning("👉 서버 관리자: `python scraper.py`를 실행하여 데이터를 수집해 주세요.")
        return

    st.markdown(f"""
    보유하고 있는 챔피언을 선택하면, **lolchess.gg**의 실시간 메타 데이터를 분석하여 
    가장 적합한 덱을 추천해 드립니다. 
    *(마지막 업데이트: {data.get('updated_at', '알 수 없음')})*
    """)

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
                btn_html = f'<a href="{deck["link"]}" target="_blank" class="guide-btn">공략 더보기 🔗</a>' if deck.get('link') else ""
                
                header_html = f"""
                <div class="deck-header">
                    <h4 style="margin:0;">{rank_badge} Rank {rank} &nbsp;|&nbsp; <span style="color:{title_color}">{deck['name']}</span></h4>
                    {btn_html}
                </div>
                """
                st.markdown(header_html, unsafe_allow_html=True)
                st.markdown(f"✅&nbsp;&nbsp;**{match_count}명 일치** :gray[({', '.join(matched_names)})]")
                st.write("")
                
                champ_html = '<div class="champ-container">'
                for c in deck['champions']:
                    is_mine = "mine" if c['name'] in selected_champs else ""
                    
                    items_html = ""
                    if 'items' in c and c['items']:
                        items_html = '<div class="item-container">'
                        for item_url in c['items']:
                            items_html += f'<img src="{item_url}" class="item-img">'
                        items_html += '</div>'

                    champ_html += f"""<div class="champ-card"><img src="{c['image_url']}" class="champ-img {is_mine}"><div class="champ-name {is_mine}">{c['name']}</div>{items_html}</div>"""
                champ_html += '</div>'
                
                st.markdown(champ_html, unsafe_allow_html=True)

    else:
        st.info("챔피언을 선택하면 덱 추천이 시작됩니다.")

if __name__ == "__main__":
    main()
