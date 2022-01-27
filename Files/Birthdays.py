import datetime,sqlite3,os
from dateutil.relativedelta import relativedelta as rd
######################################################################################################################################
def bdayReminder():
    for x in mainDB.execute("SELECT fname,lname,bday from Contacts").fetchall():
        if x[2]!="":
            daysforbday=datetime.date(datetime.date.today().year,int(x[2].split("/")[1]),int(x[2].split("/")[0]))-datetime.date.today()
            if 4>daysforbday.days>=0:
                if mainDB.execute('''Select * from Reminders where Event = "{} {}'s Birthday"'''.format(x[0],x[1])).fetchone() is None:
                    if mainDB.execute("SELECT max(rowid) from Reminders").fetchone()[0] is None:
                        mainDB.execute('''Insert into Reminders (sNum,Date,Time,Event,duration) values (1, "{}", "00:00:00", "{} {}'s Birthday", "24 hours")'''.format(x[2].replace(x[2].split("/")[2],str(datetime.date.today().year)),x[0],x[1])),mainDB.commit()
                    else:mainDB.execute('''Insert into Reminders (sNum,Date,Time,Event,duration) values ({}, "{}", "00:00:00", "{} {}'s Birthday", "24 hours")'''.format(mainDB.execute("SELECT max(rowid) from Reminders").fetchone()[0]+1,x[2].replace(x[2].split("/")[2],str(datetime.date.today().year)),x[0],x[1])),mainDB.commit()
######################################################################################################################################
def findBday(*args, show = True):
    for i in args:
        for x in mainDB.execute("select fullname,bday from contacts where fname = '{0}' or fullname = '{0}' or lname = '{0}'".format(i)).fetchall():
            if x[1]!="":
                bdate=datetime.date(int(x[1].split("/")[2]),int(x[1].split("/")[1]),int(x[1].split("/")[0]))
                if show is True:return("{} was Born On {}.".format(x[0],bdate.strftime("%d %B %Y, %A")))
                else:return (x[0],bdate)
######################################################################################################################################
def birthGap(sub1, sub2, show = True):
    sub1name,sub1bday=findBday(sub1, show = False)
    sub2name,sub2bday=findBday(sub2, show = False)
    timeBW = rd(sub1bday,sub2bday)
    if show is True:
        if sub1bday>sub2bday:return("{} is Older Than {} by '{} Years {} Months {} Days'.".format(sub2name,sub1name,timeBW.years,timeBW.months,timeBW.days))
        else:return("{} is Older Than {} by '{} Years {} Months {} Days'.".format(sub1name,sub2name,abs(timeBW.years),abs(timeBW.months),abs(timeBW.days)))
    else: return (sub1bday-sub2bday)
######################################################################################################################################
def findAge(*args, show = True):
    if len(args)==0:
        for x in mainDB.execute("SELECT fullname,bday from Contacts").fetchall():
            if x[1]!="":
                age=rd(datetime.date.today(),datetime.date(int(x[1].split("/")[2]),int(x[1].split("/")[1]),int(x[1].split("/")[0])))
                print("{} is {} Years, {} Months Old.".format(x[0],age.years,age.months))
##                print("{} is {} Years, {} Months, {} Days Old.".format(x[0],age.years,age.months,age.days))
    else:
        for i in args:
            for x in mainDB.execute("SELECT fullname,bday from Contacts where fname = '{0}' or fullname = '{0}' or lname = '{0}'".format(i)).fetchall():
                if x[1]=="":return("No Birthday Record for {}.".format(x[0]))
                elif x[1]!="":
                    age=rd(datetime.date.today(),datetime.date(int(x[1].split("/")[2]),int(x[1].split("/")[1]),int(x[1].split("/")[0])))
                    if show is True:return("{} is {} Years, {} Months Old.".format(x[0],age.years,age.months))
                    else:return(age.years,age.months,age.days)
######################################################################################################################################
def findTimeLeft(*args, show = True):
    if len(args)==0:
        for x in mainDB.execute("SELECT fullname,bday from Contacts").fetchall():
            if x[1]!="":
                daysforbday=datetime.date(datetime.date.today().year,int(x[1].split("/")[1]),int(x[1].split("/")[0]))-datetime.date.today()
                if daysforbday.days<0:print("{}'s Birthday was {} Days Ago. ( Coming in {} Days )".format(x[0],abs(daysforbday.days),365+daysforbday.days))
                else:print("{}'s Birthday is Coming in {} Days.".format(x[0],daysforbday.days))
    else:
        for i in args:
            for x in mainDB.execute("select fullname,bday from contacts where fname = '{0}' or fullname = '{0}' or lname = '{0}'".format(i)).fetchall():
                if x[1]!="":
                    daysforbday=datetime.date(datetime.date.today().year,int(x[1].split("/")[1]),int(x[1].split("/")[0]))-datetime.date.today()
                    if show is True:
                        if daysforbday.days<0:print("{}'s Birthday was {} Days Ago. ( Coming in {} Days )".format(x[0],abs(daysforbday.days),365+daysforbday.days))
                        else:print("{}'s Birthday is Coming in {} Days.".format(x[0],daysforbday.days))
                    else:return(daysforbday.days)
######################################################################################################################################
def mainBirthdays(query):
    if "older" in query:return birthGap(query.split()[query.split().index("is")+1].title(),query.split()[query.split().index("than")+1].title())
    elif "what" in query or "find" in query or "how" in query:
        if "age" in query:return findAge(query.split()[query.split().index("of")+1].title())
        elif "old" in query:return findAge(query.split()[query.split().index("is")+1].title())
    elif "when" in query:
        if "birthday" in query or "bday" in query:
            for x in query.split():
                if "'s" in x:targetPerson = x.replace("'s","").title()
            return findBday(targetPerson, show = True)
    elif "all birthdays"==query or "all bdays"==query:findTimeLeft()
######################################################################################################################################      
if __name__=="__main__":
    mainDB = sqlite3.connect("C:/Users/Tania/Desktop/Harshit/EDITH/Data/mainDB.db",check_same_thread=False)
    while True:
        finalQuery = mainBirthdays(input("Say Something: "))
        if finalQuery is not None:print(finalQuery)
else:
    if __name__!="Files.Birthdays":os.chdir("..")
    startupPath=os.getcwd()
    mainDB = sqlite3.connect(startupPath+"/Data/mainDB.db",check_same_thread=False)
######################################################################################################################################
