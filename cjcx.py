import re
import json
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

authen = {
    'username': '',
    'password': '',
}

session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.31(0x18001f30) NetType/WIFI Language/zh_CN",
    "Referer": "https://app.buaa.edu.cn/"
}

def get_web(url):
    try:
        page =session.get(url, headers=headers, timeout=10)
        return page
    except requests.exceptions.Timeout:
        print("界面超时，请重试。")
        exit(0)

login_page = get_web("https://sso.buaa.edu.cn/login")
soup = BeautifulSoup(login_page.text, 'html.parser')
execution_input = soup.find('input', {'name': 'execution'})
execution_value = execution_input.get('value', '')
login_data = {
    'username': authen['username'],
    'password': authen['password'],
    'type': 'username_password',
    'submit': 'LOGIN',
    '_eventId': 'submit',
    'execution': execution_value
}

session.post("https://sso.buaa.edu.cn/login", data=login_data)
base_url = "https://app.buaa.edu.cn/buaascore/wap/default/index"

c = get_web(base_url)
session.close()

pattern = r'list:\s*(\[.*?\]),'
match = re.search(pattern, c.text, re.DOTALL)
if match:
    json_str = match.group(1)
    try:
        grade_list = json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"JSON 解析失败: {e}")
        exit()
else:
    print("未找到成绩数据列表。")
    exit()

if  __name__ == "__main__":
    XFC = 0
    table_data = []
    for course in grade_list:
        if course['year'] == "2025-2026" and course['xq'] == "1":
            XFC = XFC + float(course['xf'])
            table_data.append([course['kcmc'], course['xf'], course['kccj']])
    head = ["课程名称", "学分", "成绩"]
    print(tabulate(table_data, headers=head, tablefmt="fancy_grid"))
    print(f"本学期已修学分：{XFC}")