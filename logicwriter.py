import random as rand
import struct as st
import characterwriter as characters
def determine_char_locks(charlocs,charkey):
    char = charlocs [charkey] [0]
    if char == 3:
       loclist.append("desert")
    if char == 1:
       loclist.append("trial1")
loclist = []
complete_list = [2300,"sword1","sword2","sword3","desert","giant","trial1","trial2","melchior","burrow",
"ruins","endoftime","palace","omen1","omen2"]
charlocs = characters.randomize_char_positions("Projectfile.smc")
char_keys = ["start","start2","cathedral","castle","proto","burrow","dactyl"]
iterations = 0
while len(loclist) != len(complete_list) and iterations != 3600:
    loclist = []
    keyitems = ["pop","hilt","blade","stone","knife","gate","bike","jerky","pendant","moon","prism","tools",
    "clone","trigger","medal","ribbon"]
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
      determine_char_locks(charlocs,char_keys[i])
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
        elif heldkey == "knife":
            loclist.append("palace")
        elif heldkey == "moon":
            loclist.append("melchior")
        if 2300 in loclist and "endoftime" in loclist and "arris" not in lockeys: 
            lockeys.append("arris")
            lockeys.append("geno")
            lockeys.append("sun")
            determine_char_locks(charlocs,"proto")
        if "giant" in loclist and "claw" not in lockeys:
            lockeys.append("claw")
        if "trial1" in loclist and "trial2" in loclist and "trial" not in lockeys:
            lockeys.append("trial")
        if "burrow" in loclist and "burrow" not in lockeys:
            lockeys.append("burrow")
        if "desert" in loclist and "endoftime" in loclist and "desert" not in lockeys:
            lockeys.append("desert")
        if "sword1" in loclist and "sword2" in loclist and "sword3" in loclist and \
        "endoftime" in loclist and "reptite" not in lockeys:
            lockeys.append("reptite")
            lockeys.append("woe")
            determine_char_locks(charlocs,"dactyl")
        if "sword1" in loclist and "sword2" in loclist and "sword3" in loclist and \
        "trial1" in loclist and "trial2" in loclist and "melchior" in loclist and "melchior" \
        not in lockeys:
            lockeys.append("melchior")
        i += 1
    iterations += 1
if iterations == 3600:
    print "Oops, ran out of attempts. Please try again!"
f = open("spoiler_log.txt","w+")
f.write(str(locations))
f.close