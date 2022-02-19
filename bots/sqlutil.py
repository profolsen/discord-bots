import sqlite3
import os

def connect() :
    print(os.getenv('PROJECT_PATH') + '/data/database.db')
    return sqlite3.connect(os.getenv('PROJECT_PATH') + '/data/database.db')

def reset(conn) :
    conn.execute('drop table if exists entries;')
    conn.execute('create table entries (moment datetime DEFAULT (datetime(\'now\', \'localtime\')), category text);')

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

def reportnow(conn) :
    columns = conn.execute('''SELECT * FROM entries''').description
    summaryquery = 'SELECT ' + ", ".join(['SUM(' + x[0] + ')' for x in columns]) + ' FROM entries'
    print(summaryquery)
    wordcount = {}
    result = conn.execute(summaryquery)
    values = result.fetchall()
    i = 0
    for c in result.description :
        #print(c[0] + ' ' + str(values[0][i]))
        wordcount[c[0]] = values[0][i]
        i += 1
    return wordcount


