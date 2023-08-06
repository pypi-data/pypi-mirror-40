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

import sys, random, Tkinter
import py2play, py2play.level, py2play.player, py2play.action, py2play.character, py2play.idler

# Define the py2play.level.CREATE function.
# You MUST define this function, as the default implementation just raise an error.
# py2play.level.CREATE take a single argument, the level name (which is typically
# a string, but can be about anything. In this demo, we use an (X, Y) tuple ! :-)

def create_level(level_name):
  # Just create a new empty level.
  # In a real game, you would probably load the level from the corresponding file.
  
  return Level(*level_name)

# Replace the original py2play.level.CREATE by the new one.

py2play.level.CREATE = create_level

# Define our level class, by extending the base class provided by py2play.level.
# The level name is an (X, Y) tuple, where X and Y are the level's coordinate in
# the world. E.g. level (-1, 0) is at the left of level (0, 0) (which is the
# starting level).
# Each level is a 10 * 10 map.

class Level(py2play.level.Level):
  def __init__(self, X, Y):
    
    # Call the super constructor. Do not forget that !
    
    py2play.level.Level.__init__(self, (X, Y))
    
    # X and Y are the level coordinates in the world.
    # data is the 10 * 10 map (0 for nothing, 1 for a block), stored in a single list.
    # changed is set to 1 when the level is changed (= when a block is added).
    
    self.X, self.Y = X, Y
    self.data = [0] * 100
    self.changed = 0
    
  def __repr__(self):
    s = "level %s : \n" % (self.name,)
    for x in xrange(10):
      for y in xrange(10):
        s = s + str(self.data[10 * x + y]) + " "
      s = s + "\n"
    s = s + "characters :\n"
    for character in self.characters: s = s + "  " + `character` + "\n"
    return s
  
#class ActivePlayer(py2play.player.ActivePlayer):
#  def __init__(self, level, name, host = None, action_port = 36079, question_port = 36080):
#    py2play.player.ActivePlayer.__init__(self, level, name, host, action_port, question_port)

# In this simple demo, we don't redefine the Players class, though it
# may be done.

ActivePlayer = py2play.player.ActivePlayer


# We don't redefine the Action class too, and use the default one.
# Each action is identified by a one-character string.

Action = py2play.action.Action

# Define the constant for the different action.
# The WAIT action means doing nothing.
# The MOVE_* action means moving one case in the given direction.
# The CREATE_BLOCK action means create a block under the character.
# Py2Play only defines ACTION_WAIT, and we keep the value provided for this action.

ACTION_WAIT         = py2play.action.ACTION_WAIT
ACTION_STALLED      = py2play.action.ACTION_STALLED
ACTION_MOVE_UP      = "u"
ACTION_MOVE_DOWN    = "d"
ACTION_MOVE_LEFT    = "l"
ACTION_MOVE_RIGHT   = "r"
ACTION_CREATE_BLOCK = "c"

# Redefine the Character class.

class Character:
  def __init__(self, x, y, char):
    
    # drawx and drawy are the current position of the character, in pixel.
    # char is the letter displayed for this character -- the initial of the name.
    # moving is 1 is the character is currently moving.
    
    self.x, self.y = x, y
    self.drawx, self.drawy = self.x * 20, self.y * 20
    self.char = char
    self.moving = 0
    
  # The plan_* method are called when the character plan to do some action. The
  # action is not immediately done.
  # These methods just create the corresponding action, and then call plan_action.
  # The event param is due to the Tkinter callback system.
  
  def plan_move_up     (self, event = None): self.plan_action(Action(ACTION_MOVE_UP))
  def plan_move_down   (self, event = None): self.plan_action(Action(ACTION_MOVE_DOWN))
  def plan_move_left   (self, event = None): self.plan_action(Action(ACTION_MOVE_LEFT))
  def plan_move_right  (self, event = None): self.plan_action(Action(ACTION_MOVE_RIGHT))
  def plan_create_block(self, event = None): self.plan_action(Action(ACTION_CREATE_BLOCK))
  
  # Debugging hack !
  def plan_hack(self, event = None):
    self.plan_action(Action(ACTION_MOVE_LEFT))
    self.plan_action(Action(ACTION_MOVE_RIGHT))
  
  # begin_action is called when the character really start doing the action.
  # begin_action prepares the action. Actions that are non punctual in the time, and
  # that can be sub-divided, such as movement, should be performed in advance_time.
  # Other must be performed directly by begin_action.
  
  def begin_action(self, action):
    
    # The precedent move is ended.
    
    self.moving = 0
    
    # Delegate to the corresponding method.
    
    if   action.action == ACTION_MOVE_UP     : self.move(self.x    , self.y - 1)
    elif action.action == ACTION_MOVE_DOWN   : self.move(self.x    , self.y + 1)
    elif action.action == ACTION_MOVE_LEFT   : self.move(self.x - 1, self.y    )
    elif action.action == ACTION_MOVE_RIGHT  : self.move(self.x + 1, self.y    )
    elif action.action == ACTION_CREATE_BLOCK: self.create_block()
    
  def move(self, x, y):
    
    # next_level is the level the character is going to. Defaults to the current
    # level
    
    next_level = self.level
    
    # Check if the character is going out of the current level, and if so,
    # set next_level to the level he is going to.
    # py2play.level.get returns the level of the given name (here, the (X, Y) tuple).
    
    if x < 0:
      x = x + 10
      next_level = py2play.level.get((self.level.X - 1, self.level.Y    ))
    if x > 9:
      x = x - 10
      next_level = py2play.level.get((self.level.X + 1, self.level.Y    ))
    if y < 0:
      y = y + 10
      next_level = py2play.level.get((self.level.X    , self.level.Y - 1))
    if y > 9:
      y = y - 10
      next_level = py2play.level.get((self.level.X    , self.level.Y + 1))
      
    # Cancel the movement if the new position (in the new level) is not free (=no block).
    
    if next_level.data[x + 10 * y] > 0: return
    
    # We are moving, so moving is set to 1
    # Change the x and y position (but not the drawx and drawy which are the graphic
    # coordinates, and which will be updated by advance_time)
    
    self.moving = 1
    self.x, self.y = x, y
    
    # If the new level is not the current one, change the character's current level
    # by calling set_level.
    
    if not next_level is self.level:
      self.set_level(next_level)
    
  def create_block(self):
    
    # Create the block by changing the level's data,
    # and set the level's changed flag to 1, so as it will be redrawn.
    
    self.level.data[self.x + 10 * self.y] = 1
    self.level.changed = 1
    
  def advance_time(self, proportion):
    
    # Advance the current action, if it is "time-dividable". proportion is the
    # proportion of the action that is achieved (from 0.0 to 1.0; 0.0 means that
    # nothing has been done, and 1.0 the action has been fully done. E.g. 0.5 means
    # that half of the action is done (cumulatively), and the next advance_time
    # may be 0.5 too, and will finish the action).
    
    # If the character is moving,
    
    if self.moving:
      
      # self.current_action is the current action.
      # According to the movement direction, update drawx or drawy by + or -
      # proportion * 20.0 (20.0 is the dimension of one block in the level).
      # Then check if the character is out of the screen and, if so, move it
      # on the other edge (the level change has been done in begin_action).
      
      if   self.current_action.action == ACTION_MOVE_UP:
        self.drawy = self.drawy - proportion * 20.0
        if self.drawy < -10.0: self.drawy = self.drawy + 200.0
        
      elif self.current_action.action == ACTION_MOVE_DOWN:
        self.drawy = self.drawy + proportion * 20.0
        if self.drawy > 190.0: self.drawy = self.drawy - 200.0
        
      elif self.current_action.action == ACTION_MOVE_LEFT:
        self.drawx = self.drawx - proportion * 20.0
        if self.drawx < -10.0: self.drawx = self.drawx + 200.0
        
      elif self.current_action.action == ACTION_MOVE_RIGHT:
        self.drawx = self.drawx + proportion * 20.0
        if self.drawx > 190.0: self.drawx = self.drawx - 200.0


class PlayerCharacter(Character, py2play.character.PlayerCharacter):
  def __init__(self, player, x = None, y = None):
    
    # Call the super constructor. Do not forget that !
    
    py2play.character.PlayerCharacter.__init__(self, player)
    
    # Define the x and y coordinates of the character.
    # For a new game, the coordinates must be passed to the constructor.
    # For joining an existant game, the coordinates are the ones of the parrain.
    
    if x is None:
      # Get the position of the parrain.
      for charac in player.level.characters:
        if charac.player.my_info == self.player.parrain_info:
          Character.__init__(self, charac.x, charac.y, player.name[:1])
          break
    else: Character.__init__(self, x, y, player.name[:1])
    
    
class Monster(Character, py2play.character.NonPlayerCharacter):
  def __init__(self, x = None, y = None):
    
    # Call the super constructor. Do not forget that !
    
    py2play.character.NonPlayerCharacter.__init__(self)
    
    Character.__init__(self, x, y, "#")
    
    self.current_action = Action(ACTION_WAIT)
    self.random = random.Random()
    
    self.state = 20
    
  def begin_action(self, action):
    #h = self.random.random()
    
    #if   h < 0.1: self.current_action = Action(ACTION_MOVE_UP)
    #elif h < 0.2: self.current_action = Action(ACTION_MOVE_DOWN)
    #elif h < 0.3: self.current_action = Action(ACTION_MOVE_LEFT)
    #elif h < 0.4: self.current_action = Action(ACTION_MOVE_RIGHT)
    #else:         self.current_action = Action(ACTION_WAIT)
    
    #self.current_action = Action(ACTION_WAIT)
    #return
    
    if self.state % 4 == 0:
      if self.state < 40: self.current_action = Action(ACTION_MOVE_LEFT)
      else:               self.current_action = Action(ACTION_MOVE_RIGHT)
    else:                 self.current_action = Action(ACTION_WAIT)
    
    if self.state < 79: self.state = self.state + 1
    else:               self.state = 0
    
    Character.begin_action(self, self.current_action)
    
    
# Redefine the Idler class (and name it Game).

class Game(Tkinter.Toplevel, py2play.idler.Idler):
  def __init__(self, character):
    
    # Call the super constructor. Do not forget that !
    
    py2play.idler.Idler.__init__(self)
    
    # Initialize a Tk Toplevel window.
    
    tkroot = Tkinter.Tk(className = 'py2play_demo')
    tkroot.withdraw()
    Tkinter.Toplevel.__init__(self, tkroot)
    
    # Create a Tk canvas.
    
    self.canvas = Tkinter.Canvas(self, bg = "white")
    self.canvas.place(x = 0, y = 0, width = 200, height = 200)
    
    # character is the active character.
    # character_tags is a dictionary that maps each character to the canvas tag that represent it.
    # level_tags is a list of all tags used to draw the current level.
    
    self.character      = character
    self.character_tags = {}
    self.level          = None
    self.level_tags     = []
    
    # Set the current visible level to the main character's level.
    
    self.set_level(character.level)
    
    # Bind the different key to the corresponding plan_* method of the active character.
    
    self.bind("<Key-Up>"   , character.plan_move_up)
    self.bind("<Key-Down>" , character.plan_move_down)
    self.bind("<Key-Left>" , character.plan_move_left)
    self.bind("<Key-Right>", character.plan_move_right)
    self.bind("<Key- >"    , character.plan_create_block)
    
    self.bind("<Key-h>"    , character.plan_hack)
    
    # When the window is closed, end the game.
    
    self.bind("<Destroy>"  , self.end_game)
    
  def end_game(self, event = None):
    if self.state: # Avoid calling end_game() twice or more.
      
      # Stop idleing, end the game and exit.
      
      self.stop()
      self.character.player.end_game()
      sys.exit()
      
  def begin_round(self):
    py2play.idler.Idler.begin_round(self)
    
    # Play each character.
    # XXX self.level.characters is cloned ("[:]") because
    # begin_round may add or remove some characters !!!
    
    for charac in self.level.characters[:]: charac.begin_round()
    
    # If the main character's level has changed, update the game's current level.
    
    if not self.character.level is self.level: self.set_level(self.character.level)
    
  def advance_time(self, proportion):
    
    # Advance each character.
    
    for charac in self.level.characters: charac.advance_time(proportion)
    
    # Draw the character.
    # Draw the level if it has changed.
    # The try is to skip any Tcl/Tk error that occurs when the window is closed.
    
    try:
      self.draw_characters()
      if self.level.changed: self.draw_level()
    except Tkinter.TclError:
      pass
    
  def set_level(self, level):
    
    # Set the current level displayed in the game window
    
    # Hide the previous level, if there is one
    
    if not self.level is None: self.level.set_active(0)
    
    # Show the new level
    
    level.set_active(1)
    
    # Store the new level, and draw it.
    
    self.level = level
    self.draw_level()
    
  def draw_level(self):
    
    # Draw the current level
    
    # Delete all the previous level's tags,
    # Draw the new ones,
    # Unset the level's changed flag.
    
    self.canvas.delete(*self.level_tags)
    self.level_tags = [self.canvas.create_rectangle(x * 20, y * 20, (x + 1) * 20, (y + 1) * 20)
                       for x in xrange(10)
                       for y in xrange(10)
                       if self.level.data[x + 10 * y] > 0
                       ]
    self.level.changed = 0
    
  def draw_characters(self):
    
    # Draw the characters in the current level.
    # Character are displayed as a single letter.
    
    # Remove tags of characters that has gone away, and that are no longer in the
    # current level.
    
    for character in self.character_tags.keys():
      if not character in self.level.characters:
        self.canvas.delete(self.character_tags[character])
        del self.character_tags[character]
        
    # Add a tag for new characters,
    # or move the already existant one for other.
    
    for character in self.level.characters:
      tag = self.character_tags.get(character)
      if not tag:
        self.character_tags[character] = self.canvas.create_text(character.drawx + 10, character.drawy + 10, text = character.char)
      else:
        self.canvas.coords(tag, character.drawx + 10, character.drawy + 10)
        
