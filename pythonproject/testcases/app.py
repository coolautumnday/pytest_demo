# app.py
from flask import Flask, jsonify
import time

app = Flask(__name__)

# 普通get接口
@app.get("/api/hello")
def hello():
    time.sleep(0.01) # 模拟接口耗时10ms
    return jsonify({"code":0, "msg":"success", "data":"hello locust"})

# post接口
@app.post("/api/post")
def add():
    time.sleep(0.02)
    return jsonify({"code":0, "result":100})

# 模拟登录接口
@app.post("/api/login")
def login():
    time.sleep(0.005)
    return jsonify({"code":0, "data":{"token":"test_token_123456"}})

# ========== 这一行必须顶格，前面不能有空格！==========
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=False)
