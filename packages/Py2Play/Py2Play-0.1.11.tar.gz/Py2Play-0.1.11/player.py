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

import sys, socket, thread, struct, random, weakref
import cPickle as pickle
import __init__, py2play.action as action, py2play.idler as idler
#from py2play import recvall

QUESTION_VERSION          = "v"
QUESTION_NAME             = "n"
QUESTION_ADDRESS          = "a"
QUESTION_PLAYERS          = "p"
QUESTION_ADD_PLAYER       = "+"
QUESTION_REMOVE_PLAYER    = "-"
QUESTION_ADD_CHARACTER    = "C"
QUESTION_REMOVE_CHARACTER = "c"
QUESTION_ROUND            = "r"
QUESTION_LISTEN_ACTIONS   = "i"
QUESTION_ACTIONS          = "A"
QUESTION_GET_LEVEL        = "l"
QUESTION_CURRENT_LEVEL    = "L"
QUESTION_SEARCH_LEVEL     = "s"
QUESTION_LIST_LEVELS      = "%"
QUESTION_STORE_LEVELS     = "S"

CURRENT_PLAYER = None

class NonCompatibleVersionError: pass

class Player:
  def __init__(self, name, host = "", port = 36079):
    if host: self.host = host
    else:    self.host = socket.gethostname()
    self.name          = name
    self.port          = port
    self.queue         = None
    
  def set_character(self, character):
    self.character = character
    
  def set_level(self, level):
    self.level = level
    
class ActivePlayer(Player):
  active = 1
  def __init__(self, level, name, host = "", port = 36079):
    Player.__init__(self, name, host, port)
    
    self.level = level
    self.queue = action.ActiveQueue()
    self.socket_to_close = []
    
    self.my_info = (self.name, self.host, self.port)
    self.players_info = [self.my_info]
    print "* Py2Play * creating active player %s : %s..." % (name, self.my_info)
    
    self.open_port()
    
    global CURRENT_PLAYER
    CURRENT_PLAYER = self
    
  def parrained_by(self, host, port = 36079):
    parrain = PhantomPlayer(None, host, port)
    self.parrain_info = (parrain.name, host, port)
    print "* Py2Play * parrained by %s : %s..." % (parrain.name, self.parrain_info)
    
    parrain_version = parrain.question_version()
    if parrain_version != __init__.VERSION: raise NonCompatibleVersionError, parrain_version
    
    print "parrain V", parrain_version
    
    new = players_info2 = parrain.question_players()
    
    while len(new) > 0:
      for player_info in new:
        phantom = PhantomPlayer(*player_info)
        phantom.question_addplayer(self.my_info)
        
      players_info = players_info2
      
      # Check if another player has been added while adding this one...
      players_info2 = parrain.question_players()
      players_info2.remove(self.my_info)
      new = filter(lambda player_info: not player_info in players_info, players_info2)
      
    self.players_info.extend(players_info)
    
    self.level = parrain.question_currentlevel()
    
  def set_level(self, level):
    Player.set_level(self, level)
    
    for character in level.characters:
      if character.played and (not character.player is self):
        character.player.question_addcharacter(self.character, self.character.round - character.round)
        
  def end_game(self):
    import py2play.level as level

    if self.character in self.level.characters:
      self.level.remove_character(self.character)
    
    if len(self.players_info) > 1: # If the game still exists, send all the levels this player owns to a randomly choosen player
      self.players_info.remove(self.my_info)
      
      player = random.choice(self.players_info)
      
      # Send only level without any other player (Else this player already stores it).
      levels = filter(lambda lev: not filter(lambda character: character.played, lev.characters), level._levels.values())
      print "* Py2Play * sending levels %s to %s..." % (map(lambda lev: lev.name, levels), player[0])
      PhantomPlayer(*player).question_storelevels(levels)
      
      # Remove this player from the game
      for player in self.players_info:
        PhantomPlayer(*player).question_removeplayer(self.my_info)
        
    self.close_port()
    
    for phantom in _phantoms.values(): phantom.stop_listen_actions()
      
  def open_port(self):
    #self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #self.socket.bind(("", self.port))
    #self.socket.listen(5)
    
    self.port_opened = 1
    
    #thread.start_new_thread(self.listen_port, ())
    
  def close_port(self):
    #for socket in self.socket_to_close: socket.close()
    self.port_opened = 0
    #self.socket.shutdown(2)
    #self.socket.close()
    
  def listen_port(self):
    pass
#     while self.port_opened:
#       try: s, addr = self.socket.accept()
#       except socket.error, data:
#         if not self.port_opened: break # The socket has been closed
#         else: raise socket.error, data
#       try:
#         question = recvall(s, 1)
#         print "* Py2Play * receiving question %s..." % question
        
#         if question == QUESTION_NAME:
#           s.sendall(self.name)
#           print "name sent !"
          
#         elif question == QUESTION_VERSION:
#           s.sendall(__init__.VERSION)
#           print "version number sent !"
          
#         elif question == QUESTION_ADDRESS:
#           s.sendall(pickle.dumps(self.my_info, 2))
#           print "address sent !"
          
#         elif question == QUESTION_LISTEN_ACTIONS:
#           print "* Py2Play * %s wants to listen my actions." % (s.getpeername(),)
          
#           since_round = struct.unpack("!i", recvall(s, 4))[0]
          
#           self.socket_to_close.append(s)
          
#           if since_round != -1:
#             for act in self.queue.recover_actions(since_round):
#               action.WRITE_ACTION(s, act)
              
#           self.queue.listeners.append(s)
#           continue # Don't close socket!
        
#         elif question == QUESTION_GET_LEVEL:
#           import py2play.level as level
#           level_name = pickle.load(s.makefile("rb"))
#           lev = level.get_local(level_name)
#           if lev is None:
#             s.sendall("0")
#             print "i don't have level %s !" % (level_name,)

#           else:
#             s.sendall("1")
#             #lev.sent()
#             #pickle.dump(lev, s.makefile("wb"), 2)
#             #print "level %s sent !" % (level_name,)

#             def sendlevel(s = s):
#               lev.sent()
#               pickle.dump(lev, s.makefile("wb"), 2)
#               print "level %s sent !" % (level_name,)
#               s.close()

#             idler.IDLER.next_round_tasks.append(sendlevel)
#             continue # Don't close socket!

#         elif question == QUESTION_SEARCH_LEVEL:
#           import py2play.level as level
#           level_name = pickle.load(s.makefile("rb"))
#           lev = level.get(level_name)
#           #lev.sent()
#           #pickle.dump(lev, s.makefile("wb"), 2)
#           #print "level %s sent !" % (level_name,)

#           def sendlevel(s = s):
#             lev.sent()
#             pickle.dump(lev, s.makefile("wb"), 2)
#             print "level %s sent !" % (level_name,)
#             s.close()

#           idler.IDLER.next_round_tasks.append(sendlevel)
#           continue # Don't close socket!

#         elif question == QUESTION_LIST_LEVELS:
#           import py2play.level as level
#           pickle.dump(level._levels.keys(), s.makefile("wb"), 2)
#           print "levels list sent !"

#         elif question == QUESTION_STORE_LEVELS:
#           import py2play.level as level
#           levels = pickle.load(s.makefile("rb"))
#           for lev in levels: level.store(lev)
#           print "levels %s stored !" % map(lambda lev: lev.name, levels)
          
#         elif question == QUESTION_CURRENT_LEVEL:
#           def sendlevel(s = s):
#             self.level.sent()
#             pickle.dump(self.level, s.makefile("wb"), 2)
#             print "current level %s sent !" % (self.level.name,)
#             s.close()
            
#           idler.IDLER.next_round_tasks.append(sendlevel)
#           continue # Don't close socket!

#         elif question == QUESTION_ACTIONS:
#           start_round, end_round = struct.unpack("!ii", recvall(s, 8))
#           actions = self.queue.recover_actions(start_round, end_round)

#           s.sendall(struct.pack("!i", len(actions)))
#           for act in actions: action.WRITE_ACTION(s, act)

#           print "actions from round %s to round %s sent !" % (start_round, end_round)

#         elif question == QUESTION_PLAYERS:
#           s.sendall(pickle.dumps(self.players_info, 2))
#           print "players sent !"

#         elif question == QUESTION_ADD_PLAYER:
#           player_info = pickle.loads(s.makefile("rb").read())
#           if not player_info in self.players_info:
#             self.players_info.append(player_info)
#             print "player %s join the game !" % (player_info,)

#         elif question == QUESTION_REMOVE_PLAYER:
#           player_info = pickle.loads(s.makefile("rb").read())
#           self.players_info.remove(player_info)
#           print "player %s quit the game !" % (player_info,)

#         elif question == QUESTION_ADD_CHARACTER:
#           character, round_offset = pickle.loads(s.makefile("rb").read())
          
#           if character.played: print "character %s is visible !" % (character.player.name,)
#           else:                print "monster is visible !"
          
#           def addplayer():
#             character.regenerate_level()

#             delta = round_offset - (character.round - self.character.round)

#             if delta < 0: print "* Py2Play * Negative time for transmitting character! Skipping."
#             else: character.play_n_round(delta)

#           # Add the character in its level ON THE NEXT ROUND !
#           idler.IDLER.next_round_tasks.append(addplayer)

#         elif question == QUESTION_REMOVE_CHARACTER:
#           character = pickle.loads(s.makefile("rb").read())
#           print "character %s is no longer visible !" % (character.player.name,)

#         elif question == QUESTION_ROUND:
#           s.sendall(str(self.character.round))
#           print "round sent !"

#         else:
#           print "WARNING : unknown question '%s' received from %s !" % (`question`, s.getpeername())

#         s.close()
#       except:
#         sys.excepthook(*sys.exc_info())
#     print "* Py2Play * listen_port's thread finished !"
    
    
def PhantomPlayer(name = None, host = "", port = 36079):
  if CURRENT_PLAYER and (name == CURRENT_PLAYER.name): raise "NotPhantomPlayerError"
  
  phantom = _phantoms.get((host, port))
  if not phantom:
    phantom = _PhantomPlayer(name, host, port)
    _phantoms[host, port] = phantom
  return phantom
  
_phantoms = weakref.WeakValueDictionary()

class _PhantomPlayer(Player):
  active = 0
  def __init__(self, name = None, host = "", port = 36079):
    Player.__init__(self, name, host, port)
    if name is None: self.name = self.question_name()
    self.my_info = (self.name, self.host, self.port)
    self.queue = None
    
  def set_level(self, level):
    Player.set_level(self, level)
    
    if level.active: self.listen_actions(self.character.round)
    else:            self.stop_listen_actions()
    
  def listen_actions(self, since_round = -1):
    if not self.queue:
      print "listen_actions -> connecting to", (self.host, self.port)
      
      s = self.question(QUESTION_LISTEN_ACTIONS)
      s.sendall(struct.pack("!i", since_round))
      self.queue = action.PhantomQueue(s, self)
      
  def stop_listen_actions(self):
    if self.queue:
      self.queue.socket.shutdown(2)
      self.queue.socket.close()
      self.queue = None
      
  def question_name(self):
    return self.question(QUESTION_NAME).makefile("r").read()
  
  def question_version(self):
    return self.question(QUESTION_VERSION).makefile("r").read()
  
  def question_address(self):
    return pickle.loads(self.question(QUESTION_ADDRESS).makefile("rb").read())
  
  def question_players(self):
    return pickle.loads(self.question(QUESTION_PLAYERS).makefile("rb").read())
  
  def question_addplayer(self, player_info):
    self.question(QUESTION_ADD_PLAYER).sendall(pickle.dumps(player_info, 2))
  
  def question_removeplayer(self, player_info):
    self.question(QUESTION_REMOVE_PLAYER).sendall(pickle.dumps(player_info, 2))
  
  def question_addcharacter(self, character, round_offset):
    self.question(QUESTION_ADD_CHARACTER).sendall(pickle.dumps((character, round_offset), 2))
    
  def question_removecharacter(self, character):
    self.question(QUESTION_REMOVE_CHARACTER).sendall(pickle.dumps(character, 2))
  
  def question_round(self):
    return int(self.question(QUESTION_ROUND).makefile("r").read())
  
  def question_actions(self, start_round, end_round):
    s = self.question(QUESTION_ACTIONS)
    s.sendall(struct.pack("!ii", start_round, end_round))
    
    #file = s.makefile("r", 0)
    #nb = struct.unpack("!i", file.read(4))[0]
    #return map(action.READ_ACTION, [file] * nb)
    
    nb = struct.unpack("!i", recvall(s, 4))[0]
    return map(action.READ_ACTION, [s] * nb)
  
  def question_getlevel(self, level_name):
    s = self.question(QUESTION_GET_LEVEL)
    s.sendall(pickle.dumps(level_name, 2))
    file = s.makefile("r", 0)
    if file.read(1) == "1": return pickle.load(file)
    return None
  
  def question_searchlevel(self, level_name):
    s = self.question(QUESTION_SEARCH_LEVEL)
    s.sendall(pickle.dumps(level_name, 2))
    
    return pickle.load(s.makefile("rb", 0))
  
  def question_listlevels(self):
    s = self.question(QUESTION_LIST_LEVELS)
    return pickle.load(s.makefile("rb", 0))
    
  def question_storelevels(self, levels):
    for lev in levels: lev.sent()
    s = self.question(QUESTION_STORE_LEVELS)
    s.sendall(pickle.dumps(levels, 2))
    
  def question_currentlevel(self):
    s = self.question(QUESTION_CURRENT_LEVEL)
    return pickle.load(s.makefile("rb", 0))
  
  def question(self, question):
    pass
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     print "2", self.host, self.port
#     s.connect((self.host, self.port))
#     print "3"
#     s.sendall(question)
#     return s



