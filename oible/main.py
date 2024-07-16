import pygame
import random
import math
from decimal import Decimal

import math
import time
import pickle
import os
pygame.font.init()
pygame.init
StaticFont = "Segou UI"
originalDisplayHeight = 640
originalDisplayWidth = 640
win = pygame.display.set_mode((640,640),pygame.RESIZABLE)
pygame.display.set_caption("Oidle")
suffixes = ['','K','M','B','T','Qd','Qn','Sx','Sp','Oc','No','Dc','Udc','Ddc','Tdc','Qadc',]

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
        if lnum >= 1: self.Mantissa, self.Exponent = number/Decimal(10**math.floor(lnum)),mantissa+Decimal(math.floor(lnum))
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


def getFilePath(file):
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, file)
    return(filename)

def getFileData(OriginalFilePath,OriginalData):
  filepath = getFilePath(OriginalFilePath)
  if not os.path.exists(filepath):
    return(OriginalData)
  with open(filepath, 'rb') as file:
    return pickle.load(file)

def writeFileData(OriginalFilePath, data):
    filepath = getFilePath(OriginalFilePath)
    if not os.path.exists(filepath):
        CreateFile(filepath)
        with open(filepath, 'wb') as file:
            pickle.dump(data, file)
    with open(filepath, 'wb') as file:
        pickle.dump(data, file)

def CreateFile(file):
    with open(file, 'x') as Openedfile:
        Openedfile.close

def LoadSave():
    # Job Stuff
    global JobPriorities
    JobPriorities = getFileData('data/JobPriorities.obdat', JobPriorities)
    global OibInJob
    OibInJob = getFileData('data/OibInJob.obdat', OibInJob)
    global displayJobPointer
    displayJobPointer = getFileData('data/displayJobPointer.obdat', displayJobPointer)
    global tabpointer
    tabpointer = getFileData('data/tabpointer.obdat',tabpointer)
    global JobsList
    JobsList = getFileData('data/JobsList.obdat', JobsList)
    #upgrade tab stuff
    global upgrades
    upgrades = getFileData('data/upgrades.obdat', upgrades)
    # Resources
    global oibs
    oibs = getFileData('data/oibs.obdat', oibs)
    global elixir
    elixir = getFileData('data/elixir.obdat', elixir)
    global health
    health = getFileData('data/health.obdat', health)
    global Ouire
    Ouire = getFileData('data/Ouire.obdat', Ouire)
    global tick
    tick = getFileData('data/tick.obdat', tick)
    global Land
    Land = getFileData('data/Land.obdat', Land)
    global JobEfficiency
    JobEfficiency = getFileData('data/JobEfficiency.obdat', JobEfficiency)
    global Buildings
    Buildings = getFileData('data/Buildings.obdat', Buildings)
    global tickset 
    tickset  = getFileData('data/tickset.obdat', tickset )

def Save():
    writeFileData('data/JobPriorities.obdat', JobPriorities)
    writeFileData('data/OibInJob.obdat', OibInJob)
    writeFileData('data/displayJobPointer.obdat', displayJobPointer)
    writeFileData('data/tabpointer.obdat',tabpointer)
    writeFileData('data/JobsList.obdat', JobsList)
    writeFileData('data/upgrades.obdat', upgrades)
    writeFileData('data/oibs.obdat', oibs)
    writeFileData('data/elixir.obdat', elixir)
    writeFileData('data/health.obdat', health)
    writeFileData('data/Ouire.obdat', Ouire)
    writeFileData('data/tick.obdat', tick)
    writeFileData('data/Land.obdat', Land)
    writeFileData('data/JobEfficiency.obdat', JobEfficiency)
    writeFileData('data/Buildings.obdat', Buildings)
    writeFileData('data/tickset.obdat', tickset)

# Calculate the smallest for height and width
# CalculateHeightANDwidthIntoSmallesT = CHADIST
def CHADIST():

    if win.get_width() > win.get_height():
        return(win.get_height())
    else:
        return(win.get_width())


# Draw Rectangle(resizes with screen)
def DrawRect(surface,R,G,B,X,Y,W,H):
    pygame.draw.rect((surface),(R,G,B), (((CHADIST()/originalDisplayWidth)*X)+((win.get_width()-CHADIST())/2),((CHADIST()/originalDisplayHeight)*Y)+((win.get_height()-CHADIST())/2), (CHADIST()/originalDisplayWidth)*W, (CHADIST()/originalDisplayHeight)*H))

# Draw Rectangle thats Centered(resizes with screen)
def DrawRectCentered(surface,R,G,B,X,Y,W,H):
    X = X-W/2
    Y = Y-H/2
    pygame.draw.rect((surface),(R,G,B), (((CHADIST()/originalDisplayWidth)*X)+((win.get_width()-CHADIST())/2),((CHADIST()/originalDisplayHeight)*Y)+((win.get_height()-CHADIST())/2), (CHADIST()/originalDisplayWidth)*W, (CHADIST()/originalDisplayHeight)*H))

# Draw Text at X,Y with specific size,font and RGB (resizes with screen)
def DrawText(text,X,Y,Size,font,R,G,B,Boolean):
    font = pygame.font.SysFont(font, math.floor((CHADIST()/originalDisplayHeight)*Size))
    textSurface = font.render(text, Boolean, (R, G, B))
    textrect = textSurface.get_rect(center= ( math.floor(((CHADIST()/originalDisplayWidth)*X)+((win.get_width()-CHADIST())/2)),math.floor(((CHADIST()/originalDisplayHeight)*Y)+((win.get_height()-CHADIST())/2)) ))
    win.blit(textSurface, textrect)

# Draw Text at X,Y with specific size,font and RGB (resizes with screen)
def DrawTextXCorner(text,X,Y,Size,font,R,G,B,Boolean):
    font = pygame.font.SysFont(font, math.floor((CHADIST()/originalDisplayHeight)*Size))
    textSurface = font.render(text, Boolean, (R, G, B))
    textrect = textSurface.get_rect(center= ( math.floor(((CHADIST()/originalDisplayWidth)*X)+((win.get_width()-CHADIST())/2)),math.floor(((CHADIST()/originalDisplayHeight)*Y)+((win.get_height()-CHADIST())/2)) ))
    win.blit(textSurface, textrect)

# Draws an Image
def DrawImage(X,Y,imgname,rotation):
    image = pygame.image.load(imgname)
    Size = image.get_size() 
    ratio = (CHADIST()/originalDisplayWidth)
    image1 = pygame.transform.scale(image ,(math.floor(ratio*Size[0]) , math.floor(ratio*Size[1])) ) 
    image2 = pygame.transform.rotate(image1, rotation)
    imgRect = image2.get_rect(center= ( math.floor(((CHADIST()/originalDisplayWidth)*X)+((win.get_width()-CHADIST())/2)),math.floor(((CHADIST()/originalDisplayHeight)*Y)+((win.get_height()-CHADIST())/2)) ))
    win.blit(image2, imgRect)


# get the position of the mouse
def mousePos():
    MousePosition = (pygame.mouse.get_pos())
    MousePositionX = MousePosition[0]-(((win.get_width())-CHADIST())/2)
    MousePositionY = MousePosition[1]-(((win.get_height())-CHADIST())/2)
    MousePositionX = (MousePositionX)/(CHADIST()/(originalDisplayWidth))
    MousePositionY = (MousePositionY)/(CHADIST()/(originalDisplayHeight))
    return(MousePositionX,MousePositionY)

# Button Click
def Button(bX,bY,sx,sy,iconimg,buttonpng1,buttonpng2,func):
    clicked = False
    mouseX,mouseY = mousePos()
    onButton = False
    if abs(mouseX-bX) < sx/2:
        if abs(mouseY-bY) < sy/2:
            onButton = True
    if onButton == False:
        if buttonpng1 != False:
            DrawImage(bX,bY,buttonpng1,0)
    if onButton == True:
        for i in pygame.event.get():
            if i.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
        if buttonpng2 != False:
            DrawImage(bX,bY,buttonpng2,0)
    if iconimg != 0:
        DrawImage(bX,bY,iconimg,0)
    return func(onButton,clicked)

def Icon(x,y,offset,size,iconimg,text,variable):
    if variable != "none":
        text = text + str(variable)
    if iconimg != 0:
        DrawImage(x,y,iconimg,0)
    DrawText(text,x+offset,y,size,"Arial",200,200,200,1)

def ReturnVal(ignore,Value):
    return (ignore,Value)

def CycleLeft(ignore, Boolean):
    if Boolean == True:
        varToCycle = JobsList.pop(0) 
        JobsList.append(varToCycle)

def CycleRight(ignore, Boolean):
    if Boolean == True:
        varToCycle = JobsList.pop(len(JobsList)-1) 
        JobsList.insert(0,varToCycle)
        

def Arrows(x,y,c1,c2):
    ignore,plusm = Button(x,y-48,16,16,0,"twoarrowup.png","twoarrowup.png",ReturnVal)
    ignore,plus = Button(x,y-16,16,16,0,"arrowup.png","arrowup.png",ReturnVal)
    ignore,minus = Button(x,y+16,16,16,0,"arrowdown.png","arrowdown.png",ReturnVal)
    ignore,minusm = Button(x,y+48,16,16,0,"twoarrowdown.png","twoarrowdown.png",ReturnVal)
    return((plusm*c2+plus*c1)-(minus*c1+minusm*c2))

def ChangeToHunter(ignore,clicked):
    if clicked == True:
        global displayJobPointer
        displayJobPointer=0

def ChangeToFarmer(ignore,clicked):
    if clicked == True:
        global displayJobPointer
        displayJobPointer=1

def ChangeToHealer(ignore,clicked):
    if clicked == True:
        global displayJobPointer
        displayJobPointer=2

def ChangeToBuilder(ignore,clicked):
    if clicked == True:
        global displayJobPointer
        displayJobPointer=3

def DisplayHunter():
    text= "These guys will run around getting food and miscallenous materials for you!"
    DrawText("Hunter",320,320,40,"Arial",200,200,200,1)
    DrawText(text,320,350,20,"Arial",200,200,200,1)
    DrawText("Job Priority",280,433,20,"Arial",200,200,200,1)
    DrawText(str(JobPriorities[0])+"%",280,453,20,"Arial",200,200,200,1)
    DrawText("Jobs Occupied",180,433,20,"Arial",200,200,200,1)
    DrawText(str(OibInJob[0]),180,453,20,"Arial",200,200,200,1)
    sumjob = sum(JobPriorities)
    newval =  Arrows(400,450,1,10)
    if (newval + sumjob) > 100:
        newval = 100-sumjob
    if (newval + JobPriorities[0]) < -100:
        JobPriorities[0] = -100
        return()
    JobPriorities[0]=(JobPriorities[0]+newval)

def DisplayFarmer():
    text= "These little bros will go around harvesting elixir for you!"
    DrawText("Farmer",320,320,40,"Arial",200,200,200,1)
    DrawText(text,320,350,20,"Arial",200,200,200,1)
    DrawText("Job Priority",280,433,20,"Arial",200,200,200,1)
    DrawText(str(JobPriorities[1])+"%",280,453,20,"Arial",200,200,200,1)
    DrawText("Jobs Occupied",180,433,20,"Arial",200,200,200,1)
    DrawText(str(OibInJob[1]),180,453,20,"Arial",200,200,200,1)
    sumjob = sum(JobPriorities)
    newval =  Arrows(400,450,1,10)
    if (newval + sumjob) > 100:
        newval = 100-sumjob
    if (newval + JobPriorities[1]) < -100:
        JobPriorities[1] = -100
        return()
    JobPriorities[1]=(JobPriorities[1]+newval)

def DisplayHealer():
    text= "Immortal oibs do sound fun."
    DrawText("Healer",320,320,40,"Arial",200,200,200,1)
    DrawText(text,320,350,20,"Arial",200,200,200,1)
    DrawText("Job Priority",280,433,20,"Arial",200,200,200,1)
    DrawText(str(JobPriorities[2])+"%",280,453,20,"Arial",200,200,200,1)
    DrawText("Jobs Occupied",180,433,20,"Arial",200,200,200,1)
    DrawText(str(OibInJob[2]),180,453,20,"Arial",200,200,200,1)
    sumjob = sum(JobPriorities)
    newval =  Arrows(400,450,1,10)
    if (newval + sumjob) > 100:
        newval = 100-sumjob
    if (newval + JobPriorities[2]) < -100:
        JobPriorities[2] = -100
        return()
    JobPriorities[2]=(JobPriorities[2]+newval)

def DisplayBuilder():
    text= "Can we fix it??"
    DrawText("Builder",320,320,40,"Arial",200,200,200,1)
    DrawText(text,320,350,20,"Arial",200,200,200,1)
    DrawText("Job Priority",280,433,20,"Arial",200,200,200,1)
    DrawText(str(JobPriorities[3])+"%",280,453,20,"Arial",200,200,200,1)
    DrawText("Jobs Occupied",180,433,20,"Arial",200,200,200,1)
    DrawText(str(OibInJob[3]),180,453,20,"Arial",200,200,200,1)
    sumjob = sum(JobPriorities)
    newval =  Arrows(400,450,1,10)
    if (newval + sumjob) > 100:
        newval = 100-sumjob
    if (newval + JobPriorities[3]) < -100:
        JobPriorities[3] = -100
        return()
    JobPriorities[3]=(JobPriorities[3]+newval)


    
def UpgradesTab():

    Icon(32,96,60,16,"elixir.png","Oib Elixir: ",elixir)
    Icon(152,96,40,16,"Ouire.png","Ouire: ",Ouire)
    DisplayUpgrades()

def BuildingsTab():

    Icon(32,96,40,16,"oib.png","Oibs: ",oibs)
    Icon(152,96,60,16,"elixir.png","Oib Elixir: ",elixir)
    DrawImage(320,220,"building.png",0)
    Icon(32,320,60,16,"oib.png","Builders: ",OibInJob[3])
    Icon(32,360,85,16,"oib.png","Total Employed Oibs: ",specSum(OibInJob))

JobPngsList = ["hunter.png","farmer.png","healer.png","builder.png"]
ChangeJobsList = [ChangeToHunter,ChangeToFarmer,ChangeToHealer,ChangeToBuilder]


def JobButton(x,y,i,canShow):
    if canShow == True:
        Button(x,y,64,64,JobPngsList[JobsList[i]],False,False,ChangeJobsList[JobsList[i]])
    else:
        DrawImage(x,y,JobPngsList[JobsList[i]],0)
        DrawImage(x,y,"LOCKED.png",0)
def JobsTab():
    canShow = [True,upgrades[0].bought,upgrades[2].bought,upgrades[1].bought]

    Icon(32,96,40,16,"oib.png","Oibs: ",oibs)
    Icon(152,96,60,16,"elixir.png","Oib Elixir: ",elixir)
    Icon(282,96,40,16,"Ouire.png","Ouire: ",Ouire)

    JobButton(64,200,0,canShow[JobsList[0]])
    JobButton(192,200,1,canShow[JobsList[1]])
    JobButton(320,200,2,canShow[JobsList[2]])
    JobButton(448,200,3,canShow[JobsList[3]])

    func = JobTabs[displayJobPointer]
    func()
    Button(50,288,128,128,"arrowleft.png",False,False,CycleLeft)
    Button(590,288,128,128,"arrowright.png",False,False,CycleRight)


def ChangeToJobs(ignore,clicked):
    if clicked == True:
        global tabpointer
        tabpointer=0
def ChangeToBuilding(ignore,clicked):
    if clicked == True:
        global tabpointer
        tabpointer=1
def ChangeToUpgrades(ignore,clicked):
    if clicked == True:
        global tabpointer
        tabpointer=2

def EnterJob(i,unemployed):
    priority = BigNumber(JobPriorities[i],-2)
    BigNumber.printBig(priority)
    if BigNumber.overZero(priority):
        OibInJob[i]=OibInJob[i]+(unemployed*priority)
    elif BigNumber.underZero(priority):
        OibInJob[i]=OibInJob[i]-(OibInJob[i]*-priority)


def OibChangeJobs():
    global oibs
    oibsinjob = specSum(OibInJob)
    unemployed = oibs-oibsinjob
    EnterJob(0,unemployed)
    EnterJob(1,unemployed)
    EnterJob(2,unemployed)
    EnterJob(3,unemployed)

def OibDoJobs():
    global JobEfficiency
    l = OibInJob[0]+1
    t = (specSum(OibInJob)+l)
    JobEfficiency = (Buildings*3+1)/t
    if JobEfficiency > 1:
        JobEfficiency = 1
    HunterJobDo()
    FarmerJobDo()
    HealerJobDo()
    BuilderJobDo()

def HunterJobDo():
    global elixir
    elixirPlus = OibInJob[0]/300
    elixir=(elixir+elixirPlus)
    global Ouire
    OuirePlus = OibInJob[0]/600
    Ouire=Ouire+OuirePlus

def FarmerJobDo():
    global elixir
    elixirPlus = (OibInJob[1])*JobEfficiency
    elixir=elixir+elixirPlus


def BuilderJobDo():
    global Buildings
    BuildingsPlus = OibInJob[3]/100*JobEfficiency
    Buildings+=BuildingsPlus

def HealerJobDo():
    global health
    health = OibInJob[2]*10/oibs
    if health > 2:
        health = 2


    
def OibsDie():
    global elixir
    global oibs
    if elixir >= oibs/10:
        elixir-=oibs/10
    else:
        oibsDie=round(oibs-(elixir*10))
        ratio = oibs/oibsDie
        if ratio > .75:
            oibsDie=round(oibsDie*.75)
        oibs-=oibsDie
        if oibs < 0:
            oibs = BigNumber(0,0)

def NewOibs():
    global elixir
    global oibs
    if oibs != 0:
        oldelixir = elixir
        oldoibs = oibs
        if elixir >= oibs/2:
            elixir=elixir-round(oldoibs)
            oibs=oibs+((oldelixir)/2)

class Upgrade:
    def __init__(self,x,y,picture,function):
        self.png = picture
        self.x = x
        self.y = y
        self.func = function
        self.bought = False

    def DoUpgrade(self):
        if self.bought == False:
            on, click = Button(self.x,self.y,16,16,self.png,"blankUpgrade.png","blankUpgradeHover.png",ReturnVal)
        else:
            on, click = Button(self.x,self.y,16,16,self.png,"boughtUpgrade.png","boughtUpgrade.png",ReturnVal)
        self.func(on, click)


def void(n,a):
    return(0)


def UpgradesCreate(amount,startX,startY,ywidth,xIncrement,yIncrement):
    global void
    global upgrades
    for i in range(0,amount):
        x = startX+xIncrement*(i%ywidth) 
        y = startY+yIncrement*(math.floor(i/ywidth)) 
        upgradeButton = Upgrade(x,y,"notexture.png",void)
        upgrades.append(upgradeButton)

def TryBuy(item,cost):
    boolean = True
    for i in range(0,len(item)):
        if cost[i] > item[i]:
            boolean = False
    return(boolean)
    


# farmerUpgrade
def upgradeI(onIt, click):
    if onIt:
        text= "Unlock farmers.. duh."
        DrawText("Farmer Upgrade(I)",320,320,40,"Arial",200,200,200,1)
        DrawText(text,320,350,20,"Arial",200,200,200,1)
        DrawText("Cost:",120,330,20,"Arial",200,200,200,1)
        if upgrades[0].bought == True:
            DrawText("Bought!",120,350,20,"Arial",200,200,200,1)
        else:
            DrawText("100 Elixir",120,350,20,"Arial",200,200,200,1)
            if click:
                global elixir
                CanBuy = TryBuy([elixir],[100])
                if CanBuy:
                    elixir-=100
                    upgrades[0].bought = True
                
# builderUpgrade
def upgradeII(onIt, click):
    if onIt:
        text= "Unlock Builders duh."
        DrawText("Builders Upgrade(II)",320,320,40,"Arial",200,200,200,1)
        DrawText(text,320,350,20,"Arial",200,200,200,1)
        DrawText("Cost:",120,330,20,"Arial",200,200,200,1)
        if upgrades[1].bought == True:
            DrawText("Bought!",120,350,20,"Arial",200,200,200,1)
        else:
            DrawText("100 Ouire",120,350,20,"Arial",200,200,200,1)
            if click:
                global Ouire
                CanBuy = TryBuy([Ouire],[100])
                if CanBuy:
                    Ouire-=100
                    upgrades[1].bought = True
                
# healerUpgrade
def upgradeIII(onIt, click):
    if onIt:
        text= "Unlock Healers."
        DrawText("Builders Upgrade(II)",320,320,40,"Arial",200,200,200,1)
        DrawText(text,320,350,20,"Arial",200,200,200,1)
        DrawText("Cost:",120,330,20,"Arial",200,200,200,1)
        if upgrades[1].bought == True:
            DrawText("Bought!",120,350,20,"Arial",200,200,200,1)
        else:
            DrawText("100 Ouire",120,350,20,"Arial",200,200,200,1)
            if click:
                global Ouire
                CanBuy = TryBuy([Ouire],[100])
                if CanBuy:
                    Ouire-=100
                    upgrades[1].bought = True
                
    


upgradePngs = ["farmerUpgrade.png","builderUpgrade.png",]
upgradeFunctions = [upgradeI,upgradeII]
def UpgradesInitialize():
    for i in range(0,len(upgradePngs)):
        upgrades[i].png = upgradePngs[i]
        upgrades[i].func = upgradeFunctions[i]


def DisplayUpgrades():
    for i in range(0,len(upgrades)):
        upgrade = upgrades[i]
        upgrade.DoUpgrade()



tabs = [JobsTab,BuildingsTab,UpgradesTab]
# Job Stuff
JobTabs = [DisplayHunter,DisplayFarmer,DisplayHealer,DisplayBuilder]
JobPriorities = [10,0,0,0]
OibInJob = [BigNumber(1,0),BigNumber(1,0),BigNumber(1,0),BigNumber(1,0)]
displayJobPointer = 0
tabpointer = 0
JobsList = [0,1,2,3]
#upgrade tab stuff
upgrades = []
# Resources
oibs = BigNumber(1,2)
elixir = BigNumber(0,0)
health = BigNumber(0,0)
Ouire = BigNumber(0,0)
tick = 0
Land = 0
JobEfficiency = BigNumber(0,0)
Buildings = BigNumber(0,0)
tickset = [10]
run = True
# initialize
UpgradesCreate(10,176,200,10,32,32)
UpgradesInitialize()
while run:
    timer = time.perf_counter()
    win.fill((0,0,0))
    DrawImage(320,32,"upperTab.png",0)
    Button(32,32,64,64,"buildings.png","button.png","button.png",ChangeToBuilding)
    Button(96,32,64,64,"job.png","button.png","button.png",ChangeToJobs)
    Button(160,32,64,64,"upgrades.png","button.png","button.png",ChangeToUpgrades)
    Tab = tabs[tabpointer]
    if tick > tickset[0]:
        tickset[0]=tick+50
        NewOibs()
    OibChangeJobs()
    OibDoJobs()
    
    Tab()
    tick+=1
    pygame.display.update()

    for event in pygame.event.get():
                if event.type == pygame.QUIT: run = False
    tsmin = 0.05-(time.perf_counter()-timer)
    if tsmin >=0:
        time.sleep(tsmin)
Save()
pygame.quit()
time.sleep(500)
