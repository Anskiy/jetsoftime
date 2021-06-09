import random as rand
import struct as st
import patcher as patch

# Start marker:  0xC4700
# Boss stats:  
# Byte 0+1 - HP
# Byte 2 - Level
# Byte 10 - Magic
# Byte 13 - Magic Defense
# Byte 14 - Offense
# Byte 15 - Defense

# Start reward marker:  0xC5E00
# Byte 0+1 - XP
# Byte 2+3 - GP
# Byte 4 - Item Drop
# Byte 5 - Charm Item
# Byte 6 - TP

# Bosses:  04 - Krawlie, 90 - Yakra, 95 - Golem, 4F - Twin Golem, 99 - Masa & Mune, 9B - Nizbel, 9C - Nizbel II, 9D - Slash, 9E - Slash w/ Sword, 9F - Flea
#          A1 - Dalton, A2 - Dalton Plus, A5 - Super Slash, A9 - Heckran, BB - Flea Plus, BD - Rust Tyrano, C0 - Atropus XR, C7 - Yakra XIII, F3 - Golem Boss

# Yakra
# Masa&Mune, Heckran
# Slash, Flea, Golem, Twin Golem
# Nizbel, Rust Tyrano, Yakra 13, Nizbel II
spots =      [0x1B38C2, 0x377824, 0x24EC52, 0x3ABF86, 0x1ED226, 0x1BEBBB, 0x38821C, 0x18FC30, 0x1B8A4C, 0x36F40B, 0x5FBBA]
spot_tiers = [0,1,1,2,2,3,4,2,2,2,2]
boss_hp =    [920,3600,2100,4000,3800,6000,7000,5000,5000,4500,5400]
hard_hp =    [920,3600,2100,5000,4200,7000,8000,6000,6000,5200,5800]

#Two target bosses
#Boss parts:  B3 - Zombor's legs, B4 - Zombor's head, D7 - Lavos Spawn's shell, D8 - Lavos Spawn's head, B8 - Mega Mutant's head, B9 - Mega Mutant's bottom,
#             35 - Giga Mutant's head, 36 - Giga Mutant's bottom, 37 - Terra Mutant's head, 38 - Terra Mutant's bottom, 6E - Elder Lavos Spawn's head,
#             6F - Elder Lavos Spawn's shell

#Zombor legs, Zombor head, 
#Lavos Spawn shell, Lavos Spawn head, 
#Giga Mutant head, Giga Mutant bottom, Terra Mutant head, Terra Mutant bottom, Elder Lavos Spawn shell, Elder Lavos Spawn head

dualboss_spots1 = [0x1CE3A7, 0x18EFA0, 0x21FCEC, 0x367084, 0x1EF864]
dualboss_spots2 = [0x1CE370, 0x18F00E, 0x21FD17, 0x3670AF, 0x1EF894]
dualboss_spot_tiers = [0,2,4,4,4]
#slot_ids1 = [3,0x83,3,3,3]
#slot_ids2 = [9,9,9,9,9]  
#dualboss_slot_addrs1 = [0x1CE3A8, 0x18EFA1, 0x21FCEE, 0x367085, 0x1EF865]
dualboss_slot_addrs2 = [0x1CE371, 0x18F00F, 0x21FD18, 0x3670B0, 0x1EF895]
dualboss_hp1 = [880,5000,5500,7000,10000]
dualboss_hp2 = [1172,5000,5500,7000,10000]
dualboss_hard_hp1 = [880,6000,6500,9000,12000]
dualboss_hard_hp2 = [1172,6000,6500,9000,12000]


#Order of stats: Pointer(where applicable), HP, Level, Magic, Magic Defense, Offense, Defense, XP, GP, TP
#krawlie_spot = [500, 8, 5, 50, 44, 150, 100, 500, 5]
#yakra_spot = [0x1B38C2, 920, 6, 9, 50, 16, 127, 200, 600, 5] # Changes:  50 -> 200 XP
#golem_spot = [0x1BEBBB, 6000, 15, 25, 50, 192, 127, 2500, 4000, 40]
#twin_golem_spot = [0x38821C,7000,34,60,50,210,127,2000,5000,127]
#masamune_spot = [0x377824, 3600, 10, 9, 50, 100, 127, 500, 1500, 10]
#nizbel_spot = [0x18FC30, 5000, 10, 15, 55, 125, 253, 3000, 2200, 35]
#nizbel2_spot = [0x5FBBA, 5400, 15, 20, 50, 135, 253, 3500, 3100, 46]
#slash_spot = [4000, 10, 10, 60, 165, 127, 1400, 2100, 12]
#slashsword_spot = [0x3ABF86, 4000, 10, 10, 60, 165, 127, 2800, 4200, 25]
#flea_spot = [0x1ED226, 3800, 15, 15, 60, 100, 150, 2500, 4800, 30]
#dalton_spot = [9000, 37, 33, 50, 200, 127, 3000, 1600, 50]
#daltonplus_spot = [5000, 15, 12, 50, 75, 127, 2500, 2000, 20]
#superslash_spot = [0x16FF0D, 2500, 35, 10, 50, 120, 127, 2000, 2000, 20]
#heckran_spot = [0x24EC52, 2100, 13, 16, 50, 40, 253, 600, 1500, 10]
#fleaplus_spot = [0x1BBE0D, 2500, 35, 15, 50, 120, 127, 2000, 2000, 20]
#rusttyrano_spot = [0x1B8A4C, 5000, 16, 15, 50, 160, 127, 2400, 2000, 40]
#atropos_XR_spot = [4000, 15, 15, 50, 100, 127, 2400, 2000, 40]
#yakra13_spot = [0x36F40B, 4500, 17, 18, 50, 66, 127, 2200, 2000, 40]
#golemboss_spot = [5000, 37, 37, 58, 210, 127, 2500, 2000, 40]
#NOTE: + is used to separate stats belonging to two different parts, don't directly add them!
#zombor_spot = [0x1CE3A7 + 0x1CE370, 880 + 1172, 6, 7, 50, 35, 151, 350, 1500, 10]
#lavos_spawn_spot = [0x18EFA0 + 0x18F00E, 10000 + 5000, 37 + 15, 17 + 15, 100 + 50, 75, 253 + 127, 2500, 2000, 20]
#mega_mutant_spot = [6000 + 6000, 30, 30, 50, 230, 127, 4000, 5000, 150]
#giga_mutant_spot = [0x21FCEC + 0x21FD17, 5500 + 5500, 30, 30, 65, 240, 255, 5000, 6000, 200]
#terra_mutant_spot = [0x367084 + 0x3670AF, 7000 + 10000, 19 + 50, 21 + 100, 50 + 100, 240, 255, 7000, 10000, 255]
#elder_lavos_spawn_spot = [0x1EF864 + 0x1EF894, 13500 + 10000, 46 + 28, 150 + 32, 100 + 50, 153, 253 + 127, 8000, 12000, 255] 

# Yakra, Golem, Golem Twins, Masa & Mune, Nizbel, Nizbel II, Slash, Flea, Dalton Plus, Heckran, Super Slash, Flea Plus, RustTyrano, Atropos XR, Yakra XIII, Golem Boss
eligible_bosses = [0x90, 0x95, 0x4F, 0x99, 0x9B, 0x9C, 0x9E, 0x9F, 0xA2, 0xA9, 0xBA, 0xBB, 0xBD, 0xC0, 0xC7, 0xF3]
boss_tiers =      [   0,    3,    4,    1,    2,    2,    2,    2,    3,    1,    2,    2,    2,    1,    2,    0]

# Zombor's legs, Zombor's head, Lavos Spawn's shell, Lavos Spawn's head, Mega Mutant's head, Mega Mutant's bottom, Giga Mutant's head, Giga Mutant's bottom, Terra Mutant's head, Terra Mutant's bottom, Elder Lavos Spawn's shell, Elder Lavos Spawn's head
eligible_dualbosses1 = [0xB3,  0xD7, 0xB8, 0x35, 0x37, 0x6F]
eligible_dualbosses2 = [0xB4,  0xD8, 0xB9, 0x36, 0x38, 0x6E]
dualboss_tiers =       [   0,    2,    4,    4,    4,    4]

def randomize_bosses(outfile,difficulty):
    # Reset array to initial position.  Program will crash if you don't do that because we remove elements from the array as bosses are selected.
    eligible_bosses = [0x90, 0x95, 0x4F, 0x99, 0x9B, 0x9C, 0x9E, 0x9F, 0xA2, 0xA9, 0xBA, 0xBB, 0xBD, 0xC0, 0xC7, 0xF3]
    boss_tiers =      [   0,    3,    4,    1,    2,    2,    2,    2,    3,    1,    2,    2,    2,    1,    2,    0]
    f = open(outfile,"r+b")
    lnI = 0
    for spot in spots:
        if spot == 0x24EC52: #Hack to get around sprite overload in Heckran's spot
            safe_bosses = list(eligible_bosses)
            safe_boss_tiers = list(boss_tiers)
            for x in [0x99,0x9F,0xBB,0xC0,0x9E,0xBA]:#Masa&Mune, Flea, Flea Plus, AtroposXR, Slash and Super Slash cause crashes here
                if x in safe_bosses:
                   safe_boss_tiers.pop(safe_bosses.index(x))
                   safe_bosses.remove(x)
            boss = rand.choice(safe_bosses)
            boss_tier = safe_boss_tiers[safe_bosses.index(boss)]            
        elif spot == 0x36F40B: #Similar hack for Yakra XIII's spot
            safe_bosses =  list(eligible_bosses)
            safe_boss_tiers = list(boss_tiers)
            if 0x99 in safe_bosses: #Masa&Mune isn't safe to load here
               safe_boss_tiers.pop(safe_bosses.index(0x99))
               safe_bosses.remove(0x99)
            boss = rand.choice(safe_bosses)
            boss_tier = safe_boss_tiers[safe_bosses.index(boss)]            
        else:
            boss = rand.choice(eligible_bosses)
            boss_tier = boss_tiers[eligible_bosses.index(boss)]
        spot_tier = spot_tiers[lnI]
        
        #f.seek(0xC4700 + boss * 23 + 0);
        #hp = int.from_bytes(f.read(2), byteorder='little', signed=False);
        f.seek(0xC4700 + boss * 23 + 2);
        level = int.from_bytes(f.read(1), byteorder='little', signed=False);
        f.seek(0xC4700 + boss * 23 + 10);
        magic = int.from_bytes(f.read(1), byteorder='little', signed=False);
        #f.seek(0xC4700 + (eligible_bosses[boss] * 23) + 13);
        #magic_defense = int.from_bytes(f.read(1), byteorder='little', signed=False);
        f.seek(0xC4700 + boss * 23 + 14);
        offense = int.from_bytes(f.read(1), byteorder='little', signed=False);
        #f.seek(0xC4700 + (eligible_bosses[boss] * 23) + 15);
        #defense = int.from_bytes(f.read(1), byteorder='little', signed=False);

        f.seek(0xC5E00 + boss * 7 + 0);
        xp = int.from_bytes(f.read(2), byteorder='little', signed=False);
        f.seek(0xC5E00 + boss * 7 + 2);
        gp = int.from_bytes(f.read(2), byteorder='little', signed=False);
        f.seek(0xC5E00 + boss * 7 + 6);
        tp = int.from_bytes(f.read(1), byteorder='little', signed=False);

        boss_power = 1
        if (spot_tier - boss_tier <= -3):
            boss_power = .7
        elif (spot_tier - boss_tier == -2):
            boss_power = .85
        elif (spot_tier - boss_tier == -1):
            boss_power = .95
        elif (spot_tier - boss_tier == 1):
            boss_power = 1.15
        elif (spot_tier - boss_tier >= 2):
            boss_power = 1.25
        #elif (spot_tier - boss_tier == 3): #Boss tier 3 is quite overpowered in practice
        #    boss_power = 1.45
        if difficulty == "hard":
           if boss == 0xBD:
              hp = rand.randrange(hard_hp[lnI] * 1.5,hard_hp[lnI] * 2 + 1,200) #Rust Tyrano gets more HP to be effective
           else:
              hp = rand.randrange(hard_hp[lnI],hard_hp[lnI] * 1.5 + 1,200)
        else:
           if boss == 0xBD:
              hp = rand.randrange(boss_hp[lnI] * 1.5,boss_hp[lnI] * 2 + 1,200) #Rust Tyrano gets more HP to be effective
           else:
              hp = rand.randrange(boss_hp[lnI],boss_hp[lnI] * 1.5 + 1,200)
        level = min(int(pow(level, boss_power)), 90)
        magic = min(int(pow(magic, boss_power)), 250)
        offense = min(int(pow(offense, boss_power)), 250)
        xp = min(int(pow(xp, boss_power)), 3000) #XP and gold scale up way too fast
        gp = min(int(pow(gp, boss_power)), 6000)
        tp = min(int(pow(tp, boss_power)), 250)

        f.seek(spot)
        f.write(st.pack("B",boss))
        # To avoid graphical glitches at the Masa & Mune spot
        if lnI == 1:
            f.seek(spot + 1)
            f.write(st.pack("B", 0x03))

        f.seek(0xC4700 + boss * 23 + 0);
        f.write(st.pack("<H",hp))
        f.seek(0xC4700 + boss * 23 + 2);
        f.write(st.pack("B",level))
        f.seek(0xC4700 + boss * 23 + 10);
        f.write(st.pack("B",magic))
        #f.seek(0xC4700 + (eligible_bosses[boss] * 23) + 13);
        #magic_defense = int.from_bytes(reader.read(1), byteorder='little', signed=False);
        f.seek(0xC4700 + boss * 23 + 14);
        f.write(st.pack("B",offense))
        #f.seek(0xC4700 + (eligible_bosses[boss] * 23) + 15);
        #defense = int.from_bytes(reader.read(1), byteorder='little', signed=False);

        f.seek(0xC5E00 + boss * 7 + 0);
        f.write(st.pack("<H",xp))
        f.seek(0xC5E00 + boss * 7 + 2);
        f.write(st.pack("<H",gp))
        f.seek(0xC5E00 + boss * 7 + 6);
        f.write(st.pack("B",tp))

        boss_tiers.pop(eligible_bosses.index(boss))
        eligible_bosses.remove(boss)
        
        lnI = lnI + 1
        
def randomize_dualbosses(outfile,difficulty):
    #Largely following similar procedure to randomize_bosses, with adjustments to account for dual boss quirks.
    eligible_dualbosses1 = [0xB3,  0xD7, 0xB8, 0x35, 0x37, 0x6F]
    eligible_dualbosses2 = [0xB4,  0xD8, 0xB9, 0x36, 0x38, 0x6E]
    dualboss_tiers =       [   0,    2,    4,    4,    4,    4]
    with open(outfile,"r+b") as f:
        lni = 0
        for spot in dualboss_spots1:
            boss = rand.choice(eligible_dualbosses1)
            boss2 = eligible_dualbosses2[eligible_dualbosses1.index(boss)]
            boss_tier = dualboss_tiers[eligible_dualbosses1.index(boss)]
            spot_tier = dualboss_spot_tiers[lni]
            f.seek(dualboss_spots1[lni])
            f.write(st.pack("B",boss))
            f.seek(dualboss_spots2[lni])
            f.write(st.pack("B",boss2))
            if difficulty == "hard":
                if boss in [0xD7,0x6F]:#Do not randomize HP of the shells
                    f.seek(0xC4700 + boss * 23 + 0);
                    hp = int.from_bytes(f.read(2), byteorder='little', signed=False);
                else:
                    hp = rand.randrange(dualboss_hard_hp1[lni],dualboss_hard_hp1[lni] * 1.5 + 1,200)
                if boss2 == 0x38:#Do not randomize the HP of Terra Mutant's bottom
                    f.seek(0xC4700 + boss2 * 23 + 0);
                    hp2 = int.from_bytes(f.read(2), byteorder='little', signed=False);
                else:
                    hp2 = rand.randrange(dualboss_hard_hp2[lni],dualboss_hard_hp2[lni] * 1.5 + 1,200)
            else:
                if boss in [0xD7,0x6F]:
                    f.seek(0xC4700 + boss * 23 + 0);
                    hp = int.from_bytes(f.read(2), byteorder='little', signed=False);
                else:
                    hp = rand.randrange(dualboss_hp1[lni],dualboss_hp1[lni] * 1.5 + 1,200)
                if boss2 == 0x38:
                    f.seek(0xC4700 + boss2 * 23 + 0);
                    hp2 = int.from_bytes(f.read(2), byteorder='little', signed=False);
                else:
                    hp2 = rand.randrange(dualboss_hp2[lni],dualboss_hp2[lni] * 1.5 + 1,200)
                    
            if boss2 == 0xB9:#Special casing Mega Mutant's bottom, it has a different slot id from the rest
               f.seek(dualboss_slot_addrs2[lni])
               f.write(st.pack("B",0x07))
            f.seek(0xC4700 + boss * 23 + 0);
            f.write(st.pack("<H",hp))
            f.seek(0xC4700 + boss2 * 23 + 0);
            f.write(st.pack("<H",hp2))
            
            dualboss_tiers.pop(eligible_dualbosses1.index(boss))
            eligible_dualbosses1.remove(boss)
            eligible_dualbosses2.remove(boss2)

            for boss in [boss,boss2]:
                f.seek(0xC4700 + boss * 23 + 2);
                level = int.from_bytes(f.read(1), byteorder='little', signed=False);
                f.seek(0xC4700 + boss * 23 + 10);
                magic = int.from_bytes(f.read(1), byteorder='little', signed=False);
                f.seek(0xC4700 + boss * 23 + 14);
                offense = int.from_bytes(f.read(1), byteorder='little', signed=False);
                f.seek(0xC5E00 + boss * 7 + 0);
                xp = int.from_bytes(f.read(2), byteorder='little', signed=False);
                f.seek(0xC5E00 + boss * 7 + 2);
                gp = int.from_bytes(f.read(2), byteorder='little', signed=False);
                f.seek(0xC5E00 + boss * 7 + 6);
                tp = int.from_bytes(f.read(1), byteorder='little', signed=False);

                boss_power = 1
                if (spot_tier - boss_tier <= -3):
                    boss_power = .7
                elif (spot_tier - boss_tier == -2):
                    boss_power = .85
                elif (spot_tier - boss_tier == -1):
                    boss_power = .95
                elif (spot_tier - boss_tier == 1):
                    boss_power = 1.15
                elif (spot_tier - boss_tier >= 2):
                    boss_power = 1.25
                level = min(int(pow(level, boss_power)), 90)
                magic = min(int(pow(magic, boss_power)), 250)
                offense = min(int(pow(offense, boss_power)), 250)
                xp = min(int(pow(xp, boss_power)), 6000) #XP and gold scale up way too fast
                gp = min(int(pow(gp, boss_power)), 6000)
                tp = min(int(pow(tp, boss_power)), 250)
                f.seek(0xC4700 + boss * 23 + 2);
                f.write(st.pack("B",level))
                f.seek(0xC4700 + boss * 23 + 10);
                f.write(st.pack("B",magic))
                f.seek(0xC4700 + boss * 23 + 14);
                f.write(st.pack("B",offense))
                f.seek(0xC5E00 + boss * 7 + 0);
                f.write(st.pack("<H",xp))
                f.seek(0xC5E00 + boss * 7 + 2);
                f.write(st.pack("<H",gp))
                f.seek(0xC5E00 + boss * 7 + 6);
                f.write(st.pack("B",tp))

            lni = lni + 1
