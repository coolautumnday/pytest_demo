import sqlite3

def test_get_all_data():
    with sqlite3.connect('./SQtest.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM personnel")
        res = cur.fetchall()
        # print(res)
        for r in res:
            print(r)

if __name__ == '__main__':
    test_get_all_data()
