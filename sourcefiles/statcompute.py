from byteops import get_value_from_bytes, to_little_endian, print_bytes
import copy

# Methods for computing character stats at different levels


class PCStats:
    hp_grw_len = 8
    mp_grw_len = 8
    stat_grw_len = 7
    tp_thr_len = 0x10

    pc_ind_off = 0x0
    pc_ind_len = 1

    # Element, (WW: human/female/physicalatk)
    pc_flags_off = 0x01
    pc_flags_len = 1

    cur_hp_off = 0x3
    cur_hp_len = 2

    max_hp_off = 0x5
    max_hp_len = 2

    cur_mp_off = 0x7
    cur_mp_len = 2

    max_mp_off = 0x9
    max_mp_len = 2

    #  Cur Order: Pow, Sta, Spd, Mag, Hit, Evd, Mdf
    cur_stat_off = 0xB
    cur_stat_len = 7

    # individual stat offsets?

    lvl_off = 0x12
    lvl_len = 1

    xp_off = 0x13
    xp_len = 3

    # It looks like 0x16, 0x17 are storing total TP earned?
    # I don't think it's used in game though.
    # Interestingly, it's not counting with the double tech point bug.  It just
    # adds the TP earned in a fight to this value.

    # 0x18 through 0x26 seem to be unused.  They are 00 at game start and still
    # 00 at lavos fight, but I haven't played a game with a watch on them.
    # Warrior Workshop indicates statuses are stored in 0x24 - 0x26

    helm_off = 0x27
    helm_len = 1

    armor_off = 0x28
    armor_len = 1

    wpn_off = 0x29
    wpn_len = 0x29

    acc_off = 0x2A
    acc_len = 1

    xp_next_off = 0x2B
    xp_next_len = 2

    tp_next_off = 0x2D
    tp_next_len = 2

    # Base Order: Pow, Sta, Spd, Hit, Evd, Mag, Mdf
    base_stat_off = 0x2F
    base_stat_len = 7

    # For our purposes, this is where we stop.  The rest of the stat block is
    # computed at run time

    # The next block seems to be current stats + equip effects
    # Order(?): Pow, Sta, Spd, Mag, Hit, Evd, Mdf (same as cur)
    eqp_stat_off = 0x36
    eqp_stat_len = 7

    atk_off = 0x3D
    def_len = 1

    def_off = 0x3E
    def_len = 1

    # hp/mp with current gear (earring)
    eqp_hp_off = 0x3F
    eqp_hp_len = 2

    # 0x41 - 0x4F are unknown right now.  They are only populated when a PC
    # joins the party, so they aren't really a concern right now.
    # I *DO* need to check that multiple copies with identical stats generate
    # the same values here.
    # Look like some sort of animation pointers... some activated on attack.

    def __init__(self, stat_block,
                 hp_growth, mp_growth, stat_growth,
                 tech_level,
                 tp_thresh, xp_thresh):

        self.stat_block = stat_block[:]
        self.hp_growth = hp_growth[:]
        self.mp_growth = mp_growth[:]
        self.stat_growth = stat_growth[:]

        self.tech_level = tech_level

        # self.tp_thresh = tp_thresh[:]
        self.tp_thresh = []
        for i in range(0, len(tp_thresh), 2):
            cur = tp_thresh[i:i+2]
            self.tp_thresh.append(get_value_from_bytes(cur))

        # self.xp_thresh = xp_thresh[:]
        self.xp_thresh = []
        for i in range(0, len(xp_thresh), 2):
            cur = xp_thresh[i:i+2]
            self.xp_thresh.append(get_value_from_bytes(cur))

        self.__extract_stats()

    def stats_from_rom_default(rom, pc_ind):
        return PCStats.stats_from_rom(rom, pc_ind,
                                      0x0C0000,
                                      0x0C258A, 0x0C25C2, 0x0C25FA,
                                      0x0C2632, 0x0C26FA)

    def stats_from_rom(rom, pc_ind,
                       stat_start,
                       hp_growth_start, mp_growth_start, stat_growth_start,
                       xp_thresh_start, tp_thresh_start):

        stat_block = \
            rom[stat_start+0x50*pc_ind:stat_start+(pc_ind+1)*0x50]
        hp_growth = \
            rom[hp_growth_start+pc_ind*8:hp_growth_start+(pc_ind+1)*8]
        mp_growth = \
            rom[mp_growth_start+pc_ind*8:mp_growth_start+(pc_ind+1)*8]
        stat_growth = \
            rom[stat_growth_start+pc_ind*7:stat_growth_start+(pc_ind+1)*7]
        xp_thresh = rom[xp_thresh_start:xp_thresh_start+99*2]
        tp_thresh = \
            rom[tp_thresh_start+16*pc_ind:tp_thresh_start+16*(pc_ind+1)]

        tech_level = rom[stat_start+0x230+pc_ind]

        return PCStats(stat_block, hp_growth, mp_growth, stat_growth,
                       tech_level,
                       tp_thresh, xp_thresh)

    # Wrote most of this before defining the PCStats.offsets/lengths
    # Maybe rewrite for clarity
    def __extract_stats(self):
        self.base_stats = self.stat_block[0x2F:0x2F+7]
        self.cur_stats = self.stat_block[0xB:0xB+7]
        self.level = self.stat_block[0x12]

        self.max_hp = get_value_from_bytes(self.stat_block[0x05:0x05+2])
        self.base_hp = \
            self.max_hp - compute_hpmp_growth(self.hp_growth, self.level)

        self.max_mp = get_value_from_bytes(self.stat_block[0x09:0x09+2])
        self.base_mp = \
            self.max_mp - compute_hpmp_growth(self.mp_growth, self.level)

        self.xp_next = \
            get_value_from_bytes(self.stat_block[0x2B:0x2B+2])

        off = PCStats.xp_off
        size = PCStats.xp_len
        self.xp = \
            get_value_from_bytes(self.stat_block[off:off+size])

        if self.xp_next != self.xp_thresh[self.level]:
            print('Warning. xp_thresh does not match stat block')

        self.tp_next = \
            get_value_from_bytes(self.stat_block[0x2D:0x2D+2])

    def set_tech_level(self, new_level):
        self.tech_level = new_level

        if new_level == 8:
            self.tp_next = 0
        else:
            self.tp_next = self.tp_thresh[new_level]

    def set_level(self, new_level):

        # modify stats
        grown_stats = grow_stats(self.base_stats, self.stat_growth, new_level)

        # Speed is not handled normally.  Base and growth are 0.  The current
        # value is kept.
        grown_stats[2] = self.cur_stats[2]
        self.cur_stats = get_stat_cur_order(grown_stats)

        # modify hp
        self.max_hp = \
            compute_new_hpmp(self.level, self.max_hp,
                             self.hp_growth, new_level)
        # self.cur_hp = self.max_hp

        # modify mp
        self.max_mp =\
            compute_new_hpmp(self.level, self.max_mp,
                             self.mp_growth, new_level)
        # self.cur_mp = self.max_mp

        # xp to next level
        if new_level == 99:
            self.xp_next = 0
        else:
            self.xp_next = self.xp_thresh[new_level]

        # set total xp as sum of previous xp_thresh values
        self.xp = sum(self.xp_thresh[i] for i in range(0, new_level))

        # actually change the level...
        self.level = new_level

    def print_data(self):
        self.__update_statblock()
        print('Stat Block:')
        print_bytes(self.stat_block, 16)
        print('Base Stats:')
        print('Pow Stm Spd Hit Evd Mag Mdf')
        print(*[' %2.2X' % x for x in self.base_stats])
        print(*[' %2.2d' % x for x in self.base_stats])

        print('Cur Stats:')
        print('Pow Stm Spd Hit Evd Mag Mdf')
        temp_cur = get_stat_base_order(self.cur_stats)
        print(*[' %2.2X' % x for x in temp_cur])
        print(*[' %2.2d' % x for x in temp_cur])

        print('Max HP: %d (0x%2.2X)' % (self.max_hp, self.max_hp))
        print('Max MP: %d (0x%2.2X)' % (self.max_mp, self.max_mp))

        print('Level: %d (0x%2.2X)' % (self.level, self.level))
        print('Tech Level: %d (0x%2.2X)'
              % (self.tech_level, self.tech_level))
        print('Techs Learned: %2.2X ' %
              (sum([0x80 >> i for i in range(0, self.tech_level)])))

        print('Total XP: %d (0x%3.3X)' %
              (self.xp, self.xp))
        print('XP to next level: %d (0x%2.2X)' %
              (self.xp_next, self.xp_next))
        print('TP to next level: %d (0x%2.2X)' %
              (self.tp_next, self.tp_next))

    def __update_statblock(self):
        offsets = \
            [PCStats.cur_hp_off,
             PCStats.max_hp_off,
             PCStats.cur_mp_off,
             PCStats.max_mp_off,
             PCStats.cur_stat_off,
             PCStats.lvl_off,
             PCStats.xp_off,
             PCStats.xp_next_off,
             PCStats.tp_next_off,
             PCStats.base_stat_off]

        sizes = \
            [PCStats.cur_hp_len,
             PCStats.max_hp_len,
             PCStats.cur_mp_len,
             PCStats.max_mp_len,
             PCStats.cur_stat_len,
             PCStats.lvl_len,
             PCStats.xp_len,
             PCStats.xp_next_len,
             PCStats.tp_next_len,
             PCStats.base_stat_len]

        writes = \
            [to_little_endian(self.max_hp, PCStats.max_hp_len),
             to_little_endian(self.max_hp, PCStats.max_hp_len),
             to_little_endian(self.max_mp, PCStats.max_mp_len),
             to_little_endian(self.max_mp, PCStats.max_mp_len),
             self.cur_stats,
             bytearray([self.level]),
             to_little_endian(self.xp, PCStats.xp_len),
             to_little_endian(self.xp_next, PCStats.xp_next_len),
             to_little_endian(self.tp_next, PCStats.tp_next_len),
             self.base_stats]

        for i in range(len(offsets)):
            if len(writes[i]) != sizes[i]:
                print('Error writing at', i)
            self.stat_block[offsets[i]:offsets[i]+sizes[i]] = writes[i]

    def write_to_rom_default(self, rom, out_ind):
        self.write_to_rom(rom, out_ind,
                          0x0C0000,
                          0x0C258A, 0x0C25C2, 0x0C25FA,
                          0x0C26FA)

    def write_to_rom(self, rom, out_ind,
                     stat_start,
                     hp_growth_start,
                     mp_growth_start,
                     stat_growth_start,
                     tp_thresh_start):

        hp_grw_st = hp_growth_start + out_ind*PCStats.hp_grw_len
        rom[hp_grw_st:hp_grw_st+PCStats.hp_grw_len] = self.hp_growth[:]

        mp_grw_st = mp_growth_start + out_ind*PCStats.mp_grw_len
        rom[mp_grw_st:mp_grw_st+PCStats.mp_grw_len] = self.mp_growth[:]

        st_grw_st = stat_growth_start + out_ind*PCStats.stat_grw_len
        rom[st_grw_st:st_grw_st+PCStats.stat_grw_len] = self.stat_growth[:]

        tp_thr_st = tp_thresh_start + out_ind*PCStats.tp_thr_len

        tp_thr_bytes = bytearray()
        for x in self.tp_thresh:
            cur = to_little_endian(x, 2)
            tp_thr_bytes += cur

        rom[tp_thr_st:tp_thr_st+PCStats.tp_thr_len] = tp_thr_bytes[:]

        # Tech level
        tech_offset = stat_start + 0x230
        rom[tech_offset+out_ind] = self.tech_level

        techs_learned = sum([0x80 >> i for i in range(0, self.tech_level)])
        rom[tech_offset+7+out_ind] = techs_learned

        # Now do all of the stat block stuff
        sb_start = stat_start + 0x50*out_ind

        rom[sb_start:sb_start+0x50] = self.stat_block[:]

        offsets = \
            [sb_start + PCStats.cur_hp_off,
             sb_start + PCStats.max_hp_off,
             sb_start + PCStats.cur_mp_off,
             sb_start + PCStats.max_mp_off,
             sb_start + PCStats.cur_stat_off,
             sb_start + PCStats.lvl_off,
             sb_start + PCStats.xp_off,
             sb_start + PCStats.xp_next_off,
             sb_start + PCStats.tp_next_off,
             sb_start + PCStats.base_stat_off]

        sizes = \
            [PCStats.cur_hp_len,
             PCStats.max_hp_len,
             PCStats.cur_mp_len,
             PCStats.max_mp_len,
             PCStats.cur_stat_len,
             PCStats.lvl_len,
             PCStats.xp_len,
             PCStats.xp_next_len,
             PCStats.tp_next_len,
             PCStats.base_stat_len]

        writes = \
            [to_little_endian(self.max_hp, PCStats.max_hp_len),
             to_little_endian(self.max_hp, PCStats.max_hp_len),
             to_little_endian(self.max_mp, PCStats.max_mp_len),
             to_little_endian(self.max_mp, PCStats.max_mp_len),
             self.cur_stats,
             bytearray([self.level]),
             to_little_endian(self.xp, PCStats.xp_len),
             to_little_endian(self.xp_next, PCStats.xp_next_len),
             to_little_endian(self.tp_next, PCStats.tp_next_len),
             self.base_stats]

        for i in range(len(offsets)):
            if len(writes[i]) != sizes[i]:
                print('Error writing at', i)
            else:
                rom[offsets[i]:offsets[i]+sizes[i]] = writes[i]


# For stats other than hp/mp
def compute_stat(base_stat, stat_growth, level):
    return ((level-1)*stat_growth) // 100 + base_stat


# returns the stats in base stat order.
def grow_stats(base_stats, stat_growths, level):
    new_stats = bytearray()
    for i in range(7):
        new_stats.append(compute_stat(base_stats[i], stat_growths[i], level))

    return new_stats


# growth is an 8 byte array
# Format: Four pairs XX YY interpreted at "until level XX gain YY hp/lv"
# Ex: 0A 0D 15 0F 30 15 63 0A
#    From level 0 to level 0xA=10 gain 0xD=14 hp/lv
#    From lv 0xA+1 to 0x15 gain 0x30 hp/lv
#    From lv 0x15+1 to 0x30 gain 0x15 hp/lv
#    From lv 0x30+1 to 0x63=99 gain 0x0A hp/lv
# Hp growth is computed per level, not recomputed from scratch with each lv.
def compute_hpmp_growth(growth, level):
    cur_lv = 0
    cur_val = 0

    for i in range(0, 4):
        max_lv = growth[2*i]
        growth_rate = growth[2*i+1]

        while cur_lv <= min(max_lv, level):
            cur_val += growth_rate
            cur_lv += 1

    return cur_val


# Compute the hp or mp value of a character at a new level given their
# current level, current hp/hp, and the growth array
def compute_new_hpmp(cur_level, cur_hpmp, hpmp_growth, new_level):
    cur_growth = compute_hpmp_growth(hpmp_growth, cur_level)
    base_hpmp = cur_hpmp - cur_growth

    return base_hpmp + compute_hpmp_growth(hpmp_growth, new_level)


# Stats are recorded in different orders in different contexts.  A PC's base
# stats are recorded in one order, and the current stats are stored in another
# order.  The next two functions convert between them

# Stats: Pow, Sta, Spd (unused), Hit, Evd, Mag, Mdf
#        Ind:  0    1    2    3    4    5    6
# Base Order: Pow, Sta, Spd, Hit, Evd, Mag, Mdf
#  Cur Order: Pow, Sta, Spd, Mag, Hit, Evd, Mdf

# return base stat order given current stat order
def get_stat_base_order(cur_stat_list):
    perm = [0, 1, 2, 4, 5, 3, 6]
    base_stat_list = bytearray()

    for i in range(7):
        base_stat_list.append(cur_stat_list[perm[i]])

    return base_stat_list


# return current stat order given base stat order
def get_stat_cur_order(base_stat_list):
    perm = [0, 1, 2, 5, 3, 4, 6]
    cur_stat_list = bytearray()

    for i in range(7):
        cur_stat_list.append(base_stat_list[perm[i]])

    return cur_stat_list


if __name__ == '__main__':
    with open('jets_test.sfc', 'rb') as infile:
        rom = bytearray(infile.read())

    reassign = [1,1,1,1,1,1,1]

    # All of the heavy lifting is done by PCStats class
    orig_pcs = [PCStats.stats_from_rom_default(rom, i) for i in range(7)]
    new_pcs = [copy.deepcopy(orig_pcs[reassign[i]]) for i in range(7)]

    # Now each new_pc needs to be releveled/tech leveled
    for i in range(7):
        # correct pc index
        new_pcs[i].stat_block[0] = i

        orig_lvl = orig_pcs[i].level
        new_pcs[i].set_level(3)

        orig_tech_lvl = orig_pcs[i].tech_level
        new_pcs[i].set_tech_level(orig_tech_lvl)

        # new_pcs[i].write_to_rom_default(rom, i)

        new_pcs[i].print_data()

