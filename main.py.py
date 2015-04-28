# --------------------------------
# TRADE DATA TOOL
# --------------------------------
# NOTES:
# ListBoxes seem to be a good way to display Systems & Stations.
# Need to find a way to trigger a function when a ListBox item is
# selected so that the stations aupdate or commodity data is
# displayed as applicable.

from Tkinter import *   # Used for the GUI interface
import tkMessageBox
import ttk
import os       # Used for loading & saving files
import sys      # For safely exiting the program

mainWindow = 0 # Global window variable so it can be opened & closed from different modules

# Dictionary showing what stations belong to what systems:
systemDict = {'System 1' : ['Station A', 'Station B'], 'System 2' : ['Station X'], 'System 3' : []}
# Dictionary of commodity data for each station (High Supply = +3, High Demand = -3):
stationDict = {'Station A' : ['Gold=3', 'Silver=1', 'Bronze=-2', 'Uranium=0'],
               'Station B' : ['Gold=-1', 'Silver=0', 'Bronze=0', 'Uranium=2'],
               'Station X' : ['Gold=0', 'Silver=0', 'Bronze=2', 'Uranium=-3']}

def UI():
	# Produce Main GUI window & receive user input (filepath)"
	global mainWindow
	mainWindow = Tk()
	mainWindow.title("Ægishjálmur's App")

	# Window layout:

	# ROW 0, COLUMN 0:
	# System & station list
	systemListBox = Listbox(mainWindow, height=10, width=20)
	itemcount = 0
	for key in systemDict:
		itemcount = itemcount +1
		systemListBox.insert(itemcount, key)
	systemListBox.grid(row=0, column=0, columnspan=2, padx=5, pady=4)

	# R0, C1:

	# R0, C2:
	#Commodity list
	commodity = Text(mainWindow, height=20, width=35)
	commodity.grid(row=0, rowspan=3, column=2, padx=5, pady=8)
	commodity.insert(END, "Commodity x\nCommodity y\nCommodity z")

	# R1,C0:
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

	# R3, C0:

	# R3, C1:

	# R3, C2:
	# Import/Export buttons
	exitButton =  Button(mainWindow,text="Exit", width=10, command=clean_exit)
	exitButton.grid(row=3, column=2, padx=2, sticky=E) # Apply to grid	

	# OPEN WINDOW
	mainWindow.mainloop() # Display window

def clean_exit():
	mainWindow.destroy()

def systemSelected(station):
	# Show applicable stations for selected system
	pass

def addStation():
	pass

def addSystem():
	pass



if __name__ == '__main__':
	UI()
