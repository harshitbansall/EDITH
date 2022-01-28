import datetime,time,difflib,random,os,sqlite3,re
from threading import Thread
try:
    import zlib
except:
    pathList = str(sys.executable).split("\\")
    pathList.remove("pythonw.exe"),pathList.append("Scripts")
    os.system("/".join(pathList)+"/pip.exe install zlib")
##    os.system("/".join(pathList)+"/pip.exe install prettytable")
    time.sleep(2)
    import zlib
startupPath, prevOutput, prevsNum = os.getcwd(), "", ""
mainDB = sqlite3.connect(startupPath+"/Data/mainDB.db",check_same_thread=False)
logDB = sqlite3.connect(startupPath+"/Data/_log_.db",check_same_thread=False)
for x in mainDB.execute("SELECT * FROM Variables where File = '{}'".format(os.path.basename(__file__))).fetchall():exec("{} = {}".format(x[1],x[2]))
######################################################################################################################################
def oncePerDay():
    mainDB.execute("Update Variables set Value = '\"{}\"' where Variable = 'LastStartup'".format(str(datetime.date.today()))),mainDB.commit()
    logDB.execute("Create table if not exists _log_{} (sNum,queryID,Date,Time,Query)".format(datetime.date.today().strftime("%d%b%y"))),logDB.commit()
    from Files.Birthdays import bdayReminder as BR
    from Files.Occasions import occasionReminder as OR
    OR,BR()
######################################################################################################################################
def say(query):
    if engine.isBusy:engine.stop(),engine.setProperty("voice",engine.getProperty("voices")[1].id)
    engine.say(query),Thread(target=engine.runAndWait).start()
    while True:
        time.sleep(0.05)
        if engine.isBusy:
            engine.endLoop()
            break
######################################################################################################################################
def speak(query, show = True, end = "\n", wait = 0):
    global prevOutput
    if show is True:print(query, end = end)
    if Mute is False and prevOutput != query:time.sleep(wait),Thread(target=say,args=(query,)).start()
    prevOutput = query
######################################################################################################################################
def wikipediaSearch(query):
    query = " ".join([x for x in query.split() if x not in ['what','is','a','who','search','the']]).title()
    mainMemory = open("Data/_mainMemory_.txt").readlines()
    for q in mainMemory:
        if q=="!{}!:\n".format(query.replace(' ','').lower()):speak(mainMemory[mainMemory.index(q)+1].replace("\n","")),main()
    from wikipedia import summary
    print("Searching in Database..."),open(startupPath+"/Data/_mainMemory_.txt","a",encoding="utf-8").write("\n!{}!:\n".format(query.replace(' ','').lower())+summary(query,sentences=3)),wikipediaSearch(query),main()
######################################################################################################################################
def updateDB(sNum):
    if sNum not in [1,2,3,4,5]:
        mainDB.execute("Update funcFile2 set sNum = '' where sNum = {}".format(sNum))
        for i in reversed(range(5,sNum)):mainDB.execute("Update funcFile2 set sNum = {} where sNum = {}".format(i+1,i))
        mainDB.execute("Update funcFile2 set sNum = 5 where sNum = ''"),Thread(target=mainDB.commit).start()
######################################################################################################################################
def updateLogs(query):
    todayTable = "_log_{}".format(datetime.date.today().strftime("%d%b%y"))
    tablesNum = logDB.execute("SELECT max(rowid) from {0}".format(todayTable)).fetchone()[0]
    if tablesNum is None:
        tablesNum = 0
    logDB.execute("insert into {0} values ({1},'{2}','{3}','{4}','{5}')".format(todayTable,tablesNum+1,zlib.crc32(bytes(query,encoding='utf8')),datetime.date.today(),datetime.datetime.now().strftime("%H:%M:%S"),query)),Thread(target=logDB.commit).start()
######################################################################################################################################
def main():
    try:query=input("Say Something: ")
    except KeyboardInterrupt:speak("No Task to Abandon."),main()
    for x in mainDB.execute("select * from replaceList").fetchall():
        if re.search(r'\b{}\b'.format(x[2]), query):query=re.sub(r'\b{}\b'.format(x[2]), x[1], query)
    Thread(target = updateLogs,args = (query,)).start()
    if cSen is False:queryFunc(query.lower()),main()
    else:queryFunc(query),main()
######################################################################################################################################
def printNotifications():
    from Files.Reminders import remindReminders
    finalQuery = remindReminders()
    for x in finalQuery:speak(x, wait = 0.3)
######################################################################################################################################
def queryFunc(query):
    global prevsNum
    funcFile2execList,errorList = [(k[0],k[1]) for k in mainDB.execute("select * from funcFile2 order by sNum").fetchall() if any(y in query for y in k[2].split(";")) if bool([z for z in k[3].split() if z in query])==False],[]
    if len(funcFile2execList)==1:
        try:
            exec(funcFile2execList[0][1])
            if prevsNum != funcFile2execList[0][1]:Thread(target=updateDB,args=(funcFile2execList[0][0],)).start()
            prevsNum = funcFile2execList[0][1]
        except Exception as e:speak (str(e).title()+".")
        except KeyboardInterrupt:speak("Task Abandoned."),main()
    elif len(funcFile2execList)>1:
        for x in funcFile2execList:
            try:
                exec(x[1]),Thread(target=updateDB,args=(x[0],)).start()
                break
            except Exception as e:errorList+=[str(e).title()]
        if len(funcFile2execList)==len(errorList):
            speak(", ".join(errorList)+".")
            if "info" in query:notFound(query,prefix = "info ",prefixNum = 1)
    else:
        execList = [i[0] for i in mainDB.execute("SELECT func,trigger FROM funcFile3").fetchall() if query in i[1].split(";")]+["speak('{}')".format(random.choice(i[2].split(';'))) for i in mainDB.execute("SELECT * from funcFile1").fetchall() if query in i[1].split(";")]
        if execList!=[]:
            try:exec(execList[0])
            except Exception as e:speak ("Error: "+str(e).title())
            except KeyboardInterrupt:speak("Task Abandoned."),main()
        else:notFound(query)
######################################################################################################################################
def notFound(query,prefix = None,prefixNum = 0):
    newQuery = query
    query=" ".join([y for x in query.split() for y in ";".join([i[2] for i in mainDB.execute("SELECT * from funcFile3").fetchall() if i[2]!=""]).split(";")+";".join([i[1] for i in mainDB.execute("SELECT * from funcFile1").fetchall()]).split(";") if difflib.SequenceMatcher(None,x,y).ratio()>0.7])
    if query!=newQuery and query!="":
        speak("Do You mean '{}' ? ".format(query.title()), end = "")
        if input("Yes/No: ").lower()=="yes":queryFunc(query),main()
    speak("No Results for '{0}'. May I Search '{0}' ? ".format(newQuery.split(prefix)[prefixNum].title()), end = "")
    if input("Yes/No: ").lower()=="yes":queryFunc('google {}'.format(newQuery))
######################################################################################################################################
if __name__=="__main__":
    if Mute is False:queryFunc("silent unmute")
    if LastStartup!=str(datetime.date.today()):oncePerDay(),speak("{}".format(datetime.date.today().strftime("%d %B %Y, %A"))),time.sleep(0.2)
    else:print("{}".format(datetime.date.today().strftime("%d %B %Y, %A")))
    speak("Good {} Boss !".format(["Morning","Afternoon","Evening"][[12,18,24].index([x for x in [12,18,24] if x>datetime.datetime.now().hour][0])]))
    if Notify is True:printNotifications()
    main()
######################################################################################################################################
