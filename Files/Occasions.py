import datetime,sqlite3,os
######################################################################################################################################
def occasionReminder():
    for x in mainDB.execute("SELECT * from Occasions").fetchall():
        if x[1]=="P":daysforevent=datetime.date(datetime.date.today().year,int(x[3].split("/")[1]),int(x[3].split("/")[0]))-datetime.date.today()
        elif x[1]=="T":daysforevent=datetime.date(int(x[3].split("/")[2]),int(x[3].split("/")[1]),int(x[3].split("/")[0]))-datetime.date.today()
        if 4>daysforevent.days>0:
            if mainDB.execute('''Select * from Reminders where Event = "{}"'''.format(x[2])).fetchone() is None:
                if mainDB.execute("SELECT max(rowid) from Reminders").fetchone()[0] is None:
                    mainDB.execute('''Insert into Reminders (sNum,Date,Time,Event,duration) values (1, "{}", "{}", "{}", "24 hours")'''.format(x[3],x[4],x[2])),mainDB.commit()
                else:mainDB.execute('''Insert into Reminders (sNum,Date,Time,Event,duration) values ({}, "{}", "{}", "{}", "24 hours")'''.format(mainDB.execute("SELECT max(rowid) from Reminders").fetchone()[0]+1,x[3],x[4],x[2])),mainDB.commit()
######################################################################################################################################
def displayAll():
    for x in mainDB.execute("SELECT * from Occasions").fetchall():
        if x[1]=="P":
            daysforevent=datetime.date(datetime.date.today().year,int(x[3].split("/")[1]),int(x[3].split("/")[0]))-datetime.date.today()
        elif x[1]=="T":
            daysforevent=datetime.date(int(x[3].split("/")[2]),int(x[3].split("/")[1]),int(x[3].split("/")[0]))-datetime.date.today()
        if daysforevent.days<0:print("'{}' was '{} Days' ago.".format(x[2],abs(daysforevent.days)))
        else:print("'{} Days' Left for '{}'.".format(daysforevent.days,x[2]))
######################################################################################################################################
if __name__=="__main__":
    mainDB = sqlite3.connect("C:/Users/Tania/Desktop/Harshit/EDITH/Data/mainDB.db",check_same_thread=False)
    displayAll()
else:
    if __name__!="Files.Occasions":os.chdir("..")
    startupPath=os.getcwd()
    mainDB = sqlite3.connect(startupPath+"/Data/mainDB.db",check_same_thread=False)
######################################################################################################################################
