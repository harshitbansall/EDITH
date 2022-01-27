import os,sqlite3
from prettytable import PrettyTable

######################################################################################################################################
def selectTable(*args):
    global tableName
    tableList = [x[0] for x in mainDB.execute("SELECT name FROM sqlite_master WHERE type=\"table\"").fetchall()]
    if len(args)==1:
        query = args[0]
        table = query.split()[query.split().index("table")+1]
        if table in tableList:
            return table
        elif table.title() in tableList:
            return table.title()
        else:
            return ("No Table Named {}.".format(table))
    else:
        x = PrettyTable()
        x.field_names = ['No','Name']
        for num,k in enumerate(tableList):
            x.add_row([num+1,k])
        print(x)
        return tableList[int(input("Select Table: ".title()))-1]
######################################################################################################################################
def deleteColumn(tableName,columnDrop):
    columnList = [description[0] for description in mainDB.execute("select * from {}".format(tableName)).description]
    columnList.remove(columnDrop)
    mainDB.execute("CREATE TABLE new{0} AS SELECT {1} FROM {0}".format(tableName,", ".join(columnList)))
    mainDB.execute("DROP TABLE {}".format(tableName))
    mainDB.execute("ALTER TABLE new{0} RENAME TO {0}".format(tableName)),mainDB.commit()


##    data=mainDB.execute("SELECT * from Contacts ORDER BY fullname").fetchall()
##    mainDB.execute("""CREATE TABLE Ordered (sNum,fname,lname,fullname,bday,gender,pnumber1,pnumber2,nname,address,email)""")
##    for i in data:
##        i=list(i)
##        i[0]=data.index(tuple(i))+1
##        mainDB.execute("INSERT INTO Ordered (sNum,fname,lname,fullname,bday,gender,pnumber1,pnumber2,nname,address,email) VALUES {}".format(tuple(i)))
##    mainDB.commit()
##    mainDB.execute("DROP table Contacts")
##    mainDB.execute("ALTER TABLE Ordered RENAME TO Contacts"),mainDB.commit()

def dbHandle(tableName,query):
    if query=="show columns":
        print(tableName+": "+", ".join([description[0] for description in mainDB.execute("select * from {}".format(tableName)).description]))
    elif query=="add column":
        print(tableName+": "+", ".join([description[0] for description in mainDB.execute("select * from {}".format(tableName)).description]))
        mainDB.execute("alter table {} add column {}".format(tableName,input("Enter Name of the New Column: "))),mainDB.commit()
    elif query=="delete table":
        mainDB.execute("DROP table {}".format(selectTable())),mainDB.commit()
    elif query=="show entries" or query=="se":
        for k in mainDB.execute("select * from {}".format(tableName)).fetchall():print(k)
    elif query=="add entry":
        rawColumns=[description[0] for description in mainDB.execute("select * from {}".format(tableName)).description]
        columns,values=", ".join(rawColumns),[]
        for i in rawColumns:
            if i=="sNum":
                if mainDB.execute("SELECT max(rowid) from {}".format(tableName)).fetchone()[0] is None:
                    values+=['1']
                else:values+=['{}'.format(str(mainDB.execute("SELECT max(rowid) from {}".format(tableName)).fetchone()[0]+1))]
            else:
                values+=["'{}'".format(input("Value for {}: ".format(i)).replace("\\n","\n").replace("'","\""))]
        mainDB.execute('''insert into {} ({}) values ({})'''.format(tableName,columns,", ".join(values))),mainDB.commit()
    elif "delete" in query:
        if "column" in query:
            dbHandle(tableName,"show columns")
            deleteColumn(tableName,input("Which Column Should I Delete?: "))
        else:
            for k in mainDB.execute("select * from {}".format(tableName)).fetchall():print(k)
            mainDB.execute("Delete from {} where sNum = {}".format(tableName,input("Which Entry Do You Want To Delete ?: "))),mainDB.commit()
    elif "edit" in query or "ee"==query:
        for k in mainDB.execute("select * from {}".format(tableName)).fetchall():print(k)
        editList=mainDB.execute("select * from {} where sNum = {}".format(tableName,input("Which Entry Do You Want To Edit ?: "))).fetchall()[0]
        columns=[description[0] for description in mainDB.execute("select * from {}".format(tableName)).description]
        for i in columns:
            if i!="sNum":
                newVal=input("{} '{}': ".format(i.title(),editList[columns.index(i)]))
                if newVal!="":
                    mainDB.execute("Update {} set {} = '{}' where sNum= {}".format(tableName,i,newVal,editList[0])),mainDB.commit()
                else:continue
######################################################################################################################################
def maindbHandle(query):
    global mainDB,databaseInUse,tableName
    if query=="new table" or query=="add table":
        colList,nameNew = [],input("Enter Name of New Table: ")
        for i in range(int(input("Enter Number of Columns: "))):colList+=["{}".format(input("Enter Name of Column {} followed by Datatype: ".format(i+1)))]
        mainDB.execute("create table {} ({})".format(nameNew,", ".join(colList))),mainDB.commit()
    elif query=="show tables":print(", ".join([x[0] for x in mainDB.execute("SELECT name FROM sqlite_master WHERE type=\"table\"").fetchall()]))
    elif query=="change table" or query=="ct": 
        tableName = selectTable()
    elif query=="change database" or query=="cd":
        databaseList = [k for k in os.listdir(startupPath+"/Data") if ".db" in k]
        x = PrettyTable()
        x.field_names = ['No','Database']
        for num,k in enumerate(databaseList):
            x.add_row([num+1,k])
        print(x)
        mainDB = sqlite3.connect("C:/Users/Tania/Desktop/Harshit/EDITH/Data/mainDB.db")
        databaseInUse = databaseList[int(input("Select Database: "))-1]
        tableName = ""
        mainDB.execute("update Variables set Value = '\"{}\"' where Variable = 'databaseInUse'".format(databaseInUse)),mainDB.commit()
        mainDB = sqlite3.connect("C:/Users/Tania/Desktop/Harshit/EDITH/Data/{}".format(databaseInUse))
    else:
        if "table " in query:
            tableName = selectTable(query)
            if "No Table" in tableName:
                print(tableName)
            else:dbHandle(tableName,query)
        if tableName == "":
            tableName = selectTable()
            dbHandle(tableName,query)
        else:dbHandle(tableName,query)
######################################################################################################################################
if __name__=="__main__":
    print("Welcome to Binary Database Handling Mode.")
    tableName = ""
    startupPath = "C:/Users/Tania/Desktop/Harshit/EDITH"
    mainDB = sqlite3.connect("C:/Users/Tania/Desktop/Harshit/EDITH/Data/mainDB.db")
    for x in mainDB.execute("SELECT * FROM Variables where File = '{}'".format(os.path.basename(__file__))).fetchall():exec("{} = {}".format(x[1],x[2]))
    mainDB = sqlite3.connect("C:/Users/Tania/Desktop/Harshit/EDITH/Data/{}".format(databaseInUse))
    while True:
        try:maindbHandle(input("Say Something: "))
        except KeyboardInterrupt:print("Task Abandoned.")
else:
    tableName = ""
    startupPath=os.getcwd()
    mainDB = sqlite3.connect(startupPath+"/Data/mainDB.db")
######################################################################################################################################
