import sys
import math
import random
# Grab Snaffles and try to throw them through the opponent's goal!
# Move towards a Snaffle and use your team id to determine where you need to throw it.
RISK_DIST=5000
RISK_BLUDG_DIST=800
my_team_id = int(input())  # if 0 you need to score on the right of the map, if 1 you need to score on the left
GOAL_CENTER=(16000,3750) if my_team_id!=0 else (0,3750)
OTHER_GOAL=(0,3750) if my_team_id!=0 else (16000,3750)
GOAL_UP=(16000,1750) if my_team_id!=0 else (0,1750)
GOAL_DOWN=(16000,5750) if my_team_id!=0 else (0,5750)
players={}
bludgers={}
snaffles={}
Action_list={}

SPELLS=["PETRIFICUS", "ACCIO", "FLIPENDO", "OBLIVIATE"]
magic=0

#def if_last_and_free

def get_ray_direction(wiz, snaf):
    angle=math.acos(abs(wiz.location[1]-GOAL_UP[1])/get_distance(wiz.location, GOAL_UP))
    angle_snaf=math.acos(abs(wiz.location[1]-snaf.location[1])/get_distance(wiz.location, snaf.location))
    if angle_snaf>angle: return False
    print(wiz.ID, magic, snaf.ID, angle, angle_snaf,file=sys.stderr)
    return True

def get_distance(a,b):
    return math.hypot(abs(a[0]-b[0]),abs(a[1]-b[1]))

def check_snaffle_risk(wiz):

    for i in snaffles:
        if get_distance(GOAL_CENTER, snaffles[i].location)>RISK_DIST: continue
        if not snaffles[i].is_taken and magic>20:
            return get_nearest_appropriate_entity(GOAL_CENTER, "ACCIO", "SNAFFLE", 100000)
        if not snaffles[i].is_taken and magic>10:
            return get_nearest_appropriate_entity(GOAL_CENTER, "PETRIFICUS", "SNAFFLE", 100000)
    return ""

def check_bludg_so_close(wiz):
    for b in bludgers:
        if magic>5:
            if get_distance(bludgers[b].location, wiz.location)<RISK_BLUDG_DIST:
                return "OBLIVIATE "+str(bludgers[b].ID)
    return ""

def Petrify_wiz(wiz):
    if magic<10: return ""
    location=wiz.location
    dist=100000
    targ_id=-1
    for i in players:
        if players[i].is_friend(): continue
        speed=math.sqrt(players[i].location[0]**2+players[i].location[1]**2)
        if speed<100: continue
        if dist>get_distance(players[i].location, location):
            dist=get_distance(players[i].location, location)
            targ_id=players[i].ID
    if targ_id!=-1: return "PETRIFICUS "+str(targ_id)
    return ""

class Bludger:
    def __init__(self, blug_id, location, speed):
        self.ID=blug_id
        self.location=location
        self.speed=speed

    def __str__(self):
        return "ID: "+str(self.ID)+"\n"+\
        "location: "+str(self.location)+"\n"+\
        "velocity: "+str(self.speed)+"\n"
    def __repr__(self):
        return self.__str__()
        

def get_nearest_appropriate_entity(location, spel, entity_type, min_dist):
    global snaffles, bludgers, players
    dist=100000
    targ_id=-1
    playr=False
    lst=[]
    if entity_type=="BLUDGER": lst=bludgers
    elif entity_type=="OPPONENT_WIZARD": 
        lst=players
        playr=True
    elif entity_type=="SNAFFLE": lst=snaffles
    for i in lst:
        if playr and lst[i].is_friend(): continue
        if dist>get_distance(lst[i].location, location):
            dist=get_distance(lst[i].location, location)
            targ_id=lst[i].ID
    if dist>min_dist: return ""
    print(str(magic),file=sys.stderr)
    return spel+" "+str(targ_id)+" "+str(magic)

def chk_in_action_list(action):
    for i in Action_list:
        if Action_list[i]==action:
            return ""
    return action

class Wizard:
    def __init__(self, wiz_id, location, has_snaffle, velocity, friend_or_foe):
        self.ID=wiz_id
        self.location=location
        self.has_snaffle=has_snaffle
        self.velocity=velocity
        self.friend_or_foe=friend_or_foe
        #self.magic=magic
    
    def __str__(self):
        return "ID: "+str(self.ID)+"\n"
        #"magic: "+str(self.magic)+"\n"
        #"location: "+str(self.location)+"\n"+\
        #"has_snaffle: "+str(self.has_snaffle)+"\n"+\
        #"velocity: "+str(self.velocity)+"\n"+"\n"+\
        
    
    def is_friend(self):
        return self.friend_or_foe
    
    def move_to_nearest_snaffle(self, snaffle_list):
        global bludgers, players, magic
        if self.has_snaffle:
            return self.throw_snaff()
        min_dist=100000
        targ=(-1,-1)
        for i in snaffle_list:
            if snaffle_list[i].is_taken: continue
            if min_dist>get_distance(snaffle_list[i].location, self.location):
                min_dist=get_distance(snaffle_list[i].location, self.location)
                targ=snaffle_list[i]
        res=""
        if magic>20:
            res=check_snaffle_risk(self)
            res=chk_in_action_list(res)
            #if res=="":res=Petrify_wiz(self)
            #res=chk_in_action_list(res)
            #    res=check_bludg_so_close(self)
            #spel=random.choice(SPELLS)
            #res=""
            #if spel=="OBLIVIATE":targ_type="BLUDGER"
            #if spel=="PETRIFICUS" or spel=="FLIPENDO":targ_type=random.choice(["BLUDGER", "OPPONENT_WIZARD"])            
            #if spel=="ACCIO":targ_type="SNAFFLE"
            #res=get_nearest_appropriate_entity(self, spel, targ_type, min_dist)
            if res!="":
                return res
        if targ!=(-1,-1):
            targ.is_taken=True
            if magic>20 and get_distance(OTHER_GOAL, targ.location):
                if (OTHER_GOAL==(0,3750) and self.location[0]>targ.location[0]) \
                or (OTHER_GOAL!=(0,3750) and self.location[0]<targ.location[0]):
                    #if get_ray_direction(self,targ):
                    #magic-=20
                    return "FLIPENDO "+str(targ.ID)
            return "MOVE "+str(targ.location[0])+" "+str(targ.location[1])+" 150"        
        if get_distance(self.location, GOAL_CENTER)<1000:
            for i in snaffle_list:
                if get_distance(self.location, snaffle_list[i].location)<3000:
                    return "FLIPENDO "+str(snaffle_list[i].ID)
        if res=="":res=Petrify_wiz(self)
        res=chk_in_action_list(res)
        if res!="":
            return res

        return "MOVE "+str(GOAL_CENTER[0])+" "+str(GOAL_CENTER[1])+" 150"
        
    def throw_snaff(self):
        if my_team_id==0:            
            return "THROW 16000 3750 500"
        else:
            return "THROW 0 3750 500"
    
    def __repr__(self):
        return self.__str__()
    
class Snaffle:
    def __init__(self, snaf_id, location, is_taken):
        self.ID=snaf_id
        self.location=location
        self.is_taken=is_taken

    def check_if_taken(self, player_list):
        for i in player_list:
            if player_list[i].has_snaffle:
                if player_list[i].location==self.location:
                    return True
        return False
        
    def __str__(self):
        return "ID: "+str(self.ID)+"\n"+\
        "location: "+str(self.location)+"\n"+\
        "is_taken: "+str(self.is_taken)+"\n"
    
    def __repr__(self):
        return self.__str__()

def update_snaffles():
    for i in snaffles:
        snaffles[i].is_taken=snaffles[i].check_if_taken(players)



def update_world(entity_id, entity_type, x, y, vx, vy, state):
    #global magic
    
    if entity_type=="WIZARD":
        if entity_id in players:
            players[entity_id]=Wizard(entity_id,(x,y),state==1,(vx,vy),True)
        else:    
            players[entity_id]=Wizard(entity_id,(x,y),state==1,(vx,vy),True)
    elif entity_type=="OPPONENT_WIZARD":
        players[entity_id]=Wizard(entity_id,(x,y),state==1,(vx,vy),False)
    elif entity_type=="SNAFFLE":
        snaffles[entity_id]=Snaffle(entity_id,(x,y),False)
    elif entity_type=="BLUDGER":
        bludgers[entity_id]=Bludger(entity_id,(x,y),(vx,vy))

# game loop
while True:    
    snaffles={}
    bludgers={}
    Action_list={}
    magic+=1
    if magic>100: magic=100
    entities = int(input())  # number of entities still in game
    for i in range(entities):
        # entity_id: entity identifier
        # entity_type: "WIZARD", "OPPONENT_WIZARD" or "SNAFFLE" (or "BLUDGER" after first league)
        # x: position
        # y: position
        # vx: velocity
        # vy: velocity
        # state: 1 if the wizard is holding a Snaffle, 0 otherwise
        entity_id, entity_type, x, y, vx, vy, state = input().split()
        entity_id = int(entity_id)
        x = int(x)
        y = int(y)
        vx = int(vx)
        vy = int(vy)
        state = int(state)
        
        update_world(entity_id, entity_type, x, y, vx, vy, state)
    
    update_snaffles()
    #print(players, file=sys.stderr)
    #print(snaffles, file=sys.stderr)
    print(magic,file=sys.stderr)
    for i in players:
        if players[i].is_friend():
            Action_list[i]=players[i].move_to_nearest_snaffle(snaffles)
            if Action_list[i].startswith("OBLIVIATE"): 
                magic-=5
                Action_list[i]+=" OBLIVIATE"
            elif Action_list[i].startswith("PETRIFICUS"): 
                magic-=10
                Action_list[i]+=" PETRIFICUS"
            elif Action_list[i].startswith("ACCIO"): 
                magic-=20
                Action_list[i]+=" ACCIO"
            elif Action_list[i].startswith("FLIPENDO"): 
                magic-=20
                Action_list[i]+=" FLIPENDO"
            print(Action_list[i])
        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr)


        # Edit this line to indicate the action for each wizard (0 <= thrust <= 150, 0 <= power <= 500)
        # i.e.: "MOVE x y thrust" or "THROW x y power"
        #print("MOVE 8000 3750 100")
