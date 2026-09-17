import pytest
import sys

# 第一轮：执行全部用例
print("=====第一轮：执行全部用例=====")
ret1 = pytest.main(["testcases/", "-v"])

# ret1 !=0 代表有用例失败，执行--lf重试
if ret1 != 0:
    print("\n=====第二轮：只重试失败用例=====")
    ret2 = pytest.main(["testcases/", "-v", "--lf"])
    sys.exit(ret2)
else:
    print("✅全部用例一次执行成功，无需重试")
    sys.exit(0)
