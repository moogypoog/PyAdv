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
        basechar = character(Current.name,Current.strength,Current.agi,Current.intel,Current.inv)
        print "Done! Character saved."
	return Current

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
#itemtype is the type of item. arm indicates armor or otherwise useless item. wep is a primary equipabble weapon.
class item():
	def __init__(self,name,strength,agi,intel,itemtype="arm",desc="."):
		self.name = name
		self.statlist = [strength,agi,intel]
		self.desc = name+" is a "+findmax(self.statlist,True)+" item."+desc
		self.itemtype = itemtype
		self.equipped = False
	def output(self):
		print "name- ",self.name
		print "Raw Stats (Strength,Agility,Intelligence)- ",self.statlist
		print "Description - ",self.desc
	def unequip(self,char):
		self.equipped = False
                char.strength = char.strength - self.statlist[0]
                char.agi = char.agi - self.statlist[1]
                char.intel =  char.intel
	def equip(self,char):
		for thing in char.inv:
			if thing.itemtype == self.itemtype:
				thing.unequip(char)
		self.equipped = True
		char.strength = char.strength + self.statlist[0]
		char.agi = char.agi + self.statlist[1]
		char.intel = char.intel + self.statlist[2]
#Some basic class definitions here, i may put other weapons in another file r smth idk
Basic_Longsword = item("Basic Longsword",10,1,1,"wep")
Basic_Shortsword = item("Basic Shortsword",1,10,1,"wep")
Basic_Staff= item("Basic Staff",1,1,10,"wep")
#Class - Character, may change in future. This goes for both enemy and friendly characters.
class character():
	def __init__(self,name,strength,agi,intel,inv=[]):
		self.name = name
		self.strength = strength
		self.agi = agi
		self.intel = intel
		if findmax([strength,agi,intel],True) == "Strength":
			self.charclass = "Str"
			if not inv:
				inv.append(Basic_Longsword)
				self.inv = inv
				Basic_Longsword.equip(self)
		elif findmax([strength,agi,intel],True) == "Agility":
			self.charclass = "Agi"
			if not inv:
				inv.append(Basic_Shortsword)
				self.inv = inv
				Basic_Shortsword.equip(self)
		elif findmax([strength,agi,intel],True) == "Intelligence":
			self.charclass = "Int"
			if not inv:
				inv.append(Basic_Staff)
				self.inv = inv
				Basic_Staff.equip(self)
		self.inv = inv
		with open("data","w") as savingfile:
			savingfile.write(self.name+"\n"+str(self.strength)+"\n"+str(self.agi)+"\n"+str(intel))
			for item in self.inv:
                            pass
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
		with open("data","r") as openedfile:
			pass
	elif initialinput == "3":
		print "You may now close this window."
        else:
            print "Invalid option entered. Exitting. No data has been saved."
#Function - One instance of a Battle
def batinstance(estrength,eagi,eint,Current,fstrength=None,fagi=None,fint=None,finv=None,charclass=None):
         import random
	 if Current is None and not fstrength:
		print "Fatal Error! No friendly character instance has been found. Setting all attributes to 0"
	 if fstrength is None or fagi is None or fint is None or finv is None or charclass is None:
		fstrength = Current.strength
		fagi = Current.agi
		fint = Current.intel
		finv = Current.inv
		charclass = Current.charclass
	 fevasion = 2 * fagi
	 eevasion = 2 * eagi
	 while fstrength > 0 and estrength > 0:
		print
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
                                if random.randrange(0,100) < eevasion:
                                    print "Missed!"
                                elif random.randrange(0,100) < fint:
                                    pass
                                    print "Critical strike! hit for an extra"
                                else:
                                    estrength = estrength - fstrength/(random.randrange(10,fstrength*0.9))
		elif userinput == 2:
				fevasion =fevasion + (fagi/4)
		elif userinput == 3:
				counter = 0
				usable = []
				cls()
				print "Please choose an item from the list."
				for thing in finv:
					if thing.itemtype == "arm":
						print "UNUSABLE - "+thing.name
					else:
						print str(counter)+" - "+thing.name
						print
						usable.append(thing)
						counter = counter + 1
						#RETURN TO THIS. UNFINISHED.

#Function - Clear screen by printing a jillion times. Again, this could probably be changed but its the simplest way that (With shell agnosticism) the screen can be cleared (at least, the simplest i've found.
def cls():
	for i in range(100):
		print 
