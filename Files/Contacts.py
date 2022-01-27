import sqlite3,os,time
from tkinter import *
##from PIL import ImageTk,Image
from threading import Thread
##mainDB,passList = sqlite3.connect(startupPath+"/Data/mainDB.db"),[]
##for x in open(startupPath+"/Data/gmailPasses.txt","r").readlines():passList+=[eval(x)]
##for x in passList:
##    if "In Use" in x:
##        currentEmail,currentPass=x[1],x[2]
##def showImages(*args):
##    if len(args[1])==1:Label(root, image = eval("personImage{}".format(args[0]))).grid(row=0,column=0,columnspan=3)
##    elif len(args[1])>=args[0]>0:
##        mainImage = Label(root, image = eval("personImage{}".format(args[0])))
##        root.title(args[1][args[0]-1]),mainImage.grid(row=0,column=0,columnspan=3),Button(root,text="<< Previous",command=lambda: [mainImage.grid_forget(),showImages(args[0]-1,args[1])]).grid(row=1,column=0),Label(root,text=args[1][args[0]-1]).grid(row=1,column=1),Button(root,text="Next >>",command=lambda: [mainImage.grid_forget(),showImages(args[0]+1,args[1])]).grid(row=1,column=2)
######################################################################################################################################       
def showInfo(personList):
##    personImageList=[]
    for i in personList:
        print("\nFull Name: "+i[3]+"\nBirthday: "+i[4]+"\nGender: "+i[5]+"\nPhone Numbers: "+", ".join([x for x in [i[6],i[7]] if x!=""])+"\nNick Name: "+i[8]+"\nAddress: "+i[9]+"\nE-Mail: "+i[10]+"\n")
##        if os.path.isfile(startupPath+"/Data/Contacts/Images/"+i[3]+".jpg"):personImageList+=[i[3]]
##    if personImageList!=[]:
##        global root
##        root = Tk()
##        for i in personImageList:exec("global personImage{0}\npersonImage{0}=Image.open('{1}.jpg')\nw,b=personImage{0}.size\npersonImage{0} = ImageTk.PhotoImage(personImage{0}.resize((w//8, b//8), Image.ANTIALIAS))".format(personImageList.index(i)+1,startupPath+"/Data/Contacts/Images/"+i))
##        showImages(1,personImageList)
######################################################################################################################################
def executeDB(*args):
    l1=[]
    if len(args)==0:condition,getVars="","*"
    elif len(args)==1:condition,getVars=args[0],"*"
    else:
        condition,getVars=args[0],",".join(args[1:])
        if getVars=="all":getVars="sNum,fname,lname,fullname,bday,gender,pnumber1,pnumber2,nname,address,email"
    if getVars=="*" and condition!="":
        showInfo(mainDB.execute("SELECT {} from Contacts {}".format(getVars,condition)).fetchall())
    for i in mainDB.execute("SELECT {} from Contacts {}".format(getVars,condition)).fetchall():
        if getVars=="*":
            if condition=="":print(i)
        else:l1+=[i]
    return l1
######################################################################################################################################
def sortContacts():
    data=mainDB.execute("SELECT * from Contacts ORDER BY fullname").fetchall()
    mainDB.execute("""CREATE TABLE Ordered (sNum,fname text,lname text,fullname text,bday text,gender text,pnumber1 text,pnumber2 text,nname text,address text,email text)""")
    for i in data:
        i=list(i)
        i[0]=data.index(tuple(i))+1
        mainDB.execute("INSERT INTO Ordered (sNum,fname,lname,fullname,bday,gender,pnumber1,pnumber2,nname,address,email) VALUES {}".format(tuple(i)))
    mainDB.commit()
    mainDB.execute("DROP table Contacts")
    mainDB.execute("ALTER TABLE Ordered RENAME TO Contacts"),mainDB.commit()
######################################################################################################################################
def addC(values):
    mainDB.execute("INSERT INTO Contacts (sNum,fname,lname,fullname,bday,gender,pnumber1,pnumber2,nname,address,email) VALUES {}".format(values)),mainDB.commit(),sortContacts()
######################################################################################################################################
def email(toMail):
    from email.message import EmailMessage
    msg=EmailMessage()
    print("To: "+toMail+"\nFrom: "+currentEmail)
    msg['Subject'],body,msg['From'],msg['To']=input("Subject: "),"",currentEmail,toMail
    print("Type '#end' to end Your Message and '#attach' to attach files.")
    while True:
        line=input()
        if "#end" in line:break
        elif "#attach" in line:print("yoyo")
        else:body+=line+"\n"
    msg.set_content(body),print("Sending E-Mail...",end="")
    import smtplib,ssl
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
        server.login(currentEmail, currentPass)
        server.send_message(msg)
        return(" Email Sent.")
######################################################################################################################################
def mainContacts(query):
    if "add contact"==query:
        mainDB.execute("INSERT INTO Contacts (sNum,fname,lname,fullname,bday,gender,pnumber1,pnumber2,nname,address,email) VALUES ('1','{0}', '{1}', '{0} {1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')".format(input("First Name: "),input("Last Name: "),input("Birthday (DD/MM/YYYY): "),input("Gender: "),input("Phone Number 1: "),input("Phone Number 2: "),input("Nick Name: "),input("Address: "),input("E-Mail: "))),mainDB.commit(),sortContacts()
##    elif "make"==query:mainDB.execute("""CREATE TABLE Contacts (fname text,lname text,bday text,gender text,pnumber1 text,nname text,address text,email text)""")
    elif "show contacts"==query:executeDB()
    elif "change email"==query:
        emailList=mainDB.execute("SELECT address,token from Accounts where token !=''").fetchall()
        for k in emailList:print("{} : {}".format(emailList.index(k)+1,k[0]))
        global currentEmail,currentPassword
        mainDB.execute("UPDATE Accounts SET status = '' where status = 'In Use'"),mainDB.execute("UPDATE Accounts SET status = 'In Use' where address = '{}'".format(emailList[int(input("Which E-Mail should I Use: "))-1][0])),mainDB.commit(),print("E-Mail Changed.")
        currentEmail,currentPassword=mainDB.execute("SELECT address,token from Accounts where status = 'In Use'").fetchall()[0]
##        for x in passList:print(str(passList.index(x)+1)+" : "+x[1])
##        for x in passList:
##            global currentEmail,currentPass
##            if currentEmail in x:
##                num=int(input("Which E-Mail should I Use: "))
##                passList[passList.index(x)][0],passList[num-1][0]="","In Use"
##        currentEmail,currentPass=passList[num-1][1],passList[num-1][2]
##        open("gmailPasses.txt","w").write("\n".join([str(x) for x in passList]))
    elif "info" in query:
        if query.split("info ")[1].isdigit():
            if len(query.split("info ")[1]) in [10,8,11,12]:executeDB("where pnumber1='{}'".format(query.split("info ")[1]))
            else: raise Exception("Invalid Phone Number.")
        elif "@" in query.split("info ")[1]:executeDB("where email='{}'".format(query.split("info ")[1]))
        else:
            personList = mainDB.execute("Select * from Contacts where fname='{0}' or lname='{0}' or fullname='{0}' or nname='{0}'".format(query.split("info ")[1].title())).fetchall()
            if personList == []:raise Exception("No Contact Named '{0}'".format(query.split("info ")[1].title()))
            else:showInfo(personList)
    elif "email" in query:
        getEmails,num=executeDB("where fname='{0}' or lname='{0}' or nname='{0}'".format(query.split("email ")[1].title()),"fname,lname,email"),0
        if getEmails == []:raise Exception("No Contact Named '{0}'".format(query.split("email ")[1].title()))
        if len(getEmails)>1:
            for i in getEmails:print(str(getEmails.index(i)+1)+" : "+i[0]+" "+i[1])
            num=int(input("Which '{}' should I E-Mail: ".format(query.split("email ")[1].title())))-1
            toMail=getEmails[num][2]
        elif len(getEmails)==1:toMail=getEmails[0][2]
        elif len(getEmails)==0 and "@" in query.split()[1]:toMail=query.split()[1]
        else:
            toMail="##"
            raise Exception ("No Contact Named '{0}'".format(query.split("email ")[1].title()))
        if toMail=="":raise Exception("No E-Mail Associated to the Contact '{} {}'".format(getEmails[num][0],getEmails[num][1]))
        elif "@" in toMail:email(toMail)
    elif "call" in query:
        getPnums=executeDB("where fname='{0}' or lname='{0}' or nname='{0}' or fullname='{0}'".format(query.split("call ")[1].title()),"fname,lname,pnumber1")
        if getPnums == []:raise Exception("No Contact Named '{0}'".format(query.split("call ")[1].title()))
        if len(getPnums)>1:
            for i in getPnums:print(str(getPnums.index(i)+1)+" : "+i[0]+" "+i[1])
            person=getPnums[int(input("Which '{}' should I Call: ".format(query.split("call ")[1].title())))-1]
        elif len(getPnums)==1:person=getPnums[0]
        try:
            import pyqrcode,png
            fileName=startupPath+'/Data/Contacts/QR Dump/{} {} ({}).png'.format(person[0],person[1],person[2])
            pyqrcode.create("{}".format(person[2])).png(fileName, scale = 6)
            os.startfile(fileName)
            return("Calling '{} {}' at '+91{}'.".format(person[0],person[1],person[2]))
        except:raise Exception("'{}' is Not in Contacts".format(query.split("call ")[1].title()))
    elif "delete" in query:
        deleteList=executeDB("where fname='{0}' or lname='{0}' or nname='{0}'".format(query.split("delete ")[1].title()),"fname,lname")
        if deleteList == []:raise Exception("No Contact Named '{0}'".format(query.split("delete ")[1].title()))
        if len(deleteList)>1:
            for i in deleteList:print(str(deleteList.index(i)+1)+" : "+i[0]+" "+i[1])
            deleteItem=deleteList[int(input("Which '{}' should I Delete: ".format(query.split("delete ")[1].title())))-1]
        elif len(deleteList)==1:deleteItem=deleteList[0]
        mainDB.execute("DELETE from Contacts WHERE fname='{0}' AND lname='{1}'".format(deleteItem[0],deleteItem[1])),mainDB.commit(),print("Contact Deleted."),sortContacts()
    elif "edit" in query:
        editList=executeDB("where fname='{0}' or lname='{0}' or nname='{0}'".format(query.split("edit ")[1].title()),"all")
        if editList == []:raise Exception("No Contact Named '{0}'".format(query.split("edit ")[1].title()))
        fields=["","First Name","Last Name","Full Name","Birthday","Gender","Phone Number 1","Phone Number 2","Nick Name","Address","E-Mail"]
        if len(editList)>1:
            for i in editList:print(str(editList.index(i)+1)+" : "+i[1]+" "+i[2])
            editItem=editList[int(input("Which '{}' should I Edit: ".format(query.split("edit ")[1].title())))-1]
        elif len(editList)==1:editItem=editList[0]
        editItem=list(editItem)
        for k in fields:
            if k=="Full Name":
                editItem[fields.index(k)]="{} {}".format(editItem[1],editItem[2])
            elif k!="":
                var=input("{} '{}': ".format(k,editItem[fields.index(k)]))
                if var!="":editItem[fields.index(k)]=var
        mainDB.execute("DELETE from Contacts where sNum = {}".format(editItem[0])),mainDB.commit(),addC(tuple(editItem))
##    else:print(executeDB("where fname='{0}' or nname='{0}'".format(query.split()[0]),query.split()[1]))
######################################################################################################################################
if __name__=="__main__":
    print("Welcome to Binary Contact Edit Mode.")
    startupPath="C:/Users/Tania/Desktop/Harshit/EDITH"
    mainDB = sqlite3.connect("C:/Users/Tania/Desktop/Harshit/EDITH/Data/mainDB.db")
    currentEmail,currentPassword=mainDB.execute("SELECT address,token from Accounts where status = 'In Use'").fetchall()[0]
    while True:
        mainContacts(input("Say Something: "))
else:
    startupPath=os.getcwd()
    mainDB = sqlite3.connect(startupPath+"/Data/mainDB.db")
    currentEmail,currentPass=mainDB.execute("SELECT address,token from Accounts where status = 'In Use'").fetchall()[0]
######################################################################################################################################
