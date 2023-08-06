import TARBSBeta
import random

TARBSBeta.debug = False
TARBSBeta.enable_logging = False
TARBSBeta.genlog()

TARBSBeta.use_default_output = True

defence = TARBSBeta.Shield("White Privilege", 1000)

weak_hp = TARBSBeta.Hp_potion("Weak HP Potion", 5)
med_hp = TARBSBeta.Hp_potion("Standard HP Potion", 10)
strong_hp = TARBSBeta.Hp_potion("Strong HP Potion", 15)
op_hp = TARBSBeta.Hp_potion("Overpowered HP Potion", 100)


drops = [defence, weak_hp, weak_hp, weak_hp, weak_hp, med_hp, strong_hp, med_hp, op_hp]

TARBSBeta.add_item(defence,1)

player = TARBSBeta.Player("Steve", 20, 5, 100)
zombie = TARBSBeta.Enemy("Dave", 20, 5, 9, drops)

potions = [weak_hp, op_hp]

for potion in potions:
    TARBSBeta.add_item(potion, 10)

bf = TARBSBeta.Battlefield("Desert", "A dry, sandy desert", player, zombie)
status = bf.start_battle()

player.equip_shield(defence)
