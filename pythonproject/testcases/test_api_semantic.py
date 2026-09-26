import requests
import pytest

from sentence_transformers import SentenceTransformer

@pytest.fixture(scope="session")
def api_base_url():
    # 你的本地服务地址
    return "http://127.0.0.1:8000"

@pytest.fixture(scope="session")
def embedding_model():
    # 加载轻量模型，第一次运行会自动下载
    # all-MiniLM-L6-v2 很小，CPU跑得很快
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model

def cosine_similarity(vec1, vec2):
    import numpy as np
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 ==0 or norm2 ==0:
        return 0.0
    return np.dot(vec1, vec2) / (norm1 * norm2)

def test_qa_semantic_match(api_base_url, embedding_model):
    # 1. 请求业务API
    payload = {"query": "什么是向量数据库？"}
    # resp = requests.post(f"{api_base_url}/qa", json=payload, timeout=20)
    # assert resp.status_code == 200
    # answer = resp.json()["answer"]
    answer = "向量数据库存储向量嵌入，做相似度检索，用于大模型应用"
    # 2. 预期参考回答
    reference = "向量数据库专门存储向量嵌入，可以做相似度检索，常用于RAG大模型应用"
    # 3. 向量化+相似度计算
    vec_ans = embedding_model.encode(answer)
    vec_ref = embedding_model.encode(reference)
    sim = cosine_similarity(vec_ans, vec_ref)
    print(f"相似度分数: {sim:.3f}")

    # 断言阈值，根据业务调整
    assert sim >= 0.75, f"语义相似度过低，分数：{sim}"
