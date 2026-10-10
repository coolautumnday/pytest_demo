import sqlite3
import time
import pytest


@pytest.mark.parametrize("new_name, new_age, uid", [('修改名字', 19, 1)])
def test_update_date(new_name, new_age, uid):
    with sqlite3.connect('../SQtest.db') as conn:
        cur = conn.cursor()
        sql = "UPDATE testcase SET name=?,age=?, create_time=? WHERE id=?"
        try:
            update_time= time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            cur.execute(sql, (new_name, new_age, update_time, uid))
            update_count = cur.rowcount
            print('修改成功，修改了{}条数据'.format(update_count))
        except Exception as e:
            print('修改出错，报错信息为{}'.format(e))

if __name__ == '__main__':
    test_update_date()
