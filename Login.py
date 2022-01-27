import hashlib,os
def hash(y):
    hasher = hashlib.md5(y.encode())
    return (hasher.hexdigest())
def askCredentials(x):
    if x!=0:
        os.chdir("Data")
        username=input("Enter Username: ")
        password=input("Enter Password: ")
        mainPass,mainUser=hash(password),hash(username)
        if mainUser=="c724418d2617be3a1f16c5caa3b6987c" and mainPass=="50680400cbc42d694023e2e3653d63b1":
            open("_Log_.txt","a").write("\n{}   {}   GRANTED".format(username,mainPass))
            import EDITH as edith
        else:
            open("_Log_.txt","a").write("\n{}           {}        DENIED".format(username,password))
            x-=1
            print("Wrong Username or Password")
            print(x,"Chances Left.")
            os.chdir("..")
            askCredentials(x)
    else:
        exit()
if __name__=="__main__":askCredentials(3)
