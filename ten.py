#encoding: utf-8
import urllib2
import time
import re
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

def getPageInfo(url, page) :
    realURL = url + "&page=" + str(page)

    soup = getSoup(realURL)
    tbody = soup.find(attrs={'class':'datalist'}).table.tbody
    trArray = tbody.findAll("tr")
    numArray = tbody.findAll("script")

    # print trArray
    for index, tr in enumerate(trArray) :
        record = {}
        td = tr.findAll("td")
        record['person']        = td[0].text.encode("utf8")
        record['prediction']    = td[3].text.encode("utf8")
        record['num']           = numArray[index * 2 + 1].text.encode("utf8")[13:19]
        record['predict_time']  = td[5].text.encode("utf8")
        record['price']         = td[6].text.encode("utf8")
        record['success']       = td[9].text.encode("utf8")
        if record['success'] == '--' :
            record['success'] = '0'
        record['success_date']  = td[10].text.encode("utf8")


        dateAndTime = re.split('\s+', record['predict_time'])
        date = dateAndTime[0]
        time = dateAndTime[1].split(":")[0]

        if int(time) > 14 :
            date = str(datetime.datetime.strptime(date, "%Y-%m-%d").date() + datetime.timedelta(days=1))

        detail = ts.get_hist_data(record['num'], start=date)
        # print detail

        if detail.empty :
            continue
        df = detail.iloc[::-1]

        startCaculate = 0
        for i in range(0,21) :

            info = getPreDetail(df, i)
            # pprint(info)

            if info :
                if i == 0 : startCaculate = info['open']
                record['increase-' + str(i)] = getIncrease(startCaculate, info)
            else :
                record['increase-' + str(i)] = ''

        # pprint(record)
        insertDB(record, "ten")
        # exit()

def getPreDetail(df, day) :
    price = {}

    if len(df) > day :
        for p in ["open", "close", "high", "low"] :
            if p == 'high':
                price[p] = max(float(x) for x in (df[p][0: day + 1]))
            elif p == 'low' :
                price[p] = min(float(x) for x in (df[p][0: day + 1]))
            else :
                price[p] = float(df[p][day])

    return price

def getIncrease(base, info) :

    closeIncrease = str('%.2f' % ((info['close'] - base) * 100 / base))
    highIncrease  = str('%.2f' % ((info['high']  - base) * 100 / base))
    lowIncrease   = str('%.2f' % ((info['low']   - base) * 100 / base))

    return ','.join([closeIncrease, highIncrease, lowIncrease])

def insertDB(info, table) :
    print info['person'] + ":" + info['predict_time'] + ":" + info['prediction']
    cur = conn.cursor()
    statement = "insert into " + table + "(person,prediction,num,predict_time,success_date,price,success,increaseone,increasetwo,increasefive,increaseten," + \
        "increasefifteen,increasetwenty) VALUES('" + info['person'] + "','" + info['prediction'] + "','" + \
        info['num'] + "','" + info['predict_time'] + "','" + info['success_date'] + "','" + \
        info['price'] + "','" + info['success'] + "','" + info['increase-1'] + "','" + info['increase-2'] + "','" + \
        info['increase-5'] + "','" + info['increase-10'] + "','" + info['increase-15'] + "','" + \
        info['increase-20'] + "')"
    # print statement
    try :
        cur.execute(statement)
        cur.close()
        conn.commit()
    except MySQLdb.Error, e:
        print "\tMysql Error %d: %s" % (e.args[0], e.args[1])

host = "localhost"
user = "root"
passwd = "1qazxsw2"
port = 3306
database = "stock"

conn = MySQLdb.connect(host=host,user=user,passwd=passwd,db=database,port=port,charset='utf8')

tenURL = "http://www.178448.com/fjzt-1.html?view=archiver"
page = 53689

while page > 0 :
    print "page:" + str(page)
    getPageInfo(tenURL, page)
    page = page - 1
