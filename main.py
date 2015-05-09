# --------------------------------
# + + T E A M  T R A D E + +
# --------------------------------
# https://github.com/PangolinPaw/teamTrade
# 
from Tkinter import *   # Used for the GUI interface
import tkMessageBox
import ttk
import os       # Used for loading & saving files
import sys      # For safely exiting the program
import pickle   # To save & load data to .txt files
# For saving data online:
import dropbox

# Global window variables so they can be opened & closed from different modules:
mainWindow = 0 
stationInput = 0
APIinput = 0
contextMenu = 0

# Global list of systems & commodities to save having to pass their contents around:
systemListBox = 0 
commodity = 0
trades = 0
systemData = []
currentStationSelection = 0

defaultComm = [u'Explosives=0', u'Hydrogen Fuel=0', u'Mineral Oil=0', u'Pesticides=0', u'Clothing=0', u'Consumer Tech.=0', u'Domestic App.=0', u'Algae=0', u'Animal Meat=0', u'Coffee=0', u'Fish=0', u'Food Cart.=0', u'Fruit & Veg=0', u'Grain=0', u'Synthetic Meat=0', u'Tea=0', u'Polymers=0', u'Semiconductor=0', u'Superconductor=0', u'Beer=0', u'Liquor=0', u'Narcotics=0', u'Tobacco=0', u'Wine=0', u'Atmospheric pr=0', u'Crop Harvester=0', u'Marine Equip.=0', u'Microbial Fur.=0', u'Mineral Ext.=0', u'Power Gen.=0', u'Water Purifier=0', u'Agri-Meds=0', u'Basic Meds=0', u'Combat Stab.=0', u'Perf. Enhance=0', u'Progenator C.=0', u'Aluminium=0', u'Beryllium=0', u'Cobalt=0', u'Copper=0', u'Gallium=0', u'Gold=0', u'Indium=0', u'Lithium=0', u'Palladium=0', u'Platinum=0', u'Silver=0', u'Tantalum=0', u'Titanium=0', u'Uranium=-0']

# Name & location of file full of commodity data.
filename = 'trade_data.txt'
# Dropbox API keys stored in this file
APIfile = 'API.txt'

def version():
        # Version info & eventually help text/instructions.
        source = "http://pangolinpaw.github.io/teamTrade/"

        versionNotes = """VERSION HISTORY 
---------------
v 0.7
- Swap commodity text box for a list box
- Add context-sensitive right click menu to change commodity supply/demand

v0.6.1
- Implement alphabetised System list.

v0.6
- Add basic Suggested Trade Route functionality.
- Alphabetised System list attempted, but a bug prevented implementation.

v0.5.1
- Remove placeholder code from Add Station function & replace with proper input window.

v0.5
- Replace 'file' saving system with 'pickle' system for easier retrieval.
- Add funtional Add Station feature that uses placeholder names.
- Bug fixes.

v0.4
- Add help text and usage instructions.
- Add functional Delete Station feature.

v0.3
- Add cascade menu ribbon and associated functions.
- Mark 'work in progress' areas of the code with capitalised comments.

v0.2:
- Improve dictionary format.
- Minor adjustment to UI window grid to accomodate scroll bars.

v0.1:
- Build basic UI.
- Set title and versioning system."""

        helpText = """ 
Don't Panic.

Introduction
------------
This is tool designed to store and share trade data from the Elite: Dangerous game.

My intention is to produce an application that's the middle ground between offline note-taking tools and the crowdsource Elite Dangerous Data Network apps that are available.

The idea is that you and a few friends will each use this tool and have each copy pointed towards a common online source. This will allow you each to record market supply and demand data and automatically make the information available amongst yourselves without making your valuable trade routes public knowledge.

Usage
------------
Adding Data:
When you visit a new station's commodity market, add it's details using the Add button on the left of this tool's window.

Select the newly added station to view it's commodity supply and demand (which won't contain any useful data yet). Mark each commodity with the supply or demand level from the in-game commodity market using the right mouse button (data is automatically saved after each change).

Sharing Data:
When you close the program or select 'Upload data' from the File menu, the Team Trade application will try to send your locally stored data to an external source. On each subsequent run of the program, data is then imported from this source.

You can set this source via the 'Change Upload URL' option in the Settings menu. You are responsible for finding and maintaining this external file hosting and for sharing the URL with other users of the Team Trade tool which which you want to share collaborative market data.

Team Trade can be used in offline mode by setting the Upload URL to a local direcotry on your PC.

Feedback
------------
Feedback and bug reports are very welcome. Please submit these via the project's GitHub repo:

%s""" % (source)

        return [versionNotes, helpText, source]
        
def showVersion():
        versionDetail = version()[0]
        print "\n%s" % versionDetail

def showInstructions():
        instructions = version()[1]
        print "\n%s" % instructions

def showSource():
    sourceURL = version()[2]
    print "\nThis tool is open source & the code can be viewed at\n%s" % sourceURL

def changeAPI():
        # Create input dialogue for new API keys
        global APIinpit
        APIinput = Tk()
        APIinput.title("New API keys")
        # Text:
        Label(APIinput, text="Please enter new Dropbox API details below\n https://www.dropbox.com/developers/apps).").grid(row=0, column=0, columnspan=2, sticky=W)
        Label(APIinput, text="API Key: ").grid(row=1, column=0)
        Label(APIinput, text="API Secret: ").grid(row=2, column=0)
        # Data entry text boxes:
        keyEntry = Entry(APIinput)
        secretEntry = Entry(APIinput)
        keyEntry.grid(row=1, column=1)
        secretEntry.grid(row=2, column=1)
        # Button:
        submitButton = Button(APIinput, text="OK", width=10, command=lambda: APIsetup(['SAVE', keyEntry.get(), secretEntry.get()]))
        submitButton.grid(row=3, column=1, pady=4, padx=8, sticky=E)
        # Start focus on entry box & set Enter to trigger button's function
        keyEntry.focus_force()
        APIinput.bind('<Return>', (lambda event: APIsetup(['SAVE', keyEntry.get(), secretEntry.get()])))
        
        mainloop()

def confirmAPI():
    # Confirm entry of API keys & close entry dialogue
    global APIinput
    confirmationMessage = "API keys changed"
    selection = tkMessageBox.askquestion("Delete Station", confirmationMessage, icon='warning')
    if selection == 'yes':
        APIinput.destroy()

def APIsetup(settings):
    # Load or save API keys based on settings - ['SAVE'/'LOAD', API KEY, API SECRET]
    if settings[0] == 'SAVE':
        app_key = settings[1]
        app_secret = settings[2]
        saveFile = open(APIfile, 'wb')
        pickle.dump({'KEY' : app_key, 'SECRET' : app_secret}, saveFile)
        saveFile.close()
        confirmAPI()
        
    if settings[0] == 'LOAD':
        loadFile = (APIfile, 'r')
        APIdetails = pickle.load(APIfile)
        app_key = APIdetails['KEY']
        app_secret = APIdetails['SECRET']
        loadFile.close()
        
    return dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

def downloadData():
    # Retrieve trade data from shared source & store in a list for use by the program
    global systemData

    # DOWNLOAD CODE GOES HERE

    if os.path.exists(filename): # Check if the trade data file exists (if not, it is created when the program is closed)
        loadFile = open(filename, 'r')
        systemData= pickle.load(loadFile)
        loadFile.close()
    else:
    # No trade data found, insert test data (High Supply = +3, High Demand = -3):
        systemData =    [['Placeholder System - Placeholder Station', defaultComm]]


def UI():
    # Produce Main GUI window

    downloadData() # Update local list of system data with the shared copy

    global mainWindow
    mainWindow = Tk()
    mainWindow.protocol('WM_DELETE_WINDOW', clean_exit) # Save data when window is closed   
    mainWindow.title("Team Trade")

    mainWindow.config(menu=UImenu()) # Add menu accross the top

    # Right-click menu for changing supply/demand status of a commodity
    global contextMenu
    contextMenu = Menu(mainWindow, tearoff=0)
    contextMenu.add_command(label="High Supply", command= lambda: changeStatus('HS'))
    contextMenu.add_command(label="Medium Supply", command= lambda: changeStatus('MS'))
    contextMenu.add_command(label="Low Supply", command= lambda: changeStatus('LS'))
    contextMenu.add_separator()
    contextMenu.add_command(label="Not Available", command= lambda: changeStatus('--'))
    contextMenu.add_separator()
    contextMenu.add_command(label="Low Demand", command= lambda: changeStatus('LD'))
    contextMenu.add_command(label="Medium Demand", command= lambda: changeStatus('MD'))
    contextMenu.add_command(label="High Demand", command= lambda: changeStatus('HD'))
    mainWindow.bind("<Button-3>", popup)

    # WINDOW LAYOUT

    # ROW 0, COLUMN 0:
    # System & station list
    updateSystems()

    # R0, C1:
    
    # R0, C2:
    # systemListBox scroll bar
    scrollBarS = Scrollbar(mainWindow, orient=VERTICAL)
    scrollBarS.grid(row=0, column=2, pady=4, sticky=NS)
    # Link scroll bar to list box
    scrollBarS.configure(command=systemListBox.yview)
    systemListBox.configure(yscrollcommand=scrollBarS.set)

    # R0, C3
    global commodity
    # Commodity list box
    commodity = Listbox(mainWindow, height=35, width=45)
    commodity.grid(row=0, rowspan=3, column=3, padx=5, pady=8)
    

    # R0, C4:
    # Commodity scroll bar
    scrollBarC = Scrollbar(mainWindow, orient=VERTICAL)
    scrollBarC.grid(row=0, column=4, pady=8, rowspan=3, sticky=NS)
    # Link scroll bar to list box
    scrollBarC.configure(command=commodity.yview)
    commodity.configure(yscrollcommand=scrollBarC.set)

    # R1, C0:
    # Add system & station button
    addSystemButton = Button(mainWindow,text="Add", width=7, command=lambda: addStation())
    addSystemButton.grid(row=1, column=0, padx=2, sticky=E)

    # R1, C1:
    # Delete system & station button
    delSystemButton = Button(mainWindow,text="Remove", width=7, command= lambda: delStation(currentStationSelection))
    delSystemButton.grid(row=1, column=1, padx=2, sticky=W)

    # R1, C2:

    # R2, C0:
    # Suggested trades list
    global trades
    trades = Listbox(mainWindow, height=10, width=35)
    itemcount = 0
    trades.grid(row=2, column=0, columnspan=2, padx=5, pady=2)
    #trades.insert(END, "Suggested Trades")

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

def updateSystems():
    global systemListBox
    global systemData

    # Sort contents of systemList into System alphabetical order
    systemData.sort()

    # Add the systems to the list box & display
    systemListBox = Listbox(mainWindow, height=15, width=35)
    for line in systemData:
        systemListBox.insert(END, line[0])

    systemListBox.grid(row=0, column=0, columnspan=2, padx=5, pady=4, sticky=NS)
    # Update displayed commodities once an item in the listbox is selected:
    systemListBox.bind('<<ListboxSelect>>', showCommodities)

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
    settingsMenu.add_command(label="Change up/download location", command=changeAPI)
    menubar.add_cascade(label="Settings", menu=settingsMenu)

    # Info menu
    infoMenu = Menu(menubar, tearoff=0)
    infoMenu.add_command(label="User instructions", command=showInstructions)
    infoMenu.add_command(label="Version history", command=showVersion)
    infoMenu.add_command(label="View source", command=showSource)
    menubar.add_cascade(label="Info", menu=infoMenu)

    return menubar


def clean_exit():
        # Safely close window. Eventually the upload code will also go in here.
        saveData(systemData)
        mainWindow.destroy()

def changeURL():
    # Change up/download URL (can be set to a local direcotry)
    global URL
    print '[Error]: Change URL function has not yet been implemented.'
    

def uploadData():
    # Upload contents of trade data file to predefined URL
    print '[Error]: Upload data function has not yet been implemented.'
    

def saveChange():
        # Save currently displayed commodities to the list (only uploaded when program exits)
        global commodity
        systemData[currentStationSelection][1] = [] # Fetch from 'commodity' list the selected station's data
        for line in commodity.get(0,END):
                # Loop through textbox contents
                name, info = line.split("\t\t")
                
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
                systemData[currentStationSelection][1].append("%s=%s" % (name, info))
        

def saveData(tradeData):
    # Save data to file & upload it
    saveFile = open(filename, 'w', 0)
    pickle.dump(tradeData, saveFile) # Each station is saved on a new line
    saveFile.close
    uploadData()


def showCommodities(station):
        # Show applicable commodity data for selected station
        global currentStationSelection
        currentStationSelection = systemListBox.curselection()[0]
        
        commodity.delete(0,END)
        commodityData = systemData[currentStationSelection][1]

        itemCount = 0
        for item in commodityData:
                itemCount = itemCount +1
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
                commodity.insert(END, "%s\t\t(%s)" % (name, info))

        showTrades(systemData[currentStationSelection][1])

def popup(event):
    # This lets the right click emnu pop up over the main window
    contextMenu.tk_popup(event.x_root, event.y_root, 0)
        
def changeStatus(newStatus):
    # Change supply/demand of selected commodity & save data
    original = commodity.get(commodity.curselection()[0],None) # Get current selection text
    originalName = original.split('\t\t')[0] # Discard all but the name
    commodity.insert(commodity.curselection()[0], '%s\t\t(%s)' % (originalName, newStatus)) # Insert original name with new status
    commodity.delete(commodity.curselection()[0],last=None) # Delete old entry
    saveChange()
        
def addStation():
    # Add new system/station to list
    global systemData
    global stationInput

    # Create input dialogue:
    stationInput = Tk()
    stationInput.title("New Station")
    # Text:
    Label(stationInput, text="Please enter new Station details below.").grid(row=0, column=0, columnspan=2)
    Label(stationInput, text="System: ").grid(row=1, column=0)
    Label(stationInput, text="Station: ").grid(row=2, column=0)
    # Data entry text boxes:
    sysEntry = Entry(stationInput)
    staEntry = Entry(stationInput)
    sysEntry.grid(row=1, column=1)
    staEntry.grid(row=2, column=1)
    # Button:
    submitButton = Button(stationInput, text="Add", width=10, command=lambda: updateStationList([sysEntry.get(), staEntry.get()]))
    submitButton.grid(row=3, column=1, pady=4, padx=8, sticky=E)
    # Start focus on entry box & set Enter to trigger button's function
    sysEntry.focus_force()
    stationInput.bind('<Return>', (lambda event: updateStationList([sysEntry.get(), staEntry.get()])))
        
    mainloop()     


def updateStationList(details):
    systemData.append(["%s - %s" % (details[0], details[1]), defaultComm])
    updateSystems()
    stationInput.destroy()

def delStation(index):
    # Delete system/station from list
    global systemData
    confirmationMessage = "Are you sure you want to delete all data for this station?\n'%s'" % (systemData[index][0])
    selection = tkMessageBox.askquestion("Delete Station", confirmationMessage, icon='warning')
    if selection == 'yes':
        del systemData[index]
        updateSystems()

def showTrades(localData):
        # Recieves commodity list for local station & displays potential destinations
        global trades
        trades.delete(0,END)
        for localProduct in localData:
                # Loop through selected station's commodities
                localComm = localProduct.split('=')
                localName = localComm[0]
                localVal = int(localComm[1])
                if localVal != 0: # Only do the following loops if the commodity is actually locally available
                        for station in systemData:
                                # Loop through all other stations
                                for distantProduct in station[1]:
                                        # Loop through that station's commodities
                                        distantComm = distantProduct.split('=')
                                        distantName = distantComm[0]
                                        distantVal = int(distantComm[1])

                                        if localName == distantName:
                                                if localVal < 0:
                                                        if distantVal > 1:
                                                                trades.insert(END, '%s From %s' % (localName, station[0]))
                                                if localVal > 0:
                                                        if distantVal < -1:
                                                                trades.insert(END, '%s To %s' % (localName, station[0]))

        

if __name__ == '__main__':
    UI()
