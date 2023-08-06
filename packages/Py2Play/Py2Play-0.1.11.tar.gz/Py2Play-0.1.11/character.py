# -*- coding: utf-8 -*-

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

import random
import py2play.action as action, py2play.player as player

class PlayerCharacter(object):
  played = 1
  def __init__(self, player, round = 0):
    self.player         = player
    self.level          = None
    self.round          = round
    self.current_action = None
    self.random         = random.Random()
    
    if player: player.set_character(self)
    
  def set_level(self, level, init = 0):
    if not self.level is None:
      self.level.remove_character(self)
    self.level = level
    
    #idler.IDLER.next_round_tasks.append(lambda :
    level.add_character(self)
    
    if init: level.init_character(self)
    
    self.player.set_level(level)
    
  def plan_action(self, action): self.player.queue.plan_action(action)
  
  def begin_action(self, action): pass
  
  def begin_round(self):
    self.player.queue.fill()
    self.current_action = self.player.queue.pop(self.round)
    self.round = self.round + 1

    self.begin_action(self.current_action)
    
  def play_n_round(self, n):
    for i in range(n):
      self.advance_time(1.0)
      
      self.current_action = self.player.queue.pop(self.round)
      self.round = self.round + 1
      self.begin_action(self.current_action)
      
  def advance_time(self, proportion): pass
  
  def __getstate__(self):
    my_super = super(PlayerCharacter, self)
    if hasattr(my_super, "__getstate__"): state = my_super.__getstate__()
    else:                                 state = self.__dict__.copy()
    return self._treat_getstate(state)
  
  def _treat_getstate(self, state):
    if state is self.__dict__: state = state.copy()
    del state["player"] # Do NOT send the player (player contains socket and other non-pickleable object)
    state["player_info"] = self.player.my_info # Infos needed to recreate a PhantomPlayer at unpickling time
    
    state["level"] = None # Do NOT send the level (too big !)
    state["level_name"] = self.level.name # Infos needed to regenerate the level
    
    return state
  
  def __setstate__(self, state):
    my_super = super(PlayerCharacter, self)
    if hasattr(my_super, "__setstate__"): my_super.__setstate__(state)
    else:                                 self.__dict__ = state
    self._treat_setstate(state)
    
  def _treat_setstate(self, state):
    if (not player.CURRENT_PLAYER) or (self.player_info != player.CURRENT_PLAYER.my_info):
      self.player = player.PhantomPlayer(*self.player_info)
      self.player.set_character(self)
    else: self.player = None
    
    del self.player_info
    
  def regenerate_level(self):
    import py2play.level as level
    
    lev = level.get(self.level_name)
    
    if filter(lambda character: character.played and (character.player.name == self.player.name), lev.characters):
      print "%s dupliqué !!!!!!!!!!!!!!" % self.player.name
      
    self.set_level(lev)
    
  def __repr__(self): return "<Character %s>" % self.player.name

    
class NonPlayerCharacter(object):
  played = 0
  def __init__(self, round = 0):
    self.level          = None
    self.round          = round
    self.current_action = None
    
  def set_level(self, level, init = 0):
    if not self.level is None: self.level.remove_character(self)
    old_level = self.level
    self.level = level
    
    if old_level:
      import py2play.level
      
      for lev in py2play.level._levels.values():
        for character in lev.characters:
          if character.played and (character.player.name < player.CURRENT_PLAYER.name):
            return # This player has a higher priority to advertise the other about this level changement.
          
      #for character in old_level.characters: # XXX multiple active levels
      #  if character.played and (character.player.name < player.CURRENT_PLAYER.name):
      #    return # This player has a higher priority to advertise the other about this level changement.
          
    level.add_character(self)
    if init: level.init_character(self)
    
    if old_level:
      for character in level.characters:
        #if character.played and (not character.player is player.CURRENT_PLAYER) and ((not old_level) or (not character in old_level.characters)):  # XXX multiple active levels
        if character.played and (not character.player is player.CURRENT_PLAYER) and (not character in old_level.characters):  # XXX multiple active levels
          character.player.question_addcharacter(self, self.round - character.round)
          
  def begin_round(self):
    self.current_action = self.choose_action()
    self.round = self.round + 1
    self.begin_action(self.current_action)
    
  def choose_action(self): pass
  
  def begin_action(self, action): pass
  
  def advance_time(self, proportion): pass
  
  def play_n_round(self, n):
    for i in range(n):
      self.advance_time(1.0)
      
      self.current_action = self.choose_action()
      self.round = self.round + 1
      self.begin_action(self.current_action)
      
  def __getstate__(self):
    my_super = super(NonPlayerCharacter, self)
    if hasattr(my_super, "__getstate__"): state = my_super.__getstate__()
    else:                                 state = self.__dict__.copy()
    return self._treat_getstate(state)

  def _treat_getstate(self, state):
    state["level"] = None # Do NOT send the level (too big !)
    state["level_name"] = self.level.name # Infos needed to regenerate the level
    return state
  
  def regenerate_level(self):
    import py2play.level as level
    
    # self.set_level(level.get(self.level_name))
    self.level = level.get(self.level_name)
    
    if filter(lambda character: not character.played, self.level.characters):
      print "Monstre dupliqué !!!!!!!!!!!!!!"
    else:
      self.level.add_character(self)
    
  def __repr__(self): return "<Monster>"
    
    
