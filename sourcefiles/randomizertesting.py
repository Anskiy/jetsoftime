from shutil import copyfile
import struct as st
from os import stat
from time import time
import sys
import treasurewriter as treasures
import specialwriter as hardcoded_items
import shopwriter as shops
import characterwritertesting as char_slots
import logicwriter as keyitems
import random as rand
import logicwriter_chronosanity as chronosanity_logic
import ipswriter as bigpatches
import patcher as patches
import enemywriter as enemystuff
import bossrando as boss_shuffler
import bossscaler as boss_scale
import techwriter as tech_order
import randomizerguitesting as gui
import tabchange as tabwriter

def tenthousands_digit(digit):
    digit = st.unpack(">B",digit)
    digit = int(digit[0]) * 0x10000
    return digit       
def make_number(digit,digit2):
       digit2 = st.unpack(">H",digit2)
       digit2 = int(digit2[0])
       number = digit + digit2
#       print "{:X}".format(number)
       return number
def get_length(length):
       length = st.unpack(">H",length)
       length = int(length[0])
       return length
def write_data(length,pointer,position):
        bRepeatable = False
        if length == 0:
            length = p.read(2)
            length = get_length(length)
            data = get_data()            
            position += 3
            bRepeatable = True
        while length > 0:
          if not bRepeatable:
            data = get_data()
            position += 1
          f.seek(pointer)
          f.write(st.pack("B",data))
          pointer += 1
          length -= 1
        return position
def get_data():
        data = p.read(1)
        data = st.unpack("B",data)
        data = int(data[0])
        return data
def read_names():
        p = open("names.txt","r")
        names = p.readline()
        names = names.split(",")
        p.close()
        return names

# Script variables
flags = ""
sourcefile = ""
difficulty = ""
glitch_fixes = ""
fast_move = ""
sense_dpad = ""
lost_worlds = ""
boss_scaler = ""
zeal_end = ""
quick_pendant = ""
locked_chars = ""
tech_list = ""
seed = ""
tech_list = ""
unlocked_magic = ""
characters = ['Crono', 'Marle', 'Lucca', 'Frog', 'Robo', 'Ayla', 'Magus']
char_locs = []
quiet_mode = ""
chronosanity = ""
tab_treasures = ""
boss_rando = ""
shop_prices = ""
   
#
# Handle the command line interface for the randomizer.
#   
def command_line():
     global flags
     global sourcefile
     global difficulty
     global glitch_fixes
     global fast_move
     global sense_dpad
     global lost_worlds
     global boss_scaler
     global zeal_end
     global quick_pendant
     global locked_chars
     global tech_list
     global seed
     global tech_list_balanced
     global unlocked_magic
     global chronosanity
     global tab_treasures
     global boss_rando
     global shop_prices
     
     flags = ""
     sourcefile = input("Please enter ROM name or drag it onto the screen.")
     sourcefile = sourcefile.strip("\"")
     if sourcefile.find(".sfc") == -1:
         if sourcefile.find(".smc") == - 1:
             input("Invalid File Name. Try placing the ROM in the same folder as the randomizer. Also, try writing the extension(.sfc/smc).")
             exit()
     seed = input("Enter seed(or leave blank if you want to randomly generate one).")
     if seed is None or seed == "":
        names = read_names()
        seed = "".join(rand.choice(names) for i in range(2))
     rand.seed(seed)
     difficulty = input(f"Choose your difficulty \nEasy(e)/Normal(n)/Hard(h)")
     if difficulty == "n":
         difficulty = "normal"
     elif difficulty == "e":
         difficulty = "easy"
     else:
         difficulty = "hard"
     flags = flags + difficulty[0]
     glitch_fixes = input("Would you like to disable (most known) glitches(g)? Y/N ")
     glitch_fixes = glitch_fixes.upper()
     if glitch_fixes == "Y":
        flags = flags + "g" 
     fast_move = input("Would you like to move faster on the overworld/Epoch(s)? Y/N ")
     fast_move = fast_move.upper()
     if fast_move == "Y":
        flags = flags + "s"
     sense_dpad = input("Would you like faster dpad inputs in menus(d)? Y/N ")
     sense_dpad = sense_dpad.upper()
     if sense_dpad == "Y":
        flags = flags + "d"
     lost_worlds = input("Would you want to activate Lost Worlds(l)? Y/N ")
     lost_worlds = lost_worlds.upper()
     if lost_worlds == "Y":
         flags = flags + "l"
     boss_scaler = input("Do you want bosses to scale with progression(b)? Y/N ")
     boss_scaler = boss_scaler.upper()
     if boss_scaler == "Y":
        flags = flags + "b"
     boss_rando = input("Do you want randomized bosses(ro)? Y/N ")
     boss_rando = boss_rando.upper()
     if boss_rando == "Y":
        flags = flags + "ro"     
     zeal_end = input("Would you like Zeal 2 to be a final boss? Note that defeating Lavos still ends the game(z). Y/N ")
     zeal_end = zeal_end.upper()
     if zeal_end == "Y":
        flags = flags + "z"
     if lost_worlds == "Y":
        pass
     else:
         quick_pendant = input("Do you want the pendant to be charged earlier(p)? Y/N ")
         quick_pendant = quick_pendant.upper()
         if quick_pendant == "Y":
            flags = flags + "p"
     locked_chars = input("Do you want characters to be further locked(c)? Y/N ")
     locked_chars = locked_chars.upper()
     if locked_chars == "Y":
        flags = flags + "c"
     tech_list = input("Do you want to randomize techs(te)? Y/N ")
     tech_list = tech_list.upper()
     if tech_list == "Y":
         flags = flags + "te"
         tech_list = "Fully Random"
         tech_list_balanced = input("Do you want to balance the randomized techs(tex)? Y/N ")
         tech_list_balanced = tech_list_balanced.upper()
         if tech_list_balanced == "Y":
            flags = flags + "x"
            tech_list = "Balanced Random"
     unlocked_magic = input("Do you want the ability to learn all techs without visiting Spekkio(m)? Y/N")
     unlocked_magic = unlocked_magic.upper()
     if unlocked_magic == "Y":
         flags = flags + "te"
     quiet_mode = input("Do you want to enable quiet mode (No music)(q)? Y/N")
     quiet_mode = quiet_mode.upper()
     if quiet_mode == "Y":
         flags = flags + "q"
     chronosanity = input("Do you want to enable Chronosanity (key items can appear in chests)? (cr)? Y/N")
     chronosanity = chronosanity.upper()
     if chronosanity == "Y":
         flags = flags + "cr"
     tab_treasures = input("Do you want all treasures to be tabs(tb)? Y/N ")
     tab_treasures = tab_treasures.upper()
     if tab_treasures == "Y":
        flags = flags + "tb"
     shop_prices = input("Do you want shop prices to be Normal(n), Free(f), Mostly Random(m), or Fully Random(r)?")
     shop_prices = shop_prices.upper()
     if shop_prices == "F":
        shop_prices = "Free"
        flags = flags + "spf"
     elif shop_prices == "M":
        shop_prices = "Mostly Random"
        flags = flags + "spm"
     elif shop_prices == "R":
        shop_prices = "Fully_Random"
        flags = flags + "spr"
     else:
        shop_prices = "Normal"

#
# Given a tk IntVar, convert it to a Y/N value for use by the randomizer.
#
def get_flag_value(flag_var):
  if flag_var.get() == 1:
    return "Y"
  else:
    return "N"
  
#
# Handle seed generation from the GUI.
# Convert all of the GUI datastore values internal values
# for the randomizer and then generate the ROM.
#  
def handle_gui(datastore):
  global flags
  global sourcefile
  global difficulty
  global glitch_fixes
  global fast_move
  global sense_dpad
  global lost_worlds
  global boss_scaler
  global zeal_end
  global quick_pendant
  global locked_chars
  global tech_list
  global seed
  global characters
  global char_locs
  global unlocked_magic
  global quiet_mode
  global chronosanity
  global tab_treasures
  global boss_rando
  global shop_prices

  # Hopefully get the chosen character locations
  x = 0
  while x < len(characters):
    if len(char_locs)>6:
        char_locs[x] = datastore.charLocVars[characters[x]].get()
    else :
        char_locs.append(datastore.charLocVars[characters[x]].get())
    x = x + 1
  
  # Get the user's chosen difficulty
  difficulty = datastore.difficulty.get()

  # Get the user's chosen tech randomization
  tech_list = datastore.techRando.get()
  
  # Get the user's chosen shop price settings
  shop_prices = datastore.shopPrices.get()
  
  # build the flag string from the gui datastore vars
  flags = difficulty[0]
  for flag, value in datastore.flags.items():
    if value.get() == 1:
      flags = flags + flag
  if tech_list == "Fully Random":
      flags = flags + "te"
  elif tech_list == "Balanced Random":
      flags = flags + "tex"
  
  # Set the flag variables based on what the user chose
  glitch_fixes = get_flag_value(datastore.flags['g'])
  fast_move = get_flag_value(datastore.flags['s'])
  sense_dpad = get_flag_value(datastore.flags['d'])
  lost_worlds = get_flag_value(datastore.flags['l'])
  boss_scaler = get_flag_value(datastore.flags['b'])
  boss_rando = get_flag_value(datastore.flags['ro'])
  zeal_end = get_flag_value(datastore.flags['z'])
  quick_pendant = get_flag_value(datastore.flags['p'])
  locked_chars = get_flag_value(datastore.flags['c'])
  unlocked_magic = get_flag_value(datastore.flags['m'])
  quiet_mode = get_flag_value(datastore.flags['q'])
  chronosanity = get_flag_value(datastore.flags['cr'])
  tab_treasures = get_flag_value(datastore.flags['tb'])
  
  # source ROM
  sourcefile = datastore.inputFile.get()
  
  # seed
  seed = datastore.seed.get()
  if seed is None or seed == "":
    names = read_names()
    seed = "".join(rand.choice(names) for i in range(2))
  rand.seed(seed)
  datastore.seed.set(seed)
  
  # GUI values have been converted, generate the ROM.
  generate_rom()
   
   
#
# Generate the randomized ROM.
#    
def generate_rom():
     global flags
     global sourcefile
     global difficulty
     global glitch_fixes
     global fast_move
     global sense_dpad
     global lost_worlds
     global boss_rando
     global boss_scaler
     global zeal_end
     global quick_pendant
     global locked_chars
     global tech_list
     global seed
     global characters
     global char_locs
     global unlocked_magic
     global quiet_mode
     global chronosanity
     global tab_treasures
     global shop_prices
     
     outfile = sourcefile.split(".")
     outfile = str(outfile[0])
     if flags == "":
       outfile = "%s.%s.sfc"%(outfile,seed)
     else:
       outfile = "%s.%s.%s.sfc"%(outfile,flags,seed)
     size = stat(sourcefile).st_size
     if size % 0x400 == 0:
        copyfile(sourcefile, outfile)
     elif size % 0x200 == 0:
        print("SNES header detected. Removing header from output file.")
        f = open(sourcefile, 'r+b')
        data = f.read()
        f.close()
        data = data[0x200:]
        open(outfile, 'w+').close()
        f = open(outfile, 'r+b')
        f.write(data)
        f.close()
     print("Applying patch. This might take a while.")
     bigpatches.write_patch("patch.ips",outfile)
     patches.patch_file("patches/patch_codebase.txt",outfile)
     if glitch_fixes == "Y":
        patches.patch_file("patches/save_anywhere_patch.txt",outfile)
        patches.patch_file("patches/unequip_patch.txt",outfile)
        patches.patch_file("patches/fadeout_patch.txt",outfile)
        patches.patch_file("patches/hp_overflow_patch.txt",outfile)
     if fast_move == "Y":
        patches.patch_file("patches/fast_overworld_walk_patch.txt",outfile)
        patches.patch_file("patches/faster_epoch_patch.txt",outfile)
     if sense_dpad == "Y":
        patches.patch_file("patches/faster_menu_dpad.txt",outfile)
     if zeal_end == "Y":
        patches.patch_file("patches/zeal_end_boss.txt",outfile)
     if lost_worlds == "Y":
        bigpatches.write_patch("patches/lost.ips",outfile)
     if lost_worlds == "Y":
         pass
     elif quick_pendant == "Y":
             patches.patch_file("patches/fast_charge_pendant.txt",outfile)
     if unlocked_magic == "Y":
         bigpatches.write_patch("patches/fastmagic.ips",outfile)
     if difficulty == "hard":
         bigpatches.write_patch("patches/hard.ips",outfile)
     tabwriter.rewrite_tabs(outfile)
     print("Randomizing treasures...")
     treasures.randomize_treasures(outfile,difficulty, tab_treasures)
     hardcoded_items.randomize_hardcoded_items(outfile, tab_treasures)
     print("Randomizing enemy loot...")
     enemystuff.randomize_enemy_stuff(outfile,difficulty)
     print("Randomizing shops...")
     shops.randomize_shops(outfile)
     shops.modify_shop_prices(outfile, shop_prices)
     print("Randomizing character locations...")
     char_locs = char_slots.randomize_char_positions(outfile,locked_chars,lost_worlds,characters,char_locs)
     print("Now placing key items...")
     if chronosanity == "Y":
       chronosanity_logic.writeKeyItems(
           outfile, char_locs, (locked_chars == "Y"), (quick_pendant == "Y"), lost_worlds == "Y")
     elif lost_worlds == "Y":
       keyitemlist = keyitems.randomize_lost_worlds_keys(char_locs,outfile)
     else:
       keyitemlist = keyitems.randomize_keys(char_locs,outfile,locked_chars)
     if boss_scaler == "Y" and chronosanity != "Y":
         print("Rescaling bosses based on key items..")
         boss_scale.scale_bosses(char_locs,keyitemlist,locked_chars,outfile)
     if boss_rando == "Y":
         boss_shuffler.randomize_bosses(outfile,difficulty)
         boss_shuffler.randomize_dualbosses(outfile,difficulty)
     if tech_list == "Fully Random":
         tech_order.take_pointer(outfile)
     elif tech_list == "Balanced Random":
         tech_order.take_pointer_balanced(outfile)
     if quiet_mode == "Y":
         bigpatches.write_patch("patches/nomusic.ips",outfile)
     # Tyrano Castle chest hack
     f = open(outfile,"r+b")
     f.seek(0x35F6D5)
     f.write(st.pack("B",1))
     f.close()
     #Mystic Mtn event fix in Lost Worlds
     if lost_worlds == "Y":         
       f = open(outfile,"r+b")
       bigpatches.write_patch("patches/mysticmtnfix.ips",outfile)
       bigpatches.write_patch("patches/losteot.ips",outfile)
     #Bangor Dome event fix if character locks are on
       if locked_chars == "Y":
         bigpatches.write_patch("patches/bangorfix.ips",outfile)
       f.close()
     print("Randomization completed successfully.")
     
     
     
if __name__ == "__main__":
  if len(sys.argv) > 1 and sys.argv[1] == "-c":
    command_line()
    generate_rom()
    input("Press Enter to exit.")
  else:
    gui.guiMain()
  
