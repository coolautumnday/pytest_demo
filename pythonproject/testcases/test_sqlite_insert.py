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

insert_data = {'personnel':[], 'subject' : [], 'class' : []}
subject_name = ['语文', '数学', '英语', '物理', '生物', '化学']
sql_ = ["""INSERT INTO personnel (id, name, age, sex, create_time) VALUES (?, ?, ?, ?, ?)""",
       """INSERT INTO score_subject (id, name, score, subject) VALUES (?, ?, ?, ?)""",
       """INSERT INTO class_name (id, name, class) VALUES (?, ?, ?)"""
       ]

for i in range(1000):
    uid = i + 1
    name = get_random_hanzi_str(3)
    age = random.randint(0, 59)
    sex = '男' if random.randint(0, 1) else '女'
    create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    insert_data['personnel'].append((uid, name, age, sex, create_time))

# print('asfdsa', insert_data)
for j in subject_name:
    for i in insert_data['personnel']:
        uid = i[0]
        name = i[1]
        score = random.randint(5, 100)
        subject = j
        insert_data['subject'].append((uid, name, score, subject))

for i in insert_data['personnel']:
    uid = i[0]
    name = i[1]
    class_id = random.randint(1, 10)
    insert_data['class'].append((uid, name, class_id))

# print(insert_data)
def test_insert_data():
    for x in range(3):
        sql = sql_[x]
        if 'personnel' in sql:
            data = insert_data['personnel']
        elif'subject' in sql:
            data = insert_data['subject']
        else:
            data = insert_data['class']
        try:
            with sqlite3.connect('./SQtest.db', timeout=10) as connet:
                con = connet.cursor()
                con.executemany(sql, data)
                connet.commit()
                print(f'插入表批量插入结果{con.rowcount}')
        except Exception as e:
            print('插入出错，报错信息为{}'.format(e))

if __name__ == "__main__":
    test_insert_data()