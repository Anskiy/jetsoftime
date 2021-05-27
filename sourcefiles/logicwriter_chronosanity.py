# Python libraries
import enum
import random as rand
import struct as st

# jets of time libraries
import characterwriter as chars
import logicfactory
import logictypes
import treasurewriter as treasure

#
# This script file implements the Chronosanity logic.
# It uses a weighted random distribution to place key items
# based on logical access rules per location.  Any baseline key
# item location that does not get a key item assigned to it will
# be assigned a random treasure.
#

# Script variables
locationGroups = []

#
# Get a list of LocationGroups that are available for key item placement.
#
# param: game - Game object used to determine location access
#
# return: List of all available LocationGroups
#
def getAvailableLocations(game):
  # Have the game object update what characters are available based on the
  # currently available items and time periods.
  game.updateAvailableCharacters()
  
  # Get a list of all accessible location groups
  accessibleLocationGroups = []
  for locationGroup in locationGroups:
    if locationGroup.canAccess(game):
      if locationGroup.getAvailableLocationCount() > 0:
        accessibleLocationGroups.append(locationGroup)
  
  return accessibleLocationGroups
  
# end getAvailableLocations

#
# Given a list of LocationGroups, get a random location.
#
# param: groups - List of LocationGroups
# 
# return: The LocationGroup the Location was chosen from
# return: A Location randomly chosen from the groups list
#
def getRandomLocation(groups):
  # get the max rand value from the combined weightings of the location groups
  # This will be used to help select a location group
  weightTotal = 0
  for group in groups:
    weightTotal = weightTotal + group.getWeight()
  
  # Select a location group
  locationChoice = rand.randint(1, weightTotal)
  counter = 0
  chosenGroup = None
  for group in groups:
    counter = counter + group.getWeight()
    if counter >= locationChoice:
      chosenGroup = group
      break
    
  # Select a random location from the chosen location group.
  location = rand.choice(chosenGroup.getLocations())
  
  return chosenGroup, location
# end getRandomLocation

#
# Given a weighted list of key items, get a shuffled
# version of the list with only a single copy of each item.
#
# param: weightedList - Weighted key item list
#
# return: Shuffled list of key items with duplicates removed
#
def getShuffledKeyItemList(weightedList):
  tempList = weightedList.copy()
  rand.shuffle(tempList)
  
  keyItemList = []
  for keyItem in tempList:
    if not (keyItem in keyItemList):
      keyItemList.append(keyItem)
  
  return keyItemList
# end getShuffledKeyItemList

#
# Randomly place key items.
#
# param: gameConfig A GameConfig object with the configuration information
#                   necessary to place keys for the selected game type
#
# return: A tuple containing:
#             A Boolean indicating whether or not key item placement was successful
#             A list of locations with key items assigned
#
def determineKeyItemPlacement(gameConfig):
  global locationGroups
  locationGroups = gameConfig.getLocations()
  game = gameConfig.getGame()
  remainingKeyItems = gameConfig.getKeyItemList()
  chosenLocations = []
  return determineKeyItemPlacement_impl(chosenLocations, remainingKeyItems, game)
# end place_key_items


#
# NOTE: Do not call this function directly. This will be called 
#       by determineKeyItemPlacement after setting up the parameters
#       needed by this function.
#
# This function will recursively determine key item locations
# such that a seed can be 100% completed.  This uses a weighted random
# approach to placement and will only consider logically accessible locations.
#
# The algorithm for determining locations - For each recursion:
#   If there are no key items remaining, unwind the recursion, otherwise
#     Get a list of logically accessible locations
#     Choose a location randomly (locations are weighted)
#     Get a shuffled list of the remaining key items
#     Loop through the key item list, trying each one in the chosen location
#       Recurse and try the next location/key item
#     
#
# param: chosenLocations - List of locations already chosen for key items
# param: remainingKeyItems - List of key items remaining to be placed
# param: game - Game object used to determine logic
#
# return: A tuple containing:
#             A Boolean indicating whether or not key item placement was successful
#             A list of locations with key items assigned
#
def determineKeyItemPlacement_impl(chosenLocations, remainingKeyItems, game):
  if len(remainingKeyItems) == 0:
    # We've placed all key items.  This is our breakout condition
    return True, chosenLocations
  else:
    # We still have key items to place.
    availableLocations = getAvailableLocations(game)
    if len(availableLocations) == 0:
      # This item configuration is not completable. 
      return False, chosenLocations
    else:
      # Continue placing key items.
      keyItemConfirmed = False
      returnedChosenLocations = None
      
      # Choose a random location
      locationGroup, location = getRandomLocation(availableLocations)
      locationGroup.removeLocation(location)
      locationGroup.decayWeight()
      chosenLocations.append(location)
      
      # If 2/3 of the key items have been placed
      # then remove the key item bias from the remaining list.
      # This is to slightly reduce the occurrence of the lowest weighted
      # items from showing up dispraportionately on extremely late checks
      # like Mount Woe or the Guardia Treasury.
      # TODO - Move this out of the general item placement code and into chronosanity specific code (gameconfig?)
      if game.getKeyItemCount() == 10:
        newList = []
        for key in remainingKeyItems:
          if not key in newList:
            newList.append(key)
        remainingKeyItems = newList
      
      # Use the weighted key item list to get a list of key items
      # that we can loop through and attempt to place.
      localKeyItemList = getShuffledKeyItemList(remainingKeyItems)
      for keyItem in localKeyItemList:
        # Try placing this key item and then recurse
        location.setKeyItem(keyItem)
        game.addKeyItem(keyItem)
        
        newKeyItemList = [x for x in remainingKeyItems if x != keyItem]
        # recurse and try to place the next key item.
        keyItemConfirmed, returnedChosenLocations = \
            determineKeyItemPlacement_impl(chosenLocations, newKeyItemList, game)
        
        if keyItemConfirmed:
          # We're unwinding the recursion here, all key items are placed.
          return keyItemConfirmed, returnedChosenLocations
        else:
          game.removeKeyItem(keyItem)
      # end keyItem loop
      
      # If we get here, we failed to place an item.  Undo location modifications
      locationGroup.addLocation(location)
      locationGroup.undoWeightDecay()
      chosenLocations.remove(location)
      location.unsetKeyItem()
      
      return False, chosenLocations

# end determineKeyItemPlacement_impl recursive function

#
# Write out the spoiler log.
#
# param: chosenLocations - List of locations containing key items
# param: charLocations - Dictionary of locations to characters
#
def writeSpoilerLog(chosenLocations, charLocations):
  spoilerLog = open("spoiler_log.txt","w+")
  # Write the key item location to the spoiler log
  
  spoilerLog.write("Key ItemLocations:\n")
  for location in chosenLocations:
    spoilerLog.write("  " + location.getName() + ": " + location.getKeyItem().name + "\n")
  
  # Write the character locations to the spoiler log
  spoilerLog.write("\n\nCharacter Locations:\n")
  for loc, char in charLocations.items():
    character = logictypes.Characters(char[0])
    spoilerLog.write("  " + loc + ": " + character.name + "\n")
  spoilerLog.close()


#
# Get a random treasure for a baseline location.
# This function uses the loot selection algorithm from treasures.py.
# Loot tiers are set as part of the location construction.
#
# param: location - BaselineLocation that needs loot 
#
# return: The item code for a random treasure
#
def getRandomTreasure(location):
  treasureCode = 0;
  
  lootTier = location.getLootTier()
  # loot selection algorithm stolen from treasurewriter.py
  rand_num = rand.randrange(0,11,1)
  # Mid tier loot - early checks
  if lootTier == logictypes.LootTiers.Mid:
    if rand_num > 5:
      treasureCode = rand.choice(treasure.plvlconsumables + \
                                 treasure.mlvlconsumables)
    else:
      rand_num = rand.randrange(0,100,1)
      if rand_num > 74:
        if rand_num > 94:
          treasureCode = rand.choice(treasure.hlvlitems)
        else:
          treasureCode = rand.choice(treasure.glvlitems)
      else:
        treasureCode = rand.choice(treasure.mlvlitems)
        
  # Mid-high tier loot - moderately gated or more difficult checks
  elif lootTier == logictypes.LootTiers.MidHigh:
    if rand_num > 5:
      treasureCode = rand.choice(treasure.mlvlconsumables + \
                                 treasure.glvlconsumables)
    else:
      rand_num = rand.randrange(0,100,1)
      if rand_num > 74:
        if rand_num > 94:
          treasureCode = rand.choice(treasure.alvlitems)
        else:
          treasureCode = rand.choice(treasure.hlvlitems)
      else:
        treasureCode = rand.choice(treasure.glvlitems)
  
  # High tier loot - Late or difficult checks
  elif lootTier == logictypes.LootTiers.High:
    if rand_num > 6:
      treasureCode = rand.choice(treasure.glvlconsumables + \
                                 treasure.hlvlconsumables + \
                                 treasure.alvlconsumables)
    else:
      rand_num = rand.randrange(0,100,1)
      if rand_num > 74:
        treasureCode = rand.choice(treasure.alvlitems)
      else:
        treasureCode = rand.choice(treasure.glvlitems + \
                                   treasure.hlvlitems)
                                
  return treasureCode
# end getRandomTreasure function
    
   
#
# Determine key item placements and write them to the provided ROM file.
# Additionally, a spoiler log is written that lists where the key items and
# characters were placed.
#
# param: outFile - File name of the output ROM
# param: charLocations - Dictionary of character locations from characterwriter.py
# param: lockedChars - Whether or not the locked characters flag is selected
# param: earlyPendant - Whether or not the early pendant charge flag is selected
# param: lostWorlds - Whether or not the Lost Worlds flag is selected
#
def writeKeyItems(outFile, charLocations, lockedChars, earlyPendant, lostWorlds):
  # Get a game configuration for the provided flags
  gameConfig = logicfactory.getGameConfig(True, lostWorlds, earlyPendant, lockedChars, charLocations)

  # Determine placements for the key items
  success, chosenLocations = determineKeyItemPlacement(gameConfig)
  
  if not success:
    print("Unable to place key items.")
    return
  
  # Write key items to their locations in the ROM.
  romFile = open(outFile, "r+b")
  for location in chosenLocations:
    location.writeKeyItem(romFile)
  
  # Go through any baseline locations not assigned an item and place a 
  # piece of treasure. Treasure quality is based on the location's loot tier.
  for locationGroup in locationGroups:
    for location in locationGroup.getLocations():
      if type(location) == logictypes.BaselineLocation and (not location in chosenLocations):
        # This is a baseline location without a key item.  
        # Assign a piece of treasure.
        treasureCode = getRandomTreasure(location)
        location.writeTreasure(treasureCode, romFile)
  
  romFile.close()
  
  writeSpoilerLog(chosenLocations, charLocations)
  
# End writeKeyItems function

