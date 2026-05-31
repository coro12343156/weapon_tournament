
# 画像、フォント、音声の変数を宣言するpyファイル

import os
import pygame


game_folder = os.path.dirname(__file__)
image_folder = os.path.join(game_folder, "images")
font_folder = os.path.join(game_folder, "fonts")
audio_folder = os.path.join(os.path.dirname(__file__),"audio")

icon = pygame.image.load(os.path.join(image_folder, "icon.png"))
pygame.display.set_icon(icon)

font  = pygame.font.Font(os.path.join(font_folder, "x12y16pxMaruMonica.ttf"), 32)
font2 = pygame.font.Font(os.path.join(font_folder, "x12y16pxMaruMonica.ttf"), 24)

iron_sword = pygame.image.load(os.path.join(image_folder, "iron_sword.png"))
iron_axe = pygame.image.load(os.path.join(image_folder, "iron_axe.png"))
book = pygame.image.load(os.path.join(image_folder, "knowledge_book.png"))
lava_bucket = pygame.image.load(os.path.join(image_folder, "lava_bucket.png"))
iron_spear = pygame.image.load(os.path.join(image_folder, "iron_spear_in_hand.png"))
darkness = pygame.image.load(os.path.join(image_folder, "darkness.png"))
timer = pygame.image.load(os.path.join(image_folder, "clock_01.png"))
mace = pygame.image.load(os.path.join(image_folder, "mace.png"))
trident = pygame.image.load(os.path.join(image_folder, "trident.png"))
tfish = pygame.image.load(os.path.join(image_folder, "tropical_fish.png"))
iron_chain = pygame.image.load(os.path.join(image_folder, "iron_chain.png"))
brick = pygame.image.load(os.path.join(image_folder, "brick.png"))
cod = pygame.image.load(os.path.join(image_folder, "cod.png"))
bow = pygame.image.load(os.path.join(image_folder, "bow.png"))
cbow = pygame.image.load(os.path.join(image_folder, "crossbow.png"))
tnt = pygame.image.load(os.path.join(image_folder, "tnt.png"))
pickaxe = pygame.image.load(os.path.join(image_folder, "pickaxe.png"))
anvil = pygame.image.load(os.path.join(image_folder, "anvil.png"))
minecart = pygame.image.load(os.path.join(image_folder, "minecart.png"))
lead = pygame.image.load(os.path.join(image_folder, "lead.png"))
end_crystal = pygame.image.load(os.path.join(image_folder, "end_crystal.png"))
beacon = pygame.image.load(os.path.join(image_folder, "beacon.png"))
beacon.set_colorkey((255, 255, 255))
dye = pygame.image.load(os.path.join(image_folder, "dye.png"))
hoe = pygame.image.load(os.path.join(image_folder, "hoe.png"))
bundle = pygame.image.load(os.path.join(image_folder, "bundle.png"))
bundleopen = pygame.image.load(os.path.join(image_folder, "bundleopen.png"))
ns = pygame.image.load(os.path.join(image_folder, "nether_star.png"))
pufferfish = pygame.image.load(os.path.join(image_folder, "pufferfish.png"))
elytra = pygame.image.load(os.path.join(image_folder, "elytra.png"))
elytrab = pygame.image.load(os.path.join(image_folder, "elytrab.png"))
egg = pygame.image.load(os.path.join(image_folder, "egg.png"))

arrow = pygame.image.load(os.path.join(image_folder, "arrow.png"))
barrier = pygame.image.load(os.path.join(image_folder, "barrier.png"))
potion = pygame.image.load(os.path.join(image_folder, "potion.png"))

gold = pygame.image.load(os.path.join(image_folder, "gold.png"))
diamond = pygame.image.load(os.path.join(image_folder, "diamond.png"))