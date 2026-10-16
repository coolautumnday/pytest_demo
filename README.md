## 项目简介
个人独立搭建的自动化测试框架 Demo，结合 AI 辅助开发。基于 Python+pytest，集成 Playwright Web UI 自动化、Appium 安卓移动端自动化、接口测试、Locust 接口压测、sqlite3 数据 CRUD、OCR 图文识别，Allure 生成可视化测试报告。

## 技术栈
pytest、Playwright、Appium、Locust、sqlite3、OCR、Allure、Python3

## 运行方式
一键执行测试并生成 Allure 报告
cd D:\gitdemo
python main.py
执行main.py后自动完成：

运行全部 pytest 测试用例
生成 allure-results 测试原始数据
构建 allure 静态报告到allure-report目录
在allure-report目录自动生成open_report.bat，双击即可一键打开 Allure 报告

## 功能模块
Playwright：Web 批量 UI 自动化测试
Appium：安卓移动端自动化测试
接口测试：本地接口校验
Locust：接口压力测试
sqlite3：测试数据增删改查
OCR：图片文本识别，返回文字与坐标信息

## 项目亮点
✅ 统一入口main.py，一键执行测试并构建 Allure 报告 
✅ 自动生成 bat 脚本，双击直接打开测试报告 
✅ pytest 一站式集成 Web/APP/ 接口 / 压测 / OCR / 数据库能力 
✅ AI 辅助完成 Demo 框架开发

## 作者说明
个人独立开发自动化测试 Demo 项目，用于自动化测试技术实践学习。