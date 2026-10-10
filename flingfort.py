#!/usr/bin/env python3
"""Flingfort: original fullscreen terminal slingshot game. Standard library only."""
import curses,math,time,random
from dataclasses import dataclass
VERSION='1.0.0'
@dataclass
class Block:
 x:float
 y:float
 hp:int=2
 target:bool=False
@dataclass
class Shot:
 x:float
 y:float
 vx:float
 vy:float

def launch(angle,power):
 a=math.radians(angle);speed=power/3
 return Shot(7,3,math.cos(a)*speed,math.sin(a)*speed)

def advance(shot,blocks,dt=.06):
 shot.x+=shot.vx*dt;shot.y+=shot.vy*dt;shot.vy-=10*dt
 for b in blocks:
  if b.hp>0 and abs(shot.x-b.x)<1.6 and abs(shot.y-b.y)<1.6:
   b.hp-=1 if b.target else 2
   shot.vx*=.5;shot.vy*=.5
   return 'hit'
 if shot.y<1 or shot.x>96:return 'end'
 return 'flying'

def settle(blocks):
 # Unsupported blocks fall one grid step; landing damage knocks out low targets.
 for b in sorted(blocks,key=lambda b:b.y):
  if b.hp<=0 or b.y<=2:continue
  if not any(o.hp>0 and o is not b and abs(o.x-b.x)<2 and abs(o.y-(b.y-2))<1 for o in blocks):
   b.y=max(2,b.y-2)
   for o in blocks:
    if o.target and o.hp>0 and o is not b and abs(o.x-b.x)<2 and abs(o.y-b.y)<1:o.hp=0

def level(n):
 r=random.Random(n);blocks=[]
 for tower in range(2+min(n//3,2)):
  x=48+tower*11
  height=2+n%3
  for row in range(height):blocks.append(Block(x,2+row*2))
  blocks.append(Block(x,2+height*2,1,True))
 blocks.append(Block(65+r.randrange(6),2,1,True))
 return blocks

def play(screen):
 curses.curs_set(0);screen.nodelay(True);screen.keypad(True)
 if curses.has_colors():
  curses.start_color();curses.use_default_colors()
  for i,c in enumerate([curses.COLOR_CYAN,curses.COLOR_YELLOW,curses.COLOR_GREEN,curses.COLOR_RED,curses.COLOR_BLUE],1):curses.init_pair(i,c,-1)
 def put(y,x,text,c=0):
  h,w=screen.getmaxyx()
  if 0<=y<h and 0<=x<w-1:
   try:screen.addnstr(y,x,text,w-x-1,curses.color_pair(c))
   except curses.error:pass
 n=1;blocks=level(n);angle=38;power=55;shots=7;shot=None;trail=[];message='Knock out the green targets. Towers collapse when their supports break.';last=time.monotonic();paused=False
 while True:
  now=time.monotonic();dt=min(now-last,.09);last=now
  h,w=screen.getmaxyx()
  key=screen.getch()
  screen.erase()
  if key in (ord('q'),ord('Q')):return
  if h<22 or w<70:
   put(0,0,'Flingfort needs a terminal at least 70 columns x 22 rows.',1);put(2,0,'Resize your terminal, or press q to quit.');screen.refresh();time.sleep(.04);continue
  if key in (ord('r'),ord('R')):blocks=level(n);shots=7;shot=None;trail=[];message='Level restarted.'
  if key in (ord('p'),ord('P')):paused=not paused
  alive=any(b.target and b.hp>0 for b in blocks)
  if key in (ord('n'),ord('N')) and not alive:n+=1;blocks=level(n);shots=7;shot=None;trail=[];message='New fort!'
  if not shot and alive and not paused:
   if key in (curses.KEY_LEFT,ord('a')):angle=max(5,angle-2)
   if key in (curses.KEY_RIGHT,ord('d')):angle=min(85,angle+2)
   if key in (curses.KEY_UP,ord('w')):power=min(100,power+2)
   if key in (curses.KEY_DOWN,ord('s')):power=max(20,power-2)
   if key==ord(' ') and shots>0:shot=launch(angle,power);shots-=1;trail=[];message='Flying!'
  if shot and not paused:
   outcome=advance(shot,blocks,dt);trail.append((shot.x,shot.y));trail=trail[-100:]
   if outcome=='hit':message='Impact!';settle(blocks)
   if outcome=='end':shot=None;settle(blocks)
  if not any(b.target and b.hp>0 for b in blocks):message='FORT CLEARED! Press n for the next level.'
  elif shots==0 and not shot:message='Out of shots. Press r to try again.'
  floor=h-5;sx=(w-4)/100;sy=(h-9)/22
  def draw(x,y,text,color):put(floor-int(y*sy),2+int(x*sx),text,color)
  put(0,2,'FLINGFORT  |  LEVEL '+str(n)+'  |  SHOTS '+str(shots)+'  |  '+('PAUSED' if paused else 'Original terminal physics game'),1)
  put(2,2,f'ANGLE {angle:2d} deg   POWER {power:3d}%    '+message,2)
  for x,y in trail:draw(x,y,'.',5)
  if not shot and shots>0:
   preview=launch(angle,power)
   for i in range(10):
    preview.x+=preview.vx*.10;preview.y+=preview.vy*.10;preview.vy-=1
    if preview.y>0:draw(preview.x,preview.y,'.',1)
  draw(7,2,'Y',2)
  for b in blocks:
   if b.hp>0:draw(b.x,b.y,'@@' if b.target else '##',3 if b.target else 2)
  if shot:draw(shot.x,shot.y,'OO',4)
  put(floor,1,'='*(w-3),3)
  put(h-3,2,'A/D or Left/Right: angle   W/S or Up/Down: power   Space: fire',1)
  put(h-2,2,'R: restart   N: next cleared fort   P: pause   Q: quit',1)
  screen.refresh();time.sleep(.025)

def main():
 try:curses.wrapper(play)
 except KeyboardInterrupt:pass
 except curses.error as exc:print('Use an interactive terminal with TERM set (for example xterm-256color):',exc);return 1
 return 0
if __name__=='__main__':raise SystemExit(main())
