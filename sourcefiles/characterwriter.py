import random as rand
import struct as st
chrono = [0,70,8,5,8,5,8,8,15,1,0,0,20,5,0,0]
marle = [1,65,12,2,6,8,8,6,25,1,0,0,20,5,0,0]
lucca = [2,62,12,2,6,8,8,7,25,1,0,0,20,5,0,0]
robo = [3,130,6,7,10,3,7,7,10,1,0,0,20,5,0,0]
frog = [4,80,9,4,8,6,8,8,15,1,0,0,20,5,0,0]
ayla = [5,80,4,10,9,3,10,12,10,1,0,0,20,5,0,0]
magus = [6,110,14,8,7,10,12,10,30,1,0,0,20,50,0,0]
def set_stats(file_pointer,character,location):
    if location == "start" or location == "start2" or location == "cathedral":
        char_array = character[1:]
        write_stats(file_pointer,character,char_array)
        return
    elif location == "castle":
        if character == chrono:
           char_array = [122,16,10,14,6,9,9,16,5,0xF0,0,0xA0,0x32,2,0xC0]
        elif character == marle:
           char_array = [109,20,3,8,11,13,7,26,5,0xF0,0,0xA0,0x32,2,0xC0]
        elif character == lucca:
           char_array = [114,20,3,9,11,13,8,26,5,0xF0,0,0xA0,0x32,2,0xC0]
        elif character == robo:
           char_array = [170,14,13,17,5,8,8,11,5,0xF0,0,0xA0,50,2,0xC0]
        elif character == frog:
           char_array = [128,17,9,14,9,9,9,16,5,0xF0,0,0xA0,50,2,0xC0]
        elif character == ayla:
           char_array = [140,12,16,15,4,12,15,11,5,0xF0,0,0xA0,50,2,0xC0]
        elif character == magus:
           char_array = [150,22,13,11,13,15,12,32,5,0xF0,0,0xA0,50,0,0]
    elif location == "proto" or location == "burrow" or location == "dactyl":
        if character == chrono:
           char_array = [187,26,17,22,8,10,11,19,10,0x30,0x07,650,100,3,0xE0]
        elif character == marle:
           char_array = [164,30,4,12,16,20,9,29,10,0x30,0x07,650,100,3,0xE0]
        elif character == lucca:
           char_array = [179,30,4,13,17,20,9,29,10,0x30,0x07,650,100,3,0xE0]
        elif character == robo:
           char_array = [235,24,21,26,7,10,9,14,10,0x30,0x07,650,100,3,0xE0]
        elif character == frog:
           char_array = [188,27,15,22,13,10,11,19,10,0x30,0x07,650,200,3,0xE0]
        elif character == ayla:
           char_array = [215,22,23,24,5,16,19,14,10,0x30,0x07,650,100,3,0xE0]
        elif character == magus:
           char_array = [200,32,19,16,18,19,15,35,10,0x30,0x07,650,50,0,0]
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
      loadchars = [0x57,0x5C,0x62,0x6A,0x68,0x6C,0x6D]
      charnames = [0x39D7E,0x39D80,0x377090,0x5F6E5,0x372AB7,0x38931D,0x3BB90E]
      chars = [0x39D82,0x39D84,0x376FEB,0x5F5EE,0x372A6F,0x389265,0x3BB8FA]
      chars2 = [0,0,0x377088,0x5F6DD,0x372AAD,0x389313,0x3BB904]
      chars3 = [0,0,0x377099,0x5F6E8,0x372AC1,0x389328,0x3BB916]
      chars4 = [0,0,0x3770D1,0x5F6E8,0x372ADB,0x389343,0x3BB927]
      charloads = [0,0,0x3770D2,0x5F6E8,0x372ADC,0x389345,0x3BB928]
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
   f = open(outfile,"r+b")
   character_locations = {"start": "", "start2": "", "cathedral": "", "castle": "", "proto": "", "burrow": "", "dactyl": ""}
   characters = [chrono, marle, lucca, robo, frog, ayla, magus]
   for location in character_locations:
      character_locations[location] = rand.choice(characters)
      chosen_char = character_locations[location]
      set_stats(f,chosen_char,location)
      characters.remove(chosen_char)
   write_chars(f,character_locations)
   f.close
   return character_locations
if __name__ == "__main__":
    randomize_char_positions("Project.sfc")