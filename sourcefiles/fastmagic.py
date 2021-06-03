
from byteops import get_value_from_bytes, to_file_ptr
from enum import IntEnum


class Char(IntEnum):
    CRONO = 0
    MARLE = 1
    LUCCA = 2
    ROBO = 3
    FROG = 4
    AYLA = 5
    MAGUS = 6


# This is more in line with how the other randomizer functions work
def set_fast_magic_file(filename):
    with open(filename, 'r+b') as file:

        # This should give the start address for tech control headers no matter
        # how the rom has been messed with.
        # Default: 0x0C1BEB
        file.seek(0x01CBA1)
        control_ptr_bytes = file.read(3)
        control_ptr = get_value_from_bytes(control_ptr_bytes)
        control_ptr = to_file_ptr(control_ptr)

        print("%6.6X" % control_ptr)

        magic_learners = [Char.CRONO, Char.MARLE, Char.LUCCA, Char.FROG]

        for x in magic_learners:
            # Each control header is 11 bytes and each PC has 8 single techs
            # Then there's a blank 0th control header
            file.seek(control_ptr + (1+x*8)*11)

            for i in range(0, 8):
                # Resetting the 0x80 bit marks a tech as non-magical.
                # TP will accumulate regardless of magic learning provided the
                # next tech has the 0x80 bit unset.

                y = bytearray(file.read(1))
                y[0] &= 0x7F
                file.seek(-1, 1)
                file.write(y)
                file.seek(10, 1)  # 1 written byte + 10 after == 11 bytes

        # The remaining issue is the menu not displaying techs past a certain
        # tech level until magic is learned from Spekkio.

        # The array in rom beginning at (default) 0x3FF951 gives this threshold
        # Default Values: 03 03 03 FF 03 FF 00
        # Note: Magus is 00 but also comes with magic learned initially.

        file.seek(0x3FF894)  # location of ptr to thresh on rom
        thresh_ptr_bytes = file.read(3)
        thresh_ptr = get_value_from_bytes(thresh_ptr_bytes)
        thresh_ptr = to_file_ptr(thresh_ptr)

        for x in magic_learners:
            file.seek(thresh_ptr + x)
            # Set the threshold to 0xFF.  Could be 8 instead if you want to
            # differentiate between magic learners and others.
            file.write(b'\xFF')


def set_fast_magic(rom):

    # This should give the start address for tech control headers no matter
    # how the rom has been messed with.
    # Default: 0x0C1BEB
    control_ptr = get_value_from_bytes(rom[0x01CBA1:0x01CBA1+3])
    control_ptr = to_file_ptr(control_ptr)

    magic_learners = [Char.CRONO, Char.MARLE, Char.LUCCA, Char.FROG]

    for x in magic_learners:
        # Each control header is 11 bytes and each PC has 8 single techs
        # Then there's a blank 0th control header
        tech_ptr = control_ptr + (1+x*8)*11

        for i in range(0, 8):
            # Resetting the 0x80 bit marks a tech as non-magical for learning.
            # TP will accumulate regardless of magic learning as long as the
            # next tech has the 0x80 bit unset.
            rom[tech_ptr] &= 0x7F
            tech_ptr += 11

    # The remaining issue is the menu not displaying techs past a certain point
    # until magic is learned from Spekkio.

    # The array in rom beginning at (default) 0x3FF951 gives this threshold
    # Default Values: 03 03 03 FF 03 FF 00
    # Note: Magus is 00 but also comes with magic learned initially.

    thresh_ptr = get_value_from_bytes(rom[0x3FF894:0x3FF894+3])
    thresh_ptr = to_file_ptr(thresh_ptr)
    for x in magic_learners:
        # Set the threshold to 0xFF
        rom[thresh_ptr + x] = 0xFF


if __name__ == '__main__':
    with open("test.sfc", 'rb') as file:
        rom = bytearray(file.read())
        with open("test-out-2.sfc", 'w+b') as outfile2:
            outfile2.write(rom)

        set_fast_magic(rom)

        with open('test-out-1.sfc', 'wb') as outfile:
            outfile.write(rom)

        set_fast_magic_file("test-out-2.sfc")
