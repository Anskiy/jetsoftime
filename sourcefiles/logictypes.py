import enum
import struct as st

#
# This file holds various classes/types used by the logic placement code.
#

#
# Enum representing various loot tiers that are used
# for assigning treasure to unused key item checks.
#
class LootTiers(enum.Enum):
  Mid = 0
  MidHigh = 1
  High = 2
# end LootTiers enum class

#
# Enum type for the game's key items.
#
class KeyItems(enum.Enum):
  tomapop = 0xE3
  hilt = 0x51
  blade = 0x50
  dreamstone = 0xDC
  rubyknife = 0xE0
  gatekey = 0xD7
  jerky = 0xDB
  pendant = 0xD6
  moonstone = 0xDE
  prismshard = 0xD8
  grandleon = 0x42
  clone = 0xE2
  ctrigger = 0xD9
  heromedal = 0xB3
  roboribbon = 0xB8
# end KeyItems enum class

#
# Enum type used for the game's characters.
# Enum values correspond to the in game character IDs.
#
class Characters(enum.Enum):
  Crono = 0
  Marle = 1
  Lucca = 2
  Robo = 3
  Frog = 4
  Ayla = 5
  Magus = 6
# end Character enum class

#
# The Game class is used to keep track of game state
# as the randomizer places key items.  It:
#   - Tracks key items obtained
#   - Tracks characters obtained
#   - Keeps track of user selected flags
#   - Provides logic convenience functions
#  
class Game:
  def __init__(self, charLocations):
    self.characters = set()
    self.keyItems = set()
    self.earlyPendant = False
    self.lockedChars = False
    self.lostWorlds = False
    self.charLocations = charLocations
  
  #
  # Get the number of key items that have been acquired by the player.
  #
  # return: Number of obtained key items
  #
  def getKeyItemCount(self):
    return len(self.keyItems)
  
  #
  # Set whether or not this seed is using the early pendant flag.
  # This is used to determine when sealed chests and sealed doors become available.
  #
  # param: pflag - boolean, whether or not the early pendant flag is on
  #
  def setEarlyPendant(self, pflag):
    self.earlyPendant = pflag
  
  #
  # Set whether or not this seed is using the Locked Characters flag.
  # This is used to determine when characters become available to unlock further checks.
  #
  # param cflag - boolean, whether or not the locked characters flag is on
  #
  def setLockedCharacters(self, cflag):
    self.lockedChars = cflag
  
  #
  # Set whether or not this seed is using the Lost Worlds flag.
  # This is used to determine time period access in Lost Worlds games.
  #
  # param lFlag - boolean, whether or not the Lost Worlds flag is on
  #
  def setLostWorlds(self, lFlag):
    self.lostWorlds = lFlag
  
  #
  # Check if the player has the specified character
  #
  # param: character - Name of a character
  # return: true if the character has been acquired, false if not
  #
  def hasCharacter(self, character):
    return character in self.characters
    
  #
  # Add a character to the set of characters acquired
  #
  # param: character - The character to add
  #
  def addCharacter(self, character):
    self.characters.add(character)
    
  #
  # Remove a character from the set of characters acquired
  #
  # param: character: The character to remove
  #
  def removeCharacter(self, character):
    self.characters.discard(character)
    
  #
  # Check if the player has a given key item.
  #
  # param: item - The key item to check for
  # returns: True if the player has the key item, false if not
  #
  def hasKeyItem(self, item):
    return item in self.keyItems
  #
  # Add a key item to the set of key items acquired
  #
  # param: item - The Key Item to add
  #
  def addKeyItem(self, item):
    self.keyItems.add(item)
    
  #
  # Remove a key item from the set of key items acquired
  #
  # param: item: The Key Item to remove
  #
  def removeKeyItem(self, item):
    self.keyItems.discard(item)

  #
  # Determine which characters are available based on what key items/time periods
  # are available to the player.
  #
  # The character locations are provided at object construction.  The dictionary
  # is provided as output from running the characterwriter.py script.
  #
  def updateAvailableCharacters(self):
    # charLocations is a dictionary that uses the location name as
    # a key and the character data structure as a value.
    #
    # NOTE: The first entry in the character data is the character ID.
    #       Use the ID to get the correct character from the enum.

    # Empty the set just in case the placement algorithm had to 
    # backtrack and a character is no longer available.
    self.characters.clear()
    
    # The first four characters are always available.
    self.addCharacter(Characters(self.charLocations['start'][0]))
    self.addCharacter(Characters(self.charLocations['start2'][0]))
    self.addCharacter(Characters(self.charLocations['cathedral'][0]))
    self.addCharacter(Characters(self.charLocations['castle'][0]))
    
    # The remaining three characters are progression gated.
    if self.canAccessFuture():
      self.addCharacter(Characters(self.charLocations['proto'][0]))
    if self.canAccessDactylCharacter():
      self.addCharacter(Characters(self.charLocations['dactyl'][0]))
    if self.hasMasamune():
      self.addCharacter(Characters(self.charLocations['burrow'][0]))
  # end updateAvailableCharacters function
    
  #
  # Logic convenience functions.  These can be used to
  # quickly check if particular eras or locations are
  # logically accessible.
  #
  def canAccessDactylCharacter(self):
    # If character locking is on, dreamstone is required to get the
    # Dactyl Nest character in addition to prehistory access.
    return (self.canAccessPrehistory() and 
           ((not self.lockedChars) or self.hasKeyItem(KeyItems.dreamstone)))
  
  def canAccessFuture(self):
    return self.hasKeyItem(KeyItems.pendant) or self.lostWorlds
    
  def canAccessPrehistory(self):
    return self.hasKeyItem(KeyItems.gatekey) or self.lostWorlds
    
  def canAccessTyranoLair(self):
    return self.canAccessPrehistory() and self.hasKeyItem(KeyItems.dreamstone)
    
  def hasMasamune(self):
    return (self.hasKeyItem(KeyItems.hilt) and 
            self.hasKeyItem(KeyItems.blade))
            
  def canAccessMagusCastle(self):
    return (self.hasMasamune() and 
            self.hasCharacter(Characters.Frog))
    
  def canAccessDarkAges(self):
    return ((self.canAccessTyranoLair()) or
           (self.canAccessMagusCastle()) or
           (self.lostWorlds))
        
  def canAccessOceanPalace(self):
    return (self.canAccessDarkAges() and 
            self.hasKeyItem(KeyItems.rubyknife))
    
  def canAccessBlackOmen(self):
    return (self.canAccessFuture() and 
            self.hasKeyItem(KeyItems.clone) and 
            self.hasKeyItem(KeyItems.ctrigger))
  
  def canGetSunstone(self):
    return (self.canAccessFuture() and
            self.canAccessPrehistory() and
            self.hasKeyItem(KeyItems.moonstone))
  
  def canAccessKingsTrial(self):
    return (self.hasCharacter(Characters.Marle) and
            self.hasKeyItem(KeyItems.prismshard))
  
  def canAccessMelchiorsRefinements(self):
    return (self.canAccessKingsTrial() and
            self.canGetSunstone())
  
  def canAccessGiantsClaw(self):
    return self.hasKeyItem(KeyItems.tomapop)
    
  def canAccessRuins(self):
    return self.hasKeyItem(KeyItems.grandleon)
    
  def canAccessSealedChests(self):
    return (self.hasKeyItem(KeyItems.pendant) and 
           (self.earlyPendant or self.canAccessDarkAges()))
           
  def canAccessBurrowItem(self):
    return self.hasKeyItem(KeyItems.heromedal)
    
  def canAccessFionasShrine(self):
    return self.hasCharacter(Characters.Robo)
# End Game class

#
# This class represents a location within the game.
# It is the parent class for the different location types
#
class Location:
  def __init__(self, name, pointer):
    self.name = name
    self.pointer = pointer
    self.keyItem = None
    
  #
  # Get the name of this location.
  #
  # return: The name of this location
  #
  def getName(self):
    return self.name
    
  #
  # Get the pointer for this treasure location.
  #
  # return: The pointer for this treasure location
  #
  def getPointer(self):
    return self.pointer 
    
  #
  # Set the key item at this location.
  #
  # param: keyItem The key item to be placed at this location
  #
  def setKeyItem(self, keyItem):
    self.keyItem = keyItem
    
  #
  # Get the key item placed at this location.
  #
  # return: The key item being held in this location
  #
  def getKeyItem(self):
    return self.keyItem
    
  #
  # Unset the key item from this location.
  #
  def unsetKeyItem(self):
    self.keyItem = None
  
  #
  # Write the key item set to this location to a provided file handle.
  #
  # param: fileHandle The file to write the key item to
  #  
  def writeKeyItem(self, fileHandle):
    fileHandle.seek(self.getPointer())
    fileHandle.write(st.pack("B", self.getKeyItem().value))
  
# End Location class

#
# This Location type represents a location tied to an event.
# These are used for the sealed chests, which are not treated like normal chests.
# They have two pointers associated with them.
#
class EventLocation(Location):
  def __init__(self, name, pointer, pointer2):
    Location.__init__(self, name, pointer)
    self.pointer2 = pointer2

  #
  # Get the second pointer for this location.
  #
  def getPointer2(self):
    return self.pointer2
    
  #
  # Write the key item set to this location to a provided file handle.
  #
  # param: fileHandle The file to write the key item to
  #  
  def writeKeyItem(self, fileHandle):
    super().writeKeyItem(fileHandle)
    fileHandle.seek(self.getPointer2())
    fileHandle.write(st.pack("B", self.getKeyItem().value))
    
# End EventLocation class


#
# This class represents a normal check in the randomizer.
# EventLocation provides all of the pointers needed. 
# This class allows for a loot tier to be specified, that 
# will be used to assign a piece of loot to locations that
# were not assigned a key item.
#
class BaselineLocation(EventLocation):
  def __init__(self, name, pointer, pointer2, lootTier):
    EventLocation.__init__(self, name, pointer, pointer2)
    self.lootTier = lootTier
    
  #
  # Get the loot tier associated with this check.
  #
  # return: The loot tier associated with this check
  #
  def getLootTier(self):
    return self.lootTier
  
  #
  # Write the given treasure to the provided ROM file.
  #
  # param: treasure - Hex code for a treasure
  # param: fileHandle - The ROM file to write the treasure to
  #  
  def writeTreasure(self, treasure, fileHandle):
    fileHandle.seek(self.getPointer())
    fileHandle.write(st.pack("B", treasure))
    fileHandle.seek(self.getPointer2())
    fileHandle.write(st.pack("B", treasure))
  
# End BaselineLocation class

#
# This class represents a set of linked locations.  The key item will
# be set in both of the locations.  This is used for the blue pyramid
# where there are two chests but the player can only get one.
#
class LinkedLocation(Location):
  def __init__(self, name, location1, location2):
    Location.__init__(self, name, 0)
    self.location1 = location1
    self.location2 = location2
    
  #
  # Set the key item for both locations in this linked location.
  #
  def setKeyItem(self, keyItem):
    super().setKeyItem(keyItem)
    self.location1.setKeyItem(keyItem)
    self.location2.setKeyItem(keyItem)
    
  #
  # Unset the key item from this location.
  #
  def unsetKeyItem(self):
    self.keyItem = None
    self.location1.unsetKeyItem()
    self.location2.unsetKeyItem()
    
  #
  # Write the key item to both of the linked locations
  #
  def writeKeyItem(self, fileHandle):
    self.location1.writeKeyItem(fileHandle)
    self.location2.writeKeyItem(fileHandle)
# end LinkedLocation class
    
#
# This class represents a group of locations controlled by 
# the same access rule.
#
class LocationGroup:
  #
  # Constructor for a LocationGroup.
  #
  # param: name - The name of this LocationGroup
  # param: weight - The initial weighting factor of this LocationGroup
  # param: accessRule - A function used to determine if this LocationGroup is accessible
  # param: weightDecay - Optional function to define weight decay of this LocationGroup
  #
  def __init__(self, name, weight, accessRule, weightDecay = None):
    self.name = name
    self.locations = []
    self.weight = weight
    self.accessRule = accessRule
    self.weightDecay = weightDecay
    self.weightStack = []
    
    
  #
  # Return whether or not this location group is accessible.
  #
  # param: game - The game object with current game state
  # return: True if this location is accessible, false if not
  #
  def canAccess(self, game):
    return self.accessRule(game)
    
  #
  # Get the name of this location.
  #
  # return: The name of this location
  #
  def getName(self):
    return self.name
    
  #
  # Get the weight value being used to select locations from this group.
  #
  # return: Weight value used by this location group
  #
  def getWeight(self):
    return self.weight
    
  #
  # Set the weight used when selecting locations from this group.
  # The weight cannot be set less than 1.
  #
  # param: weight - Weight value to set
  #
  def setWeight(self, weight):
    if weight < 1:
      weight = 1
    self.weight = weight
  
  #
  # This function is used to decay the weight value of this 
  # LocationGroup when a location is chosen from it.
  #
  def decayWeight(self):
    self.weightStack.append(self.weight)
    if self.weightDecay == None:
      # If no weight decay function was given, reduce the weight of this
      # LocationGroup to 1 to make it unlikelyto get any other items.
      self.setWeight(1)
    else:
      self.setWeight(self.weightDecay(self.weight))
  
  #
  # Undo a previous weight decay of this LocationGroup.
  # The previous weight values are stored in the weightStack.
  #
  def undoWeightDecay(self):
    if len(self.weightStack) > 0:
      self.setWeight(self.weightStack.pop())
  
  #
  # Get the number of available locations in this group.
  #
  # return: The number of locations in this group
  #
  def getAvailableLocationCount(self):
    return len(self.locations)
  
  #
  # Add a location to this location group. If the location is 
  # already part of this location group then nothing happens.
  #
  # param: location - A location object to add to this location group
  #
  def addLocation(self, location):
    if not location in self.locations:
      self.locations.append(location)
    return self
  
  #
  # Remove a location from this group.
  #
  # param: location - Location to remove from this group
  #
  def removeLocation(self, location):
    self.locations.remove(location)
  
  #
  # Get a list of all locations that are part of this location group.
  #
  # return: List of locations associated with this location group
  #
  def getLocations(self):
    return self.locations.copy()
# End LocationGroup class