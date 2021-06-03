# TODO List:
#  -Add entry for atb delays.  Right now, I NOP those out elsewhere, but some
#   sadist may want to add them back in.  Also, when the tech list changes the
#   delays become incorrectly mapped. -- Done
#  -Fix X-menu desc_ptrs (maybe in techrefs) -- Done.

import copy
from byteops import get_record, set_record, print_bytes, \
    get_value_from_bytes, to_little_endian, to_file_ptr, to_rom_ptr
from techrefs import fix_tech_refs


class TechDB:
    control_size = 0xB
    effect_size = 0xC
    gfx_size = 0x7
    target_size = 0x2
    bat_grp_size = 0x3
    menu_grp_size = 0x1
    name_size = 0xB
    desc_ptr_size = 0x2
    lrn_req_size = 0x3
    lrn_ref_size = 0x5
    mp_size = 0x1
    atb_pen_size = 0x1

    def __init__(self):
        self.controls = bytearray([])
        self.control_count = 0
        self.control_start = 0

        self.effects = bytearray([])
        self.effect_count = 0
        self.effect_start = 0

        self.gfx = bytearray([])
        self.gfx_count = 0
        self.gfx_start = 0

        self.targets = bytearray([])
        self.target_count = 0
        self.target_start = 0

        self.bat_grps = bytearray([])
        self.bat_grp_count = 0
        self.bat_grp_start = 0

        self.menu_grps = bytearray([])
        self.menu_grp_count = 0
        self.menu_grp_start = 0

        self.names = bytearray([])
        self.name_count = 0
        self.name_start = 0

        self.desc_start = 0
        self.descs = bytearray([])

        self.desc_ptrs = bytearray([])
        self.desc_ptr_count = 0
        self.desc_ptr_start = 0

        self.techs_learned = bytearray([])
        self.techs_learned_start = 0
        self.orig_techs_learned_start = 0

        self.lrn_reqs = bytearray([])
        self.lrn_req_count = 0x38
        self.lrn_req_start = 0

        self.lrn_refs = bytearray([])
        self.lrn_ref_count = 0x19
        self.lrn_ref_start = 0

        self.mps = bytearray([])
        self.mp_count = 0x39
        self.mp_start = 0

        self.menu_mp_reqs = bytearray([])
        self.menu_req_start = 0

        self.group_sizes = bytearray([])
        self.group_sizes_start = 0

        self.atb_pens = bytearray([])
        self.atb_pen_count = 0
        self.atb_pen_start = 0

        self.group_used = bytearray([])
        self.first_dual_grp = 0
        self.first_trip_grp = 0
        self.first_rock_grp = 0

        self.first_trip_tech = 0
        self.first_dual_tech = 0
        self.first_rock_tech = 0

        self.num_techs = 0

        self.menu_usable_ids = {}
        self.pc_target = bytearray()

        self.rock_types = bytearray()

    def get_default_db(vanilla_rom):
        db = TechDB.db_from_rom(vanilla_rom,
                                0x0C1BEB, 0x7C,
                                0x0C213F, 0x44,
                                0x0D45A6, 0x80,
                                0x0C1ACB, 0x75,
                                0x0C249F, 0x32,
                                0x0C2963, 0x25,
                                0x0C15C4, 0x75,
                                0x0C3A09, 0x79,
                                0x0C3B0D, 0x0C43AF,
                                0x0C0230,
                                0x0C27F7, 0x38,
                                0x0C2778, 0x19,
                                0x0C253B, 0x44,
                                0x0C28DB, 0x0C2962,
                                0x02BD40, 0x25,
                                0x0C2BDC, 0x75+15)

        # TODO:  Move all of this stuff into the basic db_from_rom function
        # TODO:  Change this to read pointers from the actual rom.
        db.menu_usable_ids = [False]*db.control_count
        for x in [0x09, 0x0C, 0x0F, 0x1A, 0x1D, 0x21, 0x24, 0x27, 0x29]:
            db.menu_usable_ids[x] = True

        # Fix the "learned fire whirl" bug
        db.lrn_refs[2] = 0x3

        # Record which techs have pc-specific targetting
        for i in range(0, db.target_count):
            start = 2*i
            if db.targets[start] in {0x0D, 0x13, 0x14}:  # Based around Robo
                db.pc_target[i] = 3
            elif db.targets[start] in {0x1B}:  # Based around Magus
                db.pc_target[i] = 6
            else:
                db.pc_target[i] = 0xFF

        db.first_dual_tech = 0x39
        db.first_trip_tech = 0x66
        db.first_rock_tech = 0x70
        db.num_techs = 0x75

        # Record which rocks have a corresponding tech in the db.
        # For vanilla, of course all rocks are used
        db.rock_types = bytearray.fromhex('00 01 02 03 04')

        return db

    # Give a bunch of pointers to where data is on the rom and shove it all
    # Into a TechDB.
    def db_from_rom(rom,
                    control_start, control_count,
                    effect_start, effect_count,
                    gfx_start, gfx_count,
                    target_start, target_count,
                    bat_grp_start, bat_grp_count,
                    menu_grp_start, menu_grp_count,
                    name_start, name_count,
                    desc_ptr_start, desc_ptr_count,
                    desc_start, desc_end,
                    lrn_start,
                    lrn_req_start, lrn_req_count,
                    lrn_ref_start, lrn_ref_count,
                    mp_start, mp_count,
                    menu_mp_start, menu_mp_end,
                    group_length_start, group_length_count,
                    atb_pen_start, atb_pen_count):

        db = TechDB()

        control_end = control_start + TechDB.control_size*control_count
        db.controls = rom[control_start:control_end]
        db.control_count = control_count
        db.control_start = control_start

        effect_end = effect_start + TechDB.effect_size*effect_count
        db.effects = rom[effect_start:effect_end]
        db.effect_count = effect_count
        db.effect_start = effect_start

        gfx_end = gfx_start+TechDB.gfx_size*gfx_count
        db.gfx = rom[gfx_start:gfx_end]
        db.gfx_count = gfx_count
        db.gfx_start = gfx_start

        target_end = target_start+TechDB.target_size*target_count
        db.targets = rom[target_start:target_end]
        db.target_count = target_count
        db.target_start = target_start

        bat_grp_end = bat_grp_start + TechDB.bat_grp_size*bat_grp_count
        db.bat_grps = rom[bat_grp_start:bat_grp_end]
        db.bat_grp_count = bat_grp_count
        db.bat_grp_start = bat_grp_start

        menu_grp_end = menu_grp_start+TechDB.menu_grp_size*menu_grp_count

        # Also sets up some thresholds for dual/triple/rock groups
        # Takes care of counts too.

        # TODO: There's a little problem here because it's not easy to
        # determine how many rock groups there are by looking at the rom.
        # We just assume that it's 5 when reading from the rom, but this
        # should be redone if we want to correctly read an altered db
        db.set_menu_grps(rom[menu_grp_start:menu_grp_end], 5)
        db.menu_grp_start = menu_grp_start

        names_end = name_start + TechDB.name_size*name_count
        db.names = rom[name_start:names_end]
        db.name_count = name_count
        db.name_start = name_start

        desc_ptr_end = desc_ptr_start+TechDB.desc_ptr_size*desc_ptr_count
        db.desc_ptrs = rom[desc_ptr_start:desc_ptr_end]
        db.desc_ptr_count = desc_ptr_count
        db.desc_ptr_start = desc_ptr_start

        db.desc_start = desc_start
        db.descs = rom[desc_start:desc_end]

        # 7 bytes for current tech levels and then one byte per menu group
        techs_learned_size = 7+menu_grp_count
        db.techs_learned = rom[lrn_start:lrn_start+techs_learned_size]
        db.techs_learned_start = lrn_start

        lrn_req_end = lrn_req_start + lrn_req_count*TechDB.lrn_req_size
        db.lrn_reqs = rom[lrn_req_start:lrn_req_end]
        db.lrn_req_count = lrn_req_count
        db.lrn_req_start = lrn_req_start

        lrn_ref_end = lrn_ref_start+TechDB.lrn_ref_size*lrn_ref_count
        db.lrn_refs = rom[lrn_ref_start:lrn_ref_end]
        db.lrn_ref_count = lrn_ref_count
        db.lrn_ref_start = lrn_ref_start

        db.mps = rom[mp_start:mp_start+mp_count]
        db.mp_count = mp_count
        db.mp_start = mp_start

        db.menu_mp_reqs = rom[menu_mp_start:menu_mp_end]
        db.menu_req_start = menu_mp_start

        group_length_end = group_length_start+group_length_count
        db.group_sizes = rom[group_length_start:group_length_end]
        db.group_sizes_start = group_length_start

        atb_pen_end = atb_pen_start+TechDB.atb_pen_size*atb_pen_count
        db.atb_pens = rom[atb_pen_start:atb_pen_end]
        db.atb_pen_count = atb_pen_count
        db.atb_pen_start = atb_pen_start

        db.pc_target = bytearray([0xFF]*db.control_count)

        # Try to get a menu-usable implementation here.
        db.menu_usable_ids = [False]*db.control_count

        # $FF/F82E A9 80       LDA #$80 <-- how the menu routine should start
        # $FF/F82E 22 XX XX XX JSL $XXXXXX  <-- how it looks if expanded

        rt_start = rom[0x3FF82E]
        pos = 0

        if rt_start == 0xA9:
            # Not expanded, still starting with the LDA #$80
            pos = 0x3FF830  # Start of TSB block

        elif rt_start == 0x22:
            # Expanded, starts with a JSL
            rt_addr = get_value_from_bytes(rom[rt_start+1, rt_start+4])
            rt_addr = to_file_ptr(rt_addr)

            # new rt has the LDA #$80 (2 bytes) and then starts the TSBs
            pos = rt_addr+2

        while rom[pos] == 0x0C:
            db.menu_usable_ids[rom[pos+1]] = True
            pos += 3

        """
        (db.orig_control_start, db.orig_effect_start,
         db.orig_gfx_start, db.orig_target_start,
         db.orig_bat_grp_start, db.orig_menu_grp_start,
         db.orig_name_start, db.orig_desc_ptr_start,
         db.orig_desc_start, db.orig_techs_learned_start,
         db.orig_lrn_req_start, db.orig_lrn_ref_start,
         db.orig_mp_start, db.orig_menu_req_start,
         db.orig_group_sizes_start, db.orig_atb_pen_start) = \
            (db.control_start, db.effect_start,
             db.gfx_start, db.target_start,
             db.bat_grp_start, db.menu_grp_start,
             db.name_start, db.desc_ptr_start,
             db.desc_start, db.techs_learned_start,
             db.lrn_req_start, db.lrn_ref_start,
             db.mp_start, db.menu_req_start,
             db.group_sizes_start, db.atb_pen_start)
        """
        db.orig_techs_learned_start = db.techs_learned_start

        return db

    # For techs to be learned after battle, the learn refs need to point to
    # the right places in the learn reqs.  If the learn reqs are going to move
    # in memory or techs get shuffled, the learn refs need to be recomputed.
    def rewrite_lrn_refs(self):

        # You have to add 3 because of a blank "tech 0" entry in the lrn_reqs
        addr = self.lrn_req_start % 0x010000+3

        for i in range(0, self.lrn_ref_count):
            start = i*TechDB.lrn_ref_size
            grp_ind = i+7
            if (grp_ind < self.first_trip_grp):
                group_len = 3
            else:
                group_len = 1

            self.lrn_refs[start:start+3] = [self.menu_grps[grp_ind],
                                            self.group_sizes[grp_ind],
                                            group_len]

            self.lrn_refs[start+3:start+5] = to_little_endian(addr, 2)

            addr += group_len*TechDB.lrn_req_size

    # Helper function converting a three element battle group into a bitmask
    # meu group
    def bat_to_menu(bat_grp):
        menu_grp = 0x0
        for x in bat_grp:
            if x != 0xFF:
                menu_grp = menu_grp | (0x80 >> x)

        return menu_grp

    # Add new effect header unless already present.  Return index to the header
    # in the data.
    # Used when adding techs to a db.  In current implementation we should
    # never actually add a new header.
    def add_effect_header(self, new_effect):
        found = False
        for ind in range(0, self.effect_count):
            eh = get_record(self.effects, ind, self.effect_size)
            if eh == new_effect:
                # print("Effect header found at %2.2X" % ind)
                found = True
                break

        if not found:
            print("Effect header not found.  Appending.")
            self.effects += new_effect

        return ind

    # Gets most information about a tech.  Most notable missing info is the
    # animation script, but it's not needed since we're just shuffling techs.
    def get_tech(self, tech_id):
        ret_tech = dict()
        ret_tech['control'] = get_record(self.controls,
                                         tech_id,
                                         self.control_size)

        ret_tech['effects'] = [[], [], []]
        for i in range(0, 3):
            eff_ind = (ret_tech['control'][5+i] & 0x7F)
            eff = get_record(self.effects, eff_ind, self.effect_size)
            # print_bytes(eff,12)
            ret_tech['effects'][i] = eff[:]

        ret_tech['gfx'] = get_record(self.gfx, tech_id, self.gfx_size)

        ret_tech['target'] = get_record(self.targets,
                                        tech_id,
                                        self.target_size)

        ret_tech['name'] = get_record(self.names, tech_id, self.name_size)

        ret_tech['lrn_req'] = get_record(self.lrn_reqs,
                                         tech_id-0x38,
                                         self.lrn_req_size)

        bat_id = ret_tech['control'][0] & 0x7F
        ret_tech['bat_grp'] = get_record(self.bat_grps,
                                         bat_id,
                                         self.bat_grp_size)

        desc_ptr = get_record(self.desc_ptrs, tech_id,
                              self.desc_ptr_size)
        start = get_value_from_bytes(desc_ptr)
        start = start - (self.desc_start % 0x010000)

        end = start
        while self.descs[end] != 0x00:
            end += 1

        ret_tech['desc'] = self.descs[start:end]

        first_dual_tech = self.group_sizes[self.first_dual_grp]
        if tech_id < first_dual_tech:
            ret_tech['lrn_reqs'] = None
        else:
            ret_tech['lrn_reqs'] = get_record(self.lrn_reqs,
                                              tech_id-0x38,
                                              self.lrn_req_size)

        ret_tech['atb_pen'] = [self.atb_pens[tech_id]]
        first_trip_tech = self.group_sizes[self.first_trip_grp]
        num_trips = len(self.menu_grps)-self.first_trip_grp

        if tech_id >= first_trip_tech:
            ret_tech['atb_pen'].append(self.atb_pens[tech_id+num_trips])

        return ret_tech
    # End get_tech

    # Update desc ptrs to point into the right place
    def set_desc_start(self, new_start):
        offset = (new_start % 0x010000) - (self.desc_start % 0x010000)

        for i in range(self.desc_ptr_count):
            ptr = get_record(self.desc_ptrs, i, self.desc_ptr_size)
            ptr_addr = get_value_from_bytes(ptr)
            ptr_addr = ptr_addr + offset
            new_ptr = to_little_endian(ptr_addr, 2)
            set_record(self.desc_ptrs, new_ptr, i, self.desc_ptr_size)

        self.desc_start = new_start

    # Companion to get_tech.  Puts a tech into the db.  Again, we assume that
    # the animation script is in the rom already and we just pass the right
    # index to it in the gfx data.
    def set_tech(self, tech, id):
        set_record(self.controls, tech['control'], id, TechDB.control_size)
        set_record(self.gfx, tech['gfx'], id, TechDB.gfx_size)
        set_record(self.targets, tech['target'], id, TechDB.target_size)
        set_record(self.names, tech['name'], id, TechDB.name_size)

        grp_count = 0
        for x in tech['bat_grp']:
            if x != 0xFF:
                grp_count += 1

        if grp_count > 1 and len(tech['lrn_req']) > 0:
            set_record(self.lrn_reqs, tech['lrn_req'], id-0x38,
                       TechDB.lrn_req_size)

        # print_bytes(self.atb_pens, 16)
        # print(tech['atb_pen'], format(id, 'X'))
        # input()
        self.atb_pens[id] = tech['atb_pen'][0]

        if grp_count == 3:
            num_trips = \
                len(self.menu_grps) - self.group_sizes[self.first_trip_grp]

            self.atb_pens[id+num_trips] = tech['atb_pen'][1]

        # leave desc alone for now
        # leave mp alone for now

    # different from set_tech() because set_tech assumes that there's space
    # for a tech with a given id.  This just takes a tech and puts it where
    # it's supposed to go.
    def add_tech(self, tech):

        menu_grp = TechDB.bat_to_menu(tech['bat_grp'])
        menu_ind = self.add_menu_grp(menu_grp)

        bat_ind = self.add_bat_grp(tech['bat_grp'])

        group_cap = 0
        if menu_ind < self.first_dual_grp:
            print("Inserting single tech.  Probably an error.")
            group_cap = 8
        elif menu_ind < self.first_trip_grp:
            print("Inserting dual tech.")
            group_cap = 3
        else:
            print("Inserting triple tech.")
            group_cap = 1

        if (self.group_used[menu_ind] >= group_cap):
            print("Error: Inserting into full group")
            return None

        tech_id = self.group_sizes[menu_ind] + self.group_used[menu_ind]
        print("Inserting at tech_id 0x%2.2X" % tech_id)

        # Update the control header to the right index.  Preserve x80 bit
        bat_grp_ind = tech['control'][0]
        bat_grp_ind = bat_ind | (bat_grp_ind & 0x80)
        tech['control'][0] = bat_grp_ind

        # Effects
        for i in range(0, 3):
            ind = self.add_effect_header(tech['effects'][i])

            eff_x80 = tech['control'][5+i] & 0x80
            tech['control'][5+i] = ind | eff_x80

        set_record(self.controls, tech_id,
                   self.control_size, tech['control'])

        set_record(self.gfx, tech_id, self.gfx_size,
                   tech['gfx'])

        set_record(self.targets, tech_id, self.target_size,
                   tech['target'])

        set_record(self.names, tech_id, self.name_size,
                   tech['name'])

        # point the new desc_ptr to the end of the list
        desc_ptr = to_little_endian(self.desc_start + len(self.descs), 2)
        set_record(self.desc_ptrs, tech_id, self.desc_ptr_size,
                   desc_ptr)

        self.descs.extend(tech['desc'] + bytearray([0]))

        set_record(self.lrn_reqs, tech_id-0x38, self.lrn_req_size,
                   tech['lrn_req'])

        temp_grp = tech['bat_grp']
        temp_grp = bytearray(sorted(temp_grp))

        menu_mps = []
        for i in range(2):
            menu_mps.append(temp_grp[i]*8+tech['lrn_req'][i])

        self.menu_mp_reqs[(tech_id-0x38)*2:(tech_id-0x37)*2] = menu_mps[0:2]

        self.group_used[menu_ind] += 1

    def set_menu_grps(self, menu_grps, num_rocks):
        self.menu_grps = menu_grps
        self.menu_grp_count = len(menu_grps)

        # Now check for first dual, trip, etc.
        in_singles = True
        in_duals = False
        in_trips = False

        for i in range(0, len(menu_grps)):
            x = menu_grps[i]
            count = 0
            for j in range(0, 8):
                if (x & 0x80) == 0x80:
                    count += 1
                x = (x << 1) & 0xFF

            if count == 0:
                print("ERROR: Zero menu group.")
                return
            if in_singles:
                if count == 2:
                    in_singles = False
                    in_duals = True
                    self.first_dual_grp = i
                elif count == 3:
                    print("ERROR: Skipped from single to dual")
                    return
            elif in_duals:
                if count == 3:
                    in_duals = False
                    in_trips = True
                    self.first_trip_grp = i
                elif count == 1:
                    print("ERROR: Went from dual to single")
                    return
            elif in_trips:
                if count == 2:
                    print("ERROR: Went from triple to dual")
                    return
                elif count == 1:
                    print("ERROR: Went from triple to single.")
                    return

        self.first_rock_grp = len(menu_grps) - num_rocks

        self.group_used = bytearray([0]*len(menu_grps))
        for i in range(0, self.first_dual_grp):
            self.group_used[i] = 8

        for i in range(self.first_dual_grp, self.first_trip_grp):
            self.group_used[i] = 3

        for i in range(self.first_trip_grp, len(menu_grps)):
            self.group_used[i] = 1
    # Ending set_menu_grps

    def get_menu_grp_ind(self, menu_grp):
        for i in range(0, len(self.menu_grps)):
            if self.menu_grps[i] == menu_grp:
                return i

        return None

    # Update all pointers in lrn_refs based on the current start and the
    # new start.
    # Only the low order 2 bytes are used from new_start.
    def set_lrn_req_start(self, new_start):
        start = new_start % 0x010000
        offset = start - (self.lrn_req_start % 0x010000)

        # print_bytes(self.lrn_refs, 5)
        for i in range(self.lrn_ref_count):
            ptr_start = i*self.lrn_ref_size+3
            ptr = self.lrn_refs[ptr_start:ptr_start+2]
            ptr_val = get_value_from_bytes(ptr)
            ptr_val = ptr_val + offset

            self.lrn_refs[ptr_start:ptr_start+2] = to_little_endian(ptr_val, 2)

        # print_bytes(self.lrn_refs, 5)
        self.lrn_req_start = new_start

    # End set_lrn_req_start

    def add_bat_grp(self, bat_grp, is_rock=False):
        # First check whether the menu group is already recorded
        menu_grp = 0x0
        for x in bat_grp:
            if x != 0xFF:
                menu_grp = menu_grp | (0x80 >> x)

        # print("Menu grp: %2.2X" % menu_grp)
        ind = self.add_menu_grp(menu_grp, is_rock)

        # Now see if the battle group is already there
        ind_grp = get_record(self.bat_grps, ind, self.bat_grp_size)

        if ind_grp == bat_grp:
            return ind
        elif ind_grp == bytearray([0, 0, 0]):
            # print("Found empty group in expected position. Filling.")
            split = self.bat_grp_size*ind
            self.bat_grps[split:split+3] = bat_grp
            return ind
        else:
            # Need to look for the rest
            found = False
            for i in range(ind, self.bat_grp_count):
                i_grp = get_record(self.bat_grps, i, self.bat_grp_size)
                # The order really matters, so it's a list comparison
                if(i_grp == bat_grp):
                    print("Group found at %d" % i)
                    ind = i
                    found = True
                    break
            if not found:
                # Just add onto the end
                # print('Adding to end in position %2.2X' % self.bat_grp_count)
                ind = self.bat_grp_count
                self.bat_grps.extend(bat_grp)
                self.bat_grp_count += 1
            # This is either set when found in the loop or set above when not
            # found.
            return ind
        # Ending the else for needing to search the list
    # Ending add_bat_grp

    # Adds new bitmask menu group to the tech db
    # Returns an index to the newly added group.  Will also return the index
    # of the group if it already exists.
    def add_menu_grp(self, menu_grp, is_rock=False):
        # Only duals/trips/rocks for now. No single

        temp = menu_grp
        num_pcs = 0
        for i in range(0, 8):
            if temp & 0x01 != 0:
                num_pcs += 1

            temp = temp >> 1

        start_grp = 0
        end_grp = 0

        if num_pcs == 1 or num_pcs > 3:
            print('Error: Group %2.2X has size == %d' % (menu_grp, num_pcs))
            start_grp = None
            end_grp = None
        elif num_pcs == 2:
            num_to_add = 3
            start_grp = self.first_dual_grp
            end_grp = self.first_trip_grp
        else:
            num_to_add = 1
            if is_rock:
                # print('Is rock.')
                start_grp = self.first_rock_grp
                end_grp = self.menu_grp_count
            else:
                # print('Is not rock.')
                start_grp = self.first_trip_grp
                end_grp = self.first_rock_grp

        ins_ind = start_grp
        found = False
        for i in range(start_grp, end_grp):
            if self.menu_grps[i] == menu_grp:
                found = True
                # print("Menu group already found at index %d." % i)
                return i

        if not found:
            print("Menu group not already found.  Making room.")

            ins_ind = end_grp
            self.menu_grps.insert(ins_ind, menu_grp)
            # Then we need to make some new space in many places

            if ins_ind == len(self.menu_grps):
                ins_size = self.group_sizes[ins_ind-1]+1
            else:
                ins_size = self.group_sizes[ins_ind]

            # shift all sizes up by the right amount
            # insert with index of old first_trip
            for i in range(end_grp, len(self.group_sizes)):
                self.group_sizes[i] += num_to_add

            self.group_sizes.insert(ins_ind, ins_size)
            self.group_used.insert(ins_ind, 0)
            if num_pcs == 2:
                self.first_trip_grp += 1
            self.first_rock_grp += 1

            tech_id_start = self.group_sizes[ins_ind]

            # Inserting a new battle group means that all control headers need
            # to have their battle group checked and updated.
            for i in range(0, self.control_count):
                start = i*self.control_size
                bat_grp_x80 = self.controls[start] & 0x80
                bat_grp_ind = self.controls[start] & 0x7F

                if bat_grp_ind >= ins_ind:
                    bat_grp_ind += 1
                    self.controls[start] = bat_grp_ind | bat_grp_x80

            lrn_refs_to_add = 0
            lrn_reqs_to_add = 0
            if not is_rock:
                lrn_refs_to_add = 1
                lrn_reqs_to_add = num_to_add

            dat = [self.controls, self.gfx, self.names, self.desc_ptrs,
                   self.targets, self.techs_learned, self.lrn_refs,
                   self.menu_mp_reqs, self.bat_grps, self.lrn_reqs]

            self.control_count += num_to_add
            self.gfx_count += num_to_add
            self.name_count += num_to_add
            self.desc_ptr_count += num_to_add
            self.target_count += num_to_add
            self.lrn_ref_count += lrn_refs_to_add
            self.bat_grp_count += 1
            self.lrn_req_count += lrn_reqs_to_add

            # menu_mp insert spot is a bit harder because it comes in two byte
            # chunks until triples and then 3 byte chunks
            if num_pcs == 3:
                num_trips_before = (tech_id_start
                                    - self.group_sizes[self.first_trip_grp])
            else:
                num_trips_before = 0

            menu_mp_split = ((tech_id_start - 0x38)*2
                             + num_trips_before)

            splits = [tech_id_start*self.control_size,        # control
                      tech_id_start*self.gfx_size,            # gfx
                      tech_id_start*self.name_size,           # names
                      tech_id_start*self.desc_ptr_size,       # desc_ptrs
                      tech_id_start*self.target_size,         # targets
                      ins_ind*1,                              # techs_learned
                      (ins_ind-7)*self.lrn_ref_size,          # lrn_refs
                      menu_mp_split,                          # menu_mp_reqs
                      ins_ind*self.bat_grp_size,              # bat_grps
                      (tech_id_start-0x38)*3]                 # lrn_req

            sizes = [self.control_size*num_to_add,            # control
                     self.gfx_size*num_to_add,                # gfx
                     self.name_size*num_to_add,               # names
                     self.desc_ptr_size*num_to_add,           # desc_ptrs
                     self.target_size*num_to_add,             # targets
                     1,                                       # techs_learned
                     5*lrn_refs_to_add,                       # lrn_refs
                     num_to_add*num_pcs,                      # menu_mp_reqs
                     3,                                       # bat_grps
                     3*lrn_reqs_to_add]                       # lrn_req

            for i in range(0, len(sizes)):
                dat[i][splits[i]:splits[i]] = bytearray([0]*sizes[i])

            if not is_rock:
                # Now fix the pointers in lrn_refs.  All of the ones after the
                # insertion are off.

                start = (ins_ind-7)*self.lrn_ref_size
                after = start + self.lrn_ref_size
                self.lrn_refs[start+3:start+5] = self.lrn_refs[after+3:after+5]

                self.lrn_refs[start] = menu_grp
                self.lrn_refs[start+1] = self.lrn_refs[after+1]
                self.lrn_refs[start+2] = num_to_add

                for i in range(ins_ind-6, self.lrn_ref_count):
                    start = i*self.lrn_ref_size
                    ptr = self.lrn_refs[start+3:start+5]
                    new_addr = get_value_from_bytes(ptr)+9
                    self.lrn_refs[start+3:start+5] = \
                        to_little_endian(new_addr, 2)
                    self.lrn_refs[start+1] += 3
        else:
            pass
            # print("Already found menu group.  No expansion to do.")

        # When not already found, ins_ind (usually self.first_trip) is returned
        return ins_ind
    # End add_menu_grp

    # This needs to go to another file
    def randomize_sing_techs(self, char_id, perm):
        # Swap: effect, mp
        # Swap: controls and what goes with it
        #    gfx, target, name, desc_ptr
        # Swap: menu usability
        # Update effect indices in control headers
        # Update lrn_reqs
        # Update menu_mp_reqs (but menu is so broken...later)
        # But menu_mp_reqs are for rocks, so let's fix them soon

        dat = [self.effects, self.mps,
               self.controls,
               self.gfx,
               self.targets,
               self.names,
               self.desc_ptrs,
               self.menu_usable_ids,
               self.pc_target]

        sizes = [TechDB.effect_size, 1,
                 TechDB.control_size,
                 TechDB.gfx_size,
                 TechDB.target_size,
                 TechDB.name_size,
                 TechDB.desc_ptr_size,
                 1,
                 1]

        temp_dat = copy.deepcopy(dat)

        # swap all the records

        for i in range(0, 8):
            to_ind = 1+8*char_id + perm[i]
            from_ind = 1+8*char_id + i

            for j in range(0, len(dat)):
                x = get_record(temp_dat[j], from_ind, sizes[j])
                dat[j][to_ind*sizes[j]:(to_ind+1)*sizes[j]] = x[:]

        # update effect indices in control headers
        eff_min = 1+8*char_id
        eff_max = eff_min + 7
        for i in range(0, self.control_count):
            # bytes 5,6,7 are effect indices
            ctl_start = i*TechDB.control_size
            for j in range(5, 8):
                eff = self.controls[ctl_start+j]
                eff_x80 = eff & 0x80
                eff_ind = eff & 0x7F

                if eff_min <= eff_ind <= eff_max:
                    new_ind = perm[eff_ind - eff_min]+eff_min
                    self.controls[ctl_start+j] = eff_x80 | new_ind

        # update lrn_reqs
        # look through menu grps for the pc of interest.  Figure out where they
        # are in the lrn_req list, and apply perm
        char_bit = 0x80 >> char_id
        for i in range(self.first_dual_grp, self.first_rock_grp):
            if self.menu_grps[i] & char_bit != 0:
                # our pc is in the menu group
                grp = self.menu_grps[i]

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

                start_tech = self.group_sizes[i]
                lrn_loc = (start_tech-0x38)*TechDB.lrn_req_size+pos

                for tech in range(start_tech, start_tech+size):
                    tech_lrn_start = (tech-0x38)*TechDB.lrn_req_size
                    lrn_loc = tech_lrn_start+pos
                    # print("%2.2X" % tech)
                    # print(pos)
                    # y = get_record(self.lrn_reqs, tech-0x38, 3)
                    # print(y)
                    # print(perm)

                    self.lrn_reqs[lrn_loc] = perm[self.lrn_reqs[lrn_loc]-1]+1

        # update menu_mp_reqs for triple techs (and menu if that ever works)
        for (i, x) in enumerate(self.menu_mp_reqs):
            pc = (x-1) % 8
            if pc == char_id:
                tech_num = (x-1) // 8
                tech_num = perm[tech_num]
                self.menu_mp_reqs[i] = pc*8+tech_num+1

        # Is that it?

    def write_default_db(db, rom):
        TechDB.write_db(db, rom,
                        0x0C1BEB,
                        0x0C213F,
                        0x0D45A6,
                        0x0C1ACB,
                        0x0C2963,
                        0x0C249F,
                        0x0C15C4,
                        0x0C3B0D,
                        0x0C3A09,
                        0x0C0230,
                        0x0C27F7,
                        0x0C2778,
                        0x0C253B,
                        0x0C28DB,
                        0x02BD40,
                        0x0C2BDC)

    # This method writes 0xFF to the rom in the places the db is recording.
    # This is used for two main reasons.  First, we want to make sure that old
    # data is not read when we relocate.  Writing the FFs should make things
    # error out.  Second, we test that a db is faithfully recording by
    # FFing and then writing the real data back over.
    def write_db_ff(db, rom,
                    control_start,
                    effect_start,
                    gfx_start,
                    targets_start,
                    menu_grps_start,
                    bat_grps_start,
                    names_start,
                    desc_start,
                    desc_ptr_start,
                    techs_learned_start,
                    lrn_req_start,
                    lrn_refs_start,
                    mp_start,
                    menu_mp_reqs_start,
                    group_sizes_start,
                    atb_pen_start):

        starts = [control_start, effect_start, gfx_start, targets_start,
                  menu_grps_start, bat_grps_start, names_start,
                  desc_start, desc_ptr_start, techs_learned_start,
                  lrn_req_start, lrn_refs_start, mp_start,
                  menu_mp_reqs_start, group_sizes_start,
                  atb_pen_start]

        db_dat = [db.controls, db.effects, db.gfx, db.targets,
                  db.menu_grps, db.bat_grps, db.names,
                  db.descs, db.desc_ptrs, db.techs_learned,
                  db.lrn_reqs, db.lrn_refs, db.mps,
                  db.menu_mp_reqs, db.group_sizes,
                  db.atb_pens]

        for i in range(len(starts)):
            length = len(db_dat[i])
            rom[starts[i]:starts[i]+length] = bytearray([0xFF]*length)

    def write_db_ff_internal(db, rom):
        TechDB.write_db_ff(db, rom,
                           db.control_start,
                           db.effect_start,
                           db.gfx_start,
                           db.target_start,
                           db.menu_grp_start,
                           db.bat_grp_start,
                           db.name_start,
                           db.desc_start,
                           db.desc_ptr_start,
                           db.techs_learned_start,
                           db.lrn_req_start,
                           db.lrn_ref_start,
                           db.mp_start,
                           db.menu_req_start,
                           db.group_sizes_start,
                           db.atb_pen_start)

    def write_db(db, rom,
                 control_start,
                 effect_start,
                 gfx_start,
                 target_start,
                 menu_grp_start,
                 bat_grp_start,
                 name_start,
                 desc_start,
                 desc_ptr_start,
                 techs_learned_start,
                 lrn_req_start,
                 lrn_ref_start,
                 mp_start,
                 menu_mp_req_start,
                 group_sizes_start,
                 atb_pen_start):

        # First fix all of the references.  This is important to do first
        # because techs_learned has a block copied potentially to a new bank.

        num_trips = len(db.menu_grps) - db.first_trip_grp

        fix_tech_refs(rom,
                      control_start,
                      effect_start,
                      gfx_start,
                      target_start,
                      bat_grp_start,
                      menu_grp_start,
                      name_start,
                      desc_ptr_start,
                      desc_start,
                      db.orig_techs_learned_start, techs_learned_start,
                      lrn_req_start,
                      lrn_ref_start,
                      mp_start,
                      menu_mp_req_start,
                      group_sizes_start,
                      atb_pen_start, num_trips)

        # These two need more care since the relative location of trip/rock
        # will vary depending on the reassignment
        # $FF/F97A BF 83 29 CC LDA $CC2983,x  --> 0x3FF97B  (Rock Techs)
        # $FF/F91A BF 79 29 CC LDA $CC2979,x  --> 0x3FF91B  (Triple Techs)

        trip_grp_start = menu_grp_start + db.first_trip_grp
        trip_grp_start = to_rom_ptr(trip_grp_start)
        trip_grp_start_b = to_little_endian(trip_grp_start, 3)

        rom[0x3FF91B:0x3FF91B+3] = trip_grp_start_b[:]

        # this might be hit by charrando.update_rock_techs
        rock_grp_start = menu_grp_start + db.first_rock_grp
        rock_grp_start = to_rom_ptr(rock_grp_start)
        rock_grp_start_b = to_little_endian(rock_grp_start, 3)

        rom[0x3FF97B:0x3FF97B+3] = rock_grp_start_b[:]

        # Menu Req references that depend on number of techs
        num_dual_techs = 3*(db.first_dual_grp-7)
        trip_menu_mp_start = menu_mp_req_start + 3*2*num_dual_techs
        trip_menu_mp_start_b = to_little_endian(trip_menu_mp_start, 3)

        # Menu MP start of trips
        # $FF/F947 BF 35 29 CC LDA $CC2935,x --> 0x3FF948
        rom[0x3FF948:0x3FF948+3] = trip_menu_mp_start_b

        # $FF/F98C BF 53 29 CC LDA $CC2953,x
        # $CC2953 is the start of the rock part of the menu_mp_req
        num_non_rock_trips = db.first_rock_grp-db.first_trip_grp

        # Loading menu page + a value to get menu page descs
        # $C2/BE2F 69 76       ADC #$76
        # Should be num desc ptrs - 3
        rom[0x02BE30] = db.desc_ptr_count - 3

        if(db.first_rock_grp >= len(db.menu_grps)):
            mmp_offset = 0
        else:
            mmp_offset = \
                2*(db.group_sizes[db.first_rock_grp]-0x39)\
                + num_non_rock_trips

        rock_mmp_start = menu_mp_req_start + mmp_offset
        rom[0x3FF98D:0x3FF98D+3] = to_little_endian(rock_mmp_start, 3)

        """
        (db.orig_control_start, db.orig_effect_start,
         db.orig_gfx_start, db.orig_target_start,
         db.orig_bat_grp_start, db.orig_menu_grp_start,
         db.orig_name_start, db.orig_desc_ptr_start,
         db.orig_desc_start, db.orig_techs_learned_start,
         db.orig_lrn_req_start, db.orig_lrn_ref_start,
         db.orig_mp_start, db.orig_menu_req_start,
         db.orig_group_sizes_start, db.orig_atb_pen_start) = \
            (control_start, effect_start,
             gfx_start, target_start,
             bat_grp_start, menu_grp_start,
             name_start, desc_ptr_start,
             desc_start, techs_learned_start,
             lrn_req_start, lrn_ref_start,
             mp_start, menu_mp_req_start,
             group_sizes_start, atb_pen_start)
        """

        db.orig_techs_learned_start = techs_learned_start

        # After writing, the orig starts should be changed?  Otherwise
        # writing twice would break things.

        # When the characters have no duals and/or no triples some of the menus
        # get weird because they look at the start of the next group for loop
        # upper bounds.

        # So when there are no duals/trips put a dummy last entry in.
        # A write method shouldn't change the underlying db, so put the data
        # in a temp list
        first_trip_id = 0

        group_sizes_write = db.group_sizes[:]

        if db.first_dual_grp == len(db.group_sizes):
            # There are no duals and so no trips
            group_sizes_write.append(db.group_sizes[-1]+8)
            first_trip_id = 0x38
        elif db.first_trip_grp == len(db.group_sizes):
            # There are duals but no trips
            first_trip_id = db.group_sizes[db.first_trip_grp-1]+3
            group_sizes_write.append(db.group_sizes[-1]+3)
        else:
            first_trip_id = db.group_sizes[db.first_trip_grp]

        old_lrn_req_start = db.lrn_req_start
        old_desc_start = db.desc_start

        # rewrite pointers (temporarily) for the write
        db.set_lrn_req_start(lrn_req_start)
        db.set_desc_start(desc_start)

        starts = [control_start, effect_start, gfx_start, target_start,
                  menu_grp_start, bat_grp_start, name_start,
                  desc_start, desc_ptr_start, techs_learned_start+14,
                  lrn_req_start, lrn_ref_start, mp_start,
                  menu_mp_req_start, group_sizes_start,
                  atb_pen_start]

        db_dat = [db.controls, db.effects, db.gfx, db.targets,
                  db.menu_grps, db.bat_grps, db.names,
                  db.descs, db.desc_ptrs, db.techs_learned[14:],
                  db.lrn_reqs, db.lrn_refs, db.mps,
                  db.menu_mp_reqs, group_sizes_write,
                  db.atb_pens]

        for i in range(len(starts)):
            length = len(db_dat[i])
            rom[starts[i]:starts[i]+length] = db_dat[i][:]

        # You must FF-terminate the learn refs or searches in it may overflow
        rom[lrn_ref_start+db.lrn_ref_count*TechDB.lrn_ref_size] = 0xFF

        # Ditto with techs_learned (I think?)  but it's also nice to just see
        # where it ends when inspecting ram
        rom[techs_learned_start+14+len(db.techs_learned)] = 0xFF

        # The six bytes starting at 0x02BD65 give the group ranges for single,
        # dual, and triple techs.  We need to update them according to the db.
        # The format is sing start, #sing, dual_start, #dual, trip start, #trip

        rom[0x02BD68] = db.first_trip_grp-db.first_dual_grp
        rom[0x02BD69] = db.first_trip_grp
        rom[0x02BD6A] = len(db.menu_grps)-db.first_trip_grp

        # Ranges for battle menu to pick up techs
        # The battle menu will always be broken when there are too many techs.

        # $C1/CA37 A9 66       LDA #$66 <--- loading first triple tech id

        rom[0x01CA38] = first_trip_id

        # $C1/CCE5 A9 66       LDA #$66   <--- first triple tech id
        # $C1/CCE7 85 08       STA $08
        # $C1/CCE9 A9 75       LDA #$75   <--- last triple tech id+1
        # $C1/CCEB 85 0E       STA $0E

        rom[0x01CCE6] = first_trip_id
        rom[0x01CCEA] = db.group_sizes[-1]+1

        # $C1/CD08 BD 4D 28    LDA $284D,x[$7E:285C]
        # $C1/CDEE BD 4D 28    LDA $284D,x[$7E:285C]

        # These are loading the techs-learned from ram.
        # When we change the number of dual groups, this has to change.
        orig_start = 0x2830 + 7
        trip_start = orig_start + db.first_trip_grp

        trip_start_addr = to_little_endian(trip_start, 2)

        rom[0x01CD09:0x01CD09+2] = trip_start_addr
        rom[0x01CDEF:0x01CDEF+2] = trip_start_addr

        # print("Num Techs: ", db.control_count)
        num_techs = db.control_count  # counting the attack bits

        # hack to keep attack bits right for now
        for i in range(0, 7):
            rom[0x0C2583+i] = (num_techs - 7 + i)

        # Alter menu usability.  This is performed by setting the x80 bit in
        # memory corresponding to each tech.  $7E7700 + tech_id is where it
        # looks for tech #tech_id.  Sometimes there will be too many techs,
        # so we have to jump and extend the routine.
        """
        $FF/F82E A9 80       LDA #$80
        $FF/F830 0C 09 77    TSB $7709  [$7E:7709]
        $FF/F833 0C 0C 77    TSB $770C  [$7E:770C]
        $FF/F836 0C 0F 77    TSB $770F  [$7E:770F]
        $FF/F839 0C 1A 77    TSB $771A  [$7E:771A]
        $FF/F83C 0C 1D 77    TSB $771D  [$7E:771D]
        $FF/F83F 0C 21 77    TSB $7721  [$7E:7721]
        $FF/F842 0C 24 77    TSB $7724  [$7E:7724]
        $FF/F845 0C 27 77    TSB $7727  [$7E:7727]
        $FF/F848 0C 29 77    TSB $7729  [$7E:7729]
        """

        new_ids = bytearray()
        for i in range(0, len(db.menu_usable_ids)):
            if db.menu_usable_ids[i]:
                new_ids.append(i)

        if len(new_ids) <= 9:
            # We can just overwrite the old values
            write_pos = 0x3FF831
            for x in new_ids:
                rom[write_pos] = x
                write_pos += 3

            # get to the end of the last TSB we edited
            write_pos += 1

            # Write NOPs until the end of the last old TSB
            while write_pos <= 0x3FF84A:
                rom[write_pos] = 0xEA
                write_pos += 1
        else:
            # Need to jump out and write the new TSBs elsewhere

            # 29 bytes starting at 0x3FF82E
            new_rt = bytearray([0x22, 0x00, 0x74, 0x5F])  # JSL $5F7400
            while len(new_rt) < 29:
                new_rt.append(0xEA)  # NOP out the rest

            # There is some junk in the 0x3F bank, and in the future we may
            # write the new routine there for short jump to SR.
            # Or maybe write over the pieces that we took out to expand techs?
            # TODO: Find a better way to pick out free space.

            rom[0x3FF82E:0x3FF84B] = new_rt

            # the new menu rt is just a bunch of TSBs like before and then
            # a JSL
            new_menu_rt = [0xA9, 0x80]
            for x in new_ids:
                new_menu_rt.extend(bytearray([0x0C, x, 0x77]))

            new_menu_rt.append(0x6B)
            rom[0x5F7400:0x5F7400+len(new_menu_rt)] = new_menu_rt

        # Keep attack bits right for now
        for i in range(7):
            rom[0x0C2583+i] = (num_techs - 7 + i)

        # Fixing errant graphics data

        # $C1/820D A9 79       LDA #$79 -- 0x79 is offset for running away gfx
        # It should be 7th from the back.
        rom[0x01820E] = db.gfx_count-7

        # This is greendream loading
        # $C1/B365 A9 7A       LDA #$7A
        # $C1/B367 8D 93 AE    STA $AE93  [$7E:AE93]
        rom[0x01B366] = db.gfx_count-6

        # undo the changes to lrn_req and desc
        db.set_lrn_req_start(old_lrn_req_start)
        db.set_desc_start(old_desc_start)

        # Fixing errant description pointers

        # Fix "Can't run away" message.  Hardcoded description is in with
        # the techs.  We need to fix the index.
        # $C1/1097 A9 75       LDA #$75   Loading "Can't run away" index
        # Vanilla: 0x79 descs, so it's always 4 less than the count.
        num_descs = db.desc_ptr_count
        rom[0x011098] = num_descs-4

        # TODO: Fix "Single Tech" "Dual Tech" page names in X-menu.
        # apparently these are in desc_ptrs too

    # End write_db

    def write_db_internal(db, rom):
        TechDB.write_db(db, rom,
                        db.control_start,
                        db.effect_start,
                        db.gfx_start,
                        db.target_start,
                        db.menu_grp_start,
                        db.bat_grp_start,
                        db.name_start,
                        db.desc_start,
                        db.desc_ptr_start,
                        db.techs_learned_start,
                        db.lrn_req_start,
                        db.lrn_ref_start,
                        db.mp_start,
                        db.menu_req_start,
                        db.group_sizes_start,
                        db.atb_pen_start)

    def write_db_internal_file(db, filename):
        with open(filename, 'r+b') as outfile:
            rom = outfile.read()
            TechDB.write_db_internal(db, rom)

            outfile.seek(0)
            outfile.write(rom)

    def write_default_db_file(db, filename):
        with open(filename, 'r+b') as outfile:
            rom = outfile.read()
            TechDB.write_default_db(db, rom)

            outfile.seek(0)
            outfile.write(rom)

    def write_db_file(db, filename,
                      control_start,
                      effect_start,
                      gfx_start,
                      targets_start,
                      menu_grps_start,
                      bat_grps_start,
                      names_start,
                      desc_start,
                      desc_ptr_start,
                      lrn_req_start,
                      lrn_refs_start,
                      mp_start,
                      menu_mp_reqs_start,
                      group_sizes_start,
                      atb_pen_start):

        with open(filename, 'r+b') as outfile:
            rom = outfile.read()
            TechDB.write_db(db, rom,
                            control_start,
                            effect_start,
                            gfx_start,
                            targets_start,
                            menu_grps_start,
                            bat_grps_start,
                            names_start,
                            desc_start,
                            desc_ptr_start,
                            lrn_req_start,
                            lrn_refs_start,
                            mp_start,
                            menu_mp_reqs_start,
                            group_sizes_start,
                            atb_pen_start)

            outfile.seek(0)
            outfile.write(rom)


# Main method to test the techdb
# This is just a sanity check that reading and rewriting the existing db
# does not change the rom.
if __name__ == '__main__':
    with open('test.sfc', 'rb') as infile, \
         open('test-out.sfc', 'wb') as outfile:

        rom = bytearray(infile.read())
        db = TechDB.get_default_db(rom)

        testrom = rom[:]

        # FF over the data
        TechDB.write_db_ff_internal(db, testrom)
        # Write it back.
        TechDB.write_db_internal(db, testrom)

        # get a single, dual, trip, rock
        tech1 = db.get_tech(5)
        tech2 = db.get_tech(0x45)
        tech3 = db.get_tech(0x68)
        tech4 = db.get_tech(0x71)

        # write them back
        db.set_tech(tech1, 5)
        db.set_tech(tech2, 0x45)
        db.set_tech(tech3, 0x68)
        db.set_tech(tech4, 0x71)

        is_diff = False

        for i in range(0, len(rom)):
            if rom[i] != testrom[i]:
                is_diff = True
                print("Difference in byte %6.6X.  Old = %2.2X, New= %2.2X"
                      % (i, rom[i], testrom[i]))

        if not is_diff:
            print("Rewriting default db did not alter the rom. Pass.")
        else:
            print("Unexpected change to rom. Fail.")
