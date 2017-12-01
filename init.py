
#Function - Find the maximum, with more specific refinement to be made towards the three base stats. THIS NEEDS TO BE CHANGED AT SOME POINT
def findmax(userlist,statcompare=False,outputpos=True):
    maximum = userlist[0]
    position = 0
    for i in range(len(userlist)):
        if userlist[i] > maximum:
            maximum = userlist[i]
            position = i
    if statcompare:
        stats = ["Strength","Agility","Intelligence"]
        return stats[position]
    if outputpos:
        return maximum,position
    return maximum

#Class - Item, this can either be a consumable or equipable.
class item():
    def __init__(self,name,strength,agi,intel,desc="."):
        self.name = name
        self.statlist = [strength,agi,intel]
        self.desc = name+" is a "+findmax(self.statlist,True)+" item."+desc
    def output(self):
        print "name- ",self.name
        print "Raw Stats (Strength,Agility,Intelligence)- ",self.statlist
        print "Description - ",self.desc


#Some basic class definitions here, i may put other weapons in another file r smth idk
Basic_Longsword = item("Basic Longsword",2,1,1)
Basic_Shortsword = item("Basic Shortsword",1,2,1)
Basic_Staff= item("Basic Staff",1,1,2)


#Class - Character, may change in future.
class character():
    def __init__(self,name,strength,agi,intel,inv=[]):
        self.name = name
        self.strength = strength
        self.agi = agi
        self.intel = intel
        if findmax([strength,agi,intel],True) == "Strength":
            inv.append(Basic_Longsword)
            self.charclass = "Str"
        elif findmax([strength,agi,intel],True) == "Agility":
            inv.append(Basic_Shortsword)
            self.charclass = "Agi"
        elif findmax([strength,agi,intel],True) == "Intelligence":
            inv.append(Basic_Staff)
            self.charclass = "Int"
        self.inv = inv
        with open("data","w") as savingfile:
            savingfile.write(self.name+"\n"+str(self.strength)+"\n"+str(self.agi)+"\n"+str(intel))
            for item in self.inv:
                savingfile.write("\n"+str(item.name))
        
def startscreen():
    print "\t welcome to the game"
    print "(1) Start New Game"
    print "(2) Load Save Data"
    print "(3) Exit"
    initialinput = raw_input("Please input the number of the option you want")
    if initialinput == "1":
        print "loading character initialisation module"
        Current = newchar()
	return Current
    elif initialinput == "2":
        print "Loading..."
    elif initialinput == "3":
        print "You may now close this window."


#Function - makes a new character, and assigns it to the current character class. May change this later in the case of multiple character instances at once.
def newchar():
    try:
        import random
        rolling = True
        while rolling:
            strength = random.randrange(0,100)
            intel = random.randrange(0,100-strength)
            agi = random.randrange(0,100-strength-intel)
            if intel < 50:
                agi = random.randrange(0,100)
            if strength < 50 and agi < 50 and intel < 50:
                print "Stats insufficient. Rerolling."
            else:
                rolling = False
    except ImportError:
        print "Error Importing 'Random' Module! Are you sure you have this installed?"
    print "Strength- ",strength," \t Agility- ",agi," \t Intelligence- ",intel
    print "Now writing to external file and updating inventory."
    Current = character(raw_input("Please enter your characters name "),strength,agi,intel)
    return Current

#Function - One instance of a Battle
def batinstance(estrength,eagi,eint,Current,fstrength=None,fagi=None,fint=None,finv=None,charclass=None):
    if fstrength is None or fagi is None or fint is None or finv is None or charclass is None:
        fstrength = Current.strength
        fagi = Current.agi
        fint = Current.intel
        finv = Current.inv
        charclass = Current.charclass
    fevasion = 2 * fagi
    eevasion = 2 * eagi
    while fstrength > 0 and estrength > 0:
        print "1- Attack With your weapon"
        print "2- Increase your evasion (Requires Agility)"
        print "3- Use an item or spell"
	itemloop = True
	while itemloop:
        	try:
			userinput = int(raw_input("Please enter your command- "))
			itemloop = False
		except ValueError:
			print "You have not entered a number! Please re-enter."
	if userinput == 1:
	        #I am going to change this, btw
	        print "attacking!"
	        estrength = estrength - 1
	elif userinput == 2:
            fevasion =fevasion + (fagi/4)
        elif userinput == 3:
            counter = 0
            usable = []
            print "Please choose an item from the list."
            for item in finv:
                if item.itemtype == "arm":
                    print "UNUSABLE - "+item.name
                else:
                    print str(counter)+" - "+item.name
                    usable.append(item)
                    counter = counter + 1
                    #RETURN TO THIS. UNFINISHED.

#Function - Clear screen by printing a jillion times. Again, this could probably be changed but its the simplest way that (With shell agnosticism) the screen can be cleared (at least, the simplest i've found.
def cls():
    for i in range(100):
        print 
