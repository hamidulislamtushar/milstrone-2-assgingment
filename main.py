import openai
import base64
from requests import get, post



username = "admin"
password = "PCK0 SIdP q7JV HGMO JAtB KTCy"
credential = f"{username}:{password}"
token = base64.b64encode(credential.encode())
headers = {"Authorization": f"Basic {token.decode('utf-8')}"}


def create_wp_post(title, content, slug):
    api_url = "https://localhost/www/wp-json/wp/v2/posts"
    data = {
        "title": title,
        "content": content,
        "slug": slug,
        "status": "publish",
    }
    response = post(api_url, headers=headers, json=data, verify=False)


def heading(text, heading_tag):
    codes = f'<!-- wp:heading --><{heading_tag}>{text}</{heading_tag}><!-- /wp:heading -->'
    return codes


def html_paragraph(text):
    codes = f'<!-- wp:paragraph --><p>{text}</p><!-- /wp:paragraph -->'
    return codes


def oai_answer_dv(prompt):
    import os
    from dotenv import load_dotenv
    load_dotenv()
    openai.api_key = os.getenv("API_KEY")
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt= prompt,
      temperature=0.7,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
)
    output = response.get("choices")[0].get("text").strip()
    return output


with open("keywords.txt", "r") as file:
    lines = file.readlines()
    keyword_list = list(lines)

for keyword in keyword_list:

    content = ''
    intro_prompt = f"write a buying guide intro about{keyword}"
    intro = oai_answer_dv(intro_prompt)
    why = f'Why {keyword.strip().replace("best","")} is important'
    why_para = oai_answer_dv(why)
    key_factor_heading = f"Factors To Consider When Choosing The{keyword.strip().replace('best','')}"
    key_factor_para = oai_answer_dv(key_factor_heading)
    key_factor = ''
    key_factor_list = key_factor_para.strip().split('\n\n')
    for k in key_factor_list:
        key_factor1 = html_paragraph(k[3:])
        key_factor += key_factor1

    how_heading = f"How to choose {keyword}"
    how_para = oai_answer_dv(how_heading)
    how_list = how_para.strip().split('\n\n')
    how = ''
    for h in how_list:
        how1 = html_paragraph(h[3:])
        how += how1

    con = f"write a conclusion about {keyword} buying guide"
    conclusion_para = oai_answer_dv(con)

    title = f'{keyword.title().strip()} buying guide'
    slug = title.strip().replace(" ","-")

    content = f"{html_paragraph(intro)} {heading(why,'h2')}{html_paragraph(why_para)} {heading(key_factor_heading,'h2')}{key_factor} {heading(how_heading,'h2')}{how} {heading('Conclusion','h2')}{html_paragraph(conclusion_para)}"

    # print(content)
    create_wp_post(title, content, slug)
    print(keyword.strip(), "Buying Guide Posted")


