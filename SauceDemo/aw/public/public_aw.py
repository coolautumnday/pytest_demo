import functools
import logging
import os
import shutil
import subprocess
import sys

def check_result(fail_msg):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            if res is None:
                return res
            if not bool(res):
                raise AssertionError(f"{fail_msg}, 方法 {func.__name__} 返回值: {res}")
            return res
        return wrapper
    return decorator

# # main用到函数==============================
def create_read_index(report_path):
    filename = os.path.join(report_path, 'open_allure.bat')
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        f.write('@echo off allure open -h 127.0.0.1 -p 8083 allure-report start chrome http://127.0.0.1:8083 pause')
    logging.info(f"创建bat文件完成\n")

def create_files_report(report_path, ALLURE_RESULTS):
    os.makedirs(report_path, exist_ok=True)
    logging.info(f"成功创建文件夹，本次执行日志存档位置为：{report_path}\n")

    # # 清空本次allure原始结果目录
    if os.path.exists(ALLURE_RESULTS):
        shutil.rmtree(ALLURE_RESULTS)
    os.makedirs(ALLURE_RESULTS, exist_ok=True)

    # # 删除playwright test-results
    if os.path.exists("test-results"):
        shutil.rmtree("test-results")
    os.makedirs("test-results", exist_ok=True)
    logging.info(f"清理完成：{report_path}、{"test-results"}，保留.pytest_cache缓存\n")

def generate_allure_final_report(ALLURE_RESULTS, ALLURE_REPORT):
    """全部pytest轮次结束后，生成合并后的allure汇总报告"""
    logging.info("\n========== 开始生成 Allure 汇总报告 ==========")
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
    logging.info(f"allure generate 命令: {' '.join(generate_cmd)}")
    ret = subprocess.run(generate_cmd, stdout=sys.stdout, stderr=sys.stderr, text=True, env=env)
    if ret.returncode == 0:
        logging.info(f"Allure汇总报告生成成功！路径：{ALLURE_REPORT}/index.html")
        # # 自动打开allure报告
        open_cmd = [allure_exe, "open", ALLURE_REPORT]
        subprocess.Popen(open_cmd, env=env)
    else:
        logging.info("Allure报告生成失败，请检查allure命令行工具是否安装并加入环境变量！")
# # ===================================