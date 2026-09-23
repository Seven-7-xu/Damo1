import requests

def test_network():
    print("正在测试云端网络...")
    response = requests.get("https://www.baidu.com")
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        print("网络通畅，可以开始爬虫任务！")

if __name__ == "__main__":
    test_network()