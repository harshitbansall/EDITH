from calendar import *
import datetime
from dateutil.relativedelta import relativedelta as rd
######################################################################################################################################
def strToDate(rawDay):
    rawDay=rawDay.split("/")
    if len(rawDay)==1:rawDay+=[str(datetime.date.today().month)]
    if len(rawDay)==2:rawDay+=[str(datetime.date.today().year)]
    rawDate,rawMonth,rawYear=rawDay
    return datetime.date(int(rawYear),int(rawMonth),int(rawDate))
######################################################################################################################################
def findDateInStr(st):
    for k in st.split():
        if "/" in k:return k
        else:
            try:
                if len(k)<4:st=st.replace(k, str(datetime.datetime.strptime(k, "%b").month))
                else:st=st.replace(k, str(datetime.datetime.strptime(k, "%B").month))
            except:continue
    dateList = [x for x in st.split() if x.isdigit()]
    if len(dateList)==3:
        if len(dateList[2])<4:return("/".join(dateList[0:2]))
        else:return("/".join(dateList))
    elif len(dateList)<3:return("/".join(dateList))
##    elif len(dateList)==4:return("/".join(dateList[0:2]),"/".join(dateList[2:4]))
##    elif len(dateList)==6:return("/".join(dateList[0:3]),"/".join(dateList[3:6]))
######################################################################################################################################
def daysOfDateInNextYears(rawDate, yearSpan = 0):
    if yearSpan == 0:
        return (strToDate(rawDate).strftime("%A"))
    else:
        nowYear, finalYear = datetime.date.today().year, datetime.date.today().year + yearSpan
        if nowYear < finalYear:
            yearList = [i for i in range(nowYear + 1,finalYear + 1)]
            print("Days On Which {} Will Occur in Next {} Years.".format(datetime.date(2020, int(rawDate.split("/")[1]), int(rawDate.split("/")[0])).strftime("%d %B"),abs(yearSpan)))
        else:
            yearList = [i for i in reversed(range(finalYear,nowYear))]
            print("Days On Which {} Occurred in Last {} Years.".format(datetime.date(2020, int(rawDate.split("/")[1]), int(rawDate.split("/")[0])).strftime("%d %B"),abs(yearSpan)))
        for k in yearList:print("'{1}' in {0}.".format(k, daysOfDateInNextYears(rawDate+"/"+str(k))))
######################################################################################################################################
def showMonth(phrase,rawYear = datetime.date.today().year):
    if "," in phrase:phrase = phrase.split(",")
    else:phrase = phrase.split()
    for k in phrase:
        try:rawYear = int(k)
        except:rawMonth = k
    if len(rawMonth)<4:rawMonth = datetime.datetime.strptime(rawMonth, "%b").month
    else:rawMonth = datetime.datetime.strptime(rawMonth, "%B").month
    print("\n"+month(rawYear,rawMonth)+"\n")
######################################################################################################################################
def mainCalendar(query):
    if "month" in query:
        showMonth(query.split("of ")[1])
    elif "timeline" in query:
        if "next" in query:yearSpan = int(query.split()[query.split().index("next")+1])
        elif "last" in query:yearSpan = int("-"+query.split()[query.split().index("last")+1])
        daysOfDateInNextYears(findDateInStr(query), yearSpan = yearSpan)
    elif "day on" in query:return ("There will be '{0}' on {1}.".format(strToDate(findDateInStr(query)).strftime("%A"),strToDate(findDateInStr(query)).strftime("%d %B %Y")))
    elif "between" in query:
        date1 = strToDate(findDateInStr(query.split(" and ")[0]))
        date2 = strToDate(findDateInStr(query.split(" and ")[1]))
        if "days" in query:return("{} Days are Between the Given Dates.".format(abs((date1-date2).days)))
        elif "time" in query:
            timebw = rd(date1,date2)
            return ("{} Years {} Months {} Days are Between the Given Dates.".format(abs(timebw.years),abs(timebw.months),abs(timebw.days)))
######################################################################################################################################
if __name__=="__main__":
    while True:
        finalResult = mainCalendar(input("Say Something: "))
        if finalResult is not None:print (finalResult)
######################################################################################################################################
