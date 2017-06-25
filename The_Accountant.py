import sys
import math

MIN_X=0
MIN_Y=0
MAX_X=16000
MAX_Y=9000
ME_MOVE_STEP=1000
ME_ESCAPE_STEP=1500
ENEMY_MOVE_STEP=500
DANGER_ZONE=3900
DATA_POINT_VALUE=100
MIN_DISTANCE=1200

def calculate_damage(distance):
    return round(125000/(distance**1.2))

def get_distance(a,b):
    return round(math.hypot(abs(a[0]-b[0]),abs(a[1]-b[1])))

def get_point_from_hypot(hyp, source, destination):
    calc_hyp=get_distance(source, destination)
    cos=abs(source[0]-destination[0])/calc_hyp
    sin=abs(source[1]-destination[1])/calc_hyp
    return (int(hyp*cos), int(hyp*sin))

class GameObject():
    def __init__(self, mpos):
        self.pos=mpos
    
    def is_up(self, Pos):
        if self.pos[1]<Pos[1]:
            return True
    def is_down(self, Pos):
        if self.pos[1]>Pos[1]:
            return True
    def is_right(self, Pos):
        if self.pos[0]>Pos[0]:
            return True
    def is_left(self, Pos):
        if self.pos[0]<Pos[0]:
            return True
    
    def __str__(self):
        return self.__class__.__name__+"\n  Pos: "+str(self.pos)

class Data_Point(GameObject):
    def __init__(self, mpos, mId):
        super().__init__(mpos)
        self.Id=mId
    
    def __str__(self):
        return super().__str__()+"\n  ID: "+str(self.Id)

class enemy(GameObject):
    
    def __init__(self, mpos, mId, Life):
        super().__init__(mpos)
        self.Id=mId
        self.life=Life
        self.old_pos=(0,0)
    
    def set_pos(self,mpos):
        self.old_pos=self.pos
        self.pos=mpos
    
    def isMovingAway(self,mpos):
        if get_distance(self.old_pos,mpos) < get_distance(self.pos,mpos) or self.old_pos==(0,0):
            return True
        return False
    
    def __str__(self):
        return super().__str__()+"\n  ID: "+str(self.Id)\
        +"\n  life: "+str(self.life)\
        +"\n  old_pos: "+str(self.old_pos)

class wolff(GameObject):
    def __init__(self, mpos):
        super().__init__(mpos)
        self.destination=mpos
    
    def set_destination(self, mPos):
        x=mPos[0]
        y=mPos[1]
        if mPos[0]<=MIN_X:
            x=MIN_X
        elif mPos[0]>=MAX_X:
            x=MAX_X
        if mPos[1]<=MIN_Y:
            y=MIN_Y
        elif mPos[1]>=MAX_Y:
            y=MAX_Y
        self.destination=(x,y)
    
    def move(self):
        return "MOVE "+str(self.destination[0])+" "+str(self.destination[1])

    def shoot(self, enemy_id):
        return "SHOOT "+str(enemy_id)
    
    def __str__(self):
        return super().__str__()+"\n  destination: "+str(self.destination)

def go_to_nearest_enemy():
    distance=MAX_X
    me_min_distance=MAX_X
    target=None
    me_target=None
    global Wolff
    for enmy in enemies:
        for data_point in dataPoints:
            new_dist=get_distance(data_point.pos, enmy.pos)
            if new_dist<distance:
                distance=new_dist
                target=enmy
                
        me_distance=get_distance(Wolff.pos, enmy.pos)
        #print("me_distance "+str(me_distance),file=sys.stderr)
        if me_distance<=me_min_distance:
            me_min_distance=me_distance
            me_target=enmy
        
    if me_min_distance<=DANGER_ZONE:
        #print("Wolff "+str(Wolff),file=sys.stderr)
        #print("me_target "+str(me_target),file=sys.stderr)
        if Wolff.is_up(me_target.pos):
            new_pos=(Wolff.pos[0],Wolff.pos[1]-ME_ESCAPE_STEP)
            if chk_target_distance(new_pos):
                Wolff.set_destination(new_pos)
        else:
            if Wolff.pos[1]+ME_ESCAPE_STEP<MAX_Y:
                new_pos=(Wolff.pos[0],Wolff.pos[1]+ME_ESCAPE_STEP)
                if chk_target_distance(new_pos):
                    Wolff.set_destination(new_pos)
                print("1", file=sys.stderr)
            else:
                new_pos=(Wolff.pos[0],Wolff.pos[1]-ME_ESCAPE_STEP)
                if chk_target_distance(new_pos):
                    Wolff.set_destination(new_pos)
                print("2", file=sys.stderr)
        #print("me_distance "+str(me_distance),file=sys.stderr)
        if get_distance(Wolff.destination, me_target.pos)<=DANGER_ZONE:
            if Wolff.is_right(me_target.pos):
                print("3", file=sys.stderr)
                new_pos=(Wolff.destination[0]+ME_ESCAPE_STEP,Wolff.destination[1])
                if chk_target_distance(new_pos):
                    Wolff.set_destination(new_pos)
            else:
                if Wolff.pos[0]+ME_ESCAPE_STEP<MAX_X:
                    print("4", file=sys.stderr)
                    new_pos=(Wolff.destination[0]-ME_ESCAPE_STEP,Wolff.destination[1])
                    if chk_target_distance(new_pos):
                        Wolff.set_destination(new_pos)
                else:
                    print("5", file=sys.stderr)
                    new_pos=(Wolff.destination[0]+ME_ESCAPE_STEP,Wolff.destination[1])
                    if chk_target_distance(new_pos):
                        Wolff.set_destination(new_pos)
        print(me_target,file=sys.stderr)
        print(Wolff,file=sys.stderr)
        print(me_target.isMovingAway(Wolff.pos),file=sys.stderr)
        print(me_min_distance,file=sys.stderr)
        if me_min_distance>2500:
            return Wolff.shoot(me_target.Id)
        else:
            if me_target.isMovingAway(Wolff.pos):
                return Wolff.shoot(me_target.Id)
            else:
                return Wolff.move()
    Wolff.set_destination(target.pos)
    if distance<=MIN_DISTANCE:
        return Wolff.shoot(target.Id)
    else:
        return Wolff.move()
# Shoot enemies before they collect all the incriminating data!
# The closer you are to an enemy, the more damage you do but don't get too close or you'll get killed.

def chk_target_distance(pos):
    for enmy in enemies:
        if get_distance(pos, enmy.pos)<2500:
            return False
    return True

enemies=[]
dataPoints=[]

Wolff=wolff((0,0))

# game loop
while True:
    x, y = [int(i) for i in input().split()]
    Wolff.pos=(x,y)
    tmp_enemies=[]
    #enemies=[]
    dataPoints=[]
    data_count = int(input())
    for i in range(data_count):
        data_id, data_x, data_y = [int(j) for j in input().split()]
        dataPoints.append(Data_Point((data_x, data_y), data_id))
    enemy_count = int(input())
    for i in range(enemy_count):
        enemy_id, enemy_x, enemy_y, enemy_life = [int(j) for j in input().split()]
        #print("location: "+str((enemy_x, enemy_y)), file=sys.stderr)
        #enemies.append(enemy((enemy_x, enemy_y), enemy_id, enemy_life))
        tmp_enmy=enemy((enemy_x, enemy_y), enemy_id, enemy_life)
        existing_enemies=[]
        if not enemies:
            #print("11", file=sys.stderr)
            enemies.append(tmp_enmy)
        
        for enmy in enemies:
            existing_enemies.append(enmy.Id)
            if enemy_id==enmy.Id:
                #print("22", file=sys.stderr)
                enmy.life=enemy_life
                enmy.set_pos((enemy_x, enemy_y))
        if tmp_enmy.Id not in existing_enemies:
            #print("33", file=sys.stderr)
            enemies.append(tmp_enmy)
        tmp_enemies.append(enemy_id)
    
    for enmy in enemies:
        #if enmy.isMovingAway(Wolff.pos):
            #print("enemy "+str(enmy.Id)+" moving away", file=sys.stderr)
        #else:
            #print("enemy "+str(enmy.Id)+" moving closer", file=sys.stderr)
        if enmy.Id not in tmp_enemies:
            #print("44", file=sys.stderr)
            enemies.remove(enmy)
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    
    # MOVE x y or SHOOT id
    #print("enemy count "+str(len(enemies)), file=sys.stderr)
    print(go_to_nearest_enemy())
