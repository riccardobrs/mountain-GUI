import mysql.connector as msql
import sys


class DataBase:

    __connection = None

    def __init__(self, db, user, psw, host="localhost"):

        self.db = db
        self.user = user
        self.psw = psw
        self.host = host
    
    def __connect(self):

        try:
            self.__connection = msql.connect(host=self.host,
                                             user=self.user,
                                             password=self.psw,
                                             database=self.db)
        except msql.Error as error:
            print(error)
            self.__connection = None
        
    def __disconnect(self):

        self.__connection.close()
        self.__connection = None
    
    def __execute(self, query, fetchall=False, commit=False):

        self.__connect()

        cursor = self.__connection.cursor()
        cursor.execute(query)
        if commit: self.__connection.commit()

        if fetchall: result = cursor
        
        cursor.close()
        self.__disconnect()

        if fetchall: return result
        else: return
    
    def connection_error(self):

        try:
            self.__connection = msql.connect(host=self.host,
                                             user=self.user,
                                             password=self.psw,
                                             database=self.db)
            self.__disconnect()
            return None

        except msql.errors.Error as error:
            self.__connection = None
            return error

    def select(self, table, condition, columns='*'):

        if columns == '*':
            cols = columns
        else:
            if type(columns).__name__ == 'str':
                columns_list = columns.split(',')
            elif type(columns).__name__ == 'list':
                columns_list = columns
            else:
                raise TypeError
            cols = "[" + "],[".join(columns_list) + "]"
        
        query = "SELECT {0} FROM [{1}] WHERE {2}".format(cols, table, condition)
        select_output = self.__execute(query, fetchall=True)

        return select_output
        
    def update(self, table, condition, key_val):

        fields = ''
        for key,val in key_val.items():
            fields += "[" + key + "]="
            if type(val).__name__ == 'str':
                fields += "'" + val + "'"
            else:
                fields += val
            fields += ","
        fields = fields.strip(',')

        query = "UPDATE [{0}] SET {1} WHERE {2}".format(table, fields, condition)
        self.__execute(query, commit=True)
    
    def insert(self, table, key_val):

        columns = "[" + "],[".join(key_val.keys()) + "]"
        values = "["
        for key,val in key_val.items():
            if type(val).__name__ == 'str':
                values += "'" + val + "'"
            else:
                values += val
            values += ","
        values = values.strip(',')

        query = "INSERT INTO [{0}] ({1}) VALUES ({2})".format(table, columns, values)
        self.__execute(query, commit=True)

    def delete(self, table, condition):

        query = "DELETE FROM [{0}] WHERE {1}".format(table, condition)
        self.__execute(query, commit=True)
