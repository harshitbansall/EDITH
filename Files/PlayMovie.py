import os,difflib
def mainPlayMovie(query):
    query,path=query.replace("play ",""),'f:/MOVIES'
    for r, d, f in os.walk(path):
        for file in f:
            if '.mp4' in file or '.avi' in file or '.mkv' in file:
                if query.split()[len(query.split())-1][0]=="s" and query.split()[len(query.split())-1][3]=="e":
                    if 1>difflib.SequenceMatcher(None,query,file.lower()).ratio()>0.9:
                        os.startfile(os.path.join(r, file))
                        break
                else:
                    if 1>difflib.SequenceMatcher(None,query,file.lower()).ratio()>0.6:
                        os.startfile(os.path.join(r, file))
                        break
if __name__=="__main__":
    while True:
        mainPlayMovie(input("Say Something: "))
