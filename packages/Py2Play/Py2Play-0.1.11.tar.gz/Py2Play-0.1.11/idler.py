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

import time, thread

ROUND_DURATION     = 0.030
MIN_FRAME_DURATION = 0.020
SPEED              = 1.0

IDLER = None

STOPPED = 0
PLAYING = 1

class Idler:
  def __init__(self):
    self.next_round_tasks = []
    self.fps   = 0.0
    self.state = STOPPED
    
    global IDLER
    IDLER = self
    
    print "* Py2Play * IDLER created !"
    
  def start(self): thread.start_new_thread(self.idle, ())
  def stop (self,*args):
    self.state = STOPPED
    self.return_values = args
  
  def idle(self, state = PLAYING):
    self.state = state
    self.time = last_fps_computation_time = time.time()
    self.time_since_last_round = 0.0
    
    #thread.start_new_thread(self._staller, ())

    self.begin_round()
    
    
#     import profile
#     self.advance_time(1.0)
#     self.end_round()
    
#     for i in range(100):
#       self.begin_round()
#       self.advance_time(1.0)
#       self.end_round()
#       self.render()
      
#     profile.Profile.bias = 1.0e-05
#     profile.run("""
# from py2play.idler import IDLER
# for i in range(10):
#     IDLER.begin_round()
#     IDLER.advance_time(1.0)
#     IDLER.end_round()
#     IDLER.render()
# """)

    
    
    while self.state >= PLAYING:
      nb_frame = 0
      while (self.state >= PLAYING) and (nb_frame < 80):
        nb_frame = nb_frame + 1
        
        while 1: # Sleep until at least MIN_FRAME_DURATION second has passed since the last frame
          current = time.time()
          delta = (current - self.time) * SPEED
          
          if delta > MIN_FRAME_DURATION * SPEED: break
          time.sleep(MIN_FRAME_DURATION * SPEED - delta)
          
        self.time = current
        
        while self.time_since_last_round + delta > ROUND_DURATION: # Start a new frame
          spent_time = ROUND_DURATION - self.time_since_last_round
          
          self.advance_time(spent_time / ROUND_DURATION) # Complete the previous round
          self.end_round()                               # Ends the previous round
          
          self.begin_round()                             # Prepare the following round
          
          #if self.next_round_tasks:
          #  for task in self.next_round_tasks: task()
          #  self.next_round_tasks = []
          
          while self.next_round_tasks:
            task = self.next_round_tasks.pop()
            task()
            
          delta = delta - spent_time
          self.time_since_last_round = 0
          
        self.advance_time(delta / ROUND_DURATION) # start the current round
        self.time_since_last_round = self.time_since_last_round + delta
        
        self.render()
        
      current = time.time()
      self.fps = nb_frame / (current - last_fps_computation_time)
      last_fps_computation_time = current
      
    import py2play.player as player, py2play.level as level
    player.CURRENT_PLAYER.end_game()
    level.clear()
    
    return self.return_values
  
  def begin_round (self): pass
  def end_round   (self): pass
  def advance_time(self, proportion): pass
  def render      (self): pass
  
  def accel(self, nb_round):
    print "accel", nb_round
    self.time -= nb_round * ROUND_DURATION
    
  def end_game(self, *args):
    self.stop(*args)
    
  def _staller(self):
    import py2play.player as player, py2play.action as action
    
    queue = player.CURRENT_PLAYER.queue
    
    while self.state >= PLAYING:
      last_action = queue.actions[-1]
      time.sleep(ROUND_DURATION * 2.0)
      
      if queue.actions[-1] is last_action:
       while (self.state >= PLAYING) and (queue.actions[-1] is last_action): # Stalled !!!
        
        if last_action.action != action.ACTION_STALLED: print "stalled..."
        
        last_action = action.Action(action.ACTION_STALLED)
        queue.append(last_action)
        
        time.sleep(ROUND_DURATION)
        
       print "ok !"
    
