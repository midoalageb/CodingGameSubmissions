import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

def get_distance(a, b):
    return math.hypot(abs(a[0] - b[0]), abs(a[1] - b[1]))

def get_bearing(a, b):
    result = ""
    if a[0] > b[0]: result += "LEFT "
    elif a[0] < b[0]: result += "RIGHT "
    if a[1] > b[1]: result += "UP"
    elif a[1] < b[1]: result += "DOWN"
    return result

WORLD_WIDTH = 23
WORLD_HEIGHT = 21

class World():
    def __init__(self):
        self.ships = []
        self.barrels = []
        self.this_turn_barrel_ids = []
        self.this_turn_cannon_ids = []
        self.this_turn_mine_ids = []
        self.this_turn_ship_ids = []
        self.cannon_balls = []
        self.mines = []

    def get_attack(self):
        my_ships = []
        enemy_ships = []
        orders = []
        for ship in self.ships:
            if ship.mine:
                my_ships.append(ship)
            else:
                enemy_ships.append(ship)
        if my_ships:
            for my_ship in my_ships:                
                enemy_distance = []
                for enemy_ship in enemy_ships:
                    distance = get_distance(my_ship.pos, enemy_ship.pos)
                    if distance > 10:
                        continue
                    enemy_distance.append((1+distance//3, enemy_ship))            
                if enemy_distance:
                    enemy_distance.sort(key=lambda x: x[0])
                    orders.append(my_ship.fire(enemy_distance[0][1], enemy_distance[0][0]))
                else:
                    orders.append(my_ship.drop_mine())
        return orders
        
    def check_collision(self, ship):
        for shp in self.ships:
            if get_distance(shp.pos, ship.pos) <= 5:
                direction = get_bearing(ship.pos, shp.pos)
                if "UP" in direction:
                    return "MOVE "+str(ship.pos[0])+" "+\
                    str(min(ship.pos[1]+3, WORLD_HEIGHT))
                elif "DOWN" in direction:
                    return "MOVE "+str(ship.pos[0])+" "+\
                    str(max(ship.pos[1]-3, 0))
                elif "LEFT" in direction:
                    return "MOVE "+str(min(ship.pos[0]+3, WORLD_WIDTH))+" "\
                    +str(ship.pos[1])                    
                elif "RIGHT" in direction:
                    return "MOVE "+str(max(ship.pos[0]-3, 0))+" "\
                    +str(ship.pos[1]) 
        for mine in self.mines:
            if get_distance(mine.pos, ship.pos) <= 3:
                direction = get_bearing(ship.pos, mine.pos)
                if "UP" in direction:
                    return "MOVE "+str(ship.pos[0])+" "+\
                    str(min(ship.pos[1]+3, WORLD_HEIGHT))
                elif "DOWN" in direction:
                    return "MOVE "+str(ship.pos[0])+" "+\
                    str(max(ship.pos[1]-3, 0))
                elif "LEFT" in direction:
                    return "MOVE "+str(min(ship.pos[0]+3, WORLD_WIDTH))+" "\
                    +str(ship.pos[1])                    
                elif "RIGHT" in direction:
                    return "MOVE "+str(max(ship.pos[0]-3, 0))+" "\
                    +str(ship.pos[1]) 
        return None
    
    def get_optimum_barrel(self):
        my_ships = []
        orders = []
        for ship in self.ships:
            if ship.mine:
                my_ships.append(ship)                
        print("My ships", len(my_ships), file=sys.stderr)
        if my_ships:
            for my_ship in my_ships:                
                barrels_distance = []
                for barrel in self.barrels:
                    distance = get_distance(my_ship.pos, barrel.pos)
                    if my_ship.rum_stock-distance+barrel.rum > 100:
                        continue
                    barrels_distance.append((my_ship.rum_stock-distance+barrel.rum, barrel))            
                if barrels_distance:
                    barrels_distance.sort(key=lambda x: x[0], reverse=True)
                    collision = self.check_collision(my_ship)
                    if collision:
                        var = collision.split()
                        new_pos = (int(var[1]), int(var[2]))
                        if new_pos == my_ship.pos:
                            orders.append(my_ship.move(barrels_distance[0][1].pos))
                        else:
                            orders.append(collision)
                    else:
                        orders.append(my_ship.move(barrels_distance[0][1].pos))
                else:
                    # orders.append(my_ship.wait())
                    if my_ship.pos < (21,19):
                        new_pos = (21,19)
                    else:
                        new_pos = (0,0)
                    orders.append(my_ship.move(new_pos))
        print("orders", str(orders), file=sys.stderr)
        return orders
    
    def add_item(self, obj_type, *args):
        if obj_type == "SHIP":
            self.add_GameObject(Ship(*args))
        elif obj_type == "BARREL":
            self.add_GameObject(Barrel(*args[0:4]))
        elif obj_type == "CANNONBALL":
            self.add_GameObject(CannonBall(*args[0:5]))
        elif obj_type == "MINE":
            self.add_GameObject(Mine(*args[0:3]))
    
    def __str__(self):
        result = ""
        for ship in self.ships:            
            result += str(ship)+"\n"            
        for barrel in self.barrels:
            result += str(barrel)+"\n"
        return result    

    def add_GameObject(self, obj):
        if isinstance(obj, Mine):
            this_turn_list =  self.this_turn_mine_ids
            lst = self.mines
        elif isinstance(obj, CannonBall):
            this_turn_list =  self.this_turn_cannon_ids
            lst = self.cannon_balls
        elif isinstance(obj, Barrel):
            this_turn_list =  self.this_turn_barrel_ids
            lst = self.barrels
        elif isinstance(obj, Ship):
            this_turn_list =  self.this_turn_ship_ids
            lst = self.ships
        this_turn_list.append(obj.mID)
        for objec in lst:
            if objec.mID == obj.mID:
                objec.update(obj)
                return
        lst.append(obj)
    
    def remove_old_objects(self):
        self.remove_GameObject(Mine(-1, 0, 0))
        self.remove_GameObject(CannonBall(-1, 0, 0, 0, 0))
        self.remove_GameObject(Barrel(-1, 0, 0, 0))
        self.remove_GameObject(Ship(-1, 0, 0, 0, 0, 0, 0))
    
    def remove_GameObject(self, obj):
        if isinstance(obj, Mine):
            this_turn_list =  self.this_turn_mine_ids
            lst = self.mines
        elif isinstance(obj, CannonBall):
            this_turn_list =  self.this_turn_cannon_ids
            lst = self.cannon_balls
        elif isinstance(obj, Barrel):
            this_turn_list =  self.this_turn_barrel_ids
            lst = self.barrels
        elif isinstance(obj, Ship):
            this_turn_list =  self.this_turn_ship_ids
            lst = self.ships    
        for objec in lst:
            if objec.mID not in this_turn_list:
                lst.remove(objec)    
    
    def clear_current_turn(self):
        self.this_turn_barrel_ids = []
        self.this_turn_cannon_ids = []
        self.this_turn_mine_ids = []
        self.this_turn_ship_ids = []
    

class GameObject():
    def __init__(self, mID, pos_x, pos_y):
        self.mID = mID
        self.pos = (pos_x, pos_y)

    def __str__(self):        
        return str(type(self))+"\n"+"ID: "+str(self.mID)+"\n"+\
        "pos: "+str(self.pos)
        
        
class CannonBall(GameObject):
    def __init__(self, mID, pos_x, pos_y, ship_id, time_to_impact):
        GameObject.__init__(self, mID, pos_x, pos_y)
        self.ship_id = ship_id
        self.time_to_impact = time_to_impact
    
    def update(self, obj):
        self = CannonBall.__init__(self, self.mID, obj.pos[0], obj.pos[1], obj.ship_id, obj.time_to_impact)
        
    def __str__(self):
        result = GameObject.__str__(self)+"\n"
        result += "ship_id:"+ str(self.ship_id)+"\n"
        result += "time_to_impact:"+ str(self.time_to_impact)
        return result


class Mine(GameObject):
    def __init__(self, mID, pos_x, pos_y):
        GameObject.__init__(self, mID, pos_x, pos_y)        
    
    def update(self, obj):
        self = Mine.__init__(self, self.mID, obj.pos[0], obj.pos[1])
    
    def __str__(self):
        return GameObject.__str__(self)       


class Barrel(GameObject):
    def __init__(self, mID, pos_x, pos_y, rum):
        GameObject.__init__(self, mID, pos_x, pos_y)
        self.rum = rum        
        
    def update(self, barrel):
        self = Barrel.__init__(self, self.mID, barrel.pos[0], barrel.pos[1], barrel.rum)

    def __str__(self):
        result = GameObject.__str__(self)+"\n"
        result += "Rum:"+ str(self.rum)
        return result

class Ship(GameObject):
    def __init__(self, mID, pos_x, pos_y, orientation, speed, rum_stock, mine):
        GameObject.__init__(self, mID, pos_x, pos_y)
        self.orientation = orientation
        self.speed = speed
        self.mine = (mine == 1)
        self.rum_stock = rum_stock
    
    def __str__(self):
        result = GameObject.__str__(self)+"\n"
        result += "Orientation:"+ str(self.orientation)+"\n"
        result += "Speed:"+ str(self.speed)+"\n"
        result += "Mine:"+ str(self.mine)+"\n"
        result += "Rum_stock:"+ str(self.rum_stock)
        return result
        
    def update(self, ship):
        self = Ship.__init__(self, self.mID, ship.pos[0], ship.pos[1]\
        , ship.orientation, ship.speed, ship.rum_stock, ship.mine)
    
    def move(self, pos):
        return "MOVE "+str(pos[0])+" "+str(pos[1])
    
    def slow(self):
        return "SLOWER"
        
    def drop_mine(self):
        return "MINE"
        
    def get_pos_to_shoot(self, ship, turns_to_reach):
        # print("speed: "+str(ship.speed), file=sys.stderr)
        # print("turns_to_reach: "+str(turns_to_reach), file=sys.stderr)
        if ship.orientation == 0:
            return (min(ship.pos[0]+(ship.speed*turns_to_reach),WORLD_WIDTH-1),\
            ship.pos[1])
        if ship.orientation == 1:
            return (min(ship.pos[0]+(ship.speed*turns_to_reach)/2,WORLD_WIDTH-1),\
            min(ship.pos[1]+(ship.speed*turns_to_reach)/2,0))
        if ship.orientation == 2:
            return (max(ship.pos[0]-(ship.speed*turns_to_reach)/2,0),\
            max(ship.pos[1]+(ship.speed*turns_to_reach)/2,0))
        if ship.orientation == 3:
            return (max(ship.pos[0]-(ship.speed*turns_to_reach),0),\
            ship.pos[1])
        if ship.orientation == 4:
            return (max(ship.pos[0]-(ship.speed*turns_to_reach)/2,0),\
            min(ship.pos[1]+(ship.speed*turns_to_reach)/2,WORLD_HEIGHT-1))
        if ship.orientation == 5:
            return (min(ship.pos[0]+(ship.speed*turns_to_reach)/2,WORLD_WIDTH-1),\
            min(ship.pos[1]+(ship.speed*turns_to_reach)/2,WORLD_HEIGHT-1))
            
    def fire(self, ship, turns_to_reach):
        pos = self.get_pos_to_shoot(ship, turns_to_reach)
        if get_distance(self.pos, pos) <= 10:
            return "FIRE "+str(int(pos[0]))+" "+str(int(pos[1]))
        return "WAIT"
        
    def wait(self):
        return "WAIT"

world = World()
gameTurn = 0
# game loop
while True:
    world.clear_current_turn()
    my_ship_count = int(input())  # the number of remaining ships
    entity_count = int(input())  # the number of entities (e.g. ships, mines or cannonballs)
    for i in range(entity_count):
        entity_id, entity_type, x, y, arg_1, arg_2, arg_3, arg_4 = input().split()
        entity_id = int(entity_id)
        x = int(x)
        y = int(y)
        arg_1 = int(arg_1)
        arg_2 = int(arg_2)
        arg_3 = int(arg_3)
        arg_4 = int(arg_4)
        world.add_item(entity_type, entity_id, x, y, arg_1, arg_2, arg_3, arg_4)
    world.remove_old_objects()
    if gameTurn%10!=0:
        orders = world.get_optimum_barrel()        
    else:
        # orders = world.get_optimum_barrel()
        orders = world.get_attack()
        
    gameTurn += 1
    for i in range(my_ship_count):
        
        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr)

        # Any valid action, such as "WAIT" or "MOVE x y"
        print(orders[i])
