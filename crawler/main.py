# 这是一个思路代码，需要先 pip install easyocr
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import requests
from bs4 import BeautifulSoup
import easyocr
import urllib.request

def fetch_charter_image_and_ocr():
    url = "https://www.qzoi.edu.cn/xygk/xxzc.htm"
    headers = {"User-Agent": "Mozilla/5.0 ..."}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    
    # 1. 找到图片链接
    img_tag = soup.find('div', id='vsb_content').find('img')
    img_url = img_tag.get('src')
    
    # 拼接完整 URL（如果是相对路径）
    if not img_url.startswith('http'):
        img_url = "http://www.qzoi.edu.cn" + img_url
        
    print(f"找到图片地址: {img_url}")
    
    # 2. 下载图片
    print("正在下载图片...")
    try:
        #创建一个忽略SSL证书验证的上下文
        context = ssl._create_unverified_context()
        #使用urllib下载图片
        req = urllib.request.Request(img_url, headers=headers)
        with urllib.request.urlopen(req, context=context) as response:
            print(f"请求状态码: {response.status}")
            img_data = response.read()

        #确保data目录存在
        import os
        os.makedirs("data", exist_ok=True)
        with open("data/charter.jpg", "wb") as f:
            f.write(img_data)
        print("图片下载完成，已保存为 data/charter.jpg")
    except Exception as e:
        print(f"下载图片失败: {e}")
        exit()
    
    with open("data/charter.jpg", "wb") as f:
        f.write(img_data)
        
    # 3. 调用 OCR 识别
    reader = easyocr.Reader(['ch_sim', 'en']) # 识别简体中文和英文
    result = reader.readtext('data/charter.jpg', detail=0) # 只返回文本
    
    # 4. 保存为 TXT
    with open("data/charter.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(result))
    print("🎉 OCR 识别完成，已保存为 TXT！")

if __name__ == "__main__":
    fetch_charter_image_and_ocr()