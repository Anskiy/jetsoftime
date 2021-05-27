# python standard libraries
import os
import threading
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox


# custom/local libraries
import randomizertesting as randomizer

#
# Data storage class to hold GUI selection data
#
class DataStore:
  def __init__(self):
    self.flags = {}
    self.difficulty = None
    self.inputFile = None
    self.outputFile = None
    self.techRando = None
    self.shopPrices = None
    self.characters = ['Crono', 'Marle', 'Lucca', 'Frog', 'Robo', 'Ayla', 'Magus']
    self.charLocVars = {}


datastore = DataStore()
progressBar = None
optionsFrame = None

#
# Generate thread target function, calls out to the randomizer to
# generate a seed with the datastore values and stops the progress
# bar when the seed is ready.
#
def randomize():
  try:
    randomizer.handle_gui(datastore)
    progressBar.stop()
    tk.messagebox.showinfo("Randomization Complete", "Randomization complete. Seed: " + datastore.seed.get())
  except WindowsError:
    tk.messagebox.showinfo("Invalid File Name", f"Try placing the ROM in the same folder as the program. \n Also, try writing the extension(.sfc/smc).")
    progressBar.stop()

genThread = None
    
#
# Button handler function for the generate button. It starts the
# generate thread.
#
def generateHandler():
  global genThread
  if genThread == None or not genThread.is_alive():
    genThread = threading.Thread(target=randomize)
    progressBar.start(50)
    genThread.start()
  
#
# Function to display a file chooser for the input ROM.
# Set the chosen file to the datastore.
# Target of the "Browse" button.
#
def browseForRom():
  datastore.inputFile.set(askopenfilename())

def flagClear():
    datastore.difficulty.set("normal")
    datastore.flags['g'].set(0)
    datastore.flags['s'].set(0)
    datastore.flags['d'].set(0)
    datastore.flags['l'].set(0)
    datastore.flags['ro'].set(0)
    datastore.flags['b'].set(0)
    datastore.flags['z'].set(0)
    datastore.flags['p'].set(0)
    datastore.flags['c'].set(0)
    datastore.flags['m'].set(0)
    datastore.flags['q'].set(0)
    datastore.flags['tb'].set(0)
    datastore.flags['cr'].set(0)
    datastore.techRando.set("Normal")
    datastore.shopPrices.set("Normal")
    # Make sure all checkboxes are enabled
    for widget in optionsFrame.winfo_children():
      if type(widget) == tk.Checkbutton:
        widget.configure(state="normal")

def presetRace():
    flagClear()
    datastore.difficulty.set("normal")
    datastore.flags['g'].set(1)
    datastore.flags['s'].set(1)
    datastore.flags['d'].set(1)
    datastore.flags['z'].set(1)
    datastore.flags['p'].set(1)
    datastore.techRando.set("Fully Random")

def presetNew():
    flagClear()
    datastore.difficulty.set("easy")
    datastore.flags['g'].set(1)
    datastore.flags['s'].set(1)
    datastore.flags['d'].set(1)
    datastore.flags['z'].set(1)
    datastore.flags['p'].set(1)
    datastore.flags['m'].set(1)
    datastore.techRando.set("Fully Random")

def presetLost():
    flagClear()
    datastore.difficulty.set("normal")
    datastore.flags['g'].set(1)
    datastore.flags['s'].set(1)
    datastore.flags['d'].set(1)
    datastore.flags['z'].set(1)
    datastore.flags['l'].set(1)
    datastore.techRando.set("Fully Random")

def presetHard():
    flagClear()
    datastore.difficulty.set("hard")
    datastore.flags['g'].set(1)
    datastore.flags['s'].set(1)
    datastore.flags['d'].set(1)
    datastore.flags['b'].set(1)
    datastore.flags['c'].set(1)
    datastore.techRando.set("Balanced Random")

  
#
# Populate and return the frame where the user can pick game flags.
#  
def getGameFlagsFrame(window):
  frame = tk.Frame(window, borderwidth = 1)
  row = 0
  pendantCheckbox = None
  bossScalingCheckbox = None
  lostWorldsCheckbox = None

  # Janky addition for presets because I suck at python - Future
  #Presets Header
  tk.Label(frame, text="Preset Selection:").grid(row=row, column=0, sticky=tk.E)
  
  #Preset Buttons
  tk.Button(frame, text="Race", command=presetRace).grid(row=row, column=2)
  tk.Button(frame, text="New Player", command=presetNew).grid(row=row, column=3)
  tk.Button(frame, text="Lost Worlds", command=presetLost).grid(row=row, column=4)
  tk.Button(frame, text="Hard", command=presetHard).grid(row=row, column=5)
  row = row + 1
  
  # Dropdown for the difficulty flags
  difficultyValues = ["easy", "normal", "hard"]
  label = tk.Label(frame, text="Difficulty:")
  var = tk.StringVar()
  var.set('normal')
  datastore.difficulty = var
  dropdown = tk.OptionMenu(frame, var, *difficultyValues)
  dropdown.config(width = 5)
  label.grid(row = row, column = 0, sticky=tk.W)
  dropdown.grid(row = row, column = 1, sticky=tk.W)
  row = row + 1
  
  # Checkboxes for the randomizer flags
  # Disable glitches
  var = tk.IntVar()
  datastore.flags['g'] = var
  tk.Checkbutton(frame, text="Disable Glitches(g)", variable = var).grid(row=row, sticky=tk.W, columnspan=3)
  row = row + 1
  
  # Faster overworld movement
  var = tk.IntVar()
  datastore.flags['s'] = var
  tk.Checkbutton(frame, text="Fast overworld movement(s)", variable = var).grid(row=row, sticky=tk.W, columnspan=3)
  row = row + 1
  
  # faster dpad inputs in menus
  var = tk.IntVar()
  datastore.flags['d'] = var
  tk.Checkbutton(frame, text="Fast dpad in menus(d)", variable = var).grid(row=row, sticky=tk.W, columnspan=3)
  row = row + 1
  
  # Lost Worlds
  
  #
  # Callback function to disable the early pendant charge option when 
  # the user selects the Lost Worlds mode. Early Pendant is not avaiable
  # in Lost Worlds mode.
  #
  def togglePendantState():
    if datastore.flags['l'].get() == 1:
      datastore.flags['p'].set(0)
      pendantCheckbox.config(state=tk.DISABLED)
    else:
      pendantCheckbox.config(state=tk.NORMAL)
      
  var = tk.IntVar()
  datastore.flags['l'] = var
  lostWorldsCheckbox = tk.Checkbutton(frame, text="Lost Worlds(l)", variable = var, command=togglePendantState)
  lostWorldsCheckbox.grid(row=row, sticky=tk.W, columnspan=3)
  row = row + 1
  
  # Boss randomization
  var = tk.IntVar()
  datastore.flags['ro'] = var
  bossRandoCheckbox = tk.Checkbutton(frame, text="Randomize bosses(ro)", variable = var)
  bossRandoCheckbox.grid(row=row, sticky=tk.W, columnspan=3)
  row = row + 1
  
  # Boss scaling
  var = tk.IntVar()
  datastore.flags['b'] = var
  bossScalingCheckbox = tk.Checkbutton(frame, text="Boss scaling(b)", variable = var)
  bossScalingCheckbox.grid(row=row, sticky=tk.W, columnspan=3)
  row = row + 1
  
  # Zeal 2 as last boss
  var = tk.IntVar()
  datastore.flags['z'] = var
  tk.Checkbutton(frame, text="Zeal 2 as last boss(z)", variable = var).grid(row=row, sticky=tk.W, columnspan=3)
  row = row + 1
  
  # Early pendant charge
  var = tk.IntVar()
  datastore.flags['p'] = var
  pendantCheckbox= tk.Checkbutton(frame, text="Early Pendant Charge(p)", variable = var)
  pendantCheckbox.grid(row=row, sticky=tk.W, columnspan=3)
  row = row + 1
  
  # Locked characters
  var = tk.IntVar()
  datastore.flags['c'] = var
  tk.Checkbutton(frame, text="Locked characters(c)", variable = var).grid(row=row, sticky=tk.W, columnspan=3)
  row = row + 1

  # Unlocked Magic
  var = tk.IntVar()
  datastore.flags['m'] = var
  tk.Checkbutton(frame, text="Unlocked Magic(m)", variable = var).grid(row=row, sticky=tk.W, columnspan=3)
  row = row + 1

  # Quiet Mode (No Music)
  var = tk.IntVar()
  datastore.flags['q'] = var
  tk.Checkbutton(frame, text="Quiet Mode - No Music (q)", variable = var).grid(row=row, sticky=tk.W, columnspan=3)
  row = row + 1
  
  # Tab Treasures
  var = tk.IntVar()
  datastore.flags['tb'] = var
  tk.Checkbutton(frame, text="Make all treasures tabs(tb)", variable = var).grid(row=row, sticky=tk.W, columnspan=3)
  row = row + 1

  # Chronosanity
  def disableChronosanityIncompatibleFlags():
    if datastore.flags['cr'].get() == 1:
      # Boss scaling doesn't work with full rando.
      datastore.flags['b'].set(0)
      bossScalingCheckbox.config(state=tk.DISABLED)
    else:
      bossScalingCheckbox.config(state=tk.NORMAL)
      
  var = tk.IntVar()
  datastore.flags['cr'] = var
  tk.Checkbutton(frame, text="Chronosanity(cr)", variable = var, command=disableChronosanityIncompatibleFlags).grid(row=row, sticky=tk.W, columnspan=3)
  row = row + 1
  
  # Dropdown for shop price settings
  shopPriceValues = ["Normal", "Free", "Mostly Random", "Fully Random"]
  label = tk.Label(frame, text="Shop Prices:")
  var = tk.StringVar()
  var.set('Normal')
  datastore.shopPrices = var
  dropdown = tk.OptionMenu(frame, var, *shopPriceValues)
  dropdown.config(width = 20)
  label.grid(row = row, column = 0, sticky = tk.W)
  dropdown.grid(row = row, column = 1, sticky = tk.W)
  row = row + 1
  
  # Dropdown for the tech rando
  techRandoValues = ["Normal", "Balanced Random", "Fully Random"]
  label = tk.Label(frame, text="Tech Randomization:")
  var = tk.StringVar()
  var.set('Normal')
  datastore.techRando = var
  dropdown = tk.OptionMenu(frame, var, *techRandoValues)
  dropdown.config(width = 20)
  label.grid(row = row, column = 0, sticky=tk.W)
  dropdown.grid(row = row, column = 1, sticky=tk.W)
  row = row + 1

   # Let the user choose a seed (optional parameter)
  tk.Label(frame, text="Seed(optional):").grid(row=row, column=0, sticky=tk.E)
  datastore.seed = tk.StringVar()
  tk.Entry(frame, textvariable=datastore.seed).grid(row=row, column=1)
  row = row + 1
  
  # Let the user select the base ROM to copy and patch
  tk.Label(frame, text="Input ROM:").grid(row=row, column=0, sticky=tk.E)
  datastore.inputFile = tk.StringVar()
  tk.Entry(frame, textvariable=datastore.inputFile).grid(row=row, column=1)
  tk.Button(frame, text="Browse", command=browseForRom).grid(row=row, column=2)
  row = row + 1

  # Add a progress bar to the GUI for ROM generation
  global progressBar
  progressBar = ttk.Progressbar(frame, orient='horizontal', mode='indeterminate')
  progressBar.grid(row = row, column = 0, columnspan = 3, sticky=tk.N+tk.S+tk.E+tk.W)
  row = row + 1
  
  return frame
  

#
# Main entry function for the GUI. Set up and launch the display.
#  
def guiMain():
  global optionsFrame
  mainWindow = tk.Tk()
  mainWindow.wm_title("Jets of Time")

  tabs = ttk.Notebook(mainWindow)
  optionsFrame = getGameFlagsFrame(tabs)
  tabs.add(optionsFrame,text="Flags")
  tabs.add(getCharacterFrame(tabs),text="Characters")
  tabs.pack(expand=1,fill="both")
  #optionsFrame = getGameFlagsFrame(mainWindow)
  #optionsFrame.pack(expand=1, fill="both")
  
  tk.Button(mainWindow, text="Generate", command=generateHandler).pack()
  
  mainWindow.mainloop()
  
def getCharacterFrame(notebook):
  frame = ttk.Frame(notebook)
  frame.grid(column=0, row=0, sticky=(tk.N,tk.W,tk.E,tk.S))
  #frame.columnconfigure(0, weight=1)
  
  # Add a row for each character with a location dropdown
  charLocChoices = ['', 'Start1', 'Start2', 'Cathedral', 'Guardia Castle', 'Proto Dome', 'Frog Burrow', 'Dactyl Nest']
  rowval = 0
  for char in datastore.characters:
    label = tk.Label(frame, text=(char + ":"))
    var = tk.StringVar()
    var.set('')
    datastore.charLocVars[char] = var
    dropdown = tk.OptionMenu(frame, var, *charLocChoices)
    dropdown.config(width = 12)
    label.grid(row = rowval, column = 0, sticky=tk.W)
    dropdown.grid(row = rowval, column = 1, sticky=tk.W)
    rowval = rowval + 1
  
  return frame