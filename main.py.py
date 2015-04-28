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

# Dictionary of commodity data for each station (High Supply = +3, High Demand = -3):
stationDict = {'System 1 - Station A' : ['Gold=3', 'Silver=1', 'Bronze=-2', 'Uranium=0'],
               'System 2 - Station B' : ['Gold=2', 'Silver=2', 'Bronze=-3', 'Uranium=-1'],
               'System 2 - Station C' : ['Gold=1', 'Silver=3', 'Bronze=-2', 'Uranium=-2'],
               'System 3 - Station D' : ['Gold=0', 'Silver=2', 'Bronze=-1', 'Uranium=-3'],
               'System 4 - Station E' : ['Gold=-1', 'Silver=1', 'Bronze=0', 'Uranium=-2'],
               'System 5 - Station F' : ['Gold=-2', 'Silver=0', 'Bronze=1', 'Uranium=-1'],
               'System 5 - Station G' : ['Gold=-3', 'Silver=-1', 'Bronze=2', 'Uranium=0'],
               'System 5 - Station H' : ['Gold=-2', 'Silver=-2', 'Bronze=3', 'Uranium=1'],
               'System 6 - Station I' : ['Gold=-1', 'Silver=-3', 'Bronze=2', 'Uranium=2'],
               'System 7 - Station J' : ['Gold=0', 'Silver=-2', 'Bronze=1', 'Uranium=3'],
               'System 7 - Station K' : ['Gold=1', 'Silver=-1', 'Bronze=2', 'Uranium=2'],
               'System 8 - Station L' : ['Gold=2', 'Silver=0', 'Bronze=3', 'Uranium=1'],
               'System 9 - Station M' : ['Gold=3', 'Silver=1', 'Bronze=2', 'Uranium=0'],
               'System 9 - Station N' : ['Gold=2', 'Silver=2', 'Bronze=1', 'Uranium=-1']}

def version():
        versionNum = 0.1
        notes = """
- Nonfunctional UI built.
- Title and versioning system set."""
        return [versionNum, notes]

def UI():
	# Produce Main GUI window & receive user input (filepath)"
	global mainWindow
	mainWindow = Tk()
	mainWindow.title("Team Trade")

	# Window layout:

	# ROW 0, COLUMN 0:
	# System & station list
	systemListBox = Listbox(mainWindow, height=10, width=20)
	itemcount = 0
	for key in stationDict:
		itemcount = itemcount +1
		systemListBox.insert(itemcount, key)
	systemListBox.grid(row=0, column=0, columnspan=2, padx=5, pady=4, sticky=NS)

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
	commodity = Text(mainWindow, height=20, width=35)
	commodity.grid(row=0, rowspan=3, column=3, padx=5, pady=8)
	commodity.insert(END, "Commodity x\nCommodity y\nCommodity z")

	# R0, C4:
	# scommodity scroll bar
	scrollBarC = Scrollbar(mainWindow, orient=VERTICAL)
	scrollBarC.grid(row=0, column=4, pady=8, rowspan=3, sticky=NS)
	# Link scroll bar to list box
	scrollBarC.configure(command=commodity.yview)
	commodity.configure(yscrollcommand=scrollBarC.set)

	# R1, C0:
	# Add system & station button
	addSystemButton = Button(mainWindow,text="Add", width=7, command=addStation)
	addSystemButton.grid(row=1, column=0, padx=2, sticky=E)

	# R1, C1:
	# Delete system & station button
	delSystemButton = Button(mainWindow,text="Remove", width=7, command= lambda: delStation(PLACEHOLDER-SELECTED-STATION))
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
	# Import/Export buttons
	exitButton =  Button(mainWindow,text="Exit", width=10, command=clean_exit)
	exitButton.grid(row=3, column=3, padx=2, sticky=E) # Apply to grid

	# R3, C4:

	# OPEN WINDOW
	mainWindow.mainloop() # Display window

def clean_exit():
        # Safely close window. Eventually the upload code will also go in here.
	mainWindow.destroy()

def showCommodities(station):
	# Show applicable commodity data for selected station
	pass

def addStation():
        # Add new system/station to list
	pass

def delStation():
        # Delete system/station from list
        pass


if __name__ == '__main__':
	UI()
