import os
import cx_Oracle
import random
def myCon():
    dsn = cx_Oracle.makedsn("systrade.iptime.org", 1521, service_name = "XE") # 오라클 주소
    connection = cx_Oracle.connect(user="indisystrade", password="sys123", dsn=dsn, encoding="UTF-8") # 오라클 접속
    return connection;

def test01(connection):
    cur = connection.cursor() # 실행 결과 데이터를 담을 메모리 객체
    for row in cur.execute("select * from lotto order by seq desc"):
        print(row)
def test02(connection):
    cur = connection.cursor()
    cur.execute("select * from lotto order by seq desc")
    while True:
        row = cur.fetchone()
        if row is None:
            break
        print(row)

def test03(connection):
    cur = connection.cursor()
    cur.execute("select * from lotto order by seq desc")
    num_rows = 10
    while True:
        rows = cur.fetchmany(num_rows)
        if not rows:
            break
        for row in rows:
            print(row)

def test04(connection):
    cur = connection.cursor()
    cur.execute("select * from (select * from lotto order by seq desc) A where rownum <=5")
    rows = cur.fetchall()   # 리턴한 객체를 한번에 리턴시킨다.
    for row in rows:
        print(row)

def insert( connection, seq, ball1, ball2, ball3, ball4, ball5, ball6, ball_bonus ):
    sql = ('insert into lotto(seq, ball1, ball2, ball3, ball4, ball5, ball6, ball_bonus) '
           'values(:seq, :ball1, :ball2, :ball3, :ball4, :ball5, :ball6, :ball_bonus)')

    try:
        with connection.cursor() as cursor:
            # execute the insert statement
            cursor.execute(sql, [seq, ball1, ball2, ball3, ball4, ball5, ball6, ball_bonus])
            # commit work
            connection.commit()
    except cx_Oracle.Error as error:
        print('Error occurred:')
        print(error)



LOCATION = r"C:\Users\jskim\PycharmProjects\instantclient_21_3"
os.environ["PATH"] = LOCATION + ";" + os.environ["PATH"] #환경변수 등록

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #insert(myCon(),1013, 21, 22, 26, 34, 36, 41, 32)
    #test04(myCon())
    #print("=============================#########################################3")
    arr = [21, 22, 26, 34, 36, 41, 32,
           5, 11, 18, 20, 35, 45, 3,
           1, 9, 12, 26, 35, 38, 42,
           9, 12, 15, 25, 34, 36, 3,
           15, 23, 29, 34, 40, 44, 20]
    for i in range(0, len(arr)):
        print(i, arr[i])

    for j in range(1, 6):
        random_number = random.randint(0, len(arr) - 1)
        ball1 = arr[random_number]
        random_number = random.randint(0, len(arr) - 1)
        ball2 = arr[random_number]
        random_number = random.randint(0, len(arr) - 1)
        ball3 = arr[random_number]
        print(j, ball1, ball2, ball3)
    #print_hi(os.environ["PATH"])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
