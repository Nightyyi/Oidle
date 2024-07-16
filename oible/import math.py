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
        mantissa = (mantissa)
        lnum = (log10(number))
        number = Decimal(number)
        if lnum >= 1: 
            self.Mantissa = number/Decimal(10**math.floor(lnum))
            self.Exponent = mantissa+Decimal(math.floor(lnum))
        elif lnum <= -1: 
            self.Mantissa = number*Decimal(10**math.floor(lnum))
            self.Exponent = mantissa-Decimal(math.floor(lnum))
        else: self.Mantissa, self.Exponent = Decimal(number), Decimal(mantissa)
    
    def flowcheck(self):
        num = self.Mantissa
        lnum =log10(num)
        if lnum >= 1:
            self.Mantissa/= Decimal(10**math.floor(lnum))
            self.Exponent+= Decimal(math.floor(lnum))
        if lnum <= -1:
            self.Mantissa*= Decimal(10**math.floor(lnum))
            self.Exponent-= Decimal(math.floor(lnum))

    def __neg__(self):
        return(BigNumber(self.Mantissa*-1,self.Exponent))

    def __add__(self,another):
        if type(another) == int:
            another = BigNumber(another,0)
        if type(self) == int:
            self = BigNumber(self,0)
        
        if (self.Mantissa != 0.0 and another.Mantissa != 0.0):
            mdiff = self.Exponent-another.Exponent
            if abs(0-mdiff) < 30:
                if mdiff > 0:
                    numnew = (another.Mantissa*10**-(mdiff)+self.Mantissa)
                elif mdiff < 0:
                    numnew = (self.Mantissa*10**(mdiff)+another.Mantissa)
                else:
                    numnew = another.Mantissa+self.Mantissa
            elif another.Exponent > self.Exponent:
                numnew = another.Mantissa
            else:
                numnew = self.Mantissa
        else:
            numnew=self.Mantissa+another.Mantissa
            
        if another.Exponent > self.Exponent:
            mantisnew = another.Exponent
        else:
            mantisnew = self.Exponent
        return(BigNumber(numnew,mantisnew))
    
    def __sub__(self,another):
        if type(another) == int:
            another = BigNumber(another,0)
        if type(self) == int:
            self = BigNumber(self,0)
        
        if (self.Mantissa != 0.0 and another.Mantissa != 0.0):
            mdiff = self.Exponent-another.Exponent
            if abs(0-mdiff) < 30:
                if mdiff > 0:
                    numnew = (self.Mantissa-another.Mantissa*10**-(mdiff))
                elif mdiff < 0:
                    numnew = -(another.Mantissa-self.Mantissa*10**(mdiff))
                else:
                    numnew = self.Mantissa-another.Mantissa
                    return(BigNumber(numnew,0))
            elif another.Exponent > self.Exponent:
                numnew = another.Mantissa
            else:
                numnew = self.Mantissa
        else:
            numnew=self.Mantissa+another.Mantissa
        mantisnew = self.Exponent - another.Exponent
        return(BigNumber(numnew,mantisnew))

    def __mul__(self,another):
        a = self
        b = another
        if type(b) == float:
            b = BigNumber(b,0)
        if type(a) == float:
            a = BigNumber(a,0)
        if type(b) == int:
            b = BigNumber(b,0)
        if type(a) == float:
            a = BigNumber(a,0)    
        if (a.Mantissa != 0.0 and b.Mantissa != 0.0):    
            numnew = (a.Mantissa*b.Mantissa)
            mantisnew = a.Exponent + b.Exponent
            return(BigNumber(numnew,mantisnew))
        else:
            return(BigNumber(0,0))


    def __truediv__(self,another):
        if type(another) == int:
            another = BigNumber(another,0)
        if type(self) == int:
            self = BigNumber(self,0)
        if (self.Mantissa != 0.0 and another.Mantissa != 0.0):
            numnew = (self.Mantissa/another.Mantissa)
        else:
            return(BigNumber(0,0))
        mantisnew = self.Exponent - another.Exponent
        return(BigNumber(numnew,mantisnew))

    def __round__(self):
        return(BigNumber(round(self.Mantissa),self.Exponent))

    def bigCompare(self,another):
        if self.Exponent > another.mantissa: return(True,False,False)
        elif another.mantissa > self.Exponent: return(False,False,True) 
        elif self.Mantissa > another.number: return(True,False,False) 
        elif another.number > self.Mantissa: return(False,False,True) 
        else: return(False,True,False)

    def overZero(self):
        return(self.Mantissa > 0)
    
    def underZero(self):
        return(self.Mantissa < 0)
            
    def __lt__(self,another):  
        if type(another) != BigNumber:
            another = BigNumber(another,0)
        if type(self) != BigNumber:
            self = BigNumber(self,0)
        if self.Exponent < another.Exponent: return(True)
        elif another.Exponent < self.Exponent: return(False) 
        elif self.Mantissa < another.Mantissa: return(True) 
        elif another.Mantissa < self.Mantissa: return(False) 
        else: return(False)

    def __gt__(self,another):
        if type(another) != BigNumber:
            another = BigNumber(another,0)
        if type(self) != BigNumber:
            self = BigNumber(self,0)
        if self.Exponent > another.Exponent: return(False)
        elif another.Exponent > self.Exponent: return(True) 
        elif self.Mantissa > another.Mantissa: return(False) 
        elif another.Mantissa > self.Mantissa: return(True) 
        return(False)
    
    def __le__(self,another):
        if type(another) != BigNumber:
            another = BigNumber(another,0)
        if type(self) != BigNumber:
            self = BigNumber(self,0)
        if self.Exponent > another.Exponent: return(True)
        elif another.Exponent > self.Exponent: return(False) 
        elif self.Mantissa > another.Mantissa: return(True) 
        elif another.Mantissa > self.Mantissa: return(False) 
        return(True)
    
    def __ge__(self,another):
        if type(another) != BigNumber:
            another = BigNumber(another,0)
        if type(self) != BigNumber:
            self = BigNumber(self,0)
        if self.Exponent > another.Exponent: return(False)
        elif another.Exponent > self.Exponent: return(True) 
        elif self.Mantissa > another.Mantissa: return(False) 
        elif another.Mantissa > self.Mantissa: return(True) 
        return(True)
    
    def __eq__(self,another):
        if type(another) != BigNumber:
            another = BigNumber(another,0)
        if type(self) != BigNumber:
            self = BigNumber(self,0)
        if self.Exponent > another.Exponent: return(False)
        elif another.Exponent > self.Exponent: return(False) 
        elif self.Mantissa > another.Mantissa: return(False) 
        elif another.Mantissa > self.Mantissa: return(False) 
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
        if self.Exponent > another.Exponent: return(True)
        elif another.Exponent > self.Exponent: return(True) 
        elif self.Mantissa > another.Mantissa: return(True) 
        elif another.Mantissa > self.Mantissa: return(True) 
        return(False)

    def __sum__(list):
        out = BigNumber(0,0)
        for x in enumerate(list,0):
            out=out+x
        return(out)

    def sum(list):
        return(specSum(list))
    
    def __str__(self):
        
        
        if (self.Exponent) < (len(suffixes)*3): 
            t = int(self.Exponent/3)
            if t < 0:
                t = 0
            aa = self.Exponent-(self.Exponent//3)*3
            num = math.floor((self.Mantissa*(10**aa)))
            return((((str(num))))+suffixes[t])
        else: return(str(math.floor((self.Mantissa*1000))//1000)+'e'+str(self.Exponent))
    

    def printBig(self):
        print(str(self.Mantissa)+"e+"+str(self.Exponent))
