import subprocess
import os
import shutil
import sys
import time
# ===================== 配置区 =====================
MAX_RETRY_ROUND = 2    # 全量跑完后，最多再整体重试失败集合几轮
TEST_RESULT_DIR = "test-results"
now_time = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
report_path = './report/' + now_time + '/'

# allure路径，放在本次时间戳报告目录内
ALLURE_RESULTS = os.path.join(report_path, "allure-results")
ALLURE_REPORT = os.path.join(report_path, "allure-report")

# =================================================
def create_read_index():
    filename = os.path.join(report_path, 'index.bat')
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        f.write('''@echo off
allure open -h 127.0.0.1 -p 8083 allure-report
start chrome http://127.0.0.1:8083
pause''')
    print(f"✅ 创建bat文件完成\n")

def creat_files_report():
    os.makedirs(report_path, exist_ok=True)
    print(f"✅ 成功创建文件夹，本次执行日志存档位置为：{report_path}\n")

    # 清空本次allure原始结果目录
    if os.path.exists(ALLURE_RESULTS):
        shutil.rmtree(ALLURE_RESULTS)
    os.makedirs(ALLURE_RESULTS, exist_ok=True)

    # 删除playwright test-results
    if os.path.exists(TEST_RESULT_DIR):
        shutil.rmtree(TEST_RESULT_DIR)
    os.makedirs(TEST_RESULT_DIR, exist_ok=True)
    print(f"✅ 清理完成：{report_path}、{TEST_RESULT_DIR}，保留.pytest_cache缓存\n")


def run_pytest(pytest_args: list, round_num: int) -> int:
    html_report = os.path.join(report_path, f"report_{round_num}.html")
    junit_xml = os.path.join(report_path, f"result_{round_num}.xml")
    cmd = [
        "pytest",
        "-m", "smoke",
        "--html", html_report,
        "--junitxml", junit_xml,
        "--alluredir", ALLURE_RESULTS   # 每一轮pytest都输出到同一个allure‑results，自动追加
    ] + pytest_args

    print(f"========== 【第 {round_num} 轮测试开始】 ==========")
    print(f"执行命令：{' '.join(cmd)}")
    print(f"HTML报告：{html_report}")
    print(f"JUnit文件：{junit_xml}")
    print(f"Allure原始数据目录：{ALLURE_RESULTS}\n")
    try:
        result = subprocess.run(
            cmd,
            stdout=sys.stdout,
            stderr=sys.stderr,
            text=True
        )
        return result.returncode
    except Exception as e:
        print(f"❌ 执行pytest异常：{e}")
        return 1


def generate_allure_final_report():
    """全部pytest轮次结束后，生成合并后的allure汇总报告"""
    print("\n========== 开始生成 Allure 汇总报告 ==========")
    env = os.environ.copy()
    env["JAVA_HOME"] = r"D:\jdk11"
    env["PATH"] = os.path.join(env["JAVA_HOME"], "bin") + os.pathsep + env["PATH"]

    allure_exe = r"D:\Program Files (x86)\allure-2.46.1\bin\allure.bat"
    generate_cmd = [
        allure_exe,
        "generate",
        ALLURE_RESULTS,
        "-o",
        ALLURE_REPORT,
        "--clean"
    ]
    print(f"allure generate 命令: {' '.join(generate_cmd)}")
    ret = subprocess.run(generate_cmd, stdout=sys.stdout, stderr=sys.stderr, text=True, env=env)
    if ret.returncode == 0:
        print(f"✅ Allure汇总报告生成成功！路径：{ALLURE_REPORT}/index.html")
        # ========== 新增：自动打开allure报告 ==========
        open_cmd = [allure_exe, "open", ALLURE_REPORT]
        subprocess.Popen(open_cmd, env=env)
    else:
        print("❌ Allure报告生成失败，请检查allure命令行工具是否安装并加入环境变量！")


if __name__ == "__main__":
    creat_files_report()
    create_read_index()

    # 清除pytest缓存
    run_pytest(["--cache-clear"], round_num=0)

    current_round = 1
    # 第一轮执行全部用例
    ret_code = run_pytest([], round_num=current_round)

    # 失败重跑，--lf，结果继续追加到同一个allure‑results，**不清理**
    while ret_code != 0 and current_round < MAX_RETRY_ROUND + 1:
        current_round += 1
        print(f"\n========== 检测到失败用例，开始第{current_round}轮【仅执行上次失败用例 --lf】 ==========\n")
        ret_code = run_pytest(["--lf"], round_num=current_round)

    # 🎯全部pytest执行完成，生成一份合并的allure报告（包含第一轮+所有重试轮次的数据）
    generate_allure_final_report()

    if ret_code == 0:
        print("\n🎉 最终：所有用例执行成功！")
    else:
        print(f"\n💥 最终：经过{MAX_RETRY_ROUND}轮重试后，仍然存在失败用例！")
    sys.exit(ret_code)
