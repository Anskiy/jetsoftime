import struct as st

def scale_bosses(characters,key_locations,locked_characters,outfile):
  #Order of stats: HP, Level, Magic, Magic Defense, Offense, Defense, Experience, Gold, xTech Points
  global retinite_core
  retinite_core = [0xC4C36,0xC4C38,0xC4C40,0xC4C43,0xC4C44,0xC4C45,0xC5F96,0xC5F98,0xC5F9C]
  global retinite_legs
  retinite_legs = [0xC5743,0xC5745,0xC574D,0xC5750,0xC5751,0xC5752,0xC62F3,"",0xC62F9]
  global retinite_head
  retinite_head = [0xC575A,0xC575C,0xC5764,0xC5767,0xC5768,0xC5769,0xC62FA,"",0xC6300]
  global display
  display = ["",0xC5773,0xC577B,0xC577E,0xC577F,0xC5780]
  global motherbrain
  motherbrain = [0xC5812,0xC5814,0xC581C,0xC581F,0xC5820,0xC5821,0xC6332,0xC6334,0xC6338]
  global yakraxiii
  yakraxiii = [0xC58E1,0xC58E3,0xC58EB,0xC58EE,0xC58EF,0xC58F0,0xC6371,0xC6373,0xC6377]
  global dragon_tank
  dragon_tank = [0xC5435,0xC5437,0xC543F,0xC5442,0xC5443,0xC5444,0xC6205,0xC6207,0xC620B]
  global dragon_wheel
  dragon_wheel = [0xC544C,0xC544E,0xC5456,0xC5459,0xC545A,0xC545B]
  global dragon_head
  dragon_head = [0xC568B,0xC568D,0xC5695,0xC5698,0xC5699,0xC569A]
  global giga_gaia
  giga_gaia = [0xC59C7,0xC59C9,0xC59D1,0xC59D4,0xC59D5,0xC59D6,0xC63B7,0xC63B9,0xC63BD]
  global rusttyrano 
  rusttyrano = [0xC57FB,0xC57FD,0xC5805,0xC5808,0xC5809,0xC580A,0xC632B,0xC632D,0xC6331]
  global nizbel
  nizbel = [0xC54ED,0xC54EF,0xC54F7,0xC54FA,0xC54FB,0xC54FC,0xC623D,0xC623F,0xC6243]
  global gaia_right
  gaia_right = [0xC59DE,0xC59E0,0xC59E8,0xC59EB,0xC59EC,0xC59ED]
  global gaia_left
  gaia_left = [0xC59F5,0xC59F7,0xC59FF,0xC5A02,0xC5A03,0xC5A04]
  global bit
  bit = [0xC5999,0xC599B,0xC59A3,0xC59A6,0xC59A7,0xC59A8]
  global guardian
  guardian = [0xC5A0C,0xC5A0E,0xC5A16,0xC5A19,0xC5A1A,0xC5A1B,0xC63CC,0xC63CE,0xC63D2]
  global sonofsun
  sonofsun = ["",0xC5D1C,0xC5D24,"","","",0xC64BA,0xC64BC,0xC64C0]
  global sos_flame
  sos_flame = ["",0xC5D33,0xC5D3B,"","",""]
  global rseries
  rseries = [0xC5D48,0xC5D4A,0xC5D52,0xC5D55,0xC5D56,0xC5D57,0xC64C8,0xC64CA,0xC64CE]
  global dtankpower
  dtankpower = 0
  global nizbelpower
  nizbelpower = 0
  global desertpower
  desertpower = 0
  global rustpower  
  rustpower = 0
  global guardianpower
  guardianpower = 0
  global sunpower
  sunpower = 0 
  global motherpower
  motherpower = 0
  global gigapower
  gigapower = 0
  global yakraxiiipower
  yakraxiiipower = 0
  global rseriespower
  rseriespower = 0
  important_keys = ["knife","clone","trigger"]
  set_power(key_locations,important_keys)
  if locked_characters == "Y":
     if (characters ["proto"] == "Robo" or characters ["proto"] == "Ayla"):
        rseriespower = 1
     if (characters ["proto"] == "Chrono" or characters ["proto"] == "Magus"):
        rseriespower = 2
  f = open(outfile,"r+b")
  scale_stats(rustpower,rusttyrano,f)
  scale_stats(dtankpower,dragon_tank,f)
  scale_stats(dtankpower,dragon_wheel,f)
  scale_stats(dtankpower,dragon_head,f)
  scale_stats(sunpower,sonofsun,f)
  scale_stats(sunpower,sos_flame,f)
  scale_stats(nizbelpower,nizbel,f)
  scale_stats(desertpower,retinite_core,f)
  scale_stats(desertpower,retinite_head,f)
  scale_stats(desertpower,retinite_legs,f)
  scale_stats(yakraxiiipower,yakraxiii,f)
  scale_stats(guardianpower,guardian,f)
  scale_stats(guardianpower,bit,f)
  scale_stats(motherpower,motherbrain,f)
  scale_stats(motherpower,display,f)
  scale_stats(rseriespower,rseries,f)
  scale_stats(gigapower,giga_gaia,f)
  scale_stats(gigapower,gaia_left,f)
  scale_stats(gigapower,gaia_right,f)
  f.close()
def set_power(locations,important_keys,rank = 3):
    futurelocs = ["arris","geno","sun"]
    importantlocs = []
    global dtankpower
    global guardianpower
    global motherpower
    global sunpower
    global nizbelpower
    global yakraxiiipower
    global rustpower
    global gigapower
    global desertpower
    for locs in locations:
        if locations [locs] in important_keys:
           importantlocs.append(locs)
    important_keys.clear()
    for locs in importantlocs:
        if locs == "reptite":
           important_keys.append("gate")
           nizbelpower = rank
        if locs in futurelocs:
           important_keys.append("pendant")
           dtankpower = rank - 1
           if locs == "arris":
              guardianpower = dtankpower + 1
           if locs == "sun":
              sunpower = dtankpower + 1
           if locs == "geno":
              motherpower = dtankpower + 1
        if locs == "melchior":
           yakraxiiipower = rank
           important_keys.append("moon")
           if "gate" not in important_keys:
              important_keys.append("gate")
           if "pendant" not in important_keys:
              important_keys.append("pendant")
           dtankpower = yakraxiiipower - 1
        if locs == "trial":
             important_keys.append("prism")
             yakraxiiipower = rank
        if locs == "claw":
           important_keys.append("pop")
           rustpower = rank
        if locs == "desert":
           desertpower = rank
        if locs == "woe":
           gigapower = rank
        if locs == "burrow":
           important_keys.append("medal")
    if rank > 2:
       important_keys.append("blade")
       important_keys.append("hilt")
       important_keys.append("stone")
    rank = rank - 1
    if rank > 0:
        set_power(locations,important_keys,rank)
def scale_stats(bosspower,boss,pointer):
    if bosspower == 0: return
    boss_stats = []
    i = 0
    halfword_stats = [0,6,7]
    if boss == rusttyrano:
       if bosspower < 2:
          boss_stats = [6000,16,16,50,160,127,3000,4000,50]
       elif bosspower < 3:
          boss_stats = [7000,20,20,50,170,127,4500,6500,75]
       else: boss_stats = [8000,30,30,50,180,127,6000,8000,100]
    if boss == dragon_tank:
       if bosspower < 2:
          boss_stats = [1100,15,15,60,50,160,2300,3400,30]
       else: boss_stats = [1300,30,30,60,100,160,3400,5000,50]
    if boss == dragon_wheel:
       if bosspower < 2:
          boss_stats = [1000,25,25,60,42,160]
       else: boss_stats = [1100,25,25,60,85,160]
    if boss == dragon_head:
       if bosspower < 2:
            boss_stats = [1400,20,20,60,50,160]
       else: boss_stats = [1600,30,30,60,50,160]
    if boss == sonofsun:
       if bosspower < 2:
            boss_stats = ["",20,20,"","","",3100,4200,35]
       elif bosspower < 3:
            boss_stats = ["",30,20,"","","",4300,6200,50]
       else: boss_stats = ["",30,30,"","","",5200,8000,70]
    if boss == sos_flame:
       if bosspower < 2:
            boss_stats = ["",20,20,"","",""]
       elif bosspower < 3:
            boss_stats = ["",30,20,"","",""]
       else: boss_stats = ["",30,30,"","",""]
    if boss == nizbel:
       if bosspower < 2:
          boss_stats = [6000,20,20,60,155,253,4500,5100,55]
       elif bosspower < 3:
          boss_stats = [7000,30,30,60,175,253,6000,7200,70]
       else: boss_stats = [8000,40,40,65,190,253,8000,10000,95]
    if boss == retinite_head or boss == retinite_legs:
       if bosspower < 2:
          boss_stats = [2000,15,15,60,130,153,1600,0,18]
       elif bosspower < 3:
          boss_stats = [2200,20,20,65,160,165,2000,0,25]
       else: boss_stats = [2400,25,25,70,190,178,2200,0,30]
    if boss == retinite_core:
       if bosspower < 2:
          boss_stats = [700,15,19,60,50,153,3200,2600,36]
       elif bosspower < 3:
          boss_stats = [800,15,19,65,50,165,4000,3800,50]
       else: boss_stats = [900,15,19,70,50,178,4400,4500,60]
    if boss == yakraxiii:
       if bosspower < 2:
          boss_stats = [5200,17,18,50,95,127,3300,4000,50]
       elif bosspower < 3:
            boss_stats = [5800,17,18,50,120,127,4600,7000,70]
       else: boss_stats = [6300,17,18,50,150,127,5500,10000,90]
    if boss == guardian:
       if bosspower < 2:
          boss_stats = [3500,15,15,50,16,127,3000,4000,32]
       elif bosspower < 3:
            boss_stats = [4000,20,20,50,16,127,4100,6000,46]
       else: boss_stats = [4300,30,30,50,16,127,5200,8000,60]
    if boss == bit:
       if bosspower < 2:
          boss_stats = [500,12,12,50,32,127]
       elif bosspower < 3:
            boss_stats = [500,15,15,50,50,127]
       else: boss_stats = [500,17,17,50,74,127]
    if boss == motherbrain:
       if bosspower < 2:
          boss_stats = [3500,20,20,50,100,127,4000,6200,50]
       elif bosspower < 3:
             boss_stats = [4000,30,30,50,100,127,5500,7300,71]
       else: boss_stats = [4500,40,40,50,100,127,6400,8100,93]
    if boss == display:
       if bosspower < 2:
          boss_stats = [1,15,15,50,144,127]
       elif bosspower < 3:
          boss_stats = [1,15,20,50,144,127]
       else: boss_stats = [1,15,25,50,144,127]
    if boss == rseries:
       if bosspower < 2:
          boss_stats = [1200,15,15,50,52,127,600,400,10]
       else: boss_stats = [1400,20,20,50,75,127,800,600,15]
    if boss == giga_gaia:
       if bosspower < 2:
          boss_stats = [8000,32,15,50,50,127,5000,7000,110]
       elif bosspower < 3:
             boss_stats = [9000,32,15,50,50,127,6200,8200,130]
       else: boss_stats = [10000,32,15,50,50,127,7400,9200,150]
    if boss == gaia_left:
       if bosspower < 2:
          boss_stats = [2500,20,30,61,40,127]
       elif bosspower < 3:
            boss_stats = [3000,30,30,61,40,127]
       else: boss_stats = [3500,40,30,61,40,127]
    if boss == gaia_right:
       if bosspower < 2:
          boss_stats = [2500,20,30,50,60,158]
       elif bosspower < 3:
            boss_stats = [3000,30,30,50,60,158]
       else: boss_stats = [3500,40,30,50,60,158]
    while i < len(boss_stats):
          if boss [i] == "":
             i += 1
             continue
          pointer.seek(boss [i])
          if i in halfword_stats:
             pointer.write(st.pack("H",boss_stats[i]))
          else: 
             pointer.write(st.pack("B",boss_stats[i]))
          i += 1