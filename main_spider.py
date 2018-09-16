from typing import Any, Union, List
from KX import HTML_Parser, Sql_MG
import urllib.parse, urllib.request, time
toturl = ["http://www.bishijie.com/kuaixun/", 2, 3, "http://www.tuoniaox.com/", "http://www.chaindd.com/nictation"]
newid = []
db = ''
tab = ''
header = {'Connection': 'keep-alive',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',}



class SpiderMain(object):

    def main_spider(self):
        while True:
            mode = 0
            for ul in toturl:
                cont = ""
                mode = mode + 1
                if type('str') == type(ul):
                    try:
                        req = urllib.request.Request(ul, None, headers=header)
                        cont = urllib.request.urlopen(req)                        #读取网页
                    except:
                        print("\r网页读取错误！")
                        continue
                    cont = cont.read()
                thenew = newid[mode-1]
                thenew = HTML_Parser.HtmlParser().parse(cont, mode, thenew)
                newid[mode-1] = thenew
                if mode == 5:                                                    #保存更新信息
                    newsid = open("C:/Users/Public/Win/KXID.ini", "w")
                    for id in newid:
                        newsid.write(str(id))
                        newsid.write('\n')
                Sql_MG.SQLMG().time_count()

            #程序暂停
            slptime = 10
            for timslp in range(0, 10):
                Sql_MG.SQLMG().time_count()
                print(",程序将在%d秒后继续运行" % slptime, end="")
                slptime = slptime - 1
                time.sleep(1)
            Sql_MG.SQLMG().time_count()


if __name__ == "__main__":
    try:
        newsid = open("C:/Users/Public/Win/KXID.ini", "r")
        ids = newsid.read().splitlines()
        if len(ids) == 0:
            newid = ['0', '0', '0', '0', '0']
        else:
            for id in ids:
                newid.append(id)
        newsid.close()
    except:
        newid = ['0', '0', '0', '0', '0']

    Sql_MG.SQLMG().sql_login()
    HTML_Parser.HtmlParser().get_news()
    SpiderMain().main_spider()
