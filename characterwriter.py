import random as rand
import struct as st
chrono = [0,70,8,5,8,5,8,8,2,1,0,0,20,2,0,0]
marle = [1,65,12,2,6,8,8,6,8,1,0,0,20,10,0,0]
lucca = [2,62,12,2,6,8,8,7,7,1,0,0,20,10,0,0]
robo = [3,130,6,7,10,3,7,7,1,1,0,0,20,5,0,0]
frog = [4,80,9,4,8,6,8,8,3,1,0,0,20,10,0,0]
ayla = [5,80,4,10,9,3,10,12,1,1,0,0,20,10,0,0]
magus = [6,110,14,8,7,10,12,10,9,1,0,0,20,100,0,0]
def set_stats(file_pointer,character,location):
    if location == "start" or location == "start2":
        char_array = character[1:]
        write_stats(file_pointer,character,char_array)
        return
    elif location == "cathedral":
        if character == chrono:
           char_array = [122,16,10,14,6,9,9,8,5,0xF0,0,0xA0,0,2,0xC0]
        elif character == marle:
           char_array = [109,20,3,8,11,9,7,14,5,0xF0,0,0xA0,0,2,0xC0]
        elif character == lucca:
           char_array = [114,20,3,9,11,9,8,13,5,0xF0,0,0xA0,0,2,0xC0]
        elif character == robo:
           char_array = [170,14,13,17,5,8,8,6,5,0xF0,0,0xA0,50,2,0xC0]
        elif character == frog:
           char_array = [128,17,9,14,8,9,9,9,5,0xF0,0,0xA0,0,2,0xC0]
        elif character == ayla:
           char_array = [140,12,16,15,4,12,15,7,5,0xF0,0,0xA0,100,2,0xC0]
        elif character == magus:
           char_array = [150,22,12,11,14,15,12,16,5,0xF0,0,0xA0,100,0,0]
    elif location == "castle":
        if character == chrono:
           char_array = [187,26,17,22,8,10,11,16,10,0x30,0x07,650,200,3,0xE0]
        elif character == marle:
           char_array = [164,30,4,11,15,10,8,21,10,0x30,0x07,650,150,3,0xE0]
        elif character == lucca:
           char_array = [179,30,4,13,17,11,9,22,10,0x30,0x07,650,160,3,0xE0]
        elif character == robo:
           char_array = [235,24,21,26,7,9,8,12,10,0x30,0x07,650,150,3,0xE0]
        elif character == frog:
           char_array = [188,27,15,22,10,10,11,17,10,0x30,0x07,650,160,3,0xE0]
        elif character == ayla:
           char_array = [215,22,23,24,5,16,19,14,10,0x30,0x07,650,200,3,0xE0]
        elif character == magus:
           char_array = [200,32,18,16,20,19,15,24,10,0x30,0x07,650,100,0,0]
    elif location == "proto":
        if character == chrono:
           char_array = [262,36,24,31,10,12,13,24,15,0xBE,0x19,1450,500,4,0xF0]
        elif character == marle:
           char_array = [228,40,6,15,20,12,11,32,15,0xBE,0x19,1450,250,4,0xF0]
        elif character == lucca:
           char_array = [250,40,5,17,22,13,11,30,15,0xBE,0x19,1450,250,4,0xF0]
        elif character == robo:
           char_array = [310,34,29,33,10,12,10,17,15,0xBE,0x19,1450,400,4,0xF0]
        elif character == frog:
           char_array = [258,37,22,30,13,12,13,25,15,0xBE,0x19,1450,250,4,0xF0]
        elif character == ayla:
           char_array = [290,32,31,33,7,20,23,22,15,0xBE,0x19,1450,400,4,0xF0]
        elif character == magus:
           char_array = [250,42,24,21,25,22,19,33,15,0xBE,0x19,1450,140,2,0xC0]
    elif location == "burrow":
        if character == chrono:
           char_array = [337,46,31,39,12,13,15,32,20,0xE0,0x3D,2500,400,5,0xF8]
        elif character == marle:
           char_array = [298,50,7,19,25,13,12,40,20,0xE0,0x3D,2500,400,5,0xF8]
        elif character == lucca:
           char_array = [325,50,7,21,27,15,13,38,20,0xE0,0x3D,2500,400,5,0xF8]
        elif character == robo:
           char_array = [405,44,37,43,12,14,12,25,20,0xE0,0x3D,2500,600,5,0xF8]
        elif character == frog:
           char_array = [328,47,28,38,15,14,15,33,20,0xE0,0x3D,2500,400,5,0xF8]
        elif character == ayla:
           char_array = [367,42,38,41,8,23,27,29,20,0xE0,0x3D,2500,600,5,0xF8]
        elif character == magus:
           char_array = [300,52,30,26,31,26,22,42,20,0xE0,0x3D,2500,400,3,0xE0]
    elif location == "dactyl":
        if character == chrono:
           char_array = [436,56,38,47,15,15,17,40,25,0x78,0x78,3800,800,6,0xFC]
        elif character == marle:
           char_array = [376,60,9,22,29,15,14,49,25,0x78,0x78,3800,600,6,0xFC]
        elif character == lucca:
           char_array = [401,60,8,25,32,18,14,47,25,0x78,0x78,3800,600,6,0xFC]
        elif character == robo:
           char_array = [505,54,45,52,15,17,14,32,25,0x78,0x78,3800,800,6,0xFC]
        elif character == frog:
           char_array = [418,57,35,46,18,15,18,42,25,0x78,0x78,3800,600,6,0xFC]
        elif character == ayla:
           char_array = [452,52,46,50,10,27,31,37,25,0x78,0x78,3800,800,6,0xFC]
        elif character == magus:
           char_array = [350,62,36,31,37,30,25,51,25,0x78,0x78,3800,400,4,0xF0]
    write_stats(file_pointer,character,char_array)
def write_stats(file_pointer,character,stats):
        start_pointer = 0xC0000 + character[0] * 0x50
        techlist_pointer = 0xC0237 + character[0]
        technumber_pointer = 0xC0230 + character[0]
        file_pointer.seek(start_pointer + 0x3)
        file_pointer.write(st.pack("H",stats[0]))
        file_pointer.seek(start_pointer + 0x5)
        file_pointer.write(st.pack("H",stats[0]))
        file_pointer.seek(start_pointer + 0x7)
        file_pointer.write(st.pack("H",stats[1]))
        file_pointer.seek(start_pointer + 0x9)
        file_pointer.write(st.pack("H",stats[1]))
        file_pointer.seek(start_pointer + 0xB)
        file_pointer.write(st.pack("B",stats[2]))
        file_pointer.seek(start_pointer + 0xC)
        file_pointer.write(st.pack("B",stats[3]))
        file_pointer.seek(start_pointer + 0xE)
        file_pointer.write(st.pack("B",stats[4]))
        file_pointer.seek(start_pointer + 0xF)
        file_pointer.write(st.pack("B",stats[5]))
        file_pointer.seek(start_pointer + 0x10)
        file_pointer.write(st.pack("B",stats[6]))
        file_pointer.seek(start_pointer + 0x11)
        file_pointer.write(st.pack("B",stats[7]))
        file_pointer.seek(start_pointer + 0x12)
        file_pointer.write(st.pack("B",stats[8]))
        file_pointer.seek(start_pointer + 0x13)
        file_pointer.write(st.pack("B",stats[9]))
        file_pointer.seek(start_pointer + 0x14)
        file_pointer.write(st.pack("H",stats[10]))
        file_pointer.seek(start_pointer + 0x2B)
        file_pointer.write(st.pack("H",stats[11]))
        file_pointer.seek(start_pointer + 0x2D)
        file_pointer.write(st.pack("H",stats[12]))
        file_pointer.seek(technumber_pointer)
        file_pointer.write(st.pack("B",stats[13]))
        file_pointer.seek(techlist_pointer)
        file_pointer.write(st.pack("B",stats[14]))
def write_chars(file_pointer,char_dict):
      char_keys = ["start","start2","cathedral","castle","proto","burrow","dactyl"]
      loadchars = [0x57,0x5C,0x62,0x68,0x6A,0x6C,0x6D]
      charnames = [0x39D7E,0x39D80,0x377090,0x5F6E5,0x372AB9,0x1BDB83,0x3BB90E]
      chars = [0x39D82,0x39D84,0x376FEB,0x5F5EE,0x372A6F,0x1BDACB,0x3BB8FA]
      chars2 = [0,0,0x377088,0x5F6DD,0x372AAF,0x1BDB79,0x3BB904]
      chars3 = [0,0,0x377099,0x5F6E8,0x372AC3,0x1BDB8E,0x3BB916]
      chars4 = [0,0,0x3770D1,0x5F6E8,0x372ADD,0x1BDBA9,0x3BB927]
      charloads = [0,0,0x3770D2,0x5F6E8,0x372ADE,0x1BDBAB,0x3BB928]
      i = 0
      while i < 7:
            char = char_dict[char_keys[i]][0]
            file_pointer.seek(charnames[i])
            file_pointer.write(st.pack("B",char | 0xC0))
            file_pointer.seek(chars[i])
            file_pointer.write(st.pack("B",char))
            if i < 2:
                i += 1
                continue
            file_pointer.seek(chars2[i])
            file_pointer.write(st.pack("B",char))
            file_pointer.seek(chars3[i])
            file_pointer.write(st.pack("B",char))
            file_pointer.seek(chars4[i])
            file_pointer.write(st.pack("B",char))
            if chars4[i] != charloads[i]:
                file_pointer.seek(charloads[i])
                file_pointer.write(st.pack("B",loadchars[char]))
            i += 1
def randomize_char_positions(outfile):
   FrogPlaced = False
   f = open(outfile,"r+b")
   while not FrogPlaced:
     character_locations = {"start": "", "start2": "", "cathedral": "", "castle": "", "proto": "", "burrow": "", "dactyl": ""}
     characters = [chrono, marle, lucca, robo, frog, ayla, magus]
     for location in character_locations:
        if location == "dactyl" and not FrogPlaced:
              if characters == [frog]:
                   continue
              characters.remove(frog)
        character_locations[location] = rand.choice(characters)
        chosen_char = character_locations[location]
        if chosen_char == frog:
           FrogPlaced = True
        set_stats(f,chosen_char,location)
        characters.remove(chosen_char)
        if location == "dactyl" and not FrogPlaced:
              characters.append(frog)
   write_chars(f,character_locations)
   f.close
   return character_locations
if __name__ == "__main__":
    randomize_char_positions("Projectfile.smc")