from KX import Sql_MG
from bs4 import BeautifulSoup
import re, json, urllib.request, urllib.parse, time, difflib
newstime = 0
news = []
newszz = 0


class HtmlParser(object):

    def _get_new_data(self, soup, mode, renewid):

        datadric = {}
        fid = ''
        #币世界快讯 http://www.bishijie.com/kuaixun/
        if mode == 1:
            all_node = soup.find_all("ul", id=re.compile("\d"))
            for node in all_node:
                newid = str(node.get('id'))
                if fid == '':
                    fid = newid
                if newid == renewid:
                    return fid
                datadric = {}
                tempdata = node.select("span")[0].parent.parent
                datadric["data"] = tempdata["class"][2]
                datadric["time"] = node.select("span")[0].text
                datadric["title"] = node.select("h2")[0].text
                datadric["text"] = node.select("div")[0].text.strip()
                if HtmlParser().cunt_parse(datadric['title']):
                    print("\r操作：已去除相似项")
                    continue
                lik = node.select("h2")[0].contents[0]['href']
                datadric['from_link'] = "http://www.bishijie.com" + lik
                Sql_MG.SQLMG().sql_write(datadric)

        #金色财经快讯 https://www.jinse.com/lives
        #json:https://api.jinse.com/v4/live/list?limit=20&reading=false
        if mode == 2:
            jscj = urllib.request.urlopen("https://api.jinse.com/v4/live/list?limit=20&reading=false")
            jscj = json.load(jscj)
            times = jscj['list']
            for jtime in times:
                all_node = jtime['lives']
                for node in all_node:
                    newid = str(node['id'])
                    if fid == '':
                        fid = newid
                    if newid == renewid:
                        return fid
                    datadric = {}
                    try:
                        tot = node['content']
                        ttime = node['created_at']
                        ttime = time.localtime(ttime)
                        datadric['data'] = time.strftime("%Y-%m-%d", ttime)
                        datadric['time'] = time.strftime("%H:%M", ttime)
                        datadric["title"] = re.search('\| (.+)】', tot)[1]
                        datadric["text"] = re.search('】(.+)', tot)[1]
                        if HtmlParser().cunt_parse(datadric['title']):
                            continue
                        datadric['from_link'] = node['link']
                    except:
                        continue
                    if datadric['from_link'] == '' or datadric == None:
                        datadric['from_link'] = "https://www.jinse.com/lives/" + str(node['id'])
                    Sql_MG.SQLMG().sql_write(datadric)

        #content 内容 title 标题
        if mode == 3:
            xckx = urllib.request.urlopen("https://api-prod.wallstreetcn.com/apiv1/content/lives?channel=xiaocong-channel&client=pc&cursor=&limit=50&first_page=false&accept_symbols=coin")
            xckx = json.load(xckx)
            all_node = xckx['data']['items']
            for node in all_node:
                newid = str(node['id'])
                if fid == '':
                    fid = newid
                if newid == renewid:
                    return fid
                datadric = {}
                ttime = node['display_time']
                ttime = time.localtime(ttime)
                datadric['data'] = time.strftime("%Y-%m-%d", ttime)
                datadric['time'] = time.strftime("%H:%M", ttime)
                if node['content'] == '' or node['content'] == None:
                    continue
                i = re.search(">(.+)<", node['content'])[1]
                i = re.sub('<a href[^>]*>', '', i)
                datadric['title'] = node['title']
                datadric['text'] = re.sub('</a>', '', i)
                if HtmlParser().cunt_parse(datadric['title']):
                    print("\r信息重复！")
                    continue
                datadric['from_link'] = node['global_more_uri']
                Sql_MG.SQLMG().sql_write(datadric)

        #鸵鸟区块链 http://www.tuoniaox.com/
        if mode == 4:
            all_node = soup.select(".con.bgc.line22.clearfix.news-flash")
            all_node = all_node[0].select('li')
            for node in all_node:
                datadric = {}
                nr = node.select('p')[0].text
                cont = re.search('】(.+)', nr)[1]
                yueri = re.search("鸵鸟区块链(.*?)月(.*?)日", cont)
                if yueri == None:
                    continue
                tuoniao = '鸵鸟区块链' + yueri[1] + '月' + yueri[2] + '日消息，'
                datadric['data'] =time.strftime("%Y-", time.localtime()) + yueri[1] + "-" + yueri[2]
                datadric['time'] = node.select('.time')[0].text
                newid = datadric['data'] + datadric['time']
                if fid == '':
                    fid = newid
                if newid == renewid:
                    return fid
                datadric['title'] = re.search('【(.+)】', nr)[1]
                datadric['text'] = cont.strip().strip(tuoniao)
                if HtmlParser().cunt_parse(datadric['title']):
                    print("\r信息重复！")
                    continue
                datadric['from_link'] = ''
                hrfs = node.select('a')
                for hrf in hrfs:
                    datadric['from_link'] = hrf['href']
                if datadric['from_link'] == '' or datadric['from_link'] == None:
                    datadric['from_link'] = "http://www.tuoniaox.com/"
                    Sql_MG.SQLMG().sql_write(datadric)

        #链得得快讯：http://www.chaindd.com/nictation
        if mode == 5:
            all_node = soup.find_all('li', id=re.compile('\d'))
            for node in all_node:
                #更新检测
                newid = str(node['id'])
                if fid == '':
                    fid = newid
                if newid == renewid:
                    return fid
                datadric = {}
                riqi = node.select('h2')[0].parent.parent.parent.select('.date')[0].select('time')[0].text.strip()
                riqi = re.sub(r'[年月]', '-', riqi)
                datadric['data'] = re.sub(r'日', '', riqi)
                datadric['time'] = node.select('.source')[0].text.strip()
                datadric['title'] = node.select('h2')[0].text
                #去重检测
                if HtmlParser().cunt_parse(datadric['title']):
                    print("\r操作：已去除相似项")
                    continue
                datadric['text'] = node.select('p')[0].text.strip()
                datadric['from_link'] = node.select('a')[0]['href']
                Sql_MG.SQLMG().sql_write(datadric)
        return fid

    #去重
    def cunt_parse(self, cunt):
        global newszz
        if len(news) == 0:
            news.append(cunt)
        for comp in news:
            xsd = difflib.SequenceMatcher(a=cunt, b=comp).ratio()
            if xsd >= 0.6:
                print("\r检测到\n%s\n和\n%s\n相似度：%0.2f" % (cunt, comp, xsd))
                return True
        if len(news) < 207:
            news.append(cunt)
        else:
            if newszz == 207:
                newszz = 0
            news[newszz] = cunt
            newszz = newszz + 1
        return False

    def get_news(self):
        rest = Sql_MG.SQLMG().get_title()
        for tit in rest:
            news.append(tit[0])


    def parse(self, html_cont, mode, renewid):
        soup = ""
        if mode == 1 or mode == 4 or mode == 5:
            soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        thenew = self._get_new_data(soup, mode, renewid)
        return thenew
