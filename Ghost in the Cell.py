import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

NUM_CONCURRENT_TROOPS = 8

class World:
    def __init__(self):
        self.players = []
        self.factories = []
        self.troops = []
        self.connections = []     
        self.bombs = []        
        self.bomb_defended = []
    
    def get_player(self, mId):
        for player in self.players:
            if player.mId == mId:
                return player                
    
    def get_factory(self, mId):
        for factory in self.factories:
            if factory.mId == mId:
                return factory
        return None
    
    def get_bomb(self, mId):
        for bomb in self.bombs:
            if bomb.mId == mId or bomb.mId == -1:
                bomb.mId = mId
                return bomb
        return None
    
    def get_num_troops(self, mId):
        count = 0
        for troop in self.troops:
            if troop.owner.mId == mId:
                count+=1
        return count
    
    def get_best_factory_to_bomb(self):
        player = self.get_player(1)
        enemy = self.get_player(-1)
        if len(player.bombs) <= 0:
            return None
        for bomb in player.bombs:
            if bomb.fired and not bomb.exploded:
                #print(str(bomb), file=sys.stderr)
                return None
        lst = enemy.factories
        lst.sort(key=lambda x: x.num_cyborgs, reverse = True)
        #print(str(lst), file=sys.stderr)
        if lst:
            if lst[0].num_cyborgs < 10:                
                return None
            source_list = self.get_nearest_factory_lst(lst[0].mId)
            for fact in source_list:
                if fact.owner.mId == 1:
                    return (fact, lst[0])
        return None
    
    def get_nearest_factory_lst(self, source):
        lst=[]
        final=[]        
        for connection in self.connections:
            if source == connection.fact_1 or source == connection.fact_2:
                lst.append(connection)
        lst.sort(key=lambda x: x.distance)
        for connection in lst:
            if source == connection.fact_1:
                final.append(self.get_factory(connection.fact_2))
            elif source == connection.fact_2:
                final.append(self.get_factory(connection.fact_1))
        return final
    
    def get_highest_production_factory_lst(self, *args):        
        lst = sorted(self.factories, key=lambda x: x.production, reverse=True)
        if args:
            lst = [i for i in lst if i.owner.mId in args]
        return lst
            
    def get_distance_to_factory(self, source, dest):
        for connection in self.connections:
            if source == connection.fact_1 and dest == connection.fact_2:
                return connection.distance
            if source == connection.fact_2 and dest == connection.fact_1:
                return connection.distance
        return 0
            
    def calculate_attack_cost(self, source, destination, extra):
        cost = 0
        if destination.owner.mId ==1 and (destination.num_cyborgs>10 or \
        destination.production ==3):
            return 1000000     
        if source.num_cyborgs < destination.num_cyborgs:
            return 1000000      
        distance = self.get_distance_to_factory(source.mId, destination.mId)
        cost += distance+destination.num_cyborgs+\
        extra + destination.production*distance - destination.production
        return cost
    
    def get_factories_attack_costs(self, extra, *args):
        attack_costs=[]
        targets = self.get_highest_production_factory_lst(0, -1)
        player = self.get_player(1)
        for fact in player.factories:
            for targ_fact in targets:
                attack_costs.append((fact, targ_fact, \
                self.calculate_attack_cost(fact, targ_fact, extra)))
        attack_costs.sort(key=lambda x: x[2])
        #print(attack_costs, file = sys.stderr)
        return attack_costs
    
    def get_factories_attack_costs_multiple(self, targ_fact):
        player = self.get_player(1)
        army = 0
        for fact in player.factories:            
            army += fact.num_cyborgs
        if army > targ_fact.num_cyborgs:
            return True
        return False
    
    def attack_from_largest_farthest(self, target, extra):
        player = self.get_player(1)
        fact = player.get_biggest_army()
        return "MOVE "+str(fact.mId)+" "+str(target.mId)+" "+\
            str((fact.num_cyborgs+extra)//2)
    
    def get_defend_actions(self):
        player = self.get_player(1)
        for bomb in self.bombs:
            if bomb.owner.mId == -1 and bomb.fired and not bomb.exploded \
            and not self.chk_bomb_defended(bomb.mId):
                lst = player.factories
                lst.sort(key=lambda x: x.num_cyborgs, reverse = True)    
                if lst:
                    source_list = self.get_nearest_factory_lst(lst[0].mId)
                    self.bomb_defended.append((bomb.mId, True))
                    return "MOVE "+str(lst[0].mId)+" "+str(source_list[0].mId)+\
                    " "+str(lst[0].num_cyborgs)
        return ""
    
    def chk_bomb_defended(self, bomb_id):
        for stats in self.bomb_defended:
            if stats[0] == bomb_id and stats[1]:
                return True
        return False
        
    def get_next_move(self, extra):
        attacks = self.get_factories_attack_costs(extra, True)
        bomb_action = self.get_best_factory_to_bomb()
        upgrades = self.get_upgrade_actions()
        defend = self.get_defend_actions()
        action = ""
        if not attacks: 
            action = "WAIT"
        else:         
            if self.get_num_troops(1) <NUM_CONCURRENT_TROOPS:                
                mult=""
                for attack in attacks:
                    if attack[2] > 50:
                        if not self.get_factories_attack_costs_multiple(attack[1]):
                            if mult =="": mult = "WAIT"
                        else:
                            mult += self.attack_from_largest_farthest(attack[1], extra)+";"
                    else:
                        mult += "MOVE "+str(attack[0].mId)+" "+str(attack[1].mId)+" "+\
                        str(attack[1].num_cyborgs+extra)+";"
                mult = self.remove_semicolums(mult)
                action = mult
            else:
                action = "WAIT"
        b_action = ""
        if bomb_action:
            player = self.get_player(1)
            for bomb in player.bombs:
                if not bomb.fired:
                    b_action = bomb.fire(bomb_action[0], bomb_action[1])
                    bmb = self.get_bomb(bomb.mId)
                    try:
                        bmb.fire(bomb_action[0], bomb_action[1])
                    except ValueError:
                        continue
                    break
        if action == "WAIT" and (b_action or upgrades or defend):
            action = ""
        b_action = self.remove_semicolums(b_action)
        upgrades = self.remove_semicolums(upgrades)
        defend = self.remove_semicolums(defend)        
        action += ";"+b_action
        action = self.remove_semicolums(action)
        action += ";"+upgrades
        action = self.remove_semicolums(action)
        action +=";"+defend
        return self.remove_semicolums(action)
                
    def remove_semicolums(self, strng):
        if not strng: return strng
        if strng[0] == ";": strng = strng[1:]
        if not strng: return strng
        if strng[len(strng)-1] == ";": strng = strng[:len(strng)-1]
        if not strng: return strng
        if strng[len(strng)-1] == ";": strng = strng[:len(strng)-1]
        if not strng: return strng
        if strng[len(strng)-1] == ";": strng = strng[:len(strng)-1]
        return strng
    
    def chk_factory_is_attacked(self, factory_id):
        for troop in self.troops:
            if troop.end_factory.mId == factory_id:
                return True
        return False
    
    def get_upgrade_actions(self):
        actions = ""
        for factory in self.factories:
            if factory.owner.mId != 1: continue
            try:
                factory.upgrade()
                if actions:
                    actions+=";INC "+str(factory.mId)
                else:
                    actions+="INC "+str(factory.mId)
            except ValueError:
                continue
        return self.remove_semicolums(actions)
    
    def get_factories_list(self):
        lst=[]
        for factory in self.factories:
            lst.append(factory.mId)
        return lst
    
    def get_troops_list(self):
        lst=[]
        for troop in self.troops:
            lst.append(troop.mId)
        return lst
    
    def reset(self):
        for player in self.players:
            player.troops = []
            player.factories = []
        self.factories = []
        self.troops = []
    
    def read_world(self, entity_type, entity_id, *args):        
        if entity_type == "FACTORY":
            for player in self.players:
                if player.mId == args[0]:
                    target_player = player
                    break
            connection_list = []
            for connection in self.connections:
                if connection.fact_1 == entity_id:
                    connection_list.append(connection)
            factory = Factory(entity_id, target_player, *args[1:3], connection_list)
            self.factories.append(factory)
            target_player.factories.append(factory)   
        elif entity_type == "TROOP":        
            for player in self.players:                
                if player.mId == args[0]:
                    target_player = player
                    break
            troop = Troop(entity_id, target_player, *args[1:])
            self.troops.append(troop)
            target_player.troops.append(troop)   
        elif entity_type == "PLAYER":
            self.players.append(Player(entity_id))        
        elif entity_type == "LINK":
            self.connections.append(Connection(*args))                
        elif entity_type == "BOMB":
            bomb = self.get_bomb(entity_id)
            player = self.get_player(args[0])
            bomb_player = player.get_bomb(entity_id)
            source = self.get_factory(args[1])
            dest = self.get_factory(args[2])
            #print("***Time remain: "+str(args[3]), file=sys.stderr)
            bomb.update_bomb(True, source, dest, args[3])
            bomb_player.update_bomb(True, source, dest, args[3])
                        
    def __repr__(self):
        out = ""
        for player in self.players:
            out+=str(player)+"\n"
        for factory in self.factories:
            out+=str(factory)+"\n"
        for troop in self.troops:
            out+=str(troop)+"\n"
        for connection in self.connections:
            out+=str(connection)+"\n"
        return out


class Connection:
    def __init__(self, fact_1, fact_2, distance):
        self.fact_1 = fact_1
        self.fact_2 = fact_2
        self.distance = distance        
    
    def __repr__(self):
        return str(self.fact_1)+" "+str(self.fact_2)+" "+str(self.distance)    


class Factory:
    def __init__(self, mId, owner, num_cyborgs, prduction, connections):
        self.mId = mId
        self.owner = owner
        self.num_cyborgs = num_cyborgs
        self.production = prduction
        self.connections = connections
    
    def upgrade(self):
        if self.num_cyborgs < 10 or self.production == 3:
            raise ValueError
        self.production+=1
        self.num_cyborgs -= 10
    
    def __repr__(self):
        return "Factory: "+str(self.mId)+"\n"+\
        "owner: "+str(self.owner.mId)+"\n"+\
        "num_cyborgs: "+str(self.num_cyborgs)+"\n"+\
        "production: "+str(self.production)        
   
   
class Bomb:
    def __init__(self, owner, fired, source = None, destination = None):
        self.mId = -1
        self.owner = owner
        self.fired = fired        
        self.source = source
        self.destination = destination
        self.exploded = False
        self.time_remain = 500
    
    def update_bomb(self, fired, source, destination, time_remain):
        self.fired = fired
        self.source = source
        self.destination = destination
        self.time_remain = time_remain
        if self.time_remain <= 1:
            self.exploded = True
   
    def fire(self, source, target):
        if self.owner.mId != 1:
           raise ValueError
        self.source = source  
        self.destination = target
        self.fired = True
        return "BOMB "+str(source.mId)+" "+str(target.mId)
        
    def __repr__(self):
        return "Bomb: "+str(self.mId)+"\n"+\
        " Owner: "+str(self.owner)+"\n"+\
        " Fired: "+str(self.fired)+"\n"+\
        " Source: "+str(self.source)+"\n"+\
        " Destination: "+str(self.destination)+"\n"+\
        " Exploded: "+str(self.exploded)+"\n"+\
        " Time remain: "+str(self.time_remain)
        
        
class Player:
    def __init__(self, mId, factories = [], troops = []):
        self.mId = mId
        self.factories = []
        self.troops = []
        self.bombs = []
        self.bombs.append(Bomb(self, False)) 
        self.bombs.append(Bomb(self, False))
    
    def get_biggest_army(self):
        big = 0
        source = None
        for fact in self.factories:
            if fact.num_cyborgs > 0 and fact.num_cyborgs > big:
                source = fact
                big = fact.num_cyborgs
        return source
    
    def get_bomb(self, mId):
        for bomb in self.bombs:
            if bomb.mId == mId or bomb.mId == -1:
                bomb.mId = mId
                return bomb
        return None
    
    def get_factories_list(self):
        lst=[]
        for factory in self.factories:
            lst.append(factory.mId)
        return lst
    
    def get_troops_list(self):
        lst=[]
        for troop in self.troops:
            lst.append(troop.mId)
        return lst
    
    def __repr__(self):
        out = "Player: "+str(self.mId)+"\n Factories: "
        for factory in self.factories:
            out+=str(factory.mId)+" "
        out += "\n Troops: "
        for troop in self.troops:
            out+=str(troop.mId)+" "
        return out


class Troop:
    def __init__(self, mId, owner, start_factory, end_factory, \
    num_cyborgs, remain_time_to_arrive):
        self.mId = mId
        self.owner = owner
        self.start_factory = start_factory
        self.end_factory = end_factory
        self.num_cyborgs = num_cyborgs
        self.remain_time_to_arrive = remain_time_to_arrive
        
    def __repr__(self):
        return "Troop: "+str(self.mId)+"\n"+\
        "Owner: "+str(self.owner.mId)+"\n"+\
        "Start Factory: "+str(self.start_factory)+"\n"+\
        "End Factory: "+str(self.end_factory)+"\n"+\
        "num_cyborgs: "+str(self.num_cyborgs)+"\n"+\
        "remain_time_to_arrive: "+str(self.remain_time_to_arrive)

world = World()

world.read_world("PLAYER", 1)
world.read_world("PLAYER", -1)
world.read_world("PLAYER", 0)

world.bombs.append(Bomb(world.get_player(1),False))
world.bombs.append(Bomb(world.get_player(1),False))
world.bombs.append(Bomb(world.get_player(-1),False))
world.bombs.append(Bomb(world.get_player(-1),False))

factory_count = int(input())  # the number of factories
link_count = int(input())  # the number of links between factories
for i in range(link_count):
    factory_1, factory_2, distance = [int(j) for j in input().split()]
    world.read_world("LINK", -1, factory_1, factory_2, distance)

# game loop
while True:
    world.reset()
    entity_count = int(input())  # the number of entities (e.g. factories and troops)
    for i in range(entity_count):
        entity_id, entity_type, arg_1, arg_2, arg_3, arg_4, arg_5 = input().split()
        entity_id = int(entity_id)
        arg_1 = int(arg_1)
        arg_2 = int(arg_2)
        arg_3 = int(arg_3)
        arg_4 = int(arg_4)
        arg_5 = int(arg_5)
        world.read_world(entity_type, entity_id, arg_1, arg_2, arg_3, arg_4, arg_5)    

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    #print(str(world), file=sys.stderr)
    #lst = world.get_factories_attack_costs(1)
    #print("*****", str(lst), file=sys.stderr)
    
    # Any valid action, such as "WAIT" or "MOVE source destination cyborgs"
    print(world.get_next_move(5))
