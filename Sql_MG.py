import pymysql
import time
import getpass
db = ''
tab = ''
newstime = 0
runtime = time.perf_counter()


class SQLMG(object):

    def sql_write(self, wrt):
        global newstime
        newstime = newstime + 1
        cursor = db.cursor()                                                     #数据写入
        datatime_ = wrt['data'] + " " + wrt['time']
        sql = "INSERT INTO %s(日期,标题,内容,来源) VALUES ('%s', '%s', '%s', '%s' )" % (tab, datatime_, wrt['title'], wrt['text'], wrt['from_link'])
        try:
            cursor.execute(sql)
            db.commit()
        except:
            print("\r错误！请检查表名是否正确！")
            db.rollback()
        SQLMG().time_count()


    def time_count(self):
        endtime = time.perf_counter()
        print("\r已经抓取的消息数：%d,运行时间：" % newstime, end="")
        print("%0.2f s" % (endtime - runtime), end="")


    def get_title(self):
        cusr = db.cursor()
        sql = "SELECT 标题 FROM news order by 日期 DESC LIMIT 0,207"
        try:
            cusr.execute(sql)
            results = cusr.fetchall()
            return results
        except:
            print("\r历史标题读取错误!")


    def sql_login(self):
        global db, tab
        try:
            newsid = open("C:/Users/Public/Win/KXUser.ini", "r")
            ids = newsid.read().splitlines()
            if len(ids) == 0:
                ids = ['', '', '']
        except:
            ids = ['', '', '']
        while True:
            usrname = input("MYSQL用户名:" + ids[0] + "/")
            if usrname == "":
                usrname = ids[0]
            pswd = input("MYSQL密码:")
            try:
                db = pymysql.connect("localhost", usrname, pswd)
                print("\r登陆成功!")
                break
            except:
                print("\rMYSQL登陆失败！，请检查用户名或密码是否正确，或者MYSQL服务是否打开")
        while True:
            try:
                sqlku = input("请选择数据库:" + ids[1] + "/")
                if sqlku == "":
                    sqlku = ids[1]
                db = pymysql.connect("localhost", usrname, pswd, sqlku)
                tab = input("请选择要录入的表:" + ids[2] + "/")
                if tab == "":
                    tab = ids[2]
                break
            except:
                print("\r操作错误!")
        sqluser = open("C:/Users/Public/Win/KXUser.ini", "w")
        sqluser.write(usrname + "\n" + sqlku + "\n" + tab)