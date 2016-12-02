#encoding: utf-8
import urllib2
import time
import re
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
            return BeautifulSoup(res,fromEncoding="gb18030")

        except :
            print "Could not get soup from " + url
            print "Sleep 3 seconds and retrying ..."
            time.sleep(3)
            times = times + 1

    return ""

def getPageInfo(url, page) :
    realURL = url + "?page=" + str(page)
    soup = getSoup(realURL)
    trArray = soup.find(attrs={'class':'datalist'}).table.tbody.findAll("tr")
    print trArray
    for tr in trArray :
        record = {}
        td = tr.findAll("td")
        record['person']        = td[0].text.encode("utf8")
        record['prediction']    = td[3].text.encode("utf8")
        record['predict_time']  = td[5].text.encode("utf8")
        record['price']         = td[6].text.encode("utf8")
        record['success']       = td[9].text.encode("utf8")
        record['success_date']  = td[10].text.encode("utf8")


        dateAndTime = re.split('\s+', record['predict_time'])
        print dateAndTime
        date = dateAndTime[0]
        time = dateAndTime[1]
        pprint(record)
        print date
        print time
        exit()


        detail = ts.get_hist_data(record['num'], start=date)
        df = detail.iloc[::-1]

        startCaculate = 0
        for i in [1, 2, 5, 10, 15, 20] :

            info = getPreDetail(df, i)

            if info :
                if i == 1 : startCaculate = info['open']
                record['increase-' + str(i)] = getIncrease(startCaculate, info)
            else :
                record['increase-' + str(i)] = ''

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

def insertDB(info, table) :
    print info['date'] + ":" + info['name']
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
        print "Update last record..."
        volume = float(info['volume']) * 2
        volumemoney = float(info['volumemoney']) * 2
        dealrate = float(info['dealrate']) * 2
        statement = "update " + table + " set volume='" + str(volume) + \
                    "',volumemoney='" + str(volumemoney) + "',dealrate='" + \
                    str(dealrate) + "' where dealprice='" + info['dealprice'] + "' and num='" + info['num'] + "' and volume='" + \
                    info['volume'] + "' and buy='" + info['buy'] + "' and sell='" + info['sell'] + "'"
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

tenURL = "http://www.178448.com/fjzt-1.html"
page = 1

while page > 0 :
    print "page:" + str(page)
    getPageInfo(tenURL, page)
    page = page + 1
