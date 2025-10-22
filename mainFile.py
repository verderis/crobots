"""
CROBOTS-like minimal engine in Python — teaching version with live visualization and dynamic bot loading.

Run: python crobots_py_starter.py

Features:
- Simple 2D arena with pseudo-random scenarios (robot start positions + obstacles)
- Robot API for students: implement a class inheriting `RobotController` and override `step(sensors)`
- Sensors: own position/heading, radar (nearest target within range), hit status
- Actions: throttle (-1..1), turn (-pi..pi), fire() (single projectile)
- Weapons: simple projectile with speed, range, and collision
- Turn-based simulation loop (fixed dt)
- Visualization using matplotlib (positions, headings, projectiles)
- Dynamic bot loading from external Python modules for easy classroom use
"""

import importlib
import math
import random
import time
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict

# ---------- Constants ----------
ARENA_WIDTH = 800
ARENA_HEIGHT = 600
DT = 0.1
MAX_SPEED = 120.0
MAX_TURN_RATE = math.pi
PROJECTILE_SPEED = 300.0
PROJECTILE_RANGE = 500.0
RADAR_RANGE = 400.0
ROBOT_RADIUS = 12
PROJECTILE_RADIUS = 3
OBSTACLE_RADIUS = 20

def clamp(x,a,b): return max(a,min(b,x))
def angle_normalize(a): return (a+math.pi)%(2*math.pi)-math.pi
def dist(a,b): return math.hypot(a[0]-b[0],a[1]-b[1])

@dataclass
class SensorState:
    pos: Tuple[float,float]
    heading: float
    radar_distance: Optional[float]
    radar_bearing: Optional[float]
    hit: bool
    time: float

class RobotController:
    def __init__(self,name:str="robot"): self.name=name
    def init(self,info:Dict): self.info=info
    def step(self,sensors:SensorState)->Dict: return {'throttle':0.0,'turn':0.0,'fire':False}

class Projectile:
    def __init__(self,owner_id,x,y,heading,created_time):
        self.owner_id=owner_id; self.x=x; self.y=y; self.heading=heading
        self.vx=math.cos(heading)*PROJECTILE_SPEED; self.vy=math.sin(heading)*PROJECTILE_SPEED
        self.distance_travelled=0; self.created_time=created_time
    def step(self,dt):
        self.x+=self.vx*dt; self.y+=self.vy*dt; self.distance_travelled+=PROJECTILE_SPEED*dt

class Obstacle:
    def __init__(self,x,y,r=OBSTACLE_RADIUS): self.x=x; self.y=y; self.r=r

class RobotState:
    def __init__(self,controller,robot_id,x,y,heading):
        self.controller=controller; self.id=robot_id; self.x=x; self.y=y; self.heading=heading
        self.vx=self.vy=0; self.health=100; self.hit=False; self.last_fire_time=-1.0

class Arena:
    def __init__(self,width=ARENA_WIDTH,height=ARENA_HEIGHT,seed=None):
        self.width=width; self.height=height; self.seed=seed; random.seed(seed)
        self.robots=[]; self.projectiles=[]; self.obstacles=[]; self.time=0.0

    def add_robot(self,controller,x,y,heading):
        rid=len(self.robots); rc=RobotState(controller,rid,x,y,heading)
        self.robots.append(rc); controller.init({'arena_w':self.width,'arena_h':self.height,'robot_id':rid})
        return rc

    def spawn_random_scenario(self,n_robots=2,n_obstacles=6,margin=60,bot_modules:Optional[List[str]]=None):
        self.obstacles=[Obstacle(random.uniform(margin,self.width-margin),random.uniform(margin,self.height-margin)) for _ in range(n_obstacles)]
        self.robots=[]
        for i in range(n_robots):
            while True:
                x=random.uniform(margin,self.width-margin); y=random.uniform(margin,self.height-margin); heading=random.uniform(-math.pi,math.pi)
                if all(dist((x,y),(obs.x,obs.y))>(obs.r+ROBOT_RADIUS+10) for obs in self.obstacles): break
            controller=self._load_bot(bot_modules[i]) if bot_modules and i<len(bot_modules) else RandomBot(f"bot_{i}")
            self.add_robot(controller,x,y,heading)

    def _load_bot(self,module_name:str)->RobotController:
        mod=importlib.import_module(module_name)
        for attr in dir(mod):
            obj=getattr(mod,attr)
            if isinstance(obj,type) and issubclass(obj,RobotController) and obj is not RobotController:
                return obj(attr)
        raise ValueError(f"No RobotController subclass found in {module_name}")

    def _sense_for(self,robot):
        nearest_d=None; nearest_bearing=None
        for other in self.robots:
            if other.id==robot.id: continue
            d=dist((robot.x,robot.y),(other.x,other.y))
            if d<=RADAR_RANGE and (nearest_d is None or d<nearest_d):
                bearing=angle_normalize(math.atan2(other.y-robot.y,other.x-robot.x)-robot.heading)
                nearest_d,nearest_bearing=d,bearing
        return SensorState((robot.x,robot.y),robot.heading,nearest_d,nearest_bearing,robot.hit,self.time)

    def step(self,dt=DT):
        actions=[]
        for r in self.robots:
            sensors=self._sense_for(r)
            try: actions.append(r.controller.step(sensors))
            except: actions.append({'throttle':0,'turn':0,'fire':False})
        for r,a in zip(self.robots,actions):
            th=clamp(a.get('throttle',0),-1,1); turn=clamp(a.get('turn',0),-MAX_TURN_RATE*dt,MAX_TURN_RATE*dt)
            r.heading=angle_normalize(r.heading+turn)
            speed=th*MAX_SPEED; r.vx=math.cos(r.heading)*speed; r.vy=math.sin(r.heading)*speed
            r.x=clamp(r.x+r.vx*dt,0,self.width); r.y=clamp(r.y+r.vy*dt,0,self.height)
            if a.get('fire',False) and self.time-r.last_fire_time>0.3:
                self.projectiles.append(Projectile(r.id,r.x+math.cos(r.heading)*(ROBOT_RADIUS+2),r.y+math.sin(r.heading)*(ROBOT_RADIUS+2),r.heading,self.time)); r.last_fire_time=self.time
        for p in list(self.projectiles):
            p.step(dt)
            if p.x<0 or p.x>self.width or p.y<0 or p.y>self.height or p.distance_travelled>PROJECTILE_RANGE:
                self.projectiles.remove(p); continue
            for r in self.robots:
                if r.id!=p.owner_id and dist((p.x,p.y),(r.x,r.y))<(PROJECTILE_RADIUS+ROBOT_RADIUS):
                    r.health-=25; r.hit=True; self.projectiles.remove(p); break
        for r in self.robots:
            for obs in self.obstacles:
                d=dist((r.x,r.y),(obs.x,obs.y))
                if d<(ROBOT_RADIUS+obs.r):
                    dx=r.x-obs.x; dy=r.y-obs.y; nd=math.hypot(dx,dy) or 1e-3; overlap=(ROBOT_RADIUS+obs.r)-nd
                    r.x+=dx/nd*overlap; r.y+=dy/nd*overlap
        for r in self.robots: r.hit=False
        self.time+=dt

    def render(self,ax):
        ax.clear(); ax.set_xlim(0,self.width); ax.set_ylim(0,self.height)
        for obs in self.obstacles: ax.add_patch(plt.Circle((obs.x,obs.y),obs.r,color='gray',alpha=0.4))
        for r in self.robots:
            ax.add_patch(plt.Circle((r.x,r.y),ROBOT_RADIUS,color='blue' if r.health>0 else 'red',fill=True,alpha=0.5))
            ax.arrow(r.x,r.y,math.cos(r.heading)*15,math.sin(r.heading)*15,head_width=5,fc='k',ec='k')
        for p in self.projectiles:
            ax.add_patch(plt.Circle((p.x,p.y),PROJECTILE_RADIUS,color='orange'))
        ax.set_title(f"t={self.time:.1f}s")

class RandomBot(RobotController):
    def step(self,s):
        if random.random()<0.05: self._turn=random.uniform(-0.5,0.5)
        th=0.6; turn=getattr(self,'_turn',0)*DT; fire=s.radar_distance and s.radar_distance<200 and random.random()<0.25
        return {'throttle':th,'turn':turn,'fire':fire}

class SeekerBot(RobotController):
    def step(self,s):
        if s.radar_distance is None: return {'throttle':0.2,'turn':0.1*DT,'fire':False}
        turn=clamp(s.radar_bearing*3.0,-MAX_TURN_RATE*DT,MAX_TURN_RATE*DT)
        fire=s.radar_distance<220 and abs(s.radar_bearing)<0.3
        return {'throttle':0.8,'turn':turn,'fire':fire}

def run_demo(n_robots=3,seed=None,ticks=300,bot_modules:Optional[List[str]]=None):
    arena=Arena(seed=seed); arena.spawn_random_scenario(n_robots=n_robots,n_obstacles=6,bot_modules=bot_modules)
    fig,ax=plt.subplots(); plt.ion(); plt.show()
    for t in range(ticks):
        arena.step(DT); arena.render(ax); plt.pause(0.01)
        alive=[r for r in arena.robots if r.health>0]
        if len(alive)<=1: break
    plt.ioff(); plt.show()

if __name__=='__main__':
    print("Running CROBOTS Python demo (visual mode)...")
    run_demo(n_robots=3,seed=42)
    print("Done.")
