import streamlit as st
import json
import os

DATA_FILE = "tft_data.json"

def load_data():
    """
    저장된 tft_data.json 파일을 읽어옵니다.
    """
    try:
        if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
            return None, "MAINTENANCE"
        
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data, None
    except Exception:
        return None, "MAINTENANCE"

def show_maintenance_page():
    """
    시스템 점검 중임을 알리는 세련된 페이지를 렌더링합니다.
    """
    st.markdown("""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 70vh; text-align: center;">
            <h1 style="font-size: 80px; margin-bottom: 20px;">🛠️</h1>
            <h2 style="color: #444444; margin-bottom: 10px; font-weight: bold;">현재 시스템 점검 중입니다</h2>
            <p style="color: #666666; font-size: 18px; line-height: 1.6;">
                더 나은 서비스를 위해 데이터를 업데이트하고 있습니다.<br>
                잠시 후 다시 접속해 주세요.
            </p>
            <div style="margin-top: 30px; padding: 10px 20px; border: 1px solid #ccc; border-radius: 20px; color: #888; font-size: 13px;">
                TFT Meta Recommender Service
            </div>
        </div>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="TFT 덱 추천기", page_icon="♟️", layout="wide")

    # CSS 설정 (생략 방지 위해 그대로 유지)
    st.markdown("""
    <style>
        [data-testid="stHeaderActionElements"] { display: none; }
        .deck-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
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
        .champ-card { width: 70px; display: flex; flex-direction: column; align-items: center; vertical-align: top; margin-bottom: 5px; }
        .champ-img { width: 60px; height: 60px; object-fit: cover; border-radius: 6px; border: 2px solid #444; }
        .champ-img.mine { border-color: #ff4b4b; box-shadow: 0 0 8px rgba(255, 75, 75, 0.6); }
        .champ-name { font-size: 11px; text-align: center; margin-top: 4px; color: #aaaaaa; width: 100%; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .champ-name.mine { color: #ff4b4b; font-weight: bold; }
        .item-container { display: flex; gap: 2px; margin-top: 3px; justify-content: center; flex-wrap: wrap; min-height: 18px; }
        .item-img { width: 16px; height: 16px; border-radius: 2px; border: 1px solid #222; }
    </style>
    """, unsafe_allow_html=True)

    data, error = load_data()

    # 에러 발생 시 점검 페이지 표시
    if error == "MAINTENANCE":
        show_maintenance_page()
        return

    # 정상 화면 레이아웃
    col1, col2 = st.columns([8, 2])
    with col1:
        st.title("♟️ TFT 실시간 메타 덱 추천")
    with col2:
        st.write("")
        if st.button("🔄 화면 새로고침"):
            st.rerun()

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
