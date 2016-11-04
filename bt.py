#encoding: utf-8
import urllib2
import time
from pprint import pprint
# from bs4 import BeautifulSoup
from BeautifulSoup import BeautifulSoup
import tushare as ts
import MySQLdb

def getSoup (url) :
    times = 0
    while times < 10 :
        try :
            req = urllib2.Request(url)
            res = urllib2.urlopen(req, timeout = 15).read()
            # return BeautifulSoup(res, "html.parser")
            return BeautifulSoup(res)

        except :
            print "Could not get soup from " + url
            print "Sleep 3 seconds and retrying ..."
            time.sleep(3)
            times = times + 1

    return ""

def getPageInfo(url, num, page) :
    realURL = url + "?num=" + str(num) + "&p=" + str(page)
    soup = getSoup(realURL)
    trArray = soup.find(id='dataTable').findAll("tr")[1:]
    record = {}
    for index, tr in enumerate(trArray) :
        td = tr.findAll("td")
        record['type']        = td[8].text.encode("utf8")[0]
        if record['type'] != 'A' :
            continue
        record['date']        = td[0].text.encode("utf8")
        record['num']         = td[1].a.text.encode("utf8")
        record['name']        = td[2].a.text.encode("utf8")
        record['dealprice']   = float(td[3].text.encode("utf8"))
        record['volume']      = float(td[4].text.encode("utf8"))
        record['volumemoney'] = td[5].text.encode("utf8")
        record['buy']         = td[6].text.encode("utf8")
        record['sell']        = td[7].text.encode("utf8")

        detail = ts.get_hist_data(record['num'], start=record['date'], end=record['date'])
        record['closeprice']  = float(detail[u"close"][0])
        record['islimited']   = 0 if float(detail[u"p_change"][0]) < 9.9 else 1
        record['discount']    = '%.2f' % ((record['dealprice'] - record['closeprice']) / record['closeprice'] * 100)
        record['dealrate']    = '%.2f' % (record['volume'] * 100 / float(detail[u"volume"][0]))
        record['sameplace']   = 1 if record['buy'] == record['sell'] else 0
        pprint(record)

def insertDB(info, table) :
    pass


bigURL = "http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/dzjy/index.phtml"
page = 1
while page < 2 :
    bigTradeInfo = getPageInfo(bigURL, 60, page)
    insertDB(bigTradeInfo, "bigtrade")
    page = page + 1
