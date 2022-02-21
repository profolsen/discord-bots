import sqlite3
import os
from random import randint
from pathlib import Path


def connect(new) :
    i = 0
    while Path(os.getenv('PROJECT_PATH') + '/data/database' + str(i) + '.db').is_file() :
        i += 1
    i = 1 if not new and i == 0 else i
    if new :
        path = os.getenv('PROJECT_PATH') + '/data/database' + str(i) + '.db'
    else :
        path = os.getenv('PROJECT_PATH') + '/data/database' + str(i-1) + '.db'
    return sqlite3.connect(path)

def reset(conn) :
    conn.execute('drop table if exists entries;')
    conn.execute('create table entries (moment text DEFAULT (datetime(\'now\', \'localtime\')), category text);')
    conn.commit()
    conn.close()

def update(conn, category, words) :
    #first add new columns to table if necessary.
    oldcolumns = [x[0] for x in (conn.execute('''SELECT * FROM entries''').description)]
    valuepairs = []
    for word in words :
        print('1 ' + str(oldcolumns))
        if word.find('@') > -1 :
            valuepairs.append(word.split('@'))
        else :
            valuepairs.append([word, 'true'])
        lastpair = valuepairs[-1]
        print('2 ' + str(lastpair))
        if not lastpair[0] in oldcolumns :
            alterstatement = 'ALTER TABLE entries ADD ' + str(lastpair[0]) + ' INTEGER DEFAULT 0'
            oldcolumns.append(lastpair[0])
            print('3 ' + alterstatement)
            conn.execute(alterstatement)
    #construct the insert statement
    print(str(valuepairs))
    insertstatement = 'insert into entries(category ' + ', '\
                      + ", ".join([x[0] for x in valuepairs]) + ') '\
                      ' values (\'' + category + '\', '\
                      + ", ".join([x[1] for x in valuepairs]) + ')'
    print(insertstatement)
    conn.execute(insertstatement)
    conn.commit()
    conn.close()

def reportnow(conn) :
    columns = conn.execute('''SELECT * FROM entries''').description
    summaryquery = 'SELECT ' + ", ".join(['SUM(' + x[0] + ')' for x in columns]) + ' FROM entries'
    print(summaryquery)
    wordcount = {}
    result = conn.execute(summaryquery)
    values = result.fetchall()
    conn.commit()
    conn.close()
    i = 0
    for c in result.description :
        #print(c[0] + ' ' + str(values[0][i]))
        wordcount[c[0]] = values[0][i]
        i += 1
    return wordcount

def dailydata(conn, category, days, words) :
    fromclause = " FROM entries "
    whereclause = " WHERE moment > (SELECT DATETIME(\'now\', \'-" + str(days) + " day\')) AND category = \'" + category + "\' "
    groupbyclause = "GROUP BY DATE(moment)"
    if len(words) > 0 :
        selectclause = "SELECT date(moment) as moment, " + ", ".join([("round(avg(" + word + "), 3) as avg_" + word) for word in words]) + " "
    else :
        selectclause = "SELECT date(moment) as moment, COUNT(*) as " + category + " "
    query = selectclause + fromclause + whereclause + groupbyclause
    print(query)
    cursor = conn.execute(query)
    return cursortocsv(cursor)

#the time diff query:
#select diff, count(*) from (select *,
#       (strftime('%s', moment) - (select strftime('%s', max(i.moment)) from
#            entries i where strftime('%s',i.moment) < strftime('%s', entries.moment) and i.category = 'Z')) / (60*60) as diff
#        from entries where category = 'Y') x group by x.diff;

def timediff(conn, cause, effect) :
    query = " select diff, count(*) as frequency from (select *, " +\
        " (strftime('%s', moment) - (select strftime('%s', max(i.moment)) from " +\
        " entries i where strftime('%s',i.moment) < strftime('%s', entries.moment) and i.category = \'" + cause + "\')) / (60*60) as diff " +\
        " from entries where category = \'" + effect + "\') x group by x.diff"
    cursor = conn.execute(query)
    cursor = conn.execute(query)
    return cursortocsv(cursor)


#Utiltiy functions.  Now we are getting meta!!!

def cursortocsv(cursor) :
    rows = cursor.fetchall()
    columns = cursor.description
    header = ", ".join([column[0] for column in columns]) + "\n"
    data = "\n".join([(", ".join([str(value) for value in values])) for values in rows])
    return header + data;


############################################################
### FUNCTIONS TO SET UP TEST TABLE #########################
############################################################

def randompopulate(conn) :
    conn.execute('drop table if exists entries;')
    conn.execute('create table entries (moment text DEFAULT (datetime(\'now\', \'localtime\')), category text, ' +\
                 'a integer, b integer, c integer, d integer, e integer);')
    for i in range(0, 500) :
        category = randomchoice(['X', 'Y', 'Z'])
        word = randomchoice(['a', 'b', 'c', 'd', 'e'])
        insertstatement = "INSERT INTO entries(moment, category, " + word + ") VALUES ("
        insertstatement += "\'" + randomdatetime(2022, '02') + "\', \'" + category + "\', " + str(randint(1, 10)) + ")"
        print(insertstatement)
        conn.execute(insertstatement)
    conn.commit()
    conn.close()

def randomdatetime(year, month) :
    datetimestring = str(year) + "-" + str(month) + "-"
    datetimestring += str(randint(10, 28)) + " "
    datetimestring += str(randint(10, 23)) + ":" + str(randint(10, 59)) + ":" + str(randint(10, 59))
    return datetimestring

def randomchoice(categories) :
    return categories[randint(0, len(categories)-1)]


