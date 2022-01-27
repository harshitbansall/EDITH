##def writeFunc(content,fileNum):
##    os.chdir('Data')
##    lines = open('funcFile{}.txt'.format(fileNum)).readlines()
##    for x in range(len(lines)):
##        if "\n" in lines[x]:lines[x]=lines[x].replace("\n","")
##    for x in range(len(lines)):
##        if "" in lines:lines.remove("")
##    lines+=[content]
##    open('funcFile{}.txt'.format(fileNum),"w").write("\n".join(lines))
def mainNewCommand(query):
    if "when i say" in query:newCom,newArg=query.split(" when i say ")[0],query.split(" when i say ")[1]
    else:newArg,newCom=input("Enter New Argument: "),input("What do you want me to Do: ")
    if "reply" in newCom:mainDB.execute('''INSERT INTO funcFile1 (sNum,input,output,auth) VALUES ({}, "{}", "{}", "USER")'''.format(mainDB.execute("SELECT max(rowid) from funcFile1").fetchone()[0]+1,newArg,newCom.replace('reply ','').title()+".")),mainDB.commit()
    elif "do" in newCom:mainDB.execute('''INSERT INTO funcFile3 (sNum,func,trigger,auth) VALUES ({}, '{}', "{}", "USER")'''.format(mainDB.execute("SELECT max(rowid) from funcFile3").fetchone()[0]+1,newCom.replace('do ','').replace("\\n","\n").replace("'","\""),newArg)),mainDB.commit()
    elif "type" in newCom:mainDB.execute('''INSERT INTO replaceList (sNum,Phrase,Trigger) VALUES ({}, '{}', "{}")'''.format(mainDB.execute("SELECT max(rowid) from replaceList").fetchone()[0]+1,newCom.replace('type ','').title(),newArg)),mainDB.commit()
    else:mainDB.execute('''INSERT INTO funcFile3 (sNum,func,trigger,auth) VALUES ({}, 'queryFunc("{}")', "{}", "USER")'''.format(mainDB.execute("SELECT max(rowid) from funcFile3").fetchone()[0]+1,newCom,newArg)),mainDB.commit()
    return ("Functions Updated.")

if __name__=="__main__":
    import sqlite3,clipboard,os
    startupPath=os.getcwd()
    if "Files" in startupPath:
        os.chdir("..")
        startupPath=os.getcwd()
    mainDB = sqlite3.connect(startupPath+"/Data/mainDB.db")
    print("Welcome To Binary Function Edit Mode.")
    while True:
        ask=list(input("Mode?: "))
        if ask[0]=="d":
            if ask[1] in ["1","2","3"]:
                for i in mainDB.execute("SELECT * from funcFile{} where auth='USER'".format(ask[1])).fetchall():print(i)
                mainDB.execute("DELETE from funcFile{} where sNum = {} and auth='USER'".format(ask[1],input("Which Command do you want to delete: "))),mainDB.commit()
            elif ask[1]=="r":
                for i in mainDB.execute("SELECT * from Reminders".format(ask[1])).fetchall():print(i)
                mainDB.execute("DELETE from Reminders where sNum = {}".format(input("Which Command do you want to delete: "))),mainDB.commit()
            elif ask[1]=="l":
                for i in mainDB.execute("SELECT * from replaceList".format(ask[1])).fetchall():print(i)
                mainDB.execute("DELETE from replaceList where sNum = {}".format(input("Which Function do you want to delete: "))),mainDB.commit()

        elif ask[0]=="s":
            if ask[1] in ["1","2","3"]:
                for i in mainDB.execute("SELECT * from funcFile{} order by sNum".format(ask[1])).fetchall():print(i)
            elif ask[1]=="a":
                for i in mainDB.execute("SELECT * from Accounts".format(ask[1])).fetchall():print(i)
            elif ask[1]=="c":
                for i in mainDB.execute("SELECT * from Contacts".format(ask[1])).fetchall():print(i)
            elif ask[1]=="r":
                for i in mainDB.execute("SELECT * from Reminders".format(ask[1])).fetchall():print(i)
            elif ask[1]=="o":
                for i in mainDB.execute("SELECT * from Occasions".format(ask[1])).fetchall():print(i)
        elif ask[0]=="e":
            file=ask[1]
            if file=="3":
                for i in mainDB.execute("SELECT sNum,func,trigger from funcFile3").fetchall():print(i)
                sNum,func,trigger=mainDB.execute("SELECT sNum,func,trigger from funcFile3 where sNum = {}".format(int(input("Which Command Do you want to Edit?: ")))).fetchall()[0]
                clipboard.copy(func.replace("\n","\\n"))
                newFunc=input("New Function for '{}': ".format(func.replace("\n","\\n")))
                if newFunc!="":mainDB.execute("UPDATE funcFile3 SET func = '{}' where func = '{}'".format(newFunc.replace("\\n","\n"),func)),mainDB.commit()
                clipboard.copy(trigger)
                newCom=input("New Command for '{}': ".format(trigger))
                if newCom!="":mainDB.execute("UPDATE funcFile3 SET trigger = '{}' where trigger = '{}'".format(newCom,trigger)),mainDB.commit()
                print("Function Updated.")
            if file=="2":
                for i in mainDB.execute("SELECT sNum,func,trigger,exceptions from funcFile2 order by sNum").fetchall():print(i)
                sNum,func,trigger,exceptions=mainDB.execute("SELECT sNum,func,trigger,exceptions from funcFile2 where sNum = {}".format(int(input("Which Command Do you want to Edit?: ")))).fetchall()[0]
                clipboard.copy(func.replace("\n","\\n"))
                newFunc=input("New Function for '{}': ".format(func.replace("\n","\\n")))
                if newFunc!="":mainDB.execute("UPDATE funcFile2 SET func = '{}' where func = '{}'".format(newFunc.replace("\\n","\n"),func)),mainDB.commit()
                clipboard.copy(trigger)
                newCom=input("New Command for '{}': ".format(",".join(trigger.split(";"))))
                if newCom!="":mainDB.execute("UPDATE funcFile2 SET trigger = '{}' where trigger = '{}'".format(newCom,trigger)),mainDB.commit()
                clipboard.copy(exceptions)
                newExc=input("New Exceptions for '{}': ".format(exceptions))
                if newExc=="none" or newExc=="None":mainDB.execute("UPDATE funcFile2 SET exceptions = '' where sNum = {}".format(sNum)),mainDB.commit()
                elif newExc!="":mainDB.execute("UPDATE funcFile2 SET exceptions = '{}' where sNum = {}".format(newExc,sNum)),mainDB.commit()
                print("Function Updated.")
            elif file=="1":
                for i in mainDB.execute("SELECT sNum,input,output from funcFile1 where auth != 'SYS' ").fetchall():print(i)
                sNum,inputArg,output=mainDB.execute("SELECT sNum,input,output from funcFile1 where sNum = {}".format(int(input("Which Command Do you want to Edit?: ")))).fetchall()[0]
                clipboard.copy(inputArg)
                newinputArg=input("New Input for '{}': ".format(inputArg))
                if newinputArg!="":mainDB.execute("UPDATE funcFile1 SET input = '{}' where input = '{}'".format(newinputArg,inputArg)),mainDB.commit()
                clipboard.copy(output)
                newoutput=input("New Output for '{}': ".format(",".join(output.split(";"))))
                if newoutput!="":mainDB.execute("UPDATE funcFile1 SET output = '{}' where output = '{}'".format(newoutput,output)),mainDB.commit()
                print("Function Updated.")
        elif ask[0]=="a":
            file=ask[1]
            if file=="3":
                mainDB.execute('''INSERT INTO funcFile3 (sNum,func,trigger,auth) VALUES ({}, '{}', "{}", "USER")'''.format(mainDB.execute("SELECT max(rowid) from funcFile3").fetchone()[0]+1,input("Function: ").replace("\\n","\n").replace("'","\""),input("Trigger: "))),mainDB.commit()
            if file=="2":
                mainDB.execute('''INSERT INTO funcFile2 (sNum,func,trigger,exceptions,auth) VALUES ({}, '{}', "{}", "{}", "USER")'''.format(mainDB.execute("SELECT max(rowid) from funcFile2").fetchone()[0]+1,input("Function: ").replace("\\n","\n").replace("'","\""),input("Trigger: "),input("Exeptions: "))),mainDB.commit()
            elif file=="r":
                if mainDB.execute("SELECT max(rowid) from Reminders").fetchone()[0] is None:mainDB.execute('''INSERT INTO Reminders (sNum,Date,Time,Event,duration) VALUES ({}, "{}", "{}", "{}")'''.format(1,input("Date: "),input("Time: "),input("Event: "),input("Duration: "))),mainDB.commit()
                else:mainDB.execute('''INSERT INTO Reminders (sNum,Date,Time,Event,duration) VALUES ({}, "{}", "{}", "{}")'''.format(mainDB.execute("SELECT max(rowid) from Reminders").fetchone()[0]+1,input("Date: "),input("Time: "),input("Event: "),input("Duration: "))),mainDB.commit()
            elif file=="o":
                if mainDB.execute("SELECT max(rowid) from Occasions").fetchone()[0] is None:mainDB.execute('''INSERT INTO Occasions (sNum,Type,Occasion,Date,Time) VALUES ({}, "{}", "{}", "{}", "{}")'''.format(1,input("Type: "),input("Occasion: "),input("Date: "),input("Time: "))),mainDB.commit()
                else:mainDB.execute('''INSERT INTO Occasions (sNum,Type,Occasion,Date,Time) VALUES ({}, "{}", "{}", "{}", "{}")'''.format(mainDB.execute("SELECT max(rowid) from Occasions").fetchone()[0]+1,input("Type: "),input("Occasion: "),input("Date: "),input("Time: "))),mainDB.commit()
                
else:
    import sqlite3,os
    startupPath=os.getcwd()
    mainDB = sqlite3.connect(startupPath+"/Data/mainDB.db")
