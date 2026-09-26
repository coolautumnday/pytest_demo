import requests

url = "http://127.0.0.1:9003/ocr"
payload = {
    "img_path": r"D:\OCR\test1.png" # 图片绝对路径
}
resp = requests.post(url, json=payload)
print(resp.json())