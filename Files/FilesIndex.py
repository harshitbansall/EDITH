import os,shutil,re,sys,requests,sqlite3,datetime,magic
from prettytable import PrettyTable
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
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
    
######################################################################################################################################
def mainFilesIndex(query):
    global ExplorerMode
    if query in ['win mode','windows mode']:
        mainDB.execute("UPDATE Variables SET Value = '\"Windows\"' WHERE Variable = 'ExplorerMode' AND File = '{}'".format(os.path.basename(__file__))),mainDB.commit()
        ExplorerMode = 'Windows'
        return "Windows Explorer Mode Active."
    elif query=="backup":
        import datetime
        hour=datetime.datetime.now().hour
        minute=datetime.datetime.now().minute
        second=datetime.datetime.now().second
        shutil.copytree(startupPath,"G:/Backup/EDITH/EDITH {} {}.{}.{}".format(datetime.date.today(),hour,minute,second),symlinks=False)
        return ("EDITH Backup Completed.")
    return mainWindowsExplorer(query)
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
