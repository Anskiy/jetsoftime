from shutil import copyfile
import struct as st
from os import stat
if __name__ == "__main__":
     sourcefile = raw_input("Enter ROM please.")
     outfile = sourcefile.split(".")
     outfile = outfile[0]
     outfile = str(outfile) + "123" + ".sfc"
     size = stat(sourcefile).st_size
     if size % 0x400 == 0:
        copyfile(sourcefile, outfile)
     elif size % 0x200 == 0:
        print "SNES header detected. Removing header from output file."
        f = open(sourcefile, 'r+b')
        data = f.read()
        f.close()
        data = data[0x200:]
        open(outfile, 'w+').close()
        f = open(outfile, 'r+b')
        f.write(data)
        f.close()
     p = open("patch.txt","r")
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
            print bytes[i]
            f.seek(address)
            f.write(st.pack("B",bytes[i]))
            address += 1            
            i += 1
     f.close
     p.close
# if address > 0x3FFFFF and bytes[i] == 00:
#                    while length > 0:
#                        f.write(st.pack("B",bytes[i]))
#                        address += 1
#                        length -= 1
#                    i == length
#                    continue