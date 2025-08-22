# PySQL 
#--------------------------------------
# libraries :
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
    'password' : 'password',
    'database' : 'db',
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
#_________________________________________________________________________________________________

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
#--------------------------------------------------------
def Database(command,name=None):
    if command=='create':
        query=f"CREATE DATABASE IF NOT EXISTS {name}"
        execute(cnx,query)
        print(f'{name} Database Created.')
    elif command=='delete':
        query=f"DROP DATABASE IF EXISTS {name}"
        execute(cnx,query)
        print(f'{name} Database Deleted')
    if command=='show':
        query="SHOW DATABASES"
        Databases=execute(cnx,query,fetch=True)
        if Databases:
            table=PrettyTable()
            table.field_names=['Databases']
            list=lister_1(Databases)
            for i in list:
                table.add_row(i)
            print(table)

        #------------------------------------------------
def Table_Show(command,name=None):
    #---------------------------------------------------
    if command=='select':
        query=f"SELECT*FROM {name} "
        Table=execute(cnx,query,fetch=True)
        list=lister_2(Table)
        table=PrettyTable()
        table.field_names=get_column_name('just-name',name)
        for i in list:
            table.add_row(i)
        print(table)
    #----------------------------------------------------
    if command=='show':
        query="SHOW TABLES"
        Tables=execute(cnx,query,fetch=True)
        table=PrettyTable()
        table.field_names=['Tables']
        list=lister_1(Tables)
        for i in list:
            table.add_row(i)
        print(table)
    if command=='column':
        column=name[1]
        table=name[0]
        query=f"SELECT {column} FROM {table} "
        Table=execute(cnx,query,fetch=True)
        table=PrettyTable()
        table.field_names=['ID',f"{column}"]
        list=lister_1(Table)
        for i,row in enumerate(list):
            table.add_row(row)
        print(table)


#Create Table -----------------------------------------------------
Numeric=['INT','TINYINT','SMALLINT','MEDIUMINT''BIGINT']
Float=['FLOAT','DECIMAL','NUMERIC','DOUBLE']
String=['VARCHAR','CHAR']
text=['TEXT','TINYTEXT','MEDIUMTEXT','LONGTEXT']
Time_date=['DATE','DATETIME','TIMESTAMP','TOME','YEAR']
Blob=['BLOB','TINYBLOB','MEDIUMBLOB','LONGBLOB'] 
def get_column_data():
    """get Column Data from User for create a column"""
    ColumnData={
    'NAME':'',
    'TYPE':'',
    'LENGHT':'',
    'AUTO_INCREMENT':False,
    'PRIMARY_KEY':False,
    'SIGNED':False,
    'Null':False,
    'DEFAULT':''
    }
    ColumnData['NAME']=input('Column name: ')
    ColumnData['TYPE']=input('Column type: ').upper()

    if ColumnData['TYPE'] in String:
        ColumnData['LENGHT']=int(input('Column lenght: '))
    Auto_Increment=input('AUTO_INCREMENT (on/off): ').upper()
    if Auto_Increment=='ON':
        ColumnData['AUTO_INCREMENT']=True
    else:
        pass
    Primary_key=input('PRIMARY_KEY (on/off): ').upper()
    if Primary_key=='ON':
        ColumnData['PRIMARY_KEY']=True
    else:
        pass
    Not_Null=input('NOT NULL (on/off): ').lower()
    if Not_Null=='ON':
        ColumnData['Null']=True
    else:
        pass
    ColumnData['DEFAULT']=input('DEFAULT :')
    return ColumnData
#----------------------------------------------------------
def column_query_maker():
    """Create Column Query"""
    ColumnData=get_column_data()
    query=[]
    name=ColumnData['NAME']
    query.append(name)
    type=ColumnData['TYPE']
    if type=='VARCHAR':
        lenght=ColumnData['LENGHT']
        char=f'{type}({lenght})'
        query.append(char)
    else:
        query.append(type)
    null=ColumnData['Null']
    if null:
        query.append('NOT NULL')
    default=ColumnData['DEFAULT']
    if default!='':
        if ColumnData['TYPE'] in String or text:
            query.append(f"DEFAULT '{default}'")
        else:
            query.append(f'DEFAULT {default}')
    if ColumnData['AUTO_INCREMENT']:
        query.append('AUTO_INCREMENT')
    if ColumnData['PRIMARY_KEY']:
        query.append('PRIMARY KEY')
    Query=" ".join(query)
    return Query
#---------------------------------------------------
def table_query_maker(name):
    querys=[]
    add=input('Enter for Column Data :').lower()
    while add!='end':
        query=column_query_maker()
        querys.append(query)
        add=input('Enter for Column Data :').lower()
    Create_Table=[f"CREATE TABLE {name} (\n"]
    for i in range(0,len(querys)):
        if i< len(querys)-1:
            Create_Table.append(querys[i]+",\n")
        else:
            Create_Table.append(querys[i]+"\n")
    Create_Table.append(")")
    Query=" ".join(Create_Table)
    return Query

def Table(command,name,rename=None):
    if command=='create':
        Query=table_query_maker(name)
        execute(cnx,Query)
        print('Table Created!')
    elif command=='delete':
        Table_Show('show')
        query=f"DROP TABLE {name}"
        sure=input('are you sure? :').lower()
        if sure=='yes':
            execute(cnx,query)
            print(f'{name} deleted')
    if command=='rename':
        query=f'RENAME TABLE {name} TO {rename}'
        execute(cnx,query)
        print('Table renamed')


# inputs : (col1 , col2 , col3 ,....)
# inputs : [ (data1) , (data2) , (data3) , ...]
def Add():
    #-------------------------------------------------
    Table_Show('show')
    name=input('Table name :')
    column_name=get_column_name('just-add',name)
    type_list=[]
    prin_list=[]
    percent=[]
    ID=[]
    for col in column_name:
        for part in col:
            if part=='auto_increment':
                data=(col[0],col[1],"auto_increment")
                Stri=f'({col[0]} : {col[1]} : AUTO )'
            else:
                data=(col[0],col[1])
                Stri=f'({col[0]} : {col[1]})'
        type_list.append(data)
        prin_list.append(Stri)
    print(f'Types : {prin_list}')
    #------------------------------------------------
    count=0
    for col in type_list:
        for part in col:
            if part=='auto_increment':
                count+=1
    for i in range(0,len(type_list)-count):
        percent.append('%s')
    Percent=",".join(percent)
    temp=[]
    for i,row in enumerate(type_list):
        for part in row:
            if part=='auto_increment':
                temp.append(i)
    for i in range(0,len(type_list)):
        if i not in temp:
            ID.append(type_list[i][0])
    Head=",".join(ID)
    #-------------------------------------------------
    Data=input('send your data : ')
    my_Data=ast.literal_eval(Data)
    #-------------------------------------------------
    query=f"INSERT INTO {name} ({Head}) VALUES ({Percent})"
    for row in my_Data :
        execute(cnx,query,row)
    print('saved')
    #-------------------------------------------------


def update(command,data):
    if command=='update':
        table=data[0]
        column=data[1]
        value=data[2]
        parameter=data[3]
        point=data[4]
        query=f"UPDATE {table} SET {column} = %s WHERE {parameter} = %s"
        execute(cnx,query,(value,point))
        print('updated')
    if command=='type':
        table=data[0]
        column=data[2]
        type=data[3]
        query=f"ALTER TABLE {table} MODIFY COLUMN {column} {type}"
        execute(cnx,query)
        print('updated')







help="""
for show Databases : show db
- - - - - - - - - - - - - - - -
for chenge Database : chenge db 
for create Database : create db 
for delete Database : delete db
- - - - - - - - - - - - - - - -
for create Table : create table
for delete Table : delete table
- - - - - - - - - - - - - - - -
for show tables : show tables
- - - - - - - - - - - - - - - - 
for add data : Add
for rename table : rename x to y
"""

def main(action):
    parts=list(action.split())
    if len(parts)>=1 :
        if parts[0]=='select':
            table=parts[1]
            Table_Show('select',table)
        if parts[0]=='create'and parts[1]=='db':
            database=parts[2]
            Database('create',database)
        if parts[0]=='delete'and parts[1]=='db':
            database=parts[2]
            Database('delete',database)
        if parts[0]=='use':
            database=parts[1]
            swich(database)
        if action=='show db':
            Database('show')
        if action=='show tables':
            Table_Show('show')
        if parts[0]=='create'and parts[1]=='table':
            table=parts[2]
            Table('create',table)
        if parts[0]=='delete'and parts[1]=='table':
            table=parts[2]
            Table('delete',table)
        if action=='add':
            Add()
        if parts[0]=='rename':
            name=parts[1]
            rename=parts[3]
            Table('rename',name,rename)
        if parts[0]=='get'and parts[2]=='column':
            name=parts[1]
            print(get_column_name('just-add',name))
        if parts[1]=='set' :
            table=parts[0]
            column=parts[2]
            value=parts[4]
            parameter=parts[6]
            point=parts[8]
            data=(table,column,value,parameter,point)
            update('update',data)
        if parts[1]=='update':
            table=parts[0]
            column=parts[2]
            type=parts[3]
            data=(table,column,type)
            update('type',data)
        if parts[0]=='list':
            data=(parts[3],parts[1])
            Table_Show('column',data)
            # show column in table



# 
cnx=connect()
action=input().lower()
while action!='close':
    main(action)
    action=input().lower()
cnx.close()

#table set column = x where name = y
# table update column  type
# list column in table










    


        
