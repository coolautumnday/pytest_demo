import sqlite3
import random
import time

conn = sqlite3.connect('./SQtest.db')

c = conn.cursor()


def get_random_hanzi():
    # 0x4E00 一 ，0x9FA5 龥
    code = random.randint(0x4E00, 0x9FA5)
    return chr(code)


def get_random_hanzi_str(length=3):
    return "".join(get_random_hanzi() for _ in range(length))


def test_insert_date():
    test_insert_list = []
    for i in range(10):
        name = get_random_hanzi_str(3)
        age = random.randint(0, 59)
        sex = '男' if random.randint(0, 1) else '女'
        create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        test_insert_list.append((name, age, sex, create_time))
    # print('asdfdas', insert_list)
    sql = """INSERT INTO testcase (name, age, sex, create_time) VALUES (?, ?, ?, ?)"""

    try:
        with sqlite3.connect('./SQtest.db', timeout=10) as connet:
            con = connet.cursor()
            con.executemany(sql, test_insert_list)
            connet.commit()
            print(f'批量插入结果{con.rowcount}')
    except Exception as e:
        print('插入出错，报错信息为{}'.format(e))

if __name__ == "__main__":
    test_insert_date()