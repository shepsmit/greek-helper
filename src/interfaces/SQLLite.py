import sqlite3
import re


def regexp(expr, item):
    try:
        reg = re.compile(expr)
        return reg.search(item) is not None
    except Exception as e:
        print(e)

class SQL_Database:
    def __init__(self,db_file):

        self.db_path = db_file
        try:
            self.con = sqlite3.connect(self.db_path)
            self.con.create_function("REGEXP", 2, regexp)
            self.cur = self.con.cursor()
        except Exception as e:
            print(e)

    def close(self):
        self.con.close()

    def run_query(self,query):
        res = self.cur.execute(query).fetchall()
        return res
    
    def run_query_params(self,query:str ,params:list)->list:
        if isinstance(params, list):
            res = self.cur.execute(query,tuple(params)).fetchall()
            return res
        else:
            print("SQLLITE: RUn Query Params param error")
            return ["DB_QUERY_PARAM_ERROR"]
    
    def _execute_statement(self, statement):
        self.cur.execute(statement)
        self.con.commit()

    def create_table(self, table_info):
        s = "CREATE TABLE {0}".format(table_info)
        self._execute_statement(s)
    
    def insert_table(self, table_info, params):
        param_s = "?,"*len(params)
        param_s = param_s[:-1] # get rid of the trailing comma

        s = "INSERT INTO {0} VALUES({1})".format(table_info, param_s)
        self.cur.execute(s, tuple(params))
        self.con.commit()
    
    def update_table(self, table, column, data, where_col="", where_cond=""):

        s = "UPDATE {0} SET {1}=?".format(table, column)
        
        if(where_col != ""):
            s += " WHERE {0} =?".format(where_col)
            params = (data,where_cond)
        else:
            params = (data,)

        self.cur.execute(s,params)
        self.con.commit()