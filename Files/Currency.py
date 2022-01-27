dollar={"rupees":75.53,"yen":107.50,"dirham":3.67,"euro":0.91,"pound":0.81}
def mainCurrency(query):
    splitQuery=query.split()
    value,fromCurrency,toCurrency=splitQuery[1],splitQuery[2],splitQuery[4]
    if fromCurrency=="dollars":finalValue=float(value)*dollar[toCurrency]
    elif toCurrency=="dollars":finalValue=float(value)/dollar[fromCurrency]
    else:finalValue=(float(value)/dollar[fromCurrency])*dollar[toCurrency]
    return (str(value)+" "+fromCurrency.capitalize()+" : "+str(round(finalValue,2))+" "+toCurrency.capitalize())
    
    
