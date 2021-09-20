# In this simple RPG game, the hero fights the goblin. He has the options to:

# 1. fight goblin
# 2. do nothing - in which case the goblin will attack him anyway
# 3. flee
import random

class Character:
    def __init__(self, name, health, power, dodge, perception, armor, money, inventory, bounty, player_status):
        self.name = name
        self.health = health
        self.power = power
        self.dodge = dodge
        self.perception = perception
        self.armor = armor
        self.money = money
        self.inventory = inventory
        self.bounty = bounty
        self.player_status = player_status

    def attack(self, opposite):
        opposite.miss_me()
        if opposite.dodging == False:
            if self.name == "Hero":
                hero.critical()
            self.motion_of_attack(opposite)
            if self.player_status == True:
                print(f"You do {self.power} damage to the {opposite.name}.")
            else:
                print(f"{self.name} does {self.power} damage to the {opposite.name}.")
        else:
            print(f"{self.name} needs to work on their aim!")
        opposite.ability(self)
        if opposite.health <= 0:
            print(f"\nThe {opposite.name} is dead.")
            if self.player_status == True:
                self.money += opposite.bounty
                print(f"You received {opposite.bounty} coins!\nYou have {self.money} coins!\n")
    
    def alive(self):
        life = True
        if self.health <= 0:
            life = False
        return life
    
    def print_status(self):
        if self.player_status == True:
            print(f"You have {self.health} health, {self.armor} armor, {int(((self.dodge)/20)*100)}% dodge and {self.power} power.")
        else:
            print(f"The {self.name} has {self.health} health, {self.armor} armor, {int(((self.dodge)/20)*100)}% dodge and {self.power} power.")
    
    def use_item(self):
        if len(self.inventory) > 0:
            number = 1 
            for item in self.inventory:
                print(f"{number}: {item.name} - {item.points} {item.quality} points")
                number += 1
            item_index_to_use = int(input("Which item would you like to use: ")) - 1
            item = self.inventory[item_index_to_use]
            if item.quality == "healing":
                self.health += item.points
                print(f"health increase {item.points}")
            if item.quality == "armor":
                self.armor += item.points
            if item.quality == "dodge":
                if item.points + self.dodge >= 18:
                    self.dodge = 18
                else:
                    self.dodge += item.points
            del self.inventory[item_index_to_use]
        else:
            print("You are out of items.")
    
    def miss_me(self):
        self.dodging = False
        dodge_chance = random.randint(1, 20)
        if dodge_chance <= self.dodge:
            self.dodging = True
            print(f"The attack missed {self.name}")
        return self.dodging

    def perception_check(self, level):
        self.perception_state = False
        perception_chance = random.randint(1, 20)
        level *= 10
        if self.perception > (perception_chance//level):
            self.perception_state = True
        return self.perception_state

    def motion_of_attack(self, opposite):
        if opposite.armor > 0:
            armor_counter = opposite.armor
            power_counter = 0
            while power_counter < self.power:
                if opposite.armor > 0:
                    opposite.armor -= 1
                    armor_counter -= 1
                    power_counter += 1
                else:
                    break
            temp_power = self.power - power_counter
            opposite.health -= temp_power
        else:
            opposite.health -= self.power
        return opposite.armor and opposite.health

class Hero(Character):
    def critical(self):
        self.power = 5
        crit_chance = random.randint(1, 5)
        if crit_chance == 1:
            print(f"You got a critical hit!\nYou do double damage!")
            self.power = 2 * self.power
        else:
            self.power = self.power
    def ability(self, opponent):
        pass

class Medic(Character):
    def ability(self, opponent):
        heal_chance = random.randint(1, 5)
        if heal_chance != 1:
            print(f"\n{self.name} found a health pack\nRecovered 2 health points")
            self.health += 2

class Goblin(Character):
    def ability(self, opponent):
        pass

class Zombie(Character):
    def ability(self, opponent):
        if self.health < 1:
            self.health = 1
            print(f"\nThe {self.name} still seems to be alive!")
        return self.health

class Shadow(Character):
    def ability(self, opponent):
        pass

class Mirror(Character):
    def ability(self, opponent):
        reflect_chance = random.randint(1, 5)
        if reflect_chance != 5:
            self.motion_of_attack(opponent)
            print(f"{self.name} reflected back some of the damage!")
            print(f"{self.name} does {int((opponent.power)/2)} damage to the {opponent.name}.\n")

class Static(Character):
    charger = 1
    def ability(self, opposite):
        self.charge = False
        if self.charger == 2:
            print(f"{self.name} releases a burst of electricity!")
            self.power = 2
            opposite.health -= 3
            if opposite.armor > 0:
                print(f"The electricity went through {opposite.name}'s armor!")
            print(f"{self.name} does 3 damage to the {opposite.name}.\n")
            self.charger = 1
        else:
            print(f"{self.name} is building energy!")
            self.charger +=1
        return self.charger

class Store:
    def __init__(self, name):
        self.name = name
        self.store_inventory = []
    def add_Items(self, name, quality, points, cost):
        newItem = Item(name, quality, points, cost)
        self.store_inventory.append(newItem)
    def buy_from_store_inventory(self, player):
        print(self.name)
        number = 1
        for item in self.store_inventory:
            print(f"{number}: {item.name} - {item.points} {item.quality} points - {item.cost} coins")
            number += 1
        self.store_inventory.append(f"{number}: exit")
        print(f"{number}: exit")
        self.store_inventory.pop()
        print(f"You have {player.money} coins.")
        buy_item_index = int(input("What item would you like to buy: ")) - 1
        if buy_item_index < len(self.store_inventory):
            item = self.store_inventory[buy_item_index]
            if player.money >= item.cost:
                player.money -= item.cost
                player.inventory.append(item)
                print(f"You bought {item.name}!\nYou now have {player.money} coins!\n")
            else:
                print("You do not have enough money!\n")
        else:
            print("Exiting Store")

class Item(Store):
    def __init__(self, name, quality, points, cost):
        self.name = name
        self.quality = quality
        self.points = points
        self.cost = cost
stone = Item("stone", "special", 2, 0)
store1 = Store("Old Man Store")
store1.add_Items("supertonic", "healing", 10, 3)
store1.add_Items("Regular Armor", "armor", 10, 10)
store1.add_Items("Evasion Potion", "dodge", 2, 5)
store2 = Store("Battle Store")
store2.add_Items("supertonic", "healing", 10, 3)
store2.add_Items("Regular Armor", "armor", 10, 10)
store2.add_Items("Evasion Potion", "dodge", 2, 5)

# name, health, power, dodge, perception, armor, money, inventory, bounty, player_status
goblin = Goblin("Goblin", 8, 4, 10, 20, 5, 5, [], 8, False)
hero = Hero("Hero", 10, 4, 5, 20, 5, 5, [], 6, False)
zombie = Zombie("Zombie", 1 , 1, 0, 0, 0, 5, [], 6, False)
medic = Medic("Medic", 11, 3, 5, 20, 3, 5, [], 6, False)
shadow = Shadow("Shadow", 1, 3, 15, 20, 0, 5, [], 15, False)
mirror = Mirror("Mirror", 10, 2, 10, 20, 5, 5, [], 6, False)
static = Static("Static", 9, 2, 8, 18, 5, 5, [], 6, False)

character_lst = [goblin, hero, medic, mirror, static, shadow]
hero_list = [hero, medic, mirror, static]
def character_list_printer(mode, list):
    if mode == 2:
        list.append(zombie)
        character_index = 0
        for character in list:
            print(f"{character_index+1}: {character.name} - Health = {character.health}, Armor = {character.armor}, Power = {character.power} & dodge = {int(((character.dodge)/20)*100)}% ")
            character_index += 1
    else:
        character_index = 0
        for character in list:
            print(f"{character_index+1}: {character.name} - Health = {character.health}, Armor = {character.armor},Power = {character.power} & dodge = {int(((character.dodge)/20)*100)}% ")
            character_index += 1

def character_select(name, character_list):
    picked = False
    while picked == False:
        if name == "player":
            name_input = int(input(">"))
            if name_input in range(1, len(character_list)+1):
                character = character_list[name_input-1]
                del character_list[name_input-1]
                picked == True
                return character
            else:
                print("Invalid input, try again.")
        elif name == "chosen":
            name_input = int(input(">"))
            character = character_list[name_input-1]
            del character_list[name_input-1]
            picked == True
            return character
        elif name != "random":
            index = character_list.index(name)
            character = character_list[index]
            picked == True
            return character
        elif name == "random":
            character_list
            index = random.randint(0, (len(character_list))-1)
            character = character_list[index]
            picked == True
            return character

def random_select(name):
    random_index = random.randint(0, len(character_lst)-1)
    random_character = character_lst[random_index]
    return random_character

def combat(player, opponent):
    while player.alive():
        player
        player.print_status()
        opponent.print_status()
        print()
        print("What do you want to do?")
        print(f"1. fight {opponent.name}")
        print("2. do nothing")
        print("3. flee")
        print("4. use item")
        print("> ", end=' ')
        raw_input = input()
        print()
        if raw_input == "1":
        # player attacks enemy
            player.attack(opponent)
        elif raw_input == "2":
            pass
        elif raw_input == "3":
            print("You ran from the battle!")
            return False
        elif raw_input == "4":
            player.use_item()
        elif raw_input == "aim for the head":
            if opponent == zombie:
                opponent.health = 0
                print("You decapitated the Zombie!")
            else:
                print("That doesn't work on this enemy")
        else:
            print(f"Invalid input {raw_input}")
        if opponent.health > 0:
            # enemy attacks player
            opponent.attack(player)
            print()
        if opponent.health <= 0:
            if opponent.player_status == True:
                print("Game Over!")
                break
            return True
        if player.health <= 0:
            print("Game Over!")
            break
    return False

def go_in_store(player, store):
    if store.name == "Old Man Store":
        print("Old Man: Do you want to buy some smuggled items?")
    else: 
        print("Do you want to stock up before next battle?")
    in_store = False
    in_store = yes_no()
    while in_store == True:
        store.buy_from_store_inventory(player)
        if store.name == "Old Man Store":
            print("Old Man: Do you want anything else?")
        else: 
            print("Do you want anything else?")
        stay = yes_no()
        if stay == True:
            in_store = True
        else:
            in_store = False
            if store.name == "Old Man Store":
                print("Old Man: If you ever want to buy something, I'll be here.\n")  
            else:
                print("Win next battle to make it back to the store!")

def yes_no():
    print("1: yes")
    print("2: no")
    yes_input = input(">")
    print()
    yes = False
    if yes_input == "1":
        yes = True
    elif yes_input =="2":
        pass
    else:
        print("Incorrect value give, value taken as \"no\"")
    return yes

def main():
    print("You open you're eyes to see an old man sitting on a bench.")
    print("You look around quickly and realize you're in a jail cell")
    print("Old Man: You've been knocked out for awhile.")
    print("Old Man: Who did you say you were again.")
    character_list_printer(3, hero_list)
    player = character_select("player", hero_list)
    player.player_status = True
    print()
    print(f"Old Man: Ah you're a {player.name}. I should've known.")
    print()
    player_position = 0
    area0 = False
    area1 = False
    area2 = False
    area3 = False
    area4_fight1 = False
    area4_fight2 = False
    while player.alive() and player_position < 6:
        while player_position == 0:
            if area0 == False:
                print("You are standing in the middle of the jail cell.")
                print("What would you like to look at?")
                print("1: Inspect the gate ahead of you.")
                print("2: Look to the old man on the bench on your left")
                print("3: Look at the wall on your right.")
                direction = input(">")
                print()
                if direction == "1":
                    print("The padlock keeping the gate the gate locked seems 100 years old and could break with a mild breeze.")
                    print("Perhaps something around you could break it.\n")
                    if stone in player.inventory:
                        print("You have a stone in your inventory, do you want to try to break the lock?")
                        yes_or_no = yes_no()
                        if yes_or_no == True:
                            print("You bash the lock 3 times until breaks.")
                            print("The gate swings open, you run forward to escape\n")
                            area0 = True
                            player_position += 1
                elif direction == "2":
                    print("The old man notices that you've been eyeballing him")
                    print("Old Man: What are you looking at?")
                    go_in_store(player, store1)
                elif direction == "3":
                    print("There's a piece of the stone wall sticking out")
                    print("Do you want to take it?")
                    yes_or_no = yes_no()
                    if yes_or_no == True:
                        player.inventory.append(stone)
                        print("Stone added to inventory!")
                else:
                    print(f"Invalid input {direction}")
            else:
                print("You are standing in the middle of the jail cell.")
                print(("1: Talk to the old man."))
                print("2: Move forward")
                leave_jail = input(">")
                print()
                if leave_jail == "1":
                    go_in_store(player, store1)
                else:
                    player_position += 1
        while player_position == 1:
            if area1 == False:
                enemy = goblin
                print("The guard heard all the commotion and running towards you!")
                print("Goblin Guard: What are you doing?")
                print("Goblin Guard: I just saw all of that from behind the desk!")
                print()
                win = combat(player, enemy)
                if win == True:
                    area1 = True
                    player_position +=1
                else:
                    player_position -= 1
            else:
                move = input("1: Move forward\n2: Move backward\n>")
                print()
                if move == "1":
                    player_position += 1
                    break
                else:
                    player_position -= 1
                    break
        while player_position == 2:
            print("You come to a fork in the hallway.\nYou can move left or right")
            print("1: Move left\n2: Move right\n3: Catch your breathe\n4: Go back")
            move = input(">")
            print()
            if move == "1":
                player_position += 2
                break
            elif move == "2": 
                player_position += 1
                break
            elif move == "3":
                print("You take a few deep breaths")
                if area2 == False:
                    player.health += 2 
                    print(f"{player.name} recovered 2 health points.")
                    area2 = True
                    player.print_status()
                print("You hear heavy grunting to your left,\nbut to the right seems eerily quiet.")
            elif move == "4":
                player_position -= 1
                break
            else:
                print("You did nothing")
        while player_position == 3:
            if area3 == False:
                enemy = shadow
                print(enemy.health)
                print("silence overcomes you!")
                print()
                win = combat(player, enemy)
                if win == True:
                    area3 = True
                else:
                    player_position -= 1
            else:
                print("You defeated the ghost of this area, it appears there's a plaque on the back wall.")
                move = input("1: Inspect the plaque\n2: Move backward\n>")
                print()
                if move == "1":
                    print("To defeat the Zombie \"aim for the head\"")
                    
                else:
                    player_position = 2
                    print("moved back to 2")
        while player_position == 4:
            enemy1 = character_select("random", hero_list) #random_select("enemy1")
            enemy2 = zombie
            while area4_fight1 == False:
                while enemy1.alive():
                    win = combat(player, enemy1)
                    if win == True:
                        area4_fight1 = True
                    else:
                        player_position -= 2
                    break
                break
            if area4_fight1 == True:
                while area4_fight2 == False:
                    while enemy2.alive():
                        win = combat(player, enemy2)
                        if win == True:
                            area4_fight2 = True
                            player_position += 1
                        else:
                            player_position -= 2
                        break
                    break
            break
        while player_position == 5:
            print("You see a light at the end of the hallway!")
            print("You run towards it as fast as you can!")
            print("You run out into the open air outside the jail!")
            print("You Win!\nGame Over!")
            player_position += 1
            break
    

def battle():    
    print("Choose your fighter!")
    mode = 1
    character_list_printer(mode, character_lst)
    player = character_select("player", character_lst)
    player.player_status = True
    wins = 0
    mode = 2
    while player.alive():
        print("Choose your next foe!")
        character_list_printer(mode, character_lst)
        enemy = character_select("chosen", character_lst)
        win = combat(player, enemy)
        if win == True:
            wins += 1
            if len(character_lst) > 0:
                print("Do you want to fight again?")
                yes_or_no = yes_no()
                if yes_or_no != True:
                    print("Thanks for playing!")
                    print(f"You won {wins} times!")
                    break
                else:
                    print(f"You have {wins} wins.")
                    go_in_store(player, store2)
                    mode += 1
            else:
                print("You defeated all the enemies!")
                print("Thanks for playing!")
                print(f"You won {wins} times!")
                break
        else:
            print("Thanks for playing!")
            print(f"You won {wins} times!")
mode = input("1: Story Mode\n2: Battle Mode\n>")
print()
if mode == "1":
    main()
elif mode == "2":
    battle()
else:
    print("I guess you don't want to play!")
    print("Thanks anyway!")


