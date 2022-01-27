import math,re
def mainMathFuncs(*args):
    query=args[0]
    if "+" in query or "-" in query or "/" in query or "*" in query:
        for x in re.split('[+-/*]',query):
            if "sin" in x or "cos" in x or "sec" in x or "tan" in x or "cot" in x or "log" in x:
                query=query.replace(x,str(mainMathFuncs(x,"ask")))
        return ("'{}' is Equal to '{}'.".format(args[0],round(eval(query),3)))
    else:
        if "find" in query:whatisAsked=query.split()[query.split().index("find")+1]
        else:whatisAsked=query.split()[0]
        if len(list(whatisAsked))>3:mathFunc,mathArg=whatisAsked[0:3],whatisAsked[3:]
        else:mathFunc,mathArg=whatisAsked,query.split()[query.split().index(whatisAsked)+1]
        if mathFunc=="sin":value=round(math.sin(math.radians(float(mathArg))),3)
        elif mathFunc=="cos":value=round(math.cos(math.radians(float(mathArg))),3)
        elif mathFunc=="sec":value=round(1/math.cos(math.radians(float(mathArg))),3)
        elif mathFunc=="tan":value=round(math.tan(math.radians(float(mathArg))),3)
        elif mathFunc=="cot":value=round(1/math.tan(math.radians(float(mathArg))),3)
        elif mathFunc=="log":
            if "base" in query:value=round(math.log(float(mathArg),float(query.split()[query.split().index("base")+1])),3)
            else:value=round(math.log(float(mathArg)),3)
        if len(args)!=2:
            if "base" not in query:return "The Value of {} {} is '{}' .".format(mathFunc.title(),str(mathArg),str(value))
            else:return "The Value of {} {} to Base {} is '{}' .".format(mathFunc.title(),str(mathArg),query.split()[query.split().index("base")+1],str(value))
        else:return value

if __name__=="__main__":
    while True:
        print(mainMathFuncs(input("Say Something: ")))
