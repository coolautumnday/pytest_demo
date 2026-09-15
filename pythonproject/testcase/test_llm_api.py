import pytest
import requests
from sentence_transformers import SentenceTransformer, util

# 加载本地向量模型（all-MiniLM-L6-v2轻量，中文可换bge模型）
model = SentenceTransformer('all-MiniLM-L6-v2')


# ---------------------- 工具函数1：向量相似度校验 ----------------------
def calc_semantic_similarity(text_a: str, text_b: str) -> float:
    emb1 = model.encode(text_a, convert_to_tensor=True)
    emb2 = model.encode(text_b, convert_to_tensor=True)
    cos_sim = util.cos_sim(emb1, emb2)
    return float(cos_sim.item())


# ---------------------- 工具函数2：LLM-as-judge裁判评估 ----------------------
def llm_judge(question: str, actual_answer: str, reference_answer: str, judge_api_url: str, api_key: str):
    """
    裁判大模型：评估被测模型回答是否满足要求
    返回score: 0~10，越高越符合预期
    """
    judge_prompt = f"""
                【评测任务】
                用户问题：{question}
                参考答案：{reference_answer}
                被测模型回答：{actual_answer}
                
                评测规则：
                1. 判断被测回答是否准确回答用户问题，不能有错误信息、幻觉；
                2. 只要语义一致，表述不一样也算正确；
                3. 输出JSON格式：{{"score":分数(0-10), "reason":"理由"}}
                """
    payload = {
        "model": "xxx",
        "messages": [{"role": "user", "content": judge_prompt}],
        "temperature": 0
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    resp = requests.post(judge_api_url, json=payload, headers=headers, timeout=30)
    data = resp.json()
    return data


# ---------------------- 测试用例：被测LLM接口 ----------------------
@pytest.mark.parametrize(
    "user_query, ref_answer, sim_threshold",
    [
        ("什么是pytest？", "pytest是Python自动化测试框架", 0.7),
    ]
)
def test_llm_api_semantic(user_query, ref_answer, sim_threshold):
    # 1. requests调用被测大模型接口
    url = "http://127.0.0.1:8000/chat"
    resp = requests.post(url, json={"query": user_query}, timeout=20)
    assert resp.status_code == 200
    actual_text = resp.json()["reply"]
    print(f"\n被测输出：{actual_text}")

    # 方案A：sentence-transformers 向量相似度断言
    sim_score = calc_semantic_similarity(actual_text, ref_answer)
    print(f"语义相似度：{sim_score:.3f}")
    assert sim_score >= sim_threshold, f"相似度不足，当前：{sim_score}"

    # 方案B：LLM-as-judge裁判校验（按需开启，会额外调用裁判模型）
    # judge_result = llm_judge(
    #     question=user_query,
    #     actual_answer=actual_text,
    #     reference_answer=ref_answer,
    #     judge_api_url="https://xxx/v1/chat/completions",
    #     api_key="sk-xxx"
    # )
    # judge_score = judge_result["score"]
    # assert judge_score >=7, f"裁判判定不达标，分数：{judge_score}"
