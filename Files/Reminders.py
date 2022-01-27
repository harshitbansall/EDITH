import sqlite3,os,datetime,re
startupPath=os.getcwd()
######################################################################################################################################
def newReminder(eventDate,eventTime,eventName,eventDuration):
    if mainDB.execute("SELECT max(rowid) from Reminders").fetchone()[0] is None:mainDB.execute('''INSERT INTO Reminders (sNum,Date,Time,Event,duration) VALUES ({}, "{}", "{}", "{}", "{}")'''.format(1,eventDate,eventTime,eventName,eventDuration)),mainDB.commit()
    else:mainDB.execute('''INSERT INTO Reminders (sNum,Date,Time,Event,duration) VALUES ({}, "{}", "{}", "{}", "{}")'''.format(mainDB.execute("SELECT max(rowid) from Reminders").fetchone()[0]+1,eventDate,eventTime,eventName,eventDuration)),mainDB.commit()
######################################################################################################################################
def sortReminders():
    data=mainDB.execute("SELECT * from Reminders ORDER BY Event").fetchall()
    mainDB.execute("""CREATE TABLE Ordered (sNum,Date,Time,Event,duration)""")
    for i in data:
        i=list(i)
        i[0]=data.index(tuple(i))+1
        mainDB.execute("INSERT INTO Ordered (sNum,Date,Time,Event,duration) VALUES {}".format(tuple(i)))
    mainDB.execute("DROP table Reminders")
    mainDB.execute("ALTER TABLE Ordered RENAME TO Reminders"),mainDB.commit()
######################################################################################################################################
def remindReminders():
    rl = []
    for x in mainDB.execute("SELECT * from Reminders").fetchall():
        startTime=(int(x[2].split(":")[0]),int(x[2].split(":")[1]),int(x[2].split(":")[2]))
        daysforevent=datetime.datetime(int(x[1].split("/")[2]),int(x[1].split("/")[1]),int(x[1].split("/")[0]),startTime[0],startTime[1],startTime[2])-datetime.datetime.now()
        if daysforevent.days==-2:mainDB.execute("Delete from Reminders where sNum={}".format(x[0])),sortReminders()
        elif daysforevent.days==-1:
            dateToday=str(datetime.date.today()).split("-")
            if "hour" in x[4] or "Hour" in x[4]:timeLeft=str(datetime.datetime(int(dateToday[0]),int(dateToday[1]),int(dateToday[2]),startTime[0],startTime[1],startTime[2])+datetime.timedelta(hours=int(x[4].split()[0]))-datetime.datetime.today()).split(":")
            elif ":" in x[4]:timeLeft=str(datetime.datetime(int(dateToday[0]),int(dateToday[1]),int(dateToday[2]),int(x[4].split(":")[0]),int(x[4].split(":")[1]),int(x[4].split(":")[2]))-datetime.datetime.today()).split(":")
            if "Birthday" in x[3]:rl+=["Today is '{}'. Greet him/her with best wishes. {} Hours {} Minutes Left.".format(x[3],timeLeft[0],timeLeft[1])]
            else:rl+=["'{}' has begun. {} Hours {} Minutes Left.".format(x[3],timeLeft[0],timeLeft[1])]
        elif daysforevent.days==0:rl+=["{} Hours {} Minutes Left for event '{}'.".format(str(daysforevent).split(":")[0],str(daysforevent).split(":")[1],x[3])]
        elif daysforevent.days==1:rl+=["{} Day left for '{}'.".format(daysforevent.days,x[3])]
        elif 4>daysforevent.days>1:rl+=["{} Days left for '{}'.".format(daysforevent.days,x[3])]
    return rl
######################################################################################################################################
def mainReminders(query):
    if "show reminders"==query:
        for k in mainDB.execute("Select * from Reminders").fetchall():print(k)
    elif "remind" in query:
        eventDict={"eventDate":"","eventTime":"","eventName":"","eventDuration":""}
        for k in query.split():
            if "/" in k:eventDict["eventDate"]=k
            elif ":" in k:eventDict["eventTime"]=k
        if eventDict["eventDate"]=="":
            eventDict["eventDate"]=input("Date: ")
            if eventDict["eventDate"]=="":eventDict["eventDate"]="/".join(reversed(str(datetime.date.today()).split("-")))
        if eventDict["eventTime"]=="":
            eventDict["eventTime"]=input("Time: ")
            if eventDict["eventTime"]=="":eventDict["eventTime"]="00:00:00"
        if query=="remind me":eventDict["eventName"]=input("Event: ")
        else:eventDict["eventName"]=" ".join([x for x in query.replace(eventDict["eventDate"],"").replace(eventDict["eventTime"],"").split() if x not in ["remind","me","of","in","at","for","the","on","by"]])
        if eventDict["eventDuration"]=="":
            eventDict["eventDuration"]=input("Duration: ")
            if eventDict["eventDuration"]=="":eventDict["eventDuration"]="All-Day"
        newReminder(eventDict["eventDate"],eventDict["eventTime"],eventDict["eventName"].title(),eventDict["eventDuration"]),print("Reminder Set.")
######################################################################################################################################
if __name__=="__main__":
    if "Files" in startupPath:
        os.chdir("..")
        startupPath=os.getcwd()
    mainDB = sqlite3.connect(startupPath+"/Data/mainDB.db",check_same_thread=False)
    remindReminders()
    while True:mainReminders(input("Say Something: "))
else:
    mainDB = sqlite3.connect(startupPath+"/Data/mainDB.db",check_same_thread=False)
######################################################################################################################################
