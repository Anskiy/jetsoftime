from byteops import get_record
from techdb import TechDB
import copy
import random


# generate a random permutation where each object has a different probability
# of being drawn.
# Uniform distribution is [1,1,1,....,1]
def generate_permutation_freq(rel_freqs):

    perm = [0]*len(rel_freqs)
    for i in range(len(rel_freqs)):
        perm[i] = i

    for start in range(0, len(rel_freqs)-1):
        N = sum(rel_freqs[start:])
        x = random.randrange(1, N+1)

        for i in range(start, len(rel_freqs)):
            x -= rel_freqs[i]
            if x <= 0:
                perm[start], perm[i] = perm[i], perm[start]
                rel_freqs[start], rel_freqs[i] = rel_freqs[i], rel_freqs[start]
                break

    return perm


def randomize_single_techs_uniform(db):

    freqs = [1]*8

    for i in range(7):
        perm = generate_permutation_freq(freqs)
        randomize_pc_techs(db, i, perm)


def randomize_single_techs_balanced(db):
    freqs = [[8, 7, 6, 4, 3, 5, 1, 2],
             [7, 8, 6, 5, 1, 2, 3, 4],
             [8, 4, 6, 5, 7, 2, 3, 1],
             [8, 7, 6, 2, 3, 1, 5, 4],
             [8, 6, 7, 1, 3, 2, 4, 5],
             [8, 7, 5, 2, 6, 4, 3, 1],
             [5, 5, 5, 3, 7, 2, 8, 1]]

    for i in range(7):
        perm = generate_permutation_freq(freqs[i])
        randomize_pc_techs(db, i, perm)


def randomize_pc_techs(db, char_id, perm, preserve_magic=True):
    # Shuffle everything goes goes with tech_id: gfx, target, name, desc_ptr,
    #   effect, mp, atb_pen
    # Fix pointers to effect headers in control headers
    # Shuffle menu usability
    # Update effect indices in control headers
    # Update lrn_reqs
    # Update menu_mp_reqs

    dat = [db.effects, db.mps,
           db.controls,
           db.gfx,
           db.targets,
           db.names,
           db.desc_ptrs,
           db.menu_usable_ids,
           db.pc_target,
           db.atb_pens]

    sizes = [TechDB.effect_size, 1,
             TechDB.control_size,
             TechDB.gfx_size,
             TechDB.target_size,
             TechDB.name_size,
             TechDB.desc_ptr_size,
             1,
             1,
             1]

    temp_dat = copy.deepcopy(dat)

    # shuffle it all up!  PC's tech #i to goes to #perm[i]
    for i in range(0, 8):
        to_ind = 1+8*char_id + perm[i]
        from_ind = 1+8*char_id + i

        for j in range(0, len(dat)):
            x = get_record(temp_dat[j], from_ind, sizes[j])
            dat[j][to_ind*sizes[j]:(to_ind+1)*sizes[j]] = x[:]

    if preserve_magic:
        # Copy the old first bytes back to the new control headers.
        # Technically we only need the x80 (magic) bit, but the first byte
        # of the hearder is just (magic_bit | pc_ind) for single techs
        old_controls = temp_dat[2]
        ctl_start = (1+8*char_id)*TechDB.control_size

        for i in range(8):
            db.controls[ctl_start+TechDB.control_size*i] = \
                old_controls[ctl_start+TechDB.control_size*i]

    # update effect indices in control headers
    eff_min = 1+8*char_id
    eff_max = eff_min + 7
    for i in range(0, db.control_count):
        # bytes 5,6,7 are effect indices
        ctl_start = i*TechDB.control_size
        for j in range(5, 8):
            eff = db.controls[ctl_start+j]
            eff_x80 = eff & 0x80
            eff_ind = eff & 0x7F

            if eff_min <= eff_ind <= eff_max:
                new_ind = perm[eff_ind - eff_min]+eff_min
                db.controls[ctl_start+j] = eff_x80 | new_ind

    # update lrn_reqs
    # look through menu grps for the pc of interest.  Figure out where they
    # are in the lrn_req list, and apply perm
    char_bit = 0x80 >> char_id
    for i in range(db.first_dual_grp, db.first_rock_grp):
        if db.menu_grps[i] & char_bit != 0:
            # our pc is in the menu group
            grp = db.menu_grps[i]

            num_chars = 0
            mask = 0x80
            pos = 0

            for j in range(0, 8):
                if mask & grp != 0:
                    if j == char_id:
                        pos = num_chars
                    num_chars += 1
                mask = mask >> 1

            size = 0
            if num_chars == 2:
                size = 3
            else:
                size = 1

            start_tech = db.group_sizes[i]
            lrn_loc = (start_tech-0x39)*TechDB.lrn_req_size+pos

            for tech in range(start_tech, start_tech+size):
                tech_lrn_start = (tech-0x39)*TechDB.lrn_req_size
                lrn_loc = tech_lrn_start+pos
                db.lrn_reqs[lrn_loc] = perm[db.lrn_reqs[lrn_loc]-1]+1

    # update menu_mp_reqs for triple techs (and menu if that ever works)
    for (i, x) in enumerate(db.menu_mp_reqs):
        pc = (x-1) % 8
        if pc == char_id:
            tech_num = (x-1) // 8
            tech_num = perm[tech_num]
            db.menu_mp_reqs[i] = pc*8+tech_num+1

    # Is that it?


if __name__ == '__main__':

    # test.sfc should be a CT rom without any tech randomization
    # The only thing that breaks if the techs are already randomized is that
    # the menu-usable techs will be broken
    with open('test.sfc', 'r+b') as infile, \
         open('test-out.sfc', 'wb') as outfile:
        rom = bytearray(infile.read())
        db = TechDB.get_default_db(rom)

        random.seed(12345)
        randomize_single_techs_balanced(db)
        TechDB.write_db_internal(db, rom)

        # print_bytes(db.controls, TechDB.control_size)

        outfile.write(rom)
