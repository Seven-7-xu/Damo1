import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

BASE = "https://qzoi.aihaoke.net"
#LOGIN_URL = f"{BASE}/teacher/login"  # 若学生端为 /student/，相应修改

LOGIN_URL = "https://passport.aihaoke.net/auth/login?tenantSiteUrl=https://qzoi.aihaoke.net&locale=zh-CN"

def create_session():
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })
    return s

def login(session: requests.Session):
    r = session.get(LOGIN_URL, timeout=10)
    soup = BeautifulSoup(r.text, "lxml")

    form = soup.find("form")
    if not form:
        print("[!] 未找到登录表单，将使用当前URL提交")
    # 如果找不到 form，我们就不从 form 里找了，直接找页面里所有的 input
    data = {}
    search_area = form if form else soup

    for inp in search_area.find_all("input"):
        name = inp.get("name")
        if not name:
            continue
        # 不管是隐藏还是普通输入框，先收集起来
        data[name] = inp.get("value", "")

    # 强行把账号密码塞进去（根据实际 name 替换）
    data["username"] = os.getenv("JW_USER")
    data["password"] = os.getenv("JW_PASS")
            
    # 根据实际输入框的 name 属性修改
    data["username"] = os.getenv("JW_USER")
    data["password"] = os.getenv("JW_PASS")

    # 不需要 action 了，直接提交到 LOGIN_URL
    r = session.post(
    LOGIN_URL,
    data=data,
    timeout=10,
    )
    r.raise_for_status()

    # 登录成功判断：页面应出现“退出”或用户姓名
    if "退出" not in r.text and "logout" not in r.text.lower():
        print("[!] 登录可能失败，请检查 username/password 字段名或 POST 地址")
    else:
        print("[+] 登录成功")
    return r.text