# python standard libraries
import os
import pathlib
import pickle
import threading
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter import messagebox


# custom/local libraries
import randomizer

#
# Data storage class to hold GUI selection data
#
class DataStore:
  def __init__(self):
    self.flags = {}
    self.difficulty = None
    self.inputFile = None
    self.outputFolder = None
    self.techRando = None
    self.shopPrices = None

    self.char_choices = None
    self.dup_techs = None
    
  #
  # Get a path to the settings file.
  # On Windows, this is in %APPDATA%\JetsOfTime
  # On Linux/Mac this is in $HOME/.JetsOfTime
  #
  def getSettingsFile(self):
    filePath = ""
    if os.name == "nt":
      # If on Windows, put the settings file in roaming appdata
      dir = os.getenv('APPDATA')
      filePath = pathlib.Path(dir).joinpath('JetsOfTime')
    else:
      # If on Mac/Linux, make it a hidden file in the home directory
      filePath = pathlib.Path(os.path.expanduser('~')).joinpath('.JetsOfTime')
      
    return filePath.joinpath("settings.dat")
  # end getSettingsFile method
  
  #
  # Serialize and save this DataStore object.
  #
  def save(self):
    try:
      filePath = self.getSettingsFile()
      if not filePath.parent.exists():
        filePath.parent.mkdir()
        
      # We can't pickle the datastore since tkinter objects can't be pickled
      # Set up a dictionary with the relevant data and pickle that instead
      data = {}
      # flags
      flags = {}
      for flag in self.flags:
        flags[flag] = self.flags[flag].get()
      data["flags"] = flags
      # dropdowns
      data["difficulty"] = self.difficulty.get()
      data["shopPrices"] = self.shopPrices.get()
      data["techRando"] = self.techRando.get()
      # textboxes
      data["inputFile"] = self.inputFile.get()
      data["outputFolder"] = self.outputFolder.get()

      if self.char_choices is None:  # DC settings has never been opened before
          choices = [[1 for i in range(7)] for j in range(7)]
          dup_techs = 0
      else:
          choices = [[1 for i in range(7)] for j in range(7)]
          for i in range(7):
              for j in range(7):
                  choices[i][j] = self.char_choices[i][j].get()
          dup_techs = self.dup_techs.get()
          
      data["charChoices"] = choices
      data['dupDuals'] = dup_techs
      
      file = open(str(filePath), "wb")
      pickle.dump(data, file)
    except:
      # Swallow any exceptions here. We don't want failures here
      # to break the randomizer.
      print("Unable to save settings.")
  # end save method
  
  #
  # Load a serialized DataStore object.
  #
  def load(self):
    try:
      filePath = self.getSettingsFile()
      if filePath.exists():
        # Load the saved settings
        file = open(str(filePath), "rb")
        settings = pickle.load(file)
        
        self.difficulty.set(settings["difficulty"])
        self.inputFile.set(settings["inputFile"])
        self.outputFolder.set(settings["outputFolder"])
        self.techRando.set(settings["techRando"])
        self.shopPrices.set(settings["shopPrices"])
        for flag in settings["flags"]:
          self.flags[flag].set(settings["flags"][flag])

        try:
            cc = settings["charChoices"]
        except KeyError:
            cc = [[1 for i in range(7)] for j in range(7)]

        try:
            dt = settings['dupDuals']
        except KeyError:
            dt = 0

        self.dup_techs = tk.IntVar(value=dt)

        self.char_choices = []
        for i in range(7):
            self.char_choices.append([])
            for j in range(7):
                self.char_choices[i].append(tk.IntVar(value=cc[i][j]))

        # self.dup_techs.set(settings['dupDuals'].get())
                
    except:
      # Swallow any exceptions here. We don't want failures here
      # to break the randomizer.
      print("Failed to load prior settings.  Starting clean.")
  # end load method

datastore = DataStore()
progressBar = None
optionsFrame = None

#
# tkinter does not have a native tooltip implementation.
# This tooltip implementation is stolen from Stack Overflow:
# https://stackoverflow.com/a/36221216
#
class CreateToolTip(object):
  """
  create a tooltip for a given widget
  """
  def __init__(self, widget, text='widget info'):
    self.waittime = 800     #miliseconds
    self.wraplength = 300   #pixels
    self.widget = widget
    self.text = text
    self.widget.bind("<Enter>", self.enter)
    self.widget.bind("<Leave>", self.leave)
    self.widget.bind("<ButtonPress>", self.leave)
    self.id = None
    self.tw = None

  def enter(self, event=None):
    self.schedule()

  def leave(self, event=None):
    self.unschedule()
    self.hidetip()

  def schedule(self):
    self.unschedule()
    self.id = self.widget.after(self.waittime, self.showtip)

  def unschedule(self):
    id = self.id
    self.id = None
    if id:
      self.widget.after_cancel(id)

  def showtip(self, event=None):
    x = y = 0
    x, y, cx, cy = self.widget.bbox("insert")
    x += self.widget.winfo_rootx() + 25
    y += self.widget.winfo_rooty() + 20
    # creates a toplevel window
    self.tw = tk.Toplevel(self.widget)
    # Leaves only the label and removes the app window
    self.tw.wm_overrideredirect(True)
    self.tw.wm_geometry("+%d+%d" % (x, y))
    label = tk.Label(self.tw, text=self.text, justify='left',
                 background="#ffffff", relief='solid', borderwidth=1,
                 wraplength = self.wraplength)
    label.pack(ipadx=1)

  def hidetip(self):
    tw = self.tw
    self.tw= None
    if tw:
      tw.destroy()
# end class CreateToolTip

#
# Generate thread target function, calls out to the randomizer to
# generate a seed with the datastore values and stops the progress
# bar when the seed is ready.
#
def randomize():
  try:
    randomizer.handle_gui(datastore)
    datastore.save()
    progressBar.stop()
    tk.messagebox.showinfo("Randomization Complete", "Randomization complete. Seed: " + datastore.seed.get())
  except WindowsError as we:
    print(str(we))
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
  
#
# Function to display a file chooser for the output folder.
# Set the chosen folder to the datastore.
# Target of the "Browse" button.
#
def browseForOutputFolder():
  datastore.outputFolder.set(askdirectory())

def flagClear():
    datastore.difficulty.set("normal")
    for flagstr in datastore.flags:
      datastore.flags[flagstr].set(0)
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
#    datastore.flags['s'].set(1)
#    datastore.flags['d'].set(1)
    datastore.flags['z'].set(1)
    datastore.flags['p'].set(1)
    datastore.techRando.set("Fully Random")

def presetNew():
    flagClear()
    datastore.difficulty.set("easy")
    datastore.flags['g'].set(1)
#    datastore.flags['s'].set(1)
#    datastore.flags['d'].set(1)
    datastore.flags['z'].set(1)
    datastore.flags['p'].set(1)
    datastore.flags['m'].set(1)
    datastore.techRando.set("Fully Random")

def presetLost():
    flagClear()
    datastore.difficulty.set("normal")
    datastore.flags['g'].set(1)
#    datastore.flags['s'].set(1)
#    datastore.flags['d'].set(1)
    datastore.flags['z'].set(1)
    datastore.flags['l'].set(1)
    datastore.techRando.set("Fully Random")

def presetHard():
    flagClear()
    datastore.difficulty.set("hard")
    datastore.flags['g'].set(1)
#    datastore.flags['s'].set(1)
#    datastore.flags['d'].set(1)
    datastore.flags['b'].set(1)
    datastore.flags['c'].set(1)
    datastore.techRando.set("Balanced Random")

# Frame for presets, hopefully.

def getPresetsFrame(window):
  frame = tk.Frame(window, borderwidth=1, highlightbackground="black", highlightthickness=1)
  row = 0
  #Presets Header
  tk.Label(frame, text="Preset Selection:").grid(row=row, column=0, sticky=tk.E)
  
  #Preset Buttons
  tk.Button(frame, text="Race", command=presetRace).grid(row=row, column=1)
  tk.Button(frame, text="New Player", command=presetNew).grid(row=row, column=2)
  tk.Button(frame, text="Lost Worlds", command=presetLost).grid(row=row, column=3)
  tk.Button(frame, text="Hard", command=presetHard).grid(row=row, column=4)
  return frame
  
#
# Get a frame for game options not related to randomization.
#
def getGameOptionsFrame(window):
  frame = tk.Frame(window, borderwidth = 1, highlightbackground="black", highlightthickness=1)
  row = 0
  
  label = tk.Label(frame, text="Game Options:")
  label.grid(row = row, column = 0, sticky=tk.W)
  row = row + 1
  
  # Disable glitches
  var = tk.IntVar()
  datastore.flags['g'] = var
  checkButton = tk.Checkbutton(frame, text="Disable Glitches (g)", variable = var)
  checkButton.grid(row=row, column=0, sticky=tk.W, columnspan=2)
  CreateToolTip(checkButton, "Disables common glitches such as the unequip and save anywhere glitches.")
  
  # Faster overworld movement
#  var = tk.IntVar()
#  datastore.flags['s'] = var
#  checkButton = tk.Checkbutton(frame, text="Fast overworld movement (s)", variable = var)
#  checkButton.grid(row=row, column=2, sticky=tk.W, columnspan=2)
#  CreateToolTip(checkButton, "Move faster on the overworld while walking and riding in the Epoch.")
#  row = row + 1
  
  # faster dpad inputs in menus
#  var = tk.IntVar()
#  datastore.flags['d'] = var
#  checkButton = tk.Checkbutton(frame, text="Fast dpad in menus (d)", variable = var)
#  checkButton.grid(row=row, column=0, sticky=tk.W, columnspan=2)
#  CreateToolTip(checkButton, "Dpad inputs in menus are faster and more responsive.")
  
  # Quiet Mode (No Music)
  var = tk.IntVar()
  datastore.flags['q'] = var
  checkButton = tk.Checkbutton(frame, text="Quiet Mode - No Music (q)", variable = var)
  checkButton.grid(row=row, column=2, sticky=tk.W, columnspan=2)
  CreateToolTip(checkButton, "Music is disabled.  Sound effects will still play.")
  row = row + 1
  
  return frame
  

#
# Get a frame for the flags that affect randomization
#
def getRandomizerOptionsFrame(window):
  frame = tk.Frame(window, borderwidth = 1, highlightbackground="black", highlightthickness=1)
  row = 0
  pendantCheckbox = None
  bossScalingCheckbox = None
  lostWorldsCheckbox = None

  label = tk.Label(frame, text="Randomizer Options:")
  label.grid(row = row, column = 0, sticky=tk.W)
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
  dropdown.grid(row = row, column = 1, sticky=tk.W, columnspan=2)
  CreateToolTip(dropdown, \
      "Game difficulty:\n"
      "Easy - Quality of treasure from chests and monster drops greatly improved.\n"
      "Normal - Standard treasure drops, standard enemy difficulty.\n"
      "Hard - Reduced treasure quality, some enemies have been made more difficult, "
      "some exp and tech point rewards have been reduced.")
  row = row + 1
  
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
  lostWorldsCheckbox = tk.Checkbutton(frame, text="Lost Worlds (l)", variable = var, command=togglePendantState)
  lostWorldsCheckbox.grid(row=row, column=0, sticky=tk.W, columnspan=2)
  CreateToolTip(lostWorldsCheckbox, "An alternate game mode where you start with access to Prehistory, the Dark Ages, and the Future. Find the clone and c.trigger to climb Death Peak and beat the Black Omen, or find the Dreamstone and Ruby Knife to make your way to Lavos through the Ocean Palace. 600AD and 1000AD are unavailable until the very end of the game.")
  
  # Boss randomization
  var = tk.IntVar()
  datastore.flags['ro'] = var
  bossRandoCheckbox = tk.Checkbutton(frame, text="Randomize bosses (ro)", variable = var)
  bossRandoCheckbox.grid(row=row, column=2, sticky=tk.W, columnspan=2)
  CreateToolTip(bossRandoCheckbox, "Various dungeon bosses are shuffled and scaled.  Does not affect end game bosses.")
  row = row + 1

  # Boss scaling
  var = tk.IntVar()
  datastore.flags['b'] = var
  bossScalingCheckbox = tk.Checkbutton(frame, text="Boss scaling (b)", variable = var)
  bossScalingCheckbox.grid(row=row, column=0, sticky=tk.W, columnspan=2)
  CreateToolTip(bossScalingCheckbox, "Bosses are scaled in difficulty based on how many key items they block.  Early bosses are unaffected.")
  
  # Zeal 2 as last boss
  var = tk.IntVar()
  datastore.flags['z'] = var
  checkButton = tk.Checkbutton(frame, text="Zeal 2 as last boss (z)", variable = var)
  checkButton.grid(row=row, column=2, sticky=tk.W, columnspan=2)
  CreateToolTip(checkButton, "The game ends after defeating Zeal 2 when going through the Black Omen.  Lavos is still required for the Ocean Palace route.")
  row = row + 1
  
  # Early pendant charge
  var = tk.IntVar()
  datastore.flags['p'] = var
  pendantCheckbox= tk.Checkbutton(frame, text="Early Pendant Charge (p)", variable = var)
  pendantCheckbox.grid(row=row, column=0, sticky=tk.W, columnspan=2)
  CreateToolTip(pendantCheckbox, "The pendant becomes charged immediately upon access to the Future, granting access to sealed doors and chests.")
  
  # Locked characters
  var = tk.IntVar()
  datastore.flags['c'] = var
  checkButton = tk.Checkbutton(frame, text="Locked characters (c)", variable = var)
  checkButton.grid(row=row, column=2, sticky=tk.W, columnspan=2)
  CreateToolTip(checkButton, "The Dreamstone is required to access the character in the Dactyl Nest and power must be turned on at the Factory before the Proto Dome character can be obtained.")
  row = row + 1

  # Unlocked Magic
  var = tk.IntVar()
  datastore.flags['m'] = var
  checkButton = tk.Checkbutton(frame, text="Unlocked Magic (m)", variable = var)
  checkButton.grid(row=row, column=0, sticky=tk.W, columnspan=2)
  CreateToolTip(checkButton, "Magic is unlocked at the start of the game, no trip to Spekkio required.")
  
  # Tab Treasures
  var = tk.IntVar()
  datastore.flags['tb'] = var
  checkButton = tk.Checkbutton(frame, text="Make all treasures tabs (tb)", variable = var)
  checkButton.grid(row=row, column=2, sticky=tk.W, columnspan=3)
  CreateToolTip(checkButton, "All treasures chest contents are replaced with power, magic, or speed tabs.")
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
  checkButton = tk.Checkbutton(frame, text="Chronosanity (cr)", variable = var, command=disableChronosanityIncompatibleFlags)
  checkButton.grid(row=row, sticky=tk.W, columnspan=2)
  CreateToolTip(checkButton, "Key items can now show up in most treasure chests in addition to their normal locations.")
  # row = row + 1

  # Duplicate Characters
  def dcEnable():
      if datastore.flags['dc'].get() == 1:
          dcSettingsButton.config(state=tk.ACTIVE)
      else:
          dcSettingsButton.config(state=tk.DISABLED)

  var = tk.IntVar()
  datastore.flags['dc'] = var
  checkButton = \
      tk.Checkbutton(frame, text="Duplicate Characters (dc)",
                     variable=var,
                     command=dcEnable)
  checkButton.grid(row=row, column=2, sticky=tk.W, columnspan=2)
  CreateToolTip(checkButton,
                "Characters can now show up more than once.  "
                + "Quests are activated and turned in based on the default "
                + "NAME of the character.")
  row = row + 1

  dcSettingsButton = tk.Button(frame, text='Duplicate Settings',
                               command=lambda: getDupOptionsWindow(window))
  # The datastore flags are not set yet, so we read directly from the settings
  # file to see if the dc settings should start off active or not.
  filePath = datastore.getSettingsFile()
  if filePath.exists():
      with open(str(filePath), 'rb') as setFile:
          settings = pickle.load(setFile)
          try:
              dc_enabled = settings['flags']['dc']
          except:
              dc_enabled = False
  else:
      dc_enabled = False

  if not dc_enabled:
      dcSettingsButton.config(state=tk.DISABLED)

  dcSettingsButton.grid(row=row, column=2, sticky=tk.W, columnspan=2)
  CreateToolTip(dcSettingsButton,
                'Settings for duplicate characters.  Must have dc flag ' +
                'enabled to activate this.')
  row += 1
  
  # Dropdown for shop price settings
  shopPriceValues = ["Normal", "Free", "Mostly Random", "Fully Random"]
  label = tk.Label(frame, text="Shop Prices:")
  var = tk.StringVar()
  var.set('Normal')
  datastore.shopPrices = var
  dropdown = tk.OptionMenu(frame, var, *shopPriceValues)
  dropdown.config(width = 20)
  label.grid(row = row, column = 0, sticky = tk.W)
  dropdown.grid(row = row, column = 1, sticky = tk.W, columnspan=2)
  CreateToolTip(dropdown, "Determines shop prices:\n"
      "Normal - Standard randomizer shop prices\n"
      "Free - Everything costs 1G (minimum allowed by the game)\n"
      "Mostly Random - Random prices except for some key consumables\n"
      "Fully Random - Random price for every item")
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
  dropdown.grid(row = row, column = 1, sticky=tk.W, columnspan=2)
  CreateToolTip(dropdown, "Determines the order in which techs are learned:\n"
      "Normal - Vanilla tech order.\n"
      "Balanced Random - Random tech order, but stronger techs are more likely to show up later.\n"
      "Fully Random - Tech order is fully randomized.")
  row = row + 1
  
  return frame

# Make the options window when someone clicks the DC Settings button.
# Will lock out input from other windows while open.
# Will preset an error message given invalid settings
def getDupOptionsWindow(window):
    dc_set = tk.Toplevel(window)

    def onClose():
        for i in range(len(datastore.char_choices)):
            isset = False
            for j in datastore.char_choices[i]:
                if j.get() == 1:
                    isset = True

            if isset is False:
                tk.messagebox.showerror('Error.',
                                        'Each character must have at least' +
                                        'one choice selected.')
                return

        dc_set.destroy()

    dc_set.protocol('WM_DELETE_WINDOW', onClose)

    dcframe = tk.Frame(dc_set, borderwidth=1, highlightbackground='black',
                       highlightthickness=1)

    row = 0
    col = 0

    char_names = ['Crono', 'Marle', 'Lucca', 'Robo', 'Frog', 'Ayla', 'Magus']

    tk.Label(dcframe,
             text='Indicate what each character is allowed to be randomized '
             + 'into using the checkboxes below.').grid(row=row, column=0,
                                                        columnspan=8)

    row += 1

    initialize = (datastore.char_choices is None)

    if initialize:
        datastore.char_choices = []
        for i in range(7):
            datastore.char_choices.append([])
            for j in range(7):
                datastore.char_choices[i].append(tk.IntVar(value=1))

        datastore.dup_techs = tk.IntVar(value=0)

    for i in range(7):
        tk.Label(dcframe,
                 text=char_names[i]+' choices:',
                 anchor="w").grid(row=row, column=0)

        col += 1

        for j in range(7):
            var = datastore.char_choices[i][j]
            tk.Checkbutton(dcframe, text=char_names[j],
                           variable=var).grid(row=row, column=col)

            col += 1

        col = 0
        row += 1

    dcframe.pack(expand=1, fill='both')

    dcframe = tk.Frame(dc_set, borderwidth=1, highlightbackground='black',
                       highlightthickness=1)

    def setAll(val):
        for i in range(len(datastore.char_choices)):
            for j in datastore.char_choices[i]:
                j.set(val)

    # Is it dumb to use argumentless lambdas for the commands?
    # Look into functools.partial
    button = tk.Button(dcframe, text='Check All',
                       command=lambda: setAll(1))
    button.grid(row=row, column=0, columnspan=2)

    button = tk.Button(dcframe, text='Uncheck All',
                       command=lambda: setAll(0))
    button.grid(row=row, column=2, columnspan=2)

    dcframe.pack(expand=1, fill='both')

    dcframe = tk.Frame(dc_set, borderwidth=1, highlightbackground='black',
                       highlightthickness=1)

    label = tk.Label(dcframe, text='Additional Options')
    label.grid(row=0, column=0)

    var = datastore.dup_techs
    checkbutton = tk.Checkbutton(dcframe, text='Duplicate Duals',
                                 variable=var)
    checkbutton.grid(row=1, column=0)
    CreateToolTip(checkbutton,
                  'Check this to enable dual techs betweeen copies of the '
                  + 'same character (e.g. Ayla+Ayla beast toss).')

    dcframe.pack(expand=1, fill='both')

    dcframe = tk.Frame(dc_set, borderwidth=1, highlightbackground='black',
                       highlightthickness=1)

    button = tk.Button(dcframe, text='Return',
                       command=onClose)
    button.grid()

    dcframe.pack(expand=1, fill='both')

    # Is this the right way to lock focus?
    dc_set.focus_get()
    dc_set.grab_set()

#
# Get the frame with the generate button and ROM selection
#
def getGenerateFrame(window):
  frame = tk.Frame(window, borderwidth = 1, highlightbackground="black", highlightthickness=1)
  frame.columnconfigure(4, weight=1)
  row = 0
  
  # Let the user choose a seed (optional parameter)
  label = tk.Label(frame, text="Seed(optional):")
  label.grid(row=row, column=0, sticky=tk.W+tk.E)
  datastore.seed = tk.StringVar()
  tk.Entry(frame, textvariable=datastore.seed).grid(row=row, column=1, columnspan=3)
  CreateToolTip(label, "Enter a seed for the randomizer.  Games generated with the same seed and flags will be identical every time.  This field is optional and a seed will be randomly selected if none is provided.")
  row = row + 1
  
  # Let the user select the base ROM to copy and patch
  label = tk.Label(frame, text="Input ROM:")
  label.grid(row=row, column=0, sticky=tk.W+tk.E)
  datastore.inputFile = tk.StringVar()
  tk.Entry(frame, textvariable=datastore.inputFile).grid(row=row, column=1, columnspan=3)
  tk.Button(frame, text="Browse", command=browseForRom).grid(row=row, column=4, sticky=tk.W)
  CreateToolTip(label, "The vanilla Chrono Trigger ROM used to generate a randomized game.")
  row = row + 1
  
  # Let the user select the base ROM to copy and patch
  label = tk.Label(frame, text="Output Folder:")
  label.grid(row=row, column=0, sticky=tk.W+tk.E)
  datastore.outputFolder = tk.StringVar()
  tk.Entry(frame, textvariable=datastore.outputFolder).grid(row=row, column=1, columnspan=3)
  tk.Button(frame, text="Browse", command=browseForOutputFolder).grid(row=row, column=4, sticky=tk.W)
  CreateToolTip(label, "The output location of the randomized ROM.  Defaults to the input ROM location if left blank.")
  row = row + 1

  # Add a progress bar to the GUI for ROM generation
  global progressBar
  progressBar = ttk.Progressbar(frame, orient='horizontal', mode='indeterminate')
  progressBar.grid(row = row, column = 0, columnspan = 5, sticky=tk.E+tk.W)
  row = row + 1
  
  tk.Button(frame, text="Generate", command=generateHandler).grid(row=row, column=2, sticky=tk.W, columnspan=2)
  
  return frame

#
# Main entry function for the GUI. Set up and launch the display.
#  
def guiMain():
  global optionsFrame
  mainWindow = tk.Tk()
  mainWindow.wm_title("Jets of Time")

  presetFrame = getPresetsFrame(mainWindow)
  presetFrame.pack(expand=1, fill="both")
  
  getGameOptionsFrame(mainWindow).pack(expand=1, fill="both")
  
  optionsFrame = getRandomizerOptionsFrame(mainWindow)
  optionsFrame.pack(expand=1, fill="both")
  
  getGenerateFrame(mainWindow).pack(expand=1, fill="both")
  datastore.load()
    
  mainWindow.mainloop()
  
