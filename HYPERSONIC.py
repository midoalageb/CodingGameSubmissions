import sys
import math
from operator import itemgetter
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

class empty_square():
    def __init__(self, mPos):
        self.pos=mPos
    
    def __str__(self):
        return self.__class__.__name__+" \n  Pos: "+str(self.pos)
        

class box():
    def __init__(self, mPos):
        self.pos=mPos
    def __str__(self):
        return self.__class__.__name__+" \n  Pos: "+str(self.pos)
    def __eq__(self, other):
        return self.pos == other.pos

class wall():
    def __init__(self, mPos):
        self.pos=mPos
    def __str__(self):
        return self.__class__.__name__+" \n  Pos: "+str(self.pos)
        
class item():
    def __init__(self, mPos, mTyp):
        self.pos=mPos
        self.typ=mTyp
    def __str__(self):
        return self.__class__.__name__+" \n  Pos: "\
        +str(self.pos)+"\n  Type: "\
        +"Extra range" if self.typ==1 else "Extra bomb"

class bomb():
    def __init__(self, Owner, mPos, mRadius, mTimer):
        self.owner=Owner
        self.pos=mPos
        self.radius=mRadius
        self.timer=mTimer
    
    def setTimer(self, mTimer):
        self.timer=mTimer
    
    def setRadius(self, mRadius):
        self.radius=mRadius
    
    def tick(self):
        if self.timer>1:
            self.timer-=1
    
    def set_owner(self, owner):
        self.owner=owner
    
    def __str__(self):
        return self.__class__.__name__+" \n  Pos: "\
        +str(self.pos)+" \n  owner: "\
        +str(self.owner)+" \n  radius: "\
        +str(self.radius)+" \n  timer: "\
        +str(self.timer)

class bot():
    global world, enemy_bombs
    def __init__(self, ID, mPos, numBombs, mBombRaius):
        self.mId=ID
        self.pos=mPos
        self.num_bombs=numBombs
        self.bomb_radius=mBombRaius
        self.destination=(0,0)
        self.placed_bombs=[]
        self.bombs=[]
        self.bomb_timer=8
        
    def add_bomb(self, mPos, *arg):
        if arg:
            for bmb in self.bombs:
                if mPos==bmb.pos:
                    return
            self.bombs.append(bomb(arg[0], mPos, arg[1], arg[2]))
        else:
            for bmb in self.bombs:
                if mPos==bmb.pos:
                    return
            self.bombs.append(bomb(self.mId, mPos, self.bomb_radius, self.bomb_timer)) 
        
    def set_bomb_radius(self, radius):
        for bmb in self.bombs:
            bmb.setRadius(radius)
    
    def tick_all(self):
        for bmb in self.bombs:
            bmb.tick()
            if bmb.timer<=1:
                self.bombs.remove(bmb)
        #print("ID "+str(self.mId),file=sys.stderr)
        #print("num bombs "+str(self.num_bombs),file=sys.stderr)
    
    def set_destination(self, dest):
        self.destination=dest
    
    def get_bombs(self):
        return self.bombs
    
    def bomb(self):
        return "BOMB "+str(self.destination[0])+" "+str(self.destination[1])
    
    def move(self):
        #nxt=(0,0)
        #print(self.destination[0]>self.pos[0],file=sys.stderr)
        #print(self.destination[0],file=sys.stderr)
        #right
        #if self.destination[0]>self.pos[0]:
        #    #print(world[(self.pos[0]+1,self.pos[1])],file=sys.stderr)
        #    if isinstance(world[(self.pos[0]+1,self.pos[1])], empty_square):
        #        #print("hi",file=sys.stderr)
        #        nxt=(self.pos[0]+1,self.pos[1])
        #        for bmb in enemy_bombs:
        #            if self.isPointInbombPath(nxt,bmb):
        #                nxt=(self.pos[0]+1,self.pos[1]+1)
        ##left
        #if self.destination[0]<self.pos[0]:
        #    #print(world[(self.pos[0]-1,self.pos[1])],file=sys.stderr)
        #    if isinstance(world[(self.pos[0]-1,self.pos[1])], empty_square):        
        #        nxt=(self.pos[0]-1,self.pos[1])
        #        for bmb in enemy_bombs:
        #            if self.isPointInbombPath(nxt,bmb):
        #                nxt=(self.pos[0]-1,self.pos[1]-1)
        ##top
        #if self.destination[1]<self.pos[1]:
        #    #print(world[(self.pos[0],self.pos[1]-1)],file=sys.stderr)
        #    if isinstance(world[(self.pos[0],self.pos[1]-1)], empty_square):        
        #        nxt=(self.pos[0],self.pos[1]-1)
        #        for bmb in enemy_bombs:
        #            if self.isPointInbombPath(nxt,bmb):
        #                nxt=(self.pos[0]-1,self.pos[1]-1)
        #bottom
        #if self.destination[1]>self.pos[1]:
        #    #print(world[(self.pos[0],self.pos[1]+1)],file=sys.stderr)
        #    if isinstance(world[(self.pos[0],self.pos[1]+1)], empty_square):        
        #        nxt=(self.pos[0],self.pos[1]+1)
        #        for bmb in enemy_bombs:
        #            if self.isPointInbombPath(nxt,bmb):
        #                nxt=(self.pos[0]+1,self.pos[1]+1)
        #print("next "+str(nxt),file=sys.stderr)
        #if nxt==(0,0):
        #    nxt=self.destination
        #return "MOVE "+str(nxt[0])+" "+str(nxt[1])
        return "MOVE "+str(self.destination[0])+" "+str(self.destination[1])

    def isPointInbombPath(self,point, bmb):
        #print("isInPath", file=sys.stderr)
        #print(self.pos, file=sys.stderr)
        #print(bmb.pos, file=sys.stderr)
        if point[0]==bmb.pos[0] and abs(point[1]-bmb.pos[1])<=bmb.radius:
            if point[1]>bmb.pos[1]:
                for i in range(abs(point[1]-bmb.pos[1])):
                    if not isinstance(world[bmb.pos[0],bmb.pos[1]+i],empty_square):
                        return False
            else:
                for i in range(abs(point[1]-bmb.pos[1])):
                    if not isinstance(world[bmb.pos[0],point[1]+i],empty_square):
                        return False
            return True
        elif point[1]==bmb.pos[1] and abs(point[0]-bmb.pos[0])<=bmb.radius:
            if point[0]>bmb.pos[0]:
                for i in range(abs(point[0]-bmb.pos[0])):
                    if not isinstance(world[bmb.pos[0]+i,bmb.pos[1]],empty_square):
                        return False
            else:
                for i in range(abs(point[0]-bmb.pos[0])):
                    if not isinstance(world[point[0]+i,bmb.pos[1]],empty_square):
                        return False
            return True
        return False

    def isInbombPath(self, bmb):
        #print("isInPath", file=sys.stderr)
        #print(self.pos, file=sys.stderr)
        #print(bmb.pos, file=sys.stderr)
        if self.pos[0]==bmb.pos[0] and abs(self.pos[1]-bmb.pos[1])<=bmb.radius:
            if self.pos[1]>bmb.pos[1]:
                for i in range(abs(self.pos[1]-bmb.pos[1])):
                    if not isinstance(world[bmb.pos[0],bmb.pos[1]+i],empty_square) and not isinstance(world[bmb.pos[0],bmb.pos[1]+i],bomb):
                        return False
            else:
                for i in range(abs(self.pos[1]-bmb.pos[1])):
                    if not isinstance(world[bmb.pos[0],self.pos[1]+i],empty_square) and not isinstance(world[bmb.pos[0],self.pos[1]+i],bomb):
                        return False
            return True
        elif self.pos[1]==bmb.pos[1] and abs(self.pos[0]-bmb.pos[0])<=bmb.radius:
            if self.pos[0]>bmb.pos[0]:
                for i in range(abs(self.pos[0]-bmb.pos[0])):
                    if not isinstance(world[bmb.pos[0]+i,bmb.pos[1]],empty_square) and not isinstance(world[bmb.pos[0]+i,bmb.pos[1]],bomb):
                        return False
            else:
                for i in range(abs(self.pos[0]-bmb.pos[0])):
                    if not isinstance(world[self.pos[0]+i,bmb.pos[1]],empty_square) and not isinstance(world[self.pos[0]+i,bmb.pos[1]],bomb):
                        return False
            return True
        return False
        
        #if self.pos[0]==bmb.pos[0] and abs(self.pos[0]-bmb.pos[0])<=bmb.radius:
        #    return True
        #elif self.pos[1]==bmb.pos[1] and abs(self.pos[1]-bmb.pos[1])<=bmb.radius:
        #    return True
        #return False
    def __str__(self):
        return self.__class__.__name__+" \n  Pos: "\
        +str(self.pos)+" \n  ID: "\
        +str(self.mId)+" \n  num_bombs: "\
        +str(self.num_bombs)+" \n  bomb_radius: "\
        +str(self.bomb_radius)+" \n  destination: "\
        +str(self.destination)+" \n  placed_bombs: "\
        +str(self.placed_bombs)+" \n  bombs: "\
        +str(self.bombs)+" \n  bomb_timer: "\
        +str(self.bomb_timer)

def get_dist(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])

def get_nearest_Box(*arg):
    min_dist=200
    lst=[]
    dest=(0,0)
    for bx in boxes:
        dist=get_dist(me.pos,bx.pos)
        if dist<min_dist:
            min_dist=dist
            dest=bx.pos
        lst.append((dest,dist))
    lst.sort(key=itemgetter(1))
    if arg:
        dest=lst[arg[0]][0]
        
    if dest[0]-1>0 and world[(dest[0]-1,dest[1])] is empty_square:
        return (dest[0]-1,dest[1])
    if dest[0]+1<width and world[(dest[0]+1,dest[1])] is empty_square:
        return (dest[0]+1,dest[1])
    if dest[1]-1>0 and world[(dest[0], dest[1]-1)] is empty_square:
        return (dest[0],dest[1]-1)
    if dest[1]+1<height and world[(dest[0], dest[1]+1)] is empty_square:
        return (dest[0],dest[1]+1)
    return dest

def chk_bmb_explode():
    #print(thread_bomb,file=sys.stderr)
    if isinstance(thread_bomb, bomb):
        if thread_bomb.timer>1:
            return False
        if thread_bomb.timer==1:
            thread_bomb.timer-=1
            return False
    return True

def move_left(Pos):
    if Pos[0]-1>=0 and (isinstance(world[Pos[0]-1,Pos[1]],empty_square) or isinstance(world[Pos[0]-1,Pos[1]],item)):
        return (Pos[0]-1,Pos[1])
    else: return Pos

def move_right(Pos):
    if Pos[0]+1<width and (isinstance(world[Pos[0]+1,Pos[1]],empty_square) or isinstance(world[Pos[0]+1,Pos[1]],item)):
        return (Pos[0]+1,Pos[1])
    else: return Pos

def move_up(Pos):
    if Pos[1]-1>=0 and (isinstance(world[Pos[0],Pos[1]-1],empty_square) or isinstance(world[Pos[0],Pos[1]-1],item)):
        return (Pos[0],Pos[1]-1)
    else: return Pos

def move_down(Pos):
    if Pos[1]+1<height and (isinstance(world[Pos[0],Pos[1]+1],empty_square) or isinstance(world[Pos[0],Pos[1]+1],item)):
        return (Pos[0],Pos[1]+1)
    else: return Pos

def chk_box_left(Pos):
    if Pos[0]-1<0:
        return False
    return isinstance(world[Pos[0]-1,Pos[1]],box)

def chk_box_right(Pos):
    if Pos[0]+1>=width:
        return False
    return isinstance(world[Pos[0]+1,Pos[1]],box)

def chk_box_up(Pos):
    if Pos[1]-1<0:
        return False
    return isinstance(world[Pos[0],Pos[1]-1],box)

def chk_box_down(Pos):
    if Pos[1]+1>=height:
        return False
    return isinstance(world[Pos[0],Pos[1]+1],box)
    
def get_path_to_destination(dest):
    print("test dest "+str(dest),file=sys.stderr)
    if not isinstance(world[dest], empty_square):
        return False
    path=[]
    path.append(me.pos)
    start=me.pos
    count=0
    while start!=dest and count<20:
        print("path "+str(path),file=sys.stderr)
        print("count "+str(count),file=sys.stderr)
        count+=1
        if start==dest:
            return True
        test=move_right(start)
        print("test "+str(test),file=sys.stderr)
        if not test in path and test!=start:
            path.append(test)
            print(" path "+str(path),file=sys.stderr)
            start=test
            continue
        test=move_left(start)
        print("test "+str(test),file=sys.stderr)
        if not test in path and test!=start:
            path.append(test)
            print(" path "+str(path),file=sys.stderr)
            start=test
            continue
        test=move_down(start)
        print("test "+str(test),file=sys.stderr)
        if not test in path and test!=start:
            path.append(test)
            print(" path "+str(path),file=sys.stderr)
            start=test
            continue
        test=move_up(start)
        print("test "+str(test),file=sys.stderr)
        if not test in path and test!=start:
            path.append(test)
            print(" path "+str(path),file=sys.stderr)
            start=test
            continue
        path=[]
        path.append(me.pos)
        start=me.pos
        #count=0
    if start==dest:
            return True
    return False

def chk_neighbor_box():
    return chk_box_left(me.pos) or chk_box_right(me.pos) \
    or chk_box_up(me.pos) or chk_box_down(me.pos)

width, height, my_id = [int(i) for i in input().split()]

start_pos=(0,0)
removed_box=[]
world={}
boxes=[]
thread_bomb=(0,0)
same_place=0
last_place=(0,0)

me=bot(my_id, (0,0), 1, 2)
enemy=bot(-1, (width,height), 1, 2)
enemy_bombs=[]
first_round=True

# game loop
while True:
    me.tick_all()
    #print(me,file=sys.stderr)
    enemy.tick_all()
    if thread_bomb is bomb:
        thread_bomb.tick()
    world={}
    boxes=[]
    enemy_bombs=[]
    for i in range(height):    
        row = input()
        for j in range(len(row)):
            if row[j]=='.':
                world[(j,i)]=empty_square((j,i))                
            elif row[j]=='X':
                world[(j,i)]=wall((j,i))
            else:
                if not (j,i) in removed_box:    
                    bx=box((j,i))
                    world[(j,i)]=bx
                    boxes.append(bx)
                else:
                    world[(j,i)]=empty_square((j,i))
    entities = int(input())
    for i in range(entities):
        entity_type, owner, x, y, param_1, param_2 = [int(j) for j in input().split()]
        #Players
        if entity_type==0:
            if owner==my_id:
                if first_round:
                    start_pos=(x,y)
                    first_round=False
                me.pos=(x,y)
                me.num_bombs=param_1
                me.bomb_radius=param_2
                me.set_bomb_radius(param_2)
            else:
                if enemy.mId==-1:
                    enemy.mId=owner
                enemy.pos=(x,y)
                enemy.num_bombs=param_1
                enemy.bomb_radius=param_2
                enemy.set_bomb_radius(param_2)
        #Bombs
        elif entity_type==1:
            world[(x,y)]=bomb(owner, (x,y), param_2, param_1)
            if owner==my_id:
                me.add_bomb((x,y))
                enemy.add_bomb((x,y), owner, param_2, param_1)
                enemy_bombs.append(bomb(owner, (x,y), param_2, param_1))
            else:
                enemy.add_bomb((x,y))
                enemy_bombs.append(bomb(owner, (x,y), param_2, param_1))
        #Items
        elif entity_type==2:
            world[(x,y)]=item((x,y), param_1)
            #print(world[(x,y)],file=sys.stderr)
    #print(me.bombs, file=sys.stderr)
    mbox=near=get_nearest_Box()
    #tmp_near=get_nearest_Box()
    #while boxes:
    #    mbox=near=get_nearest_Box()
    #    print("near box "+ str(near), file=sys.stderr)
    #tmp_near=near
    #    left_near=move_left(near)
    #    print(" left_near "+ str(left_near), file=sys.stderr)
    #    right_near=move_right(near)
    #    print(" right_near "+ str(right_near), file=sys.stderr)
    #    down_near=move_down(near)
    #    print(" down_near "+ str(down_near), file=sys.stderr)
    #    up_near=move_up(near)
    #    print(" up_near "+ str(up_near), file=sys.stderr)
    #    if left_near!=near:
    #        if get_path_to_destination(left_near):
    #            print("  Left", file=sys.stderr)
    #            near=left_near
    #            break
    #    if right_near!=near:
    #        if get_path_to_destination(right_near):
    #            near=right_near
    #            break
    #    if down_near!=near:
    #        if get_path_to_destination(down_near):
    #            near=down_near
    #            break
    #    if up_near!=near:
    #        if get_path_to_destination(up_near):
    #            near=up_near
    #            break
    #    print("boxes "+str(len(boxes)), file=sys.stderr)
    #    for bx in boxes:
    #        if bx.pos==mbox:
    #            boxes.remove(bx)
    #    print("boxes "+str(len(boxes)), file=sys.stderr)
        
    #if not boxes:
    #    near=tmp_near
    #if me.num_bombs!=0:
    #    near=get_nearest_Box(1)
    #    print("near2 "+str(near), file=sys.stderr)
    #else:
    #    near=get_nearest_Box()
    #    print("near "+str(near), file=sys.stderr)
    
    out=""
    
    if me.destination==start_pos or get_dist(me.pos, start_pos)==1:
        if chk_bmb_explode():
            print("BOOM", file=sys.stderr)
            thread_bomb=(0,0)
            
    if thread_bomb==(0,0):
        me.set_destination(near)
        print("1",file=sys.stderr)
    
    if chk_neighbor_box():
        out=me.bomb()
        print("2",file=sys.stderr)
        if len(me.bombs)==0:
            removed_box.append(near)
        me.add_bomb(me.pos)
    else:
        out=me.move()
        print("3",file=sys.stderr)
    
    if not boxes:
        me.set_destination(enemy.pos)
        if get_dist(me.pos, enemy.pos)<3:
            out=me.bomb()
        else:
            out=me.move()
        
   
    for bmb in enemy.bombs:
    
        if me.isInbombPath(bmb):
            #print(" enemy bomb in path",file=sys.stderr)
            thread_bomb=bmb
            if thread_bomb.pos[0]==start_pos[0]:
                if start_pos[0]+1<width-1:
                    me.set_destination((start_pos[0]+1,start_pos[1]))
                else:
                    me.set_destination((start_pos[0]-1,start_pos[1]))
                print("4",file=sys.stderr)
            elif thread_bomb.pos[1]==start_pos[1]:
                if start_pos[1]+1<height-1:
                    me.set_destination((start_pos[0],start_pos[1]+1))
                else:
                    me.set_destination((start_pos[0],start_pos[1]-1))
                #me.set_destination((0,1))
                print("5",file=sys.stderr)
            else:
                me.set_destination(start_pos)
                print("6",file=sys.stderr)
            out=me.move()
            #print(out,file=sys.stderr)
    
    if out.startswith('BOMB') and me.num_bombs>0:
        enemy.add_bomb(me.pos, me.mId, me.bomb_radius, me.bomb_timer)
    print("thread_bomb " +str(thread_bomb),file=sys.stderr)
        #for bmb in enemy.bombs:
            #print("xenemy bomb " +str(bmb),file=sys.stderr)
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    
    print(out)
