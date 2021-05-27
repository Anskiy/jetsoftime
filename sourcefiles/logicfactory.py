import enum

import logictypes
from logictypes import *

#
# The LogicFactory is used by the logic writer to get a GameConfig
# object for the flags that the user selected.  The returned GameConfig
# object holds a list of all LocationGroups, KeyItems, and a configured
# Game object.  These are used by the logic writer to handle key item placement.
#
# TODO: There is some duplication in locations between the different GameConfig
#       objects.  Optimally the locations would be defined once and referenced
#       by the GameConfigs that cared about them. 
#

#
# The GameConfig class holds the locations and key items associated with a game type.
#
class GameConfig:
  def __init__(self):
    self.keyItemList = []
    self.locationGroups = []
    self.game = None
    self.initLocations()
    self.initKeyItems()
    self.initGame()

  #
  # Subclasses will override this method to 
  # initialize LocationGroups for their specific mode.
  #
  def initLocations(self):
    raise NotImplementedError()
	
  #
  # Subclasses will override this method to
  # initialize key items for their specific mode.
  #
  def initKeyItems(self):
    raise NotImplementedError()

  #
  # Subclasses will override this method to
  # configure a game object for their specific mode.
  #
  def initGame(self):
    raise NotImplementedError()
    
  #
  # Get the LocationGroups associated with this game mode.
  #
  # return: A list of LocationGroup objects for this mode
  #
  def getLocations(self):
    return self.locationGroups
    
  #
  # Get the list of key items associated with this game mode.
  #
  # return: A list of KeyItem objects for this mode
  #
  def getKeyItemList(self):
    return self.keyItemList
    
  #
  # Get the Game object associated with this mode.
  #
  # return: A configured Game object for this mode
  #
  def getGame(self):
    return self.game
# end GameLogic class


#
# This class represents the game configuration for a 
# standard Chronosanity game.
#
class ChronosanityGameConfig(GameConfig):
  def __init__(self, charLocations, earlyPendant, lockedChars):
    self.charLocations = charLocations
    self.earlyPendant = earlyPendant
    self.lockedChars = lockedChars
    GameConfig.__init__(self)
	
  def initLocations(self):
    # Dark Ages 
    # Mount Woe does not go away in the randomizer, so it
    # is being considered for key item drops.
    darkagesLocations = \
      LocationGroup("Darkages", 30, lambda game:game.canAccessDarkAges())
    (darkagesLocations
      .addLocation(Location("Mt Woe 1st Screen",0x35F770))
      .addLocation(Location("Mt Woe 2nd Screen 1",0x35F748))
      .addLocation(Location("Mt Woe 2nd Screen 2",0x35F74C))
      .addLocation(Location("Mt Woe 2nd Screen 3",0x35F750))
      .addLocation(Location("Mt Woe 2nd Screen 4",0x35F754))
      .addLocation(Location("Mt Woe 2nd Screen 5",0x35F758))
      .addLocation(Location("Mt Woe 3rd Screen 1",0x35F75C))
      .addLocation(Location("Mt Woe 3rd Screen 2",0x35F760))
      .addLocation(Location("Mt Woe 3rd Screen 3",0x35F764))
      .addLocation(Location("Mt Woe 3rd Screen 4",0x35F768))
      .addLocation(Location("Mt Woe 3rd Screen 5",0x35F76C))
      .addLocation(Location("Mt Woe Final 1",0x35F774))
      .addLocation(Location("Mt Woe Final 2",0x35F778))
      .addLocation(BaselineLocation("Mount Woe", 0x381010, 0x381013, LootTiers.High))
    )

    # Fiona Shrine (Key Item only)
    fionaShrineLocations = \
      LocationGroup("Fionashrine", 2, lambda game:game.canAccessFionasShrine())
    (fionaShrineLocations
      .addLocation(BaselineLocation("Fiona's Shrine", 0x6EF5E, 0x6EF61, LootTiers.MidHigh))
    )

    # Future
    futureOpenLocations = \
      LocationGroup("FutureOpen", 20, lambda game:game.canAccessFuture())
    (futureOpenLocations
      # Chests
      .addLocation(Location("Arris Dome",0x35F5C8))
      .addLocation(Location("Arris Dome Food Store",0x35F744))
      # KeyItems    
      .addLocation(BaselineLocation("Arris Dome Doan", 0x392F4C, 0x392F4E, LootTiers.MidHigh))
      .addLocation(BaselineLocation("Sun Palace", 0x1B8D95, 0x1B8D97, LootTiers.MidHigh))
    )
    
    futureSewersLocations = \
      LocationGroup("FutureSewers", 9, lambda game:game.canAccessFuture())
    (futureSewersLocations
      .addLocation(Location("Sewers 1",0x35F614))     
      .addLocation(Location("Sewers 2",0x35F618))
      .addLocation(Location("Sewers 3",0x35F61C))
    )
    
    futureLabLocations = \
      LocationGroup("FutureLabs", 15, lambda game:game.canAccessFuture())
    (futureLabLocations
      .addLocation(Location("Lab 16 1",0x35F5B8))
      .addLocation(Location("Lab 16 2",0x35F5BC))
      .addLocation(Location("Lab 16 3",0x35F5C0))
      .addLocation(Location("Lab 16 4",0x35F5C4))
      .addLocation(Location("Lab 32 1",0x35F5E0))
      # 1000AD, opened after trial - putting it here to dilute the lab pool a bit
      .addLocation(Location("Prison Tower",0x35F7DC)) 
      # Race log chest is not included.      
      #.addLocation(Location("Lab 32 2",0x35F5E4))
    )
    
    genoDomeLocations = \
      LocationGroup("GenoDome", 33, lambda game:game.canAccessFuture())
    (genoDomeLocations
      .addLocation(Location("Geno Dome 1st Floor 1",0x35F630))
      .addLocation(Location("Geno Dome 1st Floor 2",0x35F634))
      .addLocation(Location("Geno Dome 1st Floor 3",0x35F638))
      .addLocation(Location("Geno Dome 1st Floor 4",0x35F63C))
      .addLocation(Location("Geno Dome Room 1",0x35F640))
      .addLocation(Location("Geno Dome Room 2",0x35F644))
      .addLocation(Location("Proto 4 Chamber 1",0x35F648))
      .addLocation(Location("Proto 4 Chamber 2",0x35F64C))
      .addLocation(Location("Geno Dome 2nd Floor 1",0x35F668))
      .addLocation(Location("Geno Dome 2nd Floor 2",0x35F66C))
      .addLocation(Location("Geno Dome 2nd Floor 3",0x35F670))
      .addLocation(Location("Geno Dome 2nd Floor 4",0x35F674))
      .addLocation(BaselineLocation("Geno Dome Mother Brain", 0x1B1844, 0x1B1846, LootTiers.MidHigh))
    )
    
    factoryLocations = \
      LocationGroup("Factory", 30, lambda game:game.canAccessFuture())
    (factoryLocations
      .addLocation(Location("Factory Ruins Left - Auxillary Console",0x35F5E8))
      .addLocation(Location("Factory Ruins Left - Security Center (Right)",0x35F5EC))
      .addLocation(Location("Factory Ruins Left - Security Center (Left)",0x35F5F0))
      .addLocation(Location("Factory Ruins Left - Power Core",0x35F610))
      .addLocation(Location("Factory Ruins Right - Data Core 1",0x35F650))
      .addLocation(Location("Factory Ruins Right - Data Core 2",0x35F654))
      .addLocation(Location("Factory Ruins Right - Factory Floor (Top)",0x35F5F4))
      .addLocation(Location("Factory Ruins Right - Factory Floor (Left)",0x35F5F8))
      .addLocation(Location("Factory Ruins Right - Factory Floor (Bottom)",0x35F5FC))
      .addLocation(Location("Factory Ruins Right - Factory Floor (Secret)",0x35F600))
      .addLocation(Location("Factory Ruins Right - Crane Control Room (lower)",0x35F604))
      .addLocation(Location("Factory Ruins Right - Crane Control Room (upper)",0x35F608))
      .addLocation(Location("Factory Ruins Right - Information Archive",0x35F60C))
      #.addLocation(Location("Factory Ruins Right - Robot Storage",0x35F7A0)) # Inaccessible chest
    )

    # GiantsClawLocations
    giantsClawLocations = \
      LocationGroup("Giantsclaw", 30, lambda game:game.canAccessGiantsClaw())
    (giantsClawLocations
      .addLocation(Location("Giant's Claw Kino's Cell",0x35F468))
      .addLocation(Location("Giant's Claw Traps",0x35F46C))
      .addLocation(Location("Giant's Claw Caves 1",0x35F56C))
      .addLocation(Location("Giant's Claw Caves 2",0x35F570))
      .addLocation(Location("Giant's Claw Caves 3",0x35F574))
      .addLocation(Location("Giant's Claw Caves 4",0x35F578))
      #.addLocation(Location("Giant's Claw Caves Rock Chest",0x35F57C)) # Rock chest - Don't include
      .addLocation(Location("Giant's Claw Caves 5",0x35F580))
      .addLocation(BaselineLocation("Giant's Claw", 0x1B8ABB, 0x1B8ABF, LootTiers.Mid)) #key item
    )

    # Northern Ruins
    northernRuinsLocations = \
      LocationGroup("NorthernRuins", 8, \
        lambda game:(game.canAccessRuins()))
    (northernRuinsLocations
      # regular chests in the sealed ruins
      # Note: These aren't actually real chests, they are handled in event
      #       code similar to how sealed chests are handled.
      .addLocation(EventLocation("Northern Ruins Basement 600AD",0x1BAF0A, 0x1BAF0F))
      .addLocation(EventLocation("Northern Ruins Upstairs 600AD",0x39313, 0x39319))
      .addLocation(EventLocation("Northern Ruins Upstairs 1000AD",0x392FD, 0x39303))
      # Sealed chests in Northern Ruins
      # TODO - Sealed chests in this location are shared across time periods in such
      #        a way that the player can end up with two copies of a key item if they 
      #        collect it in 1000AD first, then in 600AD.  Commenting these out for
      #        now.  Either these chests will need to be separated or removed
      #        from the pool of key item locations.
      #.addLocation(EventLocation("Hero's Grave 1",0x1B03CD,0x1B03D0))
      #.addLocation(EventLocation("Hero's Grave 2",0x1B0401,0x1B0404))
      #.addLocation(EventLocation("Hero's Grave 3",0x393F8,0x393FF))
    )
    
    northernRuinsFrogLocked = \
      LocationGroup("NorthernRuinsFrogLocked", 1, \
        lambda game:(game.canAccessRuins() and game.hasCharacter(Characters.Frog)))
    (northernRuinsFrogLocked
      .addLocation(EventLocation("Northern Ruins Basement 1000AD",0x1BAEF4, 0x1BAEF9))
    )

    # Guardia Treasury
    guardiaTreasuryLocations = \
      LocationGroup("GuardiaTreasury", 36, lambda game:game.canAccessKingsTrial())
    (guardiaTreasuryLocations
      .addLocation(Location("Guardia Basement 1", 0x35F41C))
      .addLocation(Location("Guardia Basement 2", 0x35F420))
      .addLocation(Location("Guardia Basement 3", 0x35F424))
      .addLocation(Location("Guardia Treasury 1", 0x35F7A4))
      .addLocation(Location("Guardia Treasury 2", 0x35F7A8))
      .addLocation(Location("Guardia Treasury 3", 0x35F7AC))
      .addLocation(BaselineLocation("King's Trial", 0x38045D, 0x38045F, LootTiers.High))
    )
    
    # Ozzie's Fort locations
    # Ozzie's fort is a high level location.  For the first four chests, don't
    # consider these locations until the player has either the pendant or gate key.
    # The final two chests are locked behind the trio battle.  Only consider these if
    # the player has access to the Dark Ages.
    earlyOzziesFortLocations = \
      LocationGroup("Ozzie's Fort Front", 6, \
        lambda game: (game.canAccessFuture() or game.canAccessPrehistory()))
    (earlyOzziesFortLocations
      .addLocation(Location("Ozzie's Fort Guillotines 1",0x35F554))
      .addLocation(Location("Ozzie's Fort Guillotines 2",0x35F558))
      .addLocation(Location("Ozzie's Fort Guillotines 3",0x35F55C))
      .addLocation(Location("Ozzie's Fort Guillotines 4",0x35F560))
    )
    
    lateOzziesFortLocations = \
      LocationGroup("Ozzie's Fort Back", 6, \
      lambda game: \
        (game.canAccessFuture() or game.canAccessPrehistory()) and \
        game.canAccessDarkAges())
    (lateOzziesFortLocations
      .addLocation(Location("Ozzie's Fort Final 1",0x35F564))
      .addLocation(Location("Ozzie's Fort Final 2",0x35F568))
    )

    # Open locations always available with no access requirements
    # Open locations are split into multiple groups so that weighting
    # can be applied separately to individual areas.
    openLocations = LocationGroup("Open", 10, \
       lambda game: True, \
       lambda weight:int(weight * 0.2))
    (openLocations
      .addLocation(Location("Truce Mayor's House F1",0x35F40C))
      .addLocation(Location("Truce Mayor's House F2",0x35F410))
      .addLocation(Location("Forest Ruins",0x35F42C))
      .addLocation(Location("Porre Mayor's House F2",0x35F440))
      .addLocation(Location("Truce Canyon 1",0x35F470))
      .addLocation(Location("Truce Canyon 2",0x35F474))
      .addLocation(Location("Fiona's House 1",0x35F4FC))
      .addLocation(Location("Fiona's House 2",0x35F500))
      .addLocation(Location("Cursed Woods 1",0x35F4A4))
      .addLocation(Location("Cursed Woods 2",0x35F4A8))
      .addLocation(Location("Frog's Burrow Right Chest",0x35F4AC))
    )
    
    openKeys = LocationGroup("OpenKeys", 5, lambda game: True)
    (openKeys
      .addLocation(BaselineLocation("Zenan Bridge", 0x393C83, 0x393C85, LootTiers.Mid))
      .addLocation(BaselineLocation("Snail Stop", 0x380C42, 0x380C5B, LootTiers.Mid))
      .addLocation(BaselineLocation("Lazy Carpenter", 0x3966B, 0x3966D, LootTiers.Mid))
    )
    
    heckranLocations = \
      LocationGroup("Heckran", 4, lambda game: True)
    (heckranLocations
      .addLocation(Location("Heckran Cave Sidetrack",0x35F430))
      .addLocation(Location("Heckran Cave Entrance",0x35F434))
      .addLocation(Location("Heckran Cave 1",0x35F438))
      .addLocation(Location("Heckran Cave 2",0x35F43C))
      .addLocation(BaselineLocation("Taban", 0x35F888, 0x35F88A, LootTiers.Mid))
    )
    
    guardiaCastleLocations = \
      LocationGroup("GuardiaCastle", 3, lambda game: True)
    (guardiaCastleLocations
      .addLocation(Location("King's Room (Present)",0x35F414))
      .addLocation(Location("Queen's Room (Present)",0x35F418))
      .addLocation(Location("King's Room(Middle Ages)",0x35F478))
      .addLocation(Location("Queen's Room(Middle Ages)",0x35F47C))
      .addLocation(Location("Royal Kitchen",0x35F480))
      .addLocation(Location("Queen's Tower(Middle Ages)",0x35F7B0))
      .addLocation(Location("King's Tower(Middle Ages)",0x35F7CC))
      .addLocation(Location("King's Tower(Present)",0x35F7D0))
      .addLocation(Location("Queen's Tower(Present)",0x35F7D4))
      .addLocation(Location("Guardia Court Tower",0x35F7D8))
    )
    
    cathedralLocations = \
      LocationGroup("CathedralLocations", 6, lambda game: True)
    (cathedralLocations
      .addLocation(Location("Manoria Cathedral 1",0x35F488))
      .addLocation(Location("Manoria Cathedral 2",0x35F48C))
      .addLocation(Location("Manoria Cathedral 3",0x35F490))
      .addLocation(Location("Cathedral Interior 1",0x35F494))
      .addLocation(Location("Cathedral Interior 2",0x35F498))
      .addLocation(Location("Cathedral Interior 3",0x35F49C))
      .addLocation(Location("Cathedral Interior 4",0x35F4A0))
      .addLocation(Location("Manoria Shrine Sideroom 1",0x35F588))
      .addLocation(Location("Manoria Shrine Sideroom 2",0x35F58C))
      .addLocation(Location("Manoria Bromide Room 1",0x35F590))
      .addLocation(Location("Manoria Bromide Room 2",0x35F594))
      .addLocation(Location("Manoria Bromide Room 3",0x35F598))
      .addLocation(Location("Manoria Magus Shrine 1",0x35F59C))
      .addLocation(Location("Manoria Magus Shrine 2",0x35F5A0))
      .addLocation(Location("Yakra's Room",0x35F584))
    )
    
    denadoroLocations = \
      LocationGroup("DenadoroLocations", 6, lambda game:True)
    (denadoroLocations
      .addLocation(Location("Denadoro Mts Screen 2 1",0x35F4B0))
      .addLocation(Location("Denadoro Mts Screen 2 2",0x35F4B4))
      .addLocation(Location("Denadoro Mts Screen 2 3",0x35F4B8))
      .addLocation(Location("Denadoro Mts Final 1",0x35F4BC))
      .addLocation(Location("Denadoro Mts Final 2",0x35F4C0))     
      .addLocation(Location("Denadoro Mts Final 3",0x35F4C4))     
      .addLocation(Location("Denadoro Mts Waterfall Top 1",0x35F4C8))     
      .addLocation(Location("Denadoro Mts Waterfall Top 2",0x35F4CC))     
      .addLocation(Location("Denadoro Mts Waterfall Top 3",0x35F4D0))     
      .addLocation(Location("Denadoro Mts Waterfall Top 4",0x35F4D4))     
      .addLocation(Location("Denadoro Mts Waterfall Top 5",0x35F4D8))     
      .addLocation(Location("Denadoro Mts Entrance 1",0x35F4DC))      
      .addLocation(Location("Denadoro Mts Entrance 2",0x35F4E0))      
      .addLocation(Location("Denadoro Mts Screen 3 1",0x35F4E4))      
      .addLocation(Location("Denadoro Mts Screen 3 2",0x35F4E8))      
      .addLocation(Location("Denadoro Mts Screen 3 3",0x35F4EC))      
      .addLocation(Location("Denadoro Mts Screen 3 4",0x35F4F0))      
      .addLocation(Location("Denadoro Mts Ambush",0x35F4F4))      
      .addLocation(Location("Denadoro Mts Save Point",0x35F4F8))
      .addLocation(BaselineLocation("Denadoro Mountain", 0x3773F1, 0x3773F3, LootTiers.Mid))
    )
      
    # Sealed locations
    sealedLocations = \
      LocationGroup("SealedLocations", 20, 
        lambda game:game.canAccessSealedChests(),
        lambda weight:int(weight * 0.3))
    (sealedLocations
      # Sealed Doors
      .addLocation(Location("Bangor Dome Seal 1", 0x35F5A4))
      .addLocation(Location("Bangor Dome Seal 2", 0x35F5A8))
      .addLocation(Location("Bangor Dome Seal 3", 0x35F5AC))
      .addLocation(Location("Trann Dome Seal 1", 0x35F5B0))
      .addLocation(Location("Trann Dome Seal 2", 0x35F5B4))
      .addLocation(Location("Arris Dome Seal 1", 0x35F5CC))
      .addLocation(Location("Arris Dome Seal 2", 0x35F5D0))
      .addLocation(Location("Arris Dome Seal 3", 0x35F5D4))
      .addLocation(Location("Arris Dome Seal 4", 0x35F5D8))
      # Sealed chests
      .addLocation(EventLocation("Truce Inn 600AD Sealed",0x19FE7C,0x19FE83))     
      .addLocation(EventLocation("Porre Elder's House 1 Sealed",0x1B90EA,0x1B90F2))     
      .addLocation(EventLocation("Porre Elder's House 2 Sealed",0x1B9123,0x1B9126))     
      .addLocation(EventLocation("Guardia Castle 600AD Sealed",0x3AED24,0x3AED26))  
      .addLocation(EventLocation("Guardia Forest 600AD Sealed",0x39633B,0x39633D))      
      .addLocation(EventLocation("Truce Inn 1000AD Sealed",0xC3328,0xC332C))           
      .addLocation(EventLocation("Porre Mayor's House Sealed 1",0x1BACD6,0x1BACD8))     
      .addLocation(EventLocation("Porre Mayor's House Sealed 2",0x1BACF7,0x1BACF9))     
      .addLocation(EventLocation("Guardia Forest 1000AD Sealed",0x3908B5,0x3908C9))     
      .addLocation(EventLocation("Guardia Castle 1000AD Sealed",0x3AEF65,0x3AEF67))     
      .addLocation(EventLocation("Heckran's Cave Sealed 1",0x24EC29,0x24EC2B))      
      .addLocation(EventLocation("Heckran's Cave Sealed 2",0x24EC3B,0x24EC3D))
      # Since the blue pyramid only lets you get one of the two chests,
      # set the key item to be in both of them.
      .addLocation(LinkedLocation("Blue Pyramid", \
          EventLocation("Left Chest", 0x1BAB33,0x1BAB35), \
          EventLocation("Right Chest", 0x1BAB62,0x1BAB64)))
    )
    
    # Sealed chest in the magic cave.
    # Requires both powered up pendant and Magus' Castle access
    magicCaveLocations = \
      LocationGroup("Magic Cave", 4, \
        lambda game: game.canAccessSealedChests() and game.canAccessMagusCastle())
    (magicCaveLocations
      .addLocation(EventLocation("Magic Cave",0x1B31C7,0x1B31CA))
    )
    
    # Prehistory
    prehistoryForestMazeLocations = \
      LocationGroup("PrehistoryForestMaze", 18, lambda game:game.canAccessPrehistory())
    (prehistoryForestMazeLocations
      .addLocation(Location("Mystic Mtn Stream",0x35F678))
      .addLocation(Location("Forest Maze 1",0x35F67C))
      .addLocation(Location("Forest Maze 2",0x35F680))
      .addLocation(Location("Forest Maze 3",0x35F684))
      .addLocation(Location("Forest Maze 4",0x35F688))
      .addLocation(Location("Forest Maze 5",0x35F68C))
      .addLocation(Location("Forest Maze 6",0x35F690))
      .addLocation(Location("Forest Maze 7",0x35F694))
      .addLocation(Location("Forest Maze 8",0x35F698))
      .addLocation(Location("Forest Maze 9",0x35F69C))
    )
    
    prehistoryReptiteLocations = \
      LocationGroup("PrehistoryReptite", 27, lambda game:game.canAccessPrehistory())
    (prehistoryReptiteLocations
      .addLocation(Location("Reptite Lair Reptites 1",0x35F6B8))
      .addLocation(Location("Reptite Lair Reptites 2",0x35F6BC))
      .addLocation(BaselineLocation("Reptite Lair", 0x18FC04, 0x18FC07, LootTiers.MidHigh)) #Reptite Lair Key Item
    )
    
    # Dactyl Nest already has a character, so give it a relatively low weight compared
    # to the other prehistory locations.
    prehistoryDactylNest = \
      LocationGroup("PrehistoryDactylNest", 6, lambda game:game.canAccessPrehistory())
    (prehistoryDactylNest
      .addLocation(Location("Dactyl Nest 1",0x35F6C0))
      .addLocation(Location("Dactyl Nest 2",0x35F6C4))
      .addLocation(Location("Dactyl Nest 3",0x35F6C8)) 
    )

    # MelchiorRefinements
    melchiorsRefinementslocations = \
      LocationGroup("MelchiorRefinements", 15, lambda game:game.canAccessMelchiorsRefinements())
    (melchiorsRefinementslocations
      .addLocation(BaselineLocation("Melchior's Refinements", 0x3805DE, 0x3805E0, LootTiers.High))
    )

    # Frog's Burrow
    frogsBurrowLocation = \
      LocationGroup("FrogsBurrowLocation", 9, lambda game:game.canAccessBurrowItem())
    (frogsBurrowLocation
      .addLocation(BaselineLocation("Frog's Burrow Left Chest", 0x3891DE, 0x3891E0, LootTiers.MidHigh))
    )
    
    # Prehistory
    self.locationGroups.append(prehistoryForestMazeLocations)
    self.locationGroups.append(prehistoryReptiteLocations)
    self.locationGroups.append(prehistoryDactylNest)
    
    # Dark Ages
    self.locationGroups.append(darkagesLocations)
    
    # 600/1000AD
    self.locationGroups.append(fionaShrineLocations)
    self.locationGroups.append(giantsClawLocations)
    self.locationGroups.append(northernRuinsLocations)
    self.locationGroups.append(northernRuinsFrogLocked)
    self.locationGroups.append(guardiaTreasuryLocations)
    self.locationGroups.append(openLocations)
    self.locationGroups.append(openKeys)
    self.locationGroups.append(heckranLocations)
    self.locationGroups.append(cathedralLocations)
    self.locationGroups.append(guardiaCastleLocations)
    self.locationGroups.append(denadoroLocations)
    self.locationGroups.append(magicCaveLocations)
    self.locationGroups.append(melchiorsRefinementslocations)
    self.locationGroups.append(frogsBurrowLocation)
    self.locationGroups.append(earlyOzziesFortLocations)
    self.locationGroups.append(lateOzziesFortLocations)
    
    # Future
    self.locationGroups.append(futureOpenLocations)
    self.locationGroups.append(futureLabLocations)
    self.locationGroups.append(futureSewersLocations)
    self.locationGroups.append(genoDomeLocations)
    self.locationGroups.append(factoryLocations)
    
    # Sealed Locations (chests and doors)
    self.locationGroups.append(sealedLocations)
    
  def initKeyItems(self):
    # NOTE:
    # The initial list of key items contains multiples of most of the key items, and
    # not in equal number.  The pendant and gate key are more heavily weighted
    # so that they appear earlier in the run, opening up more potential checks.
    # The ruby knife, dreamstone, clone, and trigger only appear once to reduce
    # the frequency of extremely early go mode from open checks.
    # The hilt and blade show up 2-3 times each, also to reduce early go mode through
    # Magus' Castle to a reasonable number.
    
    # Seed the list with 5 copies of each item
    keyItemList = [key for key in (KeyItems)]
    keyItemList.extend([key for key in (KeyItems)])
    keyItemList.extend([key for key in (KeyItems)])
    keyItemList.extend([key for key in (KeyItems)])
    keyItemList.extend([key for key in (KeyItems)])
    
    # remove all but 1 copy of the dreamstone/ruby knife/clone/trigger
    keyItemList[:] = [x for x in keyItemList if x != KeyItems.rubyknife]
    keyItemList[:] = [x for x in keyItemList if x != KeyItems.dreamstone]
    keyItemList[:] = [x for x in keyItemList if x != KeyItems.clone]
    keyItemList[:] = [x for x in keyItemList if x != KeyItems.ctrigger]
    keyItemList.extend([KeyItems.rubyknife, KeyItems.dreamstone, 
                        KeyItems.clone, KeyItems.ctrigger])
    
    # remove some copies of the hilt/blade to reduce early go mode through Magus' Castle
    keyItemList.remove(KeyItems.hilt)
    keyItemList.remove(KeyItems.hilt)
    keyItemList.remove(KeyItems.blade)
    keyItemList.remove(KeyItems.blade)
    keyItemList.remove(KeyItems.blade)
    
    # Add additional copies of the pendant and gate key
    keyItemList.extend([KeyItems.gatekey, KeyItems.gatekey, KeyItems.gatekey, 
                        KeyItems.pendant, KeyItems.pendant, KeyItems.pendant])
    
    self.keyItemList = keyItemList

    
  def initGame(self):
    self.game = Game(self.charLocations)
    self.game.setEarlyPendant(self.earlyPendant)
    self.game.setLockedCharacters(self.lockedChars)
    
# end ChronosanityGameConfig class

#
# This class represents the game configuration for a 
# Lost Worlds Chronosanity game.
#
class ChronosanityLostWorldsGameConfig(GameConfig):
  def __init__(self, charLocations):
    self.charLocations = charLocations
    GameConfig.__init__(self)
    
  def initGame(self):
    self.game = Game(self.charLocations)
    self.game.setLostWorlds(True)
    # locked characters don't matter in Lost Worlds item placement logic
    # early pendant charge doesn't work in this mode
    
  def initKeyItems(self):
    # Since almost all checks are available from the start, no weighting is 
    # being applied to the Lost Worlds key items
    self.keyItemList = [KeyItems.pendant, KeyItems.clone, \
                   KeyItems.ctrigger, KeyItems.rubyknife, KeyItems.dreamstone]
    
                   
  def initLocations(self):
    locationGroups = []
  
    # Prehistory
    prehistoryForestMazeLocations = \
        LocationGroup("PrehistoryForestMaze", 10, lambda game:True)
    (prehistoryForestMazeLocations
        .addLocation(Location("Mystic Mtn Stream",0x35F678))
        .addLocation(Location("Forest Maze 1",0x35F67C))
        .addLocation(Location("Forest Maze 2",0x35F680))
        .addLocation(Location("Forest Maze 3",0x35F684))
        .addLocation(Location("Forest Maze 4",0x35F688))
        .addLocation(Location("Forest Maze 5",0x35F68C))
        .addLocation(Location("Forest Maze 6",0x35F690))
        .addLocation(Location("Forest Maze 7",0x35F694))
        .addLocation(Location("Forest Maze 8",0x35F698))
        .addLocation(Location("Forest Maze 9",0x35F69C))
    )
    
    prehistoryReptiteLocations = \
        LocationGroup("PrehistoryReptite", 10, lambda game:True)
    (prehistoryReptiteLocations
        .addLocation(Location("Reptite Lair Reptites 1",0x35F6B8))
        .addLocation(Location("Reptite Lair Reptites 2",0x35F6BC))
        .addLocation(BaselineLocation("Reptite Lair", 0x18FC04, 0x18FC07, LootTiers.MidHigh)) #Reptite Lair Key Item
    )
    
    # Dactyl Nest already has a character, so give it a relatively low weight compared
    # to the other prehistory locations.
    prehistoryDactylNest = \
        LocationGroup("PrehistoryDactylNest", 6, lambda game:True)
    (prehistoryDactylNest
        .addLocation(Location("Dactyl Nest 1",0x35F6C0))
        .addLocation(Location("Dactyl Nest 2",0x35F6C4))
        .addLocation(Location("Dactyl Nest 3",0x35F6C8)) 
    )
    
    # Dark Ages 
    # Mount Woe does not go away in the randomizer, so it
    # is being considered for key item drops.
    darkagesLocations = \
        LocationGroup("Darkages", 10, lambda game:True)
    (darkagesLocations
        .addLocation(Location("Mt Woe 1st Screen",0x35F770))
        .addLocation(Location("Mt Woe 2nd Screen 1",0x35F748))
        .addLocation(Location("Mt Woe 2nd Screen 2",0x35F74C))
        .addLocation(Location("Mt Woe 2nd Screen 3",0x35F750))
        .addLocation(Location("Mt Woe 2nd Screen 4",0x35F754))
        .addLocation(Location("Mt Woe 2nd Screen 5",0x35F758))
        .addLocation(Location("Mt Woe 3rd Screen 1",0x35F75C))
        .addLocation(Location("Mt Woe 3rd Screen 2",0x35F760))
        .addLocation(Location("Mt Woe 3rd Screen 3",0x35F764))
        .addLocation(Location("Mt Woe 3rd Screen 4",0x35F768))
        .addLocation(Location("Mt Woe 3rd Screen 5",0x35F76C))
        .addLocation(Location("Mt Woe Final 1",0x35F774))
        .addLocation(Location("Mt Woe Final 2",0x35F778))
        .addLocation(BaselineLocation("Mount Woe", 0x381010, 0x381013, LootTiers.High))
    )

    # Future
    futureOpenLocations = \
        LocationGroup("FutureOpen", 10, lambda game:True)
    (futureOpenLocations
        # Chests
        .addLocation(Location("Arris Dome",0x35F5C8))
        .addLocation(Location("Arris Dome Food Store",0x35F744))
        # KeyItems    
        .addLocation(BaselineLocation("Arris Dome Doan", 0x392F4C, 0x392F4E, LootTiers.MidHigh))
        .addLocation(BaselineLocation("Sun Palace", 0x1B8D95, 0x1B8D97, LootTiers.MidHigh))
    )
    
    futureSewersLocations = \
        LocationGroup("FutureSewers", 8, lambda game:True)
    (futureSewersLocations
        .addLocation(Location("Sewers 1",0x35F614))     
        .addLocation(Location("Sewers 2",0x35F618))
        .addLocation(Location("Sewers 3",0x35F61C))
    )
    
    futureLabLocations = \
        LocationGroup("FutureLabs", 10, lambda game:True)
    (futureLabLocations
        .addLocation(Location("Lab 16 1",0x35F5B8))
        .addLocation(Location("Lab 16 2",0x35F5BC))
        .addLocation(Location("Lab 16 3",0x35F5C0))
        .addLocation(Location("Lab 16 4",0x35F5C4))
        .addLocation(Location("Lab 32 1",0x35F5E0)) 
        # Race log chest is not included.      
        #.addLocation(Location("Lab 32 2",0x35F5E4))
    )
    
    genoDomeLocations = \
        LocationGroup("GenoDome", 10, lambda game:True)
    (genoDomeLocations
        .addLocation(Location("Geno Dome 1st Floor 1",0x35F630))
        .addLocation(Location("Geno Dome 1st Floor 2",0x35F634))
        .addLocation(Location("Geno Dome 1st Floor 3",0x35F638))
        .addLocation(Location("Geno Dome 1st Floor 4",0x35F63C))
        .addLocation(Location("Geno Dome Room 1",0x35F640))
        .addLocation(Location("Geno Dome Room 2",0x35F644))
        .addLocation(Location("Proto 4 Chamber 1",0x35F648))
        .addLocation(Location("Proto 4 Chamber 2",0x35F64C))
        .addLocation(Location("Geno Dome 2nd Floor 1",0x35F668))
        .addLocation(Location("Geno Dome 2nd Floor 2",0x35F66C))
        .addLocation(Location("Geno Dome 2nd Floor 3",0x35F670))
        .addLocation(Location("Geno Dome 2nd Floor 4",0x35F674))
        .addLocation(BaselineLocation("Geno Dome Mother Brain", 0x1B1844, 0x1B1846, LootTiers.MidHigh))
    )
    
    factoryLocations = \
        LocationGroup("Factory", 10, lambda game:True)
    (factoryLocations
        .addLocation(Location("Factory Ruins Left - Auxillary Console",0x35F5E8))
        .addLocation(Location("Factory Ruins Left - Security Center (Right)",0x35F5EC))
        .addLocation(Location("Factory Ruins Left - Security Center (Left)",0x35F5F0))
        .addLocation(Location("Factory Ruins Left - Power Core",0x35F610))
        .addLocation(Location("Factory Ruins Right - Data Core 1",0x35F650))
        .addLocation(Location("Factory Ruins Right - Data Core 2",0x35F654))
        .addLocation(Location("Factory Ruins Right - Factory Floor (Top)",0x35F5F4))
        .addLocation(Location("Factory Ruins Right - Factory Floor (Left)",0x35F5F8))
        .addLocation(Location("Factory Ruins Right - Factory Floor (Bottom)",0x35F5FC))
        .addLocation(Location("Factory Ruins Right - Factory Floor (Secret)",0x35F600))
        .addLocation(Location("Factory Ruins Right - Crane Control Room (lower)",0x35F604))
        .addLocation(Location("Factory Ruins Right - Crane Control Room (upper)",0x35F608))
        .addLocation(Location("Factory Ruins Right - Information Archive",0x35F60C))
    )
    
    # Sealed locations
    sealedLocations = \
        LocationGroup("SealedLocations", 10, 
            lambda game:game.canAccessSealedChests())
    (sealedLocations
        # Sealed Doors
        .addLocation(Location("Bangor Dome Seal 1", 0x35F5A4))
        .addLocation(Location("Bangor Dome Seal 2", 0x35F5A8))
        .addLocation(Location("Bangor Dome Seal 3", 0x35F5AC))
        .addLocation(Location("Trann Dome Seal 1", 0x35F5B0))
        .addLocation(Location("Trann Dome Seal 2", 0x35F5B4))
        .addLocation(Location("Arris Dome Seal 1", 0x35F5CC))
        .addLocation(Location("Arris Dome Seal 2", 0x35F5D0))
        .addLocation(Location("Arris Dome Seal 3", 0x35F5D4))
        .addLocation(Location("Arris Dome Seal 4", 0x35F5D8))
    )
    
    # 65 Million BC
    self.locationGroups.append(prehistoryForestMazeLocations)
    self.locationGroups.append(prehistoryReptiteLocations)
    self.locationGroups.append(prehistoryDactylNest)
    
    # 12000 BC
    self.locationGroups.append(darkagesLocations)  
    
    # 2300 AD
    self.locationGroups.append(futureOpenLocations)
    self.locationGroups.append(futureLabLocations)
    self.locationGroups.append(futureSewersLocations)
    self.locationGroups.append(genoDomeLocations)
    self.locationGroups.append(factoryLocations)
    
    # Sealed Locations (chests and doors)
    self.locationGroups.append(sealedLocations)

# end ChronosanityLostWorldsGameConfig class

#
# This class represents the game configuration for a 
# Normal game.
#
class NormalGameConfig(GameConfig):
  def __init__(self, charLocations, earlyPendant, lockedChars):
    self.charLocations = charLocations
    self.earlyPendant = earlyPendant
    self.lockedChars = lockedChars
    GameConfig.__init__(self)
    
  def initGame(self):
    self.game = Game(self.charLocations)
    self.game.setEarlyPendant(self.earlyPendant)
    self.game.setLockedCharacters(self.lockedChars)
    
  def initKeyItems(self):
    self.keyItemList = [key for key in (KeyItems)]
    
                   
  def initLocations(self): 
    prehistoryLocations = \
      LocationGroup("PrehistoryReptite", 1, lambda game:game.canAccessPrehistory())
    (prehistoryLocations
      .addLocation(BaselineLocation("Reptite Lair", 0x18FC04, 0x18FC07, LootTiers.MidHigh)) #Reptite Lair Key Item
    )
    
    darkagesLocations = \
        LocationGroup("Darkages", 1, lambda game:game.canAccessDarkAges())
    (darkagesLocations
        .addLocation(BaselineLocation("Mount Woe", 0x381010, 0x381013, LootTiers.High))
    )
  
    openKeys = LocationGroup("OpenKeys", 5, lambda game: True, lambda weight: weight-1)
    (openKeys
      .addLocation(BaselineLocation("Zenan Bridge", 0x393C83, 0x393C85, LootTiers.Mid))
      .addLocation(BaselineLocation("Snail Stop", 0x380C42, 0x380C5B, LootTiers.Mid))
      .addLocation(BaselineLocation("Lazy Carpenter", 0x3966B, 0x3966D, LootTiers.Mid))
      .addLocation(BaselineLocation("Taban", 0x35F888, 0x35F88A, LootTiers.Mid))
      .addLocation(BaselineLocation("Denadoro Mountain", 0x3773F1, 0x3773F3, LootTiers.Mid))
    )
    
    melchiorsRefinementslocations = \
      LocationGroup("MelchiorRefinements", 1, lambda game:game.canAccessMelchiorsRefinements())
    (melchiorsRefinementslocations
      .addLocation(BaselineLocation("Melchior's Refinements", 0x3805DE, 0x3805E0, LootTiers.High))
    )

    frogsBurrowLocation = \
      LocationGroup("FrogsBurrowLocation", 1, lambda game:game.canAccessBurrowItem())
    (frogsBurrowLocation
      .addLocation(BaselineLocation("Frog's Burrow Left Chest", 0x3891DE, 0x3891E0, LootTiers.MidHigh))
    )
    
    guardiaTreasuryLocations = \
      LocationGroup("GuardiaTreasury", 1, lambda game:game.canAccessKingsTrial())
    (guardiaTreasuryLocations
      .addLocation(BaselineLocation("King's Trial", 0x38045D, 0x38045F, LootTiers.High))
    )
    
    giantsClawLocations = \
      LocationGroup("Giantsclaw", 1, lambda game:game.canAccessGiantsClaw())
    (giantsClawLocations
      .addLocation(BaselineLocation("Giant's Claw", 0x1B8ABB, 0x1B8ABF, LootTiers.Mid)) #key item
    )
    
    fionaShrineLocations = \
      LocationGroup("Fionashrine", 1, lambda game:game.canAccessFionasShrine())
    (fionaShrineLocations
      .addLocation(BaselineLocation("Fiona's Shrine", 0x6EF5E, 0x6EF61, LootTiers.MidHigh))
    )
    
    futureKeys = \
        LocationGroup("FutureOpen", 3, lambda game:game.canAccessFuture(), lambda weight: weight-1)
    (futureKeys   
        .addLocation(BaselineLocation("Arris Dome Doan", 0x392F4C, 0x392F4E, LootTiers.MidHigh))
        .addLocation(BaselineLocation("Sun Palace", 0x1B8D95, 0x1B8D97, LootTiers.MidHigh))
        .addLocation(BaselineLocation("Geno Dome Mother Brain", 0x1B1844, 0x1B1846, LootTiers.MidHigh))
    )
    
    # Prehistory
    self.locationGroups.append(prehistoryLocations)
    # Dark Ages
    self.locationGroups.append(darkagesLocations)
    # 600/1000
    self.locationGroups.append(openKeys)
    self.locationGroups.append(melchiorsRefinementslocations)
    self.locationGroups.append(frogsBurrowLocation)
    self.locationGroups.append(guardiaTreasuryLocations)
    self.locationGroups.append(giantsClawLocations)
    self.locationGroups.append(fionaShrineLocations)
    # 2300
    self.locationGroups.append(futureKeys)
# end NormalGameConfig class
   
#
# This class represents the game configuration for a 
# Lost Worlds game.
#
class LostWorldsGameConfig(GameConfig):
  def __init__(self, charLocations):
    self.charLocations = charLocations
    GameConfig.__init__(self)
    
  def initGame(self):
    self.game = Game(self.charLocations)
    self.game.setLostWorlds(True)
    
  def initKeyItems(self):
    self.keyItemList = [KeyItems.pendant, KeyItems.clone, \
                   KeyItems.ctrigger, KeyItems.rubyknife, KeyItems.dreamstone]
                   
  def initLocations(self): 
    prehistoryLocations = \
      LocationGroup("PrehistoryReptite", 1, lambda game:True)
    (prehistoryLocations
      .addLocation(BaselineLocation("Reptite Lair", 0x18FC04, 0x18FC07, LootTiers.MidHigh)) #Reptite Lair Key Item
    )
    
    darkagesLocations = \
        LocationGroup("Darkages", 1, lambda game:True)
    (darkagesLocations
        .addLocation(BaselineLocation("Mount Woe", 0x381010, 0x381013, LootTiers.High))
    )
    
    futureKeys = \
        LocationGroup("FutureOpen", 3, lambda game:True, lambda weight: weight-1)
    (futureKeys   
        .addLocation(BaselineLocation("Arris Dome Doan", 0x392F4C, 0x392F4E, LootTiers.MidHigh))
        .addLocation(BaselineLocation("Sun Palace", 0x1B8D95, 0x1B8D97, LootTiers.MidHigh))
        .addLocation(BaselineLocation("Geno Dome Mother Brain", 0x1B1844, 0x1B1846, LootTiers.MidHigh))
    )
    
    # Prehistory
    self.locationGroups.append(prehistoryLocations)
    # Dark Ages
    self.locationGroups.append(darkagesLocations)
    # 2300
    self.locationGroups.append(futureKeys)

# end LostWorldsGameCofig class    

#
# Get a GameConfig object based on randomizer flags.
# The GameConfig object will have have the correct locations,
# initial key items, and game setup for the selected flags.
#
# param: chroosanity - Whether or not the chronosanity flag is selected
# param: lostWorlds - Whether or not the Lost Worlds flag is selected
# param: earlyPendant - Whether or not the early pendant charge flag is selected
# param: lockedChars - Whether or not the locked characters flag is selected
# param: charLocations - Dictionary of character locations from characterwriter.py
#
# return: A GameConfig object appropriate for the given flag set
#
def getGameConfig(chronosanity, lostWorlds, earlyPendant, lockedChars, charLocations):
  gameConfig = None
  if chronosanity and lostWorlds:
    gameConfig = ChronosanityLostWorldsGameConfig(charLocations)
  elif chronosanity:
    gameConfig = ChronosanityGameConfig(charLocations, earlyPendant, lockedChars)
  elif lostWorlds:
    gameConfig = LostWorldsGameConfig(charLocations)
  else:
    gameConfig = NormalGameConfig(charLocations, earlyPendant, lockedChars)
  
  return gameConfig
# end getGameConfig
