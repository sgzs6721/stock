#encoding: utf-8
import urllib2
import time
import datetime
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
        record['date']         = td[0].text.encode("utf8")
        record['num']           = td[1].a.text.encode("utf8")
        record['name']          = td[2].a.text.encode("utf8")
        record['dealprice']     = float(td[3].text.encode("utf8"))
        record['volume']        = float(td[4].text.encode("utf8"))
        record['volumemoney']   = td[5].text.encode("utf8")
        record['buy']           = td[6].text.encode("utf8")
        record['sell']          = td[7].text.encode("utf8")

        date = record['date']

        detail = ts.get_hist_data(record['num'], start=date)
        df = detail.iloc[::-1]
        # print df
        record['closeprice']  = float(df[u"close"][0])
        record['islimited']   = 0 if float(df[u"p_change"][0]) < 9.9 else 1
        record['discount']    = '%.2f' % ((record['dealprice'] - record['closeprice']) / record['closeprice'] * 100)
        record['dealrate']    = '%.2f' % (record['volume'] * 100 / float(df[u"volume"][0]))
        record['sameplace']   = 1 if record['buy'] == record['sell'] else 0

        startCaculate = 0
        for i in [1, 2, 5, 10, 15, 20] :

            info = getPreDetail(df, i)

            if info :
                if i == 1 : startCaculate = info['open']
                record['increase-' + str(i)] = getIncrease(startCaculate, info)
            else :
                record['increase-' + str(i)] = ''

        record['ontop'] = whetherOnTop(date)
        exit()

def getPreDetail(df, day) :
    price = {}

    if len(df) > day :
        for p in ["open", "close", "high", "low"] :
            if p == 'high':
                price[p] = max(float(x) for x in (df[p][1: day + 1]))
            elif p == 'low' :
                price[p] = min(float(x) for x in (df[p][1: day + 1]))
            else :
                price[p] = float(df[p][day])

    return price

def getIncrease(base, info) :

    closeIncrease = str('%.2f' % ((info['close'] - base) * 100 / base))
    highIncrease  = str('%.2f' % ((info['high']  - base) * 100 / base))
    lowIncrease   = str('%.2f' % ((info['low']   - base) * 100 / base))

    return ','.join([closeIncrease, highIncrease, lowIncrease])

def whetherOnTop(date) :
    url = topURL + date
    soup = getSoup(url)
    trArray = soup.findAll(id='dataTable')


def insertDB(info, table) :
    pass


bigURL = "http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/dzjy/index.phtml"
topURL = "http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/lhb/index.phtml?tradedate="
page = 20
while page < 21 :
    bigTradeInfo = getPageInfo(bigURL, 60, page)
    insertDB(bigTradeInfo, "bigtrade")
    page = page + 1
