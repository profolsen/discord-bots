import sqlite3
import os
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


