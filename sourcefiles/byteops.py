# Collection of routines for operating on bytearrays


def get_record(data, index, record_size):
    return data[index*record_size:(index+1)*record_size]


def set_record(data, new_record, index, record_size):
    start = index*record_size
    data[start:start+record_size] = new_record


def print_bytes(data, row_size):
    for index, val in enumerate(data):
        if index % row_size == 0:
            print("%2.2X:  " % (index//row_size), end='')
        print("%2.2X" % (val), end=' ')
        if index % row_size == row_size-1:
            print('', end='\n')
        elif index+1 == len(data):
            print('')


def to_little_endian(value, num_bytes):
    ret = bytearray()
    while(num_bytes > 0):
        x = value % 0x100
        ret.append(x)
        value = value//0x100
        num_bytes -= 1
    return ret


def get_value_from_bytes(byte_arr):
    ret = 0
    mult = 1

    for x in byte_arr:
        ret = ret+x*mult
        mult = mult*0x100

    return ret


def get_value_from_bytes_be(byte_arr):
    ret = 0
    mult = 1

    for i in range(len(byte_arr)-1, -1, -1):
        ret = ret + byte_arr[i]*mult
        mult = mult << 8

    return ret


# Pointers/addresses in the game code to the rom are not the same as file
# locations.  This helper function turns pointers in game code into file
# pointers.
def to_file_ptr(ptr):
    if 0xC00000 <= ptr <= 0xFFFFFF:
        # The [0xC00000, 0xFFFFFF] range maps to [0x000000,0x3FFFFF]
        return ptr - 0xC00000
    elif 0x400000 <= ptr <= 0x5FFFFF:
        # Extended rom area [0x400000,0x5FFFFF] maps normally
        return ptr
    else:
        print("Warning: ptr %6.6X out of rom range. Not changing." % ptr)
        return ptr


# inverse of to_file_ptr.  Turn file pointers into snes/rom pointers.
def to_rom_ptr(ptr):
    if 0x000000 <= ptr <= 0x3FFFFF:
        # The [0xC00000, 0xFFFFFF] range maps to [0x000000,0x3FFFFF]
        return ptr + 0xC00000
    elif 0x400000 <= ptr <= 0x5FFFFF:
        # Extended rom area [0x400000,0x5FFFFF] maps normally
        return ptr
    else:
        print("Warning: ptr %6.6X out of rom range. Not changing." % ptr)
        return ptr


# Function used when repointing rom data.  Update a list of pointers to point
# relative to a new start.
# ptr_list is a list of addresses (write locations) in the rom file/bytearray
def update_ptrs(rom, ptr_list, old_start, new_start):
    for ptr in ptr_list:
        addr = get_value_from_bytes(rom[ptr:ptr+3])

        # print('%X, %X' % (ptr, addr))

        # remap snes pointer to file pointer
        addr = to_file_ptr(addr)

        offset = addr-old_start
        new_ptr = to_rom_ptr(new_start+offset)

        # print('%x' % new_ptr)
        new_ptr_bytes = to_little_endian(new_ptr, 3)

        rom[ptr:ptr+3] = new_ptr_bytes[0:3]


# When you just need starts and offsets to determine the new pointer.
# Each ptr in ptr_list is known to be an offset (list offsets param)
# from a given start location (start param)
def change_ptrs(rom, ptr_list, start, offsets, num_bytes=3):

    # Maybe verify ptr_list and offsets are the same length?
    for i in range(len(ptr_list)):
        rom_loc = ptr_list[i]

        new_val = to_little_endian(to_rom_ptr(start + offsets[i]), num_bytes)
        rom[rom_loc:rom_loc+num_bytes] = new_val[:]
        # print('%x' % to_rom_ptr(start + offsets[i]))


# Reads an n-byte ptr from the rom at a given addr (file relative).  The read
# pointer is then converted to a file pointer and returned.
# Yes it feels weird having a one line function, but it gets used frequently.
def file_ptr_from_rom(rom, addr, num_bytes=3):
    return to_file_ptr(get_value_from_bytes(rom[addr:addr+num_bytes]))
