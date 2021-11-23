import random as rand
import struct as st
import characterwriter as chars
def determine_char_locks(loclist,charlocs,charkey):
    char = charlocs [charkey] [0]
    if char == 3 and "desert" not in loclist:
       loclist.append("desert")
    if char == 1 and "trial1" not in loclist:
       loclist.append("trial1")
    if char == 4 and "sword3" not in loclist:
       loclist.append("sword3")
def rename_chars(charlocs):
    for charkey in charlocs:
        char = charlocs [charkey] [0]
        if char == 0:
           char = "Chrono"
        if char == 1:
           char = "Marle"
        if char == 2:
           char = "Lucca"
        if char == 3:
           char = "Robo"
        if char == 4:
           char = "Frog"
        if char == 5:
           char = "Ayla"
        if char == 6:
           char = "Magus"
        charlocs [charkey] = char
    return charlocs
def parse_keys(provided_key):
    if provided_key == "pop":
        provided_key = 0xE3
    if provided_key == "hilt":
        provided_key = 0x51
    if provided_key == "blade":
        provided_key = 0x50
    if provided_key == "stone":
        provided_key = 0xDC
    if provided_key == "knife":
       provided_key = 0xE0
    if provided_key == "gate":
       provided_key = 0xD7
    if provided_key == "bike":
       provided_key = 0xD5
    if provided_key == "jerky":
       provided_key = 0xDB
    if provided_key == "pendant":
       provided_key = 0xD6
    if provided_key == "moon":
       provided_key = 0xDE
    if provided_key == "prism":
       provided_key = 0xD8
    if provided_key == "masa2":
       provided_key = 0x42
    if provided_key == "clone":
       provided_key = 0xE2
    if provided_key == "trigger":
       provided_key = 0xD9
    if provided_key == "medal":
       provided_key = 0xB3
    if provided_key == "ribbon":
       provided_key = 0xB8
    return provided_key
def randomize_keys(char_locs,outfile,locked_chars):
    loclist = []
    complete_list = [2300,"sword1","sword2","sword3","dream","desert","giant","trial1","trial2","melchior",
    "burrow","ruins","endoftime","palace","omen1","omen2"]
    char_keys = ["start","start2","cathedral","castle","proto","burrow","dactyl"]
    iterations = 0
    while len(loclist) != len(complete_list) and iterations != 3600:
       loclist = []
       keyitems = ["pop","hilt","blade","stone","knife","gate","jerky","pendant","moon","prism","masa2","clone",
       "trigger","medal","ribbon"]
       locations = {"zenan": "","taban": "","denadoro": "","snail": "","burrow": "","carpenter": "","trial": "",
       "melchior": "","claw": "","desert": "","arris": "","geno": "","sun": "","reptite": "","woe": ""}
       lockeys = ["zenan","taban","denadoro","snail","carpenter"]
       for loc in locations:
          chosen = rand.choice(keyitems)
          locations[loc] = chosen
          keyitems.remove(chosen)
       i = 0
       while i < 4:
          determine_char_locks(loclist,char_locs,char_keys[i])
          i += 1	  
       i = 0
       while i < len(lockeys):
          heldkey = locations[lockeys[i]]
          if heldkey == "blade":
              loclist.append("sword1")
          elif heldkey == "hilt":
              loclist.append("sword2")
          elif heldkey == "stone":
              loclist.append("dream")
          elif heldkey == "prism":
              loclist.append("trial2")
          elif heldkey == "pop":
              loclist.append("giant")
          elif heldkey == "pendant":
              loclist.append(2300)
          elif heldkey == "masa2":
              loclist.append("ruins")
          elif heldkey == "medal":
              loclist.append("burrow")
          elif heldkey == "gate":
              loclist.append("endoftime")
          elif heldkey == "clone":
              loclist.append("omen1")
          elif heldkey == "trigger":
              loclist.append("omen2")
          elif heldkey == "knife":
              loclist.append("palace")
          elif heldkey == "moon":
              loclist.append("melchior")
          if 2300 in loclist and "arris" not in lockeys:
              lockeys.append("arris")
              lockeys.append("geno")
              lockeys.append("sun")
              if "woe" not in lockeys:
                  lockeys.append("woe")
              determine_char_locks(loclist,char_locs,"proto")
          if "endoftime" in loclist:
            if "woe" not in lockeys:
                lockeys.append("woe")          
            if "reptite" not in lockeys:
                lockeys.append("reptite")
                if locked_chars != "Y":                     
                    determine_char_locks(loclist,char_locs,"dactyl")
                if "dream" in loclist and locked_chars == "Y":
                    determine_char_locks(loclist,char_locs,"dactyl")
          if "giant" in loclist and "claw" not in lockeys:
              lockeys.append("claw")
          if "trial1" in loclist and "trial2" in loclist and "trial" not in lockeys:
              lockeys.append("trial")
          if "burrow" in loclist and "burrow" not in lockeys:
              lockeys.append("burrow")
          if "desert" in loclist and "desert" not in lockeys:
              lockeys.append("desert")
          if "sword1" in loclist and "sword2" in loclist:
              determine_char_locks(loclist,char_locs,"burrow")
          if "endoftime" in loclist and "trial" in lockeys \
          and "melchior" in loclist and 2300 in loclist and "melchior" not in lockeys:
                lockeys.append("melchior")
          i += 1
       iterations += 1
    if iterations == 3600:
       print("Oops, ran out of attempts. Please try again!")
    else:
       ordered_keys = ["zenan" ,"taban" ,"denadoro" ,"snail" ,"burrow" ,"carpenter" ,"trial" ,
       "melchior" ,"claw" ,"desert" ,"arris" ,"geno" ,"sun" ,"reptite" ,"woe"]
       pointer1 = [0x393C83,0x35F888,0x3773F1,0x380C42,0x3891DE,0x3966B,0x38045D,0x3805DE,0x1B8ABB,
       0x6EF5E,0x392F4C,0x1B1844,0x1B8D95,0x18FC04,0x381010]
       pointer2 = [0x393C85,0x35F88A,0x3773F3,0x380C5B,0x3891E0,0x3966D,0x38045F,0x3805E0,
       0x1B8ABF,0x6EF61,0x392F4E,0x1B1846,0x1B8D97,0x18FC07,0x381013]
       i = 0
       while i < len(ordered_keys):
           written_key = locations[ordered_keys[i]]
           written_key = parse_keys(written_key)
           f = open(outfile,"r+b")
           f.seek(pointer1[i])
           f.write(st.pack("B",written_key))
           f.seek(pointer2[i])
           f.write(st.pack("B",written_key))
           i += 1
           f.close()
    f = open("spoiler_log.txt","w+")
    rename_chars(char_locs)
    f.write(f"{str(locations)}\n{str(char_locs)}")
    f.close()
    return locations
def randomize_lost_worlds_keys(char_locs,outfile):
    loclist = []
    iterations = 0
    complete_list = ["dream","palace","omen1","omen2"]
    while len(loclist) != len(complete_list) and iterations != 3600:
        loclist = []
        keyitems = ["stone","knife","clone","trigger","pendant"]
        locations = {"arris": "","geno": "","sun": "","reptite": "","woe": ""}
        lockeys = ["arris","geno","sun","reptite","woe"]
        for loc in locations:
          chosen = rand.choice(keyitems)
          locations[loc] = chosen
          keyitems.remove(chosen)
        i = 0
        while i < len(lockeys):
           heldkey = locations[lockeys[i]]
           if heldkey == "stone":
              loclist.append("dream")
           elif heldkey == "clone":
              loclist.append("omen1")
           elif heldkey == "trigger":
              loclist.append("omen2")
           elif heldkey == "knife":
              loclist.append("palace")
           if "endoftime" in loclist and "trial" in lockeys \
           and "melchior" in loclist and 2300 in loclist and "melchior" not in lockeys:
                lockeys.append("melchior")
           i += 1
        iterations += 1
    if iterations == 3600:
       print("Oops, ran out of attempts. Please try again!")
    else:
       ordered_keys = ["arris" ,"geno" ,"sun" ,"reptite" ,"woe"]
       pointer1 = [0x392F4C,0x1B1844,0x1B8D95,0x18FC04,0x381010]
       pointer2 = [0x392F4E,0x1B1846,0x1B8D97,0x18FC07,0x381013]
       i = 0
       while i < len(ordered_keys):
           written_key = locations[ordered_keys[i]]
           written_key = parse_keys(written_key)
           f = open(outfile,"r+b")
           f.seek(pointer1[i])
           f.write(st.pack("B",written_key))
           f.seek(pointer2[i])
           f.write(st.pack("B",written_key))
           i += 1
           f.close()
    f = open("spoiler_log.txt","w+")
    rename_chars(char_locs)
    f.write(f"{str(locations)}\n{str(char_locs)}")
    f.close()
    return locations
if __name__ == "__main__":
    char_locations = chars.randomize_char_positions("Project.sfc","Y")
    randomize_keys(char_locations,"Project.sfc","Y")
