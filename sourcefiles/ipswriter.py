import struct as st
from os import stat

def tenthousands_digit(digit):
    digit = st.unpack(">B",digit)
    digit = int(digit[0]) * 0x10000
    return digit       
def make_number(digit,digit2):
       digit2 = st.unpack(">H",digit2)
       digit2 = int(digit2[0])
       number = digit + digit2
#      print "{:X}".format(number)
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
def write_patch(patch,outfile):
     global p
     global f
     p = open(patch,"r+b")
     patch_size = stat(patch).st_size
     position = 5
     f = open(outfile,'r+b')
     while position < patch_size - 4:
       p.seek(position)
       pointer1 = p.read(1)
       pointer1 = tenthousands_digit(pointer1)
       position += 1
       pointer2 = p.read(2)
       pointer = make_number(pointer1,pointer2)
       position += 2
       length = p.read(2)
       length = get_length(length)
       position += 2
       position = write_data(length,pointer,position)
     p.close()
     f.close()
