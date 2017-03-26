#encoding: utf-8
import urllib2
import time
import datetime
from pprint import pprint
from bs4 import BeautifulSoup
# from BeautifulSoup import BeautifulSoup
import tushare as ts
import MySQLdb

def getSoup (url) :
    times = 0
    while times < 10 :
        try :
            req = urllib2.Request(url)
            res = urllib2.urlopen(req, timeout = 15).read()
            return BeautifulSoup(res, "html.parser")
            # return BeautifulSoup(res,fromEncoding="gb18030")

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
    if len(trArray) == 0 :
        exit("Last Page")
    for tr in trArray :
        record = {}
        td = tr.findAll("td")
        record['type']        = td[8].text.encode("utf8")[0]
        if record['type'] != 'A' :
            continue
        record['date']          = td[0].text.encode("utf8")
        record['num']           = td[1].a.text.encode("utf8").strip()
        record['name']          = td[2].a.text.encode("utf8")
        record['dealprice']     = td[3].text.encode("utf8")
        record['volume']        = td[4].text.encode("utf8")
        record['volumemoney']   = td[5].text.encode("utf8")
        record['buy']           = td[6].text.encode("utf8").strip()
        record['sell']          = td[7].text.encode("utf8").strip()

        date = record['date']


        detail = ts.get_hist_data(record['num'], start=date)
        # print detail
        try :
            df = detail.iloc[::-1]
        except:
            continue
        # print df
        record['closeprice']  = str(df[u"close"][0])
        record['islimited']   = '0' if float(df[u"p_change"][0]) < 9.85 else '1'
        record['discount']    = '%.2f' % ((float(record['dealprice']) - float(record['closeprice'])) / float(record['closeprice']) * 100)
        record['dealrate']    = '%.2f' % (float(record['volume']) * 100 / float(df[u"volume"][0]))
        record['sameplace']   = '1' if record['buy'] == record['sell'] else '0'

        startCaculate = 0
        for i in [1, 2, 5, 10, 15, 20] :

            info = getPreDetail(df, i)

            if info :
                if i == 1 : startCaculate = info['open']
                record['increase-' + str(i)] = getIncrease(startCaculate, info)
            else :
                record['increase-' + str(i)] = ''

        [record['ontop'], record['toptype']] = whetherOnTop(date, record['num'])

        insertDB(record, "bigtrade")
        # pprint('record')

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

def whetherOnTop(date, num) :
    url = topURL + date
    soup = getSoup(url)
    tables = soup.findAll(id='dataTable')

    for index, table in enumerate(tables) :
        trs = table.findAll('tr',attrs = {'class':'head'})

        for tr in trs[2:] :
            td = tr.findAll('td')[1].text.encode("utf8")
            if td == num :
                topType = trs[0].td.span.text.encode("utf8")
                return ['1', topType]
    return ['0', '']


def insertDB(info, table) :
    print info['date'] + ":" + info['name'] + ":" + info['num'] + "***"
    cur = conn.cursor()
    statement = "insert into " + table + "(date,num,name,dealprice,closeprice,islimited,discount," + \
        "volume,volumemoney,dealrate,buy,sell,sameplace,increaseone,increasetwo,increasefive,increaseten," + \
        "increasefifteen,increasetwenty,ontop,toptype) VALUES('" + info['date'] + "','" + info['num'] + "','" + \
        info['name'] + "','" + info['dealprice'] + "','" + info['closeprice'] + "','" + \
        info['islimited'] + "','" + info['discount'] + "','" + info['volume'] + "','" + \
        info['volumemoney'] + "','" + info['dealrate'] + "','" + info['buy'] + "','" + \
        info['sell'] + "','" + info['sameplace'] + "','" + info['increase-1'] + "','" + info['increase-2'] + "','" + \
        info['increase-5'] + "','" + info['increase-10'] + "','" + info['increase-15'] + "','" + \
        info['increase-20'] + "','" + info['ontop'] + "','" + info['toptype'] + "')"
    try :
        cur.execute(statement)
        cur.close()
        conn.commit()
    except MySQLdb.Error, e:
        print "\tMysql Error %d: %s" % (e.args[0], e.args[1])
        # print "Update last record..."
        statement = "update " + table + " set volume=volume + '" + info['volume'] + \
                    "',volumemoney=volumemoney + '" + info['volumemoney'] + "',dealrate=dealrate +'" + \
                    info['dealrate'] + "' where date='"+ info['date'] +"' and dealprice='" + info['dealprice'] + "' and num='"\
                    + info['num'] + "' and buy='" + info['buy'] + "' and sell='" + info['sell'] + "'"
        print statement
        cur.execute(statement)
        cur.close()
        conn.commit()
        pass

host = "localhost"
user = "root"
passwd = "1qazxsw2"
port = 3306
database = "stock"

conn = MySQLdb.connect(host=host,user=user,passwd=passwd,db=database,port=port,charset='utf8')

bigURL = "http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/dzjy/index.phtml"
topURL = "http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/lhb/index.phtml?tradedate="
page = 1156

while page > 0 :
    print "page:" + str(page)
    getPageInfo(bigURL, 60, page)
    page = page - 1
