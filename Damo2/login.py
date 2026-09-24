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
    action = form.get("action") or LOGIN_URL

    data = {}
    for inp in form.find_all("input"):
        name = inp.get("name")
        if not name:
            continue
        if inp.get("type") == "hidden":
            data[name] = inp.get("value", "")

    # 根据实际输入框的 name 属性修改
    data["username"] = os.getenv("JW_USER")
    data["password"] = os.getenv("JW_PASS")

    r = session.post(
        requests.compat.urljoin(LOGIN_URL, action),
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