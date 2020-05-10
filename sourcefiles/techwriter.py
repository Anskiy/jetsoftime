import random as rand
import struct as st

cyclone = {"attack_byte": 0x04, "effect": 0, "tech_id": 1, "efpointer": [3,0,0,0x3A,0x3B,1,0x3E,0x80,0x80,0x0A,4,0], 
"anim": [1,0xDA,0xEF,0x20,1,1,0xFF], "text": [0xA2,0xD2,0xBC,0xC5,0xC8,0xC7,0xBE,0xEF,0xEF,0xEF,0xEF], 
"descpointer": [0x0E,0x3B], "mp_cost": 2, "targeting": [0x12,3]}
slash = {"attack_byte": 0x82, "effect": 7, "tech_id": 2, "efpointer": [3,0,0,0,0,3,0x3C,0x70,0,0x0A,0,0],
"anim": [2,0xE8,0xEC,0x21,2,2,0xFF], "text": [0xB2,0xC5,0xBA,0xCC,0xC1,0xEF,0xEF,0xEF,0xEF,0xEF,0xEF], 
"descpointer": [0x21,0x3B], "mp_cost": 2, "targeting": [0x0B,1]}
lightning = {"attack_byte": 0x82, "effect": 7, "tech_id": 3, "efpointer": [3,0,0,0,0,3,0x3C,0x70,0,0x0C,0,0], 
"anim": [3,0xF1,0,0x22,3,3,0x45], "text": [0x2F,0xAB,0xC2,0xC0,0xC1,0xCD,0xC7,0xC2,0xC7,0xC0,0xEF], 
"descpointer": [0x2B,0x3B], "mp_cost": 4, "targeting": [7,0]}
spincut = {"attack_byte": 0x04, "effect": 0, "tech_id": 4, "efpointer": [3,0,0,0x3A,0x3B,1,0x3E,0x80,0x80,0x10,4,0x80], 
"anim": [4,0xD6,0,0x27,4,4,0xFF], "text": [0xB2,0xC9,0xC2,0xC7,0xBC,0xCE,0xCD,0xEF,0xEF,0xEF,0xEF], 
"descpointer": [0x39,0x3B], "mp_cost": 6, "targeting": [7,0]}
lightning2 = {"attack_byte": 0x82, "effect": 7, "tech_id": 5, "efpointer": [3,0,0,0,0,3,0x3C,0x70,0,0x0E,0,0],
"anim": [5,0xF1,0,0x22,5,3,2], "text": [0x2F,0xAB,0xC2,0xC0,0xC1,0xCD,0xC7,0xC2,0xC7,0xC0,0xD6], 
"descpointer": [0x43,0x3B], "mp_cost": 8, "targeting": [8,0]}
life = {"attack_byte": 0, "effect": 0, "tech_id": 6, "efpointer": [1,0xD0,0x80,0,0,0,0,0xA0,0,0,0,0], 	
"anim": [6,0xE1,2,0x1B,6,6,0x1D], "text": [0x2F,0xAB,0xC2,0xBF,0xBE,0xEF,0xEF,0xEF,0xEF,0xEF,0xEF], 
"descpointer": [0x52,0x3B], "mp_cost": 10, "targeting": [3,0]}
confuse = {"attack_byte": 4, "effect": 0x14, "tech_id": 7, "efpointer": [8,4,0,0x3A,0x3B,1,0x3E,0x80,0x80,0x1D,4,0],
"anim": [7,0x20,0x24,0x2D,7,7,0xFF], "text": [0xA2,0xC8,0xC7,0xBF,0xCE,0xCC,0xBE,0xEF,0xEF,0xEF,0xEF], 
"descpointer": [0x64,0x3B], "mp_cost": 15, "targeting": [7,0]}
luminaire = {"attack_byte": 0x82, "effect": 7, "tech_id": 8, "efpointer": [3,0,0,0,0,3,0x3C,0x70,0,0x32,0,0],
"anim": [8,0xFC,0,8,8,8,1], "text": [0x2F,0xAB,0xCE,0xC6,0xC2,0xC7,0xBA,0xC2,0xCB,0xBE,0xEF],
"descpointer": [0x7E,0x3B], "mp_cost": 20, "targeting": [8,0]}
aura = {"attack_byte": 0x00, "effect": 0, "tech_id": 9, "efpointer": [0,8,0x80,0,0,0,0,0,0,0,0,0],
"anim": [9,0xE1,0xE5,0x1D,9,9,0xFF], "text": [0xA0,0xCE,0xCB,0xBA,0xEF,0xEF,0xEF,0xEF,0xEF,0xEF,0xEF],
"descpointer": [0x96,0x3B], "mp_cost": 1, "targeting": [0x80,00]}
provoke = {"attack_byte": 0x02, "effect": 0, "tech_id": 0xA, "efpointer": [2,1,4,00,00,0x50,00,0x70,00,00,00,00],
"anim": [0x0A,0x0A,0x0E,0x0E,0x0A,0x0A,0xFF], "text": [0xAF,0xCB,0xC8,0xCF,0xC8,0xC4,0xBE,0xEF,0xEF,0xEF,0xEF],
"descpointer": [0xA7,0x3B], "mp_cost": 1, "targeting": [7,0]}
ice = {"attack_byte": 0x22, "effect": 7, "tech_id": 0xB, "efpointer": [3,00,00,00,00,3,0x3C,0x70,0,0x0C,00,00],
"anim": [0x0C,0xF4,00,0x25,0x3A,0x0C,0x44], "text": [0x2F,0xA8,0xBC,0xBE,0xEF,0xEF,0xEF,0xEF,0xEF,0xEF,0xEF],
"descpointer": [0xB2,0x3B], "mp_cost": 4, "targeting": [7,0]}
cure = {"attack_byte": 0x00, "effect": 0, "tech_id": 0xC, "efpointer": [00,0x0C,0x80,00,00,00,00,00,00,00,00,00],
"anim": [0x0B,0xE1,2,0x1E,0x0B,0x0B,0xFF], "text": [0x2F,0xA2,0xCE,0xCB,0xBE,0xEF,0xEF,0xEF,0xEF,0xEF,0xEF],
"descpointer": [0xC3,0x3B], "mp_cost": 4, "targeting": [0x80,0]}
haste = {"attack_byte": 0x00, "effect": 0, "tech_id": 0xD, "efpointer": [2,3,0x80,00,00,00,00,0x70,00,00,00,00],
"anim": [0x0D,0xBB,00,0x3E,0x0D,0x0D,0x56], "text": [0x2F,0xA7,0xBA,0xCC,0xCD,0xBE,0xEF,0xEF,0xEF,0xEF,0xEF],
"descpointer": [0xD0,0x3B], "mp_cost": 6, "targeting": [0,0]}
ice2 = {"attack_byte": 0x22, "effect": 7, "tech_id": 0xE, "efpointer": [3,00,00,00,00,3,0x3C,0x70,00,0x18,00,00],
"anim": [0x0F,0xFC,00,0x25,0x3A,0x0C,0x57], "text": [0x2F,0xA8,0xBC,0xBE,0xFF,0xD6,0xEF,0xEF,0xEF,0xEF,0xEF],
"descpointer": [0xE7,0x3B], "mp_cost": 8, "targeting": [8,00]}
cure2 = {"attack_byte": 0x00, "effect": 0, "tech_id": 0xF, "efpointer": [1,0x55,0x80,00,00,00,00,00,00,00,00,00],
"anim": [0x0E,0xE1,2,0x1F,0x0B,0x0E,0xFF], "text": [0x2F,0xA2,0xCE,0xCB,0xBE,0xFF,0xD6,0xEF,0xEF,0xEF,0xEF],
"descpointer": [0xFE,0x3B], "mp_cost": 8, "targeting": [0x80,0]}
life2 = {"attack_byte": 0x00, "effect": 0, "tech_id": 0x10, "efpointer": [1,0xCF,0x80,00,00,00,00,0x80,00,00,00,00],
"anim": [0x10,0xE1,2,0x1B,6,6,0x35], "text": [0x2F,0xAB,0xC2,0xBF,0xBE,0xFF,0xD6,0xEF,0xEF,0xEF,0xEF],
"descpointer": [0x0C,0x3C], "mp_cost": 15, "targeting": [3,00]}
flametoss = {"attack_byte": 0x12, "effect": 7, "tech_id": 0x11, "efpointer": [3,0,0,0,0,3,0x3C,0x70,0,6,0,0],
"anim": [0x11,0xEB,0,0x23,0x11,0x11,0xFF], "text": [0xA5,0xC5,0xBA,0xC6,0xBE,0xFF,0xB3,0xC8,0xCC,0xCC,0xEF],
"descpointer": [0x1E,0x3C], "mp_cost": 1, "targeting": [0x0C,5]}
hypnowave = {"attack_byte": 0x02, "effect": 0, "tech_id": 0x12, "efpointer": [2,1,2,0,0,0x3C,0x0A,0x70,0,0,0,0],
"anim": [0x12,0xC9,0xCD,0x15,0x12,0x12,7], "text": [0xA7,0xD2,0xC9,0xC7,0xC8,0xFF,0xB6,0xBA,0xCF,0xBE,0xEF],
"descpointer": [0x31,0x3C], "mp_cost": 5, "targeting": [8,0]}
fire = {"attack_byte": 0x12, "effect": 7, "tech_id": 0x13, "efpointer": [3,0,0,0,0,3,0x3C,0x70,0,0x0C,0,0],
"anim": [0x13,0xEB,0,0x23,0x11,0x13,0xFF], "text": [0x2F,0xA5,0xC2,0xCB,0xBE,0xEF,0xEF,0xEF,0xEF,0xEF,0xEF],
"descpointer": [0x41,0x3C], "mp_cost": 4, "targeting": [7,0]}
napalm = {"attack_byte": 0x12, "effect": 7, "tech_id": 0x14, "efpointer": [3,0,0,0x3A,0x3B,3,0x3C,0x50,0,0x12,0,0x80],
"anim": [0x14,0xF1,0,0x0A,0x14,0x14,0x49], "text": [0xAD,0xBA,0xC9,0xBA,0xC5,0xC6,0xEF,0xEF,0xEF,0xEF,0xEF],
"descpointer": [0x55,0x3C], "mp_cost": 6, "targeting": [0x12,3]}
protect = {"attack_byte": 0, "effect": 0, "tech_id": 0x15, "efpointer": [2,4,4,0,0,0,0,0x70,0,0,0,0],
"anim": [0x15,0xCE,0,0x11,0x15,0x15,0xFF], "text": [0x2F,0xAF,0xCB,0xC8,0xCD,0xBE,0xBC,0xCD,0xEF,0xEF,0xEF],
"descpointer": [0x6B,0x3C], "mp_cost": 6, "targeting": [0,0]}
fire2 = {"attack_byte": 0x12, "effect": 7, "tech_id": 0x16, "efpointer": [3,0,0,0,0,3,0x3C,0x70,0,0x18,0,0],
"anim": [0x16,0xEB,0,0x0B,0x11,0x13,0x1C], "text": [0x2F,0xA5,0xC2,0xCB,0xBE,0xFF,0xD6,0xEF,0xEF,0xEF,0xEF],
"descpointer": [0x7E,0x3C], "mp_cost": 8, "targeting": [8,0]}
megabomb = {"attack_byte": 0x12, "effect": 7, "tech_id": 0x17, "efpointer": [3,0,0,0x3A,0x3B,3,0x3C,0x50,0,0x20,0,0x80],
"anim": [0x17,0xCA,0,0x10,0x17,0x17,0x20], "text": [0xAC,0xBE,0xC0,0xBA,0xFF,0xA1,0xC8,0xC6,0xBB,0xEF,0xEF],
"descpointer": [0x93,0x3C], "mp_cost": 15, "targeting": [0x12,3]}
flare = {"attack_byte": 0x12, "effect": 7, "tech_id": 0x18, "efpointer": [3,0,0,0,0,3,0x3C,0x70,0,0x32,0,0],
"anim": [0x18,0xF1,0,0xA,0x18,0x18,0xD], "text": [0x2F,0xA5,0xC5,0xBA,0xCB,0xBE,0xEF,0xEF,0xEF,0xEF,0xEF],
"descpointer": [0xA9,0x3C], "mp_cost": 0x14, "targeting": [8,0]}
rocketpunch = {"attack_byte": 4, "effect": 0, "tech_id": 0x19, "efpointer": [3,0,0,0x3A,0x3B,1,0x3E,0x80,0x80,0x0B,4,0x80],
"anim": [0x19,0xE6,0xC3,0x24,0x19,0x19,0xFF], "text": [0xB1,0xC8,0xBC,0xC4,0xBE,0xCD,0xAF,0xCE,0xC7,0xBC,0xC1],
"descpointer": [0xBF,0x3C], "mp_cost": 1, "targeting": [7,0]}
curebeam = {"attack_byte": 0, "effect": 0, "tech_id": 0x1A, "efpointer": [0,0xC,0x80,0,0,0,0,0,0,0,0,0],
"anim": [0x1A,0xE1,2,0x1E,0xB,0xB,0x5A], "text": [0xA2,0xCE,0xCB,0xBE,0xFF,0xA1,0xBE,0xBA,0xC6,0xEF,0xEF],
"descpointer": [0xC9,0x3C], "mp_cost": 1, "targeting": [0x80,0]}
laserspin = {"attack_byte": 0x42, "effect": 7, "tech_id": 0x1B, "efpointer": [3,0,0,0,0,3,0x3C,0x70,0,0xC,0,0],
"anim": [0x1C,0x61,0xE0,0x26,0x1B,0x1B,9], "text": [0xAB,0xBA,0xCC,0xBE,0xCB,0xFF,0xB2,0xC9,0xC2,0xC7,0xEF],
"descpointer": [0xDA,0x3C], "mp_cost": 6, "targeting": [8,0]}
robotackle = {"attack_byte": 4, "effect": 0, "tech_id": 0x1C, "efpointer": [3,0,0,0x3A,0x3B,1,0x3E,0x80,0x80,0x10,4,0x80],
"anim": [0x1B,0x61,0xE0,0x26,0x1B,0x1B,9], "text": [0xB1,0xC8,0xBB,0xC8,0xFF,0xB3,0xBA,0xBC,0xC4,0xC5,0xBE],
"descpointer": [0xEC,0x3C], "mp_cost": 6, "targeting": [7,0]}
healbeam = {"attack_byte": 0, "effect": 0, "tech_id": 0x1D, "efpointer": [0,0xC,0x80,0,0,0,0,0,0,0,0,0],
"anim": [0x1D,0xE1,2,0x13,0xB,0xB,0x59], "text": [0xA7,0xBE,0xBA,0xC5,0xFF,0xA1,0xBE,0xBA,0xC6,0xEF,0xEF],
"descpointer": [0xF7,0x3C], "mp_cost": 4, "targeting": [0x81,0]}
uzzipunch = {"attack_byte": 4, "effect": 0, "tech_id": 0x1E, "efpointer": [3,0,0,0x3A,0x3B,1,0x3E,0x80,0x80,0x19,4,0x80],
"anim": [0x1E,0xE6,0xC3,0x24,0x19,0x19,0xFF], "text": [0xB4,0xD3,0xD3,0xC2,0xFF,0xAF,0xCE,0xC7,0xBC,0xC1,0xEF],
"descpointer": [0xB,0x3D], "mp_cost": 15, "targeting": [7,0]}
areabomb = {"attack_byte": 0x12, "effect": 7, "tech_id": 0x1F, "efpointer": [3,0,0,0,0,3,0x3C,0x70,0,0x1E,0,0],
"anim": [0x1F,0xF1,0xF5,0xA,0x1F,0x1F,0x50], "text": [0xA0,0xCB,0xBE,0xBA,0xFF,0xA1,0xC8,0xC6,0xBB,0xEF,0xEF],
"descpointer": [0x20,0x3D], "mp_cost": 14, "targeting": [0x11,2]}
shock = {"attack_byte": 0x82, "effect": 7, "tech_id": 0x20, "efpointer": [3,0,0,0,0,3,0x3C,0x70,0,0x28,0,0],
"anim": [0x20,0x61,0,1,0,0,0x22], "text": [0xB2,0xC1,0xC8,0xBC,0xC4,0xEF,0xEF,0xEF,0xEF,0xEF,0xEF],
"descpointer": [0x36,0x3D], "mp_cost": 17, "targeting": [8,0]}
slurp = {"attack_byte": 0, "effect": 0, "tech_id": 0x21, "efpointer": [0,8,0x80,0,0,0,0,0,0,0,0,0],
"anim": [0x21,0xE1,0,0x1D,9,9,0xFF], "text": [0xB2,0xC5,0xCE,0xCB,0xC9,0xEF,0xEF,0xEF,0xEF,0xEF,0xEF],
"descpointer": [0x51,0x3D], "mp_cost": 1, "targeting": [0x80,0]}
slurpcut = {"attack_byte": 4, "effect": 0, "tech_id": 0x22, "efpointer": [3,0,0,0,0,1,0x3E,0xA0,0x80,0xB,0x24,0xC0],
"anim": [0x22,0xE1,0,0x1D,9,9,0xFF], "text": [0xB2,0xC5,0xCE,0xCB,0xC9,0xFF,0xA2,0xCE,0xCD,0xEF,0xEF],
"descpointer": [0x62,0x3D], "mp_cost": 2, "targeting": [7,0]}
water = {"attack_byte": 0x22, "effect": 7, "tech_id": 0x23, "efpointer": [3,0,0,0,0,3,0x3C,0x70,0,0xC,0,0],
"anim": [0x23,0xF8,0,0x16,0x23,0x23,0xFF], "text": [0x2F,0xB6,0xBA,0xCD,0xBE,0xCB,0xEF,0xEF,0xEF,0xEF,0xEF],
"descpointer": [0x73,0x3D], "mp_cost": 4, "targeting": [7,0]}
heal = {"attack_byte": 0, "effect": 0, "tech_id": 0x24, "efpointer": [0,0xC,0x80,0,0,0,0,0,0,0,0,0],
"anim": [0x24,0xE1,2,0x13,0x24,0x24,0x58], "text": [0x2F,0xA7,0xBE,0xBA,0xC5,0xEF,0xEF,0xEF,0xEF,0xEF,0xEF],
"descpointer": [0x86,0x3D], "mp_cost": 8, "targeting": [0x81,0]}
leapslash = {"attack_byte": 4, "effect": 0, "tech_id": 0x25, "efpointer": [3,0,0,0x3A,0x3B,1,0x3E,0x80,0x80,0x12,4,0x80],
"anim": [0x25,0x61,5,1,0x25,0x25,0xFF], "text": [0xAB,0xBE,0xBA,0xC9,0xFF,0xB2,0xC5,0xBA,0xCC,0xC1,0xEF],
"descpointer": [0x99,0x3D], "mp_cost": 4, "targeting": [7,0]}
water2 = {"attack_byte": 0x22, "effect": 7, "tech_id": 0x26, "efpointer": [3,0,0,0,0,3,0x3C,0x70,0,0x18,0,0],
"anim": [0x26,0xF8,0,0x16,0x23,0x23,0x32], "text": [0x2F,0xB6,0xBA,0xCD,0xBE,0xCB,0xFF,0xD6,0xEF,0xEF,0xEF],
"descpointer": [0xA9,0x3D], "mp_cost": 8, "targeting": [8,0]}
cure2_2 = {"attack_byte": 0, "effect": 0, "tech_id": 0x27, "efpointer": [1,0x55,0x80,0,0,0,0,0,0,0,0,0],
"anim": [0x27,0xE1,2,0x1F,0xB,0xE,0xFF], "text": [0x2F,0xA2,0xCE,0xCB,0xBE,0xFF,0xD6,0xEF,0xEF,0xEF,0xEF],
"descpointer": [0xBF,0x3D], "mp_cost": 8, "targeting": [0x80,0]}
frogsquash = {"attack_byte": 4, "effect": 0, "tech_id": 0x28, "efpointer": [3,0,0,0,0,6,0x3E,0x60,0,0xA,4,0],
"anim": [0x28,0xE0,0,0x1C,0x28,2,0x41], "text": [0xA5,0xCB,0xC8,0xC0,0xFF,0xB2,0xCA,0xCE,0xBA,0xCC,0xC1],
"descpointer": [0xD2,0x3D], "mp_cost": 15, "targeting": [8,0]}
kiss = {"attack_byte": 0, "effect": 0, "tech_id": 0x29, "efpointer": [1,0x50,0x80,0,0,0,0,0xA0,0,0,0,0],
"anim": [0x29,0xE1,5,0x1D,9,9,0xFF], "text": [0xAA,0xC2,0xCC,0xCC,0xEF,0xEF,0xEF,0xEF,0xEF,0xEF,0xEF],
"descpointer": [0xE6,0x3D], "mp_cost": 2, "targeting": [0x80,0]}
rollokick = {"attack_byte": 4, "effect": 0, "tech_id": 0x2A, "efpointer": [3,0,0,0x3A,0x3B,5,0x3E,0x80,0,0xE,4,0x80],
"anim": [0x2A,0x61,5,1,0x25,0x25,0xFF], "text": [0xB1,0xC8,0xC5,0xC5,0xC8,0xFF,0xAA,0xC2,0xBC,0xC4,0xEF],
"descpointer": [0xF9,0x3D], "mp_cost": 2, "targeting": [7,0]}
catattack = {"attack_byte": 4, "effect": 0, "tech_id": 0x2B, "efpointer": [3,0,0,0x3A,0x3B,5,0x3E,0x80,0,0x19,4,0],
"anim": [0x2B,0x61,0,1,0,0,0xFF], "text": [0xA2,0xBA,0xCD,0xFF,0xA0,0xCD,0xCD,0xBA,0xBC,0xC4,0xEF],
"descpointer": [8,0x3E], "mp_cost": 4, "targeting": [7,0]}
rockthrow = {"attack_byte": 4, "effect": 0, "tech_id": 0x2C, "efpointer": [3,0,0,0x3A,0x3B,5,0x3E,0x80,0,0x1E,0x46,0xC0],
"anim": [0x2C,0x61,0,1,0,0,0xFF], "text": [0xB1,0xC8,0xBC,0xC4,0xFF,0xB3,0xC1,0xCB,0xC8,0xD0,0xEF],
"descpointer": [0x18,0x3E], "mp_cost": 6, "targeting": [7,0]}
charm = {"attack_byte": 2, "effect": 0xF, "tech_id": 0x2D, "efpointer": [6,0x46,0,0,0,0,0,0x80,0,0,0,0x80],
"anim": [0x2D,0xC0,5,0xF,0x2D,0x2D,0xFF], "text": [0xA2,0xC1,0xBA,0xCB,0xC6,0xEF,0xEF,0xEF,0xEF,0xEF,0xEF],
"descpointer": [0x23,0x3E], "mp_cost": 4, "targeting": [7,0]}
tailspin = {"attack_byte": 2, "effect": 0, "tech_id": 0x2E, "efpointer": [3,0,0,0,0,3,0,0x70,0,0xC,0,0],
"anim": [0x2F,0x61,0,1,0,0,6], "text": [0xB3,0xBA,0xC2,0xC5,0xFF,0xB2,0xC9,0xC2,0xC7,0xEF,0xEF],
"descpointer": [0x30,0x3E], "mp_cost": 4, "targeting": [7,0]}
dinotail = {"attack_byte": 4, "effect": 0, "tech_id": 0x2F, "efpointer": [3,0,0,0,0,6,0x3E,0xA0,0,9,4,0],
"anim": [0x30,0x61,0,1,0x30,1,0xE], "text": [0xA3,0xC2,0xC7,0xC8,0xFF,0xB3,0xBA,0xC2,0xC5,0xEF,0xEF],
"descpointer": [0x48,0x3E], "mp_cost": 15, "targeting": [8,0]}
triplekick = {"attack_byte": 4, "effect": 0x13, "tech_id": 0x30, "efpointer": [8,3,0,0x3A,0x3B,5,0x3E,0x80,0,0x32,4,0],
"anim": [0x2E,0x61,5,1,0x25,0x25,0xFF], "text": [0xB3,0xCB,0xC2,0xC9,0xC5,0xBE,0xFF,0xAA,0xC2,0xBC,0xC4],
"descpointer": [0x5C,0x3E], "mp_cost": 20, "targeting": [7,0]}
lightning2_2 = {"attack_byte": 0x82, "effect": 7, "tech_id": 0x31, "efpointer": [3,0,0,0,0,3,0x3C,0x70,0,0xC,0,0],
"anim": [0x31,0xF1,0,0x22,3,3,2], "text": [0x2F,0xAB,0xC2,0xC0,0xC1,0xCD,0xC7,0xC2,0xC7,0xC0,0xD6],
"descpointer": [0x76,0x3E], "mp_cost": 4, "targeting": [8,0]}
ice2_2 = {"attack_byte": 0x22, "effect": 7, "tech_id": 0x32, "efpointer": [3,0,0,0,0,3,0x3C,0x70,0,0xC,0,0],
"anim": [0x35,0xFC,0,0x25,0x3A,0xC,0x57], "text": [0x2F,0xA8,0xBC,0xBE,0xFF,0xD6,0xEF,0xEF,0xEF,0xEF,0xEF],
"descpointer": [0x8B,0x3E], "mp_cost": 4, "targeting": [8,0]}
fire2_2 = {"attack_byte": 0x12, "effect": 7, "tech_id": 0x33, "efpointer": [3,0,0,0,0,3,0x3C,0x70,0,0xC,0,0],
"anim": [0x33,0xEB,0,0xB,0x11,0x13,0x1C], "text": [0x2F,0xA5,0xC2,0xCB,0xBE,0xFF,0xD6,0xEF,0xEF,0xEF,0xEF],
"descpointer": [0x9E,0x3E], "mp_cost": 4, "targeting": [8,0]}
darkbomb = {"attack_byte": 0x42, "effect": 7, "tech_id": 0x34, "efpointer": [3,0,0,0,0,3,0x3C,0x70,0,0x19,0,0],
"anim": [0x34,0xF1,4,0xA,0x34,0x34,0x21], "text": [0x2F,0xA3,0xBA,0xCB,0xC4,0xFF,0xA1,0xC8,0xC6,0xBB,0xEF],
"descpointer": [0xB2,0x3E], "mp_cost": 8, "targeting": [0x12,3]}
magicwall = {"attack_byte": 0, "effect": 0, "tech_id": 0x35, "efpointer": [2,4,0x40,0,0,0,0,0x70,0,0,0,0],
"anim": [0x36,0xCE,4,0x12,0x34,0x36,0xFF], "text": [0x2F,0xAC,0xBA,0xC0,0xC2,0xBC,0xFF,0xB6,0xBA,0xC5,0xC5],
"descpointer": [0xCA,0x3E], "mp_cost": 6, "targeting": [0,0]}
darkmist = {"attack_byte": 0x42, "effect": 7, "tech_id": 0x36, "efpointer": [3,0,0,0,0,3,0x3C,0x70,0,0x19,0,0],
"anim": [0x32,0xF8,4,0xA,0x34,0x34,0x2F], "text": [0x2F,0xA3,0xBA,0xCB,0xC4,0xFF,0xAC,0xC2,0xCC,0xCD,0xEF],
"descpointer": [0xDB,0x3E], "mp_cost": 10, "targeting": [8,0]}
blackhole = {"attack_byte": 2, "effect": 0x24, "tech_id": 0x37, "efpointer": [3,0,0,0,0,3,0x3C,0x70,0,2,0,0],
"anim": [0x37,0xF1,4,0xA,0x34,0x34,8], "text": [0x2F,0xA1,0xC5,0xBA,0xBC,0xC4,0xFF,0xA7,0xC8,0xC5,0xBE],
"descpointer": [0xF3,0x3E], "mp_cost": 15, "targeting": [0x1B,0xA]}
darkmatter = {"attack_byte": 0x42, "effect": 7, "tech_id": 0x38, "efpointer": [3,0,0,0,0,3,0x3C,0x70,0,0x2A,0,0],
"anim": [0x38,0xF1,4,0xA,0x34,0x34,0x1E], "text": [0x2F,0xA3,0xBA,0xCB,0xC4,0xAC,0xBA,0xCD,0xCD,0xBE,0xCB],
"descpointer": [2,0x3F], "mp_cost": 20, "targeting": [8,0]}
new_ids = {"cyclone": "", "slash": "", "lightning": "", "spincut": "", "lightning2": "", "life": "", "confuse": "",
"luminaire": "", "aura": "", "provoke": "", "ice": "", "cure": "", "haste": "", "ice2": "", "cure2": "", "life2": "",
"flametoss": "", "hypnowave": "", "fire": "", "napalm": "", "protect": "", "fire2": "", "megabomb": "", "flare": "",
"rocketpunch": "", "curebeam" : "", "laserspin" : "", "robotackle": "", "healbeam": "", "uzzipunch": "", 
"areabomb": "", "shock": "", "slurp": "", "slurpcut": "", "water": "", "heal": "", "leapslash": "", "water2": "",
"cure2_2": "", "frogsquash": "", "kiss": "", "rollokick": "", "catattack": "", "rockthrow": "", "charm": "", 
"tailspin": "", "dinotail": "", "triplekick": "", "lightning2_2": "", "ice2_2": "", "fire2_2": "", "darkbomb": "",
"magicwall": "", "darkmist": "", "blackhole": "", "darkmatter": ""}
global control_pointer
control_pointer = 0xC1BF6
global effect_pointer
effect_pointer = 0xC214B
global animation_pointer
animation_pointer = 0xD45AD
global mp_pointer
mp_pointer = 0xC253C
global targeting_pointer
targeting_pointer = 0xC1ACD
global text_pointer
text_pointer = 0xC15CF
global describe_pointer
describe_pointer = 0xC3A0B
"""effect_offsets = effect_pointer + ("tech_id"-1) * 12
animation_offsets = animation_pointer + ("tech_id"-1) * 7
mp_offsets = mp_pointer + ("tech_id"-1) * 1
targeting_offsets = targeting_pointer + ("tech_id"-1) * 2
text_offset = text_pointer + ("tech_id"-1) * 11
describe_offset = describe_pointer + ("tech_id"-1) * 2"""

def randomize_tech_order(character):
    i = 0
    new_id_names = ["cyclone", "slash", "lightning", "spincut", "lightning2", "life", "confuse", "luminaire", "aura", 
    "provoke", "ice", "cure", "haste", "ice2", "cure2", "life2", "flametoss", "hypnowave", "fire", "napalm", 
    "protect", "fire2", "megabomb", "flare", "rocketpunch", "curebeam", "laserspin", "robotackle", "healbeam", 
    "uzzipunch", "areabomb", "shock", "slurp", "slurpcut", "water", "heal", "leapslash", "water2", "cure2_2", 
    "frogsquash", "kiss", "rollokick", "catattack", "rockthrow", "charm", "tailspin", "dinotail", "triplekick", 
    "lightning2_2", "ice2_2", "fire2_2", "darkbomb", "magicwall", "darkmist", "blackhole", "darkmatter"]
    avail_techs = character.copy()
    while i < len(character):
          picked_tech = rand.choice(avail_techs)
          control_offset = control_pointer + ((character[i]["tech_id"]-1) * 11)
          control_offset1 = control_offset + 3
          write_bytes(picked_tech["attack_byte"],control_offset1)
          control_offset2 = control_offset + 8
          write_bytes(picked_tech["effect"],control_offset2)
          effect_offset = effect_pointer + ((character[i]["tech_id"]-1) * 12)
          write_bytes(picked_tech["efpointer"],effect_offset)
          animation_offset = animation_pointer + ((character[i]["tech_id"]-1) * 7)
          write_bytes(picked_tech["anim"],animation_offset)
          text_offset = text_pointer + ((character[i]["tech_id"]-1) * 11)
          write_bytes(picked_tech["text"],text_offset)
          describe_offset = describe_pointer + ((character[i]["tech_id"]-1) * 2)
          write_bytes(picked_tech["descpointer"],describe_offset)
          mp_offset = mp_pointer + ((character[i]["tech_id"]-1) * 1)
          write_bytes(picked_tech["mp_cost"],mp_offset)
          targeting_offset = targeting_pointer + ((character[i]["tech_id"]-1) * 2)
          write_bytes(picked_tech["targeting"],targeting_offset)
          new_ids[new_id_names[picked_tech["tech_id"]-1]] = character[i]["tech_id"]
          avail_techs.remove(picked_tech)
          i += 1
def rewrite_menu_techs():
    menu_start = 0x3FF831
    menu_techs = ["aura","cure","cure2","curebeam","healbeam","slurp","heal","cure2_2","kiss"]
    menu_i = 0
    tech_i = 0
    while tech_i < len(menu_techs):
        file_pointer.seek(menu_start + menu_i)
        file_pointer.write(st.pack("B",new_ids[menu_techs[tech_i]]))
        menu_i += 3
        tech_i += 1

def rewrite_combo_techs():
    combo_tech_address = 0xC1E63
    combo_tech_requirements = 0xC27FA
    file_pointer.seek(combo_tech_address)
    #List of dual techs below
    #Techs which are ORed with 0x80 are not directly used in the tech, and only exist to consume MP.
    #Aura Whirl
    file_pointer.write(st.pack("B",new_ids["aura"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",0x80 | new_ids["cyclone"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["cyclone"]))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["aura"] - 8))
    combo_tech_requirements += 3
    #Ice Sword
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["spincut"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["ice"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["spincut"]))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["ice"] - 8))
    combo_tech_requirements += 3
    #Ice Sword 2
    file_pointer.seek(combo_tech_address+1) 
    #Regardless of tech list order, Ice and Fire Sword 2 use a special version of Confuse that doesn't multihit, so rewriting it isn't necessary
    file_pointer.write(st.pack("B",new_ids["ice2"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["confuse"]))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["ice2"] - 8))
    combo_tech_requirements += 3
	#Fire Whirl
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["cyclone"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["flametoss"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["cyclone"]))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["flametoss"] - 16))
    combo_tech_requirements += 3
    #Fire Sword
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["spincut"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["fire"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["spincut"]))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["fire"] - 16))
    combo_tech_requirements += 3
    #Fire Sword 2
    file_pointer.seek(combo_tech_address+1)#See Ice Sword 2
    file_pointer.write(st.pack("B",new_ids["fire2"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["confuse"]))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["fire2"] - 16))
    combo_tech_requirements += 3
    #Rocket Roll
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["cyclone"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["laserspin"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["cyclone"]))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["laserspin"] - 24))
    combo_tech_requirements += 3
    #Max Cyclone
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["laserspin"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["spincut"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["spincut"]))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["laserspin"] - 24))
    combo_tech_requirements += 3
    #Super Volt
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["lightning2"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["shock"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["lightning2"]))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["shock"] - 24))
    combo_tech_requirements += 3
    #X Strike
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["cyclone"]))
    #Frog uses a different tech to get around Slurp Cut failing on certain enemies, so the next line is skipped
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["cyclone"]))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["slurpcut"] - 32))
    combo_tech_requirements += 3
    #Sword Stream
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["water"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["spincut"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["spincut"]))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["water"] - 32))
    combo_tech_requirements += 3
    #Spire
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["leapslash"]))
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["lightning2"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["lightning2"]))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["leapslash"] - 32))
    combo_tech_requirements += 3
    #Drill Kick
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["rollokick"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["cyclone"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["cyclone"]))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["rollokick"] - 40))
    combo_tech_requirements += 3
    #Volt Bite
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["catattack"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["lightning"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["lightning"]))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["catattack"] - 40))
    combo_tech_requirements += 3
    #Falcon Hit
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",0x80 | new_ids["rockthrow"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["cyclone"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["cyclone"]))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["rockthrow"] - 40))
    combo_tech_requirements += 3
    #Antipode
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["ice"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["fire"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["ice"] - 8))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["fire"] - 16))
    combo_tech_requirements += 3
    #Antipode 2
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["ice2"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["fire2"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["ice2"] - 8))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["fire2"] - 16))
    combo_tech_requirements += 3
    #Antipode 3
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["ice2"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["flare"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["ice2"] - 8))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["flare"] - 16))
    combo_tech_requirements += 3
    #Aura Beam
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["aura"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",0x80 | new_ids["curebeam"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["aura"] - 8))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["curebeam"] - 24))
    combo_tech_requirements += 3 
    #Ice Tackle
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["robotackle"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["ice"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["ice"] - 8))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["robotackle"] - 24))
    combo_tech_requirements += 3
    #Cure Touch
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["cure"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",0x80 | new_ids["healbeam"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["cure"] - 8))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["healbeam"] - 24))
    combo_tech_requirements += 3
    #Ice Water
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["water"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["ice"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["ice"] - 8))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["water"] - 32))
    combo_tech_requirements += 3
    #Glacier
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["water2"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["ice2"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["ice2"] - 8))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["water2"] - 32))
    combo_tech_requirements += 3
    #Double Cure
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["cure2"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["cure2_2"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["cure2"] - 8))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["cure2_2"] - 32))
    combo_tech_requirements += 3
    #Twin Charm
    file_pointer.seek(combo_tech_address+1)#Twin Charm uses a different spell with a higher chance of stealing
    file_pointer.write(st.pack("B",0x80 | new_ids["provoke"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["provoke"] - 8))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["charm"] - 40))
    combo_tech_requirements += 3
    #Ice Toss
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["rockthrow"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["ice"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["ice"] - 8))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["rockthrow"] - 40))
    combo_tech_requirements += 3
    #Cube Toss
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["rockthrow"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["ice2"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["ice2"] - 8))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["rockthrow"] - 40))
    combo_tech_requirements += 3
    #Fire Punch
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["rocketpunch"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["fire"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["fire"] - 16))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["rocketpunch"] - 24))
    combo_tech_requirements += 3
    #Fire Tackle
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["robotackle"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["fire2"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["fire2"] - 16))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["robotackle"] - 24))
    combo_tech_requirements += 3
    #Doublev Bomb
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["areabomb"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["megabomb"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["megabomb"] - 16))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["areabomb"] - 24))
    combo_tech_requirements += 3
    #Flame Kick
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["rollokick"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["fire"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["fire"] - 16))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["rollokick"] - 40))
    combo_tech_requirements += 3
    #Fire Whirl
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["tailspin"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["fire2"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["fire2"] - 16))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["tailspin"] - 40))
    combo_tech_requirements += 3
    #Blaze Kick
    #Like Crono, Ayla uses a different version of Triple Kick that doesn't multihit, so the previous line is skipped.
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["fire2"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["fire2"] - 16))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["triplekick"] - 40))
    combo_tech_requirements += 3
    #Blade Toss
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",0x80 | new_ids["laserspin"]))
    #See X Strike
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["laserspin"] - 24))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["slurpcut"] - 32))
    combo_tech_requirements += 3
    #Bubble Snap
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["robotackle"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["water"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["robotackle"] - 24))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["water"] - 32))
    combo_tech_requirements += 3
    #Cure Wave
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["cure2_2"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B", 0x80 | new_ids["healbeam"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["healbeam"] - 24))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["cure2_2"] - 32))
    combo_tech_requirements += 3
    #Boogie
    file_pointer.seek(combo_tech_address+1)#Boogie uses a unique spell that sets Stop
    file_pointer.write(st.pack("B",0x80 | new_ids["laserspin"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["laserspin"] - 24))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["charm"] - 40))
    combo_tech_requirements += 3
    #Spin Kick
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["rollokick"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["laserspin"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["laserspin"] - 24))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["rollokick"] - 40))
    combo_tech_requirements += 3
    #Beast Toss
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["rockthrow"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["uzzipunch"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["uzzipunch"] - 24))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["rockthrow"] - 40))
    combo_tech_requirements += 3
    #Slurp Kiss
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",0x80 | new_ids["slurp"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["kiss"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["slurp"] - 32))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["kiss"] - 40))
    combo_tech_requirements += 3
    #Bubble Hit
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["rollokick"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["water"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["water"] - 32))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["rollokick"] - 40))
    combo_tech_requirements += 3
    #Drop Kick
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["leapslash"]))
    #See Blaze Kick
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["leapslash"] - 32))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["triplekick"] - 40))
    combo_tech_requirements += 3
    #Red Pin
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["leapslash"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["fire"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["fire"] - 16))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["leapslash"] - 32))
    combo_tech_requirements += 3
    #Line Bomb
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",0x80 | new_ids["leapslash"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["megabomb"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["megabomb"] - 16))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["leapslash"] - 32))
    combo_tech_requirements += 3
    #Frog Flare
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["frogsquash"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["flare"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["flare"] - 16))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["frogsquash"] - 32))
    combo_tech_requirements += 3
    #Delta Force
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["lightning2"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["ice2"]))
    file_pointer.seek(combo_tech_address+2)
    file_pointer.write(st.pack("B",new_ids["fire2"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["lightning2"]))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["ice2"] - 8))
    file_pointer.seek(combo_tech_requirements+2)
    file_pointer.write(st.pack("B",new_ids["fire2"] - 16))
    combo_tech_requirements += 3
    #Lifeline
    file_pointer.seek(combo_tech_address+1)#Lifeline uses a unique spell to set GreenDream effect
    file_pointer.write(st.pack("B",0x80 | new_ids["life"]))
    file_pointer.seek(combo_tech_address+2)
    file_pointer.write(st.pack("B",0x80 | new_ids["laserspin"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["cyclone"]))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["life2"] - 8))
    file_pointer.seek(combo_tech_requirements+2)
    file_pointer.write(st.pack("B",new_ids["laserspin"] - 24))
    combo_tech_requirements += 3
    #Arc Impulse
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["spincut"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["leapslash"]))
    file_pointer.seek(combo_tech_address+2)
    file_pointer.write(st.pack("B",new_ids["ice2"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["spincut"]))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["ice2"] - 8))
    file_pointer.seek(combo_tech_requirements+2)
    file_pointer.write(st.pack("B",new_ids["leapslash"] - 32))
    combo_tech_requirements += 3
    #Final Kick
    #See Blaze Kick
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["lightning2"]))
    file_pointer.seek(combo_tech_address+2)
    file_pointer.write(st.pack("B",new_ids["ice2"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["lightning2"]))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["ice2"] - 8))
    file_pointer.seek(combo_tech_requirements+2)
    file_pointer.write(st.pack("B",new_ids["triplekick"] - 40))
    combo_tech_requirements += 3
    #Fire Zone
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",0x80 | new_ids["robotackle"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["spincut"]))
    file_pointer.seek(combo_tech_address+2)
    file_pointer.write(st.pack("B",new_ids["fire2"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["spincut"]))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["fire2"] - 16))
    file_pointer.seek(combo_tech_requirements+2)
    file_pointer.write(st.pack("B",new_ids["laserspin"] - 24))
    combo_tech_requirements += 3
    #Delta Storm
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["lightning2"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["fire2"]))
    file_pointer.seek(combo_tech_address+2)
    file_pointer.write(st.pack("B",new_ids["water2"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["lightning2"]))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["fire2"] - 16))
    file_pointer.seek(combo_tech_requirements+2)
    file_pointer.write(st.pack("B",new_ids["water2"] - 32))
    combo_tech_requirements += 3
    #Gatling Kick
    #See Blaze Kick
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["lightning2"]))
    file_pointer.seek(combo_tech_address+2)
    file_pointer.write(st.pack("B",new_ids["fire2"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["lightning2"]))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["fire2"] - 16))
    file_pointer.seek(combo_tech_requirements+2)
    file_pointer.write(st.pack("B",new_ids["triplekick"] - 40))
    combo_tech_requirements += 3
    #Triple Raid
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["cyclone"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["robotackle"]))
    #See X Strike
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["cyclone"]))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["robotackle"] - 24))
    file_pointer.seek(combo_tech_requirements+2)
    file_pointer.write(st.pack("B",new_ids["slurpcut"] - 32))
    combo_tech_requirements += 3
    #Twister
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["cyclone"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["laserspin"]))
    file_pointer.seek(combo_tech_address+2)
    file_pointer.write(st.pack("B",new_ids["tailspin"]))
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["cyclone"]))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["laserspin"] - 24))
    file_pointer.seek(combo_tech_requirements+2)
    file_pointer.write(st.pack("B",new_ids["tailspin"] - 40))
    combo_tech_requirements += 3
    #3D Attack
    #See Blaze Kick
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["cyclone"]))
	#See X Strike
    combo_tech_address += 11
    file_pointer.seek(combo_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["cyclone"]))
    file_pointer.seek(combo_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["slurpcut"] - 32))
    file_pointer.seek(combo_tech_requirements+2)
    file_pointer.write(st.pack("B",new_ids["triplekick"] - 40))
    #Dark Eternal
    rock_tech_requirements = 0xC2953
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["ice2"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["fire2"]))
    file_pointer.seek(combo_tech_address+2)
    file_pointer.write(st.pack("B",new_ids["darkmatter"]))
    combo_tech_address += 11
    file_pointer.seek(rock_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["ice2"]))
    file_pointer.seek(rock_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["fire2"]))
    file_pointer.seek(rock_tech_requirements+2)
    file_pointer.write(st.pack("B",new_ids["darkmatter"]))
    rock_tech_requirements += 3
    #Omega Flare
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["flare"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",new_ids["laserspin"]))
    file_pointer.seek(combo_tech_address+2)
    file_pointer.write(st.pack("B",new_ids["darkbomb"]))
    combo_tech_address += 11
    file_pointer.seek(rock_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["flare"]))
    file_pointer.seek(rock_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["laserspin"]))
    file_pointer.seek(rock_tech_requirements+2)
    file_pointer.write(st.pack("B",new_ids["darkbomb"]))
    rock_tech_requirements += 3
    #Spin Strike
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",new_ids["leapslash"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",0x80 | new_ids["robotackle"]))
    file_pointer.seek(combo_tech_address+2)
    file_pointer.write(st.pack("B",0x80 | new_ids["dinotail"]))
    combo_tech_address += 11
    file_pointer.seek(rock_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["robotackle"]))
    file_pointer.seek(rock_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["leapslash"]))
    file_pointer.seek(rock_tech_requirements+2)
    file_pointer.write(st.pack("B",new_ids["tailspin"]))
    rock_tech_requirements += 3
    #Poyozo Dance
    file_pointer.seek(combo_tech_address)
    file_pointer.write(st.pack("B",0x80 | new_ids["provoke"]))
    file_pointer.seek(combo_tech_address+1)
    file_pointer.write(st.pack("B",0x80 | new_ids["hypnowave"]))
    file_pointer.seek(combo_tech_address+2)
    file_pointer.write(st.pack("B", new_ids["tailspin"]))
    combo_tech_address += 11
    file_pointer.seek(rock_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["provoke"]))
    file_pointer.seek(rock_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["hypnowave"]))
    file_pointer.seek(rock_tech_requirements+2)
    file_pointer.write(st.pack("B",new_ids["tailspin"]))
    rock_tech_requirements += 3
    #Grand Dream
    file_pointer.seek(combo_tech_address+1)#Grand Dream uses a unique spell that's stronger than Frog Squash
    file_pointer.write(st.pack("B",0x80 | new_ids["life2"]))
    file_pointer.seek(combo_tech_address+2)
    file_pointer.write(st.pack("B",0x80 | new_ids["healbeam"]))
    file_pointer.seek(rock_tech_requirements)
    file_pointer.write(st.pack("B",new_ids["life2"]))
    file_pointer.seek(rock_tech_requirements+1)
    file_pointer.write(st.pack("B",new_ids["healbeam"]))
    file_pointer.seek(rock_tech_requirements+2)
    file_pointer.write(st.pack("B",new_ids["frogsquash"]))
def write_bytes(array,pointer):
    if isinstance(array,int):
       file_pointer.seek(pointer)
       file_pointer.write(st.pack("B",array))
    elif isinstance(array,list):
        for byte in array:
           file_pointer.seek(pointer)
           file_pointer.write(st.pack("B",byte))
           pointer += 1

def take_pointer(pointer):
    global file_pointer
    file_pointer = pointer
    file_pointer = open(file_pointer,"r+b")
    crono = [cyclone,slash,lightning,spincut,lightning2,life,confuse,luminaire]
    marle = [aura,provoke,ice,cure,haste,ice2,cure2,life2]
    lucca = [flametoss,hypnowave,fire,napalm,protect,fire2,megabomb,flare]
    robo = [rocketpunch,curebeam,laserspin,robotackle,healbeam,uzzipunch,areabomb,shock]
    frog = [slurp,slurpcut,water,heal,leapslash,water2,cure2_2,frogsquash]
    ayla = [kiss,rollokick,catattack,rockthrow,charm,tailspin,dinotail,triplekick]
    magus = [lightning2_2,ice2_2,fire2_2,darkbomb,magicwall,darkmist,blackhole,darkmatter]
    chars = [crono, marle, lucca, robo, frog, ayla, magus]
    for character in chars:
        randomize_tech_order(character)
    rewrite_menu_techs()
    rewrite_combo_techs()
    file_pointer.close()