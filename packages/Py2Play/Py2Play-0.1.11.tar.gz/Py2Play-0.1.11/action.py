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

import struct, thread, time, select, socket
import py2play.idler as idler
#from py2play import recvall

from socket import error as SocketError

MINIMUM_QUEUE_LENGHT = 3

ACTION_WAIT    = " "
ACTION_STALLED = "S"

class Action:
  def __init__(self, action = ACTION_WAIT, round = None):
    self.round  = round
    self.action = action
    
  def __repr__(self):
    return "<Action %s at round %s>" % (self.action, self.round)


#def WRITE_ACTION(socket, action):
#  socket.sendall(action.action)
#  socket.sendall(struct.pack("!i", action.round))
  
#def READ_ACTION(socket):
#  return Action(recvall(socket, 1), struct.unpack("!i", recvall(socket, 4))[0])
  

class ActiveQueue:
  def __init__(self, round = 0):
    self.round       = round
    self.actions     = []
    self.old_actions = []
    self.listeners   = []
    self.lock        = thread.allocate_lock()
    self.next_action = None
    self.fill()
    
  def plan_action(self, action):
    self.next_action = action
    
  def append(self, action):
    self.lock.acquire() # Lock to avoid that different threads call this method simultaneously.
    
    action.round = self.round
    
    i = 0
    while i < len(self.listeners):
      try:
        WRITE_ACTION(self.listeners[i], action)
        i = i + 1
      except SocketError:
        print "* Py2Play * An actions listener has close its connexion."
        del self.listeners[i]
        
    self.actions.append(action)
    self.old_actions.append(action)
    if len(self.old_actions) > 5000: del self.old_actions[0]
    self.round = self.round + 1
    
    self.lock.release()
    
  def fill(self):
    #if len(self.actions) > MINIMUM_QUEUE_LENGHT:
    #  print "TooManyAction", len(self.actions)
    
    if len(self.actions) < MINIMUM_QUEUE_LENGHT:
      if self.next_action:
        self.append(self.next_action)
        self.next_action = None
      while len(self.actions) < MINIMUM_QUEUE_LENGHT: self.append(Action())
      
  def pop(self, round):
    action = self.actions.pop(0)
    
    if round != action.round:
      print "* Py2Play * ERROR : playing action for round %s but character is at round %s !" % (action.round, round)
    
    return action
  
  def recover_actions(self, start_round, end_round = None):
    first = self.old_actions[0].round
    
    if start_round < first:
      print "* Py2Play * ERROR : cannot recover action %s, it's too old !" % start_round
      return ()
    
    if not end_round:
      end_round = self.round
    elif end_round >= self.round:
      print "* Py2Play * ERROR : cannot recover action %s, i don't have it yet ! I wait for them." % end_round
      while end_round >= self.round: time.sleep(0.003)
      
    return self.old_actions[start_round - first : end_round - first]
  
  def __len__(self): return len(self.actions)


_EMPTY = []

class PhantomQueue:
  def __init__(self, socket, player):
    self.actions = []
    self.socket  = socket
    self.player  = player
    self.socket  = socket
    self.check_late = 1
    
  def ____fill(self):
    if len(self.actions) < 1:
      try:
        while 1:
          if not select.select([self.socket], _EMPTY, _EMPTY, 0)[0]:
            print "attente..."
            idler.IDLER.accel(-1)
            
          self.actions.append(READ_ACTION(self.socket))
          
          if not select.select([self.socket], _EMPTY, _EMPTY, 0)[0]: break
          
      except:
        import sys
        sys.excepthook(*sys.exc_info())
        
        print "* Py2Play * a character is no longer reachable : %s." % self.player.name
        self.actions.append(Action())
        
        if self.player.character in self.player.level.characters:
          self.player.level.remove_character(self.player.character)
          
  def fill(self):
    if len(self.actions) < 1:
      try:
        if not select.select([self.socket], _EMPTY, _EMPTY, 0)[0]:
          t = time.time()
          self.actions.append(READ_ACTION(self.socket))
          t = t - time.time()
          
          idler.IDLER.accel(t / idler.ROUND_DURATION)
        else:
          #t = time.time()
          self.actions.append(READ_ACTION(self.socket))
          #t = t - time.time()
          #
          #idler.IDLER.accel(t / idler.ROUND_DURATION)
          
      except:
        import sys
        sys.excepthook(*sys.exc_info())
        
        print "* Py2Play * player %s is no longer reachable ! Removing him/her." % self.player.name
        self.actions.append(Action())
        
        if self.player.character in self.player.level.characters:
          self.player.level.remove_character(self.player.character)
          
  def ____pop(self, round = None):
    if (not round is None) and (self.actions) and (not self.actions[-1].round is None):
      #if self.actions[-1].round - round > MINIMUM_QUEUE_LENGHT:
      if self.actions[-1].round - round >= MINIMUM_QUEUE_LENGHT:
        if self.check_late:
          idler.IDLER.accel(self.actions[-1].round - round - MINIMUM_QUEUE_LENGHT + 1)
          self.check_late = 0
      else: self.check_late = 1
      
    if not self.actions: self.fill()
    
    #return self.actions[0]
    action = self.actions.pop(0)
		
    if (not round is None) and (not action.round is None):
      if   round > action.round:
        print "* Py2Play * WARNING : character is at round %s but the next action is for round %s ! Skipping." % (round, action.round)
        self.fill()
        return self.pop(round)
      elif round < action.round:
        print "* Py2Play * actions from round %s to round %s are lacking... i ask for them." % (round, action.round)
        actions = self.player.question_actions(round, action.round)
        if actions is None: print "* Py2Play * ERROR : cannot question for actions %s to % !" % (round, action.round)
        self.actions = actions[1:] + [action] + self.actions
        return actions[0]
      
    return action

  
  def pop(self, round = None):
    #if (not round is None) and (self.actions) and (not self.actions[-1].round is None):
    #  #if self.actions[-1].round - round > MINIMUM_QUEUE_LENGHT:
    #  if self.actions[-1].round - round >= MINIMUM_QUEUE_LENGHT:
    #    if self.check_late:
    #      idler.IDLER.accel(self.actions[-1].round - round - MINIMUM_QUEUE_LENGHT + 1)
    #      self.check_late = 0
    #  else: self.check_late = 1
      
    if not self.actions: self.fill()
    action = self.actions.pop(0)
		
    if (not round is None) and (not action.round is None):
      if   round > action.round:
        print "* Py2Play * WARNING : character is at round %s but the next action is for round %s ! Skipping." % (round, action.round)
        self.fill()
        return self.pop(round)
      elif round < action.round:
        print "* Py2Play * actions from round %s to round %s are lacking... i ask for them." % (round, action.round)
        actions = self.player.question_actions(round, action.round)
        if actions is None: print "* Py2Play * ERROR : cannot question for actions %s to % !" % (round, action.round)
        self.actions = actions[1:] + [action] + self.actions
        return actions[0]
      
    return action
 
  def __len__(self): return len(self.actions)




