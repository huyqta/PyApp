__author__ = 'qtahuy'

import pymysql

# conn = pymysql.connect(host='localhost', user='root', passwd='', port=3306, db='dbtracking', charset='utf8')

# ###############################
# Insert new record to database#
# ###############################
class MainModel(object):
    def InsertDB(data, table):
        fields = ""
        values = ""
        for item in data.items():
            fields += "`" + item[0] + "`,"
            values += "'" + item[1] + "',"

        pos = len(fields)
        fields = fields[:pos - 1]

        pos = len(values)
        values = values[:pos - 1]

        MainModel.Execute("INSERT INTO `" + table + "`(" + fields + ") VALUES (" + values + ")")
        return "Success"


    # ###############################
    # Update new record to database#
    # ###############################
    def UpdateDB(data, table, id, value):
        fields = ""
        for item in data.items():
            fields += "`" + item[0] + "` = '" + item[1] + "',"

        pos = len(fields)
        fields = fields[:pos - 1]

        MainModel.Execute("UPDATE `" + table + "` SET " + fields + " WHERE `" + id + "` =  " + value)
        return "Success"


    # ###############################
    # Delete record from database  #
    # ###############################
    def DeleteDB(table, id, value):
        MainModel.Execute("DELETE FROM `" + table + "` WHERE `" + id + "`='" + value + "'")
        return "Success"


    def SelectDB(table):
        return MainModel.Execute("SELECT * FROM `" + table + "`")


    def SelectDBWhere(table, condition):
        return MainModel.Execute("SELECT * FROM `" + table + "` WHERE " + condition)


    # ###############################
    # Execute query                #
    # ###############################
    def Execute(query):
        try:
            conn = pymysql.connect(host='localhost', user='root', passwd='', port=3306, db='dbtracking', charset='utf8')
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()
            cur.close()
            conn.close()
            return cur.fetchall()
        except ValueError:
            return "Fail"