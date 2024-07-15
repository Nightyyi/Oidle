import math
from decimal import Decimal

suffixes = [' ','K','M','B','T','Qd','Qn','Sx','Sp','Oc','No','Dc','Udc','Ddc','Tdc','Qadc',]

def log10(x):
    if type(x) == int:
        x = Decimal(x)
    if type(x) == float:
        x = Decimal(x)
    if x >0:
        return(Decimal.log10(x))
    elif x <0:
        return(-(Decimal.log10(-x)))
    else:
        return(0)

def specSum(list):
    t = BigNumber(0,0)
    for i in range(0,len(list)):
        t=t+list[i]
    return(t)

class BigNumber:
    def __init__(self,number,mantissa):
        mantissa = round(mantissa)
        lnum = Decimal(round(log10(number)))
        number = Decimal(number)
        
        if lnum >= 1: self.number, self.mantissa = number/Decimal(10**math.floor(lnum)),mantissa+Decimal(math.floor(lnum))
        elif lnum <= -1: 
            self.number = number*Decimal(10**math.floor(lnum))
            self.mantissa = mantissa-Decimal(math.floor(lnum))
        else: self.number, self.mantissa = Decimal(number), Decimal(mantissa)
    
    def flowcheck(self):
        num = self.number
        lnum =log10(num)
        if lnum >= 1:
            self.number/= Decimal(10**math.floor(lnum))
            self.mantissa+= Decimal(math.floor(lnum))
        if lnum <= -1:
            self.number*= Decimal(10**math.floor(lnum))
            self.mantissa-= Decimal(math.floor(lnum))

    def __neg__(self):
        return(BigNumber(self.number*-1,self.mantissa))

    def __add__(self,another):
        if type(another) == int:
            another = BigNumber(another,0)
        if type(self) == int:
            self = BigNumber(self,0)
        
        if (self.number != 0.0 and another.number != 0.0):
            mdiff = self.mantissa-another.mantissa
            if abs(0-mdiff) < 30:
                if mdiff > 0:
                    numnew = (another.number*10**-(mdiff)+self.number)
                elif mdiff < 0:
                    numnew = (self.number*10**(mdiff)+another.number)
                else:
                    numnew = another.number+self.number
            elif another.mantissa > self.mantissa:
                numnew = another.number
            else:
                numnew = self.number
        else:
            numnew=self.number+another.number
            
        if another.mantissa > self.mantissa:
            mantisnew = another.mantissa
        else:
            mantisnew = self.mantissa
        return(BigNumber(numnew,mantisnew))
    
    def __sub__(self,another):
        if type(another) == int:
            another = BigNumber(another,0)
        if type(self) == int:
            self = BigNumber(self,0)
        
        if (self.number != 0.0 and another.number != 0.0):
            mdiff = self.mantissa-another.mantissa
            if abs(0-mdiff) < 30:
                if mdiff > 0:
                    numnew = (self.number-another.number*10**-(mdiff))
                elif mdiff < 0:
                    numnew = -(another.number-self.number*10**(mdiff))
                else:
                    numnew = another.number-self.number
                    return(BigNumber(numnew,0))
            elif another.mantissa > self.mantissa:
                numnew = another.number
            else:
                numnew = self.number
        else:
            numnew=self.number+another.number
        mantisnew = self.mantissa - another.mantissa
        return(BigNumber(numnew,mantisnew))

    def __mul__(self,another):
        if type(another) == float:
            another = BigNumber(another,0)
        if type(self) == float:
            self = BigNumber(self,0)
        if type(another) == int:
            another = BigNumber(another,0)
        if type(self) == int:
            self = BigNumber(self,0)
        if  type(another) == BigNumber:
            if (self.number != 0.0 and another.number != 0.0):
                mdiff = round(self.mantissa-another.mantissa)
                if abs(0-mdiff) < 10000:
                    numnew = (self.number*another.number)
                else:
                    if mdiff >= 0:
                        numnew = self.number
                    else:
                        numnew = another.number
            else:
                return(BigNumber(0,0))
            mantisnew = self.mantissa + another.mantissa
            lnum =log10(numnew)
        else:
            mantisnew = self.mantissa
            numnew = self.number*Decimal(another)
        return(BigNumber(numnew,mantisnew))

    def __truediv__(self,another):
        if type(another) == int:
            another = BigNumber(another,0)
        if type(self) == int:
            self = BigNumber(self,0)
        if (self.number != 0.0 and another.number != 0.0):
            numnew = (self.number/another.number)
        else:
            return(BigNumber(0,0))
        mantisnew = self.mantissa - another.mantissa
        return(BigNumber(numnew,mantisnew))

    def __round__(self):
        return(BigNumber(round(self.number),self.mantissa))

    def bigCompare(self,another):
        if self.mantissa > another.mantissa: return(True,False,False)
        elif another.mantissa > self.mantissa: return(False,False,True) 
        elif self.number > another.number: return(True,False,False) 
        elif another.number > self.number: return(False,False,True) 
        else: return(False,True,False)
    
    def __lt__(self,another):
        if type(another) != BigNumber:
            another = BigNumber(another,0)
        if type(self) != BigNumber:
            self = BigNumber(self,0)
        if self.mantissa > another.mantissa: return(True)
        elif another.mantissa > self.mantissa: return(False) 
        elif self.number > another.number: return(True) 
        elif another.number > self.number: return(False) 
        return(False)

    def __gt__(self,another):
        if type(another) != BigNumber:
            another = BigNumber(another,0)
        if type(self) != BigNumber:
            self = BigNumber(self,0)
        if self.mantissa > another.mantissa: return(False)
        elif another.mantissa > self.mantissa: return(True) 
        elif self.number > another.number: return(False) 
        elif another.number > self.number: return(True) 
        return(False)
    
    def __le__(self,another):
        if type(another) != BigNumber:
            another = BigNumber(another,0)
        if type(self) != BigNumber:
            self = BigNumber(self,0)
        if self.mantissa > another.mantissa: return(True)
        elif another.mantissa > self.mantissa: return(False) 
        elif self.number > another.number: return(True) 
        elif another.number > self.number: return(False) 
        return(True)
    
    def __ge__(self,another):
        if type(another) != BigNumber:
            another = BigNumber(another,0)
        if type(self) != BigNumber:
            self = BigNumber(self,0)
        if self.mantissa > another.mantissa: return(False)
        elif another.mantissa > self.mantissa: return(True) 
        elif self.number > another.number: return(False) 
        elif another.number > self.number: return(True) 
        return(True)
    
    def __eq__(self,another):
        if type(another) != BigNumber:
            another = BigNumber(another,0)
        if type(self) != BigNumber:
            self = BigNumber(self,0)
        if self.mantissa > another.mantissa: return(False)
        elif another.mantissa > self.mantissa: return(False) 
        elif self.number > another.number: return(False) 
        elif another.number > self.number: return(False) 
        return(True)
    
    def __ne__(self,another):
        if type(another) == str:
            return(True)
        elif type(self) == str:
            return(True)
        if type(another) != BigNumber:
            another = BigNumber(another,0)
        if type(self) != BigNumber:
            self = BigNumber(self,0)
        if self.mantissa > another.mantissa: return(True)
        elif another.mantissa > self.mantissa: return(True) 
        elif self.number > another.number: return(True) 
        elif another.number > self.number: return(True) 
        return(False)


    
    def __sum__(list):
        out = BigNumber(0,0)
        for x in enumerate(list,0):
            out=out+x
        return(out)

    
    def sum(list):
        return(specSum(list))
    


    def __str__(self):
        if (self.mantissa) < (len(suffixes)*3): 
            t = int(self.mantissa/3)
            if t < 0:
                t = 0
            return(str((math.floor((self.number*(10**(self.mantissa-(self.mantissa//3)*3)))*1000))//1000)+suffixes[t])
        else: return(str(math.floor((self.number*1000))//1000)+'e'+str(self.mantissa))
    

    def printBig(self):
        print(str(self.number)+"e+"+str(self.mantissa))
