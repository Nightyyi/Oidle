import math
from decimal import Decimal
import decimal

suffixes = [
    " ",
    "K",
    "M",
    "B",
    "T",
    "Qd",
    "Qn",
    "Sx",
    "Sp",
    "Oc",
    "No",
    "Dc",
    "Udc",
    "Ddc",
    "Tdc",
    "Qadc",
]

def negLog10(dec: Decimal):
    if dec >0:
        return(Decimal.log10(dec))
    elif dec <0:
        return((Decimal.log10(-dec)))
    else:
        return(-1)



def specSum(list):
    t = BigNumber(0, 0)
    for i in range(0, len(list)):
        t = t + list[i]
    return t


class BigNumber:
    def __init__(self, inputMantissa, inputExponent = Decimal(0)):
        ## if the mantissa is zero why would it have a exponent? duh
        if inputMantissa == 0:
            self.Mantissa, self.Exponent = Decimal(0), Decimal(0)
            return
        ## im paranoid
        inputMantissa = Decimal(inputMantissa)
        ## we have to find how many 0's the mantissa has
        lnum = math.floor(negLog10(inputMantissa))
        if lnum != 0:
            ##check if its negative
            if Decimal.is_signed(inputMantissa):
                ## is negative which means that.
                ## smaller is bigger, smaller is smaller
                ## every magnitude that we go up will be going towards zero instead.
                ## much the same like the positive version, just in the other way
                self.Mantissa = inputMantissa * Decimal(10 ** (lnum))
                self.Exponent = inputExponent - Decimal((lnum))
                
            else:
                ## wasnt negative so.
                ## bigger is bigger, smaller is smaller, here you can see that
                ## every magnitude upwards we will push mantissa down by 1 digit
                ##                                                       |
                ##   Decimal(10 ** (lnum)) <---------------/-------------/
                ##                                        \/
                self.Mantissa = inputMantissa / Decimal(10 ** (lnum)) 
                ## then we will add 1 to the Exponent as it represents magnitude 
                self.Exponent = inputExponent + Decimal((lnum))  
        ## no change in magnitude so just pass it like normal
        else:
            self.Mantissa, self.Exponent = Decimal(inputMantissa), Decimal(inputExponent)

    def __neg__(self):
        return BigNumber(self.Mantissa * -1, self.Exponent)

    def __add__(self, another):
        if type(another) == int:
            another = BigNumber(another, 0)
        if type(self) == int:
            self = BigNumber(self, 0)

        if self.Mantissa != 0.0 and another.Mantissa != 0.0:
            mdiff = self.Exponent - another.Exponent
            if abs(0 - mdiff) < 30:
                if mdiff > 0:
                    numnew = another.Mantissa * 10 ** -(mdiff) + self.Mantissa
                elif mdiff < 0:
                    numnew = self.Mantissa * 10 ** (mdiff) + another.Mantissa
                else:
                    numnew = another.Mantissa + self.Mantissa
            elif another.Exponent > self.Exponent:
                numnew = another.Mantissa
            else:
                numnew = self.Mantissa
        else:
            numnew = self.Mantissa + another.Mantissa

        if another > self:
            mantisnew = another.Exponent
        else:
            mantisnew = self.Exponent
        return BigNumber(numnew, mantisnew)

    def __sub__(self, another):
        if type(another) == int:
            another = BigNumber(another, 0)
        if type(self) == int:
            self = BigNumber(self, 0)

        if self.Mantissa != 0.0:
            mdiff = self.Exponent - another.Exponent
            if abs(0 - mdiff) < 30:
                if mdiff > 0:
                    numnew = self.Mantissa - another.Mantissa * 10 ** -(mdiff)
                elif mdiff < 0:
                    numnew = -(another.Mantissa - self.Mantissa * 10 ** (mdiff))
                else:
                    numnew = self.Mantissa - another.Mantissa
                    return BigNumber(numnew, 0)
            elif another.Exponent > self.Exponent:
                numnew = another.Mantissa
            else:
                numnew = self.Mantissa
        else:
            numnew = - another.Mantissa
        mantisnew = self.Exponent 
        return BigNumber(numnew, mantisnew)

    def __mul__(self, another):
        if type(another) == float:
            another = BigNumber(another, 0)
        if type(self) == float:
            self = BigNumber(self, 0)
        if type(another) == int:
            another = BigNumber(another, 0)
        if type(self) == float:
            self = BigNumber(self, 0)
        if self.Mantissa != 0.0 and another.Mantissa != 0.0:
            numnew = self.Mantissa * another.Mantissa
            mantisnew = self.Exponent + another.Exponent
            return BigNumber(numnew, mantisnew)
        else:
            return BigNumber(0, 0)

    def __truediv__(self, another):
        if type(another) == int:
            another = BigNumber(another, 0)
        if type(self) == int:
            self = BigNumber(self, 0)
        if self.Mantissa != 0.0 and another.Mantissa != 0.0:
            numnew = self.Mantissa / another.Mantissa
        else:
            return BigNumber(0, 0)
        mantisnew = self.Exponent - another.Exponent
        return BigNumber(numnew, mantisnew)

    def __round__(self):
        return BigNumber((round(self.Mantissa*10000))/10000, self.Exponent)


    def overZero(self):
        return self.Mantissa > 0

    def underZero(self):
        return self.Mantissa < 0

    ## (self) lesser than (another)
    def __lt__(self, another):
        ## first check if the type is str
        if (type(another) == str):
            ## if so just return false:
            return False
        ## set another and self to BigNumber class if theyre not already it.
        if (type(another) != BigNumber):
            another = BigNumber(another, 0)
        if (type(self) != BigNumber):
            self = BigNumber(self, 0)
        ## take the sign of both mantissa's.
        selfSign = Decimal.is_signed(self.Mantissa)
        anotherSign = Decimal.is_signed(another.Mantissa)

        if (selfSign == anotherSign):
            ## if the sign is positive.
            if (not selfSign):
                ## check which exponent is bigger.
                if (self.Exponent < another.Exponent):
                    return True
                elif (self.Exponent > another.Exponent):
                    return False
                else:
                    ## now check which mantissa is bigger.
                    if (self.Mantissa < another.Mantissa):
                        return True
                    elif (self.Mantissa > another.Mantissa):
                        return False
                    else:
                        # womp womp
                        return False
            # sign is not positive, so bigger is smaller, smaller is bigger.
            else:
                ## check which exponent is bigger.
                if (self.Exponent < another.Exponent):
                    return False
                elif (self.Exponent > another.Exponent):
                    return True
                else:
                    ## now check which mantissa is bigger.
                    if (self.Mantissa < another.Mantissa):
                        return False
                    elif (self.Mantissa > another.Mantissa):
                        return True
                    else:
                        # meow
                        return False
        # atleast one of the inputs is negative.
        else:
            # find which one is negative.
            if (selfSign):
                # self.mantissa would be negative, and another.mantissa would be positive.
                # -x < x is always True
                return True
            else:
                # self.mantissa would be positive, and another.mantissa would be negative.
                # x < -x is always False
                return False

    ## (self) greater than (another)
    def __gt__(self, another):
        ## first check if the type is str
        if (type(another) == str):
            ## if so just return false:
            return False
        ## set another and self to BigNumber class if theyre not already it.
        if (type(another) != BigNumber):
            another = BigNumber(another, 0)
        if (type(self) != BigNumber):
            self = BigNumber(self, 0)
        ## take the sign of both mantissa's.
        selfSign = Decimal.is_signed(self.Mantissa)
        anotherSign = Decimal.is_signed(another.Mantissa)

        if (selfSign == anotherSign):
            ## if the sign is positive.
            if (not selfSign):
                ## check which exponent is bigger.
                if (self.Exponent < another.Exponent):
                    return False
                elif (self.Exponent > another.Exponent):
                    return True
                else:
                    ## now check which mantissa is bigger.
                    if (self.Mantissa < another.Mantissa):
                        return False
                    elif (self.Mantissa > another.Mantissa):
                        return True
                    else:
                        # womp womp
                        return False
            # sign is not positive, so bigger is smaller, smaller is bigger.
            else:
                ## check which exponent is bigger.
                if (self.Exponent < another.Exponent):
                    return True
                elif (self.Exponent > another.Exponent):
                    return False
                else:
                    ## now check which mantissa is bigger.
                    if (self.Mantissa < another.Mantissa):
                        return True
                    elif (self.Mantissa > another.Mantissa):
                        return False
                    else:
                        # meow
                        return False
        # atleast one of the inputs is negative.
        else:
            # find which one is negative.
            if (selfSign):
                # self.mantissa would be negative, and another.mantissa would be positive.
                # -x > x is always False
                return False
            else:
                # self.mantissa would be positive, and another.mantissa would be negative.
                # x > -x is always True
                return True

    ## (self) lesser than or equal to (another)
    def __le__(self, another):
        ## first check if the type is str
        if (type(another) == str):
            ## if so just return false:
            return False
        ## set another and self to BigNumber class if theyre not already it.
        if (type(another) != BigNumber):
            another = BigNumber(another, 0)
        if (type(self) != BigNumber):
            self = BigNumber(self, 0)
        ## take the sign of both mantissa's.
        selfSign = Decimal.is_signed(self.Mantissa)
        anotherSign = Decimal.is_signed(another.Mantissa)

        if (selfSign == anotherSign):
            ## if the sign is positive.
            if (not selfSign):
                ## check which exponent is bigger.
                if (self.Exponent < another.Exponent):
                    return True
                elif (self.Exponent > another.Exponent):
                    return False
                else:
                    ## now check which mantissa is bigger.
                    if (self.Mantissa < another.Mantissa):
                        return True
                    elif (self.Mantissa > another.Mantissa):
                        return False
                    else:
                        # return True since it seems like both mantissa and exponent are equal, including the sign
                        return True
            # sign is not positive, so bigger is smaller, smaller is bigger.
            else:
                ## check which exponent is bigger.
                if (self.Exponent < another.Exponent):
                    return False
                elif (self.Exponent > another.Exponent):
                    return True
                else:
                    ## now check which mantissa is bigger.
                    if (self.Mantissa < another.Mantissa):
                        return False
                    elif (self.Mantissa > another.Mantissa):
                        return True
                    else:
                        # return True since it seems like both mantissa and exponent are equal, including the sign
                        return True
        # atleast one of the inputs is negative.
        else:
            # find which one is negative.
            if (selfSign):
                # self.mantissa would be negative, and another.mantissa would be positive.
                # -x < x is always True
                return True
            else:
                # self.mantissa would be positive, and another.mantissa would be negative.
                # x < -x is always False
                return False

    ## (self) greater than or equal to (another)
    def __ge__(self, another):
        ## first check if the type is str
        if (type(another) == str):
            ## if so just return false:
            return False
        ## set another and self to BigNumber class if theyre not already it.
        if (type(another) != BigNumber):
            another = BigNumber(another, 0)
        if (type(self) != BigNumber):
            self = BigNumber(self, 0)
        ## take the sign of both mantissa's.
        selfSign = Decimal.is_signed(self.Mantissa)
        anotherSign = Decimal.is_signed(another.Mantissa)

        if (selfSign == anotherSign):
            ## if the sign is positive.
            if (not selfSign):
                ## check which exponent is bigger.
                if (self.Exponent < another.Exponent):
                    return False
                elif (self.Exponent > another.Exponent):
                    return True
                else:
                    ## now check which mantissa is bigger.
                    if (self.Mantissa < another.Mantissa):
                        return False
                    elif (self.Mantissa > another.Mantissa):
                        return True
                    else:
                        # return True since it seems like both mantissa and exponent are equal, including the sign
                        return True
            # sign is not positive, so bigger is smaller, smaller is bigger.
            else:
                ## check which exponent is bigger.
                if (self.Exponent < another.Exponent):
                    return True
                elif (self.Exponent > another.Exponent):
                    return False
                else:
                    ## now check which mantissa is bigger.
                    if (self.Mantissa < another.Mantissa):
                        return True
                    elif (self.Mantissa > another.Mantissa):
                        return False
                    else:
                        # return True since it seems like both mantissa and exponent are equal, including the sign
                        return True
        # atleast one of the inputs is negative.
        else:
            # find which one is negative.
            if (selfSign):
                # self.mantissa would be negative, and another.mantissa would be positive.
                # -x > x is always False
                return False
            else:
                # self.mantissa would be positive, and another.mantissa would be negative.
                # x > -x is always True
                return True

    ## (self) equal to (another)
    def __eq__(self, another):
        ## first check if the type is str
        if (type(another) == str):
            ## if so just return false
            return False
        ## set another and self to BigNumber class if theyre not already it.
        if (type(another) != BigNumber):
            another = BigNumber(another, 0)
        if (type(self) != BigNumber):
            self = BigNumber(self, 0)
        ## take the sign of both mantissa's.
        selfSign = Decimal.is_signed(self.Mantissa)
        anotherSign = Decimal.is_signed(another.Mantissa)
        if (selfSign == anotherSign):
            ## now check if the exponents arent the same
            if (self.Exponent != another.Exponent):
                return False
            else:
                ## now check if the mantissas arent the same
                if (self.Mantissa != another.Mantissa):
                    return False
                else:
                    # return True since it seems like both mantissa and exponent are equal, including the sign
                    return True
                
        # atleast one of the inputs is negative.
        else:
            # the signs are always different here, so they are inequal.
            return(False)

    ## (self) not equal to (another)
    def __ne__(self, another):
        ## first check if the type is str
        if (type(another) == str):
            ## if so just return True
            return True
        ## set another and self to BigNumber class if theyre not already it.
        if (type(another) != BigNumber):
            another = BigNumber(another, 0)
        if (type(self) != BigNumber):
            self = BigNumber(self, 0)
        ## take the sign of both mantissa's.
        selfSign = Decimal.is_signed(self.Mantissa)
        anotherSign = Decimal.is_signed(another.Mantissa)
        if (selfSign == anotherSign):
            ## now check if the exponents arent the same
            if (self.Exponent != another.Exponent):
                return True
            else:
                ## now check if the mantissas arent the same
                if (self.Mantissa != another.Mantissa):
                    return True
                else:
                    # return False since it seems like both mantissa and exponent are equal, including the sign
                    return False
                
        # atleast one of the inputs is negative.
        else:
            # the signs are always different here, so they are inequal.
            return(True)

    def __sum__(list):
        out = BigNumber(0, 0)
        for x in enumerate(list, 0):
            out = out + x
        return out

    def logxy(self,another):
        if (self > 0):
            if not isinstance(another, Decimal):
                another = Decimal(another)
            newmantissa = (Decimal.log10(self.Mantissa)+self.Exponent)/Decimal.log10(another)
            return(BigNumber(newmantissa))
        else:
            return(BigNumber(0,0))

    def sum(list):
        return specSum(list)

    def __str__(self):

        if (self.Exponent) < (len(suffixes) * 3):
            t = int(self.Exponent / 3)
            if t < 0:
                t = 0
            aa = self.Exponent - (self.Exponent // 3) * 3
            num = math.floor((self.Mantissa * (10**aa)))
            return (((str(num)))) + suffixes[t]
        else:
            return (
                str(math.floor((self.Mantissa * 1000)) // 1000)
                + "e"
                + str(self.Exponent)
            )

    def printBig(self):
        print(str(self.Mantissa) + "e+" + str(self.Exponent))





