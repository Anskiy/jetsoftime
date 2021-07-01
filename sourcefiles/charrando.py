# TODO List:
#  -Fix Ayla fist loading -- Done in battle.  Menu?  Need to poke around.
#     It is possible that the fist in battle just gets written back to Ayla
#  -Junk shows up in triple tech list when there are no triple techs.
#     Consider early RTS/NOP out routine when no triples (doubles?).
#     This might be fixed, but has to be tested.


import copy
import techrandomizer
import random
import ipswriter

from techdb import TechDB
from byteops import get_record, set_record, to_little_endian, \
    update_ptrs, to_rom_ptr, print_bytes
from statcompute import PCStats as PC
import scriptextend as scripts


def get_ct_name(string):
    return fix_ct_str_len(to_ct_str(string), TechDB.name_size)


def fix_ct_str_len(str_bytes, length):
    if len(str_bytes) >= length:
        str_bytes = str_bytes[0:length]
    else:
        while len(str_bytes) < length:
            str_bytes.append(0xEF)

    return str_bytes


def to_ct_str(string):
    ret = bytearray()
    for x in string:
        if x.isupper():
            ret.append(ord(x)-65+0xA0)
        elif x.islower():
            ret.append(ord(x)-97+0xBA)
        elif x == ' ':
            ret.append(0xEF)
        elif x == ',':
            ret.append(0xED)

    return ret

# Given the base TechDB and the pc reassignment list return an empty DB with
# all of the needed groups and empty space
#   orig_db should be the vanilla (or rando-vanilla) db
#   reassign is a 7 element list saying how the PCs get reassigned
#     Ex: [ 0 0 0 1 2 3 4 ] means Crono, Marle, Lucca are now Crono, Robo is
#       Marle, Frog is Lucca, Ayla is Robo, and Magus is Frog
def max_expand_empty_db(orig_db, reassign, dup_duals=False):
    new_menu_grps = bytearray()
    new_bat_grps = bytearray()
    new_grp_thresh = bytearray()

    cur_grp_ind = 0

    # Empty db.
    db = TechDB()

    # Add the single tech groups to the empty db.
    num_sing_grps = 0
    new_grp_thresh.append(1)
    for i in range(0, 7):
        grp = 0x80 >> i
        new_menu_grps.append(grp)
        new_bat_grps.extend([i, 0xFF, 0xFF])
        new_grp_thresh.append(new_grp_thresh[-1]+8)
        num_sing_grps += 1
        cur_grp_ind += 1

    # Add the dual tech groups to the empty db.
    # We use reassign[] to figure out the appropriate group in orig_db and
    # then copy the appropriate data over.
    db.first_dual_grp = cur_grp_ind
    num_dual_grps = 0
    for i in range(0, 7):
        for j in range(i+1, 7):
            # [i,j] is a potential dual tech group
            grp = 0
            orig_grp = 0
            orig_set = set()

            # Get the bitmask for [reassign[i], reassign[j]]
            for x in [i, j]:
                grp |= 0x80 >> x
                orig_grp |= 0x80 >> reassign[x]
                orig_set.add(reassign[x])

            # Find the reassign group in orig_db
            orig_ind = orig_db.get_menu_grp_ind(orig_grp)

            # If orig_ind is None it means we have a Magus involved.
            # If len(orig_set) != 2, then i,j are the same pc now

            # We're going to allow same-char-pairs
            # Same char pairs will be found in orig_db as a single tech group
            if orig_ind is not None \
               and (len(orig_set) == 2
                    or (dup_duals and
                        set([0, 1, 3, 2, 4, 5]).intersection(orig_set))):
                new_menu_grps.append(grp)

                # dummy battle group gets overwritten once we start adding
                # the tech data in
                new_bat_grps.extend([0, 0, 0])

                # There are always 3 techs in a dual group
                new_grp_thresh.append(new_grp_thresh[-1]+3)
                cur_grp_ind += 1
                num_dual_grps += 1

    # Do what we did for dual techs for triple techs
    db.first_trip_grp = cur_grp_ind
    num_trip_grps = 0

    # An extra issue is that rock groups need to be differentiated
    num_rock_grps = 0

    rock_orig_ids = []
    rock_types = []

    rock_menu_grps = []
    rock_bat_grps = bytearray()

    for i in range(0, 7):
        for j in range(i+1, 7):
            for k in range(j+1, 7):
                grp = 0
                orig_grp = 0
                orig_set = set()

                for x in [i, j, k]:
                    grp |= 0x80 >> x
                    orig_grp |= 0x80 >> reassign[x]
                    orig_set.add(reassign[x])

                orig_ind = orig_db.get_menu_grp_ind(orig_grp)

                # Again, ensure no repeats in the group and that the group
                # had a tech in orig_db
                if orig_ind is not None and len(orig_set) == 3:

                    # We will defer adding rock groups until later, but each
                    # triple group has only 1 tech, so it's safe to add it to
                    # the threshold list now
                    new_grp_thresh.append(new_grp_thresh[-1]+1)
                    if orig_ind >= orig_db.first_rock_grp:
                        # Record the rock information but don't add it yet
                        # In particular don't increment cur_grp_ind
                        rock_menu_grps.append(grp)
                        rock_bat_grps.extend([0, 0, 0])
                        orig_tech_id = orig_db.group_sizes[orig_ind]
                        rock_offset = orig_tech_id-orig_db.first_rock_tech
                        rock_orig_ids.append(orig_tech_id)
                        rock_types.append(rock_offset)
                        num_rock_grps += 1
                    else:
                        # Add triple group and dummy battle group
                        new_menu_grps.append(grp)
                        new_bat_grps.extend([0, 0, 0])
                        num_trip_grps += 1

                        # We're going to put all the rocks at the end
                        cur_grp_ind += 1
                else:
                    pass
                    # print("Skipping %2.2X" % orig_grp)

    db.first_rock_grp = cur_grp_ind
    db.rock_types = rock_types[:]

    new_menu_grps.extend(rock_menu_grps)
    new_bat_grps.extend(rock_bat_grps)

    db.menu_grps = new_menu_grps

    db.menu_grp_count = len(db.menu_grps)
    db.bat_grps = new_bat_grps
    db.bat_grp_count = len(db.menu_grps)

    # We always recorded the start of the *next* group when we added a group.
    # So now the thresholds have one extra entry.
    del(new_grp_thresh[-1])
    db.group_sizes = new_grp_thresh[:]

    # rock groups don't get learning data
    db.lrn_req_count = 3*num_dual_grps + num_trip_grps
    db.lrn_ref_count = num_dual_grps + num_trip_grps

    # 8 per char sing, 3 per dual group, 1 per trip,
    db.num_techs = (8*num_sing_grps
                    + 3*num_dual_grps
                    + num_trip_grps
                    + num_rock_grps)

    # 1 per tech, 1 blank, 7 basic attacks at end
    db.control_count = 1 + db.num_techs + 7

    # There is the empty tech at position 0 which has a gfx entry
    db.gfx_count = 1 + db.num_techs

    # Other strings (menu titles) have desc_ptrs/descs.
    # Add them after this copying
    db.desc_ptr_count = 1 + db.num_techs

    # Again, empty tech 0 adds a record
    db.target_count = 1 + db.num_techs
    db.name_count = 1 + db.num_techs

    num_menu_mps = 2*3*num_dual_grps+3*(num_trip_grps+num_rock_grps)

    db.atb_pen_count = 1 + db.num_techs + num_trip_grps + num_rock_grps

    dat = [db.controls, db.gfx, db.names,
           db.desc_ptrs, db.techs_learned, db.lrn_reqs,
           db.lrn_refs, db.mps, db.menu_mp_reqs,
           db.targets, db.atb_pens]

    counts = [db.control_count, db.gfx_count, db.name_count,
              db.desc_ptr_count, db.menu_grp_count, db.lrn_req_count,
              db.lrn_ref_count, db.mp_count, num_menu_mps,
              db.target_count, db.atb_pen_count]

    sizes = [TechDB.control_size, TechDB.gfx_size, TechDB.name_size,
             TechDB.desc_ptr_size, 1, TechDB.lrn_req_size,
             TechDB.lrn_ref_size, 1, 1,
             TechDB.target_size, 1]

    for i in range(0, len(dat)):
        dat[i][:] = bytearray([0])*(counts[i]*sizes[i])

    # There is graphics data after the tech data for things like running away
    # and greendream effect.  This needs to be appended to the new db's gfx.
    orig_tech_gfx_count = orig_db.group_sizes[-1]
    orig_tech_gfx_len = orig_tech_gfx_count * TechDB.gfx_size
    extra_gfx = orig_db.gfx[orig_tech_gfx_len:len(orig_db.gfx)]

    db.gfx.extend(extra_gfx)
    db.gfx_count = len(db.gfx) // 7

    # There are desc ptrs after tech descs.  Copy them to the end.
    orig_tech_dptr_count = orig_db.group_sizes[-1]
    orig_tech_dptr_len = orig_tech_dptr_count * TechDB.desc_ptr_size
    extra_dptr = orig_db.desc_ptrs[orig_tech_dptr_len:len(orig_db.desc_ptrs)]

    db.desc_ptrs.extend(extra_dptr)
    db.desc_ptr_count = len(db.desc_ptrs) // 2

    db.mps = orig_db.mps[:]
    db.mp_count = len(db.mps)

    db.menu_mp_reqs = bytearray([0]*(2*num_dual_grps*3 +
                                     3*num_trip_grps +
                                     3*num_rock_grps))

    db.menu_usable_ids = [False]*db.control_count

    # lrn refs can be set up relative to 0x000000 since they're empty
    db.lrn_req_start = orig_db.lrn_req_start
    db.rewrite_lrn_refs()

    db.effects = orig_db.effects[:]
    db.effect_count = orig_db.effect_count

    # just keep the original db's tech descriptions since we are not going to
    # mess with that at all.
    db.descs = orig_db.descs[:]
    db.desc_start = orig_db.desc_start

    db.pc_target = bytearray([0xFF]*db.target_count)

    # Now that the db is recording write locations, we should set the data
    # starts to match orig_db

    db.control_start = orig_db.control_start
    db.effect_start = orig_db.effect_start
    db.gfx_start = orig_db.gfx_start
    db.target_start = orig_db.target_start
    db.bat_grp_start = orig_db.bat_grp_start
    db.menu_grp_start = orig_db.menu_grp_start
    db.name_start = orig_db.name_start
    db.desc_ptr_start = orig_db.desc_ptr_start
    db.desc_start = orig_db.desc_start
    db.techs_learned_start = orig_db.techs_learned_start
    db.lrn_req_start = orig_db.lrn_req_start
    db.lrn_ref_start = orig_db.lrn_ref_start
    db.mp_start = orig_db.mp_start
    db.menu_req_start = orig_db.menu_req_start
    db.group_sizes_start = orig_db.group_sizes_start
    db.atb_pen_start = orig_db.atb_pen_start

    # I think the orig_starts are all unused now except for techs_learned.
    # The "copy the whole block" strategy is making this ugly.

    """
    db.orig_control_start = orig_db.orig_control_start
    db.orig_effect_start = orig_db.orig_effect_start
    db.orig_gfx_start = orig_db.orig_gfx_start
    db.orig_target_start = orig_db.orig_target_start
    db.orig_bat_grp_start = orig_db.orig_bat_grp_start
    db.orig_menu_grp_start = orig_db.orig_menu_grp_start
    db.orig_name_start = orig_db.orig_name_start
    db.orig_desc_ptr_start = orig_db.orig_desc_ptr_start
    db.orig_desc_start = orig_db.orig_desc_start
    db.orig_techs_learned_start = orig_db.orig_techs_learned_start
    db.orig_lrn_req_start = orig_db.orig_lrn_req_start
    db.orig_lrn_ref_start = orig_db.orig_lrn_ref_start
    db.orig_mp_start = orig_db.orig_mp_start
    db.orig_menu_req_start = orig_db.orig_menu_req_start
    db.orig_group_sizes_start = orig_db.orig_group_sizes_start
    db.orig_atb_pen_start = orig_db.orig_atb_pen_start
    """

    db.orig_techs_learned_start = orig_db.orig_techs_learned_start
    return db


# change_items changes the usability of each weapon/armor/acc to match the
# character assignment
def change_items(from_ind, to_ind, rom,
                 item_dat, item_start,
                 acc_dat, acc_start):
    # print("Putting %d's usability into %d's" % (from_ind, to_ind))
    num_items = len(item_dat)//6

    from_bit = 0x80 >> from_ind

    for i in range(0, num_items):
        offset = i*6+3
        to_use_byte = item_start+offset
        from_usable = (item_dat[offset] & from_bit)

        if(from_usable != 0):
            rom[to_use_byte] |= (0x80 >> to_ind)
        else:
            rom[to_use_byte] &= ~(0x80 >> to_ind)

    num_acc = (len(acc_dat))//4

    for i in range(0, num_acc):
        offset = i*4+3
        to_use_byte = acc_start + offset
        from_usable = (acc_dat[offset] & from_bit)

        if(from_usable != 0):
            rom[to_use_byte] |= (0x80 >> to_ind)
        else:
            rom[to_use_byte] &= ~(0x80 >> to_ind)


# One warning here.  TechDB sometimes has to move the whole stat block to make
# room for the techs learned block.  The stat changing should happen before
# the TechDB is written to the rom so that the changes get moved.
# TODO: Change this function to read the stats fom a different location.  This
#   Functionality is in the PCStats class, but it's just cumbersome.
def reassign_stats(rom, reassign):

    # All of the heavy lifting is done by PCStats class
    orig_pcs = [PC.stats_from_rom_default(rom, i) for i in range(7)]
    new_pcs = [copy.deepcopy(orig_pcs[reassign[i]]) for i in range(7)]

    # Now each new_pc needs to be releveled/tech leveled
    for i in range(7):
        # correct pc index
        new_pcs[i].stat_block[0] = i

        orig_lvl = orig_pcs[i].level
        new_pcs[i].set_level(orig_lvl)

        orig_tech_lvl = orig_pcs[i].tech_level
        new_pcs[i].set_tech_level(orig_tech_lvl)

        new_pcs[i].write_to_rom_default(rom, i)

    # This can probably be removed.  But to avoid potential issues with TechDB
    # putting the stat block in bank 4F, copy the stat block to the new bank.
    rom[0x4F0000:0x4F0000+0x230+2*7] = rom[0x0C0000:0x0C0000+0x230+2*7]


# Each control header has indices to the associated effect headers.  The order
# of the effect header indices matches the order of the battle group. When we
# make a copy of a tech for a new battle group, we have to update the indices
# to match the new characters that are performing the tech.
def fix_effect_ind(ctl_hdr, bat_grp):

    # effect indices are in bytes 5,6 and 7 (0-indexed)
    for i in range(5, 8):
        # x80 bit means ignore the effect but use the mp cost
        eff_x80 = ctl_hdr[i] & 0x80
        eff_ind = ctl_hdr[i] & 0x7F
        if 0 < eff_ind < 0x39:
            tech_num = (eff_ind-1) % 8
            new_pc = bat_grp[i-5]

            ctl_hdr[i] = (new_pc*8 + tech_num + 1) | eff_x80


def change_basic_attacks(from_ind, to_ind, orig_db, new_db):

    # Copy the control header -- really just changes the first effect byte
    orig_count = len(orig_db.controls) // TechDB.control_size
    orig_atk_start = orig_count - 7

    new_count = len(new_db.controls) // TechDB.control_size
    new_atk_start = new_count - 7

    x = get_record(orig_db.controls, orig_atk_start+from_ind,
                   TechDB.control_size)
    x[0] = to_ind
    set_record(new_db.controls, x, new_atk_start+to_ind,
               TechDB.control_size)


def change_single_techs(from_ind, to_ind, orig_db, new_db):

    new_db.mps[0] = 0

    from_start = 1+from_ind*8
    to_start = 1+to_ind*8
    for i in range(8):

        from_i = from_start + i
        to_i = to_start + i

        # first fix menu usability
        new_db.menu_usable_ids[to_i] = orig_db.menu_usable_ids[from_i]

        tech = orig_db.get_tech(from_i)

        tech['bat_grp'] = bytearray([to_ind, 0xFF, 0xFF])
        
        # In the menu (and only the menu) the game expects the effect
        # headers to be in tech_id order.  This is deep in menu code and
        # I'm worried that fixing it will make menus slower.  So for now
        # we'll shuffle the effect headers.  This means updating dual/trip
        # control headers later!

        fix_effect_ind(tech['control'], tech['bat_grp'])

        x = get_record(orig_db.effects, from_i, TechDB.effect_size)
        set_record(new_db.effects, x, to_i, TechDB.effect_size)

        new_db.mps[to_i] = orig_db.mps[from_i]

        new_db.set_tech(tech, to_i)

        # set_tech takes care of most things, but to avoid adding duplicate
        # descriptions, we just repoint to the original description.
        # We're assuming that nobody messes with the original tech descriptions
        dptr = get_record(orig_db.desc_ptrs, from_i,
                          orig_db.desc_ptr_size)
        set_record(new_db.desc_ptrs, dptr, to_i,
                   new_db.desc_ptr_size)

        if orig_db.pc_target[from_i] != 0xFF:
            new_db.pc_target[to_i] = to_ind
        else:
            new_db.pc_target[from_i] = 0xFF

def get_ll_prot_all(old_db):
    prot_all = old_db.get_tech(0x15)
    prot_all['bat_grp'] = [2, 2, 0xFF]

    prot_all['control'][0] &= 0x7F
    prot_all['control'][6] = 0x80 | 0x15
    prot_all['lrn_req'] = [5, 5, 0xFF]
    prot_all['mmp'] = [0x15, 0x15]

    prot_all['target'][0] = 0x81
    prot_all['target'][1] = 0x00

    prot_all['gfx'][0] = 0x81

    prot_all['name'] = get_ct_name('Protect All')

    return prot_all


def get_ff_hex_mist(old_db):
    hex_mist = old_db.get_tech(0x26)  # water 2 base
    hex_mist['bat_grp'] = [4, 4, 0xFF]
    hex_mist['control'][0] &= 0x7F
    hex_mist['control'][6] = 0x26
    hex_mist['control'][8:10] = [9, 9]

    hex_mist['lrn_req'] = [6, 6, 0xFF]
    hex_mist['mmp'] = [0x26, 0x26]
    hex_mist['gfx'][0] = 0x82
    hex_mist['gfx'][6] = 0x4

    hex_mist['name'] = get_ct_name('FlexgonMist')

    return hex_mist


def get_rr_supervolt(old_db):
    sv = old_db.get_tech(0x41)

    sv['bat_grp'] = [3, 3, 0xFF]
    sv['control'][6] = 0x20

    sv['lrn_req'] = [8, 8, 0xFF]
    sv['mmp'] = [0x20, 0x20]
    sv['gfx'][0] = 0x83

    return sv


def get_mm_haste_all(old_db):

    ha = old_db.get_tech(0x0D)

    ha['bat_grp'] = [1, 1, 0xFF]
    ha['control'][0] &= 0x7F
    ha['control'][6] = 0x80 | 0x0D

    ha['lrn_req'] = [5, 5, 0xFF]
    ha['mmp'] = [0x20, 0x20]

    ha['target'][0] = 0x81

    ha['gfx'][0] = 0x84
    ha['gfx'][6] = 0x15

    ha['name'] = get_ct_name('Haste All')

    return ha


def get_aa_beast_toss(old_db):
    beast_toss = old_db.get_tech(0x5F)

    beast_toss['bat_grp'] = [5, 5, 0xFF]
    beast_toss['control'][6] = 0x2C
    beast_toss['lrn_req'] = [4, 4, 0xFF]
    beast_toss['mmp'] = [0x2C, 0x2C]

    # This will need to change as we add more scripts
    beast_toss['gfx'][0] = 0x80

    return beast_toss


# Tech is the vanilla tech that needs reassignment.
# New PCs should be a battle group for the tech (may need shuffling)
def reassign_tech(tech, new_pcs, reassign):
    # redo battle group
    bat_grp = tech['bat_grp']
    new_grp = bat_grp[:]

    num_chars = 3 - bat_grp.count(0xFF)

    # Redo battle group
    temp_grp = new_pcs[:]
    for el in range(num_chars):
        pc = bat_grp[el]

        # find one of the new_pcs to fill the role of pc
        for (ind, z) in enumerate(new_pcs):
            if reassign[z] == pc:
                new_grp[el] = z
                del(new_pcs[ind])
                # The break is for same-char duals.  For example, Ayla beast
                # toss would have battle group [5, 5, 0xFF].  We only want
                # to replace one of the 5s with each reassigned Ayla.  So
                # stop looking after the first.
                break

    while len(new_grp) < 3:
        new_grp.append(0xFF)

    # Update special targetting info
    if tech['pc_target'] != 0xFF:
        for z in new_grp[0:num_chars]:
            if reassign[z] == tech['pc_target']:
                tech['pc_target'] = z
                break

    # For effect indices between 1 and 0x38, replace with the equivalent
    # effect of the reassign char
    tech['bat_grp'] = new_grp[:]
    fix_effect_ind(tech['control'], tech['bat_grp'])

    # Learn requirements and menu reqs need to be resorted by pc-index
    if tech['lrn_req'] is not None:
        lrn_req = tech['lrn_req']
    else:
        lrn_req = [0, 0, 0]  # dummy values
    mmp = tech['mmp']

    if len(mmp) == 2:
        mmp.append(0xFF)
    
    bat_grp, new_grp = zip(*sorted(zip(bat_grp, new_grp)))
    new_grp, lrn_req, mmp = zip(*sorted(zip(new_grp, lrn_req, mmp)))

    if mmp[-1] == 0xFF:
        mmp = mmp[0:2]
    
    if tech['lrn_req'] is not None:
        tech['lrn_req'] = lrn_req

    # Now apply reassign to mmp
    new_mmp = bytearray()
    
    for el in range(len(mmp)):
        pc = (mmp[el]-1) // 8
        tech_num = (mmp[el]-1) % 8
        temp_grp = tech['bat_grp'][:]
        for z in temp_grp:
            if z == 0xFF:
                continue
            elif reassign[z] == pc:
                new_pc = z
                temp_grp.remove(z)
                new_mmp.append(new_pc*8+tech_num+1)
                break

    tech['mmp'] = new_mmp[:]


def update_dual_techs(old_db, new_db, reassign, dup_duals):
    # print_bytes(old_db.menu_grps, 8)
    for i in range(0, 7):
        for j in range(i+1, 7):

            n1 = 0x80 >> i
            n2 = 0x80 >> j
            to_grp = n1 | n2

            # Hard is deleting the perf group from the tech_db.
            # Easy is making the dual tech non-learnable
            # print(f'PCs {i} and {j} became {reassign[i]} and {reassign[j]}')

            to_mg_ind = new_db.get_menu_grp_ind(to_grp)
            if reassign[i] == reassign[j]:
                if(to_mg_ind is None):
                    # print("Skipping.")
                    pass
                elif dup_duals and reassign[i] in set([0, 1, 2, 3, 4, 5]):
                    to_start_id = new_db.group_sizes[to_mg_ind]
                    if reassign[i] == 0:
                        # Cr-Cr X-strike
                        x_strike = old_db.get_tech(0x42)
                        x_strike['bat_grp'] = [0, 0, 0xFF]
                        x_strike['lrn_req'] = [1, 1, 0xFF]
                        x_strike['control'][6] = 1
                        x_strike['mmp'] = [1, 1]

                        reassign_tech(x_strike, [i, j], reassign)
                        new_db.set_tech(x_strike, to_start_id)
                    elif reassign[i] == 1:
                        # Ma-Ma Haste all
                        ha = get_mm_haste_all(old_db)
                        reassign_tech(ha, [i, j], reassign)
                        new_db.set_tech(ha, to_start_id)
                    elif reassign[i] == 2:
                        # Lu-Lu Prot All
                        prot_all = get_ll_prot_all(old_db)
                        reassign_tech(prot_all, [i, j], reassign)
                        new_db.set_tech(prot_all, to_start_id)
                    elif reassign[i] == 3:
                        # Ro-Ro Supervolt
                        sv = get_rr_supervolt(old_db)
                        reassign_tech(sv, [i, j], reassign)
                        new_db.set_tech(sv, to_start_id)
                    elif reassign[i] == 4:
                        # Fr-Fr Hex Mist
                        hex_mist = get_ff_hex_mist(old_db)
                        reassign_tech(hex_mist, [i, j], reassign)
                        new_db.set_tech(hex_mist, to_start_id)
                    elif reassign[i] == 5:
                        # Ayla-Ayla Beast Toss

                        beast_toss = get_aa_beast_toss(old_db)
                        reassign_tech(beast_toss, [i, j], reassign)
                        new_db.set_tech(beast_toss, to_start_id)

                    # Make the rest unlearnable
                    for k in range(1, 3):
                        id = to_start_id + k
                        new_db.controls[id*TechDB.control_size] |= 0x80
                else:
                    to_start_id = new_db.group_sizes[to_mg_ind]

                    print('Making techs %2.2X to %2.2X unlearnable'
                          % (to_mg_ind, to_mg_ind+2))

                    for k in range(3):
                        id = to_start_id + k

                        new_db.controls[id*TechDB.control_size] |= 0x80

                continue

            # Get the from group and its techs
            o1 = 0x80 >> reassign[i]
            o2 = 0x80 >> reassign[j]

            # This is the menu group of the "true" characters.  We'll use this
            # to look into the DB and get the right techs if they exist
            from_grp = o1 | o2

            # So if the old db doesn't know this group (magus involved) then
            # just move on!
            from_mg_ind = old_db.get_menu_grp_ind(from_grp)
            if (from_mg_ind is None):
                # print("Group not found in old_db. Skipping.")
                continue
            else:
                pass
                # print('Group found at %2.2X in old_db' % from_mg_ind)

            to_mg_ind = new_db.add_menu_grp(to_grp)
            to_start_id = new_db.group_sizes[to_mg_ind]

            from_start_id = old_db.group_sizes[from_mg_ind]
            # print('Copying techs %2.2X to %2.2X' % (from_start_id,
            #                                         from_start_id+3))
            # print('\tinto %2.2X to %2.2X of new_db)'
            #       % (to_start_id, to_start_id+3))

            for k in range(3):
                # print("Reading tech_id %2.2X" % (from_start_id+k))
                tech = old_db.get_tech(from_start_id + k)
                reassign_tech(tech, [i, j], reassign)
                new_db.set_tech(tech, to_start_id+k)


def update_trip_techs(old_db, new_db, reassign):

    for i in range(new_db.first_trip_grp, len(new_db.menu_grps)):
        to_menu_grp = new_db.menu_grps[i]
        to_tech_id = new_db.group_sizes[i]
        to_bat_grp = bytearray()

        mask = 0x80
        for j in range(8):
            if to_menu_grp & mask > 0:
                to_bat_grp.append(j)
            mask = mask >> 1

        from_grp = 0
        from_set = set()
        for x in to_bat_grp:
            from_grp |= 0x80 >> reassign[x]
            from_set.add(reassign[x])

        # print("to_grp: %2.2X\tfrom_grp %2.2X" % (to_menu_grp, from_grp))

        from_grp_ind = old_db.get_menu_grp_ind(from_grp)
        if len(from_set) != 3 or from_grp_ind is None:
            # print('No triple for %2.2X ' % from_grp)
            # print('Making %2.2X unlearnable' % to_tech_id)
            ctl_start = to_tech_id*TechDB.control_size
            new_db.controls[ctl_start] |= 0x80
        else:
            # There is a tech to copy over
            from_tech_id = old_db.group_sizes[from_grp_ind]
            # print('Copying tech %2.2X to %2.2X in new_db'
            #       % (from_tech_id, to_tech_id))

            tech = old_db.get_tech(from_tech_id)
            reassign_tech(tech, to_bat_grp, reassign)
            new_db.set_tech(tech, to_tech_id)


# This one is a doozy.  Now that the same triple tech may be repeated for
# multiple groups, everything about rocks has to be changed.
# 1) Update some pointers to the start of the rock range in techs_learned.
#    Extend the range of the rock part of techs_learned.
# 2) Add a new data block to compute which tech_ids are enabled when pc X
#    equips rock Y.
# 3) Edit the SR that checks rock requirements to use the above data block.
def update_rock_techs(rom, db, reassign):
    # There are two relevant SRs for the rock checks
    #  1) $3FF958: Determines which rock techs are learnable based on the
    #              menu_mp_reqs.
    #  2) $0282E1: Checks for rocks and sets the appropriate techs as learned

    # SR-3FF958:
    # $FF/F97A BF 83 29 CC LDA $CC2983,x
    # This loads a menu group for a rock tech.  We need $CC2983 to become the
    # new start of the rock groups.  This reference is written along with the
    # db.

    # $FF/F98C BF 53 29 CC LDA $CC2953,x
    # This needs $CC2953 to be the start of the rock part of the menu_mp_req
    # Handled by write_db

    # $FF/F9B4 C9 05       CMP #$05
    # This is the number of rock techs
    num_rock_techs = len(db.menu_grps) - db.first_rock_grp
    rom[0x3FF9B5] = num_rock_techs

    # SR-0282E1: This is where it gets hard.
    # This SR detects a PC wearing a rock and sets the relevant parts of the
    # techs_learned list when one is found.  This depends on the array written
    # in the previous SR.

    # rock_offsets is a list of techs associated with each char,rock combo.
    # They are really offsets into the $7E04A4 list from the above SR.
    # The order is (pc0,rock0), (pc0,rock1)... so a pointer is computed by
    # pc_id*5 + rock_id

    rock_ptr_start = 0x4F1200
    rock_off_start = 0x4F1300

    rock_ptrs, rock_offsets = build_rock_ptrs(db)

    rom[rock_ptr_start:rock_ptr_start+len(rock_ptrs)] = rock_ptrs[:]
    rom[rock_off_start:rock_off_start+len(rock_offsets)] = rock_offsets[:]

    # Now we have to edit the SR
    """
    $C2/82E4 9C 57 28    STZ $2857  [$7E:2857]
    $C2/82E7 A2 57 28    LDX #$2857
    $C2/82EA A0 59 28    LDY #$2859
    $C2/82ED A9 02 00    LDA #$0002
    $C2/82F0 54 7E 7E    MVN 7E 7E
    This zeroes out the part of the techs-learned list that
    """

    # $C2/82E4 9C 57 28    STZ $2857
    # This needs to point to the start of the rock part of the techs_learned
    # Start is $2837.  Add db's first rock group.
    rock_lrn_start = 0x2837 + db.first_rock_grp

    rock_start_addr = bytearray(to_little_endian(rock_lrn_start, 2)[0:2])
    rom[0x0282E5:0x0282E5+2] = rock_start_addr[:]
    rom[0x0282E8:0x0282E8+2] = rock_start_addr[:]

    # We need to be 2 bytes farther for the MVN
    rom[0x0282EB:0x0282EB+2] = to_little_endian(rock_lrn_start+2, 2)[0:2]

    # The LDA needs to be #rocks - 3
    # Unless that would be negative...
    num_rock_techs = len(db.menu_grps) - db.first_rock_grp
    clear_num = 0
    if(num_rock_techs < 3):
        clear_num = 0
    else:
        clear_num = num_rock_techs - 3

    rom[0x0282EE:0x0282EE+2] = to_little_endian(clear_num, 2)

    rom[0x0282F3:0x0282F3+4] = bytearray.fromhex('5C 00 20 4F')

    """
    $4F/2000	 A2 00 26    LDX #$2600
    $4F/2003	 A0 00 00    LDY #$0000
    $4F/2006	 A9 00 00    LDA #$0000
    $4F/2009	 E2 20       SEP #$20   #8 bit A
    $4F/200B	 BD 2A 00    LDA $002A,x[$7E:FC4D]
    $4F/200E	 C9 AE       CMP #$AE
    $4F/2010	 90 37 	     BCC $37  #to rep #$20
    $4F/2012	 C9 B3       CMP #$B3
    $4F/2014	 B0 33       BCS $33
    OK.  Now get the pointer
    $4F/2016  	 38		SEC
    $4F/2017	 E9 AE		SBC #$AE
    # We have a rock, rock_id (in A) equipped to pc_id (in Y)
    $4F/2019	 8D 90 04	STA $TEMP
    $4F/201C	 98		TYA
    $4F/201D	 8D 92 04	STA $TEMPY
    $4F/2020	 0A		ASL         # ASL should CLC
    $4F/2021	 0A		ASL
    $4F/2022     6D 92 04       ADC $TEMPY  # 5*pc_id
    $4F/2025     6D 90 04       ADC $TEMP   # 5*pc_id + rock_id
    $4F/2028	 DA		PHX
    $4F/2029	 AA		TAX
    $4F/202A	 BF 00 12 4F	LDA $4F1200,x  #ptr to rock refs
    $4F/202E	 AA		TAX
    $4F/202F	 BF 00 13 4F	LDA $4F1300,x  .loop1
    $4F/2033	 C9 FF		CMP #$FF
    $4F/2035	 F0 0E		BEQ to the LDY
    $4F/2037     A8             TAY
    $4F/2038	 B9 A4 04	LDA $04A4, y
    $4F/203B	 F0 05		BEQ $05            # to INY and loop again
    $4F/203D	 A9 80		LDA #$80
    $4F/203F	 99 XX XX	STA $ROCKSTART, 9  # addr depends on num rocks
    $4F/2042	 E8		INY
    $4F/2043	 80 EA		BRA to .loop1 (-$20)
    $4F/2045     AC 92 04       LDY $TEMPY
    $4F/2048	 FA		PLX	.outloop1
    $4F/2049	 C2 20 		REP #$20
    $4F/204B     8A             TXA
    $4F/204C	 18		CLC
    $4F/204D	 69 50 00	ADC #$0050
    $4F/2050	 AA		TAX
    $4F/2051	 C8		INY
    $4F/2052	 C9 30 28	CMP #$2830
    $4F/2055	 90 AF		BCC $AF**    		# to LDA #$0000
    $4F/2057	 5C 1E 83 C2	JMP back to orig to end
    """

    rock_sr = bytearray.fromhex('A2 00 26 A0 00 00 A9 00 00 E2 20 BD 2A 00' +
                                'C9 AE 90 37 C9 B3 B0 33 38 E9 AE 8D 90 04' +
                                '98 8D 92 04 0A 0A 6D 92 04 6D 90 04' +
                                'DA AA BF 00 12 4F AA BF 00 13 4F C9 FF' +
                                'F0 0E A8 B9 A4 04 F0 05 A9 80' +
                                '99' + rock_start_addr.hex() +
                                'E8 80 EA' +
                                'AC 92 04' +
                                'FA C2 20 8A 18 69 50 00 AA C8' +
                                'C9 30 28 90 AF 5C 1E 83 C2')

    rom[0x4F2000:0x4F2000+len(rock_sr)] = rock_sr[:]

    # One last wrinkle:
    """
    $C2/B9AF A2 57 28    LDX #$2857
    $C2/B9B2 A0 20 7F    LDY #$7F20
    $C2/B9B5 A9 04       LDA #$04
    $C2/B9B7 54 7E 7E    MVN 7E 7E
    This is called right after the above SR.  It copies the rock part of
    techs-learned into a copy in 7e7f00
    """
    rom[0x02B9B0:0x02B9B0+2] = rock_start_addr[0:2]

    rock_copy_start = 0x7f00 + db.first_rock_grp
    rock_copy_addr = to_little_endian(rock_copy_start, 2)
    rom[0x02B9B3:0x02B9B3+2] = rock_copy_addr

    rom[0x02B9B6] = num_rock_techs
# end update_rock_techs()


# Some techs target based around a particular pc-index.  Single techs (usually)
# target around caster, but combo techs like double bomb will look for which
# pc has a particular id (id = 3 for double bomb).  So this routine:
# 1) Adds a data range to the rom indicating whether a tech has targetting
#    around a particular pc and which pc that is (1 byte, FF=nothing weird).
# 2) Updates a few of the targetting routines to target around the pc-id given
#    by that data range.
def update_targetting(rom, db, reassign):
    # techdb keeps track of weird targetting
    rom[0x5F8000:0x5F8000+len(db.pc_target)] = db.pc_target[:]

    # Ok here's the really ugly stuff.
    # We have to fix robo and magus's self-based attacks.
    """
    Old beginning of "Around Robo" targeting (0x13,0x14)
    $C1/22A4	9C 04 96	STZ $9604
    $C1/22A7	7B		TDC
    $C1/22A8	AA		TAX

    We'll jump to a new place instead.  Should this be JSL? Maybe, but slower.
    Also part of the failure is an early RTS.  So we'd have to return, then
    branch based on X.  Also slower.
    $C1/22A9	5C 00 10 4F	JMP $4F1000

    Now at $4f1000:
    $4F/1000	AD E3 9E	LDA $9EE3  <--- the tech_id
    $4F/1003	AA		TAX
    $4F/1004	BF 00 80 5F	LDA $5F8000, x <--- target focus pc
    $4F/1008	48		PHA
    $4F/1009	7B		TDC
    $4F/100A	AA		TAX
    $4F/100B	BD 80 29	LDA $2980,x	.begin
    $4F/100E	C3 01		CMP $01,s
    $4F/1010	F0 0B		BEQ $0B 	to .success
    $4F/1012	E8		INX
    $4F/1013	E0 03 00	CPX #0003
    $4F/1016	D0 F3		BNE $F3		to .begin
    $4F/1018	68		PLA		# fix stack
    $4F/1019	5C B6 22 C1	JMP $C122B6 	# to original RTS
    $4F/101D	68		PLA		.success
    $4F/101E	5C B7 22 C1	JMP $C122B7	# to original continuation
    When first writing this I was scared to use memory, so I used the stack.
    At this point I have little desire to change it.
    """

    area_robo = bytearray.fromhex('9C 04 96 7B AA 5C 00 10 4F')
    find_robo_area = bytearray.fromhex('AD E3 9E AA BF 00 80 5F 48 7B AA ' +
                                       'BD 80 29 C3 01 F0 0B E8 E0 03 00 ' +
                                       'D0 F3 68 5C B6 22 C1 68 5C B7 22 C1')

    rom[0x0122A4:0x0122A4+len(area_robo)] = area_robo
    rom[0x4F1000:0x4F1000+len(find_robo_area)] = find_robo_area

    # Blade Toss is almost identical.  There's no STZ though, and we're
    # going to jump to essentially identical code.
    # Yes, SR would be nice, but it gets weird sorting the early return out.

    # $C1/21D6 BD 80 29    LDA $2980,x[$7E:2980] --> JUMP
    line_robo = bytearray.fromhex('5C 30 10 4F')
    find_robo_line = bytearray.fromhex('AD E3 9E AA BF 00 80 5F 48 7B AA ' +
                                       'BD 80 29 C3 01 F0 0B E8 E0 03 00 ' +
                                       'D0 F3 68' +
                                       '5C E3 21 C1' + '68' +
                                       '5C E4 21 C1')

    rom[0x0121D6:0x0121D6+len(line_robo)] = line_robo
    rom[0x4F1030:0x4F1030+len(find_robo_line)] = find_robo_line

    # Magus black hole is also the same.
    # $C1/22D8 BD 80 29    LDA $2980,x[$7E:29B6]

    area_magus = bytearray.fromhex('5C 60 10 4F')
    find_mag_area = bytearray.fromhex('AD E3 9E AA BF 00 80 5F 48 7B AA ' +
                                      'BD 80 29 C3 01 F0 0B E8 E0 03 00 ' +
                                      'D0 F3 68' +
                                      '5C E5 22 C1' + '68' +
                                      '5C E6 22 C1')
    rom[0x0122D8:0x0122D8+len(area_magus)] = area_magus
    rom[0x4F1060:0x4F1060+len(find_mag_area)] = find_mag_area


# The game needs to quickly determine which rock techs are enabled when PC-X
# equips Rock-Y.  This function builds a list of each character's rock techs
# as well as a pointer table to find the appropriate char/rock combo
def build_rock_ptrs(db):
    ptrs = [0]
    techs = []

    for pc in range(0, 7):
        rock_ids = [[], [], [], [], []]
        pc_bitmask = 0x80 >> pc

        for grp_id in range(db.first_rock_grp, len(db.menu_grps)):
            grp = db.menu_grps[grp_id]
            if grp & pc_bitmask != 0:
                offset = grp_id - db.first_rock_grp
                rock = db.rock_types[offset]
                tech = db.first_rock_tech+offset
                rock_ids[rock].append(tech)

        for i in range(0, 5):
            ptrs.append(ptrs[-1]+len(rock_ids[i])+1)
            techs.extend(rock_ids[i] + [0xFF])

    return ptrs, techs


# For some graphics pointer tables, the game uses the next pointer as the
# endpoint for the current pointer's data.  So repointing pc graphics will not
# work because the endpoints will not be computed properly.  The current scheme
# is to copy the endpoints to another location (the new_starts) and update the
# code that reads the endpoints to read from that block.
def copy_update_graphics_ptrs(rom, anim_new_start, unk_new_start, reassign):

    # 242600	242783	PTR	N	"Pointers to character animations (?)
    anim_start = 0x242600
    anim_end = 0x242784
    anim_size = anim_end-anim_start

    # 242800	242983	PTR	N	"Pointers to unconfirmed animation data
    unk_start = 0x242800
    unk_end = 0x242984
    unk_size = unk_end-unk_start

    # Copy pointers to elsewhere
    anim_new_end = anim_new_start+anim_size
    rom[anim_new_start:anim_new_end] = rom[anim_start:anim_end]

    unk_new_end = unk_new_start+unk_size
    rom[unk_new_start:unk_new_end] = rom[unk_start:unk_end]

    """
    Anims:  Animation data is divided into 4 chunks, one for each direction the
    character can face.  To determine where these chunks begin/end, the game
    finds the size of the anim data by subtracting the ptr from the next ptr.
    We are going to move the end points to the new block and read from there.

    $CC/E9EF BF 00 26 E4 LDA $E42600,x[$E4:2602]
    $CC/E9F3 85 86       STA $86    [$00:0086]
    $CC/E9F5 BF 01 26 E4 LDA $E42601,x[$E4:2603]
    $CC/E9F9 85 87       STA $87    [$00:0087]

    Later for Y-menu animations.  This is loading the next pointer for
    determining an endpoint
    $C2/F4CE BF 02 00 E4 LDA $E40002,x[$E4:2604]

    Again, getting the endpoint by doing two INY to get to the next pointer
    $C0/44EF C8          INY
    $C0/44F0 C8          INY
    $C0/44F1 B7 B5       LDA [$B5],y[$E4:2602]
    $C0/44F3 38          SEC
    $C0/44F4 88          DEY
    $C0/44F5 88          DEY
    """

    endpt = to_rom_ptr(anim_new_start + 2)
    endpt_bytes = to_little_endian(endpt, 3)

    # This is the ugliest thing I've done.
    # Note: since writing this comment, much uglier things have been done.
    # The below replaces the block with an LDA from the new block
    rom[0x0044EF:0x0044F6] = bytearray.fromhex('BB BF'
                                               + endpt_bytes.hex()
                                               + '38 EA')

    """
    Again for monster anims!
    $C0/4746 C8          INY
    $C0/4747 C8          INY
    $C0/4748 B7 B5       LDA [$B5],y[$E4:260E]
    $C0/474A 88          DEY
    $C0/474B 88          DEY
    $C0/474C 38          SEC

    End point loading
    $CC/EB34 BF 00 26 E4 LDA $E42600,x[$E4:260E]
    $CC/EB38 85 88       STA $88    [$00:0088]
    $CC/EB3A BF 00 28 E4 LDA $E42800,x[$E4:280E]
    """

    rom[0x004746:0x00474D] = bytearray.fromhex('BB BF'
                                               + endpt_bytes.hex()
                                               + '38 EA')

    anim_ptrs = [0x0CE9F0, 0x0CE9F6, 0x02F4CF, 0x0CEB35]
    update_ptrs(rom, anim_ptrs, anim_start, anim_new_start)

    """
    Unknown Anim data: Similar to the above.  The beginning of the next 
    object's data is used to determine length sometimes.  It's not divided by
    four like animations.  Someone online said this data counts how many frames
    to display each part of the animation.

    This is the next object's data being read
    $CC/E9FB BF 00 28 E4 LDA $E42800,x[$E4:2802]
    $CC/E9FF 85 88       STA $88    [$00:0088]
    $CC/EA01 BF 01 28 E4 LDA $E42801,x[$E4:280B]
    $CC/EA05 85 89       STA $89    [$00:0089]
    """

    unk_ptrs = [0x0CE9FC, 0x0CEA02, 0x0CEB3B]
    update_ptrs(rom, unk_ptrs, unk_start, unk_new_start)


def reassign_magic(rom, db, reassign):

    # Range starting at 0x3FF951 holds a PC's max tech level before magic
    # needs to be learned.  Only applies to menu drawing
    # Vanilla: 03 03 03 FF 03 FF 00
    # Note: Magus is 00 but also comes with magic learned initially.
    magic_thresh = rom[0x3FF951:0x3FF951+7]

    for i in range(7):
        reassign_pc_magic(reassign[i], i, rom, db, magic_thresh)


def reassign_pc_magic(from_ind, to_ind, rom, db, magic_thresh):

    # Change PC's needs-magic threshold
    rom[0x3FF951+to_ind] = magic_thresh[from_ind]

    # Here's a new wrinkle.  If the x80 bit of a tech is 0, then a tech will
    # be learned regardless of magic level.  So if we want to cap it at
    # exactly the value above, we have to write an x80 bit.

    # We also have to write 0 to that bit for all techs prior

    # Note, this means the change_magic routine must be run *after* all of the
    # techs are in place!

    tech_level = rom[0x3FF951+to_ind]

    # set techs before tech_level to not need magic
    for i in range(0, min(tech_level, 8)):
        ctl_start = (to_ind*8+i+1)*TechDB.control_size
        db.controls[ctl_start] &= 0x7F

    # set tech of tech_level and on to need magic
    for i in range(min(tech_level, 8), 8):
        ctl_start = (to_ind*8+i+1)*TechDB.control_size
        db.controls[ctl_start] |= 0x80

    # The intial setting of the magic-learned byte (0x7F01E0) needs to be
    # set from within a script in Telepod Exhibit

    # The script update is in cr_telepod_exhibit.flux and should already be
    # applied when this option is selected

    # I imagine there's a different patch needed for lost worlds?


def get_reassign_techdb(orig_db, reassign, dup_duals=False):
    # Make a db with the right menu/battle groups but no techs added yet
    new_db = max_expand_empty_db(orig_db, reassign, dup_duals)

    for i in range(7):
        change_single_techs(reassign[i], i, orig_db, new_db)
        change_basic_attacks(reassign[i], i, orig_db, new_db)

    update_dual_techs(orig_db, new_db, reassign, dup_duals)

    update_trip_techs(orig_db, new_db, reassign)

    # hardcode the new starts for the db here.  I have the free space manager
    # but integrating it with the rest of the randomizer is an ordeal.
    # Should be max 0xFE techs now?  Should never exceed 0x9A.

    new_db.control_start = 0x5F0000
    new_db.effect_start = 0x5F1000
    new_db.gfx_start = 0x5F2000
    new_db.target_start = 0x5f3000
    new_db.bat_grp_start = 0x5F3200
    new_db.menu_grp_start = 0x5F3500
    new_db.name_start = 0x5F4000

    # new_db.desc_new_start = 0x5F5100
    new_db.set_desc_start(0x5F5100)
    new_db.desc_ptr_start = 0x5F4600

    new_db.techs_learned_start = 0x4F0230

    new_db.set_lrn_req_start(0x5F6000)
    new_db.lrn_ref_start = 0x5F6200

    new_db.mp_start = 0x5F6400
    new_db.menu_req_start = 0x5F6500
    new_db.group_sizes_start = 0x5F6600

    # Added this later.  Squeezing it between controls and effects since I
    # way over allocated there.
    new_db.atb_pen_start = 0x5F0F00

    return new_db


def reassign_tech_refs(rom, db, reassign):

    update_rock_techs(rom, db, reassign)
    update_targetting(rom, db, reassign)

    # Change the ranged/melee specification
    # $C1/4A44 BF 3C F6 CC LDA $CCF63C,x[$CC:F6C4]
    # 01 - melee, 00 - ranged
    atk_range = rom[0x0CF63C:0x0CF63C+7]
    for i in range(7):
        from_ind = reassign[i]
        to_ind = i
        rom[0x0CF63C+to_ind] = atk_range[from_ind]

    # $C2/91B4 FC DB 91    JSR ($91DB,x)[$C2:0CA9]
    # These are pointers for damage formulas for the menu.  They do not seem
    # to be used for combat.  Power tabs boost Luno's atack in battle but not
    # on the menu.
    atk_forms = rom[0x0291DB:0x0291DB+7*2]
    atk_form_start = 0x0291DB

    for i in range(7):
        to_ind = i
        from_ind = reassign[i]

        to_start = atk_form_start+2*to_ind
        from_start = 2*from_ind
        rom[to_start:to_start+2] = atk_forms[from_start:from_start+2]


# Not needed anymore?  Functionality moved into get_reassign_techdb()
def reassign_techs(rom, db, new_db, reassign):

    # We need to keep unaltered pc data around.  Consider just ripping out the
    # needed bits instead.

    # Make a db with the right menu/battle groups but no techs added yet
    new_db = max_expand_empty_db(db, reassign)

    for i in range(7):
        change_single_techs(reassign[i], i, db, new_db)
        change_basic_attacks(reassign[i], i, db, new_db)

    update_rock_techs(rom, db, reassign)
    update_targetting(rom, db, reassign)


def change_pc_graphics(from_ind, to_ind,
                       rom,
                       orig_anim, anim_start, anim_new_start,
                       orig_unk, unk_start, unk_new_start,
                       orig_gfx, gfx_start,
                       orig_asm, asm_start,
                       really_unk,
                       atk_bytes, atk_byte_start):

    # Reassign gfx ptr -- 3 byte absolute pointer
    rom[gfx_start+3*to_ind:gfx_start+3*(to_ind+1)] = \
        orig_gfx[3*from_ind:3*(from_ind+1)]

    # Reassign sprite asm ptr -- 3 byte absolute pointer
    rom[asm_start+3*to_ind:asm_start+3*(to_ind+1)] = \
        orig_asm[3*from_ind:3*(from_ind+1)]

    # Reassign anim ptr -- 2 byte relative to bank 0x24
    rom[anim_start+2*to_ind:anim_start+2*(to_ind+1)] = \
        orig_anim[2*from_ind:2*(from_ind+1)]

    # The anim ptr in the next spot is used as an endpoint for the anim data
    # Copy this ptr into the same spot in the anim_new_start range
    rom[anim_new_start+2*(to_ind+1):anim_new_start+2*(to_ind+2)] = \
        orig_anim[2*(from_ind+1):2*(from_ind+2)]

    # Unconfirmed anim ptrs -- 2 byte relative to bank 0x24
    rom[unk_start+2*(to_ind):unk_start+2*(to_ind+1)] = \
        orig_unk[2*(from_ind):2*(from_ind+1)]

    # Again, the next ptr is used as an endpoint sometimes
    rom[unk_new_start+2*(to_ind+1):unk_new_start+2*(to_ind+2)] = \
        orig_unk[2*(from_ind+1):2*(from_ind+2)]

    # $C2/B4F0 BF 19 B5 C2 LDA $C2B519,x[$C2:B51A]
    # This is something loaded when processing graphics.  No idea what, but it
    # is pc-index specific.  X-Menu casting animations fail when this is unset
    rom[0x02B519+to_ind] = really_unk[from_ind]

    # Basic attack animation bytes
    # 3 bytes per char, but it goes in groups of 7
    for i in range(0, 3):
        to_byte = atk_byte_start + 7*i + to_ind
        from_byte = 7*i + from_ind

        rom[to_byte] = atk_bytes[from_byte]


# Every time a fight is initiated, the game checks Ayla's level and upgrades
# her fist if needed.  Now there can be many Aylas so we have to use the
# reassign list to check them all.
# 1) Write the reassign list somewhere in memory (0x4F1100)
# 2) Rewrite the Ayla checks (there are three, one per battle pc) to check
#    the reassign list instead of the raw pc_id.
def fix_ayla_fist(rom, reassign):
    # use the char assignment to determine who is Ayla
    rom[0x4F1100:0x4F1100+len(reassign)] = reassign[:]

    # Update the three pre-battle Ayla checks
    """
    $C1/FAC5 AD 2D 5E    LDA $5E2D  [$7E:5E2D]
    $C1/FAC8 C9 05       CMP #$05
    $C1/FACA D0 0A       BNE $0A    [$FAD6
    $C1/FACC 7B          TDC
    $C1/FACD AD 3F 5E    LDA $5E3F  [$7E:5E3F]
    $C1/FAD0 20 AE FD    JSR $FDAE  [$C1:FDAE]   lv/0x18 to get wpn index
    $C1/FAD3 8D 56 5E    STA $5E56  [$7E:5E56]

    $C1/FAC5 5C 10 11 4F    JMP $4F1110
    $C1/FAC9 EA             NOP
    $C1/FACA ---- Same as before

    $4F/1100 AD 2D 5E       LDA $5E2D
    $4F/1103 AA             TAX
    $4F/1104 BF 00 11 4F    LDA $4F1100,x
    $4F/1108 C9 05          CMP #05
    $4F/110A 5C CA FA C1    JMP $C1FACA
    """

    rom[0x01FAC5:0x01FAC5+5] = bytearray.fromhex('5C 10 11 4F EA')
    ayla_pc1 = bytearray.fromhex('AD 2D 5E' +
                                 'AA' +
                                 'BF 00 11 4F' +
                                 'C9 05' +
                                 '5C CA FA C1')
    rom[0x4F1110:0x4F1110+len(ayla_pc1)] = ayla_pc1

    # Other pcs are similar
    # pc2 - LDA $5EAD, pc3 - LDA $5F2D

    rom[0x01FADD:0x01FADD+5] = bytearray.fromhex('5C 20 11 4F EA')
    ayla_pc2 = bytearray.fromhex('AD AD 5E' +
                                 'AA' +
                                 'BF 00 11 4F' +
                                 'C9 05' +
                                 '5C E2 FA C1')

    rom[0x4F1120:0x4F1120+len(ayla_pc2)] = ayla_pc2

    rom[0x01FAF5:0x01FAF5+5] = bytearray.fromhex('5C 30 11 4F EA')
    ayla_pc3 = bytearray.fromhex('AD 2D 5F' +
                                 'AA' +
                                 'BF 00 11 4F' +
                                 'C9 05' +
                                 '5C FA FA C1')

    rom[0x4F1130:0x4F1130+len(ayla_pc3)] = ayla_pc3


# Repoint overworld sprites using reassign.
# This method needs access to the reassignment list on the rom.  Its location
# is given by reassign_start.
# This method also needs to write some new routines (~45 bytes).  These
# will be placed at rt_start.
def fix_overworld_sprites(rom, rt_start, reassign_start, reassign):

    """
    $7E2980, $7E2981, and $7E2982 have the pc-indices of the party.
    We just need to apply reassign[] to them.
    JSR $2BBC does the work.

    $C2/2B80 AF 80 29 7E LDA $7E2980[$7E:2980]
    $C2/2B84 A0 00 B0    LDY #$B000
    $C2/2B87 20 BC 2B    JSR $2BBC  [$C2:2BBC]
    $C2/2B8A AF 80 29 7E LDA $7E2980[$7E:2980]
    $C2/2B8E A0 00 BC    LDY #$BC00
    $C2/2B91 20 CF 2B    JSR $2BCF  [$C2:2BCF]
    $C2/2B94 AF 81 29 7E LDA $7E2981[$7E:2981]
    $C2/2B98 A0 00 B4    LDY #$B400
    $C2/2B9B 20 BC 2B    JSR $2BBC  [$C2:2BBC]
    $C2/2B9E AF 81 29 7E LDA $7E2981[$7E:2981]
    $C2/2BA2 A0 40 BC    LDY #$BC40
    $C2/2BA5 20 CF 2B    JSR $2BCF  [$C2:2BCF]
    $C2/2BA8 AF 82 29 7E LDA $7E2982[$7E:2982]
    $C2/2BAC A0 00 B8    LDY #$B800
    $C2/2BAF 20 BC 2B    JSR $2BBC  [$C2:2BBC]
    $C2/2BB2 AF 82 29 7E LDA $7E2982[$7E:2982]
    $C2/2BB6 A0 80 BC    LDY #$BC80
    $C2/2BB9 4C CF 2B    JMP $2BCF  [$C2:2BCF]
    """

    rt_write_ptr = to_rom_ptr(rt_start)

    if reassign_start is None:
        # Write the reassignment list before the routine
        reassign_start_ptr = to_rom_ptr(rt_start)
        # print('Writing reassign[] @ %X' % reassign_start_ptr)
        rom[reassign_start_ptr:reassign_start_ptr+len(reassign)] = \
            reassign[:]

        # Set the routine write pointer just after the reassignment list
        rt_write_ptr = to_rom_ptr(rt_start) + len(reassign)
    else:
        # Otherwise, do what the params say to do
        reassign_start_ptr = to_rom_ptr(reassign_start)
        rt_write_ptr = to_rom_ptr(rt_start)

    reassign_start_bytes = to_little_endian(reassign_start_ptr, 3)

    rt_start_ptr = rt_write_ptr
    rt_start_bytes = to_little_endian(rt_start_ptr, 3)

    pc1_call = bytearray.fromhex('22' + rt_start_bytes.hex())
    pc1_rt = bytearray.fromhex('AF 80 29 7E 29 FF 00 DA AA BF'
                               + reassign_start_bytes.hex()
                               + 'FA 6B')

    rt_start_ptr += len(pc1_rt)
    rt_start_bytes = to_little_endian(rt_start_ptr, 3)

    pc2_call = bytearray.fromhex('22' + rt_start_bytes.hex())
    pc2_rt = bytearray.fromhex('AF 81 29 7E 29 FF 00 DA AA BF'
                               + reassign_start_bytes.hex()
                               + 'FA 6B')

    rt_start_ptr += len(pc2_rt)
    rt_start_bytes = to_little_endian(rt_start_ptr, 3)

    pc3_call = bytearray.fromhex('22' + rt_start_bytes.hex())
    pc3_rt = bytearray.fromhex('AF 82 29 7E 29 FF 00 DA AA BF'
                               + reassign_start_bytes.hex()
                               + 'FA 6B')

    # write_start was set at the very start
    rom[rt_write_ptr:rt_write_ptr+len(pc1_rt)+len(pc2_rt)+len(pc3_rt)] = \
        (pc1_rt[:]+pc2_rt[:]+pc3_rt[:])

    rom[0x022B80:0x022B80+4] = pc1_call[:]
    rom[0x022B8A:0x022B8A+4] = pc1_call[:]
    rom[0x022B94:0x022B94+4] = pc2_call[:]
    rom[0x022B9E:0x022B9E+4] = pc2_call[:]
    rom[0x022BA8:0x022BA8+4] = pc3_call[:]
    rom[0x022BB2:0x022BB2+4] = pc3_call[:]


def fix_menu_graphics(rom, reassign, rt_addr=0x5F75D0):
    # fix menu magic type picture
    # $C2/A27C BF C6 A2 C2 LDA $C2A2C6,x[$C2:A2C6]
    # X has the pc-index which needs to be reeassigned

    rt_addr_bytes = to_little_endian(to_rom_ptr(rt_addr), 3)
    call = bytearray.fromhex('22' + rt_addr_bytes.hex())

    # rt is LDA from pc-index and then the LDA above
    # hardcoded reassign in 0x5F7580.  Sure why not?
    rt = bytearray.fromhex('BF 80 75 5F AA BF C6 A2 C2 6B')

    rom[0x02A27C:0x02A27C+4] = call[:]
    rom[rt_addr:rt_addr+len(rt)] = rt[:]

    # Change menu portrait (not palette)
    portrait_start = 0x3F0000
    portrait_size = 0x480

    portraits = rom[portrait_start:portrait_start+7*portrait_size]

    for i in range(7):
        from_ind = reassign[i]
        to_ind = i

        from_port_start = from_ind*portrait_size
        to_port_start = portrait_start+to_ind*portrait_size

        rom[to_port_start:to_port_start+portrait_size] = \
            portraits[from_port_start:from_port_start+portrait_size]

    # TODO: fix weapon image in stats block


# Sometimes the palettes are really ugly when you make a swap.  We'll try to
# manually fix them up.  The list of fixes will change with feedback.
def fix_palettes(rom, reassign):

    # SNES color format: 5 bits per color, bgr order, leading bit unset
    # 0bbb bbgg gggr rrrr

    # PC palettes have 12 colors, so 24 bytes total.

    pal_start = 0x240000
    pal_size = 24

    pals = \
        [rom[pal_start+i*pal_size:pal_start+(i+1)*pal_size] for i in range(7)]

    cr_st = pal_start
    mg_st = pal_start+6*pal_size
    ma_st = pal_start + pal_size
    lu_st = pal_start + 2*pal_size

    # The biggest issue is that lucca's bright pink hair occurs in in a slot
    # that is dark for everyone else.  It is in slot 11, and the color right
    # before is dark, so we'll just copy that one over.
    if reassign[2] == 6:
        # It's not perfect, but at least he has flowing pink hair now.
        rom[lu_st+4*2:lu_st+5*2] = pals[2][10*2:11*2]
        rom[lu_st+5*2:lu_st+6*2] = pals[2][8*2:9*2]
        rom[lu_st+9*2:lu_st+10*2] = pals[2][4*2:5*2]
        rom[lu_st+8*2:lu_st+9*2] = pals[2][6*2:7*2]
        rom[lu_st+6*2:lu_st+7*2] = pals[2][5*2:6*2]
        rom[lu_st+10*2:lu_st+11*2] = pals[2][11*2:12*2]
    elif reassign[2] == 0:
        rom[lu_st+4*2:lu_st+5*2] = pals[2][10*2:11*2]
        rom[lu_st+5*2:lu_st+6*2] = pals[2][8*2:9*2]
        rom[lu_st+6*2:lu_st+7*2] = pals[2][5*2:6*2]
        rom[lu_st+7*2:lu_st+8*2] = pals[2][4*2:5*2]
        rom[lu_st+8*2:lu_st+9*2] = pals[2][7*2:8*2]
        #rom[lu_st+9*2:lu_st+10*2] = pals[2][6*2:7*2]
        rom[lu_st+10*2:lu_st+11*2] = pals[2][9*2:10*2]
    elif reassign[2] == 5:
        rom[lu_st+4*2:lu_st+5*2] = pals[2][10*2:11*2]
        # rom[lu_st+5*2:lu_st+6*2] = pals[2][8*2:9*2]
        rom[lu_st+5*2:lu_st+6*2] = to_little_endian(0x5D37, 2)
        rom[lu_st+6*2:lu_st+7*2] = pals[2][8*2:9*2]
        rom[lu_st+7*2:lu_st+8*2] = pals[2][9*2:10*2]

        rom[lu_st+8*2:lu_st+9*2] = pals[2][5*2:5*2]
        rom[lu_st+9*2:lu_st+10*2] = pals[2][6*2:8*2]

        rom[lu_st+10*2:lu_st+11*2] = pals[2][9*2:10*2]
    elif reassign[2] == 1:
        # Hair
        rom[lu_st+4*2:lu_st+5*2] = pals[6][1*2:2*2]  # light
        rom[lu_st+5*2:lu_st+6*2] = pals[2][10*2:11*2]    # mid
        rom[lu_st+6*2:lu_st+7*2] = pals[2][8*2:9*2]   # dark
        rom[lu_st+7*2:lu_st+8*2] = pals[2][9*2:10*2]   # darkest

        # Tunic
        rom[lu_st+8*2:lu_st+9*2] = pals[2][4*2:5*2]
        rom[lu_st+9*2:lu_st+10*2] = pals[2][7*2:8*2]
        rom[lu_st+10*2:lu_st+11*2] = pals[2][6*2:7*2]
    elif reassign[2] == 3:
        rom[lu_st+4*2:lu_st+5*2] = pals[2][10*2:11*2]
        rom[lu_st+5*2:lu_st+6*2] = pals[2][8*2:9*2]
        rom[lu_st+10*2:lu_st+11*2] = pals[2][9*2:10*2]
        rom[lu_st+9*2:lu_st+10*2] = pals[2][7*2:8*2]
        rom[lu_st+7*2:lu_st+8*2] = pals[2][4*2:5*2]

        rom[lu_st+6*2:lu_st+7*2] = pals[2][5*2:6*2]
        rom[lu_st+8*2:lu_st+9*2] = pals[2][6*2:7*2]
    elif reassign[2] != 2:
        pals[2][10*2:11*2] = pals[2][9*2:10*2]
        rom[pal_start+2*pal_size:pal_start+3*pal_size] = pals[2][:]

    # When Crono becomes Marle, there are a few problems.
    #  (1) The light blue in Crono's shirt (#7) becomes the outline of Marle's
    #      face.
    #  (2) The tan color of Crono's pants gets put into Marle's hair. Marle
    #      uses 3 colors for hair while Crono only uses two.

    if reassign[0] == 1:
        # Make a dark Crono color the Marle face outline
        rom[pal_start + 2*7:pal_start + 2*8] = pals[0][10*2:11*2]

        # Use a dark red from Marle's palette as the missing dark red from
        # Crono's palette since he only has two hair colors
        rom[pal_start+2*6:pal_start+2*7] = pals[1][7*2:8*2]

        # Move the light blue of Crono's shirt to Marle's clothes shadow
        rom[pal_start+2*8:pal_start+2*11] = pals[0][7*2:10*2]
    elif reassign[0] == 5:
        rom[cr_st+8*2:cr_st+11*2] = pals[0][7*2:10*2]
        rom[cr_st+7*2:cr_st+8*2] = pals[0][10*2:11*2]
        rom[cr_st+2*6:cr_st+2*7] = pals[1][7*2:8*2]

    if reassign[1] == 0:
        # shirt color
        rom[ma_st+7*2:ma_st+10*2] = pals[1][8*2:11*2]

        rom[ma_st+10*2:ma_st+11*2] = pals[1][7*2:8*2]

        # hair color shift to remove the lightest color
        rom[ma_st+4*2:ma_st+6*2] = pals[1][5*2:7*2]

        # pants
        rom[ma_st+6*2:ma_st+7*2] = pals[1][4*2:5*2]

    if reassign[6] == 0:
        # shirt color
        rom[mg_st+7*2:mg_st+10*2] = pals[6][8*2:11*2]

    # Many of the character portraits are gross but they require more care.


def reassign_graphics(rom, anim_new_start, unk_new_start, reassign):

    # Copy pointer tables when needed.  Update some references to the tables
    copy_update_graphics_ptrs(rom, anim_new_start, unk_new_start, reassign)

    # 242600	242783	PTR	N	"Pointers to character animations (?)
    anim_start = 0x242600
    anim_end = 0x242784
    anim_ptrs = rom[anim_start:anim_end]

    # 242800	242983	PTR	N	"Pointers to unconfirmed animation data
    unk_start = 0x242800
    unk_end = 0x242984
    unk_ptrs = rom[unk_start:unk_end]

    # Normal walk/run sprite indices are at 0x24F000
    # These end up not needing any change once the other data is reassigned
    # sprite_start = 0x24F000
    # sprite_size = 0x5
    # sprites = rom[sprite_start:sprite_start+7*sprite_size]

    # gfx for battle -- 3 byte absolute pointers
    gfx_start = 0x242000
    gfx_size = 0x3
    gfx_ptrs = rom[gfx_start:gfx_start+gfx_size*7]

    # sprite asm for battle -- 3 byte absolute pointers
    asm_start = 0x242300
    asm_size = 0x3
    asm_ptrs = rom[asm_start:asm_start+asm_size*7]

    # $C2/B4F0 BF 19 B5 C2 LDA $C2B519,x[$C2:B51A]
    # This is something loaded when processing graphics.  No idea what, but it
    # is pc-index specific.  X-Menu casting animations fail when this is unset
    really_unk = rom[0x02B519:0x02B519+7]

    # $C1/4328 FC 63 7A    JSR ($7A63,x)[$C1:432C]
    # This is routine for attacks.  Looks like basic attacks and techs get
    # different routines.

    # It looks like each char has three sets of gfx for melee/ranged/crit
    atk_byte_start = 0x0D4000
    # 3 bytes per char, but it goes in groups of 7
    atk_byte_size = 3
    atk_bytes = rom[atk_byte_start:atk_byte_start+7*atk_byte_size]

    # If a player is killed by an attack, there is a little script that says
    # what animations to play.  After days of searching, I finally found how
    # it gets loaded.
    """
    $C1/417A AD 81 29    LDA $2981  [$7E:2981]
    $C1/417D 0A          ASL A
    $C1/417E 0A          ASL A
    $C1/417F 18          CLC
    $C1/4180 6D DC 96    ADC $96DC  [$7E:96DC]
    $C1/4183 AA          TAX
    $C1/4184 BF 42 5F D1 LDA $D15F42,x[$D1:5F57]

    The above snippet is for the second party member ($2981).  The index is
    multiplied by 4 and then an offset ($96DC) is taken from within those four
    bytes.
    """

    pc_scripts = rom[0x115F42:0x115F42+4*7]

    for i in range(7):
        start = 0x115F42 + 4*i
        j = reassign[i]
        rom[start:start+4] = pc_scripts[4*j:4*(j+1)]

    for i in range(7):
        change_pc_graphics(reassign[i], i, rom,
                           anim_ptrs, anim_start, anim_new_start,
                           unk_ptrs, unk_start, unk_new_start,
                           gfx_ptrs, gfx_start,
                           asm_ptrs, asm_start,
                           really_unk,
                           atk_bytes, atk_byte_start)

    # Live with a copy of reassign in rom.  Set its start to None.
    # Again, we need a free space manager object...
    # Ok, I have a free space manager that sort of works, but making it work
    # with the rest of the randomizer is dicey.
    fix_overworld_sprites(rom, 0x5F7580, None, reassign)
    fix_palettes(rom, reassign)

    # Random thing I found while finding a vanilla bug:
    # $CC/E60B C9 06       CMP #$06
    # $CC/E60D D0 06       BNE $06    [$E615]
    # $CC/E60F 8E 15 A1    STX $A115  [$7E:A115]
    # $CC/E612 EE 17 A1    INC $A117  [$7E:A117]
    # This is recording when Magus is in the party to try to keep the 'Tech'
    # and 'Comb' text correct.  It still doesn't work in vanilla, but for
    # dup chars we should remove the magus check

    # New:
    # $CC/E60B EA          NOP
    # $CC/E60C EA          NOP
    # $CC/E60D 80 06       BRA $06    [$E615]

    rom[0x0CE60B:0x0CE60B+3] = bytearray.fromhex('EA EA 80')

    # TODO: Fix this bug completely.
    # The game stores whether a battle pc has any dual techs in a 3 byte range
    # beginning at 0x7E9F25.
    # We just need to catch when there's exactly one non-dual haver, store
    # their index in $7EA115 and put a 1 in $7eA115...later.

    # Break in the code at
    # $CC/E780 7B          TDC
    # $CC/E781 AA          TAX
    # $CC/E782 86 80       STX $80
    # $CC/E784 86 82       STX $82
    # $CC/E786 64 82       STZ $82
    # $CC/E788 64 8C       STZ $8C
    # $CC/E78A A5 83       LDA $83
    # Just setting up the next part of whatever it's doing after setting the
    # $9F25 range.  This is where I will strike.


def reassign_items(rom, reassign):

    item_dat = rom[0x0C06A4:0x0C0A1C]
    item_start = 0x0C06A4
    acc_dat = rom[0x0C0A1C:0x0C0ABC]
    acc_start = 0x0C0A1C

    for i in range(7):
        change_items(reassign[i], i, rom,
                     item_dat, item_start,
                     acc_dat, acc_start)


# The game limits you to 0x7F techs.  As far as I can tell, the only
# real issue is when building the battle menu.  The game wants to test if
# a value is 0xFF but instead checks if a value is negative so it catches
# 0x80 and up.
# Basically we just replace a bunch of BMI (branch minus) with CMP 0xFF, BEQ
def extend_techs(rom):
    # $CC/E75B BF 95 F3 CC LDA $CCF395,x
    # $CC/E75F 85 80       STA $80
    # $CC/E761 BF 96 F3 CC LDA $CCF396,x
    # $CC/E765 85 81       STA $81
    # $CC/E767 A6 80       LDX $80
    # $CC/E769 BD C6 1A    LDA $1AC6,x
    # $CC/E76C 30 05       BMI $05    [$E773]
    # $CC/E76E A9 01       LDA #$01
    # $CC/E770 99 25 9F    STA $9F25,y
    # $CC/E773 BD FE 1A    LDA $1AFE,x  # Trip tech spot of menu
    # $CC/E776 30 05       BMI $05      # should be CMP #$FF, BEQ
    # $CC/E778 A9 01       LDA #$01
    # $CC/E77A 99 28 9F    STA $9F28,y
    # $CC/E77D 88          DEY          # Should return here

    # This BMI needs to be CMP #$FF, BEQ $05
    rom[0x0CE75B:0x0CE75B+4] = bytearray.fromhex('5C 00 F0 5F')
    
    rt = bytearray.fromhex('BF 95 F3 CC' +
                           '85 80' +
                           'BF 96 F3 CC' +
                           '85 81' +
                           'A6 80' +
                           'BD C6 1A' +
                           '30 05' +
                           'A9 01' +
                           '99 25 9F' +
                           'BD FE 1A' +
                           'C9 FF' +        # CMP #$FF
                           'F0 05' +
                           'A9 01' +
                           '99 28 9F' +
                           '5C 7D E7 CC')    # JMP back to the DEY (see above)

    rom[0x5FF000:0x5FF000+len(rt)] = rt[:]
    # TODO:  See if there's a way to save 2 stupid bytes to avoid jumping.

    '''
    Same story as above
    $CC/E887 BF 95 F3 CC LDA $CCF395,x
    $CC/E88B 85 84       STA $84
    $CC/E88D BF 96 F3 CC LDA $CCF396,x
    $CC/E891 85 85       STA $85
    $CC/E893 A6 84       LDX $84
    $CC/E895 BD FE 1A    LDA $1AFE,x
    $CC/E898 99 D0 94    STA $94D0,y
    $CC/E89B 30 05       BMI $05    [$E8A2]
    $CC/E89D A9 12       LDA #$12
    $CC/E89F 99 51 95    STA $9551,y
    $CC/E8A2 E6 83       INC $83
    '''

    rt2_st = 0x5FF000 + len(rt)
    rt2_st_b = to_little_endian(rt2_st, 3)
    rom[0x0CE887:0x0CE887+4] = bytearray.fromhex('5C'+rt2_st_b.hex())
    rt2 = bytearray.fromhex('BF 95 F3 CC 85 84 BF 96 F3 CC 85 85 A6 84' +
                            'BD FE 1A 99 D0 94' +
                            'C9 FF F0 05' +
                            'A9 12 99 51 95' +
                            '5C A2 E8 CC')
    rom[rt2_st:rt2_st+len(rt2)] = rt2[:]

    '''
    $C2/BD9A E2 20       SEP #$20
    $C2/BD9C AD 4C 0F    LDA $0F4C
    $C2/BD9F 30 05       BMI $05    [$BDA6]
    '''

    rt3_st = rt2_st+len(rt2)
    rt3_st_b = to_little_endian(rt3_st, 3)
    rom[0x02BD9A:0x02BD9A+4] = bytearray.fromhex('5C' + rt3_st_b.hex())
    rom[0x02BD9F] = 0xF0

    rt3 = bytearray.fromhex('E2 20 AD 4C 0F' +
                            'C9 FF' +
                            '5C 9F BD C2')

    rom[rt3_st:rt3_st+len(rt3)] = rt3[:]


def reassign_characters_file(filename, char_choices, dup_duals,
                             tech_rando_type, lost_worlds):
    with open(filename, 'rb') as infile:
        rom = bytearray(infile.read())

    extend_techs(rom)

    reassign = [random.choice(char_choices[i]) for i in range(7)]
    reassign_characters(rom, reassign, dup_duals, tech_rando_type, lost_worlds)

    with open(filename, 'wb') as outfile,\
         open('patches/chardup_telepod_patch.ips', 'rb') as telepod_patch,\
         open('patches/chardup_spekkio_patch.ips', 'rb') as spek_patch:

        outfile.write(rom)
        ipswriter.write_patch_objs(telepod_patch, outfile)

        if not lost_worlds:
            ipswriter.write_patch_objs(spek_patch, outfile)


# Do everything to apply the reassignment list to the rom
# Assume db is created from get_reassign_techdb with the provided reassign list
def reassign_characters(rom, reassign, dup_duals,
                        tech_rando_type, lost_worlds):

    # print(reassign)

    # Technically we can do this regardless...Maybe when we're sure it works!
    if dup_duals:
        scripts.script_extend(rom, 0x5F8100, 0x5F8200)
        scripts.add_dup_dual_scripts(rom, 0x5F8100, 0x5F8200, 0x5F8400)

    orig_db = TechDB.get_default_db(rom)

    new_db = get_reassign_techdb(orig_db, reassign, dup_duals)

    reassign_tech_refs(rom, new_db, reassign)
    reassign_magic(rom, new_db, reassign)

    reassign_graphics(rom, 0x5F7000, 0x5F7200, reassign)
    fix_menu_graphics(rom, reassign)

    reassign_stats(rom, reassign)
    fix_ayla_fist(rom, reassign)

    reassign_items(rom, reassign)

    if tech_rando_type == "Fully Random":
        techrandomizer.randomize_single_techs_uniform(new_db)
    elif tech_rando_type == "Balanced Random":
        techrandomizer.randomize_single_techs_balanced(new_db)

    # Nuke the old db to make sure we're using only newly written data
    TechDB.write_db_ff_internal(orig_db, rom)

    TechDB.write_db_internal(new_db, rom)

    # Script things here for now.  Consolidate later.

    # In King's Trial (Loc 0x1B6, Loc Event 0x60) Marle does animation A8
    # I believe this kiss animation is only held by girls.  We're going to
    # change it to something else for non-Marle in spot 1.

    if reassign[1] != 1:
        rom[0x36F1F2] = 0x1A  # Should be laughing now

    

    # Probably need one for Frog cutting the mountain.


# Main
if __name__ == '__main__':

    # jets_test.sfc should be a JoT rom with NOTHING extra done to techs
    # No unlocked magic (but this might be OK) and definitely no tech
    # randomization (but I might have fixed the techdb so this is OK).
    with open('jets_test.sfc', 'rb') as infile:
        rom = bytearray(infile.read())

    orig_db = TechDB.get_default_db(rom)

    x = get_ct_name('FlexgonMist')
    print_bytes(x, 16)
    
    quit()
    # orig_db = TechDB.db_from_rom_internal(rom)

    random.seed(1234567890)
    reassign = [random.randrange(0, 7) for i in range(7)]

    # print(reassign)
    # reassign[2] = 1

    new_db = get_reassign_techdb(orig_db, dup_duals, reassign)

    # These actually do some work on the rom to fix references
    reassign_tech_refs(rom, new_db, reassign)
    # update_rock_techs(rom, new_db, reassign)
    # update_targetting(rom, new_db, reassign)

    # reassign magic is out of the tech_db because it influences the rom
    reassign_magic(rom, new_db, reassign)

    reassign_graphics(rom, 0x5F7000, 0x5F7200, reassign)
    fix_menu_graphics(rom, reassign)

    reassign_stats(rom, reassign)

    # techrandomizer.randomize_single_techs_uniform(new_db)

    TechDB.write_db_internal(new_db, rom)

    # quick dirty hack to kill ATB delay
    # new_rom[0x01BDF5:0x01BDF5+4] = bytearray.fromhex('A9 00 EA EA')
    # new_rom[0x01BE71:0x01BE71+4] = bytearray.fromhex('A9 00 EA EA')
    # new_rom[0x01BEEE:0x01BEEE+4] = bytearray.fromhex('A9 00 EA EA')

    # print_bytes(new_db.lrn_reqs, 9)
    # print_bytes(new_db.lrn_refs, 5)
    # print_bytes(new_db.menu_grps, 16)

    with open('jets_test-out.sfc', 'wb') as outfile:
        outfile.write(rom)
