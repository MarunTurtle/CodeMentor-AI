# Third-party libraries for HTTP requests, web scraping, and AI
import requests
import openai
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# Local application imports for configuration and language mappings
import keys
from langs import langs

# Notion client and block imports for content management
from notion.client import NotionClient
from notion.block import (
    SubsubheaderBlock, TextBlock, PageBlock,
    CalloutBlock, QuoteBlock, CodeBlock, ColumnListBlock, ColumnBlock
)

openai.api_key = keys.openai
notion_token_v2 = keys.token
notion_page_id = keys.page_id

# create user_agent for data scraping
ua = UserAgent()
user_agent = ua.random
headers = {
    'User-Agent': user_agent
}

def code_comments(param):
    try:
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[
                {
                    'role': 'system',
                    'content': (
                        '당신은 숙련된 프로그래머이자 경험 많은 코드 리뷰어입니다. '
                        'Python 코드 분석, 복잡한 개념을 명확하게 설명하는 데 능숙하며, '
                        '건설적인 피드백을 제공할 수 있습니다. 문제 해결, Big-O 표기법을 사용한 '
                        '알고리즘 효율성, 코딩 모범 사례에 대해 논의하는 방법을 이해하고, '
                        '코드 유지 관리 및 확장성에 대한 통찰력을 제공할 수 있습니다. '
                        '한국어로 작성하되 중요한 프로그래밍 키워드는 영어로 표기해야 합니다.'
                        '말투는  (\"~이다\")로 작성하시오.'
                    )
                },
                {
                    'role': 'user',
                    'content': (
                        "자신이 작성한 Python 코드 스니펫을 분석해 주세요. 한국어로 작성하되 분석할 때 중요한 프로그래밍 관련 키워드는 영어로 답변해 주십시오. 제공된 코드 스니펫의 일부를 언급해야 한다면 코드 마크업을 이용하세요. 말투는 ('~이다')로 작성하시오. 다음 기준에 따라 코드를 검토해주세요:\n\n"
                        "1. 문제 이해: 코드가 문제를 어떻게 이해하고 있는가?\n"
                        "2. 알고리즘과 전략: 선택된 알고리즘과 문제 해결 전략을 설명하고, 왜 이 알고리즘이 문제에 적합한지 서술하세요. Big-O 표기법을 사용하여 로직의 시간 복잡성을 포함해주세요.\n"
                        "3. 요구 사항 충족과 가독성: 코드가 모든 요구 사항을 충족하는지 검토하고, 가독성을 평가하세요. 누락된 부분이나 개선점이 있다면 지적해주세요.\n"
                        "4. 유지 보수성과 확장 가능성: 코드의 유지 보수를 쉽게 할 수 있는 구조를 평가하고, 변경되는 요구 사항에 어떻게 적응할 수 있는지 분석해주세요.\n"
                        "코드 스니펫은 다음과 같습니다:\n" + param
                    )
                }
            ],
            temperature=0.3,
            top_p = 0.2,  # Adjust the creativity/variability of the response
            max_tokens=2000
        )
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return

    return response['choices'][0]['message']['content']

def fetch_complete_problem_data(prob_n):
    # Create a user_agent for data scraping
    ua = UserAgent()
    user_agent = ua.random
    headers = {
        'User-Agent': user_agent
    }

    print("문제 정보 추출 중")
    
    # Fetch problem data from solved.ac API
    url_solved_ac = "https://solved.ac/api/v3/problem/show"
    querystring = {"problemId": str(prob_n)}
    api_headers = {"Accept": "application/json"}
    
    try:
        response_solved_ac = requests.get(url_solved_ac, headers=api_headers, params=querystring)
        response_solved_ac.raise_for_status()  # This will throw an error if the call fails
        data = response_solved_ac.json()
        problemId = data['problemId']
        titleKo = data['titleKo']
        level = data['level']
        tags = [tag['displayNames'][0]['name'] for tag in data['tags']]
        solved_ac_details = [problemId, titleKo, level, tags]
    except requests.RequestException:
        print("Solved.ac API ERROR!")
        solved_ac_details = []

    # Fetch additional problem details from ACM-ICPC problem page
    url_acm_icpc = f'https://www.acmicpc.net/problem/{prob_n}'
    try:
        response_acm_icpc = requests.get(url_acm_icpc, headers=headers)
        response_acm_icpc.raise_for_status()  # This will throw an error if the call fails

        soup = BeautifulSoup(response_acm_icpc.content, 'html.parser')
        
        problem_description_div = soup.select_one('#problem_description')
        problem_text = "\n".join([p.text.strip() for p in problem_description_div.find_all('p')])

        problem_input_div = soup.select_one('#problem_input')
        input_text = "\n".join([p.text.strip() for p in problem_input_div.find_all('p')])
        
        problem_output_div = soup.select_one('#problem_output')
        output_text = "\n".join([p.text.strip() for p in problem_output_div.find_all('p')])

        list_sampleinput_text = []
        list_sampleoutput_text = []
        sample_index = 1
        while True:
            sample_input_text = soup.select_one(f'#sample-input-{sample_index}')
            sample_output_text = soup.select_one(f'#sample-output-{sample_index}')
            if not (sample_input_text and sample_output_text):
                break
            list_sampleinput_text.append(sample_input_text.text.replace('\xa0', ' ').strip())
            list_sampleoutput_text.append(sample_output_text.text.replace('\xa0', ' ').strip())
            sample_index += 1

        acm_icpc_details = [
            "문제", problem_text, "입력", input_text,
            "출력", output_text, "예제 입력", list_sampleinput_text,
            "예제 출력", list_sampleoutput_text
        ]
    except requests.RequestException:
        print("Failed to fetch problem details from ACM-ICPC.")
        acm_icpc_details = []

    print("문제 정보 추출 완료")

    # Combine and return the fetched data
    return solved_ac_details + acm_icpc_details
    
def get_code(code_link):
    with requests.Session() as session:

        print("코드 분석중")
        r = session.get(code_link, headers=headers)
        soup = BeautifulSoup(r.text,'html.parser')

        h1_tag = soup.find('h1', class_="pull-left")
        a_tag = h1_tag.find('a', href=lambda x: x and '/problem/' in x)

        if a_tag:
            href_value = a_tag['href']
            problem_number = href_value.split('/')[-1]

        textarea_tag = soup.find('textarea', {'class': 'form-control no-mathjax codemirror-textarea'})
        if textarea_tag:
            source_code = textarea_tag.text

        divs = soup.find_all('div', {'class': 'col-md-12'})

        for div in divs:
            headline_tag = div.find('div', {'class': 'headline'})
            if headline_tag:
                h2_tag = headline_tag.find('h2')
                if h2_tag:
                    lang = h2_tag.text
                    code_lang = langs[lang]

        tds = soup.find_all('td', {'class': 'text-center'})
        info = []
        for td in tds:
            info.append(td.text)
        extra_info=info[1:]
        extra_info[0]=extra_info[0]+'KB'
        extra_info[1]=extra_info[1]+'ms'
        extra_info[2]=extra_info[2]+'B'

        print("코드 분석 완료")
        return [problem_number, code_lang, source_code,extra_info]

def post_page(problem_info, submitted_code, code, extra_info, code_link):
    try:
        client = NotionClient(token_v2=notion_token_v2)
    except Exception as e:
        print("Notion Client Error:", e)
        return
    
    print("노션 커밋 중")

    page = client.get_block(notion_page_id)

    # Page title
    post_title = f'{problem_info[0]} - {problem_info[1]}'
    new_page = page.children.add_new(PageBlock, title=post_title)

    # Problem link
    link_text_block = new_page.children.add_new(TextBlock)
    link_text_block.title = f'[문제 링크](https://www.acmicpc.net/problem/{problem_info[0]})'

    # Solution link
    link_text_block = new_page.children.add_new(TextBlock)
    link_text_block.title = f'[해결 링크]({(code_link[0])})'

    # Page icon
    tier = str(problem_info[2])
    icon_url = f'https://d2gd6pc034wcta.cloudfront.net/tier/{tier}.svg'
    new_page.icon = icon_url

    # Page callout with tags
    callout_info = '/'.join(problem_info[3])
    callout = new_page.children.add_new(CalloutBlock, title=callout_info)
    callout.icon = "💡"
    callout.color = "gray_background"

    # Adding problem, input, output
    new_page.children.add_new(SubsubheaderBlock, title=problem_info[4])  # Problem headline
    problem_text_callout = new_page.children.add_new(CalloutBlock, title=problem_info[5])
    problem_text_callout.icon = "🧐"
    problem_text_callout.color = "blue_background"
    
    # Create a new column list for organizing Input and Output sections
    column_list1 = new_page.children.add_new(ColumnListBlock)

    # Create the first column for Input section
    input_column = column_list1.children.add_new(ColumnBlock)
    
    # Add a subsubheader for Input
    input_column.children.add_new(SubsubheaderBlock, title=problem_info[6])
    # Add a callout block for Input text
    input_text_callout = input_column.children.add_new(CalloutBlock, title=problem_info[7])
    input_text_callout.icon = "⌨"  # Set the icon to a keyboard
    input_text_callout.color = "yellow_background"  # Set the background color to yellow

    # Create the second column for Output section
    output_column = column_list1.children.add_new(ColumnBlock)
    # Add a subsubheader for Output
   
    output_column.children.add_new(SubsubheaderBlock, title=problem_info[8])
    # Add a callout block for Output text
    output_text_callout = output_column.children.add_new(CalloutBlock, title=problem_info[9])
    output_text_callout.icon = "🖥️"  # Set the icon to a computer monitor
    output_text_callout.color = "yellow_background"  # Set the background color to yellow

    # Sample Inputs and Outputs with headlines and texts
    column_list2 = new_page.children.add_new(ColumnListBlock)  # Add a new column list
    
    # Create the first column for input
    input_column = column_list2.children.add_new(ColumnBlock)
    input_column.children.add_new(TextBlock, title=f'**{problem_info[10]}**')  # Sample Input Headline, bold
    # Add all sample input texts under the headline
    for sample_input_text in problem_info[11]:
        input_column.children.add_new(TextBlock, title=f'{sample_input_text}', color='gray_background')  # Sample Input Texts, grey background

    # Create the second column for output
    output_column = column_list2.children.add_new(ColumnBlock)
    output_column.children.add_new(TextBlock, title=f'**{problem_info[12]}**')  # Sample Output Headline, bold
    # Add all sample output texts under the headline
    for sample_output_text in problem_info[13]:
        output_column.children.add_new(TextBlock, title=f'{sample_output_text}', color='gray_background')  # Sample Output Texts

    # Submit Info Callout
    quote_info = f"**{'Memory   '+extra_info[0]:<50}{'Time   '+extra_info[1]:^0}{'Code Length   '+extra_info[2]:>50}**"
    quote = new_page.children.add_new(QuoteBlock)
    quote.title = quote_info

    # Formatting code for display
    code_lines = code.splitlines()
    formatted_code = '\n    '.join(code_lines)
    formatted_code = '    ' + formatted_code  # Add indentation to the first line as well

    # Code block
    new_page.children.add_new(CodeBlock, title=formatted_code, language=submitted_code)

    print("챗GPT 작성 중")

    # code comments
    new_text_block = new_page.children.add_new(TextBlock)
    new_text_block.title = code_comments("\n".join(code_lines))

    print(f'{problem_info[0]} 커밋 완료')

def main():
    while True:
        code_links = input(">>>Input Source Code Links: ")
        code_links = [code_link.strip() for code_link in code_links.split('\n')]
        if code_links[0].lower() == "done":
            break
        for code_link in code_links:
            submit_info = get_code(code_link)
            problem_info = fetch_complete_problem_data(submit_info[0])
            post_page(problem_info, submit_info[1], submit_info[2], submit_info[3], code_links)

if __name__ == "__main__":
    main()