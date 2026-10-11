import sqlite3

def test_delete_data():
    with sqlite3.connect('./SQtest.db') as conn:
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM personnel where name have '修改’")
            delete_count = cur.rowcount
            print('删除成功，删除了{}条数据'.format(delete_count))
        except Exception as e:
            print('删除出错，报错信息为{}'.format(e))

if __name__ == '__main__':
    test_delete_data()