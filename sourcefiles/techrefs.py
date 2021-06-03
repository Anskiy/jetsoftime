# Some scripts for dealing with expanding/moving tech data
from byteops import to_little_endian, to_rom_ptr, change_ptrs


def fix_control_refs(rom, control_new_start):

    # Experimentally determined location of pointers to control headers
    control_refs = [0x01CB56, 0x01CB6F, 0x01CB88, 0x01CBA1,
                    0x01D547, 0x01D594, 0x01D5A4, 0x01D5CE,
                    0x01D620, 0x01D695, 0x01D6A5, 0x01D733,
                    0x01F483, 0x01F5B8]

    control_offs = [5, 6, 7, 0,
                    0, 1, 1, 5,
                    8, 2, 3, 1,
                    0, 0]
    """
    print('control offsets:')
    for ptr in control_refs:
        x = rom[ptr:ptr+3]
        v = get_value_from_bytes(x)
        v = to_file_ptr(v)
        offset = v - control_old_start
        print(offset)
    print('done.')
    """

    # update_ptrs(rom, control_refs, control_old_start, control_new_start)
    change_ptrs(rom, control_refs, control_new_start, control_offs)


def fix_effect_refs(rom, effect_new_start):

    # Experimentally determined location of pointers to effect headers
    effect_refs = [0x01BF96, 0x01D5F0, 0x02B440, 0x02B449]

    effect_offs = [0, 0, 2, 1]

    """
    print('effect offsets:')
    for ptr in effect_refs:
        x = rom[ptr:ptr+3]
        v = get_value_from_bytes(x)
        v = to_file_ptr(v)
        offset = v - effect_old_start
        print(offset)
    print('done.')
    """

    change_ptrs(rom, effect_refs, effect_new_start, effect_offs)
    # update_ptrs(rom, effect_refs, effect_old_start, effect_new_start)


def fix_gfx_refs(rom, gfx_new_start):

    # Experimentally determined location of pointers to gfx headers
    gfx_refs = [0x0145BC, 0x0145C3, 0x145CA, 0x145D1, 0x145D8,
                0x145DF, 0x145E6]

    gfx_offs = [0, 1, 2, 3, 4, 5, 6]

    # update_ptrs(rom, gfx_refs, gfx_old_start, gfx_new_start)
    change_ptrs(rom, gfx_refs, gfx_new_start, gfx_offs)


def fix_target_refs(rom, target_new_start):

    # Experimentally determined location of pointers to targetting data
    target_refs = [0x1C254, 0x1C25A, 0x1C9BD, 0x1C9CA,
                   0x1CA9F, 0x1CAAC, 0x1CD4A, 0x1CD57, 0x2B458]

    target_offs = [1, 0, 1, 0,
                   1, 0, 1, 0, 0]

    # update_ptrs(rom, target_refs, target_old_start, target_new_start)
    change_ptrs(rom, target_refs, target_new_start, target_offs)


def fix_bat_grp_refs(rom, bat_grp_new_start):

    # Experimentally determined location of pointers to battle groups
    bat_grp_refs = [0x1CBAE, 0x1CBB5, 0x1CBBC, 0x1D55F,
                    0x1D566, 0x1D56D, 0x3FF8D7, 0x3FF8E2]

    # The big offsets are for times when single tech groups are skipped over
    # Used in X-Menu I believe.
    bat_grp_offs = [0, 1, 2, 0, 1, 2, 20, 21]

    """
    print('bat grp offsets:')
    for ptr in bat_grp_refs:
        x = rom[ptr:ptr+3]
        v = get_value_from_bytes(x)
        v = to_file_ptr(v)
        offset = v - 0x0C249F
        print(offset)
    print('done.')

    input()
    """

    change_ptrs(rom, bat_grp_refs, bat_grp_new_start, bat_grp_offs)
    # update_ptrs(rom, bat_grp_refs, bat_grp_old_start, bat_grp_new_start)


def fix_menu_grp_refs(rom, menu_grp_new_start):
    # Experimentally determined location of pointers to menu groups

    # Menu group references
    # $C2/BCE8 BF 63 29 CC LDA $CC2963,x  --> 0x02BCE9
    # $FF/F865 BF 63 29 CC LDA $CC2963,x  --> 0x3FF866
    # $C2/BBF3 BF 63 29 CC LDA $CC2963,x  --> 0x02BBF4

    # These two need more care since the relative location of trip/rock
    # will vary depending on the reassignment
    # $FF/F97A BF 83 29 CC LDA $CC2983,x  --> 0x3FF97B  (Rock Techs)
    # $FF/F91A BF 79 29 CC LDA $CC2979,x  --> 0x3FF91B  (Triple Techs)
    menu_grp_refs = [0x02BCE9, 0x3FF866, 0x02BBF4]  # + [0x3FF97B, 0x3FF91B]

    menu_grp_offs = [0, 0, 0]

    # update_ptrs(rom, menu_grp_refs, menu_grp_old_start, menu_grp_new_start)
    change_ptrs(rom, menu_grp_refs, menu_grp_new_start, menu_grp_offs)


def fix_name_refs(rom, names_new_start):

    # We'll need to place these bytes in a few places
    rom_new_start = to_rom_ptr(names_new_start)
    names_new_start_bytes = to_little_endian(rom_new_start, 3)

    # 1) Change name pointers in battle
    # $C1/0B69 69 C4 15    ADC #$15C4
    #   This now needs to add the last two bytes of the names_new_start
    rom[0x010B6A:0x010B6A+2] = names_new_start_bytes[0:2]

    # $C1/0B73 54 7E CC    MVN CC 7E
    #  The bank CC needs to be replaced by the new bank
    rom[0x010B75] = names_new_start_bytes[2]

    # 2) Change name pointers in X-button menu

    # $C2/BDD9 A9 C4 15    LDA #$15C4
    #  As before, we have to change this constant to the last two bytes of the
    #  new start.
    rom[0x02BDDA:0x02BDDA+2] = names_new_start_bytes[0:2]

    # $C2/BDE3 A9 0B CC    LDA #$CC0B
    # The 0B part should be left alone, but the CC part eventually gets written
    #  as the new data bank register.  There's a XBA PHA PLB block later for
    #  this.
    rom[0x02BDE5] = names_new_start_bytes[2]

    # 3) Change pointers when a tech is learned

    # $C2/5AA8 69 C4 15    ADC #$15C4
    #  This is like the previous instances.
    rom[0x025AA9:0x025AA9+2] = names_new_start_bytes[0:2]

    # $C2/5AAB 8D 37 02    STA $0237  [$7E:0237]
    # $C2/5AB0 A9 CC       LDA #$CC
    # $C2/5AB2 8D 39 02    STA $0239  [$7E:0239]
    # This is writing the address (little endian) 0xCC15C4 into memory.
    # We just need to change the #$CC to the new bank
    rom[0x025AB1] = names_new_start_bytes[2]


def fix_desc_ptr_refs(rom, desc_ptr_new_start):
    # Tech descriptions are similar to tech names, but they are a bit different
    # because the descriptions are a variable size.  So there is a block of
    # pointers that look into another block of descriptions.  Pointers are only
    # two bytes.  These are looked at in two places in the game
    #   1) the X-menu and
    #   2) the battle menu

    # 1) X-menu
    #   $C2/BE63 A2 09 3A    LDX #$3A09
    #   $C2/BE66 8E 0D 02    STX $020D  [$7E:020D]
    #   $C2/BE69 A9 CC       LDA #$CC
    #   $C2/BE6B 8D 0F 02    STA $020F  [$7E:020F]
    # This loads the address 0xCC3A09, which is the start of the pointer block
    # into $020D - $020F (remember little endian).  Then later we have
    #   $C2/57E7 A5 0C       LDA $0C    [$00:020C]   # Tech_id in $0C
    #   $C2/57E9 29 FF 00    AND #$00FF
    #   $C2/57EC 0A          ASL A                   # *2 b/c 2 bytes
    #   $C2/57ED A8          TAY
    #   $C2/57EE B7 0D       LDA [$0D],y
    # So 0xCC3A09+2*tech_id is the pointer for the tech's description.
    # Important Note: This second block is a general purpose block.  It is used
    #   all the time for reading 2 byte pointers.  The index is put in $0C
    #   and the next 3 bytes are the address.
    # Another Note: Whenever the game does this pointer -> data for messages
    #   it seems to want the bank of the message to match the bank of the
    #   pointer.  Usually it just reads the bank from the pointer and writes
    #   it as the bank for the address.

    desc_ptr_new_start_bytes = \
        to_little_endian(to_rom_ptr(desc_ptr_new_start), 3)

    #   $C2/BE63 A2 09 3A    LDX #$3A09
    rom[0x02BE64:0x02BE64+2] = desc_ptr_new_start_bytes[0:2]

    #   $C2/BE69 A9 CC       LDA #$CC
    rom[0x02BE6A] = desc_ptr_new_start_bytes[2]

    # 2) Battle Menu
    # The code to load the pointer is below:
    #   $CD/0322 A2 09 3A    LDX #$3A09
    #   $CD/0325 8E 0D 02    STX $020D  [$7E:020D]
    #   $CD/0328 48          PHA
    #   $CD/0329 A9 CC       LDA #$CC
    #   $CD/032B 8D 0F 02    STA $020F  [$7E:020F]
    # The part that loads the description is the same block as before.
    rom[0x0D0323:0x0D0323+2] = desc_ptr_new_start_bytes[0:2]
    rom[0x0D032A] = desc_ptr_new_start_bytes[2]


def fix_desc_refs(rom, desc_new_start):
    # This is handled by the techdb since the techdb needs to keep a correct
    # list of desc_ptrs
    pass


def fix_techs_learned(rom, techs_learned_old_start, techs_learned_new_start):
    # This should probably be directly in the techdb routine?

    # At 0x0C0230 there is a block of data that represents each
    # character's tech progression as well as all double/triple techs learned.
    #   First 7 bytes: number representing each character's tech progression
    #   Next bytes: bitmask represnting techs learned in each performance
    #     group (menu group?). Nth high order bit on means the nth tech in that
    #     group is learned.
    # The problem is that this block is copied into memory as well.  The
    # instruction that moves it is:
    #  $C2/958C 54 7E CC    MVN CC 7E               A:027F X:0000 Y:2600
    # This copies 0x027F bytes starting at CC0000 (really 0C0000) to memory
    # beginning at 0x7E2600.

    # The fast solution is to copy the rom region into a new bank (say 4F) and
    # then change the MVN command to use that bank.

    # This is the size of the MVN instruction that sends the techs_learned
    # data into memory.  It also sends all of the PC initial data.
    mvn_size = 0x27F

    # rom_old_start = to_rom_ptr(techs_learned_old_start)
    rom_new_start = to_rom_ptr(techs_learned_new_start)

    # old_start_bytes = to_little_endian(rom_old_start, 3)
    new_start_bytes = to_little_endian(rom_new_start, 3)

    old_mvn_st = (techs_learned_old_start >> 16) << 16
    new_mvn_st = (techs_learned_new_start >> 16) << 16

    rom[new_mvn_st:new_mvn_st+mvn_size] \
        = rom[old_mvn_st:old_mvn_st+mvn_size]

    # Change $C2/958C 54 7E CC    MVN CC 7E
    rom[0x02958E] = new_start_bytes[2]

    # the tech_db needs to be sure to write this out *before* updating the
    # actual techs_learned bit.


def fix_lrn_req_refs(rom, lrn_req_new_start):
    # Tech Learning Requirements
    # Block beginning at 0x0C27F7 has triples XX YY ZZ with tech levels.  For
    # example the first triple (aside from a blank 00 00 00) is 01 01 FF which
    # says Aura Whirl needs Crono's 1st tech and Marle's 1st tech.  The order
    # of the three is in absolute pc index order (Cr, Ma, Lu, Ro, Fr, Ay, Mg)

    # Here's where the requirements are compared against the reqs
    # $C1/F595 DF 00 00 CC CMP $CC0000,x
    # Change the bank to the new one.
    rom_new_start = to_rom_ptr(lrn_req_new_start)
    lrn_req_new_start_bytes = to_little_endian(rom_new_start, 3)
    rom[0x01F595+3] = lrn_req_new_start_bytes[2]


def fix_lrn_ref_refs(rom, lrn_ref_new_start):
    # The references to learning requirements are much harder to pin down.
    # There is a block from 0x0C2778 to 0x0C27F5 which gives information
    # for accessing the learning reqs.  Five byte blocks.
    #   -1st byte: bitmask of chars involved in tech (cr=0x80, ma=0x40,...)
    #   -2nd byte: first tech_id for these characters
    #   -3rd byte: number of techs (starting from the 2nd byte) for these chars
    #   -4th/5th byte: 16-bit address into the learning reqs for 2nd byte tech

    # Second record: A0 3C 03 03 28
    # A0 = 1010 0000 -> Crono, Lucca
    # 3C = tech_id of fire_whirl
    # 03 = number of techs Crono+Lucca has
    # 03 28 = req of fire_whirl is at 0x0C2803 (there: 01 01 FF. Checks out)

    # The code gets an offset into the start of the refs block
    # Change this to the new start's last two bytes
    # $C1/F260 A2 78 27    LDX #$2778

    # We only need the last two bytes
    rom_new_start = to_rom_ptr(lrn_ref_new_start)
    lrn_ref_start_bytes = to_little_endian(rom_new_start, 3)
    rom[0x01F261:0x01F261+2] = lrn_ref_start_bytes[0:2]

    # This index (eventually) is used in the following lines
    #   $C1/F26A BF 00 00 CC LDA $CC0000,x
    #   $C1/F28D BF 01 00 CC LDA $CC0001,x
    #   $C1/F2B0 BF 01 00 CC LDA $CC0001,x
    #   $C1/F2B9 BF 02 00 CC LDA $CC0002,x
    #   $C1/F2C4 BF 03 00 CC LDA $CC0003,x
    # We only need to change the CC part

    rom[0x01F26A+3] = lrn_ref_start_bytes[2]
    rom[0x01F28D+3] = lrn_ref_start_bytes[2]
    rom[0x01F2B0+3] = lrn_ref_start_bytes[2]
    rom[0x01F2B9+3] = lrn_ref_start_bytes[2]
    rom[0x01F2C4+3] = lrn_ref_start_bytes[2]


def fix_mp_refs(rom, mp_new_start):

    # $C2/BC4D BF 3B 25 CC LDA $CC253B,x --> 0x02BC4E (single tech menu)
    # $C1/CB5C BF 3B 25 CC LDA $CC253B,x --> 0x01CB5D (pre-battle, tech use)
    # $C1/CB75 BF 3B 25 CC LDA $CC253B,x --> 0x01CB76 (pre-battle, dual use?)
    # $C1/CB8E BF 3B 25 CC LDA $CC253B,x --> 0x01CB8F (in-battle)

    mp_refs = [0x02BC4E, 0x01CB5D, 0x01CB76, 0x01CB8F]
    mp_offs = [0, 0, 0, 0]

    # update_ptrs(rom, mp_refs, mp_old_start, mp_new_start)
    change_ptrs(rom, mp_refs, mp_new_start, mp_offs)


def fix_menu_req_refs(rom, menu_req_new_start):
    # combo techs in x-menu use a different block for reqs.  These are used
    # to compute the mp cost of the techs involved in the combo.
    # The block starts at 0xCC28DB and lists the absolute tech_id of each tech
    # involved in a dual/triple.  Has a 00 at the end.  Unsure if needed.

    # Reqs are listed in tech_id order.  The entries of each record are sorted
    # in absolute pc-index order.  Dual tech records are 2 bytes, triple tech
    # records are 3 bytes.

    # $FF/F8F6 BF DB 28 CC LDA $CC28DB,x --> 0x3FF8F7
    # $FF/F8FF BF DB 28 CC LDA $CC28DB,x --> 0x3FF900
    # $FF/F947 BF 35 29 CC LDA $CC2935,x --> 0x3FF948
    # This one needs to be fixed depending on the number of dual techs

    # Note: The above three run upon hitting start when the game loads
    # $FF/F98C BF 53 29 CC LDA $CC2953,x --> 0x3FF98D (Rock techs)
    # This one is handled by the rock routines.

    menu_req_refs = [0x3FF8F7, 0x3FF900]  # +[0x3FF948, 0x3FF98D]
    menu_req_offs = [0, 0]

    # update_ptrs(rom, menu_req_refs, menu_req_old_start, menu_req_new_start)
    change_ptrs(rom, menu_req_refs, menu_req_new_start, menu_req_offs)


def fix_grp_begin_refs(rom, grp_begin_new_start):
    # Group Sizes
    # I believe these are mainly used for the battle menu.  They have the form
    # XX YY where XX is the start tech of one group and YY is the start tech of
    # the next.  The data is short, so just reproduce it here
    #
    # 0x02BD40:
    # 01 09 11 19 21 29 31 39 3C 3F 42 45 48 4B 4E 51
    # 54 57 5A 5D 60 63 66 67 68 69 6A 6B 6C 6D 6E 6F
    # 70 71 72 73 74 00 <-- 0x02BD65

    grp_begin_refs = [0x02BD12, 0x02BD18]
    grp_begin_offs = [1, 0]

    # update_ptrs(rom, grp_begin_refs, grp_begin_old_start,
    #             grp_begin_new_start)

    change_ptrs(rom, grp_begin_refs, grp_begin_new_start, grp_begin_offs)


def fix_atb_pen_refs(rom, atb_pen_new_start, num_trips):

    # ATB Delay
    # When using a tech, there is (supposed to be) an ATB penalty.  Each
    # tech has a 1 byte record in a range beginning at 0x0C2BDC.  The high
    # four bits give pc-1 in the battle group's delay while the low four bits
    # are used for pc-2.
    # Ex. A value of 57 means 50% penalty for P1 and 70% for P2

    # When there is a triple tech, there 15 extra bytes (10 trips + 5 rocks)
    # at the end of the range which determine the pc-3's delay. Low 4 bits.

    atb_pen_refs = [0x01BDF6, 0x01BE72]
    atb_pen_offs = [0, 0]

    # update_ptrs(rom, atb_pen_refs, atb_pen_old_start, atb_pen_new_start)
    change_ptrs(rom, atb_pen_refs, atb_pen_new_start, atb_pen_offs)

    """
    print('offsets:')
    for ptr in grp_begin_refs:
        x = rom[ptr:ptr+3]
        v = get_value_from_bytes(x)
        v = to_file_ptr(v)
        offset = v - grp_begin_old_start
        print(offset)
    print('done.')

    input()
    """

    # There is a reference at 0x01BEEF for loading pc-3's delay
    # This address should be exactly num_trips past the start.  Note that
    # num_trips is counting all triples, including rocks.

    pc3_start = atb_pen_new_start + num_trips
    pc3_start = to_rom_ptr(pc3_start)
    pc3_start_bytes = to_little_endian(pc3_start, 3)

    rom[0x01BEEF:0x01BEEF+3] = pc3_start_bytes[:]


# This routine does not really write new data (one exception).  It just finds
# and replaces pointers to the data.
# The one exception is that with techs_learned some data is copied because
# the relevant instruction that needs changing copies additional data.
def fix_tech_refs(rom,
                  control_new_start,
                  effect_new_start,
                  gfx_new_start,
                  target_new_start,
                  bat_grp_new_start,
                  menu_grp_new_start,
                  names_new_start,
                  desc_ptr_new_start,
                  desc_new_start,
                  techs_learned_old_start, techs_learned_new_start,
                  lrn_req_new_start,
                  lrn_ref_new_start,
                  mp_new_start,
                  menu_req_new_start,
                  grp_begin_new_start,
                  atb_pen_new_start, num_trips):

    fix_control_refs(rom, control_new_start)
    fix_effect_refs(rom, effect_new_start)
    fix_gfx_refs(rom, gfx_new_start)
    fix_target_refs(rom, target_new_start)
    fix_bat_grp_refs(rom, bat_grp_new_start)
    fix_menu_grp_refs(rom, menu_grp_new_start)
    fix_name_refs(rom, names_new_start)
    fix_desc_ptr_refs(rom, desc_ptr_new_start)
    fix_desc_refs(rom, desc_new_start)
    fix_techs_learned(rom, techs_learned_old_start, techs_learned_new_start)
    fix_lrn_req_refs(rom, lrn_req_new_start)
    fix_lrn_ref_refs(rom, lrn_ref_new_start)
    fix_mp_refs(rom, mp_new_start)
    fix_menu_req_refs(rom, menu_req_new_start)
    fix_grp_begin_refs(rom, grp_begin_new_start)
    fix_atb_pen_refs(rom, atb_pen_new_start, num_trips)
