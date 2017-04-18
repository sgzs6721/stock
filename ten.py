#encoding: utf-8
import urllib2
import time
import re
import datetime
from pprint import pprint
from bs4 import BeautifulSoup
# from BeautifulSoup import BeautifulSoup
# import tushare as ts
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
    realURL = url + "page=" + str(page)

    soup = getSoup(realURL)
    tbody = soup.find(attrs={'class':'datalist'}).table.tbody
    trArray = tbody.findAll("tr")
    #numArray = tbody.findAll("script")

    trArray.reverse()

    for index, tr in enumerate(trArray) :
        record = {}
        td = tr.findAll("td")
        record['person']        = td[0].text.encode("utf8")
        record['name']          = td[3].text.encode("utf8")
        #record['code']          = numArray[index * 2 + 1].text.encode("utf8")[13:19]
        record['price']         = td[6].text.encode("utf8")
        record['success']       = td[9].text.encode("utf8")

        if record['success'] == '--' :
            record['success'] = '0'

        dateAndTime = re.split('\s+', td[5].text.encode("utf8"))
        record['pdate'] = dateAndTime[0]

        record['ptime'] = dateAndTime[1]
        record['sdate'] = td[10].text.encode("utf8")

        # pprint(record)
        insertNum = 0
        if not checkExistRecord(record, "ten") :
            print record['person'] + ":" + record['pdate'] + " " + record['ptime'] + ":" + record['name'] + " not existed,insert into db"
            insertNum = insertDB(record, "ten")
        else :
            print "existed"

    return insertNum


def checkExistRecord(record, table) :
    cur = conn.cursor()
    queryStatement = "select * from `" + table + "` where person = '" + record['person'] + "' AND name = '" + record['name'] + \
                     "' AND pdate = '" + record['pdate'] + "'"

    try :
        cur.execute(queryStatement)
        info = cur.fetchall()
        # pprint(info)
        if len(info) :
            return True
    except :
        print "select error!"
        exit(1)

    return False

def insertDB(info, table) :
    # print info['person'] + ":" + info['pdate'] + " " + info['ptime'] + ":" + info['name']

    cur = conn.cursor()

    insertStatement = "insert into " + table + "(person,name,price,pdate,ptime,success,sdate) VALUES(\"" + info['person'] + "\",'" + \
        info['name'] + "','" + info['price'] + "','" + info['pdate'] + "','" + info['ptime'] + "','" + info['success'] + "','" + \
        info['sdate'] + "')"

    statisticTable = "statistics"

    insert = "insert into `" + statisticTable + "` (person,num,success) VALUES(\"" + info['person'] + "\",'1','"

    personExist = checkExistPerson(info['person'], statisticTable)

    success = "0"
    if not info['success'] == '0':
        success = '1'

    if personExist :
        insert = "update `" + statisticTable + "` set num = num + 1,success = success + " + success + " where id = '" + str(personExist) + "'"
    else :
        insert = insert + success + "')"

    # return
    insertNum = 0
    try :
        insertNum = cur.execute(insertStatement)
        result = cur.execute(insert)
        print "update statistics:" + str(result) + " success:" + success
        cur.close()
        conn.commit()

    except MySQLdb.Error, e:
        print "\tMysql Error %d: %s" % (e.args[0], e.args[1])
        conn.rollback()

    return insertNum

def checkExistPerson(person, table) :
    checkStatement = "select * from `" + table + "` where person = \"" + person + "\""
    cur = conn.cursor()

    try:
        cur.execute(checkStatement)
        personInfo = cur.fetchall()
        cur.close()
        conn.commit()

    except MySQLdb.Error, e:
        print "\tCould not check whether the user is existed!"
        exit(1)

    result = 0
    if len(personInfo) :
        # pprint(personInfo)
        result = personInfo[0][0]

    return result


host = "localhost"
user = "root"
passwd = "1qazxsw2"
port = 3306
database = "stock"

conn = MySQLdb.connect(host=host,user=user,passwd=passwd,db=database,port=port,charset='utf8')

# tenURL = "http://www.178448.com/fjzt-1.html?view=archiver&"
tenURL = "http://www.178448.com/fjzt-1.html?"
page = 1

while page >= 1 :
    # print "page:" + str(page)
    insertNum = getPageInfo(tenURL, page)
    if True :
        if insertNum >15 :
            page = page + 1
            continue
        else :
            if page > 1 :
                page = page - 1
                continue
        print "sleep 100s"
        time.sleep(100)
    else :
        page = page - 1
    #exit()
