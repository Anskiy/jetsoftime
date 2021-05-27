from shutil import copyfile
import struct as st
from os import stat
def patch_file(patch,outfile):
     p = open(patch,"r")
     f = open(outfile,'r+b')
     for line in p:
        writelist = []
        line = line.split(":")
        address = int(line[0],0x10)
        length = int(line[1],0x10)
        bytes = line[2]
        bytes = bytes.split(" ")
        i = 0
        while i < length:
            bytes[i] = int(bytes[i],0x10)
            f.seek(address)
            f.write(st.pack("B",bytes[i]))
            address += 1            
            i += 1
     f.close()
     p.close()
if __name__ == "__main__":
    file = input("Enter patch name.")
    patch_file(file,"Projectfile.smc")
