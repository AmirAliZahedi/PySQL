import mysql.connector 
from mysql.connector import Error
from prettytable import PrettyTable
import ast 
#--------------------------------------
blank=['default','',' ']
#--------------------------
def login():
    username=input('-username : ')
    if username in blank:
        username='system'
    if username=='admin':
        return {
    'host' : 'localhost',
    'user' : 'root',
    'password' : 'amiralimysql',
    'database' : 'mydb',
    'username' : 'admin'
    }
    password=input("-password : ")
    #---------------------------
    action=input("-setting :  ")
    if action=='professional':
        host=input("-host : ").lower()
        if host in blank:
            host='localhost'
        user=input("-user : ").lower()
        if user in blank:
            user='root'
    else:
        host='localhost'
        user='root'
    database=input("database : ")
    setting={
        'host' : host,
        'user' : user,
        'password' : password,
        'database' : database,
        'username' : username
    }
    return setting
#------------------------------------------

user=login()

def config(action=None):
    if action:
        setting={
            'host' : user['host'],
            'user' : user['user'],
            'password' : user['password'],
            'database' : action
        }
        return setting
    else:
        setting={
            'host' : user['host'],
            'user' : user['user'],
            'password' : user['password'],
            'database' : user['database']
        }
        return setting

def connect():
    global cnx
    setting=config()
    try:
        cnx = mysql.connector.connect(**setting)
        if cnx.is_connected():
            print('Connected')
            return cnx
    except Error as e : 
        print(f'Error : {e}')
        return None
    
def swich(database):
    global cnx
    setting=config(database)
    try:
        cnx = mysql.connector.connect(**setting)
        if cnx.is_connected():
            print('Connected')
    except Error as e : 
        print(f'Error : {e}')
        return None
#________________________________________________________________________________________________
def execute(cnx, query, data=None, fetch=False):
    try:
        with cnx.cursor() as cursor:
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            if query.strip().upper().startswith(('INSERT','UPDATE','DELETE','CREATE')):
                cnx.commit()
            if fetch:
                return cursor.fetchall()

    except Error as e:
        print(f"Error:(query)-{e}")
        cnx.rollback()

def lister_1(Data):
    list=[]
    data=[]
    for row in Data:
        data.append(row[0])
        list.append(data)
        data=[]
    return list
def lister_2(data):
    Data=[]
    list=[]
    for row in data:
        for i in row:
            Data.append(i)
        list.append(Data)
        Data=[]
    return list
def get_column_name(command,name):
    if command=='just-name':
        query=f"DESCRIBE {name}"
        list=execute(cnx,query,fetch=True)
        column=[]
        for row in list :
            column.append(row[0])
        return column
    elif command=='just-add':
        query=f"DESCRIBE {name}"
        list=execute(cnx,query,fetch=True)
        return list


class Database:
    def __init__(self,name):
        self.name=name
    def create(self):
        query=f"CREATE DATABASE IF NOT EXISTS {self.name}"
        execute(cnx,query)
        print(f'{self.name} Database Created.')
    def delete(self):
        query=f"DROP DATABASE IF EXISTS {self.name}"
        execute(cnx,query)
        print(f'{self.name} Database Deleted')
    @staticmethod
    def show():
        query="SHOW DATABASES"
        Databases=execute(cnx,query,fetch=True)
        if Databases:
            table=PrettyTable()
            table.field_names=['Databases']
            list=lister_1(Databases)
            for i in list:
                table.add_row(i)
            print(table)


def database(command,name):
    database=Database(name)
    if command=='create':
        database.create()
    if command=='delete':
        database.delete()
    if command=='show':
        database.show()

    
class Table:
    def __init__(self,name):
        self.name=name
    def select(self):
        query=f'SELECT*FROM {self.name}'
        Table=execute(cnx,query,fetch=True)
        list=lister_2(Table)
        table=PrettyTable()
        table.field_names=get_column_name('just-name',self.name)
        for i in list:
            table.add_row(i)
        print(table)
        @staticmethod
        def show():
            query="SHOW TABLES"
            Tables=execute(cnx,query,fetch=True)
            table=PrettyTable()
            table.field_names=['Tables']
            list=lister_1(Tables)
            for i in list:
                table.add_row(i)
            print(table)

    

