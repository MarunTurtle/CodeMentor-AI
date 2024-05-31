# CodeMentor AI

#### 비디오 데모: [https://youtu.be/THAn1hq-eVc]

#### 설명:
- CodeMentor AI는 코드 스니펫에 대한 피드백 생성을 자동화하기 위해 개발된 도구임.
- 이 프로젝트는 OpenAI의 GPT-4 모델과 Notion API의 기능을 활용하여 다양한 프로그래밍 언어로 작성된 코드를 분석하고, 통찰력 있는 피드백을 생성하며, Notion 페이지에 업로드 함.

### 배경 및 동기:
1. **코딩/알고리즘 테스트를 준비하면서 두 가지 문제를 해결하고 싶었음**
    - **첫 번째 문제:** 솔루션과 문제의 세부사항, 요구사항 등을 깔끔한 스타일로 Notion에 기록하고 싶었지만, 이를 수동으로 복사하고 붙여넣는 작업이 너무 번거로웠음.
    - **두 번째 문제:** 내 솔루션이 좋은 코드인지 평가받고 싶었음. [참고 영상](https://www.notion.so/AI-93b3d6e97fb54475a7e5bf9d814502f0?pvs=21)을 통해 좋은 코드의 네 가지 기준을 세우게 됨:
        - **문제 이해:** 솔루션은 문제를 어떻게 이해하고 있으며, 제시된 핵심 문제를 해결하고 있는가?
        - **알고리즘과 전략:** 코드가 문제 해결을 위해 적절한 알고리즘, 방법, 또는 라이브러리를 선택했는가? 최적의 Big O 시간 및 공간 복잡성을 가지고 있는가?
        - **요구사항과 가독성:** 코드가 모든 요구사항을 충족하고 있으며, 오류 처리 및 가독성을 포함하여 잘 작성되었는가?
        - **유지보수성 및 확장성:** 코드 구조가 유지보수가 용이하고, 변경되는 요구사항에 적응할 수 있는가?
2. **이러한 문제를 해결하기 위해 CodeMentor AI를 개발하게 되었음.** 이 프로그램은 Notion에 솔루션을 자동으로 기록하고, 위의 기준에 따라 코드를 평가함으로써 두 가지 문제를 모두 해결함.

### 주요 기능:
1. **자동 코드 리뷰:** OpenAI의 GPT-4 모델을 활용하여 다양한 프로그래밍 언어로 작성된 코드에 대한 자세한 댓글을 생성함.
2. **웹 스크래핑:** BeautifulSoup을 사용하여 여러 경쟁 프로그래밍 웹사이트에서 문제 세부사항을 추출함.
3. **Notion 업로드:** 문제 세부사항, 코드 스니펫, 생성된 피드백을 포함한 종합적인 Notion 페이지를 작성함.
4. **데이터 수집:** [solved.ac](http://solved.ac/) 및 ACM-ICPC에서 문제 데이터를 가져와 문제에 대한 전체적인 정보를 제공함.

### 프로젝트 파일:
1. **main.py:** 응용 프로그램을 실행하는 주요 스크립트로, 사용자 입력을 처리하고 데이터를 처리하며 Notion 페이지 생성을 관리함.
2. **keys.py:** OpenAI 및 Notion API 접근에 필요한 API 키와 토큰을 포함함.
3. **langs.py:** 프로젝트에서 사용되는 프로그래밍 언어의 매핑을 포함함.
4. **urls.txt:** 프로젝트에서 사용되는 문제 또는 데이터셋의 URL을 포함하는 텍스트 파일

### API 키 얻기

`keys.py` 파일에 필요한 API 키와 토큰을 설정하려면 다음 단계를 따르세요:

1. **OpenAI API 키:**
   - [OpenAI 웹사이트](https://www.openai.com/)를 방문하여 계정에 로그인함.
   - API 섹션으로 이동하여 새 API 키를 생성함.
   - API 키를 복사하여 `keys.py` 파일의 `'openai_api_key'`에 해당 키로 대체함.

2. **Notion 통합 토큰:**
   - [Notion 웹사이트](https://www.notion.so/)에 접속하여 계정에 로그인함.
   - [Notion Integrations](https://www.notion.so/my-integrations) 페이지에서 새로운 통합을 생성함.
   - 새 통합 토큰을 생성하고 복사함.
   - 통합을 사용할 특정 Notion 페이지 또는 워크스페이스와 공유함.
   - `keys.py` 파일의 `'notion_website_token'`에 해당 토큰으로 대체함.

3. **Notion 페이지 ID:**
   - 프로젝트와 연결하려는 Notion 페이지를 엶.
   - Notion 페이지의 URL을 복사함.
   - URL은 `https://www.notion.so/yourusername/PageName-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` 형식으로 되어 있음.
   - 마지막 슬래시 이후 부분(페이지 ID)을 추출함.
   - `keys.py` 파일의 `'notion_page_id'`에 해당 페이지 ID로 대체함.

다음은 키를 추가한 후 `keys.py` 파일의 예시임:

\`\`\`python
openai = 'your_openai_api_key'
token = 'your_notion_integration_token'
page_id = 'your_notion_page_id'
\`\`\`

### 설치 및 설정:
CodeMentor AI를 설정하고 실행하려면 다음 단계를 따르세요:

1. **리포지토리 클론:**
   \`\`\`bash
   git clone [GitHub Repository URL]
   \`\`\`
2. **프로젝트 디렉토리로 이동:**
   \`\`\`bash
   cd CodeMentor_AI
   \`\`\`
3. **필요한 종속성 설치:**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`
4. **응용 프로그램 실행:**
   \`\`\`bash
   python main.py
   \`\`\`

### 상세 설명:
#### 기능 개요:
- **API 키 설정:**
  이 프로젝트는 OpenAI 및 Notion의 API 키가 필요함. 이 키들은 `keys.py` 파일에 저장되어 있음. 응용 프로그램을 실행하기 전에 유효한 키를 가지고 있는지 확인함.
  
- **코드 댓글 생성:**
  `code_comments` 함수는 OpenAI의 GPT-4 모델을 사용하여 제공된 코드 스니펫을 분석하고 한국어로 댓글을 생성하며, 주요 프로그래밍 용어는 영어로 표시함. 이 함수는 코드 품질 향상에 도움이 되는 자세한 피드백을 보장함.

- **문제 데이터 가져오기:**
  `fetch_complete_problem_data` 함수는 solved.ac 및 ACM-ICPC 웹사이트에서 문제 세부사항을 가져옴. 두 소스의 데이터를 결합하여 종합적인 문제 정보를 제공함.

- **코드 가져오기:**
  `get_code` 함수는 주어진 URL에서 코드와 관련 메타데이터를 추출함. BeautifulSoup을 사용하여 HTML 내용을 구문 분석하고 문제 번호, 프로그래밍 언어, 코드 스니펫과 같은 관련 정보를 추출함.

- **Notion 페이지 생성:**
  `post_page` 함수는 추출된 문제 세부사항과 코드를 사용하여 Notion 페이지를 생성하고 채움. 구조화된 섹션으로 콘텐츠를 구성하고 생성된 댓글을 페이지에 추가함.

#### 디자인 선택:
- **언어:** 파이썬은 풍부한 라이브러리 생태계와 웹 스크래핑, API 통합, 자연어 처리의 용이성 때문에 선택되었음.
- **모듈형 구조:** 코드는 읽기 쉽고 유지 관리가 용이하도록 함수로 구성됨. 각 함수는 특정 책임을 가지며, 코드 이해 및 수정이 쉬워짐.
- **API 통합:** 이 프로젝트는 외부 API(OpenAI 및 Notion)와 통합되어 기능을 향상시킴. 이러한 선택은 자연어 처리 및 콘텐츠 관리와 같은 복잡한 작업을 자동화할 수 있게 함.

### 향후 개선 사항:
- **향상된 피드백:** OpenAI API에서 사용되는 프롬프트와 매개변수를 정제하여 피드백의 정확성과 깊이를 향상시킴.
- **사용자 인터페이스:** 도구를 더 쉽게 접근할 수 있도록 그래픽 사용자 인터페이스(GUI)를 개발함. e.g. Chrome Extension
- **다중 언어 지원:** 도구를 확장하여 여러 프로그래밍 언어를 지원하고 다양한 언어로 피드백을 제공함.

### 결론:
CodeMentor AI 프로젝트는 인공지능과 자동화를 결합하여 코드 품질과 생산성을 향상시킬 수 있는 가능성을 보여줌. 피드백 과정을 자동화함으로써 프로그래머들이 적시에 건설적인 피드백을 받을 수 있도록 도와줌으로써, 궁극적으로 코딩 기술과 프로젝트 결과를 향상시킴.