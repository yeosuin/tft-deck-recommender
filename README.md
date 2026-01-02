# ♟️ TFT Meta Deck Recommender (TFT 덱 추천기)

사용자가 보유한 챔피언을 기반으로 **lolchess.gg**의 실시간 메타 데이터를 분석하여 최적의 TFT(전략적 팀 전투) 덱을 추천해 주는 웹 애플리케이션입니다.

## 🚀 Features (주요 기능)

*   **실시간 데이터 크롤링**: `lolchess.gg/meta`의 최신 덱 정보를 실시간으로 가져옵니다.
*   **스마트 추천 알고리즘**: 사용자가 선택한 챔피언들과 가장 많이 일치하는 상위 티어 덱을 우선적으로 추천합니다.
*   **상세 정보 제공**:
    *   덱 구성 챔피언 및 추천 아이템 이미지 시각화
    *   일치하는 챔피언 수 및 명단 표시
    *   '공략 더보기'를 통한 상세 빌더 페이지 연결
*   **반응형 UI**: PC와 모바일 환경 모두에 최적화된 깔끔한 카드형 디자인 (Streamlit 기반).

## 🛠️ Tech Stack (기술 스택)

*   **Language**: Python 3.9+
*   **Web Framework**: [Streamlit](https://streamlit.io/)
*   **Crawling**: `requests`, `BeautifulSoup4`
*   **Deployment**: Streamlit Cloud (Recommended)

## 🤖 Vibe Coding & AI

이 프로젝트는 **Vibe Coding (바이브 코딩)** 방법론을 통해 개발되었습니다.
복잡한 구현 세부 사항보다는 **"무엇을 만들고 싶은가"**에 대한 자연어 의도(Intention)를 AI에게 전달하고, AI가 작성한 코드를 검토 및 조율하며 완성했습니다.

*   **Used AI Model**: Google **Gemini 2.0 Pro Experimental** & **Gemini 2.5 Flash**
    *   (초기 설계 및 복잡한 로직 구현: 2.0 Pro / 최적화 및 디버깅: 2.5 Flash)
*   **Role of AI**: 
    *   전체적인 코드 아키텍처 설계 및 구현
    *   `lolchess.gg` HTML/JSON 데이터 구조 역공학 및 파싱 로직 작성
    *   Streamlit UI/UX 디자인 및 CSS 커스터마이징
    *   오류 디버깅 및 코드 최적화

## 📦 Installation & Run

1. **Clone Repository**
   ```bash
   git clone https://github.com/yeosuin/tft-deck-recommender.git
   cd tft-deck-recommender
   ```

2. **Install Requirements**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run App**
   ```bash
   streamlit run tft_app.py
   ```

## 📝 License

This project is open-source and available under the MIT License.
*Data source: [lolchess.gg](https://lolchess.gg)*
