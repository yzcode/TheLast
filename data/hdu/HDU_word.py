# -*- coding: utf-8 -*-

import MySQLdb
import json
import time


mysql_con = None


def logging(msg, lv):
    ISOTIMEFORMAT = "%Y-%m-%d %X"
    logtime = time.strftime(ISOTIMEFORMAT, time.localtime())
    lvstr = ["MASSAGE", "WARNING", "ERROR  "]
    print lvstr[lv], logtime, ":", msg


def generate():
    logging("Start generating the test file!", 0)
    logging("Fetching Username in the Database!", 0)
    sql_cur = mysql_con.cursor()
    user_sql = "SELECT user,count(User) as subs FROM OJ_data.hdu_data group by User order by subs desc"
    sql_cur.execute(user_sql)
    user_list = []
    for record in sql_cur.fetchall():
        if record[0].find("judge") == -1 and record[0].find("nlgxh") == -1 and record[0].find("oj") == -1 and record[0].find("vj") == -1 and record[0].find("test") == -1:
            user_list.append(record[0])
    logging("Fetching Username in the Database finished!", 0)
    logging("Fetching records in the Database", 0)
    status_sql = "SELECT Problem FROM OJ_data.hdu_data where user = '%s' and result != 'Compilation Error';"
    test_data = []
    for username in user_list:
        if len(test_data) == len(user_list) * 0.75:
            logging("Fetching records 75%", 0)
        elif len(test_data) == len(user_list) * 0.5:
            logging("Fetching records 50%", 0)
        elif len(test_data) == len(user_list) * 0.25:
            logging("Fetching records 25%", 0)
        user_record = []
        sql_cur.execute(status_sql % username)
        for status in sql_cur.fetchall():
            if len(user_record) == 0 or user_record[-1] != int(status[0]):
                user_record.append(int(status[0]))
        test_data.append({
            "user": username,
            "status": user_record,
        })
    logging("Fetching records in the Database finished!", 0)
    logging("There will be %d users in the test file" % len(test_data), 0)
    logging("Start writing to the file", 0)
    test_file = open("./hdu_word.txt", "w")
    for test_record in test_data:
        for status in test_record["status"]:
            test_file.write("%d " % status)
        test_file.write("\n")
    test_file.flush()
    logging("Finish writing to the file", 0)
    logging("Finish generating the test file!", 0)


def vaild(fname):
    logging("Vaild start!", 0)
    out_file = open(fname, "r")
    std_file = open("./testfile.out", "r")
    count = int(std_file.readline())
    hit = 0
    amt_out = 0
    amt_std = 0
    for i in range(0, count):
        out_info = out_file.readline().split(" ")
        out_cnt = int(out_info[1])
        amt_out += out_cnt
        std_info = std_file.readline().split(" ")
        std_cnt = int(std_info[1])
        amt_std += std_cnt
        out_sta = map(int, filter(lambda x: len(x) > 1, out_file.readline().split(" ")))
        std_sta = map(int, filter(lambda x: len(x) > 1, std_file.readline().split(" ")))
        for sta in out_sta:
            if sta in std_sta:
                hit += 1
    P = hit * 1.0 / amt_out
    R = hit * 1.0 / amt_std
    F1 = 2 * P * R / (P + R)
    print ("Pre: %f, Rec: %f, F1: %f" % (P, R, F1))
    logging("Vaild finish!", 0)


def main():
    while True:
        print "(1)Generate Test File"
        print "(2)Vaild F1"
        print "(3)Generate Raw File"
        print "(0)Quit"
        option = int(input())
        if option == 1:
            generate()
        elif option == 0:
            break
        else:
            continue
    pass


if __name__ == '__main__':
    logging("Word start!", 0)
    mysql_con = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="199528",
        db="OJ_data",
        charset="utf8"
    )
    main()
    mysql_con.close()
    logging("Word finished!", 0)