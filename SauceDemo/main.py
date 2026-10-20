import time
from aw.public.public_aw import *

MAX_RETRY_ROUND = 2  # 最多重试轮次
CASE_LIST_FILE = "case_list.txt"
BASE_CASE_DIR = "testcase"
now_time = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime())
report_path = './report/' + now_time + '/'
ALLURE_RESULTS = os.path.join(report_path, "allure-results")
ALLURE_REPORT = os.path.join(report_path, "allure-report")


if __name__ == "__main__":
    # # 每次执行前清空allure结果目录，防止脏数据
    if os.path.exists(ALLURE_RESULTS):
        shutil.rmtree(ALLURE_RESULTS)
    os.makedirs(ALLURE_RESULTS, exist_ok=True)

    create_files_report(report_path, ALLURE_RESULTS)
    create_read_index(report_path)
    # 读取用例清单
    case_items, case_file_exist = read_case_list(CASE_LIST_FILE, BASE_CASE_DIR)
    # case_list处理，存在但是无有效用例，case_items为空，pytest不传参数默认跑testcase全部用例

    subprocess.run(["pytest", "--cache-clear"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    logging.info("pytest缓存清理完成")
    current_round = 1

    logging.info(f"DEBUG: 准备传给run_pytest的用例列表 = {case_items}")

    first_run_args = case_items
    ret_code = run_pytest(report_path, ALLURE_RESULTS, first_run_args, round_num=current_round)
    # 失败重跑，--lf，结果追加到同一个allure‑results
    while ret_code != 0 and current_round < MAX_RETRY_ROUND + 1:
        current_round += 1
        logging.info(f"\n========== 检测到失败用例，开始第{current_round}轮【仅执行上次失败用例 --lf】 ==========\n")
        ret_code = run_pytest(report_path, ALLURE_RESULTS, ["--lf"], round_num=current_round)
    # 全部执行完成，生成合并的allure报告
    generate_allure_final_report(ALLURE_RESULTS, ALLURE_REPORT)
    if ret_code == 0:
        logging.info("\n 最终：所有用例执行成功！")
    else:
        logging.info(f"\n 最终：经过{MAX_RETRY_ROUND}轮重试后，仍然存在失败用例！")
    # # 如果存在失败用例，将截图、录屏及日志放入report_path文件夹
    if os.path.exists(r'./test-results/'):
        for itm in os.listdir(r'./test-results'):
            src_item = os.path.join(r'./test-results/', itm)
            dst_item = os.path.join(report_path, itm)
            shutil.move(src_item, dst_item)
        os.rmdir(r'./test-results')
    sys.exit(ret_code)
