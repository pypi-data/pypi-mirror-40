import TARBSengine
import random

TARBSengine.debug = True
TARBSengine.enable_logging = True
TARBSengine.genlog()

player = TARBSengine.Player("Steve", 20, 20, 5, 10)
zombie = TARBSengine.Enemy("Dave", 20, 5, 9)

desert = TARBSengine.Battlefield("Desert", "A dry, hot, generic desert", player, zombie)
