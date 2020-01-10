import pymysql
import time

from commonutils.settings import *
class MysqlUtil:
    def __init__(self,project,env,db):
        self.env=env
        self.db=db
        self.project=project
        self.mysql_connection=pymysql.connect(
                                                      host=SETTING[project][env]['MYSQL'][db]['host'],
                                                      user=SETTING[project][env]['MYSQL'][db]['user'],
                                                      password=SETTING[project][env]['MYSQL'][db][
                                                          'password'],
                                                      db=SETTING[project][env]['MYSQL'][db]['db'],
                                                      charset=SETTING[project][env]['MYSQL'][db]['charset'],
                                                      port=SETTING[project][env]['MYSQL'][db]['port'],
                                                      cursorclass=pymysql.cursors.DictCursor)
        self.mysql_cursor= self.mysql_connection.cursor()
        print (SETTING[project][env]['MYSQL'][db]['host'])

    def __del__(self):
        self.mysql_connection.close()
        self.mysql_cursor.close()

    def query_all(self,sql):
        cursor =self.mysql_cursor
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    def query_in_time(self,sql,num):
        cursor = self.mysql_cursor
        #cursor.execute(sql)
        #result = cursor.fetchall()
        for i in range(num):
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                return result
            else:
                time.sleep(3)
                continue
        return None

if __name__=='__main__':
    mysql_util = MysqlUtil('ach_envconfig', 'T1', "userlevel_achv_xq")
