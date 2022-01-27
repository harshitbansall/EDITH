import math,random
projectVelocity,projectAngle,projectRange,projectHeight,projectTime="","","","",""
whatisGiven=["",""]
def trajectoryofProjectile():
    import numpy as np
    import matplotlib.pyplot as plt
    global projectRange,projectTime
    if projectRange=="":
        projectRange=float(calcRangeofProjectile().split()[4])
    if projectTime=="":
        projectTime=float(calcTimeofProjectile().split()[4])
    timemat = float(projectTime)*np.linspace(0,1,float(projectRange)+10)[:,None]
    x,y=((float(projectVelocity)*timemat)*np.cos(float(projectAngle)/180.0*np.pi)),((float(projectVelocity)*timemat)*np.sin(float(projectAngle)/180.0*np.pi))-((4.9)*(timemat**2))
    plt.plot(x,y),plt.xlabel('Range'),plt.ylabel('Height'),plt.title('Projectile Trajectory'),plt.show()
def units(quantity):
    funcList3=[['meters/second',["velocity"]],['meters',["range","height"]],['seconds',["time"]]]
    return  (" ".join([" {}.".format(funcList3[x][0]) for x in range(len(funcList3)) if any(x==quantity for x in funcList3[x][1])]))
def calcSin(projectAngle,token):
    funcList4=[["math.sin(math.radians({}))".format(projectAngle),[1]],["2*math.sin(math.radians({}))*math.cos(math.radians({}))".format(projectAngle,projectAngle),[2]],["math.sin(math.radians({}))**2".format(projectAngle),[3]]]
    return ( eval (" ".join([funcList4[x][0] for x in range(len(funcList4)) if funcList4[x][1][0]==token])))
def calcVelocityofProjectile(*args):
    if args[0]==projectAngle:
        funcList5=[["((projectRange*9.8)/calcSin(projectAngle,2))**0.5",[projectRange]],["((projectHeight*19.6)/calcSin(projectAngle,3))**0.5",[projectHeight]],["(projectTime*9.8)/(2*calcSin(projectAngle,1))",[projectTime]]]
        projectVelocity=eval(" ".join([funcList5[x][0] for x in range(len(funcList5)) if any(y==args[1] for y in funcList5[x][1])]))
        if len(args)==3:return projectVelocity
        else:return ("The Calculated Velocity is "+str(round(projectVelocity,2))+units("velocity"))
    elif args[0]==projectHeight and args[1]==projectRange:return (calcVelocityofProjectile(math.degrees(math.atan(4*projectHeight/projectRange)),projectRange))
def calcAngle(*args):
    funcList9=[['math.degrees(math.asin((projectHeight*19.6)**0.5/projectVelocity))',[projectVelocity,projectHeight]],['(math.degrees(math.asin((projectRange*9.8)/(projectVelocity**2)))/2)',[projectVelocity,projectRange]]]
    return (eval ("\n".join([funcList9[x][0] for x in range(len(funcList9)) if list(args)==funcList9[x][1]])))
def calcRangeofProjectile():
    funcList8=[['"The Obtained Range is "+str(round(((projectVelocity**2)*calcSin(projectAngle,2))/9.8,2))+units("range")',[projectVelocity,projectAngle]],['(calcRangeofProjectile(projectVelocity,calcAngle(projectVelocity,projectHeight)))',[projectVelocity,projectHeight]],['(calcRangeofProjectile(calcVelocityofProjectile(projectAngle,projectHeight,"ask"),projectAngle))',[projectAngle,projectHeight]]]
    return(eval ("".join([funcList8[x][0] for x in range(len(funcList8)) if whatisGiven==funcList8[x][1]])))
def calcHeightofProjectile():
    funcList7=[['"The Obtained Height is {}{}".format(str(round(projectVelocity**2*calcSin(projectAngle,3)/19.6,2)),units("height"))',[projectVelocity,projectAngle]],['(calcHeightofProjectile(projectVelocity,calcAngle(projectVelocity,projectRange)))',[projectVelocity,projectRange]],['(calcHeightofProjectile(calcVelocityofProjectile(projectAngle,projectRange,"ask"),projectAngle))',[projectAngle,projectRange]]]
    return (eval ("\n".join([funcList7[x][0] for x in range(len(funcList7)) if whatisGiven==funcList7[x][1]])))
def calcTimeofProjectile():
    return (eval ('"The Obtained Time is {}{}".format(str(round(projectVelocity*calcSin(projectAngle,1)/4.9,3)),units("time"))'))
def mainProjectile(query):
    if "max" in query:
        query.remove("max")
        if query[1]=="range":query+=["angle","is","45"]
        elif query[1]=="height":query+=["angle","is","90"] 
    for i in range(query.count("is")):exec ('global project{0}\nproject{0}=float({1})\nwhatisGiven[{2}]=float({1})\nquery.remove("is")\n'.format(query[query.index('is')-1].title(),query[query.index('is')+1],i))
    if "show" in query:
        trajectoryofProjectile()
    else:
        return(eval("".join(["calc{}ofProjectile()".format(x) for x in ["Range","Height","Time","Velocity"] if x.lower()==query[query.index("find")+1]])))
