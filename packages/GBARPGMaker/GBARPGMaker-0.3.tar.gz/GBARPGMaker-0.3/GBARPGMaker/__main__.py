from GBARPGMaker import GBARPGMaker
import sys

sys.path.append("./")

import config

grm = GBARPGMaker(config.tilemap_path, config.hero_image_path)
grm.make_game()
