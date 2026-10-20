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

def read_case_list(file_path, file_path_name):
    """
    读取case_list.txt，自动补全testcase路径，【优化：全局一次遍历构建文件名索引】
    返回元组 (case_list:list, file_exists:bool)
    支持输入：
        test_demo1                     # 只写文件名，自动递归整个testcase树查找
        test_demo1.py
        test_demo1.py::test_case
        subdir/test_demo1              # 显式写子目录路径，直接拼接
        .\testcase\test_demo1.py::xxx  # 绝对路径直接保留
    """
    import os

    cases = []
    file_exists = os.path.exists(file_path)
    if not file_exists:
        logging.info(f"{file_path} 文件不存在，执行全部用例")
        return cases, file_exists

    file_index = {}
    for dirpath, _, filenames in os.walk(file_path_name):
        for fname in filenames:
            if fname.endswith(".py"):
                fullpath = os.path.abspath(os.path.join(dirpath, fname))
                if fname not in file_index:
                    file_index[fname] = []
                file_index[fname].append(fullpath)

    with open(file_path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            # 跳过空行、注释行
            if not line or line.startswith("#"):
                continue

            # 分离 用例文件部分 和 ::用例函数部分
            if "::" in line:
                file_part, func_part = line.split("::", maxsplit=1)
            else:
                file_part = line
                func_part = None

            # 判断是否是绝对路径，如果是绝对路径不做补全
            if os.path.isabs(file_part):
                final_file = file_part
            else:
                # 判断用户输入是否自带目录分隔符 \ /
                has_dir_sep = ("\\" in file_part) or ("/" in file_part)

                if has_dir_sep:
                    # 用户显式写了子目录路径，沿用老逻辑直接拼接
                    if not file_part.endswith(".py"):
                        file_part = file_part + ".py"
                    final_file = os.path.join(file_path_name, file_part)
                else:
                    # 纯文件名，直接查预先建好的索引字典，不再walk磁盘
                    if not file_part.endswith(".py"):
                        search_name = file_part + ".py"
                    else:
                        search_name = file_part

                    found_list = file_index.get(search_name, [])
                    if len(found_list) == 0:
                        logging.warning(f"解析用例：{line} → 在 {file_path_name} 目录树未找到文件 {search_name}，跳过该用例")
                        continue
                    elif len(found_list) > 1:
                        logging.warning(f"解析用例：{line} → 找到多个同名文件 {found_list}，存在歧义，跳过该用例")
                        continue
                    else:
                        final_file = found_list[0]

            # 组装完整pytest用例路径
            if func_part is not None:
                full_case = f"{final_file}::{func_part}"
            else:
                full_case = final_file
            cases.append(full_case)
            logging.info(f"解析用例：{line} → {full_case}")

    if len(cases) == 0:
        logging.info(f"️{file_path} 文件存在，但是有效用例行为0！将执行testcase目录全部用例")
    return cases, file_exists



def create_read_index(report_path):
    filename = os.path.join(report_path, 'open_allure.bat')
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    bat_content = '''@echo off
    chcp 65001 >nul
    cd /d "%~dp0"
    allure open -h 127.0.0.1 -p 8083 allure-report
    pause
    '''
    with open(filename, 'w', encoding="gbk") as f:
        f.write(bat_content)
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
    return


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


def run_pytest(report_path, ALLURE_RESULTS, pytest_args: list, round_num: int) -> int:
    html_report = os.path.join(report_path, f"report_{round_num}.html")
    junit_xml = os.path.join(report_path, f"result_{round_num}.xml")
    logging.info('执行用例列表', pytest_args)
    cmd = [
              "pytest",
              "--report-path", report_path,  # 把报告根目录传给conftest
              "--log-cli-level", "INFO",
              "--log-cli-format", "%(asctime)s %(levelname)s %(name)s %(message)s",
              "--log-cli-date-format", "%Y-%m-%d %H:%M:%S",
              # "--clean-alluredir",
              "--html", html_report,
              "--junitxml", junit_xml,
              "--alluredir", ALLURE_RESULTS
          ] + pytest_args
    logging.info(f"========== 【第 {round_num} 轮测试开始】 ==========")
    logging.info(f"执行命令：{' '.join(cmd)}")
    logging.info(f"HTML报告：{html_report}")
    logging.info(f"JUnit文件：{junit_xml}")
    logging.info(f"Allure原始数据目录：{ALLURE_RESULTS}\n")
    try:
        result = subprocess.run(
            cmd,
            stdout=sys.stdout,
            stderr=sys.stderr,
            text=True
        )
        return result.returncode
    except Exception as e:
        logging.info(f"执行pytest异常：{e}")
        return 1


# # ===================================
# # 图片对比
import imagehash
from PIL import Image
from pathlib import Path


def get_phash(img_path: str | Path):
    """获取图片phash"""
    with Image.open(img_path) as img:
        # 转RGB，避免png透明通道报错
        if img.mode != "RGB":
            img = img.convert("RGB")
        return imagehash.phash(img)


def match_img(ele, act_path: str=None, dif: float = 8, exceptde:bool=True):
    """
    对比两张图片phash，返回汉明距离
    :param ele: 基准图片路径
    :param act_path: 实际截图路径，默认为'./tmp/ele_tmp.png'
    :param dif: 汉明距离结果 默认 hash_size=8，最大汉明距离 64。例如距离 0=100% 相似，距离 10≈84.37%
    :return: hamming distance
    """
    ele_path = Path(ele) if isinstance(ele, str) else ele.img_name

    actual_path = Path('./tmp/ele_tmp.png') if act_path is None else Path(act_path)
    if not os.path.exists(actual_path):
        return logging.info(f"需要对比图片不存在，请重新截图")
    hash_baseline = get_phash(ele_path)
    hash_actual = get_phash(actual_path)
    logging.info('两图对比值为{}'.format(hash_baseline - hash_actual))
    os.remove(actual_path)
    if exceptde:
        return hash_baseline - hash_actual <= dif
    else:
        return hash_baseline - hash_actual > dif

