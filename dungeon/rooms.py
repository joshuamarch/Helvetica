from random import randint
from monsters import *

def rooms(player, room):
        if room == "Armoury":
            room = Armoury(player)
            return room
        elif room == "DarkPassage":
            room = DarkPassage(player)
            return room
        elif room == "Entrance":
            room = Entrance(player)
            return room
        elif room == "MirrorRoom":
            room = MirrorRoom(player)
            return room

class Room(object):
    
    def __init__(self, player):
        
        self.enter_text = "You walk into a room"
        self.paths = {}
        self.player = player
        self.nouns = []
        
        
    
    def enter(self):
        """
        enter the area and print enter text
        """
        return self.enter_text
    
    def navigate(self, direction):
        if direction in self.paths:
            self.player.last_location = self.location
            self.player.location = self.paths[direction]
            return
        else:
            return "You can't go that way."

       


class Entrance(Room):
    
    def __init__(self, player):
        
        self.nouns = ["torch"]
        
        self.player = player
        
        if "torch" in self.player.inventory:
            self.enter_text = "You are in a large entrance hall with a golden fire roaring in a hearth.\n" + \
                                "There is a door to the west, and a door to the east.\n" 
        
        else:
            self.enter_text = "You are in a large entrance hall with a golden fire roaring in a hearth.\n" + \
                                "There is a door to the west, and a door to the east.\n" + \
                                "You see a torch lying on the floor.\n"
        
        self.paths = {  "east": "DarkPassage", 
                        "west": "Armoury"}
        self.location = "Entrance"
            
        
        
    def actions(self, sentence):    
        if sentence.verb == 'go':
            self.player = self.navigate(sentence.object)
            return
        
        elif sentence.object == 'torch':
            if sentence.verb == 'look':
                return "It's a wooden torch, burning at one end."
            elif sentence.verb == 'pickup' or sentence.verb == 'grab' or sentence.verb == 'pick':
                self.player.add_item("torch")
                return "You picked up the torch"
            else:
                return "Do what to the torch? You could pick it up..."
        
        elif sentence.verb == 'look':
            return self.enter_text
            
        else:
            return "Say again?"
            

class Armoury(Room):
    
    def __init__(self, player):
        
        self.player = player
        
        self.nouns = ["sword", "key", "floor", "trinkets", "items"]
        
        
        if "torch" in self.player.inventory and "sword" in self.player.inventory:
            self.enter_text =   "You enter a room shimmering with silver and golden armour!\n" + \
                                "There are lots of trinkets and metal items all over the floor."
                                
        elif "torch" in self.player.inventory:
            self.enter_text =   "You enter a room shimmering with silver and golden armour!\n" + \
                                "There is a sword on the wall, and lots of trinkets and metal items all over the floor."
                                
        else:
            self.enter_text =   "You walk through the door into a dark room. \n" + \
                                "Maybe you would see more if you had a torch?"
                                
        self.paths = {  "east": "Entrance" }
        self.location = "Armoury"
        
            
    def actions(self, sentence):
        if sentence.verb == 'go':
            self.player = self.navigate(sentence.object)
            return
        
        elif sentence.verb == 'look' or sentence.verb == 'search':
            
            if sentence.object == 'floor' or sentence.object == 'trinkets' or sentence.object == 'items':
                check = randint(1, 50)
                
                if self.player.luck >= check:
                    self.player.add_item("passage_key")
                    return "You found a key! You put it in your pocket"
                else:
                    return "You search around but don't find anything this time - try again?"
            
            elif sentence.object == 'sword':
                return "It is a plain metal sword. Looks sharp."
                
            else:
                return self.enter_text
        
        elif sentence.object == 'sword':
            self.player.add_item("sword")
            return "You take the sword - it could come in handy later!"
        
        elif sentence.verb == 'look':
            return self.enter_text
    
        else:
            return "Say again?"

class DarkPassage(Room):
    
    def __init__(self, player):
        
        self.player = player
        self.nouns = ["door"]
        
        
        if "Dark_Passage_Door_Unlocked" in self.player.achievements:
            self.paths = { "west": "Entrance",
                        "east": "MirrorRoom"}
        else:
            self.paths = { "west": "Entrance" }
        
        
        self.location = "DarkPassage"
        
        if "torch" in self.player.inventory:
            self.enter_text =   "You walk through the door into a long dark passage continuing east.\n" + \
                                "In the faint torchlight you see a small door at the end."
                                
        else:
            self.enter_text =   "You walk through the door into a dark passage.\n" + \
                                "Maybe you would see more if you had a torch?"
                                
        
    
    def actions(self, sentence):        
        if sentence.verb == 'go':
            self.player = self.navigate(sentence.object)
            return
        
        elif sentence.object == 'door':
            
            if sentence.verb == 'look':
                return "it's a sturdy wooden door, with a rusty old lock. There's a small mirror on the door at face level."
                
            elif sentence.verb == 'open':
        
                if "passage_key" in self.player.inventory:
                    self.player.add_achievement("Dark_Passage_Door_Unlocked")
                    return "You turn the key in the lock and the door swings open"
                else:
                    return "The door is locked. Maybe you could find a key?"
        
        elif sentence.verb == 'look':
            return self.enter_text
            
        else:
            return "Say again?"
            
class MirrorRoom(Room):
    
    def __init__(self, player):
        
        self.player = player
        
        self.nouns = ["monster"]
        
        if "Mirror_Room_Monster_Killed" in self.player.achievements:
            self.paths = {  "north": "NewRoom", 
                        "west": "DarkPassage"}
            
            self.enter_text =   "You walk into an octagonal room, with each wall made up of a floor to ceiling mirror.\n"
            
        else:
            self.paths = { "west": "DarkPassage"}
            
            self.enter_text =   "You walk into an octagonal room, with each wall made up of a floor to ceiling mirror.\n" +\
                            "In the middle there's a monster... it looks just like you! It roars and gets ready to attack! \n"
        
            mirror_monster = MirrorMonster()
            self.mirror_monster = mirror_monster
        
    
    def actions(self, sentence):  
        if sentence.verb == 'go':
            self.player = self.navigate(sentence.object)
            return
        
        elif sentence.object == 'monster':
            
            if sentence.verb == "attack" or sentence.verb == "kill":
                if sentence.item == 'sword':
                    if "sword" in self.player.inventory:
                        text = self.mirror_monster.attack(self.player, "sword")
                        return text
                    else:
                        return "You don't have a sword!"
                
                elif sentence.item == 'torch':
                    if "torch" in self.player.inventory:
                        return self.mirror_monster.attack(self.player, "torch")
                    else:
                        return "You don't have a torch!"
                
                else:
                    print "You attack the monster with your fists!"
                    return self.mirror_monster.attack(self.player, "fists")

            else:
                return "The monster stares at you with your own eyes, growling."       
        
        elif sentence.verb == 'look':
            return self.enter_text
        
        else:
            return "Say again?"