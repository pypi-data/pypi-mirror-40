# IMPORTS
from datetime import datetime
import logging
import os
from random import randint, choice
from textwrap import wrap
from enum import Enum
import create_issue
from tabulate import tabulate
import gc

version = "Beta 1.0"

# Get current time for logging
current_time = datetime.now().strftime("%m-%d-%Y - %H-%M-%S")

log_dir = "logs"

# Check if log folder exists
if not os.path.isdir(log_dir):
    os.makedirs(log_dir)

# Create log with timestamp (in log folder)
logfile = "{}/{}.log".format(log_dir, current_time)

# Debug Vars
debug = False
enable_logging = False


def issue(token, title, body):
    create_issue.issue(token, title, body)


def feature(token, title, body):
    create_issue.feature(token, title, body)

# Default output is the output that comes with the engine, example:
# Attack did 30 damage
# Zombie has 150 HP left


use_default_output = False


# Create default output command if default output is enabled
def default_output(text):
    if use_default_output:
        print(text)


# Output debugging
def debugout(text):
    # Check if debugging is enabled
    if debug:
        print("Debugger:" + text)


# Generate debugging log
def genlog():
    # Check if logging is enabled
    if enable_logging:
        # noinspection PyShadowingNames

        # Define the log
        logging.basicConfig(filename=logfile, level=logging.DEBUG)

        # Add header to log with timestamp
        logging.debug(" Run from {}".format(current_time))
    else:
        debugout("Note: Log will not be generated if `TARBSengine.enable_logging` is set to true.")


# Add text to log
def log(text):
    if enable_logging:
        # Write to the log
        logging.debug(" {}: {}".format(datetime.now().strftime("%I:%M:%S"), text))


# List of people who helped on way or another
def contributors():
    print("Developer: tman540")
    print("Developer: GriffinAustin (Armor)")
    print("Indirect help: solarc (border for `player.think()`")
    print("Get your name here!")
    print("Email me to contribute or if you would like to become an official beta tester!")
    print("stautonico@gmail.com ")


# The reason for using a custom function for getting user input
# is so logging the user input can be bundled into one function
def getinput(prompt):
    usr = input(prompt)
    debugout("User input: {}".format(usr))
    log("User input: {}".format(usr))
    return usr


# Note, when adding or subtracting from the inventory,
# the `item` is referring to the item (class) in the args
# Add item to play inventory
def add_item(item, amnt):
    item.amnt += amnt
    debugout("Item given: {} x {}".format(item.name, amnt))
    log("Item given: {} x {}".format(item.name, amnt))


# Subtract items from the players inventory
def remove_item(item, amnt):
    item.amnt -= amnt
    debugout("Removed: {} x {} from player".format(amnt, item.name))
    log("Removed: {} x {} from player".format(amnt, item.name))


class Player:
    def __init__(self, name, hp, minatk, maxatk):
        # Player vars
        self.name = name
        self.hp = hp
        self.maxhp = hp
        self.minAtk = minatk
        self.maxAtk = maxatk
        self.weapon_one = None
        self.weapon_one_atk = 0
        self.HEAD = None
        self.BODY = None
        self.LEG = None
        self.HAND = None
        self.FOOT = None
        self.armor_def = 0
        self.shield = None
        self.shield_protect = 0
        self.level = 0

    def levelup(self):
        self.level += 1
        default_output("Level Up! Current Level: {}".format(self.level))
        debugout("Player leveled up to {}".format(self.level))
        log("Player leveled up to {}".format(self.level))

    def lower_level(self, amnt):
        self.level -= amnt
        if self.level < 0:
            self.level = 0
        debugout("Player leveled lowered {} levels to {}".format(amnt, self.level))
        log("Player leveled lowered {} levels to {}".format(amnt, self.level))

    # Attack function (used in the battle loop)
    def atk(self, opponent):
        # Generate an attack number between the min and max attack
        atk = randint(self.minAtk, self.maxAtk)
        # Calc the total attack by adding the atk and the extra attack damage dealt by the equipped weapon
        total_atk = atk + self.weapon_one_atk
        opponent.hp -= total_atk
        default_output("{} did {} damage, {} has {} HP remaining".format(
            self.name, total_atk, opponent.name, opponent.hp))
        debugout("Player attacked {}. Attack did {} damage. {} has {} HP remaining".format(
            opponent.name, total_atk, opponent.name, opponent.hp))
        log("Player attacked {}. Attack did {} damage. {} has {} HP remaining".format(
            opponent.name, total_atk, opponent.name, opponent.hp))

    # Note, just like the items, when equipping armor or weapons
    # the `armor` or `weapon` in the args refers to the class (weapon, or armor)

    def equip_armor(self, armor):
        """
        Armor types:
        1- Helmet
        2- Chestplate
        3- Leg
        4- Gloves
        5- Shoe/Boot
        """

        # Check if the armor exists
        if armor.amnt > 0:
            # Add extra defence
            self.armor_def += armor.defense
            # Take away the armor
            armor.amnt -= 1

            # Check armor type (HEAD)
            if armor.type == 1:
                # Set the armor
                self.HEAD = armor
                debugout("Equipped {} in head slot".format(armor.name))
                log("Equipped {} in head slot".format(armor.name))

            # Check armor type (BODY)
            elif armor.type == 2:
                # Set the armor
                self.BODY = armor
                debugout("Equipped {} in body slot".format(armor.name))
                log("Equipped {} in body slot".format(armor.name))

            # Check armor type (LEG)
            elif armor.type == 3:
                # Set the armor
                self.LEG = armor
                debugout("Equipped {} in leg slot".format(armor.name))
                log("Equipped {} in leg slot".format(armor.name))

            # Check armor type (HAND)
            elif armor.type == 4:
                # Set the armor
                self.HAND = armor
                debugout("Equipped {} in hand slot".format(armor.name))
                log("Equipped {} in hand slot".format(armor.name))

            # Check armor type (FOOT)
            elif armor.type == 5:
                # Set the armor
                self.FOOT = armor
                debugout("Equipped {} in foot slot".format(armor.name))
                log("Equipped {} in foot slot".format(armor.name))

            default_output("Equipped: {}".format(armor.name))

    def unequip_armor(self, armor):
        """
        Armor types:
        1- Helmet
        2- Chestplate
        3- Leg
        4- Gloves
        5- Shoe/Boot
        """
        if armor:
            if armor.type == 1:
                # Remove the armor from the player
                self.HEAD = None
                # Add the armor back to the "inventory"
                armor.amnt += 1
                # Subtract the defence
                self.armor_def -= armor.defense
                debugout("Unequipped {} from head slot".format(armor.name))
                log("Unequipped {} from head slot".format(armor.name))

            elif armor.type == 2:
                self.BODY = None
                armor.amnt += 1
                self.armor_def -= armor.defense
                debugout("Unequipped {} from body slot".format(armor.name))
                log("Unequipped {} from body slot".format(armor.name))

            elif armor.type == 3:
                self.LEG = None
                armor.amnt += 1
                self.armor_def -= armor.defense
                debugout("Unequipped {} from leg slot".format(armor.name))
                log("Unequipped {} from leg slot".format(armor.name))

            elif armor.type == 4:
                self.HAND = None
                armor.amnt += 1
                self.armor_def -= armor.defense
                debugout("Unequipped {} from hand slot".format(armor.name))
                log("Unequipped {} from hand slot".format(armor.name))

            elif armor.type == 5:
                self.FOOT = None
                armor.amnt += 1
                self.armor_def -= armor.defense
                debugout("Unequipped {} from foot slot".format(armor.name))
                log("Unequipped {} from foot slot".format(armor.name))

            default_output("Unequipped: {}".format(armor.name))
        else:
            default_output("You have no armor equipped!")
            debugout("Player tried to unequip {}, they had nothing equipped.".format(armor.name))
            log("Player tried to unequip {}, they had nothing equipped.".format(armor.name))

    def equip_weapon(self, weapon):
        # Check if the weapon exists
        if weapon.amnt > 0:
            # Give the player the weapon
            self.weapon_one = weapon
            # Add the attack to the users first weapon slot
            self.weapon_one_atk = weapon.atk
            debugout("Equipped weapon: {}, Damage: {}".format(weapon.name, weapon.atk))
            log("Equipped weapon: {}, Damage: {}".format(weapon.name, weapon.atk))
            default_output("Equipped weapon: {}".format(weapon.name))
            # Remove the sword from the inventory
            weapon.amnt -= 1
        else:
            default_output("You don't have any!")
            debugout("Player tried to equip {}, they didn't have any.".format(weapon.name))
            log("Player tried to equip {}, they didn't have any.".format(weapon.name))

    def equip_shield(self, shield):
        if shield.amnt > 0:
            self.shield = shield.name
            self.shield_protect = shield.defense
            debugout("Equipped shield: {}, Damage reduction: {}".format(shield.name, shield.defense))
            log("Equipped shield: {}, Damage reduction: {}".format(shield.name, shield.defense))
            default_output("Equipped shield: {}".format(shield.name))
            shield.amnt -= 1
        else:
            default_output("You don't have any!")
            debugout("Player tried to equip {}, they didn't have any.".format(shield.name))
            log("Player tried to equip {}, they didn't have any.".format(shield.name))

    def unequip_weapon(self, weapon):
        # Check if the user has a weapon equipped
        if self.weapon_one:
            # Remove the weapon
            Player.weapon_one = None
            # Remove the extra attack
            Player.weapon_one_atk = 0
            # Add one to the inventory
            weapon.amnt += 1
            debugout("{} unequipped.".format(weapon.name))
            log("{} unequipped.".format(weapon.name))
            default_output("Unequipped weapon: {}".format(weapon.name))
        else:
            default_output("You don't have any weapons equipped")
            debugout("Player tried to unequip {}, they had nothing equipped.".format(weapon.name))
            log("Player tried to unequip {}, they had nothing equipped.".format(weapon.name))

    def unequip_shield(self, shield):
        if self.shield:
            Player.shield = None
            Player.shield_protect = 0
            shield.amnt += 1
            debugout("{} unequipped.".format(shield.name))
            log("{} unequipped.".format(shield.name))
            default_output("Unequipped shield: {}".format(shield.name))
        else:
            default_output("You don't have any armor equipped")
            debugout("Player tried to unequip {}, they had nothing equipped.".format(shield.name))
            log("Player tried to unequip {}, they had nothing equipped.".format(shield.name))

    def use_hp_potion(self, hp_potion):
        # Make sure the user's health isn't already at max
        if self.hp >= self.maxhp:
            default_output("HP is already at max!")
            debugout("HP already at max!")
            log("User tried to use {}, HP already at max!".format(hp_potion.name))
        else:
            # Increase the user's hp
            self.hp += hp_potion.hp
            # check if it went over max
            if self.hp > self.maxhp:
                # lower it
                self.hp = self.maxhp
            default_output("{} health restored, current health: {}".format(hp_potion.hp, self.hp))
            debugout("{} health restored, current health: {}".format(hp_potion.hp, self.hp))
            log("{} health restored, current health: {}".format(hp_potion.hp, self.hp))

    # Display dialogue
    def say(self, text):
        print("{}: {}".format(self.name, text))
        log("{}: {}".format(self.name, text))

    # Thanks solarc
    # Display dialogue that the user doesn't speak out loud
    # noinspection PyMethodMayBeStatic
    def think(self, thought):
        print('+-' + '-' * 26 + '-+')

        for line in wrap(thought, 26):
            print('| {0:^{1}} |'.format(line, 26))

        print('+-' + '-' * 26 + '-+')
        log("Player thought: {}".format(thought))

    # Open a lootbox with specified loot (in list form)
    def open_chest(self, loot):
        reward = choice(loot)
        default_output("Reward from chest: {}".format(reward.name))
        debugout("Reward from chest: {}".format(reward.name))
        log("Reward from chest: {}".format(reward.name))
        self.additem(reward, 1)
        
    def kill(self, deathmessage, *endgame):
        print(deathmessage)
        log("Player died: {}".format(deathmessage))
        # Reset the health to max
        self.hp = self.maxhp
        # Decides if the game should exit at death
        if endgame:
            log("Game ended")
            exit()
        else:
            log("Game didn't end on player death")


class Enemy:
    def __init__(self, name, hp, minatk, maxatk, drops):
        self.name = name
        self.hp = hp
        self.minAtk = minatk
        self.maxAtk = maxatk
        self.drops = drops

    def atk(self, opponent):
        # Generate a random number between min and max attack
        atk = randint(self.minAtk, self.maxAtk)
        # Calculate the total attack (subtract the
        total_atk = atk - opponent.shield_protect - opponent.armor_def
        # Because of the shield, if the attack is going to do negative damage (heal the enemy) just make it do 0 damage
        if total_atk < 0:
            total_atk = 0
        # Subtract health from what enemy is attacking
        opponent.hp -= total_atk
        default_output(
            "{} did {} damage, {} has {} HP remaining".format(self.name, total_atk, opponent.name, opponent.hp))
        debugout("Enemy attacked {}. Attack did {} damage. {} has {} HP remaining".format(
            opponent.name, total_atk, opponent.name, opponent.hp))
        log("Enemy attacked {}. Attack did {} damage. {} has {} HP remaining".format(
            opponent.name, total_atk, opponent.name, opponent.hp))

    # Make the enemy speak (more functionality planned)
    def say(self, text):
        print("{}: {}".format(self.name, text))
        log("{}: {}".format(self.name, text))


# Non-Player Character
class NPC:
    def __init__(self, name):
        self.name = name

    def talkto(self, text, *name):
        # If name is set to true
        if name:
            print("{}: {}".format(self.name, text))
            log("{}: {}".format(self.name, text))
        else:
            print("{}".format(text))
            log("NPC: {}".format(text))


class Weapon:
    def __init__(self, name, atk):
        self.amnt = 0
        self.name = name
        self.atk = atk


class Hp_potion:
    def __init__(self, name, hp):
        self.amnt = 0
        self.name = name
        self.hp = hp


class Armor:
    # Define armor types
    class ArmorType(Enum):
        HEAD = 1
        BODY = 2
        LEG = 3
        HAND = 4
        FOOT = 5

    def __init__(self, name, defense, atype):
        self.name = name
        self.defense = defense
        self.amnt = 0
        # self.weight = weight (unused, not yet implemented)

        # Instance of `ArmorType` must be created first, then set to the value of ArmorType.
        # Set armor to the armor type (args)
        self.type = self.ArmorType(atype)
        self.type = self.type.value


class Shield:
    def __init__(self, name, defense):
        self.amnt = 0
        self.name = name
        self.defense = defense


class Quest:
    def __init__(self, name, reward):
        self.name = name
        self.reward = reward
        self.completed = False
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)
        debugout("Task: {} added to quest {}".format(task, self.name))
        log("Task: {} added to quest {}".format(task, self.name))

    def complete_task(self, task):
        self.tasks.remove(task)
        debugout("Task: {} completed in quest {}".format(task, self.name))
        log("Task: {} completed in quest {}".format(task, self.name))
        if not self.tasks:
            print("Quest completed!")
            for item in self.reward:
                add_item(item, 1)
            self.completed = True


class Battlefield:
    def __init__(self, name, description, player, enemy):
        self.name = name
        self.description = description
        self.player = player
        self.enemy = enemy
        self.battle = False
        self.winner = None
        self.player_moves = [[1, "Attack", "Perform a basic attack"], [2, "Use health potion", "Consume an HP potion to regenerate health"]]

    def start_battle(self):
        battle = True
        players_turn = True
        log("Battle started with {}".format(self.enemy.name))
        debugout("Debugger: Battle started with {}".format(self.enemy.name))
        while battle:
            while players_turn:
                # Players turn
                print(tabulate(self.player_moves))
                player_action = input("Select an action: ")
                try:
                    player_action = int(player_action)
                    if player_action == 1:
                        self.player.atk(self.enemy)
                        players_turn = False
                    elif player_action == 2:
                        potions = []
                        potions_name = []
                        count = 0
                        for obj in gc.get_objects():
                            if isinstance(obj, Hp_potion):
                                if obj.amnt <= 0:
                                    pass
                                else:
                                    count += 1
                                    potions.append([count, obj])
                                    potions_name.append([count, obj.name])
                        print(tabulate(potions_name))
                        player_potion_option = input("Select a potion to use: ")
                        try:
                            player_potion_option = int(player_potion_option)
                            self.player.use_hp_potion(potions[player_potion_option][1])
                            players_turn = False
                        except ValueError:
                            print(player_potion_option, " isn't a valid potion")
                except ValueError:
                    print(player_action, " is an invalid input, please enter a valid option.")

                if self.enemy.hp <= 0:
                    self.winner = "player"
                    log("Player defeated player")
                    debugout("Debugger: Player defeated player")
                    break

            # Enemies turn
            self.enemy.atk(self.player)
            players_turn = True
            if self.player.hp <= 0:
                self.winner = "enemy"
                log("Enemy defeated player")
                debugout("Debugger: Enemy defeated player")
                break

        if self.winner == "enemy":
            self.player.kill("You were slain by " + self.enemy.name)
            return False

        else:
            print(self.enemy.name, "died!")
            if len(self.enemy.drops) > 0:
                print(self.enemy.name, "dropped: ")
                drops = []
                count = 0
                for item in self.enemy.drops:
                    count += 1
                    drops.append([count, item.name])
                    add_item(item, 1)
                print(tabulate(drops))
            else:
                print(self.enemy.name,  " dropped nothing!")
