from appJar import gui
from colour import Color
import math

def openWindow(subWindow):
    app.showSubWindow(subWindow)

def updateCommods(temp):
    for i in ["basic","ship","herb","mineral","cloth","dye","paint","enamel"]:
        data=app.getTextArea(i)
        comdata=data.split('\n')
        for j in range(len(comdata)):
            comdatas=comdata[j].split('\t')
            allcommods[comdatas[0]].update(comdatas[3],comdatas[4],comdatas[5],comdatas[6])
    f2=open('commods.csv','w')
    for i in allcommods.keys():
        f2.write(allcommods[i].output()+'\n')
    craftCommods()
    updateCraftWindow()
    createPphRankings()

def craftCommods():
    with open('recipes.csv','r') as f:
        for line in f:
            if line.split(',')[0] in allcommods.keys():
                allcommods[line.split(',')[0]].setRecipe(line)
                allcommods[line.split(',')[0]].calculateCosts()
                allcommods[line.split(',')[0]].calculateCosts()
                allcommods[line.split(',')[0]].calculateCosts()

def updateStalls(temp):
    for i in ["tailor","blacksmith","shipyard","distillery","weavery","apothecary","furnisher"]:
        allstalls[i].update(str(app.getCheckBox("Owned"+i)),int(app.getEntry("Basic "+i)),int(app.getEntry("Skilled "+i)),int(app.getEntry("Expert "+i)),int(app.getEntry("Use Basic "+i)),int(app.getEntry("Use Skilled "+i)),int(app.getEntry("Use Expert "+i)),int(app.getEntry("Tax Basic")),int(app.getEntry("Tax Skilled")),int(app.getEntry("Tax Expert")))
    f2=open('stalls.csv','w')
    for i in allstalls.keys():
        f2.write(allstalls[i].output()+'\n')
    updateCraftWindow()
    createPphRankings()

def updateCraftWindow():
    craftCommods()
    for i in ["tailor","blacksmith","shipyard","distillery","weavery","apothecary","furnisher"]:
        for j in allcommods.keys():
            if allcommods[j].craftable and allcommods[j].stall==i:
                app.setLabel("Dispcostn"+j,allcommods[j].name)
                app.setLabel("Dispcost"+j,str(int(allcommods[j].craftcost)))
                app.setLabel("Dispcostp"+j,str(int(allcommods[j].sell-allcommods[j].craftcost)))
                app.setLabel("Dispcostq"+j,str(int(allcommods[j].buy-allcommods[j].craftcost)))

def createPphRankings():
    app.clearTextArea("Profit per hour ranking")
    Ranks={}
    for i in allcommods.keys():
        if allcommods[i].craftable==True:
            Ranks[i]=(allcommods[i].sell-allcommods[i].craftcost)/float(allcommods[i].crafttime)
    for i in allcommods.keys():
        if allcommods[i].craftable==True:
            Ranks[i+" Quick"]=(allcommods[i].buy-allcommods[i].craftcost)/float(allcommods[i].crafttime)
    Rankssorted=sorted(Ranks, key=Ranks.__getitem__,reverse=True)
    for i in Rankssorted:
        app.setTextArea("Profit per hour ranking",i+'\t\t\t\t'+str(int(Ranks[i]))+'\n')

class commod:
    def __init__(self,name,buy,sell,use,tax,comtype):
        self.name=name
        self.buy=int(buy)
        self.sell=int(sell)
        if use:
            self.use=int(use)
        else:
            self.use=use
        if tax:
            self.tax=float(tax)
        else:
            self.tax=tax
        self.comtype=comtype.strip('\n')
        self.craftable=False
        self.craftcost=0
        self.crafttime=0
        self.recipe=[]
    def update(self,buy,sell,use,tax):
        self.buy=int(buy)
        self.sell=int(sell)
        if use:
            self.use=int(use)
        else:
            self.use=use
        if tax:
            self.tax=float(tax)
        else:
            self.use=use
    def output(self):
        return self.name+','+str(self.buy)+','+str(self.sell)+','+str(self.use)+','+str(self.tax)+','+self.comtype
    def setRecipe(self,recipe):
        self.craftable=True
        self.recipe=recipe.split(',')
    def calculateCosts(self):
        N=0
        self.craftcost=0
        self.crafttime=0
        for i in range(1,len(self.recipe)):
            if self.recipe[i] in allstalls.keys():
                self.stall=self.recipe[i]
            elif self.recipe[i] in allcommods.keys():
                if allcommods[self.recipe[i]].craftable and allstalls[allcommods[self.recipe[i]].stall].owned=="True":
                    self.craftcost+=(allcommods[self.recipe[i]].tax+allcommods[self.recipe[i]].craftcost)*float(self.recipe[i+1])
                    self.crafttime+=int(allcommods[self.recipe[i]].crafttime*float(self.recipe[i+1]))
                else:
                    self.craftcost+=(allcommods[self.recipe[i]].tax+allcommods[self.recipe[i]].buy)*float(self.recipe[i+1])
            elif self.recipe[i]=="Dubloons":
                self.craftcost+=Dubcost*float(self.recipe[i+1])
            elif self.recipe[i]=="Produces":
                N=int(self.recipe[i+1])
            elif self.recipe[i]=="Basic":
                self.craftcost+=(allstalls[self.stall].bc+allstalls[self.stall].bt)*float(self.recipe[i+1])
                self.crafttime+=int(self.recipe[i+1])
            elif self.recipe[i]=="Skilled":
                self.craftcost+=(allstalls[self.stall].sc+allstalls[self.stall].st)*float(self.recipe[i+1])
                self.crafttime+=int(self.recipe[i+1])
            elif self.recipe[i]=="Expert":
                self.craftcost+=(allstalls[self.stall].ec+allstalls[self.stall].et)*float(self.recipe[i+1])
                self.crafttime+=int(self.recipe[i+1])
        self.craftcost/=float(N)
        self.crafttime/=float(N)

class stalls:
    def __init__(self,name,owned,bc,sc,ec,bu,su,eu,bt,st,et):
        self.name=name
        self.owned=owned
        self.bc=int(bc)
        self.sc=int(sc)
        self.ec=int(ec)
        self.bu=int(bu)
        self.su=int(su)
        self.eu=int(eu)
        self.bt=float(bt)
        self.st=float(st)
        self.et=float(et)
    def update(self,owned,bc,sc,ec,bu,su,eu,bt,st,et):
        self.owned=owned
        self.bc=int(bc)
        self.sc=int(sc)
        self.ec=int(ec)
        self.bu=int(bu)
        self.su=int(su)
        self.eu=int(eu)
        self.bt=float(bt)
        self.st=float(st)
        self.et=float(et)
    def output(self):
        return self.name+','+self.owned+','+str(self.bc)+','+str(self.sc)+','+str(self.ec)+','+str(self.bu)+','+str(self.su)+','+str(self.eu)+','+str(self.bt)+','+str(self.st)+','+str(self.et)
    
titlebgc = Color("#295F7B")
titletc = Color("#D8CA43")
comcolors={"basic":Color("#BDC5BF"),"ship":Color("#C6E2C2"),"herb":Color("#D3CBAB"),"mineral":Color("#DDDED0"),"cloth":Color("#E5E7BF"),"dye":Color("#EDDED9"),"paint":Color("#D2DDDE"),"enamel":Color("#DCD1CF")}
menubgc = Color("#C5C7AD")

allcommods = {}
with open('commods.csv','r') as f:
    for line in f:
        com=line.split(',')
        allcommods[com[0]]=(commod(com[0],com[1],com[2],com[3],com[4],com[5]))
allstalls={}
with open('stalls.csv','r') as f:
    for line in f:
        sta=line.split(',')
        allstalls[sta[0]]=(stalls(sta[0],sta[1],sta[2],sta[3],sta[4],sta[5],sta[6],sta[7],sta[8],sta[9],sta[10]))
Dubcost=int(open('Dubcost.csv','r').read())
craftCommods()

app = gui()
app.setBg(menubgc)
app.addLabel("title", "Stall manager")
app.setLabelBg("title", titlebgc)
app.setLabelFg("title", titletc)


#--------------------All Commidities Window----------------------------------------#
app.startSubWindow("Coms",title="All Commodities")
app.setBg("#BAC2BC")
app.setGeometry("400x800")
app.addTextArea("Commodheads")
app.setTextArea("Commodheads","Commodity\t\t\tBuy\tSell\tUse\tTax")
app.setTextAreaBg("Commodheads",titlebgc)
app.setTextAreaFg("Commodheads",titletc)
for i in comcolors.keys():
    app.addScrolledTextArea(i)
    app.setTextAreaWidth(i,400)
    app.setTextAreaBg(i,comcolors[i])
curtype="0"
for i in allcommods.keys():
    if allcommods[i].comtype.strip('\n')==curtype:
        app.setTextArea(allcommods[i].comtype.strip('\n'),'\n')
    curtype=allcommods[i].comtype.strip('\n')
    if allcommods[i].use:
        app.setTextArea(allcommods[i].comtype.strip('\n'),allcommods[i].name+'\t\t\t'+str(allcommods[i].buy)+'\t'
                +str(allcommods[i].sell)+'\t'+str(allcommods[i].use)+'\t'+str(allcommods[i].tax))
    else:
        app.setTextArea(allcommods[i].comtype.strip('\n'),allcommods[i].name+'\t\t\t'+str(allcommods[i].buy)+'\t'
                +str(allcommods[i].sell)+'\t'+allcommods[i].use+'\t'+str(allcommods[i].tax))
app.setTextAreaWidth("Commodheads",400)
app.setTextAreaHeight("Commodheads",1)
app.setTextAreaHeight("basic",4)
app.setTextAreaHeight("ship",4)
app.setTextAreaHeight("herb",8)
app.setTextAreaHeight("mineral",7)
app.setTextAreaHeight("cloth",10)
app.setTextAreaHeight("dye",4)
app.setTextAreaHeight("paint",7)
app.setTextAreaHeight("enamel",7)
app.addButton("Save Commodities",updateCommods)
app.setButtonBg("Save Commodities","#BAC2BC")
app.stopSubWindow()


#------------------------Manage labor Window----------------------------------------#
app.startSubWindow("labor",title="Manage labor")
app.setSticky("n")
app.setBg(titlebgc)
app.startTabbedFrame("StallLabor")
app.setTabbedFrameActiveBg("StallLabor",titlebgc)
app.setTabbedFrameActiveFg("StallLabor",titletc)
app.setTabbedFrameInactiveBg("StallLabor",menubgc)

for i in ["tailor","blacksmith","shipyard","distillery","weavery","apothecary","furnisher"]:
    app.startTab(i)
    app.addLabel(i+"spacel","",1,0)
    app.addLabel(i+"spacer","",1,2)
    app.startLabelFrame("Labor for "+i,1,1,hideTitle=True)
    app.setBg(menubgc)
    app.setSticky("ew")

    app.addNamedCheckBox("Owned","Owned"+i,0,0)
    if allstalls[i].owned=="True":
        own=True
    else:
        own=False
    app.setCheckBox("Owned"+i,ticked=own)
    app.setCheckBoxBg("Owned"+i,menubgc)
    app.setCheckBoxWidth("Owned"+i,2)
    app.addLabel(i+"Type","",1,0)
    app.addLabel(i+"Cost","Cost",1,1)
    app.addLabel(i+"Use","Use",1,2)
    app.addLabel(i+"Basic "+i+"Label","Basic",2,0)
    app.addLabel(i+"Skilled "+i+"Label","Skilled",3,0)
    app.addLabel(i+"Expert "+i+"Label","Expert",4,0)

    app.addNumericEntry("Basic "+i,2,1)
    app.setEntry("Basic "+i,allstalls[i].bc)
    app.setEntryAlign("Basic "+i,"center")
    app.addNumericEntry("Skilled "+i,3,1)
    app.setEntry("Skilled "+i,allstalls[i].sc)
    app.setEntryAlign("Skilled "+i,"center")
    app.addNumericEntry("Expert "+i,4,1)
    app.setEntry("Expert "+i,allstalls[i].ec)
    app.setEntryAlign("Expert "+i,"center")
    app.addNumericEntry("Use Basic "+i,2,2)
    app.setEntry("Use Basic "+i,allstalls[i].bu)
    app.setEntryAlign("Use Basic "+i,"center")
    app.addNumericEntry("Use Skilled "+i,3,2)
    app.setEntry("Use Skilled "+i,allstalls[i].su)
    app.setEntryAlign("Use Skilled "+i,"center")
    app.addNumericEntry("Use Expert "+i,4,2)
    app.setEntry("Use Expert "+i,allstalls[i].eu)
    app.setEntryAlign("Use Expert "+i,"center")

    app.setEntryWidths(["Basic "+i,"Skilled "+i,"Expert "+i,"Use Basic "+i,"Use Skilled "+i,"Use Expert "+i],10)

    app.stopLabelFrame()
    app.stopTab()

app.stopTabbedFrame()
app.setSticky("s")
app.startLabelFrame("Labor Tax",0,2,hideTitle=True)
app.setSticky("s")
app.setBg(menubgc)
app.addLabel("LTaxspace","",0,3)
app.addLabel("Tax","Tax",1,3)
app.addNumericEntry("Tax Basic",2,3)
app.setEntry("Tax Basic",allstalls[i].bt)
app.setEntryAlign("Tax Basic","center")
app.addNumericEntry("Tax Skilled",3,3)
app.setEntry("Tax Skilled",allstalls[i].st)
app.setEntryAlign("Tax Skilled","center")
app.addNumericEntry("Tax Expert",4,3)
app.setEntry("Tax Expert",allstalls[i].et)
app.setEntryAlign("Tax Expert","center")
app.setEntryWidths(["Tax Basic","Tax Skilled","Tax Expert"],10)
app.stopLabelFrame()
app.addButton("Save Stalls",updateStalls,2,0)
app.stopSubWindow()

#------------------------Craft cost window----------------------------#
app.startSubWindow("Craft costs")
app.setSticky("n")
app.setBg(titlebgc)
app.startTabbedFrame("Craftcosts")
app.setTabbedFrameActiveBg("Craftcosts",titlebgc)
app.setTabbedFrameActiveFg("Craftcosts",titletc)
app.setTabbedFrameInactiveBg("Craftcosts",menubgc)
app.setBg(menubgc)
for i in ["tailor","blacksmith","shipyard","distillery","weavery","apothecary","furnisher"]:
    app.startTab(i)
    app.setBg(menubgc)
    labeln=0
    xpos=0
    ypos=0
    for j in allcommods.keys():
        if allcommods[j].craftable and allcommods[j].stall==i:
            xpos=int(labeln%31)+1
            ypos=int(math.floor(labeln/31))*4
            app.addLabel("Dispcostn"+j,allcommods[j].name,xpos,ypos)
            app.addLabel("Dispcost"+j,str(int(allcommods[j].craftcost)),xpos,ypos+1)
            app.addLabel("Dispcostp"+j,str(int(allcommods[j].sell-allcommods[j].craftcost)),xpos,ypos+2)
            app.addLabel("Dispcostq"+j,str(int(allcommods[j].buy-allcommods[j].craftcost)),xpos,ypos+3)
            for k in ["Dispcostn"+j,"Dispcost"+j,"Dispcostp"+j,"Dispcostq"+j]:
                app.setLabelAlign(k,"left")
                app.setLabelBg(k,comcolors[allcommods[j].comtype])
            labeln+=1
    app.addLabel("craftcom"+i,"Commodity",0,0)
    app.addLabel("craftcomc"+i,"Cost",0,1)
    app.addLabel("craftcomp"+i, "Profit",0,2)
    app.addLabel("craftcomq"+i, "Quick sell",0,3)
    for j in ["craftcom"+i,"craftcomc"+i,"craftcomp"+i,"craftcomq"+i]:
        app.setLabelBg(j,titlebgc)
        app.setLabelFg(j,titletc)
        app.setLabelAlign(j,"left")
    app.addLabel("craftcom2"+i,"Commodity",0,ypos)
    app.addLabel("craftcomc2"+i,"Cost",0,ypos+1)
    app.addLabel("craftcomp2"+i, "Profit",0,ypos+2)
    app.addLabel("craftcomq2"+i, "Quick sell",0,ypos+3)
    for j in ["craftcom2"+i,"craftcomc2"+i,"craftcomp2"+i,"craftcomq2"+i]:
        app.setLabelBg(j,titlebgc)
        app.setLabelFg(j,titletc)
        app.setLabelAlign(j,"left")
    app.stopTab()
app.stopTabbedFrame()
app.stopSubWindow()

#-------------------------------Profit per hour Window------------------------------------#
app.startSubWindow("Profit per hour")
app.setBg(titlebgc)
app.addLabel("pphCommod", "Commodity",0,0)
app.addLabel("pphProf", "Profit",0,1)
app.setLabelWidth("pphCommod", 20)
app.setLabelWidth("pphProf", 20)
for i in ["pphCommod","pphProf"]:
    app.setLabelBg(i,titlebgc)
    app.setLabelFg(i,titletc)
app.addScrolledTextArea("Profit per hour ranking",1,0,2,2)
app.setTextAreaHeight("Profit per hour ranking",50)
app.setTextAreaWidth("Profit per hour ranking",40)
app.setTextAreaBg("Profit per hour ranking",menubgc)
pphranks=createPphRankings()
app.stopSubWindow()

app.addNamedButton("Show All Commodities","Coms",openWindow)
app.addNamedButton("Manage Labor","labor",openWindow)
app.addNamedButton("Show craft costs", "Craft costs",openWindow)
app.addNamedButton("Show All Profit/hr", "Profit per hour",openWindow)
app.addLabelNumericEntry("Dubloon Cost")
app.setEntry("Dubloon Cost",Dubcost)
app.setEntryWidth("Dubloon Cost",5)
app.go()
