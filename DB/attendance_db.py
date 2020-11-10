import datetime

import MySQLdb


db_config = {
    'host': 'localhost',
    'db': 'attendance',  # Database Name
    'user': 'root',
    'passwd': '',
    'charset': 'utf8',
}

try:
    # 接続
    conn = MySQLdb.connect(host=db_config['host'], db=db_config['db'], user=db_config['user'],
                           passwd=db_config['passwd'], charset=db_config['charset'])
except MySQLdb.Error as ex:
    print('MySQL Error: ', ex)

# カーソルの取得
cursor = conn.cursor()

# table作成
# ログイン情報テーブル
cursor.execute(""" CREATE TABLE IF NOT EXISTS login_info(
    id INT AUTO_INCREMENT NOT NULL,
    set_login_name TEXT NOT NULL,
    set_password TEXT NOT NULL,
    PRIMARY KEY(id)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci """)

cursor.execute(""" CREATE TABLE IF NOT EXISTS attendance_db (
    id INT AUTO_INCREMENT NOT NULL,
    name TEXT NOT NULL,
    rate INT NOT NULL,
    attendance_data TEXT NOT NULL,
    time_now DATETIME NOT NULL,
    PRIMARY KEY(id)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci """)


def add_attendance_db(name, rate, attendance_data):
    if name and rate and attendance_data:
        # 出退勤情報を作成
        cursor.execute(
            """INSERT INTO attendance_db(name, rate, attendance_data, time_now)
                        VALUES (%s, %s, %s, %s)""",
            (name, rate, attendance_data, datetime.datetime.now()))
        conn.commit()
    else:
        raise('正しく読み込まれませんでした')


def get_infomation_attendance():
    # 辞書型のカーソルを取得
    dict_cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    # id の降順で50まで取得
    dict_cursor.execute("SELECT* from attendance_db ORDER BY id DESC")

    result = dict_cursor.fetchmany(size=50)
    return result
    