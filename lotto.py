import os
import cx_Oracle
import random


def myCon():
    dsn = cx_Oracle.makedsn("localhost", 1521, service_name = "XE") # 오라클 주소
    connection = cx_Oracle.connect(user="systrade", password="sys123", dsn=dsn, encoding="UTF-8") # 오라클 접속
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


def saveFile(fileName, rows):
    f = open(f'{(fileName)}.txt','w')
    for row in rows:
        data = f'{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t{row[5]}\t{row[6]}\t{row[7]}\n'
        f.write(data)
    f.close()




def latest01_06(connection):
    cur = connection.cursor()
    cur.execute("select * from (select * from lotto order by seq desc) A where rownum <=6")
    rows = cur.fetchall()   # 리턴한 객체를 한번에 리턴 시킨다.
    latestSeq = rows[0][0]
    print(f'{latestSeq} => {latestSeq - 5}')
    saveFile(str(latestSeq), rows)

def readBallList(fileName):
    print(fileName)
    with open(fileName) as f:
        lines = f.readlines()
    return lines

def latest02_06(connection):
    cur = connection.cursor()
    cur.execute("select * from (select * from lotto order by seq desc) A where rownum >=2 and rownum <= 6")
    rows = cur.fetchall()   # 리턴한 객체를 한번에 리턴 시킨다.
    latestSeq = rows[0][0]
    print(f'{latestSeq} => {latestSeq - 5}')
    saveFile(str(latestSeq), rows)



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

def print_five_rows_include_Bonus_Ball(ballList):
    wholeArr1 = []
    for i in range(0, len(ballList)):
        ballArr = ballList[i].split('\t')
        wholeArr1.append(int(ballArr[0]))
        wholeArr1.append(int(ballArr[1]))
        wholeArr1.append(int(ballArr[2]))
        wholeArr1.append(int(ballArr[3]))
        wholeArr1.append(int(ballArr[4]))
        wholeArr1.append(int(ballArr[5]))
        wholeArr1.append(int(ballArr[6]))
    distinctArr1 = set(wholeArr1) #중복 제거
    print('최근5개 회차에 나온 숫자들',distinctArr1, '총 갯수 =', len(distinctArr1)) #list를 붙여서 set타입을 array로
    exceptArr1 = []
    for i in range(1, 45):
        if not (i in distinctArr1):
            exceptArr1.append(i)
    print('최근5개 회차에 안 나온 숫자들 =',exceptArr1)


def print_five_rows_exclude_Bonus_Ball(ballList):
    wholeArr1 = []
    for i in range(0, len(ballList)):
        ballArr = ballList[i].split('\t')
        wholeArr1.append(int(ballArr[0]))
        wholeArr1.append(int(ballArr[1]))
        wholeArr1.append(int(ballArr[2]))
        wholeArr1.append(int(ballArr[3]))
        wholeArr1.append(int(ballArr[4]))
        wholeArr1.append(int(ballArr[5]))
        #wholeArr1.append(int(ballArr[6]))
    distinctArr1 = set(wholeArr1) #중복 제거
    print('최근5개 회차에 나온 숫자들',distinctArr1, '총 갯수 =', len(distinctArr1)) #list를 붙여서 set타입을 array로
    exceptArr1 = []
    for i in range(1, 45):
        if not (i in distinctArr1):
            exceptArr1.append(i)

    print('최근5개 회차에 안 나온 숫자들 =',exceptArr1)
    return distinctArr1

def makeRandom(listArr):
    for i in range(0,5):
        ball1 = listArr[random.randrange(0, 4)]
        ball2 = listArr[random.randrange(5, 10)]
        ball3 = listArr[random.randrange(11, 15)]
        ball4 = listArr[random.randrange(16, 21)]
        print(ball1, ball2, ball3, ball4)

def makeAllCase(listArr):
    seq=1;
    dictionary = []
    for i in range(0, 5):
        for j in range(5, 10):
            for k in range(10, 15):
                for l in range(15, 21):
                    ball1 = listArr[i]
                    ball2 = listArr[j]
                    ball3 = listArr[k]
                    ball4 = listArr[l]
                    print(seq, ball1, ball2, ball3, ball4)
                    dictionary.append(f'{ball1}, {ball2}, {ball3}, {ball4}')
                    seq = seq + 1
    return seq - 1, dictionary


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #insert(myCon(),1018, 3, 19, 21, 25, 37, 45, 35)
    latest01_06(myCon())


    ballListPrev = readBallList('1017.txt')
    print(ballListPrev)
    poppedListPrev = ballListPrev.pop() #pop()은 리스트의 마지막 요소를 리스트에서 제거하고, 그 값을 리턴합니다
    #print("=============================<보너스볼 포함>#########################################")
    #print_five_rows_include_Bonus_Ball(ballList)
    #print("=============================#########################################")

    print("=============================<보너스볼 미포함>#########################################")
    excludeBonusBallArrPrev = print_five_rows_exclude_Bonus_Ball(ballListPrev)
    print("=============================#########################################")

    ballListNow = readBallList('1018.txt')
    print(ballListNow)
    poppedListNow = ballListNow.pop() #pop()은 리스트의 마지막 요소를 리스트에서 제거하고, 그 값을 리턴합니다
    print("=============================<보너스볼 미포함>#########################################")
    excludeBonusBallArrPrev = print_five_rows_exclude_Bonus_Ball(ballListNow)
    print("=============================#########################################")

    #listArr = list(excludeBonusBallArr) #set을 subscript로 접근하기 위하여 리스토로 변환
    #makeRandom(listArr)
    print("=============================#########################################")
    #countOfAllCase, dictList = makeAllCase(listArr)

    #interval = int(countOfAllCase/5)
    #print('총 갯수 = ', countOfAllCase, '5개를 뽑 을때 간격 = ', interval)
    #first = random.randrange(1, 150)
    #second = random.randrange(151, 300)
    #third = random.randrange(301, 450)
    #fourth = random.randrange(451, 600)
    #fifth = random.randrange(601, 750)

    #print(f'{first} 첫번째 = ', dictList[first])
    #print(f'{second} 두번째 = ', dictList[second])
    #print(f'{third} 세번째 = ', dictList[third])
    #print(f'{fourth} 네번째 = ', dictList[fourth])
    #print(f'{fifth} 다섯번째 = ', dictList[fifth])

    #print_hi(os.environ["PATH"])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
