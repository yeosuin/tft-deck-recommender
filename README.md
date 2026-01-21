# ♟️ TFT Meta Deck Recommender (TFT 덱 추천기)

사용자가 보유한 챔피언을 기반으로 **lolchess.gg**의 실시간 메타 데이터를 분석하여 최적의 TFT(전략적 팀 전투) 덱을 추천해 주는 웹 애플리케이션입니다.

👉 **Demo**: https://tft-deck-recommender.streamlit.app/


## 🚀 주요 특징 (Key Features)

*   **하이브리드 아키텍처 (Hybrid Architecture)**:
    *   **Data Scraper (`scraper.py`)**: 서버에서 주기적으로 실행되어 최신 메타 데이터를 수집하고 JSON 파일로 저장합니다. 봇 차단을 방지하고 서버 부하를 최소화합니다.
    *   **Web Viewer (`tft_app.py`)**: 저장된 JSON 데이터를 즉시 로드하여 사용자에게 매우 빠른 응답 속도로 덱을 추천합니다.
*   **스마트 추천 알고리즘**: 사용자가 선택한 챔피언들과 가장 많이 일치하는 상위 티어 덱을 우선적으로 보여줍니다.
*   **직관적인 UI**:
    *   반응형 카드 디자인 (모바일 최적화)
    *   챔피언 및 핵심 아이템 이미지 시각화
    *   '공략 더보기' 버튼으로 상세 빌더 페이지 연결

## 🛠️ 기술 스택 (Tech Stack)

*   **Language**: Python 3.9+
*   **Web Framework**: [Streamlit](https://streamlit.io/)
*   **Crawling**: `curl_cffi` (TLS Fingerprint 우회), `BeautifulSoup4`
*   **Deployment**: Streamlit Cloud

## 🤖 Vibe Coding & AI

이 프로젝트는 **Vibe Coding (바이브 코딩)** 방법론을 통해 개발되었습니다. 
개발자가 "안정적이고 빠른 추천 시스템"이라는 의도(Intention)를 제시하면, AI가 아키텍처를 설계하고 코드를 구현하며 상호작용했습니다.

*   **Used AI Model**: Google **Gemini 2.0 Pro Experimental** & **Gemini 2.5 Flash**
    *   (초기 설계 및 구조 분리: 2.0 Pro / UI 최적화 및 디버깅: 2.5 Flash)
*   **AI의 역할**: 
    *   크롤링/뷰어 분리 아키텍처 제안 및 구현
    *   `lolchess.gg` 데이터 구조 분석 및 JSON 파싱
    *   Streamlit UI 디자인 (CSS Customizing, Flexbox 레이아웃)
    *   `NoneType` 오류 디버깅 및 예외 처리 강화

## 📦 설치 및 실행 방법 (Installation)

### 1. 저장소 클론 및 라이브러리 설치
```bash
git clone https://github.com/your-username/tft-deck-recommender.git
cd tft-deck-recommender
pip install -r requirements.txt
```

### 2. 데이터 수집 (최초 1회 필수)
먼저 메타 데이터를 수집하여 `tft_data.json` 파일을 생성해야 합니다.
```bash
python3 scraper.py
```
*(서버 운영 시 이 스크립트를 crontab 등으로 주기적으로 실행하세요)*

### 3. 웹 앱 실행
```bash
streamlit run tft_app.py
```

## 📝 라이선스 (License)

This project is open-source and available under the MIT License.
*Data source: [lolchess.gg](https://lolchess.gg)*
