import math
from decimal import Decimal


def log10(x):
    if x >0:
        return(Decimal.log10(x))
    elif x <0:
        return(-(Decimal.log10(-x)))
    else:
        return(0)


class BigNumber:
    def __init__(self,number,mantissa):
        self.number = Decimal(number)
        self.mantissa = Decimal(mantissa)
    
    def flowcheck(self):
        num = self.number
        lnum =log10(num)
        if lnum >= 1:
            self.number/= Decimal(10**math.floor(lnum))
            self.mantissa+= Decimal(math.floor(lnum))
        if lnum <= -1:
            self.number*= Decimal(10**math.floor(lnum))
            self.mantissa-= Decimal(math.floor(lnum))

    def bigAdd(self,another):
        if (self.number != 0.0 and another.number != 0.0):
            mdiff = self.number-another.mantissa+1
            if (0-mdiff) < 30:
                if mdiff >= 0:
                    numnew = (self.number**-mdiff+another.number)
                else:
                    numnew = (another.number**mdiff+self.number)
            else:
                numnew=self.number+another.number
        else:
            numnew=self.number+another.number
        if another.mantissa > self.mantissa:
            mantisnew = another.mantissa
        else:
            mantisnew = self.mantissa
        lnum =log10(numnew)
        if lnum >= 1: return(BigNumber(self.number/Decimal(10**math.floor(lnum)),self.mantissa+Decimal(math.floor(lnum))))
        elif lnum <= -1: return(BigNumber(self.number*Decimal(10**math.floor(lnum)),self.mantissa-Decimal(math.floor(lnum))))
        else: return(BigNumber(numnew,mantisnew))

    def bigMinus(self,another):
        if (self.number != 0.0 and another.number != 0.0):
            mdiff = self.number-another.mantissa+1
            if mdiff >= 0:
                numnew = (self.number**-mdiff-another.number)
            else:
                numnew = (another.number**mdiff-self.number)
        else:
            numnew=self.number+another.number
        if another.mantissa > self.mantissa:
            mantisnew = another.mantissa
        else:
            mantisnew = self.mantissa
        lnum =log10(numnew)
        if lnum >= 1:
            self.number/= Decimal(10**math.floor(lnum))
            self.mantissa+= Decimal(math.floor(lnum))
        if lnum <= -1:
            self.number*= Decimal(10**math.floor(lnum))
            self.mantissa-= Decimal(math.floor(lnum))
        return(BigNumber(numnew,mantisnew))

    def bigMul(self,another):
        if (self.number != 0.0 and another.number != 0.0):
            mdiff = self.number-another.mantissa+1
            if mdiff >= 0:
                numnew = (self.number**-mdiff*another.number)
            else:
                numnew = (another.number**mdiff*self.number)
        else:
            return(BigNumber(0,0))
        mantisnew = self.mantissa + another.mantissa
        lnum =log10(numnew)
        if lnum >= 1:
            self.number/= Decimal(10**math.floor(lnum))
            self.mantissa+= Decimal(math.floor(lnum))
        if lnum <= -1:
            self.number*= Decimal(10**math.floor(lnum))
            self.mantissa-= Decimal(math.floor(lnum))
        return(BigNumber(numnew,mantisnew))

    def bigDiv(self,another):
        if (self.number != 0.0 and another.number != 0.0):
            mdiff = self.number-another.mantissa+1
            if mdiff >= 0:
                numnew = (self.number**-mdiff/another.number)
            else:
                numnew = (another.number**mdiff/self.number)
        else:
            return(BigNumber(0,0))
        mantisnew = self.mantissa - another.mantissa
        lnum =log10(numnew)
        if lnum >= 1:
            self.number/= Decimal(10**math.floor(lnum))
            self.mantissa+= Decimal(math.floor(lnum))
        if lnum <= -1:
            self.number*= Decimal(10**math.floor(lnum))
            self.mantissa-= Decimal(math.floor(lnum))
        return(BigNumber(numnew,mantisnew))

    def bigCompare(self,another):
        if self.mantissa > another.mantissa: return(True,False,False)
        elif another.mantissa > self.mantissa: return(False,False,True) 
        elif self.number > another.number: return(True,False,False) 
        elif another.number > self.number: return(False,False,True) 
        else: return(False,True,False)
    

    def printBig(self):
        print(str(self.number)+"e+"+str(self.mantissa))




