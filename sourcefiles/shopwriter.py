import struct as st
import random as rand
shop_starts = list(range(0xC2C6F,0xC2C9D,2))
regular_shops = [0xC2C6F,0xC2C73,0xC2C77,0xC2C79,0xC2C85] + list(range(0xC2C89,0xC2C91,2))
good_shops = [0xC2C71,0xC2C75,0xC2C7D,0xC2C81,0xC2C83,0xC2C87,0xC2C93,0xC2C97,0xC2C99]
best_shops = [0xC2C7B,0xC2C7F,0xC2C9B]
forbid_shops = [0xC2C91,0xC2C95]
lowweapons = [0x01,0x02,0x03,0x11,0x12,0x13,0x1F,0x20,0x21,0x2E,0x2F,0x30,0x3B,0x3C]
lowarmors = [0x7C,0x7D,0x7E,0x7F,0x5B,0x5C,0x5D,0x5E,0x5F]
lowaccies = [0x95,0x98,0x99,0x97,0xAC,0xA6,0x96,0xA4]
lowconsumes = [0xBD,0xC6]
midweapons = [0x04,0x05,0x06,0x0F,0x14,0x15,0x22,0x23,0x24,0x29,0x31,0x32,0x33]
midarmors = [0x80,0x81,0x82,0x83,0x84,0x85,0x88,0x8C,0x8D,0x60,0x61,0x62,0x63,0x64,0x65,0x66,0x67]
midaccies = [0xAB,0xA7,0x9C,0x9E,0xB6,0xB4,0x9D,0xA0]
midconsumes = [0xBE,0xC0,0xC1,0xC7,0xC8]
highweapons = [0x08,0x09,0x0A,0x0B,0x10,0x16,0x17,0x25,0x26,0x34,0x35,0x3E,0x3F]
higharmors = [0x8B,0x8E,0x89,0x79,0x75,0x76,0x77,0x78,0x68,0x69,0x6E]
highaccies = [0xA1,0xA5,0xB7,0xA8,0xA9,0x9F,0xB9]
highconsumes = [0xCA,0xCB,0xCC,0xBF,0xC2,0xC4,0xC3,0xC5]
bestweapons = [0x0E,0x55,0x19,0x28,0x38,0x39,0x4E]
bestarmors = [0x91,0x86,0x8F,0x6B,0x6D,0x6C]
bestaccies = [0xA3,0xBB]
bestconsumes = [0xC3,0xC5]
def pick_items(shop,rand_num):
    if shop in regular_shops:
        if rand_num <= 3 :
            item = rand.choice(rand.choice([lowconsumes,midconsumes]))
        elif rand_num > 3 and rand_num <= 7:
            item = rand.choice(rand.choice([lowarmors,midarmors]))
        elif rand_num > 7 and rand_num <= 11:
            item = rand.choice(rand.choice([lowweapons,midweapons]))
        elif rand_num > 11 and rand_num <= 15:
            item = rand.choice(rand.choice([lowaccies,midaccies]))
    elif shop in good_shops:
        if rand_num <= 3:
            item = rand.choice(rand.choice([midconsumes,highconsumes]))
        elif rand_num > 3 and rand_num <= 7:
            item = rand.choice(rand.choice([midarmors,higharmors]))
        elif rand_num > 7 and rand_num <= 11:
            item = rand.choice(rand.choice([midweapons,highweapons]))
        elif rand_num > 11 and rand_num <= 15:
            item =  rand.choice(rand.choice([midaccies,highaccies]))
    elif shop in best_shops:
        if rand_num <= 3:
            item = rand.choice(rand.choice([highconsumes,bestconsumes]))
        elif rand_num > 3 and rand_num <= 7:
            item = rand.choice(rand.choice([higharmors,bestarmors]))
        elif rand_num > 7 and rand_num <= 11:
            item = rand.choice(rand.choice([highweapons,bestweapons]))
        elif rand_num > 11 and rand_num <= 15:
            item = rand.choice(rand.choice([highaccies,bestaccies]))
    return item
def write_slots(file_pointer,shop_start,items,shop_address):
    buffer = []
    req_item_count = 0
    while items > 0:
       if items == 1:
            item = 0x00
       else:
            rand_num = rand.randrange(0,16,1)	
            item = pick_items(shop_start,rand_num)
       if item in buffer:
            continue
       buffer.append(item)
       file_pointer.seek(shop_address)
       file_pointer.write(st.pack("B",item))
       shop_address += 1
       items -= 1
    return shop_address
def warranty_shop(file_pointer):
    shop_address = 0x1AFC29
    guaranteed_items = [0x0,0xC8,0xC7,rand.choice([0x6,0x7]),rand.choice([0x15,0x16]),rand.choice([0x24,0x25]),
    rand.choice([0x31,0x32]),0x3E]
    shop_size = len(guaranteed_items) - 1
    while shop_size > -1:
            shop_address = write_guarantee(file_pointer,shop_address,guaranteed_items[shop_size],shop_size)
            shop_size -= 1
def write_guarantee(file_pointer,shop_address,item,shop_size):
    file_pointer.seek(shop_address)
    file_pointer.write(st.pack("B",item))
    shop_address += 1
    return shop_address
def randomize_shops(outfile):
   shop_pointer = 0xFC31
   shop_address = 0x1AFC31
   f = open(outfile,"r+b")
   warranty_shop(f)
   for start in shop_starts:
     if start in forbid_shops:
        f.seek(start)
        f.write(st.pack("H",shop_pointer + 1))
        continue
     shop_items = rand.randrange(4,10)
     f.seek(start)
     f.write(st.pack("H",shop_pointer))
     shop_pointer += shop_items
     shop_address = write_slots(f,start,shop_items,shop_address)
if __name__ == "__main__":
   randomize_shops("Project.sfc")