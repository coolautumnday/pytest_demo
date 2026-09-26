import requests


def test_demo1():
    # 发送get请求
    resp = requests.get("https://httpbin.org/get")

    print(resp.status_code)   # 响应状态码 200成功
    print(resp.text)          # 返回文本内容
    print(resp.json())        # 如果返回是json，直接转python字典

    assert resp.status_code == 200
    assert 'args' in resp.json()