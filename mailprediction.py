 
import sqlite3
from sqlite3 import Error
import pandas as pd
import json
import numpy as np
import re
 
 
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        print("Connection success")
        return conn
    except Error as e:
        print(e)
 
    return None
 

def fetchAllEmails(jsonStr, prefix):
    list = json.loads(jsonStr)
    emails = ""
    if len(list) < 15:
        for i in range(len(list)):
            emails += " " + prefix+list[i]['e']
    return emails.replace(".com","")

def fetchnot_RepliedEmails(jsonStr,frommail, prefix):
    list = json.loads(jsonStr)
    emails = ""
    if len(list) < 15:
        for i in range(len(list)):
            emails += " " + prefix+list[i]['e']
        emails += " "+prefix+frommail
    return emails.replace(".com","")

def dump_sent_items(conn):
    # select_task_by_priority(conn,1)
    df = pd.read_sql_query("select ed.ccjson, e.tovalue from Emails e inner join EmailDetail ed on e.email_Id = ed.emailid inner join EmailToFolder ef on e.email_Id = ef.emailId where ef.folderid = 17", conn)
    plainToValues = []
    plainCCValues = []
    for index , row in df.iterrows():
       plainToValues.append(fetchAllEmails(row["ToValue"],"to"))
       plainCCValues.append(fetchAllEmails(row["CcJson"],"cc"))

    df["plaintovalue"] = plainToValues
    df["plainccvalue"] = plainCCValues
    df.drop(['CcJson','ToValue'], 1, inplace=True)
    df.to_csv('replied_new.txt', header=None, index=None, sep=',', mode='w')

def dump_no_replies(conn):
    query = "select ed.ccjson, e.tovalue, e.fromemail from Emails e "
    query += "inner join EmailDetail ed on e.email_Id = ed.emailid "
    query += "inner join EmailReference Ref on e.email_id = ref.emailId "
    query += "inner join EmailToGroup EG on EG.MessageId = Ref.Reference "
    query += "where   EG.groupid not in (select distinct groupid from EmailToGroup EG "
    query += "inner join EmailReference Ref on EG.MessageId = Ref.Reference "
    query += "inner join EmailToFolder EF  on EF.EmailId = Ref.EmailId where EF.folderid = 17) "
    df = pd.read_sql_query(query, conn)
    plainToValues = []
    plainCCValues = []
    for index , row in df.iterrows():
       plainToValues.append(fetchnot_RepliedEmails(row["ToValue"],row["FromEmail"], "to"))  
       # plainToValues.append(row["FromEmail"])
       plainCCValues.append(fetchAllEmails(row["CcJson"],"cc"))

    df["plaintovalue"] = plainToValues
    df["plainccvalue"] = plainCCValues
    df.drop(['CcJson','ToValue', 'FromEmail'], 1, inplace=True)
    df.to_csv('not_replied_new.txt', header=None, index=None, sep=',', mode='w')



 
def main():
    # value  = "adityaprasad@vmware.com"
    # replaced = re.sub('[@]*','',value)
    # print("Replaced value ", replaced)
    database = "taskbox.sqlite"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        dump_sent_items(conn)
        dump_no_replies(conn)
    conn.close()
 
 
if __name__ == '__main__':
    main()



 
# def select_all_tasks(conn):
#     """
#     Query all rows in the tasks table
#     :param conn: the Connection object
#     :return:
#     """
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM tasks")
 
#     rows = cur.fetchall()
 
#     for row in rows:
#         print(row)
 
 
# def select_task_by_priority(conn, priority):
#     """
#     Query tasks by priority
#     :param conn: the Connection object
#     :param priority:
#     :return:
#     """
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM Accounts")
 
#     rows = cur.fetchall()
 
#     for row in rows:
#         print(row)




    # main()


