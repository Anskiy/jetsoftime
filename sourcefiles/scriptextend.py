# Apply Mauron's patch from Hi-Tech to read techs from banks other than CE.
# Minimally reimplement functionality from Hi-Tech to parse tech scripts.
# Provide some additional duplicate dual character tech scripts.

from byteops import get_value_from_bytes, print_bytes, to_file_ptr,\
    to_rom_ptr, get_record, to_little_endian
from techdb import TechDB

command_len = [-1]*0xDB

# return
command_len[0] = 1

# end tech
command_len[1] = 1

# Play Animation: 1 byte command, 1 byte operand (anim ind)
# 0x01 through 0x06 are all variants
command_len[0x02:0x07] = [2]*(0x07-0x01)

# Set Speed, 1 byte
command_len[0x07:0x10] = [1]*(0x10-0x07)

# move obj straight line to coords
command_len[0x10] = 3

# move line to stored coords
command_len[0x11] = 1

# line, to
command_len[0x12] = 2

# spiral cw to
command_len[0x15] = 3

# move obj to coords
command_len[0x19] = 3

# Move to stored coords
command_len[0x1A] = 1

# Moveto
command_len[0x1B] = 2

# Add link, id
command_len[0x1C] = 2

# Remove link, id
command_len[0x1D] = 2


# Super command: 1 byte command, 1 byte operand (command ind)
command_len[0x1E] = 2

# Pause: 1 byte command, 1 byte operand (duration)
command_len[0x20] = 2

# wait for counter to reach X
command_len[0x22] = 3  # layer 3 exception
command_len[0x23:0x25] = [2, 2, 2]

# cond return
command_len[0x25] = 2

# Load from from animation: command, anim#, frame#
command_len[0x26] = 3

# Unknown 1 bytes
command_len[0x27:0x29] = [1, 1]

# hide caster/target
command_len[0x29] = 1

# draw caster/target
command_len[0x2A] = 1

# Unknown 1 bytes
command_len[0x2B:0x2F] = [1]*(0x2F-0x2B)

# Set counter 00 ??
command_len[0x30] = 3

# store coords, obj
command_len[0x33] = 2

# Incr counter 00 (00 is an arg too)
command_len[0x34] = 2

# Increment counter
command_len[0x35] = 1
command_len[0x36] = 1

# increase counter, coordinate?, mag
command_len[0x3A] = 3

# load sprite at, target
command_len[0x3D] = 2
command_len[0x3E] = 2
command_len[0x3F] = 2
command_len[0x40] = 2

# copy, counter, coord
command_len[0x41] = 3

# store coords, obj, x off?, y off?
command_len[0x43] = 4

# store coords cur obj
command_len[0x44] = 1

# load sprite, at
command_len[0x45] = 2

# store target, to
command_len[0x47] = 2

# something about subtraction
command_len[0x49] = 3

# Show damage: 1 byte command
command_len[0x50] = 1
command_len[0x51] = 1
command_len[0x52] = 1
command_len[0x53] = 1
command_len[0x54] = 1
command_len[0x55] = 1

# Unknown 1 byte commands
command_len[0x2B:0x2F] = [1]*(0x2F-0x2B)

# Set palette, pal#
command_len[0x60] = 2

# Unknown command 61 (and variants)
command_len[0x61] = 4
command_len[0x62] = 4

command_len[0x65] = 1
command_len[0x66] = 1

# set pallete, color
command_len[0x69] = 2

# reset palette
command_len[0x6A] = 1

# unknown
command_len[0x6B] = 2

# Flash, counter, delay
command_len[0x6C] = 3

# unknown
command_len[0x6D] = 1

# draw all effects
command_len[0x6E] = 1

# hide all effects
command_len[0x6F] = 1

# drawing status: draw effect
command_len[0x70] = 1

# drawing status: draw effect
command_len[0x71] = 1

# Set Facing: 1 byte command, 1 byte operand (dir)
command_len[0x72] = 2

# Set sprite priority, prior
command_len[0x73] = 2
command_len[0x74] = 2

# set angle, from eff obj
command_len[0x75] = 2

# set angle, caster, target
command_len[0x76] = 3

# set angle, add
command_len[0x77] = 2

# Play sound: 1 byte command, 1 byte operand
command_len[0x78] = 2
command_len[0x79] = 2

# play sound 3 byte
command_len[0x7A] = 3
command_len[0x7B] = 3

# Flash screen, ?, ?
# variable length given by second argument
# command_len[0x80] = 3

# store target to ram
command_len[0x81] = 2
command_len[0x82] = 2
command_len[0x83] = 2
command_len[0x84] = 2

# set angle, val
command_len[0x85] = 2

# Move to variant: 1 byte command 2 bytes operands (?,?)
command_len[0x98] = 3
command_len[0x99] = 2
command_len[0x9A] = 3
command_len[0x9C] = 3
command_len[0x9D] = 2

# draw copies, len, transparency
command_len[0xA4] = 3

# remove copies
command_len[0xA5] = 1

# move forward, distance
command_len[0xA8] = 2
command_len[0xA9] = 2  # collision?

# circular sprite movment
command_len[0xC0] = 5
# Hi-Tech is giving weird results for this.  Reaidng C0 instead of C2, C3
command_len[0xC2] = 5

command_len[0xC3] = 4  # double check this?

# vertical sprite movement, mag
command_len[0xC4] = 3  # Hi-Tech error?
command_len[0xC5] = 2

# Draw status show shadow: 1 byte
command_len[0xD0] = 1

# Draw status hide shadow: 1 byte
command_len[0xD1] = 1

# Unknown 2 byte
command_len[0xD2] = 2

# Unknown 1 byte
command_len[0xD3:0xD7] = [1]*(0xD7-0xD3)

# shake sprite, unk, speed, #shakes
command_len[0xD8] = 4

# Load gfx packet: 1 byte command, 1 byte operand (packet ind)
command_len[0xD9] = 2

# Unknown
command_len[0xDA] = 1


class TechScript:

    def __init__(self):
        self.header = bytearray()
        self.pointers = []
        self.obj_scripts = []

        # TODO: Split into caster/target/effect counts
        self.num_objs = 0

    def __len__(self):
        return 4+sum([len(x) for x in self.obj_scripts])

    def from_rom(rom, start):
        ret = TechScript()

        ret.header = rom[start:start+4]

        bank = (start >> 16) << 16

        x = get_value_from_bytes(ret.header)
        ret.num_objs = bin(x).count('1')

        ptr_loc = start+4
        for i in range(ret.num_objs):
            obj_addr = get_value_from_bytes(rom[ptr_loc:ptr_loc+2]) + bank
            ret.obj_scripts.append(TechScript.get_obj_script(rom, obj_addr))
            ptr_loc += 2

        return ret

    def print_obj(obj):
        pos = 0

        while pos < len(obj):
            command = obj[pos]

            if command == 0x80:
                # 0x80 has the length encoded in the following byte.
                # Any other weird ones?
                length = (obj[pos+1] & 0x0F) + 1
            else:
                length = command_len[command]

            if length == -1:
                print('Figure out the length of', '%X' % command)
                quit()
            else:
                print('\t\'' + obj[pos:pos+length].hex().upper()+'\'', end='')
                pos += length
                if pos != len(obj):
                    print(' +')
                else:
                    print('')

        print('')

    def print_data(self):
        print('Header: ' + self.header.hex())

        for i in range(self.num_objs):
            print("Object %d" % i)
            TechScript.print_obj(self.obj_scripts[i])

    def write_to_rom(self, rom, start):
        rom[start:start+4] = self.header[:]

        pos = start+4

        obj_start = pos + 2*self.num_objs

        for i in range(self.num_objs):
            ptr_b = to_little_endian(obj_start, 2)
            rom[pos:pos+2] = ptr_b

            pos += 2

            rom[obj_start:obj_start+len(self.obj_scripts[i])] = \
                self.obj_scripts[i][:]

            obj_start += len(self.obj_scripts[i])

    def get_obj_script(rom, addr):
        # print('Reading from %6.6X' % addr)
        pos = addr
        while pos < len(rom):
            command = rom[pos]
            # print('Read %X' % command)

            if command == 0x80:
                # 0x80 has the length encoded in the following byte.
                # Any other weird ones?
                length = (rom[pos+1] & 0x0F) + 1
            else:
                length = command_len[command]

            if length == -1:
                print('Figure out the length of', '%X' % command)
                quit()
            elif command == 00:
                # print('Found 0x00, returning')
                # fspace.mark_block((addr, pos+1), False)
                break
            else:
                # print('Found %2.2X.  Length %d.' % (command, length))
                pos += length

        return rom[addr:pos+1]


# This function applies Mauron's patch to have tech scripts reside in many
# banks.  By default they are limited to bank CE.
def script_extend(rom, bank_st, scr_ptrs_new_st):

    rom[bank_st:bank_st+0x80] = bytearray([0xCE]*0x80)

    # Copy the script pointer table to the new location
    scr_ptrs_old_st = 0x0D5EF0
    scr_count = 0x80

    scr_ptrs = rom[scr_ptrs_old_st:scr_ptrs_old_st+scr_count*2]
    rom[scr_ptrs_new_st:scr_ptrs_new_st+len(scr_ptrs)] = scr_ptrs[:]

    # Apply Mauron patch to read from bank array

    scr_ptrs_new_st = to_rom_ptr(scr_ptrs_new_st)
    bank_st = to_rom_ptr(bank_st)

    scr_ptrs_hex = to_little_endian(scr_ptrs_new_st, 3).hex()
    bank_st_hex = to_little_endian(bank_st, 3).hex()

    mauron_tech_patch = \
        bytearray.fromhex('a8 0a aa bf'
                          + scr_ptrs_hex  # Script ptr table address
                          + '85 40 bb bf'
                          + bank_st_hex  # Bank table address
                          + '85 42 e2 20 7b'
                          + 'a8 aa b7 40 95 81 c8 b7 40 95 80 c8 bb c0 04 00'
                          + 'd0 f0 98 c2 21 65 40 85 40 7b a8 c2 20 06 80 90'
                          + '1f ad b3 a0 d0 16 a9 01 00 99 ac 5d 5a 98 0a 0a'
                          + 'a8 a7 40 99 bd 5d a5 42 99 bf 5d 7a e6 40 e6 40'
                          + 'c8 c0 10 00 d0 d5 7b e2'
                          + '20 ad b3 a0 f0 09 9c b3 a0 a4 82 84 80 80 c2')

    tech_patch_start = 0x014615

    rom[tech_patch_start:tech_patch_start+len(mauron_tech_patch)] = \
        mauron_tech_patch[:]


def add_dup_dual_scripts(rom, bank_st, scr_ptrs_st, scr_st):
    scr_st_rom = to_rom_ptr(scr_st)
    bank = scr_st_rom >> 16

    scr_id = 0x80
    loc = scr_st
    scr_ptr = to_little_endian(loc % 0x10000, 2)

    rom[bank_st+scr_id] = bank
    rom[scr_ptrs_st+scr_id*2:scr_ptrs_st+scr_id*2+2] = scr_ptr[:]

    bt = get_aa_beast_toss_scr(rom, bank_st, scr_ptrs_st)
    bt.write_to_rom(rom, loc)

    # prot all to spot 0x81
    loc += len(bt)
    scr_id += 1
    scr_ptr = to_little_endian(loc % 0x10000, 2)

    rom[bank_st+scr_id] = bank
    rom[scr_ptrs_st+scr_id*2:scr_ptrs_st+scr_id*2+2] = scr_ptr[:]

    pa = get_ll_prot_all_scr(rom, bank_st, scr_ptrs_st)
    pa.write_to_rom(rom, loc)

    # flexagon mist to 0x82

    loc += len(pa)
    scr_id += 1
    scr_ptr = to_little_endian(loc % 0x10000, 2)

    rom[bank_st+scr_id] = bank
    rom[scr_ptrs_st+scr_id*2:scr_ptrs_st+scr_id*2+2] = scr_ptr[:]

    fm = get_ff_hex_mist_scr(rom, bank_st, scr_ptrs_st)
    fm.write_to_rom(rom, loc)

    # robo supervolt to 0x83

    loc += len(fm)
    scr_id += 1
    scr_ptr = to_little_endian(loc % 0x10000, 2)

    rom[bank_st+scr_id] = bank
    rom[scr_ptrs_st+scr_id*2:scr_ptrs_st+scr_id*2+2] = scr_ptr[:]

    sv = get_rr_supervolt_scr(rom, bank_st, scr_ptrs_st)
    sv.write_to_rom(rom, loc)

    # marle hasteall to 0x84

    loc += len(sv)
    scr_id += 1
    scr_ptr = to_little_endian(loc % 0x10000, 2)

    rom[bank_st+scr_id] = bank
    rom[scr_ptrs_st+scr_id*2:scr_ptrs_st+scr_id*2+2] = scr_ptr[:]

    ha = get_mm_haste_all_scr(rom, bank_st, scr_ptrs_st)
    ha.write_to_rom(rom, loc)


def get_ff_hex_mist_scr(rom, bank_st, scr_ptrs_st):

    hex_cast_0 = TechScript.get_obj_script(rom, 0x0DC32C)
    TechScript.print_obj(hex_cast_0)

    hex_cast_2 = \
        bytearray.fromhex('720A' +  # facing
                          '0310' +  # play anim
                          '2402' +
                          '020B' +
                          '221B00' +  # wait for layer3 flag
                          '78 55' +
                          '03 1A' +
                          '0603' +  # play 1st frame of anim 03
                          '00')

    hex_cast_1 = \
        bytearray.fromhex('720B' +
                          '0310' +
                          '36' +     # Beginning of wat1 frog script (1)
                          #          # Trigger water bubbles around caster
                          '2402'     # Wait for frog bubbles
                          '020B' +
                          '78C3' +
                          '341B' +
                          '2078' +
                          '78C4' +
                          '341A' +
                          '2078' +
                          '36' +
                          '78C5' +
                          '3419' +
                          '221B00' +
                          '36' +
                          '78 55' +
                          '03 1A' +
                          '0603' +
                          '200F' +
                          '50' +
                          '2E' +
                          '01' +
                          '00')

    hex_tar_0 = \
        bytearray.fromhex('2401' +
                          '0605' +
                          '2402' +
                          '0603' +
                          '00')

    hex_tar_1 = \
        bytearray.fromhex('2401' +
                          '0605' +
                          '2402' +
                          '0603' +
                          '00')

    script_id = 0x26

    bank = rom[bank_st+script_id]
    ptr = rom[scr_ptrs_st+2*script_id:scr_ptrs_st+2*script_id+2]

    script_ptr = to_file_ptr((bank << 16)
                             + get_value_from_bytes(ptr))

    w2_scr = TechScript.from_rom(rom, script_ptr)

    fr_w_eff = \
        bytearray.fromhex('1B09' +
                          '7203' +
                          '7300' +
                          '61020007' +
                          '0200' +
                          '8500' +
                          '2401' +     # Wait for caster to do init anim
                          '78A1' +
                          '1E2C' +
                          '2001' +
                          '36' +       # Begin hex mist (2)
                          '00')

    fr_w_eff2 = \
        bytearray.fromhex('1B09' +
                          '7203' +
                          '7300' +
                          '0200' +
                          '8540' +
                          '2401' +
                          '1E2C' +
                          '00')

    fr_w_eff3 = \
        bytearray.fromhex('1B09' +
                          '7203' +
                          '7300' +
                          '0200' +
                          '8580' +
                          '2401' +
                          '1E2C' +
                          '00')

    fr_w_eff4 = \
        bytearray.fromhex('1B09' +
                          '7203' +
                          '7300' +
                          '0200' +
                          '85C0' +
                          '2401' +
                          '1E2C' +
                          '00')

    fr2_w_eff1 = \
        bytearray.fromhex('1B0A' +
                          '7203' +
                          '7300' +
                          '61020007' +
                          '0200' +
                          '8500' +
                          '2401' +     # Wait for caster to do init anim
                          '1E2C' +
                          '2001' +
                          '00')

    fr2_w_eff2 = fr_w_eff2[:]
    fr2_w_eff2[1] = 0xA

    fr2_w_eff3 = fr_w_eff3[:]
    fr2_w_eff3[1] = 0xA

    fr2_w_eff4 = fr_w_eff4[:]
    fr2_w_eff4[1] = 0xA

    ff_hex_scr = TechScript()
    ff_hex_scr.obj_scripts = [hex_cast_1, hex_cast_2,
                              hex_tar_0, hex_tar_1,
                              fr_w_eff, fr_w_eff2, fr_w_eff3, fr_w_eff4,
                              fr2_w_eff1, fr2_w_eff2, fr2_w_eff3, fr2_w_eff4,
                              w2_scr.obj_scripts[9]]

    ff_hex_scr.num_objs = len(ff_hex_scr.obj_scripts)

    # 2 cast, 2 target, 0 eff | 1 cast
    # 110 11000 00000000 | 1000 0000 0000 0000
    ff_hex_scr.header = bytearray.fromhex('D8FF8000')

    return ff_hex_scr


def get_ll_prot_all_scr(rom, bank_st, scr_ptrs_st):
    script_id = 0x15

    bank = rom[bank_st+script_id]
    ptr = rom[scr_ptrs_st+2*script_id:scr_ptrs_st+2*script_id+2]

    script_ptr = to_file_ptr((bank << 16)
                             + get_value_from_bytes(ptr))

    pa_scr = TechScript.from_rom(rom, script_ptr)
    print_bytes(pa_scr.header, 16)

    print_bytes(pa_scr.header, 16)

    cast_0_obj =\
        bytearray.fromhex('72 0B' +   # Face caster 1?
                          '03 10' +   # Fist pump?
                          '36' +      # Increment counter 1D
                          '24 03' +   # Wait for 1D to hit 2
                          # '0603' +
                          # '2403' +
                          '2E' +
                          '01' +
                          '00')

    cast_1_obj =\
        bytearray.fromhex('72 0A' +  # Face caster 0?
                          '03 10' +
                          # '36' +   # Remove the counter increment
                          '2403' +
                          # '0603' +
                          # '2403' +
                          # '2E' +   # Remove the end tech stuff
                          # '01' +
                          '00')

    tar_0_obj =\
        bytearray.fromhex('06 03' +
                          '24 02'    # Wait for 1D to hit 2 (from shld_eff)
                          '03 24' +
                          '06 03' +
                          '20 05' +
                          '36' +     # Increment counter 1D (to 3)
                          '00')

    # OK.  So you need an additional target object in cases where the target
    # is also a caster.  Specifics unclear.
    tar_1_obj =\
        bytearray.fromhex('24 02'    # Wait for 1D to hit 2 (from shld_eff)
                          '03 24' +
                          '06 03' +
                          # '36' +   # No increment
                          '00')

    shld_eff = \
        bytearray.fromhex('24 01' +  # Wait for 1D to hit 1
                          '1B 0C 72 03 73 03 61 02 02 06 20 0A 78' +
                          'EA 03 01' +
                          '36' +     # Increment counter 1D (to 2)
                          '00')

    shld_eff2 = \
        bytearray.fromhex('25 00' +  # Return if no target 1
                          '24 01' +  # Wait for counter 1D to hit 01
                          '1B 0D' +  # Move to target 1
                          '72 03 73 03 61 02 02 06 20 0A 78' +
                          'EA 03 01 00')

    shld_eff3 = \
        bytearray.fromhex('25 01' +  # Return if no target 2
                          '24 01' +  # Wait for counter 1D to hit 01
                          '1B 0E' +  # Move to target 2
                          '72 03 73 03 61 02 02 06 20 0A 78' +
                          'EA 03 01 00')
    pa_scr.obj_scripts = [cast_0_obj, cast_1_obj, tar_1_obj, tar_0_obj,
                          shld_eff, shld_eff2, shld_eff3,
                          pa_scr.obj_scripts[6]]

    # 2 caster, 2 target, 3 eff | 1 caster
    # 110 11000 11100000 100 00000 00000000
    pa_scr.header = bytearray.fromhex('D8E08000')
    pa_scr.num_objs = len(pa_scr.obj_scripts)

    # pa_scr.print_data()
    return pa_scr


def get_rr_supervolt_scr(rom, bank_st, scr_ptrs_st):

    script_id = 0x41

    bank = rom[bank_st+script_id]
    ptr = rom[scr_ptrs_st+2*script_id:scr_ptrs_st+2*script_id+2]

    script_ptr = to_file_ptr((bank << 16)
                             + get_value_from_bytes(ptr))
    sv_scr = TechScript.from_rom(rom, script_ptr)

    # We only really need to change crono's object (obj 0)
    # It looks a little weird, but it's OK for now.

    sv_scr.obj_scripts[0] = \
        bytearray.fromhex('7215' +
                          '300250' +
                          '300380' +
                          '0C' +
                          # '0310' +
                          # '0222' +
                          '0313' +
                          '033E' +
                          '0244' +   # Replace with robo's anims
                          '2301' +
                          'D0' +
                          'D930' +
                          '27' +
                          '98002B' +
                          '1B2B' +
                          'D1' +
                          '36' +
                          '2402' +
                          '7215' +
                          # '0310' +
                          # '0222' +
                          '0313' +
                          '033E' +
                          '0244' +   # Replace with robo's anims
                          '2302' +
                          '6900' +
                          '36' +
                          '2404' +
                          '6A' +
                          '341B' +
                          '788A' +
                          '221B00' +
                          '2D' +
                          '8032EB' +
                          '2002' +
                          '786E' +
                          '2D' +
                          '801228' +
                          '36' +
                          '2303' +
                          'DA' +
                          '28' +
                          '1E2A' +
                          '2407' +
                          '2E' +
                          '01' +
                          '00')

    return sv_scr


# Adapted from Mauron's haste all example at
# https://www.chronocompendium.com/Term/Modifying_Techs.html
def get_mm_haste_all_scr(rom, bank_st, scr_ptrs_st):

    script_id = 0x0D

    bank = rom[bank_st+script_id]
    ptr = rom[scr_ptrs_st+2*script_id:scr_ptrs_st+2*script_id+2]

    script_ptr = to_file_ptr((bank << 16)
                             + get_value_from_bytes(ptr))
    ha_scr = TechScript.from_rom(rom, script_ptr)

    cast0 =\
        bytearray.fromhex('3D03' +
                          '7215' +
                          '0310' +
                          '0236' +
                          '36' +    # Incr 1D to trigger clock1
                          '2403' +
                          '0603' +
                          '2405' +
                          '2E' +
                          '01' +
                          '00')

    # same as cast0 but with no counter/end tech stuff
    cast1 = \
        bytearray.fromhex('3D03' +
                          '7215' +
                          '0310' +
                          '0236' +
                          '2403' +
                          '0603' +
                          '2405' +
                          '00')

    tar0 = \
        bytearray.fromhex('2402' +
                          '7A8703' +
                          '2403' +
                          '341B' +
                          '0224' +
                          '2404' +
                          '0603' +
                          '22 1B 00' +
                          '2D' +
                          '80 12 29' +
                          '36' +
                          '00')

    tar1 = \
        bytearray.fromhex('2402' +
                          '7A8703' +
                          '2403' +
                          '0224' +
                          '2404' +
                          '0603' +
                          '00')

    clock = \
        bytearray.fromhex('1B09' +    # place at cast0
                          '7203' +
                          '7300' +
                          '6000' +
                          'D930' +
                          '2401' +
                          '70' +
                          '7A8600' +
                          '0200' +
                          '200A' +
                          '0A' +
                          '85C0' +
                          'A80A' +
                          '0B' +
                          'A80A' +
                          '0C' +
                          'A832' +
                          '71' +
                          '36' +     # incr 1d (to 2)
                          '2402' +
                          '7303' +
                          '3303' +
                          '301F10' +
                          '1A' +
                          '35'       # incr 1c (to 1, trigger clock2)
                          '23 03'    # wait for 1c, 3 (all clocks in position)
                          '0201' +
                          '0B' +
                          '2028' +
                          '70' +
                          '120C' +
                          '36' +
                          '2048' +
                          '71' +
                          '36' +
                          '00')

    clock2 = \
        bytearray.fromhex('1B0A' +    # Place at cast1
                          '7203' +
                          '7300' +
                          '6000' +
                          'D930' +
                          '2401' +
                          '70' +
                          '7A8600' +
                          '0200' +
                          '200A' +
                          '0A' +
                          '85C0' +
                          'A80A' +
                          '0B' +
                          'A80A' +
                          '0C' +
                          'A832' +
                          '71' +
                          # '36' +    # Going up.  Extra incr.
                          # '2403' +
                          '23 01'     # Wait for 1c to hit 1
                          '7303' +
                          '3304' +
                          '301F10' +
                          '1A' +
                          '35'        # Incr 1c
                          '23 03' +   # wait for 1c, 3
                          '0201' +
                          '0B' +
                          '2028' +
                          '70' +
                          '120D' +
                          # '36' +
                          '2048' +
                          '71' +
                          # '36' +
                          '00')

    clock3 = \
        bytearray.fromhex('23 02' +  # wait for 1c to hit 1
                          '7303' +
                          '3305' +
                          '301F10' +
                          '1A' +
                          '35' +
                          '2303' +
                          '0201' +
                          '0B' +
                          '2028' +
                          '70' +
                          '120E' +
                          '36' +
                          '2048' +
                          '71' +
                          '36' +
                          '00')

    ha_scr.obj_scripts = [cast0, cast1,
                          tar1, tar0,
                          clock, clock2, clock3,
                          ha_scr.obj_scripts[-1]]

    # Header: 2 caster, 2 targ, 3 eff
    # 110 110000 11100000
    ha_scr.header = bytearray.fromhex('D8E08000')
    ha_scr.num_objs = len(ha_scr.obj_scripts)

    return ha_scr


def get_aa_beast_toss_scr(rom, bank_st, scr_ptrs_st):
    db = TechDB.db_from_rom_internal(rom)

    # Let's get the beast toss script.  Has tech_id 0x5F
    gfx_hdr = get_record(db.gfx, 0x5F, TechDB.gfx_size)

    # script id is first byte of gfx header
    script_id = gfx_hdr[0]

    # It is almost certainly just fine to say script_id = 0x5F!

    bank = rom[bank_st+script_id]
    ptr = rom[scr_ptrs_st+2*script_id:scr_ptrs_st+2*script_id+2]

    script_ptr = to_file_ptr((bank << 16)
                             + get_value_from_bytes(ptr))
    bt_scr = TechScript.from_rom(rom, script_ptr)

    # rewrite obj 1 (old robo's object)
    bt_scr.obj_scripts[1] = \
        bytearray.fromhex('720A' +
                          '0213' +
                          # '7A5101' +  # Playing the robo banging sound
                          # '200A' +
                          # '7A5101' +
                          # '200A' +
                          # '7A5101' +
                          '7A C1 00' +  # Now playing the falcon hit sound
                          '20 14' +
                          '7A C1 00' +
                          '2402' +      # wait for counter
                          '720A' +      # sprite facing
                          # '0610' +    # plays one frame of anim for robo
                          # replace with ayla's anim code from bt
                          '06 48 20 0A 26 48 02 20 05 26 48 03 20 0A 06 48' +
                          '2403' +
                          # '0638' +
                          # '200A' +
                          # '0622' +
                          # '200A' +
                          # ayla's throw code from bt
                          '06 48 20 0A 26 48 02 20 05 26 48 03 20 0A 06 48' +
                          '2405' +
                          # '0638' +
                          # '200A' +
                          # '0622' +
                          # '200A' +
                          # ayla's throw code from bt
                          '06 48 20 0A 26 48 02 20 05 26 48 03 20 0A 06 48' +
                          '0313' +
                          '0603' +
                          '00')

    return bt_scr


if __name__ == '__main__':
    with open('ct_vanilla_exp.sfc', 'rb') as infile:
        rom = bytearray(infile.read())

    db = TechDB.get_default_db(rom)

    bank_st = 0x5F8100
    ptr_st = 0x5F8200
    script_extend(rom, bank_st, ptr_st)

    # get_ll_prot_all_scr(rom, bank_st, ptr_st)

    a2 = db.get_tech(0x49)
    print_bytes(a2['control'], 16)
    print_bytes(a2['gfx'], 16)

    ptr = rom[ptr_st+2*0x0D:ptr_st+2*0x0D+2]
    ptr = 0x0E0000 + get_value_from_bytes(ptr)

    print('%X' % ptr)
    haste_scr = TechScript.from_rom(rom, ptr)
    haste_scr.print_data()

    # with open('jets_test.sfc', 'rb') as infile:
    #    rom = bytearray(infile.read())
