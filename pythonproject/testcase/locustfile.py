from locust import HttpUser, task, between

# HttpUser：模拟HTTP用户
class WebUser(HttpUser):
    # 每个用户执行任务之间等待时间，1~3秒随机
    wait_time = between(1, 3)

    # 压测任务 @task 权重越大执行概率越高
    @task(2)
    def test_get(self):
        # get请求，self.client 是requests封装
        resp = self.client.get("/api/hello")
        # 断言，失败会标记为请求失败
        assert resp.status_code == 200

    @task(1)
    def test_post(self):
        payload = {"name": "locust"}
        resp = self.client.post("/api/post", json=payload)
        assert resp.json()["code"] == 0

    # 用户启动前执行一次（登录、初始化）
    def on_start(self):
        # 登录获取token，后续接口带上
        resp = self.client.post("/api/login", json={"user":"test","pwd":"123456"})
        token = resp.json()["data"]["token"]
        self.client.headers.update({"Authorization": f"Bearer {token}"})

    # 用户停止时执行
    def on_stop(self):
        print("用户退出")
