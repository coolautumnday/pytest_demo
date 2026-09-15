import subprocess
import os
import shutil
import sys
import time

# ===================== 配置区 =====================
MAX_RETRY_ROUND = 2    # 全量跑完后，最多再整体重试失败集合几轮
TEST_RESULT_DIR = "test-results"
now_time = time.strftime("%Y-%m-%d %H_%M_%S", time.localtime())
report_path = './report/' + now_time + '/'


# =================================================
def creat_files_report():
    os.mkdir(report_path)
    print(f"✅ 成功创建文件夹，本次执行日志存档位置为：{report_path}\n")
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
        "--html", html_report,
        "--junitxml", junit_xml
    ] + pytest_args

    print(f"========== 【第 {round_num} 轮测试开始】 ==========")
    print(f"执行命令：{' '.join(cmd)}")
    print(f"HTML报告：{html_report}")
    print(f"JUnit文件：{junit_xml}\n")

    # 核心修复：subprocess.run，实时输出控制台日志，Windows不会缓冲区卡死
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


if __name__ == "__main__":
    creat_files_report()
    # 执行前清空 pytest 缓存
    run_pytest([], '--cache-clear')
    current_round = 1
    # 第一轮：执行全部用例
    ret_code = run_pytest([], round_num=current_round)

    # 如果有用例失败，循环执行 --lf 只跑失败用例
    while ret_code != 0 and current_round < MAX_RETRY_ROUND + 1:
        current_round += 1
        print(f"\n========== 检测到失败用例，开始第{current_round}轮【仅执行上次失败用例 --lf】 ==========\n")
        ret_code = run_pytest(["--lf"], round_num=current_round)

    if ret_code == 0:
        print("\n🎉 最终：所有用例执行成功！")
    else:
        print(f"\n💥 最终：经过{MAX_RETRY_ROUND}轮重试后，仍然存在失败用例！")

    sys.exit(ret_code)
