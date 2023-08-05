# encoding=utf-8

# 导入SQLite驱动:
import sqlite3
import traceback
import os
import errno

'''
错误提示 database is locked
# SQLite 只支持库级锁
# 库级锁意味着同时只能允许一个写操作
# 出现此问题, 应将多余的写操作进程关闭
'''

class sqlite_wrapper(object):

    def __init__(self, conn_or_path, overwrite=False, isolation_level=''):  # isolation_level=None => autocommit_mode; isolation_level='' => a plain “BEGIN” statement
        if isinstance(conn_or_path, sqlite3.Connection):
            self.conn = conn_or_path
        elif isinstance(conn_or_path, str):
            if overwrite and os.path.exists(conn_or_path):
                try:
                    os.remove(conn_or_path)
                except OSError as e:
                    if e.errno != errno.ENOENT:
                        raise
            # 连接到SQLite数据库, 数据库文件是test.db; 如文件不存在，会自动在当前目录创建:
            self.conn = sqlite3.connect(conn_or_path, isolation_level=isolation_level) 
        else:
            raise TypeError("Unknown connection type %s" % type(conn_or_path))
        
        self.cur = self.conn.cursor()   # 创建一个Cursor:
        

    def create_table(self, ddl):
        try:
            self.cur.execute(ddl)   # 执行一条SQL_create语句，建表:
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            traceback.print_exc()
            return False


    def multi_independent_dmls(self, dmls, params_tuples):
        try:
            for dml,param_tuple in zip(dmls, params_tuples):
                self.cur.execute(dml, param_tuple)
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            traceback.print_exc()
            return False


    def dml(self, dml, params_tuple):     # insert / update / delete
        try:
            # cursor.execute('insert into user (id, name) values (\'1\', \'Michael\')')
            # sql_insert = '''
            #    INSERT INTO
            #      users(username, password, email)
            #    VALUES
            #      (?, ?, ?);
            # 下面写法会被 SQL 注入
            # sql = '''
            #    INSERT INTO
            #      users(username, password, email)
            #    VALUES
            #      ("{}", "{}", "{}")
            # '''.format('123', '345', 'a.com')
            # conn.execute(sql)
            # 参数拼接要用 ?, execute 中的参数传递必须是一个 tuple 类型
            self.cur.execute(dml, params_tuple)
            self.conn.commit()           # 必须用 commit 函数提交你的修改, 否则修改不会被写入数据库
            return self.cur              # 通过cur.rowcount获得插入的行数; cur.lastrowid获得最后插入行的主键ID  
        except:
            self.conn.rollback()
            traceback.print_exc()
            return None
            
            
    def select(self, dml, params_tuple):
        try:
            # cursor.execute('select * from user where id=?', ('1',)) 
            # 参数拼接要用 ?, execute 中的参数传递必须是一个 tuple 类型
            self.cur.execute(dml, params_tuple)
            # 获得查询结果集:
            col_name= [d[0] for d in self.cur.description]
            all_row = self.cur.fetchall()
            return [dict(zip(col_name, row)) for row in all_row]
            # return self.cur.fetchall()  # a list of tuples  --> [(u'1', u'Michael')]
        except:
            traceback.print_exc()
            return None
        
    
    def __del__(self):
        self.cur.close()
        self.conn.close()
        
        
if __name__=='__main__':

    sql_creates = [
        '''CREATE TABLE IF NOT EXISTS pods (
           id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
           podName VARCHAR(50), 
           type VARCHAR(20), 
           service VARCHAR(20), 
           status VARCHAR(40), 
           release VARCHAR(40), 
           customer VARCHAR(50), 
           datacenterCode VARCHAR(10), 
           dc_short_name VARCHAR(10), 
           fmDatacenter VARCHAR(60), 
           fusion_service_name VARCHAR(20), 
           physical_pod_name VARCHAR(40), 
           id_name VARCHAR(20), 
           associated_dr_peer VARCHAR(40), 
           lastUpdated DATETIME
        )''',
        '''CREATE TABLE IF NOT EXISTS hosts (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            systemType VARCHAR(10), 
            hostDom0 VARCHAR(80), 
            podHost VARCHAR(80), 
            podId INTEGER, 
            CONSTRAINT fk_pods FOREIGN KEY (podId) REFERENCES pods(id)
        )''',
        '''CREATE TABLE IF NOT EXISTS emAttributes (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            k VARCHAR(50), 
            v VARCHAR(200), 
            podId INTEGER, 
            CONSTRAINT fk_pods FOREIGN KEY (podId) REFERENCES pods(id)
        )''',
        '''CREATE TABLE IF NOT EXISTS podAttributes (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            k VARCHAR(50), 
            v VARCHAR(200), 
            podId INTEGER, 
            CONSTRAINT fk_pods FOREIGN KEY (podId) REFERENCES pods(id)
        )'''
    ]

    sql_mgr = sqlite_wrapper('test.db')
    for sql in sql_creates:
        sql_mgr.create_table(sql)
