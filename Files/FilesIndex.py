import os,shutil,re,sys,requests,sqlite3,datetime,magic
##from tabulate import tabulate
from prettytable import PrettyTable
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
######################################################################################################################################
def newAccessToken(clientID,clientSecret,refreshToken):
    accessTokenData = mainDB.execute("select currentAccessToken,tokenExpiry from GoogleAPI where address = '{}'".format(mainAddress)).fetchone()
    if accessTokenData not in [("",""),(None,None)]:
        if datetime.datetime.now()<datetime.datetime.strptime(accessTokenData[1], '%Y-%m-%d %H:%M:%S'):
            return accessTokenData[0]
        else:
            mainDB.execute("update GoogleAPI set currentAccessToken = '', tokenExpiry = '' where address = '{}'".format(mainAddress))
            return newAccessToken(clientID,clientSecret,refreshToken)
    else:
        try:
            response = eval(requests.post('https://oauth2.googleapis.com/token', data={'client_id': clientID,'client_secret': clientSecret,'refresh_token': refreshToken,'grant_type': 'refresh_token'}).text)
            mainDB.execute("update GoogleAPI set currentAccessToken = '{0}', tokenExpiry = '{1}' where address = '{2}'".format(response['access_token'],(datetime.datetime.now()+datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S'),mainAddress)),mainDB.commit()
            return(response['access_token'])
        except:
            import webbrowser
            print("Requirement Of New Access Token for '{}'. Kindly Paste the Redirected Link Below.".format(mainAddress)),webbrowser.open('''https://accounts.google.com/o/oauth2/v2/auth?scope=https://www.googleapis.com/auth/youtube%20https://www.googleapis.com/auth/drive&prompt=consent&access_type=offline&include_granted_scopes=true&response_type=code&state=state_parameter_passthrough_value&redirect_uri=http://localhost&client_id={}'''.format(clientID))
            response = eval(
                requests.post('https://accounts.google.com/o/oauth2/token',
                              data={'code': re.split('[=&]',input("Redirected Link: "))[3].replace("%2F","/"),'client_id': clientID,'client_secret': clientSecret,'redirect_uri': 'http://localhost','grant_type': 'authorization_code'}).text)
            mainDB.execute("update GoogleAPI set refreshToken = '{}' where address = '{}'".format(response['refresh_token'],mainAddress))
            mainDB.execute("update GoogleAPI set currentAccessToken = '{}', tokenExpiry = '{}' where address = '{}'".format(response['access_token'],(datetime.datetime.now()+datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S'),mainAddress)),mainDB.commit()
            return(response['access_token'])
######################################################################################################################################
##def showFiles(arg):
##    startNum=1
##    for file in os.listdir():
##        if arg=="files" and os.path.isfile(file):print(startNum," : ",file)
##        elif arg=="dirs" and os.path.isdir(file):print(startNum," : ",file)
##        exec("global file{}\nfile{}='{}'".format(startNum,startNum,file))
##        startNum+=1
######################################################################################################################################
def returnFile(num,fileName):
    exec("global file{0}\nfile{0}=\"{1}\"".format(num,fileName))
    if os.path.isdir(fileName):
        return 'Directory'
    else:
        return 'File'
######################################################################################################################################
def returnMime(fileName):
    if os.path.isdir(fileName):
        return 'Folder'
    else:
        return magic.from_file(fileName,mime=True).title()
######################################################################################################################################
def makeDriveGlobals():
    global mainAddress,mainAccount,accessToken,path,prevPath
    mainAddress = mainDB.execute("select address from driveAccounts where status = 'In Use'").fetchone()[0]
    mainAccount = mainDB.execute("select * from GoogleAPI where address = '{}'".format(mainAddress)).fetchone()
    accessToken = newAccessToken(mainAccount[2],mainAccount[3],mainAccount[4])
    path,prevPath = (getRootID(),"My Drive","application/vnd.google-apps.folder"),""
######################################################################################################################################
def getRootID():
    if AnonymousDriveLogin is False:
        if mainDB.execute("select rootID from driveAccounts where status = 'In Use'").fetchone() is None:
            rootID = eval(requests.get('https://www.googleapis.com/drive/v2/about',headers = {"Authorization": "Bearer " + accessToken}).text.replace("true","True").replace("false","False"))['rootFolderId']
            mainDB.execute("Insert into driveAccounts (sNum, status, address, rootID) Values ({},'','{}','{}')".format(mainDB.execute("SELECT max(rowid) from {}".format(tableName)).fetchone()[0],mainAddress,rootID)),mainDB.commit()
            return rootID
        else:
            rootIdData = mainDB.execute("select rootID from driveAccounts where status = 'In Use'").fetchone()[0]
            if rootIdData is None or rootIdData == "":
                rootID = eval(
                    requests.get('https://www.googleapis.com/drive/v2/about',
                                 headers = {"Authorization": "Bearer " + accessToken}).text.replace("true","True").replace("false","False"))['rootFolderId']
                mainDB.execute("update driveAccounts set rootID = '{}' where status = 'In Use'".format(rootID)),mainDB.commit()
                return rootID
            else:
                return rootIdData
    else:
        return eval(requests.get('https://www.googleapis.com/drive/v2/about',headers = {"Authorization": "Bearer " + accessToken}).text.replace("true","True").replace("false","False"))['rootFolderId']
######################################################################################################################################
def edithDriveBackup():
    import json,datetime
    shutil.make_archive("C:/Users/Tania/Desktop/EDITH", 'zip', "C:/Users/Tania/Desktop/Harshit/EDITH")
    requests.post("https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",headers = {"Authorization": "Bearer " + accessToken},files = {'data': ('metadata', json.dumps({"name": "EDITH {}.zip".format(datetime.datetime.now()),"parents": ["1WbSCqWEkC1iqQL2qMDEYcHQCIQj45lMZ"]}), 'application/json; charset=UTF-8'),'file': open("C:/Users/Tania/Desktop/EDITH.zip", "rb")},)
    os.remove("C:/Users/Tania/Desktop/EDITH.zip")
######################################################################################################################################
def mainWindowsExplorer(query):
    if "goto" in query:
        try:
            try:os.chdir(query.split("goto ")[1]),print ("Path Changed to: ",str(os.getcwd()).title())
            except:os.chdir(eval("file{}".format(query.split()[1]))),print ("Path Changed to: ",str(os.getcwd()).title())
        except:return ("No such Directory.")
    elif "back"==query:os.chdir(".."),print ("Path Changed to: ",os.getcwd())
    elif "show" in query or "list" in query:
        x = PrettyTable()
        x.field_names = ['No','Name','Type','Mime']
        x.title = os.getcwd().title()
        for k in [[num+1,x,returnFile(num+1,x),returnMime(x)] for num,x in enumerate(os.listdir())]:
            x.add_row(k)
        print(x)
##        open("test.txt","w").write(str(x))
##        print ("Path: {}\nDirectories: ".format(os.getcwd()),len([x for x in os.listdir() if os.path.isdir(x)])),showFiles("dirs")
##        if "files" in query:
##            print ("Files: ",len([x for x in os.listdir() if os.path.isfile(x)])),showFiles("files")
    elif "open" in query:
        try:
            try:os.startfile(query.split("open ")[1])
            except:os.startfile(eval("file{}".format(query.split()[1])))
        except:return ("No such File Exists.")
    elif "copy" in query:
        try:
            global source
            if os.path.exists(query.split("copy ")[1]):
                source=os.path.abspath(query.split("copy ")[1])
                print(query.split("copy ")[1].title(),"Copied.")
            else:
                source=os.path.abspath(eval("file{}".format(query.split()[1])))
                print(eval("file{}".format(query.split()[1])),"Copied.")
        except:return ("No such File Exists.")
    elif query=="paste":
        try:shutil.copy(source,os.getcwd()),print ("File Pasted.")
        except:print ("No file copied.")
    elif "delete" in query or "remove" in query or "dump" in query or "clear" in query:
        if "cache" in query or "memory files" in query or "data" in query:
            try:shutil.rmtree(startupPath+'\Files\__pycache__'),print ("Cleared Cache.")
            except:return ("Cleared Cache.")
        else:
            try:
                file=query.split("delete ")[1]
                if os.path.exists(file) is False:file=eval("file{}".format(query.split()[1]))
                if os.path.isfile(file) is True:
                    if input("Permanently Delete '{}' ? Yes/No: ".format(file)).lower() in ["yes","y"]:
                        os.remove(file)
                        return ("{} Removed.".format(file))
                elif os.path.isdir(file) is True:
                    if input("Permanently Delete '{}' folder ? Yes/No: ".format(file)).lower() in ["yes","y"]:
                        shutil.rmtree(os.path.abspath(file))
                        return ("{} Removed.".format(file))
            except:raise Exception ("'{}' Do Not Exists".format(query.split("delete ")[1].title()))
    elif "rename" in query:
        if os.path.isfile(query.split("rename ")[1]):
            existFile=query.split("rename ")[1]
            newRename=input("New Name for "+query.split("goto ")[1]+" : ")
        else:
            existFile=eval("file{}".format(query.split()[1]))
            newRename=input("New Name for "+eval("file{}".format(query.split()[1]))+" : ")
        if os.path.isfile(existFile):
            os.rename(existFile,newRename+"."+existFile.split(".")[1])
            return ("'{}' Renamed '{}.{}'.".format(existFile,newRename,existFile.split(".")[1]))
        else:
            os.rename(existFile,newRename)
            return ("'{}' Renamed '{}'.".format(existFile,newRename))
    elif "info" in query:
        import datetime
        file=query.split("info ")[1]
        if os.path.exists(file) is False:
            try:file=eval("file{}".format(query.split()[1]))
            except:raise Exception("No File Named '{}'".format(file.title()))
        print("File Name: "+file+"\nLocation: "+os.path.abspath(file)+"\nSize: "+str(os.stat(file).st_size/1000)+" KBs")
        if os.path.isfile(file):print ("Properties: "+magic.from_file(file).title()+"\nMIME: "+magic.from_file(file,mime=True).title())
        elif os.path.isdir(file):print ("Sub Folders:",", ".join([x for x in os.listdir(file) if "." not in x]))
        print ("Date Created: "+datetime.datetime.fromtimestamp(os.stat(file).st_ctime).strftime("%A, %d %B %Y, %I:%M:%S")+"\nDate Modified: "+datetime.datetime.fromtimestamp(os.stat(file).st_mtime).strftime("%A, %d %B %Y, %I:%M:%S"))
    elif query=="path":return (os.getcwd())
    elif "funcs" in query:
        global filename
        filename,lineNum,sNum=query.split("funcs ")[1],1,1
        if os.path.isfile(filename) is False:
            filename=eval("file{}".format(query.split("funcs ")[1]))
        print ("Functions in {}: {}".format(filename,"".join(open(filename).readlines()).count("def ")))
        for x in open(filename).readlines():
            if "def " in x:
                exec("print('{0}. {1} (line {2})')\nglobal func{0}\nfunc{0}='{1}'".format(str(sNum),"".join([y for y in x if y not in ["\n",":"," "]]).replace("def",""),lineNum))
                sNum+=1
            lineNum+=1
    elif "new code"==query:
        def nc():
            line=input()
            if "#end" in line:
                if input("Editing Mode Exited.\nRun Your Code ?: ")=="yes":__import__(newCodeFile)
            else:
                open(newCodeFile+".py","a").write(line+"\n"),nc()
        newCodeFile=input("Enter Filename: ")
        print("Basic Rules:\n1. Press 'Tab' to provide Indentation.\n2. Type '#end' to end Your Script."),nc()
    elif "call" in query:
        try:
            splitQ,argList=re.split('[()]',eval("func{}".format(query.split("call ")[1]))),[]
            exec("\n".join(['''{0}=input("Enter Value for '{0}': ")\nargList+=[{0}]'''.format(splitQ[1].split(',')[x]) for x in range(len(splitQ[1].split(',')))]))
            exec("sys.path.append(os.getcwd())\nfrom {1} import {0}".format(splitQ[0],filename.replace(".py","")))
            try:print(eval("{0}({1})".format(splitQ[0],",".join([x for x in argList]))))
            except:print(eval("{0}('{1}')".format(splitQ[0],",".join([x for x in argList]))))
        except:
            raise Exception("No Function Named '{0}'".format(query.split("call ")[1].title()))
    elif "read" in query:
        print("################################START\n")
        try:print(open(query.split("read ")[1]).read())
        except:print(open(eval("file{}".format(query.split()[1]))).read())
        print("################################END")
    elif "unzip " in query:
        from zipfile import ZipFile
        file=query.split("unzip ")[1]
        if os.path.exists(file) is False:file=eval("file{}".format(query.split()[1]))
        if ".zip" not in file:raise Exception ("'"+file+"' is not a Zip File.")
        else:print("Contents in '"+file+"'."),ZipFile(file,"r").printdir()
    elif "zip" in query:
        from zipfile import ZipFile
        if query.split()[1]=="files":
            fileName=input("Enter The Name of New Zip File: ")
            mainIndex("show files")
            zipObj = ZipFile(fileName+".zip", 'w')
            for k in input("Write File Numbers Seperated By Commas: ").split(","):zipObj.write(eval("file{}".format(k)))
            return("'{0}.zip' Saved.".format(fileName))
        else:
            file=query.split("zip ")[1]
            if os.path.exists(file) is False:
                try:file=eval("file{}".format(query.split()[1]))
                except:raise Exception("'{}' not Exists".format(file))
            if os.path.isdir(file) is False:
                ZipFile('{}.zip'.format(file.split(".")[0]), 'w').write(file)
                return("'{0}.zip' Saved.".format(file.split(".")[0]))
            else:
                shutil.make_archive(file, 'zip', file)
                return("'{0}.zip' Saved.".format(file.split(".")[0]))
    elif "extract" in query:
        file=query.split("extract ")[1]
        if os.path.exists(file) is False:file=eval("file{}".format(query.split()[1]))
        mainIndex("zip "+file)
        from zipfile import ZipFile
        ZipFile(file,"r").extractall(),print("All Files Extracted.")
    elif "convert" in query:
        file=query.split()[1]
        if os.path.exists(file) is False:file=eval("file{}".format(query.split()[1]))
        if query.split()[3]=="pdf":
            if file.endswith(".docx"):
                from docx2pdf import convert
                convert(file,"C:/Users/Tania/Desktop/{}.pdf".format(file.split(".")[0]))
                return("'"+file.split(".")[0]+".pdf' Saved to Desktop.")
            elif file.endswith(".txt"):
                from fpdf import FPDF
                pdf = FPDF()
                pdf.alias_nb_pages(),pdf.add_page(),pdf.set_font('Times', '', 9)
                for x in open(file,"r"): 
                    pdf.cell(200, 10, txt = x, ln = 1, align = 'C')
                pdf.output("C:/Users/Tania/Desktop/{}.pdf".format(file.split(".")[0]))
                return("'"+file.split(".")[0]+".pdf' Saved to Desktop.")
    elif "upload " in query:
        import json
        uploadFile = eval("file{}".format(query.split()[1]))
        if "accessToken" in globals():
            if os.path.isfile(uploadFile):
                print("Uploading '{}'...".format(uploadFile))
                requests.post("https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
                              headers = {"Authorization": "Bearer " + accessToken},
                              files = {'data':('metadata',
                                               json.dumps({"name": uploadFile,"parents":[path[0]]}),
                                               'application/json; charset=UTF-8'),
                                       'file': open(os.path.abspath(uploadFile), "rb")})
            elif os.path.isdir(uploadFile):
                print("Zipping and Uploading '{}'...".format(uploadFile))
                shutil.make_archive(uploadFile, 'zip', os.path.abspath(uploadFile))
                uploadFile += ".zip"
                requests.post("https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",headers = {"Authorization": "Bearer " + accessToken},files = {'data':('metadata',json.dumps({"name": uploadFile}),'application/json; charset=UTF-8'),'file': open(uploadFile, "rb")}),os.remove(uploadFile)
            return("'{}' Uploaded to Google Drive ({}).".format(uploadFile,mainAddress))
        else:
            makeDriveGlobals()
            return mainWindowsExplorer(query)       
######################################################################################################################################
def mainDriveExplorer(query):
    global accessToken,path,prevPath,mainAddress
    if query=="info drive account":
        userAbout = eval(requests.get('https://www.googleapis.com/drive/v2/about',headers = {"Authorization": "Bearer " + accessToken}).text.replace("true","True").replace("false","False"))
        return("Name : {}\nE-Mail : {}\nProfile Image: {}\nAllotted Space: {} GB\nUsed Space: {} GB\nPermission ID: {}\nRoot Folder ID: {}".format(userAbout['user']['displayName'],userAbout['user']['emailAddress'],userAbout['user']['picture']['url'],round(int(userAbout['quotaBytesTotal'])*9.31*10**-10,3),round(int(userAbout['quotaBytesUsed'])*9.31*10**-10,3),userAbout['user']['permissionId'],userAbout['rootFolderId']))
    elif "goto" in query:
        folderData = eval("file{}".format(query.split("goto ")[1]))
        if folderData[2]=="application/vnd.google-apps.folder": #or folderData[2]=="application/vnd.google-apps.shortcut":
            prevPath,path = path,folderData
            return("Path Changed to '{}'.".format(path[1]))
        else:
            return("'{}' is Not a Valid Google Drive Folder.".format(folderData[1]))
    elif "delete" in query:
        fileData = eval("file{}".format(query.split("delete ")[1]))
        if input("Delete '{}' and it's Contents?: ".format(fileData[1])) in ['yes','y']:
            r = requests.delete("https://www.googleapis.com/drive/v3/files/{}".format(fileData[0]),headers = {"Authorization": "Bearer " + accessToken})
            return("'{}' Deleted.".format(fileData[1]))
    elif query=="back":
        path = prevPath
        return("Path Changed to '{}'.".format(path[1]))
    elif query=="path":print(path)
    elif query=="show files":
        fileList,startNum = [],1
        for k in eval(requests.get('https://www.googleapis.com/drive/v3/files?fields=*',headers = {"Authorization": "Bearer " + accessToken}).text.replace("false","False").replace("true","True"))['files']:
##            if k['mimeType']!="application/vnd.google-apps.folder":
            try:
                if path[0] in k['parents']:
                    exec("global file{0}\nfile{0}=('{1}','{2}','{3}')".format(startNum,k['id'],k['name'].translate(non_bmp_map),k['mimeType']))
                    if k['mimeType']=="application/vnd.google-apps.folder":# or k['mimeType']=="application/vnd.google-apps.shortcut":
                        fileList+=[[startNum,k['name'].translate(non_bmp_map),'Directory']]
                    else:
                        fileList+=[[startNum,k['name'].translate(non_bmp_map),'File']]
                    startNum += 1
            except:
                continue
        if fileList == []:
            return("No Files in '{}'.".format(path[1]))
        else:
##            print("Files in '{}':".format(path[1]))
            x = PrettyTable()
            x.field_names = ['No','Name','Type']
            x.title = path[1]
            for k in fileList:
                x.add_row(k)
            print(x)
##    elif query in ['show shared files','ssf']:
##        fileList,startNum = [],1
##        for k in eval(requests.get('https://www.googleapis.com/drive/v3/files?fields=*',headers = {"Authorization": "Bearer " + accessToken}).text.replace("false","False").replace("true","True"))['files']:
##            try:
##                exec("global file{0}\nfile{0}=('{1}','{2}','{3}')".format(startNum,k['id'],k['name'].translate(non_bmp_map),k['mimeType']))
##                if k['mimeType']=="application/vnd.google-apps.folder":# or k['mimeType']=="application/vnd.google-apps.shortcut":
##                    fileList+=[[startNum,k['name'].translate(non_bmp_map),'Directory']]
##                else:
##                    fileList+=[[startNum,k['name'].translate(non_bmp_map),'File']]
##                startNum += 1
##            except:
##                continue
##        if fileList == []:
##            return("No Files in '{}'.".format(path[1]))
##        else:
##            x = PrettyTable()
##            x.field_names = ['No','Name','Type']
##            x.title = path[1]
##            for k in fileList:
##                x.add_row(k)
##            print(x)

##            for num,file in enumerate(fileList):print("{}: {}".format(num+1,file))
##    elif query=="show folders":
##        r,folderList,startNum = requests.get('https://www.googleapis.com/drive/v3/files?fields=*',headers = {"Authorization": "Bearer " + accessToken}),[],1
##        for k in eval(r.text.replace("false","False").replace("true","True"))['files']:
##            if k['mimeType']=="application/vnd.google-apps.folder":
##                try:
##                    if path[0] in k['parents']:
##                        exec("global file{0}\nfile{0}=('{1}','{2}','{3}')".format(startNum,k['id'],k['name'],k['mimeType']))
##                        folderList+=[k['name']]
##                        startNum+=1
##                except:
##                    continue
##        if folderList == []:
##            return("No Folders in '{}'.".format(path[1]))
##        else:
##            print("Folders in '{}':".format(path[1]))
##            for num,file in enumerate(folderList):print("{}: {}".format(num+1,file))
    elif "download " in query:
        prevWinPath = os.getcwd()
        os.chdir("C:/Users/Tania/Desktop")
        fileData = eval("file{}".format(query.split("download ")[1]))
        open(fileData[1].replace(":","."),"wb").write(requests.get("https://www.googleapis.com/drive/v2/files/{}?alt=media&source=downloadUrl".format(fileData[0]),headers = {"Authorization": "Bearer "+ accessToken}).content)
        os.chdir(prevWinPath)
        return "'{}' Downloaded at Desktop.".format(fileData[1])
    elif "info " in query:
        r = requests.get('https://www.googleapis.com/drive/v3/files/{}?fields=id,name,mimeType,parents,createdTime,modifiedTime,size'.format(eval("file{}".format(query.split("info ")[1]))[0]),headers = {"Authorization": "Bearer " + accessToken})
        fileInfo = eval(r.text.replace("true","True").replace("false","False"))
        print("Name : {}\nSize : {} GB\nMime Type: {}\nFile ID: {}\nParent Folder ID: {}\nCreated Time: {}\nModified Time: {}".format(fileInfo['name'],round(int(fileInfo['size'])*9.31*10**-10,3),fileInfo['mimeType'].title(),fileInfo['id'],fileInfo['parents'][0],fileInfo['createdTime'],fileInfo['modifiedTime']))
    elif query=="change drive account":
        x = PrettyTable()
        x.field_names,x.title = ['No','Account'],'Google Drive Accounts'
        for k in mainDB.execute("select sNum,address from driveAccounts order by sNum").fetchall():x.add_row([k[0],k[1]])
        print(x)
        mainAddress = mainDB.execute("select sNum,address from driveAccounts order by sNum").fetchall()[int(input("Which Account Should I Use?: "))-1][1]
        mainAccount = mainDB.execute("select * from GoogleAPI where address = '{}'".format(mainAddress)).fetchone()
        mainDB.execute("UPDATE driveAccounts SET status = '' where status = 'In Use'"),mainDB.execute("UPDATE driveAccounts SET status = 'In Use' where address = '{}'".format(mainAddress)),mainDB.commit()
        accessToken = newAccessToken(mainAccount[2],mainAccount[3],mainAccount[4])
        path,prevPath = (getRootID(),"My Drive","application/vnd.google-apps.folder"),""
        return("Account Changed.")
    elif query=="drive login":
        global AnonymousDriveLogin
        AnonymousDriveLogin = True
        accessToken = input("Temporary Access Token: ")
        path,prevPath = (getRootID(),"My Drive","application/vnd.google-apps.folder"),""
    
######################################################################################################################################
def mainFilesIndex(query):
    global ExplorerMode
    if query=="drive mode":
        mainDB.execute("UPDATE Variables SET Value = '\"Drive\"' WHERE Variable = 'ExplorerMode' AND File = '{}'".format(os.path.basename(__file__))),mainDB.commit()
        ExplorerMode = 'Drive'
        makeDriveGlobals()
        return "Google Drive Explorer Mode Active."
    elif query in ['win mode','windows mode']:
        mainDB.execute("UPDATE Variables SET Value = '\"Windows\"' WHERE Variable = 'ExplorerMode' AND File = '{}'".format(os.path.basename(__file__))),mainDB.commit()
        ExplorerMode = 'Windows'
        return "Windows Explorer Mode Active."
    elif query=="gackup":
        from threading import Thread
        Thread(target=edithDriveBackup).start()
        return("EDITH Backup On Google Drive Started.")
    elif query=="backup":
        import datetime
        hour=datetime.datetime.now().hour
        minute=datetime.datetime.now().minute
        second=datetime.datetime.now().second
        shutil.copytree(startupPath,"G:/Backup/EDITH/EDITH {} {}.{}.{}".format(datetime.date.today(),hour,minute,second),symlinks=False)
        return ("EDITH Backup Completed.")
    elif query in ["info drive account","change drive account","drive login"]:
        if ExplorerMode == "Windows":
            if input("May I Turn On Drive Mode? Yes/No: ") in ['yes','y']:print(mainFilesIndex("drive mode"))
        return mainDriveExplorer(query)
    if ExplorerMode == "Windows":
        return mainWindowsExplorer(query)
    elif ExplorerMode == "Drive":
        return mainDriveExplorer(query)
######################################################################################################################################
if __name__=="__main__":
    startupPath="C:/Users/Tania/Desktop/Harshit/EDITH"
    mainDB = sqlite3.connect("C:/Users/Tania/Desktop/Harshit/EDITH/Data/mainDB.db")
    for x in mainDB.execute("SELECT * FROM Variables where File = '{}'".format(os.path.basename(__file__))).fetchall():exec("{} = {}".format(x[1],x[2]))
    if ExplorerMode=="Drive":makeDriveGlobals()
    while True:
        finalQuery = mainFilesIndex(input("Say Something: "))
        if finalQuery is not None:print(finalQuery)
else:
    startupPath=os.getcwd()
    mainDB = sqlite3.connect(startupPath+"/Data/mainDB.db")
    for x in mainDB.execute("SELECT * FROM Variables where File = '{}'".format(os.path.basename(__file__))).fetchall():exec("{} = {}".format(x[1],x[2]))
    if ExplorerMode=="Drive":makeDriveGlobals()
######################################################################################################################################
