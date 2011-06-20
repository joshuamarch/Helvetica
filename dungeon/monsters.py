from random import randint

class Monster(object):
    
    def __init__(self):
        
        self.attributes = {"luck": 0,
                            "strength": 0,
                            "constitution": 0,
                            "speed": 0
                            }
        self.health = 50
        
        self.weapon_value = {"sword": 10}
        
        self.alive = True
        
        self.achievement = " "
    
    def monster_killed(self, player):
        player.add_achievement(self.achievement)
        
    def attack(self, player, weapon=False):
        
        player_first = self.initiative_check(player)
        
        if player_first == True:
            text = self.attacked_by_player(player, weapon)
            if self.alive:
                text += self.attack_player(player)
                return text
            else:
                self.monster_killed(player)
                return text
        else:
            text = self.attack_player(player)
            
            text += self.attacked_by_player(player, weapon)
            if alive:
                return text
            else:
                self.alive = False
                self.monster_killed(player)
                return text
        
    
    def initiative_check(self, player):
        if player.speed >= self.attributes["speed"]:
            return True
        else:
            return False
    
    def attacked_by_player(self, player, weapon=False):
        
        attack_dice = randint(1, 100)
        
        if self.weapon_value[weapon]:
            weapon_value = self.weapon_value[weapon]
        else:
            weapon_value = 0
        
        attack_value = player.strength + attack_dice + weapon_value
        
        damage = attack_value - self.attributes["constitution"]
        
        if damage < 0:
            damage = 0
        
        text = "You attack the monster with your " + weapon + " causing " + str(damage) + " damage"
        
        self.health -= damage
        
        if self.health <= 0:
            text += "You slay the beast!"
            self.alive = False
            return text
        else:
            text += "It's still alive..."
            self.alive = True
            return text
    
    def attack_player(self, player):
        
        attack_dice = randint(1, 100)
        
        attack_value = self.attributes["strength"] + attack_dice 
        
        damage = attack_value - player.constitution
        
        if damage < 0:
            damage = 0
        
        text = "The monster attacks you, causing " + str(damage) + " damage"
        
        player.health -= damage
        
        if player.health <= 0:
            text += "The beast kills you!"
            player.death()
            return text
        else:
            text += "You're still alive"
            return text
    
 
class MirrorMonster(Monster):
    
    def __init__(self):
        
        self.attributes = {"luck": 30,
                            "strength": 30,
                            "constitution": 30,
                            "speed": 30
                            }
        self.health = 50
        
        self.weapon_value = {"sword": 10, "torch": 5}
        
        self.alive = True
        
        self.achievement = "Mirror_Room_Monster_Killed"
        