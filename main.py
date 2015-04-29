# --------------------------------
# TRADE DATA TOOL
# --------------------------------
# NOTES:
# ListBoxes seem to be a good way to display Systems & Stations.
# Need to find a way to trigger a function when a ListBox item is
# selected so that the commodity data is displayed.

from Tkinter import *   # Used for the GUI interface
import tkMessageBox
import ttk
import os       # Used for loading & saving files
import sys      # For safely exiting the program

mainWindow = 0 # Global window variable so it can be opened & closed from different modules

# Global list of systems & commodities to save having to pass their contents around:
systemListBox = 0 
commodity = 0
systemData = 0

# Name & location of file full of commodity data.
filename = 'trade_data.txt'
# UP/DOWNLOAD URL GOES HERE
URL = ''

def version():
        # Version info & eventually help text/instructions.
        versionNotes = """VERSION HISTORY 
---------------
v0.3
- Added cascade menu ribbon and associated functions.
- Marked 'work in progress' areas of the code with capitalised comments.

v0.2:
- Improved dictionary format.
- Minor adjustment to UI window grid to accomodate scroll bars.

v0.1:
- Basic UI built.
- Title and versioning system set."""

		helpText = """ 
Don't Panic."""
		source = "https://github.com/PangolinPaw/teamTrade"

        return [versionNotes, helpText, source]
        
def showVersion():
		versionDetail = version()[0]
		print versionDetail

def showInstructions():
		instructions - version()[1]
		print instructions

def showSource():
	sourceURL = version()[2]
	print "This tool is open source & the code can be viewed on\n%s" % sourceURL


def downloadData():
		# Retrieve trade data from shared source & store in a list for use by the program
		global systemData

		# DOWNLOAD CODE GOES HERE

		if os.path.exists(): # Check if the trade data file exists (if not, it is created when the program is closed)
				loadFile = open(filename, 'r')
				fileLines = loadFile.Readlines()
				for line in fileLines:
						systemData.append(line) # Save file contents to list
				loadFile.close()
		else:
		# No trade data found, insert test data (High Supply = +3, High Demand = -3):
				systemData = [['System 1 - Station A', ['Gold=3', 'Silver=1', 'Bronze=-2', 'Uranium=0']],
            				  ['System 2 - Station B', ['Gold=2', 'Silver=2', 'Bronze=-3', 'Uranium=-1']],
            				  ['System 2 - Station C', ['Gold=1', 'Silver=3', 'Bronze=-2', 'Uranium=-2']],
            				  ['System 3 - Station D', ['Gold=0', 'Silver=2', 'Bronze=-1', 'Uranium=-3']],
            				  ['System 4 - Station E', ['Gold=-1', 'Silver=1', 'Bronze=0', 'Uranium=-2']],
            				  ['System 5 - Station F', ['Gold=-2', 'Silver=0', 'Bronze=1', 'Uranium=-1']],
            				  ['System 5 - Station G', ['Gold=-3', 'Silver=-1', 'Bronze=2', 'Uranium=0']],
            				  ['System 5 - Station H', ['Gold=-2', 'Silver=-2', 'Bronze=3', 'Uranium=1']]
            				  ]


def UI():
	# Produce Main GUI window

	downloadData() # Update local list of system data with the shared copy

	global mainWindow
	mainWindow = Tk()
	mainWindow.protocol('WM_DELETE_WINDOW', clean_exit) # Save data when window is closed	
	mainWindow.title("Team Trade")

	mainWindow.config(menu=UImenu()) # Add menu accross the top

	# Window layout:

	# ROW 0, COLUMN 0:
	# System & station list
	global systemListBox
	systemListBox = Listbox(mainWindow, height=10, width=20)
	itemcount = 0
	for line in systemData:
		itemcount = itemcount +1
		systemListBox.insert(itemcount, line[0])
	systemListBox.grid(row=0, column=0, columnspan=2, padx=5, pady=4, sticky=NS)

	# Update displayed commodities once an item in the listbox is selected:
	systemListBox.bind('<<ListboxSelect>>', showCommodities)

	# R0, C1:
	
	# R0, C2:
    # systemListBox scroll bar
	scrollBarS = Scrollbar(mainWindow, orient=VERTICAL)
	scrollBarS.grid(row=0, column=2, pady=4, sticky=NS)
	# Link scroll bar to list box
	scrollBarS.configure(command=systemListBox.yview)
	systemListBox.configure(yscrollcommand=scrollBarS.set)

	# R0, C3
	#Commodity list
	global commodity
	commodity = Text(mainWindow, height=20, width=35)
	commodity.grid(row=0, rowspan=3, column=3, padx=5, pady=8)
	commodity.insert(END,"Commodity Data")

	# R0, C4:
	# Commodity scroll bar
	scrollBarC = Scrollbar(mainWindow, orient=VERTICAL)
	scrollBarC.grid(row=0, column=4, pady=8, rowspan=3, sticky=NS)
	# Link scroll bar to list box
	scrollBarC.configure(command=commodity.yview)
	commodity.configure(yscrollcommand=scrollBarC.set)

	# R1, C0:
	# Add system & station button
	addSystemButton = Button(mainWindow,text="Add", width=7, command=lambda: addStation(systemData[systemListBox.curselection()[0]][0]))
	addSystemButton.grid(row=1, column=0, padx=2, sticky=E)

	# R1, C1:
	# Delete system & station button
	delSystemButton = Button(mainWindow,text="Remove", width=7, command= lambda: delStation(systemData[systemListBox.curselection()[0]][0]))
	delSystemButton.grid(row=1, column=1, padx=2, sticky=W)

	# R1, C2:

	# R2, C0:
	# Suggested trades list
	tradeListBox = Listbox(mainWindow, height=6, width=20)
	itemcount = 0
	tradeListBox.grid(row=2, column=0, columnspan=2, padx=5, pady=2)

	# R2, C1:

	# R2, C2:

	# R2, C3:

	# R2, C4:

	# R3, C0:

	# R3, C1:

	# R3, C2:

	# R3, C3:
	# Save button
	saveButton = Button(mainWindow,text="Save", width=10, command=saveChange)
	saveButton.grid(row=3, column=3, padx=2, pady=2, sticky=E)


	# R3, C4:

	# OPEN WINDOW
	mainWindow.mainloop() # Display window

def UImenu():
	# Create & control menu items accross the top of the window
	menubar = Menu(mainWindow)

	# File menu
	fileMenu = Menu(menubar, tearoff=0)
	fileMenu.add_command(label="Upload data", command=uploadData)
	fileMenu.add_command(label="Download data", command=downloadData)
	fileMenu.add_separator()
	fileMenu.add_command(label="Exit", command=clean_exit)
	menubar.add_cascade(label="File", menu=fileMenu)

	# Settings menu
	settingsMenu = Menu(menubar, tearoff=0)
	settingsMenu.add_command(label="Change upload URL", command=changeURL)
	menubar.add_cascade(label="Settings", menu=settingsMenu)

	# Info menu
	infoenu = Menu(menubar, tearoff=0)
	infoMenu.add_command(label="User instructions", command=showInstructions)
	infoMenu.add_command(label="Version history", command=showVersion)
	infoMenu.add_command(label="View source", command=showSource)
	menubar.add_cascade(label="Info", menu=infoMenu)

	return menubar


def clean_exit():
        # Safely close window. Eventually the upload code will also go in here.
        saveData(systemData)
        print 'Data saved'
        uploadData()
        mainWindow.destroy()

def changeURL():
	# Change up/download URL (can be set to a local direcotry)
	global URL
	pass


def uploadData():
	# Upload contents of trade data file to predefined URL
	pass

def saveChange():
        # Save currently displayed commodities to the list (only uploaded when program exits)
        global commodity
        systemData[systemListBox.curselection()[0]][1] = [] # Fetch from 'commodity' list the selected station's data
        for line in commodity.get(1.0,'end-1c').splitlines():
                # Loop through textbox contents
                name, info = line.split("		")
                # Convert user-fiendly supply/demand names back to integers
                if info == "(HS)":
                        info = 3
                if info == "(MS)":
                        info = 2
                if info == "(LS)":
                        info = 1
                if info == "(--)":
                        info = 0
                if info == "(LD)":
                        info = -1
                if info == "(MD)":
                        info = -2
                if info == "(HD)":
                        info = -3
                print "%s=%s" % (name, info)
                systemData[systemListBox.curselection()[0]][1].append("%s=%s" % (name, info))
        

def saveData(tradeData):
        # Save data to file & upload it
        saveFile = open(filename, 'w', 0)
        for line in tradeData:
                saveFile.write("%s\n" % line) # Each station is saved on a new line
        saveFile.close
        uploadData()


def showCommodities(station):
        # Show applicable commodity data for selected station
        commodity.delete(1.0,END)
        commodityData = systemData[systemListBox.curselection()[0]][1]
        for item in commodityData:
                name, info = item.split('=')
                # Convert integer values into user-freindly supply/demand names
                info = int(info)
                if info == 3:
                        info = "HS"
                if info == 2:
                        info = "MS"
                if info == 1:
                        info = "LS"
                if info == 0:
                        info = "--"
                if info == -1:
                        info = "LD"
                if info == -2:
                        info = "MD"
                if info == -3:
                        info = "HD"
                # Add commodity to the end of the list
                commodity.insert(END, "%s		(%s)\n" % (name, info))

def addStation(station):
        # Add new system/station to list
	print "Add '%s'" % station # PLACEHOLDER

def delStation(station):
        # Delete system/station from list
        print "Delete '%s'" % station # PLACEHOLDER


if __name__ == '__main__':
	UI()
