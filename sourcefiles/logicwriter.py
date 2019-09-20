import random as rand
import struct as st
def determine_char_locks(loclist,charlocs,charkey):
    char = charlocs [charkey] [0]
    if char == 3:
       loclist.append("desert")
    if char == 1:
       loclist.append("trial1")
    if char == 4:
       loclist.append("sword4")
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
    if provided_key == "tools":
       provided_key = 0xDA
    if provided_key == "clone":
       provided_key = 0xE2
    if provided_key == "trigger":
       provided_key = 0xD9
    if provided_key == "medal":
       provided_key = 0xB3
    if provided_key == "ribbon":
       provided_key = 0xB8
    return provided_key
def randomize_keys(char_locs,outfile):
    loclist = []
    complete_list = [2300,"sword1","sword2","sword3","sword4","desert","giant","trial1","trial2","melchior1",
    "melchior2","burrow","ruins","endoftime","palace","omen1","omen2"]
    char_keys = ["start","start2","cathedral","castle","proto","burrow","dactyl"]
    iterations = 0
    while len(loclist) != len(complete_list) and iterations != 3600:
       loclist = []
       keyitems = ["pop","hilt","blade","stone","knife","gate","bike","jerky","pendant","moon","prism",
       "tools", "clone","trigger","medal","ribbon"]
       locations = {"zenan": "","denadoro1": "","denadoro2": "","snail": "","toma": "","burrow": "",
       "carpenter": "","trial": "","melchior": "","claw": "","desert": "","arris": "","geno": "","sun": "",
       "reptite": "","woe": ""}
       lockeys = ["zenan","denadoro1","denadoro2","snail","toma","carpenter"]
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
              loclist.append("sword3")
          elif heldkey == "prism":
              loclist.append("trial2")
          elif heldkey == "pop":
              loclist.append("giant")
          elif heldkey == "pendant":
              loclist.append(2300)
          elif heldkey == "tools":
              loclist.append("ruins")
          elif heldkey == "medal":
              loclist.append("burrow")
          elif heldkey == "gate":
              loclist.append("endoftime")
          elif heldkey == "clone":
              loclist.append("omen1")
          elif heldkey == "trigger":
              loclist.append("omen2")
          elif heldkey == "jerky":
              loclist.append("melchior2")
          elif heldkey == "knife":
              loclist.append("palace")
          elif heldkey == "moon":
              loclist.append("melchior1")
          if 2300 in loclist and "endoftime" in loclist and "arris" not in lockeys: 
              lockeys.append("arris")
              lockeys.append("geno")
              lockeys.append("sun")
              determine_char_locks(loclist,char_locs,"proto")
          if "giant" in loclist and "claw" not in lockeys:
              lockeys.append("claw")
          if "trial1" in loclist and "trial2" in loclist and "trial" not in lockeys:
              lockeys.append("trial")
          if "burrow" in loclist and "burrow" not in lockeys:
              lockeys.append("burrow")
          if "desert" in loclist and "endoftime" in loclist and "desert" not in lockeys:
              lockeys.append("desert")
          if "sword1" in loclist and "sword2" in loclist and "sword3" in loclist and "sword4" in loclist\
          "endoftime" in loclist and "reptite" not in lockeys:
              lockeys.append("reptite")
              lockeys.append("woe")
              determine_char_locks(loclist,char_locs,"dactyl")
          if "sword1" in loclist and "sword2" in loclist and "sword3" in loclist and \
          "trial1" in loclist and "trial2" in loclist and "melchior1" in loclist and "melchior2" \
          in loclist and 2300 in loclist and "melchior" not in lockeys:
              lockeys.append("melchior")
          i += 1
       iterations += 1
    if iterations == 3600:
       print "Oops, ran out of attempts. Please try again!"
    else:
       ordered_keys = ["zenan" ,"denadoro1" ,"denadoro2" ,"snail" ,"toma" ,"burrow" ,"carpenter" ,"trial" ,
       "melchior" ,"claw" ,"desert" ,"arris" ,"geno" ,"sun" ,"reptite" ,"woe"]
       pointer1 = [0x393C82,0x37742F,0x18D40A,0x380C42,0x16FB36,0x1BDA37,0x3966B,0x38045D,0x3805DE,
       0x1B8AEC,0x6EF5E,0x1B4DCF,0x1B1844,0x1B8D89,0x18FC2C,0x381010]
       pointer2 = [0x393C84,0x377432,0x18D40C,0x380C5B,0x16FB38,0x1BDA3A,0x3966D,0x38045F,0x3805E0,
       0x1B8AEF,0x6EF61,0x1B4DD2,0x1B1846,0x1B8D8B,0x18FC2F,0x381013]
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
           f.close
    f = open("spoiler_log.txt","w+")
    f.write(str(locations))
    f.close