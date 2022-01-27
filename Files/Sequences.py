######################################################################################################################################
def findTerm(x,Series,token):
    if token=="ap":return float(Series[0])+(float(x)-1)*(float(Series[1])-float(Series[0]))
    else:return float(Series[0])*(float(Series[1])/float(Series[0]))**(float(x)-1)
######################################################################################################################################
def checkSeries(givenSeries,token):
    if token=="ap":
        y=2
        for x in range(1,len(givenAP)-1):
            if float(givenAP[x])-float(givenAP[x-1])==float(givenAP[x+1])-float(givenAP[x]):
                y+=1
        if y==len(givenSeries):return ("AP")
        else:return ("NOT AP")
    elif token=="gp":
        y=2
        for x in range(1,len(givenGP)-1):
            if float(givenGP[x])/float(givenGP[x-1])==float(givenGP[x+1])/float(givenGP[x]):y+=1
        if y==len(givenSeries):return ("GP")
        else:return ("NOT GP")
    else:
        if checkSeries(givenSeries,"ap")=="NOT AP":answer=checkSeries(givenSeries,"gp")
######################################################################################################################################
def checkAP(givenAP):
    y=2
    for x in range(1,len(givenAP)-1):
        if float(givenAP[x])-float(givenAP[x-1])==float(givenAP[x+1])-float(givenAP[x]):y+=1
    if y==len(givenAP):return ("yes")
    else:return ("no")
######################################################################################################################################
def checkGP(givenGP):
    y=2
    for x in range(1,len(givenGP)-1):
        if float(givenGP[x])/float(givenGP[x-1])==float(givenGP[x+1])/float(givenGP[x]):
            y+=1
    if y==len(givenGP):return ("yes")
    else:return ("no")
######################################################################################################################################
def findWhatIsGiven(query,token):
    splitQuery=query.split()
    if token=="ap":return (splitQuery[splitQuery.index("ap")+1].split(","))
    elif token=="gp":return (splitQuery[splitQuery.index("gp")+1].split(","))
    elif token=="series":return(splitQuery[splitQuery.index("series")+1].split(","))
######################################################################################################################################
def findWhatIsAsked(query):
    splitQuery=query.split()
    if "find the" in query:whatisAsked=splitQuery[splitQuery.index("find")+2]
    elif "find" in query:whatisAsked=splitQuery[splitQuery.index("find")+1]
    return (whatisAsked)
######################################################################################################################################
def mainSequences(query):
    splitQuery=query.split()
    if "ap" in query:
        givenAP=findWhatIsGiven(query,"ap")
        token=checkAP(givenAP)
        if token=="yes":
            whatisAsked=findWhatIsAsked(query)
            foundTerm=findTerm(whatisAsked,givenAP,"ap")
            return ("The "+str(whatisAsked)+"th term is "+str(foundTerm)+".")
        else:return ("The given values do not form an AP.")
    elif "gp" in query:
        givenGP=findWhatIsGiven(query,"gp")
        token=checkGP(givenGP)
        if token=="yes":
            whatisAsked=findWhatIsAsked(query)
            foundTerm=findTerm(whatisAsked,givenGP,"gp")
            return ("The "+str(whatisAsked)+"th term is "+str(foundTerm)+".")
        else:return ("The given values do not form an GP.")
    else:
        givenSeries=findWhatIsGiven(query,"series")
        token1=checkAP(givenSeries)
        token2=checkGP(givenSeries)
        if token1=="yes":
            whatisAsked=findWhatIsAsked(query)
            foundTerm=findTerm(whatisAsked,givenSeries,"ap")
            return ("The "+str(whatisAsked)+"th term is "+str(foundTerm)+".")
        elif token2=="yes":
            whatisAsked=findWhatIsAsked(query)
            foundTerm=findTerm(whatisAsked,givenSeries,"gp")
            return ("The "+str(whatisAsked)+"th term is "+str(foundTerm)+".")
        else:return ("The given values do not form an AP or GP.")
######################################################################################################################################
