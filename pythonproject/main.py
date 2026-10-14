from aw.public.public_aw import *

# ===================== 配置区 =====================
MAX_RETRY_ROUND = 2  # 最多重试轮次
CASE_LIST_FILE = "case_list.txt"
BASE_CASE_DIR = "testcase"

now_time = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
report_path = './report/' + now_time + '/'
ALLURE_RESULTS = os.path.join(report_path, "allure-results")
ALLURE_REPORT = os.path.join(report_path, "allure-report")


def read_case_list(file_path=CASE_LIST_FILE):
    """
    读取case_list.txt，自动补全testcase路径
    返回元组 (case_list:list, file_exists:bool)
    支持输入：
        test_demo1
        test_demo1.py
        test_demo1.py::test_case
        .\testcase\test_demo1.py::xxx 绝对路径直接保留
    """
    cases = []
    file_exists = os.path.exists(file_path)
    if not file_exists:
        print(f"⚠️ {file_path} 文件不存在，执行全部用例")
        return cases, file_exists

    with open(file_path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            # 跳过空行、注释行
            if not line or line.startswith("#"):
                continue
            # 分离 用例文件部分 和 :用例函数部分
            if "::" in line:
                file_part, func_part = line.split("::", maxsplit=1)
            else:
                file_part = line
                func_part = None
            # 判断是否是绝对路径，如果是绝对路径不做补全
            if os.path.isabs(file_part):
                final_file = file_part
            else:
                # 简写逻辑处理
                if not file_part.endswith(".py"):
                    # test_demo1 → test_demo1.py
                    file_part = file_part + ".py"
                # 拼接 testcase/xxx.py
                final_file = os.path.join(BASE_CASE_DIR, file_part)
            # 组装完整pytest用例路径
            if func_part is not None:
                full_case = f"{final_file}::{func_part}"
            else:
                full_case = final_file
            cases.append(full_case)
            print(f"✅ 解析用例：{line} → {full_case}")

    if len(cases) == 0:
        print(f"⚠️ {file_path} 文件存在，但是有效用例行为0！")
    return cases, file_exists


def run_pytest(pytest_args: list, round_num: int) -> int:
    html_report = os.path.join(report_path, f"report_{round_num}.html")
    junit_xml = os.path.join(report_path, f"result_{round_num}.xml")

    # 每一轮执行前清空allure结果目录，防止历史数据污染
    if os.path.exists(ALLURE_RESULTS):
        shutil.rmtree(ALLURE_RESULTS)
    os.makedirs(ALLURE_RESULTS)

    print('执行用例列表', pytest_args)
    cmd = [
              "pytest",
              "--clean-alluredir",
              "--html", html_report,
              "--junitxml", junit_xml,
              "--alluredir", ALLURE_RESULTS
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


if __name__ == "__main__":
    create_files_report(report_path, ALLURE_RESULTS)
    create_read_index(report_path)

    # 读取用例清单
    case_items, case_file_exist = read_case_list(CASE_LIST_FILE)

    # case_list.txt存在但是没有有效用例，直接退出，不跑用例
    if case_file_exist and len(case_items) == 0:
        print("❌ case_list.txt存在，但没有任何有效用例，程序退出，不执行任何测试！")
        sys.exit(1)

    # --------------------------
    # 单独执行清除缓存，不再复用run_pytest（重点修复！不会跑用例）
    # --------------------------
    subprocess.run(["pytest", "--cache-clear"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("✅ pytest缓存清理完成")

    current_round = 1
    print("DEBUG: 准备传给run_pytest的用例列表 = ", case_items)
    first_run_args = case_items
    ret_code = run_pytest(first_run_args, round_num=current_round)

    # 失败重跑，--lf，结果继续追加到同一个allure‑results
    while ret_code != 0 and current_round < MAX_RETRY_ROUND + 1:
        current_round += 1
        print(f"\n========== 检测到失败用例，开始第{current_round}轮【仅执行上次失败用例 --lf】 ==========\n")
        ret_code = run_pytest(["--lf"], round_num=current_round)

    # 🎯全部pytest执行完成，生成一份合并的allure报告
    generate_allure_final_report(ALLURE_RESULTS, ALLURE_REPORT)

    if ret_code == 0:
        print("\n🎉 最终：所有用例执行成功！")
    else:
        print(f"\n💥 最终：经过{MAX_RETRY_ROUND}轮重试后，仍然存在失败用例！")
    sys.exit(ret_code)
