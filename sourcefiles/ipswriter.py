import struct as st
from os import stat
from byteops import get_value_from_bytes_be


def tenthousands_digit(digit):
    digit = st.unpack(">B", digit)
    digit = int(digit[0]) * 0x10000
    return digit


def make_number(digit, digit2):
    digit2 = st.unpack(">H", digit2)
    digit2 = int(digit2[0])
    number = digit + digit2
    # print "{:X}".format(number)
    return number


def get_length(length):
    length = st.unpack(">H", length)
    length = int(length[0])
    return length


def write_data(length, pointer, position):
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
        f.write(st.pack("B", data))
        pointer += 1
        length -= 1
    return position


def get_data():
    data = p.read(1)
    data = st.unpack("B", data)
    data = int(data[0])
    return data


def write_patch(patch, outfile):
    global p
    global f
    p = open(patch, "r+b")
    patch_size = stat(patch).st_size
    position = 5
    f = open(outfile, 'r+b')
    while position < patch_size - 4:
        p.seek(position)
        pointer1 = p.read(1)
        pointer1 = tenthousands_digit(pointer1)
        position += 1
        pointer2 = p.read(2)
        pointer = make_number(pointer1, pointer2)
        position += 2
        length = p.read(2)
        length = get_length(length)
        position += 2
        position = write_data(length, pointer, position)
    p.close()
    f.close()


# Sometimes it is convenient to write a patch in memory.  We can make an
# io.BytesIO object out of the rom in memory and patch that for example.
# This function works on already created file-like objects.
# Open/close outside of this method!
def write_patch_objs(patch_obj, outfile_obj):
    p = patch_obj
    f = outfile_obj

    p.seek(0, 2)
    patch_size = p.tell()

    p.seek(5)  # ignore the "PATCH" at the start

    while p.tell() < patch_size - 5:

        # Get the location of the payload
        addr_bytes = p.read(3)
        addr = get_value_from_bytes_be(addr_bytes)

        # Get the size of the payload
        size_bytes = p.read(2)
        size = get_value_from_bytes_be(size_bytes)

        if size == 0:
            # RLE block
            rle_size_bytes = p.read(2)
            rle_size = get_value_from_bytes_be(rle_size_bytes)

            rle_byte = p.read(1)
            payload = bytearray([rle_byte[0]]*rle_size)
        else:
            # Normal block
            payload = p.read(size)
        f.seek(addr)
        f.write(payload)


# Version of the ips patcher that works with filenames.
def write_patch_alt(patch, outfile):
    with open(patch, 'r+b') as p, open(outfile, 'r+b') as f:
        write_patch_objs(p, f)


if __name__ == "__main__":
    with open("ct_vanilla.sfc", "rb") as infile:
        rom = infile.read()

        with open("test-out-1.sfc", "wb") as outfile1, \
             open("test-out-2.sfc", "wb") as outfile2:

            outfile1.write(rom)
            outfile2.write(rom)

        print("start.")
        write_patch("patch.ips", "test-out-1.sfc")
        print("done 1.")
        write_patch_alt("patch.ips", "test-out-2.sfc")
        print("done 2.")
        # Compare the output with cmp on Linux or FC on Windows.
