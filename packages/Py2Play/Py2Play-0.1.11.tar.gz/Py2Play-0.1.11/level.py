# Py2Play
# Copyright (C) 2001-2002 Jean-Baptiste LAMY
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import py2play.player as player, random

_levels = {}

def CREATE(level_name):
  print "* P2Play * ERROR : you MUST override p2play.level.create !"

def store(level):
  if level.name and (level.name in _levels.keys()) and (not level is _levels[level.name]):
    raise Warning("Overriding level %s !" % level.name)
  _levels[level.name] = level
  
def burry(level_name):
  del _levels[level_name]

def clear():
  _levels.clear()

def get_local(level_name):
  return _levels.get(level_name)

def get(level_name):
  level = _levels.get(level_name)
  if level: return level
  
  if player.CURRENT_PLAYER:
    random.shuffle(player.CURRENT_PLAYER.players_info)
    for player_info in player.CURRENT_PLAYER.players_info:
      if player_info != player.CURRENT_PLAYER.my_info: # Skip active player (= this player is local !)
        phantom = player.PhantomPlayer(*player_info)
        level = phantom.question_getlevel(level_name)
        if not level is None: return level
        
  level = CREATE(level_name)
  return level


class Level(object):
  def __init__(self, name):
    self.name       = name
    self.characters = []
    self.active     = 0
    
    #print "store %s : new !" % (self.name,)
    store(self)
    
  def add_character(self, character):
    #if (not character.played) and filter(lambda character: not character.played, self.characters):
    #  raise "DuplicatedMonster"
    
    self.characters.append(character)
    
    # Aligns non-player character's random generator on the level's random generator
    # (So as, if the NPC has been created by 2 different players, they would have the
    # same random generator).
    if not character.played:
      character.random = random.Random(self.random.randrange(10000))
      
  def init_character(self, character): pass
  
  def remove_character(self, character):
    self.characters.remove(character)
    
  def set_active(self, active):
    self.active = active
    
    if active:
      if not hasattr(self, "random"): self.random = random.Random()
      
      #print "store %s : activate !" % (self.name,)
      store(self)
      
      for character in self.characters:
        if character.played and (not character.player.active):
          #print "Level: LISTENING AT", character.player.name, "!!!!!!!!!!!!!!!!!!!!"
          character.player.listen_actions(character.round)
          
    else:
      for character in self.characters:
        if character.played and (not character.player.active):
          #print "Level: STOP LISTENING AT", character.player.name, "..................."
          character.player.stop_listen_actions()
          
      if filter(lambda character: character.played, self.characters):
        #print "burry %s : hidden !" % (self.name,)
        burry(self.name) # This level will now be stored by another player.
        
  def sent(self):
    if not self.active:
      #print "burry %s : sent !" % (self.name,)
      import py2play.idler as idler
      
      #idler.IDLER.next_round_tasks.append(lambda : burry(self.name))
      burry(self.name)
      
  def __setstate__(self, state):
    my_super = super(Level, self)
    if hasattr(my_super, "__setstate__"): my_super.__setstate__(state)
    else:                                 self.__dict__ = state
    
    i = 0
    while i < len(self.characters):
      if self.characters[i].played:
        if self.characters[i].player:
          self.characters[i].level = self
          self.characters[i].player.level = self
        else:
          del self.characters[i] # Player was deleted if character is the current active player's character !
          continue
      else:
        self.characters[i].level = self
      i = i + 1
      
    if self.active: # Level was active in the sender's game
      self.active = 0
    else: # Level was not active => it has been burried ! => we MUST keep it !
      #print "store %s : received not active !" % (self.name,)
      store(self) # Ici au lieu de celui de set_active ???
      

