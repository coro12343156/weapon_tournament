		# 0 - Strs2
		# 1 - sword
		# 2 - axe
		# 3 - book
		# 4 - lava
		# 5 - spear
		# 6 - dark
		# 7 - slow
		# 8 - barehand
		# 9 - mace
		# 10- trident
		# 11- tropical
		# 12- chain
		# 13- flail
		# 14- dupli
		# 15- cod
		# 16- bow
		# 17- crossbow
		# 18- tnt
		# 19- pickaxe
		# 20- anvil
		# 21- minecart
		# 22- barrier
		# 23- lead
		# 24- beacon
		# 25- dye
		# 26- potion
		# 27- hoe
		# 28- arrow
		# 29- bundle
		# 30- netherstar
		# 31- pufferfish
		# 32- elytra
		# 33- egg

import pygame
import random
import os
import math
from typing import Union
from string import Template
import unicodedata
from copy import deepcopy

def sign(x):
	if x < 0: return -1
	elif x == 0: return 0
	else: return 1

def get_aligned_center(text, y):
	return text.get_rect(center=(width//2, y))

def get_aligned_x(text):
	return text.get_rect(center=(width//2, 0)).x

def draw(text, x=-1, y=0, size=64, tremor=0, color=[255, 255, 255]):
	if x == -1:
		letter_x = get_aligned_x(pygame.font.Font(os.path.join(game_folder, "x12y16pxMaruMonica.ttf"), size).render(text, True, WHITE))
	else:
		letter_x = x
	letter_y = y - 12
	green_flag = 0
	ffont = pygame.font.Font(os.path.join(game_folder, "x12y16pxMaruMonica.ttf"), size)
	for i, s in enumerate(text):
		if s != "!":
			s_render = ffont.render(s, True, color)
			screen.blit(s_render, (letter_x + random.randint(-tremor, tremor), letter_y + random.randint(-tremor, tremor)))

			letter_x += 12 * size / 32
		elif s == "!":
			green_flag = 1 - green_flag

class Player:
	def __init__(self, x, y, color, type=3, team=-1, super=0, hp=100, small=0, mul=1, mul2=1):
		self.x = x
		self.y = y
		angle = random.random()*math.pi
		self.vx = math.cos(angle) * 6
		if abs(self.vx) <= 0.5: self.vx += 0.5
		self.vy = math.sin(angle) * 6
		self.color = color
		self.size = 32 - small * 8
		self.health = hp + super * 400

		self.super = super

		self.alive = 1

		self.stun = 0
		self.fire = 0
		self.stop = 0
		self.joust = 0
		self.chained = 0
		self.bounce = 0
		self.falling = 0
		self.broken = False

		self.nomulti = 0

		self.damagebuffer = 0

		self.remain = [[-100, -100]] * 30

		self.yanking = []
		self.yankingt= 0
		self.yanked = 0

		self.team = team

		self.flail = [x, y]
		self.flailv= [0, 0]

		self.flail2 = [x, y]
		self.flailv2= [0, 0]

		self.type = type
		self.t = 0
		self.multi = mul
		self.multi2= mul2
		self.omul = 1
		self.omul2= 1
		self.poison1= 0
		self.poison2= 0

		self.open = False

		self.cooldown = 0

		self.show1 = ["Joust: ","Damage: ","Stun: ", "Multi x: ", "Fire: ", "Speed: ", "Damage %/Amount: ", "Interval: ", "Damage: ", "Damage: ", "Damage: ", "Life Steal: ", "Entangle: ", "Damage: ", "Until Duplicate: ", "Bounce: ", "Shots: ", "Damage: ", "Debri: ", "Until Break: ", "Damage: ", "Duration: ", "Made: ", "Duration: ", "Interval: ", "Damage: ", "Damage/Heal: ", "Interval: ", "Damage: ", "Item: ", "Damage: ", "Poison: ", "Damage: ", "Summon HP: "][self.type]
		# Step2_2

		self.show2 = 0
		self.show2o= 0

		self.show3 = ["", "", "frames", "%", "frames", "", "", "frames", "", "", "", "", "frames", "", "", "", "", "", "", "frames", "", "frames", "", "frames", "frames", "", "", "frames", "", "", "", "", "", ""][self.type]

		self.tick = 0

	def move(self):
		global players, particles, arrows, nowall, nowallt, blocks, WHITE, BLACK

		self.remain.pop()
		self.remain = [[self.x, self.y]] + self.remain

		self.tick += 1

		if self.stop > 0:
			self.stop -= 1
		elif self.alive == 0:
			pass
		else:
			if self.damagebuffer > 0:
				self.health -= self.damagebuffer
				self.damagebuffer = 0
				self.stop = 5
				self.stun = 5
				particles += [Particle(self.x + random.gauss(0, 5), self.y + random.gauss(0, 5), self.vx * 2 + random.gauss(0, 2), self.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]
			if self.chained == 0 and self.broken == False:
				self.x += self.vx
				if self.bounce > 0: self.x += self.vx * 0.5
			if abs(self.x - width/2) >= ROOMSIZE/2-self.size/1.3:
				if self.type == 19 or nowall == 0 or (nowall == 1 and (self.x - width/2) > 0) or (nowall == 2 and (self.x - width/2) < 0):
					self.vx *= -1
					self.x += self.vx
					self.x += sign(width/2 - self.x) * 2
				else:
					if random.random() <= 0.2: self.health -= 1
					particles += [Particle(self.x, self.y, 0, 0, 20, 1, -1)]
				self.joust = 0
				if self.yanked > 0 and not (self.type == 7 and 300 <= self.t):
					self.health -= int(math.sqrt(self.vx ** 2 + self.vy ** 2) // 3)
				if self.bounce > 0:
					self.bounce -= 1
					self.health -= 3
				if self.type == 19:
					if self.multi2 < 0:
						self.multi2 = 600
						nowall = 1 + ((self.x - width/2) > 0)
						nowallt = 250
						for i in range(51):
							particles += [Particle(width/2-ROOMSIZE/2+ROOMSIZE*((self.x - width/2)>0), height/2-ROOMSIZE/2+ROOMSIZE/50*i, random.gauss(0, 1), random.gauss(0, 1), random.randint(5, 15), 0.4 + random.random() * 0.6)]
			if abs(self.x - width/2) >= width/2 + 100 and self.type != 22:
				self.vx *= -1
				self.x += self.vx
				self.x += sign(width/2 - self.x) * 5
			
			for i in blocks:
				if abs(self.x - i.x) <= self.size // 2 + i.size // 2 and abs(self.y - i.y) <= self.size // 2 + i.size // 2 and self.type != 22:
					self.vx *= -1
					self.x += self.vx
					self.health -= 1 + (random.random() < 0.3)

			for i in players:
				if i == self:
					continue
				else:
					if self.yanking == [] and i.yanking == [] and pow(self.x - i.x, 2) + pow(self.y - i.y, 2) <= pow(self.size * 2, 2):
						self.direct_attack(i)
						if self.bounce > 0:
							self.bounce -= 1
							self.health -= 2

			if self.chained == 0:
				self.y += self.vy
				if self.bounce > 0: self.y += self.vy * 0.5
				if self.bounce == 0: self.vy += 0.1
			if abs(self.y - height/2) >= ROOMSIZE/2-self.size/1.3:
				self.vy *= -1
				self.y += self.vy
				self.y += sign(height/2 - self.y) * 2
				self.joust = 0
				if self.yanked > 0 and not (self.type == 7 and 300 <= self.t):
					self.health -= int(math.sqrt(self.vx ** 2 + self.vy ** 2) // 3)
				if self.bounce > 0:
					self.bounce -= 1
					self.health -= 2
				if self.falling > 0:
					self.falling = 0
					self.vy *= 0.4
					self.vx = random.gauss(0, 3)
				if self.vy < 0: self.broken = False
			
			for i in blocks:
				if abs(self.x - i.x) <= self.size // 2 + i.size // 2 and abs(self.y - i.y) <= self.size // 2 + i.size // 2 and self.type != 22:
					self.vy *= -1
					self.y += self.vy
					self.health -= 1 + (random.random() < 0.3)
			
			self.flail[0] += self.flailv[0]
			self.flail[1] += self.flailv[1]
			self.flailv[1] += 0.1
			
			self.flail2[0] += self.flailv2[0]
			self.flail2[1] += self.flailv2[1]
			self.flailv2[1] += 0.1

			for i in players:
				if i == self:
					continue
				else:
					if self.yanking == [] and i.yanking == [] and pow(self.x - i.x, 2) + pow(self.y - i.y, 2) <= pow(self.size * 2, 2):
						self.direct_attack(i)
						if self.bounce > 0:
							self.bounce -= 1
							self.health -= 2

			if self.nomulti > 0:
				self.omul = self.multi
				self.omul2= self.multi2
			if self.stun > 0: self.stun -= 1
			if self.cooldown > 0: self.cooldown -= 1
			if self.fire > 0:
				if self.fire % 12 == 0:
					self.health -= 1
					particles += [Particle(self.x, self.y, 0, 0, 20, 1, -1)]
				self.fire -= 1
			if self.chained > 0:
				if self.chained % 30 == 0:
					self.health -= 1
				self.chained -= 1
			if self.falling > 0:
				self.vy += 0.8
			if self.yankingt > 0:
				self.yankingt -= 1
				if self.yankingt == 0:
					for i in self.yanking:
						i.yanked = 0
					self.yanking = []

			if self.poison1 > 0:
				self.poison2 += self.poison1
				if self.poison2 >= 120:
					self.health -= 1
					self.poison2 -= 120

			for i in self.yanking:
				i.vx += (self.x - i.x) / 400
				i.vy += (self.y - i.y) / 400
				if i.alive: pygame.draw.line(screen, BLACK, (self.x, self.y), (i.x, i.y), 4)

			self.show2o = self.show2

			if self.type == 0:
				self.show2 = int(self.multi)
				angle = -math.atan2(self.vy, self.vx)
				self.t = angle
				for enemy in players:
					if self == enemy: continue
					for i in range(1, 2):
						p = (self.x + math.cos(angle) * 75 * i, self.y - math.sin(angle) * 75 * i)
						if abs(enemy.x - p[0]) <= enemy.size + 16 and abs(enemy.y - p[1]) <= enemy.size + 16:
							if self.cooldown == 0:
								self.attack(enemy)
#						pygame.draw.circle(screen, BLACK, p, 32)

			if self.type == 1:
				self.t += self.multi
				if self.super > 0:
					self.multi2 += 1
					if 150 > self.multi2 > 100:
						self.t += self.multi * 2
					elif self.multi2 > 150:
						self.multi2 = 0
				self.show2 = int(5 * self.multi)
				angle = math.radians(self.t * 3)
				for enemy in players:
					if self == enemy: continue
					for i in range(1, 12):
						p = (self.x + math.cos(angle) * 9 * i, self.y - math.sin(angle) * 9 * i)
						if abs(enemy.x - p[0]) <= enemy.size + 5 and abs(enemy.y - p[1]) <= enemy.size + 5:
							if self.cooldown == 0:
								self.attack(enemy)
#						pygame.draw.circle(screen, BLACK, p, 10)

			if self.type == 2:
				self.t += 1 + (self.multi-1) / 5
				self.show2 = int(50 * self.multi)
				angle = math.radians(self.t * 3)
				for enemy in players:
					if self == enemy: continue
					for i in range(1, 12):
						p = (self.x + math.cos(angle) * 8 * i, self.y - math.sin(angle) * 8 * i)
						if abs(enemy.x - p[0]) <= enemy.size + 5 and abs(enemy.y - p[1]) <= enemy.size + 5:
							if self.cooldown == 0:
								self.attack(enemy)
#						pygame.draw.circle(screen, BLACK, p, 10)

			if self.type == 3:
				self.t += 1
				self.show2 = int(100 / (self.multi - 0.15))
				angle = math.radians(self.t * 3)
				for enemy in players:
					if self == enemy: continue
					for i in range(1, 3):
						p = (self.x + math.cos(angle) * 32 * i, self.y - math.sin(angle) * 32 * i)
						if abs(enemy.x - p[0]) <= enemy.size + 16 and abs(enemy.y - p[1]) <= enemy.size + 16:
							if self.cooldown == 0:
								otype = self.type
								omulti = self.multi
								osuper = self.super
								self.type = enemy.type
								self.super = enemy.super
								self.multi = enemy.multi / (self.multi - 0.15)
								self.multi2 = enemy.multi2 / (self.multi - 0.15)
								self.attack(enemy)
								self.type = otype
								self.multi = omulti
								self.super = osuper
								self.multi -= 0.02
								self.cooldown = 15
							if enemy.falling > 0:
								enemy.vy *= -1
				for arrow in arrows:
					if arrow.owner == self.type: continue
					for i in range(1, 3):
						p = (self.x + math.cos(angle) * 32 * i, self.y - math.sin(angle) * 32 * i)
						if abs(arrow.x - p[0]) <= arrow.size // 2 + 16 and abs(arrow.y - p[1]) <= arrow.size // 2 + 16:
							arrow.vx *= -1
							arrow.vy *= -1
							arrow.dmg = int(arrow.dmg / (self.multi - 0.1))
							arrow.owner = self.type
#						pygame.draw.circle(screen, BLACK, p, 32)

			if self.type == 4:
				self.t += 1
				self.show2 = int(60 * self.multi)
				angle = math.radians(self.t * 3)
				for enemy in players:
					if self == enemy: continue
					for i in range(1, 2):
						p = (self.x + math.cos(angle) * 64 * i, self.y - math.sin(angle) * 64 * i)
						if abs(enemy.x - p[0]) <= enemy.size + 16 and abs(enemy.y - p[1]) <= enemy.size + 16:
							if self.cooldown == 0:
								self.attack(enemy)
#						pygame.draw.circle(screen, BLACK, p, 32)

			if self.type == 5:
				self.t += self.multi
				self.show2 = int(self.multi*10)/10
				for enemy in players:
					angle = math.radians(self.t * 3)
					if self == enemy: continue
					for j in range(0, 3):
						for i in range(16, 21):
							p = (self.x + math.cos(angle) * 8 * i, self.y - math.sin(angle) * 8 * i)
							if abs(enemy.x - p[0]) <= enemy.size + 3 and abs(enemy.y - p[1]) <= enemy.size + 3:
								if self.cooldown == 0:
									self.attack(enemy)
	#						pygame.draw.circle(screen, BLACK, p, 6)

			if self.type == 6:
				self.t += self.multi2 * 2
				self.show2 = int(self.multi*50)/10
				for enemy in players:
					angle = math.radians(self.t * 3)
					if self == enemy: continue
					for i in range(1, 2):
						p = (self.x + math.cos(angle) * 64 * i, self.y - math.sin(angle) * 64 * i)
						if abs(enemy.x - p[0]) <= enemy.size + 18 and abs(enemy.y - p[1]) <= enemy.size + 18:
							if self.cooldown == 0:
								self.attack(enemy)
#						pygame.draw.circle(screen, BLACK, p, 36)

			if self.type == 7:
				self.show2 = int(300 / self.multi / 0.8)
				if self.health > 0:
					if self.t <= 300:
						WHITE = (233, 233, 242)
						BLACK = (0, 0, 0)
						self.t += self.multi * 0.8
					else:
						WHITE = (233 // 3, 233 // 3, 242 // 3)
						BLACK = (233 // 2, 233 // 2, 242 // 2)
						self.t += (1 - (self.multi - 1) / 4) * 1.3
						for i in players:
							if self == i: continue
							i.stop = 5
						if self.t > 360 + 120:
							for i in players:
								i.stop = 0
							self.t -= 360 + 120
						
				angle = math.radians(self.t * 3)
				for enemy in players:
					if self == enemy: continue
					for i in range(1, 2):
						p = (self.x + math.cos(angle) * 48 * i, self.y - math.sin(angle) * 48 * i)
						if abs(enemy.x - p[0]) <= enemy.size + 16 and abs(enemy.y - p[1]) <= enemy.size + 16:
							if self.cooldown == 0:
								self.attack(enemy)
	#					pygame.draw.circle(screen, BLACK, p, 32)

			if self.type == 8:
				self.t += self.multi
				self.show2 = int(self.multi)
				for enemy in players:
					if self == enemy: continue
					if pow(self.x - enemy.x, 2) + pow(self.y - enemy.y, 2) <= pow(self.size + enemy.size + 4, 2):
						if self.cooldown == 0:
							self.attack(enemy)

			if self.type == 9:
				self.t += 1 + (self.multi - 1)/5
				self.multi += 0.018 * self.multi2
				self.show2 = int(self.multi + 1)
				if self.multi > 5 or self.multi < 1: self.multi -= 0.005
				angle = math.radians(self.t * 3)
				for enemy in players:
					if self == enemy: continue
					for i in range(3, 4):
						p = (self.x + math.cos(angle) * 36 * i, self.y - math.sin(angle) * 36 * i)
						if abs(enemy.x - p[0]) <= enemy.size + 16 and abs(enemy.y - p[1]) <= enemy.size + 16:
							if self.cooldown == 0:
								self.attack(enemy)
#						pygame.draw.circle(screen, BLACK, p, 32)

			if self.type == 10:
				self.show2 = int(self.multi + 1)
				if self.joust == 0:
					self.t += 1
					if self.t % 4 == 0:
						angle = math.radians(self.t * 3)
						for enemy in players:
							if self == enemy: continue
							for i in range(1, 20):
								p = (self.x + math.cos(angle) * 24 * i, self.y - math.sin(angle) * 24 * i)
								if abs(enemy.x - p[0]) <= enemy.size + 12 and abs(enemy.y - p[1]) <= enemy.size + 12:
									self.joust = 10
									self.t += 1
									angle = math.radians(self.t * 3)
									self.vx = math.cos(angle) * 16
									self.vy =-math.sin(angle) * 16
									break
#								pygame.draw.circle(screen, BLACK, p, 24)
				else:
					self.vy -= 0.1
					self.joust -= 1
					angle = math.radians(self.t * 3)
					for enemy in players:
						if self == enemy: continue
						for i in range(3, 4):
							p = (self.x + math.cos(angle) * 36 * i, self.y - math.sin(angle) * 36 * i)
							if abs(enemy.x - p[0]) <= enemy.size + 16 and abs(enemy.y - p[1]) <= enemy.size + 16:
								if self.cooldown == 0:
									self.attack(enemy)
									self.joust = 0
									self.vx *= 0.25
									self.vy *= 0.25
	#						pygame.draw.circle(screen, BLACK, p, 32)
					if self.joust < 1:
						self.vx *= 0.25
						self.vy *= 0.25

			if self.type == 11:
				self.t += 1 + self.multi / 8
				self.show2 = int(self.multi + 2)
				angle = math.radians(self.t * 3)
				for enemy in players:
					if self == enemy: continue
					for i in range(1, 2):
						p = (self.x + math.cos(angle) * 64 * i, self.y - math.sin(angle) * 64 * i)
						if abs(enemy.x - p[0]) <= enemy.size + 16 and abs(enemy.y - p[1]) <= enemy.size + 16:
							if self.cooldown == 0:
								self.attack(enemy)
#						pygame.draw.circle(screen, BLACK, p, 32)

			if self.type == 12:
				self.t += 1.5
				self.show2 = int(self.multi * 60)
				angle = math.radians(self.t * 3)
				for enemy in players:
					if self == enemy: continue
					for i in range(1, 11):
						p = (self.x + math.cos(angle) * 9 * i, self.y - math.sin(angle) * 9 * i)
						if abs(enemy.x - p[0]) <= enemy.size + 5 and abs(enemy.y - p[1]) <= enemy.size + 5:
							if self.cooldown == 0:
								self.attack(enemy)
#						pygame.draw.circle(screen, BLACK, p, 10)

			if self.type == 13:
				self.t += 1
				self.show2 = int(3 * self.multi)
				angle = math.radians(self.t * 3)
				self.flailv[0] += (self.x - self.flail[0]) / 120
				self.flailv[1] += (self.y - self.flail[1]) / 120
				if abs(self.flailv[0]) > 16: self.flailv[0] = 16 * sign(self.flailv[0])
				if abs(self.flailv[1]) > 16: self.flailv[1] = 16 * sign(self.flailv[1])
				for enemy in players:
					if self == enemy: continue
					if pow(self.flail[0] - enemy.x, 2) + pow(self.flail[1] - enemy.y, 2) <= pow(self.size + enemy.size + 4, 2):
						if self.cooldown == 0:
							self.attack(enemy)
				if self.super > 0:
					self.flailv2[0] += (self.flail[0] - self.flail2[0]) / 120
					self.flailv2[1] += (self.flail[1] - self.flail2[1]) / 120
					if abs(self.flailv2[0]) > 16: self.flailv2[0] = 16 * sign(self.flailv2[0])
					if abs(self.flailv2[1]) > 16: self.flailv2[1] = 16 * sign(self.flailv2[1])
					for enemy in players:
						if self == enemy: continue
						if pow(self.flail2[0] - enemy.x, 2) + pow(self.flail2[1] - enemy.y, 2) <= pow(self.size + enemy.size + 4, 2):
							if self.cooldown == 0:
								self.attack(enemy)

			if self.type == 14:
				self.t += 1
				self.show2 = int(600 - self.t % 600)
				if self.t % 600 == 0 and self.t != 0:
					players.append(Player(self.x + 1, self.y, self.color, self.type, self.team, self.super, self.health, (self.size < 32)))

			if self.type == 15:
				self.t += 1
				self.show2 = int(self.multi)
				angle = math.radians(self.t * 3)
				for enemy in players:
					if self == enemy: continue
					for i in range(1, 2):
						p = (self.x + math.cos(angle) * 64 * i, self.y - math.sin(angle) * 64 * i)
						if abs(enemy.x - p[0]) <= enemy.size + 16 and abs(enemy.y - p[1]) <= enemy.size + 16:
							if self.cooldown == 0:
								self.attack(enemy)

			if self.type == 16:
				self.t += 1
				self.show2 = int(self.multi)
				if self.stun == 0: self.multi2 += 1
				angle = math.radians(self.t * 2)
				if self.multi2 >= 35:
					for i in range(self.multi):
						offs = (-self.multi/2 + i) / 30
						arrows += [Arrow(self.x, self.y, math.cos(angle + offs) * 9, -math.sin(angle + offs) * 9, 1, self.type, self.team, 0)]
					self.multi2 -= 35

			if self.type == 17:
				self.t += 1
				self.show2 = int(self.multi)
				if self.stun == 0: self.multi2 += 1
				angle = math.radians(self.t * 2)
				if self.multi2 >= 55:
					arrows += [Arrow(self.x, self.y, math.cos(angle) * 9, -math.sin(angle) * 9, self.multi, self.type, self.team, 1)]
					self.multi2 -= 55

			if self.type == 18:
				self.t += 1
				self.show2 = int(self.multi)
				if self.stun == 0: self.multi2 += 1
				angle = math.radians(self.t * 2)
				if self.multi2 >= 100:
					arrows += [Arrow(self.x, self.y, random.gauss(0, 7), random.gauss(0, 7), 1, self.type, self.team, 0, 1) for i in range(self.multi)]
					self.multi += 1
					self.multi2 -= 100

			if self.type == 19:
				self.t += 1
				self.show2 = int(max(0, self.multi2))
				self.multi2 -= self.multi
				angle = math.radians(self.t * 3)
				for enemy in players:
					if self == enemy: continue
					for i in range(1, 2):
						p = (self.x + math.cos(angle) * 64 * i, self.y - math.sin(angle) * 64 * i)
						if abs(enemy.x - p[0]) <= enemy.size + 16 and abs(enemy.y - p[1]) <= enemy.size + 16:
							if self.cooldown == 0:
								self.attack(enemy)

			if self.type == 20:
				self.t += 1
				self.show2 = int(self.multi + 6)
				angle = math.radians(self.t)
				for enemy in players:
					if self == enemy: continue
					for i in range(0, 2):
						p = (self.x + math.cos(angle) * 64 * i, self.y - math.sin(angle) * 64 * i)
						if abs(enemy.x - p[0]) <= enemy.size + 24 and abs(enemy.y - p[1]) <= enemy.size + 24:
							if self.cooldown == 0 and self.falling > 0:
								self.attack(enemy)
#							if self.cooldown == 0 and i == 1:
#								self.vy = -6
#								enemy.health -= 2
#								enemy.vy = 2
#								self.cooldown = 10
#						pygame.draw.circle(screen, BLACK, p, 48)
					if abs(self.x - enemy.x) <= 28 and self.y < enemy.y and self.vy > -6 and self.cooldown <= 0:
						self.vx = enemy.vx / 3
						self.vy = 5
						self.falling = 1

			if self.type == 21:
				self.t += 1
				self.show2 = int(180 / (1 + self.multi / 5))
				if self.stun == 0: self.multi2 += 1 + self.multi / 5
				angle = math.radians(self.t)
				if self.multi2 >= 180:
					arrows += [Arrow(width + 100, self.y, -20, 0, 9, self.type, self.team, 0, 2)]
					self.multi2 -= 180

			if self.type == 22:
				self.t += 1
				self.show2 = int(self.multi - 1)
				angle = math.radians(self.t * 3)
				for enemy in players:
					if self == enemy: continue
					for i in range(1, 2):
						p = (self.x + math.cos(angle) * 64 * i, self.y - math.sin(angle) * 64 * i)
						if abs(enemy.x - p[0]) <= enemy.size + 16 and abs(enemy.y - p[1]) <= enemy.size + 16:
							if self.cooldown == 0:
								self.attack(enemy)
#						pygame.draw.circle(screen, BLACK, p, 32)

			if self.type == 23:
				self.t += 1
				self.show2 = int(self.multi * 60)
				angle = math.radians(self.t * 3)
				for enemy in players:
					if self == enemy: continue
					if enemy.yanked > 0: continue
					for i in range(1, 2):
						p = (self.x + math.cos(angle) * 64 * i, self.y - math.sin(angle) * 64 * i)
						if abs(enemy.x - p[0]) <= enemy.size + 16 and abs(enemy.y - p[1]) <= enemy.size + 16:
							if self.cooldown == 0:
								self.attack(enemy)
#						pygame.draw.circle(screen, BLACK, p, 32)

			if self.type == 24:
				self.t += 1
				self.show2 = int(15 / self.multi)
				self.multi2 += self.multi
				angle = math.radians(self.t * 2)
				for enemy in players:
					if self == enemy: continue
					for i in range(1, 35):
						p = (self.x + math.cos(angle) * 32 * i, self.y - math.sin(angle) * 32 * i)
						if abs(enemy.x - p[0]) <= enemy.size + 8 and abs(enemy.y - p[1]) <= enemy.size + 8:
							if self.multi2 > 15:
								self.attack(enemy)
								self.multi2 -= 15
				if self.multi2 > 15:
					self.multi2 -= 15
				pygame.draw.line(screen, BLACK, (self.x, self.y), (self.x + math.cos(angle) * 1200, self.y - math.sin(angle) * 1200), 18)
				pygame.draw.line(screen, WHITE, (self.x, self.y), (self.x + math.cos(angle) * 1200, self.y - math.sin(angle) * 1200), 14)
#						pygame.draw.circle(screen, BLACK, p, 16)

			if self.type == 25:
				self.t += 1
				self.show2 = int(self.multi + 2)
				angle = math.radians(self.t * 3)
				for enemy in players:
					if self == enemy: continue
					for i in range(1, 2):
						p = (self.x + math.cos(angle) * 64 * i, self.y - math.sin(angle) * 64 * i)
						if abs(enemy.x - p[0]) <= enemy.size + 16 and abs(enemy.y - p[1]) <= enemy.size + 16:
							if self.cooldown == 0:
								self.attack(enemy)
#						pygame.draw.circle(screen, BLACK, p, 32)

			if self.type == 26:
				self.t += 1
				self.show2 = int(self.multi + 2)
				angle = math.radians(self.t * 3)
				self.multi2 += 1
				if self.multi2 >= 100:
					arrows += [Arrow(self.x, self.y, random.gauss(0, 5), -7, int(self.multi + 2), self.type, self.team, 1, 3)]
					self.multi2 -= 100

			if self.type == 27:
				self.t += 1.5 + (self.multi - 0.1) / 2
				self.show2 = int(4 / self.multi)
				angle = math.radians(self.t * 2)
				for enemy in players:
					if self == enemy: continue
					for i in range(1, 2):
						p = (self.x + math.cos(angle) * 64 * i, self.y - math.sin(angle) * 64 * i)
						if abs(enemy.x - p[0]) <= enemy.size + 16 and abs(enemy.y - p[1]) <= enemy.size + 16:
							if self.cooldown == 0:
								self.attack(enemy)
#						pygame.draw.circle(screen, BLACK, p, 32)

			if self.type == 28:
				self.show2 = int(self.multi * 3)
				angle = -math.atan2(self.vy, self.vx)
				self.t = angle
				for enemy in players:
					if self == enemy: continue
					for i in range(1, 5):
						p = (self.x + math.cos(angle) * 25 * i, self.y - math.sin(angle) * 25 * i)
						if abs(enemy.x - p[0]) <= enemy.size + 6 and abs(enemy.y - p[1]) <= enemy.size + 6:
							if self.cooldown == 0:
								self.attack(enemy)
#						pygame.draw.circle(screen, BLACK, p, 12)

			if self.type == 29:
				self.t += 1
				self.show2 = int(self.multi + 5)
				if self.stun == 0 and self.open == False: self.multi2 += 1
				angle = math.radians(self.t)
				if self.multi2 >= 60:
					arrows += [Arrow(self.x, self.y, random.gauss(0, 5), random.gauss(0, 5), 2, self.type, self.team, 0, 100) for i in range(self.multi + 4)]
					arrows += [Arrow(self.x, self.y, random.gauss(0, 5), random.gauss(0, 5), 5, self.type, self.team, 0, 101) for i in range(2)]
					self.multi2 -= 60
					self.open = True
				if self.open == True:
					noitem = 3
					for i in arrows:
						if i.atype >= 100: noitem -= 1
					if noitem > 0:
						self.open = False
						self.multi += 3

			if self.type == 30:
				self.t += 1
				self.show2 = int(self.multi * 5 + 5)
				angle = math.radians(self.t * 3)
				for enemy in players:
					if self == enemy: continue
					for i in range(1, 2):
						p = (self.x + math.cos(angle) * 64 * i, self.y - math.sin(angle) * 64 * i)
						if abs(enemy.x - p[0]) <= enemy.size + 16 and abs(enemy.y - p[1]) <= enemy.size + 16:
							if self.cooldown == 0:
								self.attack(enemy)
#						pygame.draw.circle(screen, BLACK, p, 32)

			if self.type == 31:
				self.t += 1 + self.super * 0.5
				self.show2 = int(self.multi - 1)
				angle = math.radians(self.t * 3)
				for enemy in players:
					if self == enemy: continue
					for i in range(1, 2):
						p = (self.x + math.cos(angle) * 64 * i, self.y - math.sin(angle) * 64 * i)
						if abs(enemy.x - p[0]) <= enemy.size + 16 and abs(enemy.y - p[1]) <= enemy.size + 16:
							if self.cooldown == 0:
								self.attack(enemy)
#						pygame.draw.circle(screen, BLACK, p, 32)
				if self.super > 0:
					angle = math.radians(self.t * 3 + 180)
					for enemy in players:
						if self == enemy: continue
						for i in range(1, 2):
							p = (self.x + math.cos(angle) * 64 * i, self.y - math.sin(angle) * 64 * i)
							if abs(enemy.x - p[0]) <= enemy.size + 16 and abs(enemy.y - p[1]) <= enemy.size + 16:
								if self.cooldown == 0:
									self.attack(enemy)
#							pygame.draw.circle(screen, BLACK, p, 32)

			if self.type == 32:
				self.t += 1
				self.show2 = int(self.multi + 4)
				angle = -math.atan2(self.vy, self.vx)
				self.t = angle
				if self.broken == False:
					for enemy in players:
						if self == enemy: continue
						if pow(self.x - enemy.x, 2) + pow(self.y - enemy.y, 2) <= pow(self.size + enemy.size + 4, 2):
							if self.cooldown == 0:
								self.attack(enemy)

			if self.type == 33:
				self.t += 1.5
				self.show2 = int(self.multi + 2)
				angle = math.radians(self.t * 2)
				for enemy in players:
					if self == enemy: continue
					for i in range(1, 2):
						p = (self.x + math.cos(angle) * 64 * i, self.y - math.sin(angle) * 64 * i)
						if abs(enemy.x - p[0]) <= enemy.size + 16 and abs(enemy.y - p[1]) <= enemy.size + 16:
							if self.cooldown == 0:
								self.attack(enemy)
#						pygame.draw.circle(screen, BLACK, p, 32)

# Step3_1

			if self.nomulti > 0:
				self.multi = self.omul
				self.multi2 = self.omul2
				self.nomulti -= 1

		if self.health <= 0:
			self.x = -10000
			self.alive = 0
			if self.type == 14 and (players[0] == self or players[1] == self):
				for i in players:
					if i.type == 14: i.health = -1

	def direct_attack(self, i):
		global particles, players, colors
		if self.stun or (i.type == 8 and self.type != 14) or i.joust > 0: return
		if i.type == 32: return
		if self.type == 7 and i.stop:
			selfangle = math.atan2(self.y - i.y, self.x - i.x)
			ssp = math.sqrt(pow(self.vx, 2) + pow(self.vy, 2))
			self.vx = math.cos(selfangle) * ssp
			self.vy = math.sin(selfangle) * ssp
			self.x += self.vx * 2
			self.y += self.vy * 2
			i.damagebuffer += 4
			return
		if self.yanked > 0: return
		if self.team == i.team and self.team != -1 and self.type != 14: return
		if self.type == 8:
			if self.cooldown == 0: self.attack(i)
			return
		if self.type == 32 and self.broken == False:
			if self.cooldown == 0: self.attack(i)
			return
		if self.type == 20:
			if self.cooldown == 0 and self.falling > 0: self.attack(i)
			return
		if self.type == 14:
			if (i.type != 14 or self.team != i.team) and self.cooldown == 0:
				self.attack(i)
			else:
				selfangle = math.atan2(self.y - i.y, self.x - i.x)
				iangle = math.atan2(i.y - self.y, i.x - self.x)
				ssp = math.sqrt(pow(self.vx, 2) + pow(self.vy, 2))
				isp = math.sqrt(pow(i.vx, 2) + pow(i.vy, 2))
				self.vx = math.cos(selfangle) * isp
				self.vy = math.sin(selfangle) * isp
				i.vx = math.cos(iangle) * ssp
				i.vy = math.sin(iangle) * ssp
				i.x += i.vx
				i.y += i.vy
			return
		selfangle = math.atan2(self.y - i.y, self.x - i.x)
		iangle = math.atan2(i.y - self.y, i.x - self.x)
		ssp = math.sqrt(pow(self.vx, 2) + pow(self.vy, 2))
		isp = math.sqrt(pow(i.vx, 2) + pow(i.vy, 2))
		if i.stun == 0: self.health -= int(isp/3)
		i.health -= int(ssp/3)
		self.vx = math.cos(selfangle) * isp
		self.vy = math.sin(selfangle) * isp
		i.vx = math.cos(iangle) * ssp
		i.vy = math.sin(iangle) * ssp
		i.x += i.vx
		i.y += i.vy

	def attack(self, i):
		global particles, players, colors, blocks
		if self.stun or i.joust > 0 or i.falling > 0: return
		if self.team == i.team and self.team != -1 and self.type != 11: return
		if self.yanked > 0: return

		if i.type == 6:
			i.multi += 0.1

		if self.type == 0:
			i.health -= int(self.multi)
			iangle = math.atan2(i.y - self.y, i.x - self.x)
			isp = math.sqrt(pow(i.vx, 2) + pow(i.vy, 2))
			i.vx = math.cos(iangle) * isp
			i.vy = math.sin(iangle) * isp
			i.x += i.vx
			i.y += i.vy
			self.cooldown = 15
			self.multi += 1
			self.stop = 5
			i.stop = 5
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]

		if self.type == 1:
			i.health -= int(5 * self.multi)
			if 150 > self.multi2 > 100:
				i.health -= int(5 * self.multi)
				i.stun = 10
				self.stop = 15
				i.stop = 15
			iangle = math.atan2(i.y - self.y, i.x - self.x)
			isp = math.sqrt(pow(i.vx, 2) + pow(i.vy, 2))
			i.vx = math.cos(iangle) * isp
			i.vy = math.sin(iangle) * isp
			i.x += i.vx
			i.y += i.vy
			self.cooldown = 13
			self.multi += 0.2
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]

		if self.type == 2:
			i.health -= 6 + int(self.multi / 2)
			i.stun = int(50 * self.multi) + 5
			i.stop = 5
			iangle = math.atan2(i.y - self.y, i.x - self.x)
			isp = math.sqrt(pow(i.vx, 2) + pow(i.vy, 2))
			i.vx = math.cos(iangle) * isp
			i.vy = math.sin(iangle) * isp
			i.x += i.vx
			i.y += i.vy
			self.cooldown = 16
			self.multi += 0.4
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]

		if self.type == 3:
			i.health -= int(self.multi)
			iangle = math.atan2(i.y - self.y, i.x - self.x)
			isp = math.sqrt(pow(i.vx, 2) + pow(i.vy, 2))
			i.vx = math.cos(iangle) * isp
			i.vy = math.sin(iangle) * isp
			i.x += i.vx
			i.y += i.vy
			self.cooldown = 15
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]

		if self.type == 4:
			i.health -= 5
			i.fire = int(60 * self.multi)
			iangle = math.atan2(i.y - self.y, i.x - self.x)
			isp = math.sqrt(pow(i.vx, 2) + pow(i.vy, 2))
			i.vx = math.cos(iangle) * isp
			i.vy = math.sin(iangle) * isp
			i.x += i.vx
			i.y += i.vy
			self.cooldown = 10
			self.multi += 0.25
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]

		if self.type == 5:
			i.health -= 5
			iangle = math.atan2(i.y - self.y, i.x - self.x)
			isp = math.sqrt(pow(i.vx, 2) + pow(i.vy, 2))
			i.vx = math.cos(iangle) * isp
			i.vy = math.sin(iangle) * isp
			i.x += i.vx
			i.y += i.vy
			self.cooldown = 17
			self.multi += 0.15
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]

		if self.type == 6:
			if random.randint(1, 1000) <= self.multi*50:
				i.health -= int(self.multi*50/10)
				iangle = math.atan2(i.y - self.y, i.x - self.x)
				isp = math.sqrt(pow(i.vx, 2) + pow(i.vy, 2))
				i.vx = math.cos(iangle) * isp
				i.vy = math.sin(iangle) * isp
				i.x += i.vx
				i.y += i.vy
				self.cooldown = 15
				self.multi += 0.8
				self.stop = 20
				i.stop = 20
				particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]
			else:
				i.health -= 1
				iangle = math.atan2(i.y - self.y, i.x - self.x)
				isp = math.sqrt(pow(i.vx, 2) + pow(i.vy, 2))
				i.vx = math.cos(iangle) * isp
				i.vy = math.sin(iangle) * isp
				i.x += i.vx
				i.y += i.vy
				self.multi += 0.8
				self.cooldown = 11
				self.stop = 5
				i.stop = 5

		if self.type == 7:
			if 300 <= self.t:
				i.damagebuffer += 10
			else:
				i.health -= 3
			iangle = math.atan2(i.y - self.y, i.x - self.x)
			isp = math.sqrt(pow(i.vx, 2) + pow(i.vy, 2))
			i.vx = math.cos(iangle) * isp
			i.vy = math.sin(iangle) * isp
			i.x += i.vx
			i.y += i.vy
			self.cooldown = 10
			self.multi += 0.15
			if self.multi > 4.5: self.multi = 4.5
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]

		if self.type == 8:
			i.health -= int(self.multi)
			i.stop = int(2 * self.multi)
			self.stop = int(2 * self.multi)
			i.stun = 15
			iangle = math.atan2(i.y - self.y, i.x - self.x)
			isp = math.sqrt(pow(i.vx, 2) + pow(i.vy, 2))
			i.vx += math.cos(iangle) * isp
			i.vy += math.sin(iangle) * isp
			self.cooldown = 20
			if self.super > 0:
				self.stop = int(self.multi / 3)
				i.stop = int(self.multi / 2.5)
				i.stun = 20
				self.cooldown = 15
				self.vx *= 1.02
				self.vy *= 1.02
			self.multi += 1
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]

		if self.type == 9:
			i.health -= int(self.multi + 1)
			i.stop = int(2 * self.multi)
			self.stop = int(2 * self.multi)
			iangle = math.atan2(i.y - self.y, i.x - self.x)
			isp = math.sqrt(pow(i.vx, 2) + pow(i.vy, 2))
			i.vx += math.cos(iangle) * isp
			i.vy += math.sin(iangle) * isp
			self.cooldown = 30
			self.multi = 0.3
			self.multi2 += 0.15
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]

		if self.type == 10:
			i.health -= int(self.multi + 1)
			iangle = math.atan2(i.y - self.y, i.x - self.x)
			isp = math.sqrt(pow(i.vx, 2) + pow(i.vy, 2))
			i.vx += math.cos(iangle) * isp * 0.5
			i.vy += math.sin(iangle) * isp * 0.5
			self.cooldown = 15
			self.multi += 0.3
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]

		if self.type == 11:
			self.health += int(self.multi + 2)
			if self.team != i.team:
				i.health -= int(self.multi + 2)
				iangle = math.atan2(i.y - self.y, i.x - self.x)
				isp = math.sqrt(pow(i.vx, 2) + pow(i.vy, 2))
				i.vx = math.cos(iangle) * isp
				i.vy = math.sin(iangle) * isp
				i.x += i.vx
				i.y += i.vy
			else:
				i.health += int(self.multi + 2)
			self.cooldown = 14
			self.multi += 1
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]

		if self.type == 12:
			i.health -= 3 + (i.chained > 0) * 12
			i.stun += 8 + (i.chained > 0) * 10
			i.chained = int(self.multi * 60)
			iangle = math.atan2(i.y - self.y, i.x - self.x)
			isp = math.sqrt(pow(i.vx, 2) + pow(i.vy, 2))
			i.vx = math.cos(iangle) * isp
			i.vy = math.sin(iangle) * isp
			i.x += i.vx
			i.y += i.vy
			self.cooldown = 12
			self.multi += 0.6
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]

		if self.type == 13:
			i.health -= int(self.multi * 3)
			iangle = math.atan2(i.y - self.flail[1], i.x - self.flail[0])
			isp = math.sqrt(pow(i.vx, 2) + pow(i.vy, 2))
			i.vx = math.cos(iangle) * isp
			i.vy = math.sin(iangle) * isp
			i.x += i.vx
			i.y += i.vy
			self.cooldown = 10
			self.multi += 0.3
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]

		if self.type == 14:
			i.health -= 1
			iangle = math.atan2(i.y - self.y, i.x - self.x)
			isp = math.sqrt(pow(i.vx, 2) + pow(i.vy, 2))
			i.vx = math.cos(iangle) * isp
			i.vy = math.sin(iangle) * isp
			i.x += i.vx
			i.y += i.vy
			self.cooldown = 5
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]

		if self.type == 15:
			i.health -= 1
			i.bounce = int(self.multi)
			i.remain = [[-100, -100]] * 30
			iangle = math.atan2(i.y - self.y, i.x - self.x)
			isp = math.sqrt(pow(i.vx, 2) + pow(i.vy, 2))
			i.vx = math.cos(iangle) * isp
			i.vy = math.sin(iangle) * isp
			i.x += i.vx
			i.y += i.vy
			self.cooldown = 15
			self.multi += 1
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]

		if self.type == 16:
			i.health -= 1
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]

		if self.type == 17:
			i.health -= int(self.multi)
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]

		if self.type == 19:
			i.health -= 3
			iangle = math.atan2(i.y - self.y, i.x - self.x)
			isp = math.sqrt(pow(i.vx, 2) + pow(i.vy, 2))
			i.vx = math.cos(iangle) * isp
			i.vy = math.sin(iangle) * isp
			i.x += i.vx
			i.y += i.vy
			self.cooldown = 15
			self.multi += 0.1
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]

		if self.type == 20:
			i.health -= int(self.multi) + 6
			iangle = math.atan2(i.y - self.y, i.x - self.x)
			isp = math.sqrt(pow(i.vx, 2) + pow(i.vy, 2))
			i.vx = math.cos(iangle) * isp
			i.vy = math.sin(iangle) * isp
			i.x += i.vx
			i.y += i.vy
			self.multi += 2
			i.stun = 30
			self.falling = 0
			self.cooldown = 10
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]

		if self.type == 21:
			i.health -= 9
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]

		if self.type == 22:
			i.health -= 1
			iangle = math.atan2(i.y - self.y, i.x - self.x)
			isp = math.sqrt(pow(i.vx, 2) + pow(i.vy, 2))
			i.vx = math.cos(iangle) * isp
			i.vy = math.sin(iangle) * isp
			i.x += math.cos(iangle) * 32
			i.y += math.sin(iangle) * 32
			self.cooldown = 15
			self.multi += 1
			blocks += [Block(self.x, self.y, self.type)]
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]

		if self.type == 23:
			i.health -= 1
			self.cooldown = 15
			self.yanking += [i]
			self.yankingt+= int(self.multi * 60)
			self.multi += 0.3
			i.yanked = 1
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]

		if self.type == 24:
			i.health -= 1
			self.multi += 0.25
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(20)]

		if self.type == 25:
			i.health -= int(self.multi + 2)
			i.nomulti = 350
			iangle = math.atan2(i.y - self.y, i.x - self.x)
			isp = math.sqrt(pow(i.vx, 2) + pow(i.vy, 2))
			i.vx = math.cos(iangle) * isp
			i.vy = math.sin(iangle) * isp
			self.cooldown = 13
			self.multi += 1
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]

		if self.type == 26:
			i.health -= int(self.multi + 2) // 2
			self.health += int(self.multi + 2) // 2
			iangle = math.atan2(i.y - self.y, i.x - self.x)
			isp = math.sqrt(pow(i.vx, 2) + pow(i.vy, 2))
			i.vx = math.cos(iangle) * isp
			i.vy = math.sin(iangle) * isp
			self.cooldown = 15
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]

		if self.type == 27:
			i.health -= 3
			self.stop = 2
			i.stop = 2
			self.cooldown = int(4 / self.multi)
			self.multi += 0.02
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]

		if self.type == 28:
			i.health -= int(3 * self.multi)
			iangle = math.atan2(i.y - self.y, i.x - self.x)
			isp = math.sqrt(pow(i.vx, 2) + pow(i.vy, 2))
			i.vx = math.cos(iangle) * isp
			i.vy = math.sin(iangle) * isp
			i.x += i.vx
			i.y += i.vy
			self.cooldown = 15
			self.multi += 0.3
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]

		if self.type == 29:
			i.health -= 5 + int(self.multi * 2)
			iangle = math.atan2(i.y - self.y, i.x - self.x)
			isp = math.sqrt(pow(i.vx, 2) + pow(i.vy, 2))
			i.vx = math.cos(iangle) * isp
			i.vy = math.sin(iangle) * isp
			i.x += i.vx
			i.y += i.vy
			self.cooldown = 15
			self.multi += 1
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]

		if self.type == 30:
			i.health -= int(5 * self.multi + 5)
			self.health -= 3
			iangle = math.atan2(i.y - self.y, i.x - self.x)
			isp = math.sqrt(pow(i.vx, 2) + pow(i.vy, 2))
			i.vx = math.cos(iangle) * isp
			i.vy = math.sin(iangle) * isp
			i.x += i.vx
			i.y += i.vy
			self.cooldown = 13
			self.multi += 0.2
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]

		if self.type == 31:
			i.health -= 1
			i.poison1 += 1
			iangle = math.atan2(i.y - self.y, i.x - self.x)
			isp = math.sqrt(pow(i.vx, 2) + pow(i.vy, 2))
			i.vx = math.cos(iangle) * isp
			i.vy = math.sin(iangle) * isp
			i.x += i.vx
			i.y += i.vy
			self.cooldown = 15
			self.multi += 1
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]

		if self.type == 32:
			i.health -= int(self.multi + 4)
			i.stop = 8
			self.stop = 8
			self.broken = True
			i.stun = 15
			iangle = math.atan2(i.y - self.y, i.x - self.x)
			isp = math.sqrt(pow(i.vx, 2) + pow(i.vy, 2))
			i.vx += math.cos(iangle) * isp
			i.vy += math.sin(iangle) * isp
			self.cooldown = 25
			self.multi += 1.5
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]

		if self.type == 33:
			i.stop = 8
			self.stop = 8
			i.stun = 10
			iangle = math.atan2(i.y - self.y, i.x - self.x)
			isp = math.sqrt(pow(i.vx, 2) + pow(i.vy, 2))
			i.vx += math.cos(iangle) * isp
			i.vy += math.sin(iangle) * isp
			self.cooldown = 25
			players += [Player(self.x, self.y, [(colors[self.type][n]+colors[i.type][n])//2 for n in range(3)], i.type, self.team, i.super, int(self.multi + 2 - i.super * 400), 1, i.multi, i.multi2)]
			self.multi += 1
			particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]

# Step3_2

	def draw(self):
		global l, particles

		if self.type == 6:
			angle = self.t * 3 + 45
			dark = pygame.transform.scale(darkness, (72, 72))
			dark = pygame.transform.rotate(dark, angle)
			rect = dark.get_rect(center=(36, 36) + pygame.math.Vector2(48).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(36, 36))
			screen.blit(dark, rect)

		if self.type == 24:
			angle = self.t * 2 + 45
			tbeacon = pygame.transform.scale(beacon, (64, 64))
			tbeacon = pygame.transform.rotate(tbeacon, angle)
			rect = tbeacon.get_rect(center=(32, 32) + pygame.math.Vector2(44, 44).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(32, 32))
			screen.blit(tbeacon, rect)

		if self.type == 32:
			angle = math.degrees(self.t)
			if self.broken == False:
				telytra = pygame.transform.scale(elytra, (128, 128))
			else:
				telytra = pygame.transform.scale(elytrab, (128, 128))
			telytra = pygame.transform.rotate(telytra, angle - 90)
			rect = telytra.get_rect(center=pygame.math.Vector2(self.x, self.y))
			if self.broken == False or self.tick % 4 <= 2: screen.blit(telytra, rect)

		if self.bounce > 0:
			a = 50
			for i in self.remain:
				pygame.draw.circle(screen, [self.color[i]*(a/50) for i in range(3)], (i[0], i[1]), self.size)
				pygame.draw.circle(screen, [self.color[i]*(a/100) for i in range(3)], (i[0], i[1]), self.size, 2)
				a -= 1

		if self.broken == False or self.tick % 4 <= 2:
			pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
			if self.nomulti > 0: pygame.draw.circle(screen, WHITE, (self.x, self.y), self.size)
			if self.poison2 <= 15 and self.poison1 > 0: pygame.draw.circle(screen, (160, 70, 255), (self.x, self.y), self.size)
			if self.super > 0: pygame.draw.circle(screen, [(255+i)//2 for i in self.color], (self.x, self.y), self.size - 2, 6)
			pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.size, 2)

			if self.stun % 4 == 1: pygame.draw.circle(screen, BLACK, (self.x, self.y), self.size)

			if (self.type != 14 or players[0] == self or players[1] == self) and self.alive == 1:
				if self.health >= 100:
					draw(str(self.health), self.x-27, self.y-12, 48, 0, (0, 0, 0))
				elif self.health >= 10:
					draw(str(self.health), self.x-19, self.y-12, 48, 0, (0, 0, 0))
				else:
					draw(str(self.health), self.x-11, self.y-12, 48, 0, (0, 0, 0))
			
		if self.type == 0:
			angle = math.degrees(self.t) + 45
			ec = pygame.transform.scale(end_crystal, (72, 72))
			ec = pygame.transform.rotate(ec, angle)
			rect = ec.get_rect(center=(32, 32) + pygame.math.Vector2(48, 48).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(32, 32))
			screen.blit(ec, rect)

		if self.type == 1:
			angle = self.t * 3 + 45
			sword = pygame.transform.scale(iron_sword, (64, 64))
			sword = pygame.transform.rotate(sword, angle)
			rect = sword.get_rect(center=(32, 32) + pygame.math.Vector2(48, 48).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(32, 32))
			screen.blit(sword, rect)

		if self.type == 2:
			angle = self.t * 3 + 45
			axe = pygame.transform.scale(iron_axe, (64, 64))
			axe = pygame.transform.rotate(axe, angle)
			rect = axe.get_rect(center=(32, 32) + pygame.math.Vector2(48, 48).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(32, 32))
			screen.blit(axe, rect)

		if self.type == 3:
			angle = self.t * 3 + 45
			abbook = pygame.transform.scale(book, (64, 64))
			abbook = pygame.transform.rotate(abbook, angle)
			rect = abbook.get_rect(center=(32, 32) + pygame.math.Vector2(48, 48).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(32, 32))
			screen.blit(abbook, rect)

		if self.type == 4:
			angle = self.t * 3 + 45
			lava = pygame.transform.scale(lava_bucket, (64, 64))
			lava = pygame.transform.rotate(lava, angle)
			rect = lava.get_rect(center=(40, 40) + pygame.math.Vector2(44, 44).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(40, 40))
			screen.blit(lava, rect)

		if self.type == 5:
			angle = self.t * 3 + 45
			spear = pygame.transform.scale(iron_spear, (96, 96))
			spear = pygame.transform.rotate(spear, angle)
			rect = spear.get_rect(center=(48, 48) + pygame.math.Vector2(64, 64).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(48, 48))
			screen.blit(spear, rect)

		if self.type == 7:
			angle = self.t * 3 + 45
			htimer = pygame.transform.scale(timer, (64, 64))
			htimer = pygame.transform.rotate(htimer, angle)
			rect = htimer.get_rect(center=(32, 32) + pygame.math.Vector2(32, 32).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(32, 32))
			screen.blit(htimer, rect)

		if self.type == 9:
			angle = self.t * 3 + 45
			hmace = pygame.transform.scale(mace, (96, 96))
			hmace = pygame.transform.rotate(hmace, angle)
			rect = hmace.get_rect(center=(48, 48) + pygame.math.Vector2(64, 64).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(48, 48))
			screen.blit(hmace, rect)

		if self.type == 10:
			angle = self.t * 3 + 45
			htrident = pygame.transform.scale(trident, (96, 96))
			htrident = pygame.transform.rotate(htrident, angle)
			rect = htrident.get_rect(center=(48, 48) + pygame.math.Vector2(64, 64).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(48, 48))
			screen.blit(htrident, rect)

		if self.type == 11:
			angle = self.t * 3 + 45
			fish = pygame.transform.scale(tfish, (64, 64))
			fish = pygame.transform.rotate(fish, angle)
			rect = fish.get_rect(center=(32, 32) + pygame.math.Vector2(44, 44).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(32, 32))
			screen.blit(fish, rect)

		if self.type == 12:
			angle = self.t * 3
			chain = pygame.transform.scale(iron_chain, (64, 64))
			chain = pygame.transform.rotate(chain, angle)
			rect = chain.get_rect(center=(32, 0) + pygame.math.Vector2(64, 0).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(32, 0))
			screen.blit(chain, rect)
		
		if self.chained > 0:
			angle = self.t
			for _ in range(2):
				chain = pygame.transform.scale(iron_chain, (64, 64))
				chain = pygame.transform.rotate(chain, angle)
				rect = chain.get_rect(center=(32, 0) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(32, 0))
				screen.blit(chain, rect)
				angle += 90

		if self.type == 13:
			angle = self.t * 3
			tbrick = pygame.transform.scale(brick, (64, 64))
			tbrick = pygame.transform.rotate(tbrick, angle)
			rect = tbrick.get_rect(center=(32, 0) + pygame.math.Vector2(self.flail[0], self.flail[1]) - pygame.math.Vector2(32, 0))
			screen.blit(tbrick, rect)
			if self.super > 0:
				rect = tbrick.get_rect(center=(32, 0) + pygame.math.Vector2(self.flail2[0], self.flail2[1]) - pygame.math.Vector2(32, 0))
				screen.blit(tbrick, rect)

		if self.type == 15:
			angle = self.t * 3 + 45
			tcod = pygame.transform.scale(cod, (64, 64))
			tcod = pygame.transform.rotate(tcod, angle)
			rect = tcod.get_rect(center=(32, 32) + pygame.math.Vector2(44, 44).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(32, 32))
			screen.blit(tcod, rect)

		if self.type == 16:
			angle = self.t * 2 + 45
			tbow = pygame.transform.scale(bow, (64, 64))
			tbow = pygame.transform.rotate(tbow, angle)
			rect = tbow.get_rect(center=(32, 32) + pygame.math.Vector2(32, 32).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(32, 32))
			screen.blit(tbow, rect)

		if self.type == 17:
			angle = self.t * 2 + 45
			tcbow = pygame.transform.scale(cbow, (64, 64))
			tcbow = pygame.transform.rotate(tcbow, angle)
			rect = tcbow.get_rect(center=(32, 32) + pygame.math.Vector2(32, 32).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(32, 32))
			screen.blit(tcbow, rect)

		if self.type == 19:
			angle = self.t * 3 + 45
			tpick = pygame.transform.scale(pickaxe, (64, 64))
			tpick = pygame.transform.rotate(tpick, angle)
			rect = tpick.get_rect(center=(32, 32) + pygame.math.Vector2(44, 44).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(32, 32))
			screen.blit(tpick, rect)

		if self.type == 20:
			angle = self.t + 45
			tanvil = pygame.transform.scale(anvil, (64, 64))
			tanvil = pygame.transform.rotate(tanvil, angle)
			rect = tanvil.get_rect(center=(32, 32) + pygame.math.Vector2(50, 50).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(32, 32))
			screen.blit(tanvil, rect)

		if self.type == 21:
			angle = self.t * 2 + 45
			tminecart = pygame.transform.scale(minecart, (64, 64))
			tminecart = pygame.transform.rotate(tminecart, angle)
			rect = tminecart.get_rect(center=(32, 32) + pygame.math.Vector2(50, 50).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(32, 32))
			screen.blit(tminecart, rect)

		if self.type == 22:
			angle = self.t * 3 + 45
			tbarrier = pygame.transform.scale(barrier, (64, 64))
			tbarrier = pygame.transform.rotate(tbarrier, angle)
			rect = tbarrier.get_rect(center=(32, 32) + pygame.math.Vector2(44, 44).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(32, 32))
			screen.blit(tbarrier, rect)

		if self.type == 23:
			angle = self.t * 3 + 45
			tlead = pygame.transform.scale(lead, (64, 64))
			tlead = pygame.transform.rotate(tlead, angle)
			rect = tlead.get_rect(center=(32, 32) + pygame.math.Vector2(44, 44).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(32, 32))
			screen.blit(tlead, rect)

		if self.type == 25:
			angle = self.t * 3 + 45
			tdye = pygame.transform.scale(dye, (64, 64))
			tdye = pygame.transform.rotate(tdye, angle)
			rect = tdye.get_rect(center=(32, 32) + pygame.math.Vector2(44, 44).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(32, 32))
			screen.blit(tdye, rect)

		if self.type == 26:
			angle = self.t * 3 + 45
			tpotion = pygame.transform.scale(potion, (64, 64))
			tpotion = pygame.transform.rotate(tpotion, angle)
			rect = tpotion.get_rect(center=(32, 32) + pygame.math.Vector2(44, 44).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(32, 32))
			screen.blit(tpotion, rect)

		if self.type == 27:
			angle = self.t * 2 + 45
			thoe = pygame.transform.scale(hoe, (64, 64))
			thoe = pygame.transform.rotate(thoe, angle)
			rect = thoe.get_rect(center=(32, 32) + pygame.math.Vector2(44, 44).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(32, 32))
			screen.blit(thoe, rect)
		
		if self.type == 28:
			angle = math.degrees(self.t) + 45
			tarrow = pygame.transform.scale(arrow, (64, 64))
			tarrow = pygame.transform.rotate(tarrow, angle - 90)
			rect = tarrow.get_rect(center=(32, 32) + pygame.math.Vector2(48, 48).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(32, 32))
			screen.blit(tarrow, rect)

		if self.type == 29:
			angle = self.t * 2 + 45
			if self.open == False:
				tbundle = pygame.transform.scale(bundle, (64, 64))
				tbundle = pygame.transform.rotate(tbundle, angle)
				rect = tbundle.get_rect(center=(32, 32) + pygame.math.Vector2(44, 44).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(32, 32))
				screen.blit(tbundle, rect)
			else:
				tbundle = pygame.transform.scale(bundleopen, (48, 48))
				tbundle = pygame.transform.rotate(tbundle, angle - 135)
				rect = tbundle.get_rect(center=(32, 32) + pygame.math.Vector2(32, 32).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(32, 32))
				screen.blit(tbundle, rect)

		if self.type == 30:
			angle = self.t * 3 + 45
			tns = pygame.transform.scale(ns, (72, 72))
			tns = pygame.transform.rotate(tns, angle)
			rect = tns.get_rect(center=(36, 36) + pygame.math.Vector2(44, 44).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(36, 36))
			screen.blit(tns, rect)

		if self.type == 31:
			angle = self.t * 3 + 45
			tpf = pygame.transform.scale(pufferfish, (72, 72))
			tpf = pygame.transform.rotate(tpf, angle)
			rect = tpf.get_rect(center=(36, 36) + pygame.math.Vector2(44, 44).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(36, 36))
			screen.blit(tpf, rect)
			if self.super > 0:
				tpf = pygame.transform.rotate(tpf, 180)
				rect = tpf.get_rect(center=(36, 36) + pygame.math.Vector2(44, 44).rotate(-angle - 180) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(36, 36))
				screen.blit(tpf, rect)

		if self.type == 33:
			angle = self.t * 2 + 45
			tegg = pygame.transform.scale(egg, (72, 72))
			tegg = pygame.transform.rotate(tegg, angle)
			rect = tegg.get_rect(center=(36, 36) + pygame.math.Vector2(44, 44).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(36, 36))
			screen.blit(tegg, rect)

# Step3_3

class Arrow:
	def __init__(self, x, y, vx, vy, dmg, owner, team, bounce=0, atype=0):
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy
		self.dmg = dmg
		self.bounce = bounce
		self.owner = owner
		self.team = team
		self.atype = atype

		if self.atype == 3: self.cooldown = 15
		if self.atype >= 100: self.cooldown = 45

		if self.atype < 100:
			self.size = [16, 6, 128, 32][self.atype]
		else:
			self.size = 16
	
		self.nohit = 0

	def move(self):
		global players, arrows, particles

		if self.atype <= 1:
			for i in players:
				if i.type == self.owner and i.stop > 0:
					return
				
			self.x += self.vx
			if abs(self.x - width/2) >= ROOMSIZE/2:
				self.vx *= -1
				self.x += self.vx
				self.x += sign(width/2 - self.x) * 2
				if self.bounce > 0:
					self.bounce -= 1
				else:
					self.x = -1000
			self.y += self.vy
			self.vy += 0.1
			if abs(self.y - height/2) >= ROOMSIZE/2:
				self.vy *= -1
				self.y += self.vy
				self.y += sign(height/2 - self.y) * 2
				if self.bounce > 0:
					self.bounce -= 1
				else:
					self.x = -1000
			
			hit = 0

			for i in players:
				if i.team != self.team:
					if abs(i.x - self.x) <= 28 and abs(i.y - self.y) <= 28:
						i.health -= self.dmg
						self.x = -1000
						hit = 1
			
			if hit > 0:
				for i in players:
					if i.type == self.owner and i.team == self.team:
						i.multi += 1
						if i.type == 0: i.multi -= 1
						if i.type == 3: i.multi -= 1
						if i.type == 17: i.multi += 1

			if self.x < 0: arrows.remove(self)

		elif self.atype == 2:
			for i in players:
				if i.type == self.owner and i.stop > 0:
					return
				
			self.x += self.vx
			self.y += self.vy
			
			particles += [Particle(self.x + random.gauss(0, 5) + 100, self.y + random.gauss(0, 5), self.vx * 2 + random.gauss(0, 2), self.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(3)]

			hit = 0

			if self.nohit == 0:
				for i in players:
					if i.team != self.team:
						if abs(i.x - self.x) <= 80 and abs(i.y - self.y) <= 80:
							i.health -= self.dmg
							i.stop = 10
							i.vx = -12
							particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]
							self.nohit = 1
							hit = 1
			
				if hit > 0:
					for i in players:
						if i.type == self.owner and i.team == self.team:
							i.multi += 1
							if i.type == 3: i.multi -= 1

		elif self.atype == 3:
			for i in players:
				if i.type == self.owner and i.stop > 0:
					return
				
			self.x += self.vx
			if abs(self.x - width/2) >= ROOMSIZE/2:
				self.vx *= -1
				self.x += self.vx
				self.x += sign(width/2 - self.x) * 2
				if self.bounce > 0:
					self.bounce -= 1
				else:
					self.x = -1000
			self.y += self.vy
			self.vy += 0.1
			if abs(self.y - height/2) >= ROOMSIZE/2:
				self.vy *= -1
				self.y += self.vy
				self.y += sign(height/2 - self.y) * 2
				if self.bounce > 0:
					self.bounce -= 1
				else:
					self.x = -1000
			
			hit = 0

			if self.cooldown > 0:
				self.cooldown -= 1
			else:
				for i in players:
					if i.team != self.team:
						if abs(i.x - self.x) <= 37 and abs(i.y - self.y) <= 37:
							i.health -= self.dmg
							self.x = -1000
							hit = 1
							particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]
					elif i.team == self.team:
						if abs(i.x - self.x) <= 37 and abs(i.y - self.y) <= 37:
							i.health += self.dmg
							self.x = -1000
							hit = 1
							particles += [Particle(i.x + random.gauss(0, 5), i.y + random.gauss(0, 5), i.vx * 2 + random.gauss(0, 2), i.vy * 2 + random.gauss(0, 2), random.randint(5, 16), 1, -1) for _ in range(50)]
				
				if hit > 0:
					for i in players:
						if i.type == self.owner and i.team == self.team:
							i.multi += 1
							if i.type == 3: i.multi -= 1

			if self.x < 0: arrows.remove(self)

		elif self.atype == 100 or self.atype == 101:
			for i in players:
				if i.type == self.owner and i.stop > 0:
					return
				
			self.x += self.vx
			if abs(self.x - width/2) >= ROOMSIZE/2:
				self.vx *= -1
				self.x += self.vx
				self.x += sign(width/2 - self.x) * 2
			self.y += self.vy
			self.vy += 0.1
			if abs(self.y - height/2) >= ROOMSIZE/2:
				self.vy *= -1
				self.y += self.vy
				self.y += sign(height/2 - self.y) * 2

			size = 20 + (self.atype == 101) * 20

			if self.cooldown > 0:
				self.cooldown -= 1
			else:
				for i in players:
					if i.team != self.team:
						if abs(i.x - self.x) <= size and abs(i.y - self.y) <= size and self.nohit == 0:
							i.health -= self.dmg
							self.nohit = 1
					elif self.nohit == 1:
						if abs(i.x - self.x) <= size + 64 and abs(i.y - self.y) <= size + 64:
							self.x = -1000
							self.nohit = 1
					else:
						if abs(i.x - self.x) <= size and abs(i.y - self.y) <= size:
							self.x = -1000
							self.nohit = 1

			if self.x < 0: arrows.remove(self)

	def draw(self):
		if self.atype == 0:
			angle = - math.degrees(math.atan2(self.vy, self.vx)) - 45
			tarrow = pygame.transform.scale(arrow, (64, 64))
			tarrow = pygame.transform.rotate(tarrow, angle)
			rect = tarrow.get_rect(center=(8, 8) + pygame.math.Vector2(0).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(8, 8))
			screen.blit(tarrow, rect)
		elif self.atype == 1:
			pygame.draw.circle(screen, BLACK, (self.x, self.y), 4)
		elif self.atype == 2:
			tminecart = pygame.transform.scale(minecart, (128, 128))
			rect = tminecart.get_rect(center=pygame.math.Vector2(self.x + random.randint(-3, 3), self.y + random.randint(-1, 1)))
			screen.blit(tminecart, rect)
		elif self.atype == 3:
			angle = - math.degrees(math.atan2(self.vy, self.vx)) - 45
			tpotion = pygame.transform.scale(potion, (64, 64))
			tpotion = pygame.transform.rotate(tpotion, angle)
			rect = tpotion.get_rect(center=(8, 8) + pygame.math.Vector2(0).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(8, 8))
			screen.blit(tpotion, rect)
		elif self.atype == 100:
			angle = - math.degrees(math.atan2(self.vy, self.vx)) - 45
			tgold = pygame.transform.scale(gold, (64, 64))
			tgold = pygame.transform.rotate(tgold, angle)
			rect = tgold.get_rect(center=(8, 8) + pygame.math.Vector2(0).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(8, 8))
			if self.nohit == 0 or random.randint(1, 3) == 1:
				screen.blit(tgold, rect)
		elif self.atype == 101:
			angle = - math.degrees(math.atan2(self.vy, self.vx)) - 45
			tdiamond = pygame.transform.scale(diamond, (64, 64))
			tdiamond = pygame.transform.rotate(tdiamond, angle)
			if self.nohit > 0: tdiamond = pygame.transform.grayscale(tdiamond)
			rect = tdiamond.get_rect(center=(8, 8) + pygame.math.Vector2(0).rotate(-angle) + pygame.math.Vector2(self.x, self.y) - pygame.math.Vector2(8, 8))
			if self.nohit == 0 or random.randint(1, 3) == 1:
				screen.blit(tdiamond, rect)

class Block:
	def __init__(self, x, y, owner, atype=0):
		self.x = x
		self.y = y
		self.owner = owner
		self.atype = atype

		self.size = 64

	def move(self):
		global players, arrows, particles, blocks
		
		pass

	def draw(self):
		if self.atype == 0:
			tbarrier = pygame.transform.scale(barrier, (64, 64))
			rect = tbarrier.get_rect(center=pygame.math.Vector2(self.x, self.y))
			screen.blit(tbarrier, rect)

class Particle:
	def __init__(self, x, y, spdx, spdy, size, l=1, mi=0):
		self.x = x
		self.y = y
		self.spdx = spdx
		self.spdy = spdy
		self.size = size
		self.l = l
		self.mi = mi
	
	def update(self):
		self.x += self.spdx
		self.y += self.spdy
		self.spdx *= 0.9
		self.spdy *= 0.9
		if self.size > self.mi:
			self.size -= 0.25
		else:
			if self.l > 0.2: self.l -= 0.0001
	
	def draw(self):
		pygame.draw.rect(screen, (255 - 255*self.l, 255 - 255*self.l, 255 - 255*self.l), (self.x - self.size/2, self.y - self.size/2, self.size, self.size))

width = 800
height = 800
fps = 75

ROOMSIZE = 600

WHITE = (233, 233, 242)
GRAY = (32, 32, 32)
RED = (255, 0, 0)
RHITE = (255, 150, 150)
BHITE = (150, 150, 255)
BLACK = (0, 0, 0)

game_folder = os.path.dirname(__file__)
audio_folder = os.path.join(os.path.dirname(__file__),"audio")

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Battle Royale")
clock = pygame.time.Clock()

icon = pygame.image.load(os.path.join(game_folder, "icon.png"))
pygame.display.set_icon(icon)

font  = pygame.font.Font(os.path.join(game_folder, "x12y16pxMaruMonica.ttf"), 32)
font2 = pygame.font.Font(os.path.join(game_folder, "x12y16pxMaruMonica.ttf"), 24)

iron_sword = pygame.image.load(os.path.join(game_folder, "iron_sword.png"))
iron_axe = pygame.image.load(os.path.join(game_folder, "iron_axe.png"))
book = pygame.image.load(os.path.join(game_folder, "knowledge_book.png"))
lava_bucket = pygame.image.load(os.path.join(game_folder, "lava_bucket.png"))
iron_spear = pygame.image.load(os.path.join(game_folder, "iron_spear_in_hand.png"))
darkness = pygame.image.load(os.path.join(game_folder, "darkness.png"))
timer = pygame.image.load(os.path.join(game_folder, "clock_01.png"))
mace = pygame.image.load(os.path.join(game_folder, "mace.png"))
trident = pygame.image.load(os.path.join(game_folder, "trident.png"))
tfish = pygame.image.load(os.path.join(game_folder, "tropical_fish.png"))
iron_chain = pygame.image.load(os.path.join(game_folder, "iron_chain.png"))
brick = pygame.image.load(os.path.join(game_folder, "brick.png"))
cod = pygame.image.load(os.path.join(game_folder, "cod.png"))
bow = pygame.image.load(os.path.join(game_folder, "bow.png"))
cbow = pygame.image.load(os.path.join(game_folder, "crossbow.png"))
tnt = pygame.image.load(os.path.join(game_folder, "tnt.png"))
pickaxe = pygame.image.load(os.path.join(game_folder, "pickaxe.png"))
anvil = pygame.image.load(os.path.join(game_folder, "anvil.png"))
minecart = pygame.image.load(os.path.join(game_folder, "minecart.png"))
lead = pygame.image.load(os.path.join(game_folder, "lead.png"))
end_crystal = pygame.image.load(os.path.join(game_folder, "end_crystal.png"))
beacon = pygame.image.load(os.path.join(game_folder, "beacon.png"))
beacon.set_colorkey((255, 255, 255))
dye = pygame.image.load(os.path.join(game_folder, "dye.png"))
hoe = pygame.image.load(os.path.join(game_folder, "hoe.png"))
bundle = pygame.image.load(os.path.join(game_folder, "bundle.png"))
bundleopen = pygame.image.load(os.path.join(game_folder, "bundleopen.png"))
ns = pygame.image.load(os.path.join(game_folder, "nether_star.png"))
pufferfish = pygame.image.load(os.path.join(game_folder, "pufferfish.png"))
elytra = pygame.image.load(os.path.join(game_folder, "elytra.png"))
elytrab = pygame.image.load(os.path.join(game_folder, "elytrab.png"))
egg = pygame.image.load(os.path.join(game_folder, "egg.png"))

arrow = pygame.image.load(os.path.join(game_folder, "arrow.png"))
barrier = pygame.image.load(os.path.join(game_folder, "barrier.png"))
potion = pygame.image.load(os.path.join(game_folder, "potion.png"))

gold = pygame.image.load(os.path.join(game_folder, "gold.png"))
diamond = pygame.image.load(os.path.join(game_folder, "diamond.png"))

# Step1_1

running = True
name = ["Strs2","Sword","Axe","Book","Lava","Spear","Darkness","Timer","Unarmed","Mace","Trident","Tropical Fish","Chain","Brick","Duplicator","Cod","Bow","Crossbow","TNT","Pickaxe","Anvil","Minecart","Barrier","Lead","Beacon","Dye","Potion","Hoe","Arrow","Bundle","Nether Star","Pufferfish","Elytra","Egg"]
# Step2_1
colors= [(255,200,255), (255, 90, 90), (200, 75, 45), (140, 200, 130), (255, 120, 65), (255, 215, 120), (135, 150, 180), (255, 225, 80)\
		   , (190, 190, 190), (240, 90, 160), (125, 225, 255), (255, 160, 65), (190, 185, 150), (255, 180, 160), (200, 140, 255)\
		   , (240, 210, 145), (200, 225, 145), (150, 190, 90), (230, 120, 90), (70, 195, 255), (155, 170, 195), (220, 170, 135)\
		   , (255, 85, 130), (255, 150, 70), (180, 255, 255), (230, 255, 255), (255, 150, 230), (200, 140, 60)\
		   , (230, 255, 215), (240, 130, 0), (220, 255, 235), (160, 70, 255), (50, 100, 255), (240, 225, 140)]

FIGHTERS = 32
# Step4_1

mark = 0
tournament = [i+1 for i in range(FIGHTERS)]
point = [-5] * FIGHTERS
point2= [0] * FIGHTERS
pointtotal = [0] * FIGHTERS
finished = 0

match = [0] * (FIGHTERS + 1)
winnum = [0] * (FIGHTERS + 1)

random.shuffle(tournament)

#tournament.pop(-1)

# Step4_2
# tournament = [?, ?]
perma = deepcopy(tournament)

print(tournament)

		# 0 - Strs2
		# 1 - sword*
		# 2 - axe
		# 3 - book
		# 4 - lava
		# 5 - spear
		# 6 - dark
		# 7 - slow
		# 8 - barehand*
		# 9 - mace
		# 10- trident
		# 11- tropical
		# 12- chain
		# 13- flail*
		# 14- dupli
		# 15- cod
		# 16- bow
		# 17- crossbow
		# 18- tnt
		# 19- pickaxe
		# 20- anvil
		# 21- minecart
		# 22- barrier
		# 23- lead
		# 24- beacon
		# 25- dye
		# 26- potion
		# 27- hoe
		# 28- arrow
		# 29- bundle
		# 30- netherstar
		# 31- pufferfish*
		# 32- elytra

		# 33- egg

o1 = 1

players = [Player(width/2 - ROOMSIZE/2.5, height/2, colors[tournament[0]], tournament[0], 1), Player(width/2 + ROOMSIZE/2.5, height/2, colors[tournament[1]], tournament[1], 2)]

#players = [Player(width/2 - ROOMSIZE/2.5, height/2 - ROOMSIZE/2.5, (255, 255, 140), 0), Player(width/2 + ROOMSIZE/2.5, height/2 - ROOMSIZE/2.5, (140, 140, 255), 16)]

#players = [Player(width/2 - ROOMSIZE/2.5 + ROOMSIZE/2.5/2.4*(n%6), height/2 - ROOMSIZE/2.5 + ROOMSIZE/2.5/2.4*(n//6), colors[i], i) for n, i in enumerate(tournament)]

o1 = 1
o2 = 7
o3 = 16
o4 = 17

#players = [Player(width/2 - ROOMSIZE/2.5, height/2 - ROOMSIZE/2.5, (255, 255, 140), o1), Player(width/2 + ROOMSIZE/2.5, height/2 - ROOMSIZE/2.5, (140, 140, 255), o1),Player(width/2 - ROOMSIZE/2.5, height/2 + ROOMSIZE/2.5, (255, 140, 140), o1), Player(width/2 + ROOMSIZE/2.5, height/2 + ROOMSIZE/2.5, (140, 255, 140), o1)]
#players = [Player(width/2 - ROOMSIZE/2.5, height/2 - ROOMSIZE/2.5, (255, 255, 140), o1, 1), Player(width/2 - ROOMSIZE/2.5, height/2 + ROOMSIZE/2.5, (255, 255, 140), o2, 1),Player(width/2 + ROOMSIZE/2.5, height/2 - ROOMSIZE/2.5, (140, 140, 255), o3, 2), Player(width/2 + ROOMSIZE/2.5, height/2 + ROOMSIZE/2.5, (140, 140, 255), o4, 2)]

#players = [Player(width/2 - ROOMSIZE/2.5, height/2 - ROOMSIZE/2.5, (255, 255, 140), o1), Player(width/2 + ROOMSIZE/2.5, height/2 - ROOMSIZE/2.5, (140, 140, 255), o1),Player(width/2 - ROOMSIZE/2.5, height/2 + ROOMSIZE/2.5, (255, 140, 140), o1), Player(width/2 + ROOMSIZE/2.5, height/2 + ROOMSIZE/2.5, (140, 255, 140), o1), Player(width/2 - ROOMSIZE/5, height/2 - ROOMSIZE/5, (140, 140, 140), o1), Player(width/2 + ROOMSIZE/5, height/2 - ROOMSIZE/5, (255, 140, 255), o1)]
#players = [Player(width/2 - ROOMSIZE/2.5, height/2 - ROOMSIZE/2.5, (255, 255, 140), 31, -1, 1), Player(width/2 + ROOMSIZE/2.5, height/2 - ROOMSIZE/2.5, (140, 140, 255), o1, 1),Player(width/2 - ROOMSIZE/2.5, height/2 + ROOMSIZE/2.5, (255, 140, 140), o1, 1), Player(width/2 + ROOMSIZE/2.5, height/2 + ROOMSIZE/2.5, (140, 255, 140), o1, 1), Player(width/2 - ROOMSIZE/5, height/2 - ROOMSIZE/5, (140, 140, 140), o1, 1), Player(width/2 + ROOMSIZE/5, height/2 - ROOMSIZE/5, (255, 140, 255), o1, 1)]
#players = [Player(width/2 - ROOMSIZE/2.5, height/2 - ROOMSIZE/2.5, (255, 255, 140), 0), Player(width/2 + ROOMSIZE/2.5, height/2 - ROOMSIZE/2.5, (140, 140, 255), o1, 1),Player(width/2 - ROOMSIZE/2.5, height/2 + ROOMSIZE/2.5, (255, 140, 140), o1, 1), Player(width/2 + ROOMSIZE/2.5, height/2 + ROOMSIZE/2.5, (140, 255, 140), o1, 1)]
#players = [Player(width/2 - ROOMSIZE/2.5, height/2 - ROOMSIZE/2.5, (255, 255, 140), 0), Player(width/2 + ROOMSIZE/2.5, height/2 - ROOMSIZE/2.5, (140, 140, 255), o1, 1)]

#players = [Player(width/2 - ROOMSIZE/2.5, height/2 - ROOMSIZE/2.5, (255, 255, 140), o1), Player(width/2 + ROOMSIZE/2.5, height/2 - ROOMSIZE/2.5, (140, 140, 255), o1+1),Player(width/2 - ROOMSIZE/2.5, height/2 + ROOMSIZE/2.5, (255, 140, 140), o1+2), Player(width/2 + ROOMSIZE/2.5, height/2 + ROOMSIZE/2.5, (140, 255, 140), o1+3), Player(width/2 - ROOMSIZE/5, height/2 - ROOMSIZE/5, (140, 140, 140), o1+4), Player(width/2 + ROOMSIZE/5, height/2 - ROOMSIZE/5, (255, 140, 255), o1+5)]

WAITUNTILONE = False
PERMANENTMATCH = False

arrows = []
blocks = []

#colors = [(255, 140, 140),(140, 255, 140),(140, 140, 255),(255, 255, 140)]
posxes = [width/2 - ROOMSIZE/2.5, width/2 + ROOMSIZE/2.5, width/2 - ROOMSIZE/2.5, width/2 + ROOMSIZE/2.5]
posyes = [height/2 - ROOMSIZE/2.5, height/2 - ROOMSIZE/2.5, height/2 + ROOMSIZE/2.5, height/2 + ROOMSIZE/2.5]

sp = deepcopy(players)

bullets = []

particles = []

launched = True

wins = [0, 0]
ends = 0

start = 75

nowall = 0
nowallt = 0

while launched == True:
	now = pygame.time.get_ticks()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			launched = False

	pygame.display.flip()
	clock.tick(fps)

while running == True:
	now = pygame.time.get_ticks()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			if pygame.mouse.get_pressed(5)[0]:
				if players[0].type == 0:
					pos = pygame.mouse.get_pos()
					angle = math.atan2(players[0].y - pos[1], players[0].x - pos[0])
					players[0].vx = -math.cos(angle) * 7
					players[0].vy = -math.sin(angle) * 7
			if pygame.mouse.get_pressed(5)[2]:
				if players[0].type == 0:
					pos = pygame.mouse.get_pos()
					angle = math.atan2(players[0].y - pos[1], players[0].x - pos[0])
					for i in range(5):
						arrows += [Arrow(players[0].x, players[0].y, -math.cos(angle) * 12 + random.gauss(0, 0.3), -math.sin(angle) * 12 + random.gauss(0, 0.3), 2, 0, 0, 1)]

	screen.fill(WHITE)

	pygame.draw.rect(screen, BLACK, ((width-ROOMSIZE)/2, (height-ROOMSIZE)/2, ROOMSIZE, ROOMSIZE), 6)

	if nowall > 0:
		if nowall == 1: pygame.draw.rect(screen, WHITE, ((width-ROOMSIZE)/2, (height-ROOMSIZE)/2, 8, ROOMSIZE), 6)
		if nowall == 2: pygame.draw.rect(screen, WHITE, ((width-ROOMSIZE)/2 + ROOMSIZE - 8, (height-ROOMSIZE)/2, 8, ROOMSIZE), 6)
		nowallt -= 1
		if nowallt <= 0: nowall = 0

	for i in particles:
		if i.size <= 0:
			particles.remove(i)
		else:
			i.update()
			i.draw()

	for i in arrows:
		i.move()
		i.draw()

	for i in blocks:
		i.move()
		i.draw()

	alive = 0
	onlydupli = 1
	teams = -2
	onlyteam = 1

	for l, i in enumerate(players):
		if start == 0: i.move()
		i.draw()
		if ends == 0:
			if i.alive == 0 and not WAITUNTILONE:
				if players[0] == i:
					wins[1] += 1
					ends = 120

				elif players[1] == i:
					wins[0] += 1
					ends = 120
			if WAITUNTILONE:
				if i.alive == 1 and i.team != teams and teams != -2:
					onlyteam = 0
				if i.alive == 1:
					alive += 1
					teams = i.team
				if i.alive == 1 and i.type != 14: onlydupli = 0

	if WAITUNTILONE and alive <= 1 and ends == 0: ends = 120
	if WAITUNTILONE and onlydupli == 1 and ends == 0: ends = 120
#	if WAITUNTILONE and onlyteam == 1 and ends == 0: ends = 120

	if len(players) > 100 and ends == 0:
		wins[random.randint(0, 1)] += 1
		ends = 120

	if ends == 0:
		pygame.draw.rect(screen, colors[tournament[0+mark]], (100, 64, ROOMSIZE/2, 36))
		pygame.draw.rect(screen, colors[tournament[1+mark]], (100+ROOMSIZE/2, 64, ROOMSIZE/2, 36))

	if start > 0:
		players[0].show2 = " - "
		players[1].show2 = " - "

	str1 = f"{players[0].show1}{players[0].show2} {players[0].show3}"
	str2 = f"{players[1].show1}{players[1].show2} {players[1].show3}"

	screen.blit(font.render("Super " * players[0].super + name[players[0].type], True, (0, 0, 0)), (100, 30))
	screen.blit(font.render("Super " * players[1].super + name[players[1].type], True, (0, 0, 0)), (width-100 - font.render("Super " * players[1].super + name[players[1].type], True, (0, 0, 0)).get_rect().width, 30))
	screen.blit(font.render(str1, True, (0, 0, 0)), (100 + random.randint(-2, 2) * (players[0].show2 != players[0].show2o and players[0].type != 14), 64))
	screen.blit(font.render(str2, True, (0, 0, 0)), (width-100 - font.render(str2, True, (0, 0, 0)).get_rect().width + random.randint(-2, 2) * (players[1].show2 != players[1].show2o and players[1].type != 14), 64))
	screen.blit(font.render(f"{wins[0]}-{wins[1]}", True, (0, 0, 0)), (32, 16))

	if len(tournament) > 8:
		screen.blit(font.render("Preliminary", True, (0, 0, 0)), (width/2 - font.render("Preliminary", True, (0, 0, 0)).get_rect().width / 2, 16))
		pointadd = 0
	elif len(tournament) > 4:
		screen.blit(font.render("Quarterfinals", True, (0, 0, 0)), (width/2 - font.render("Quarterfinals", True, (0, 0, 0)).get_rect().width / 2, 16))
		pointadd = 3
	elif len(tournament) > 2:
		screen.blit(font.render("Semifinals", True, (0, 0, 0)), (width/2 - font.render("Semifinals", True, (0, 0, 0)).get_rect().width / 2, 16))
		pointadd = 9
	else:
		screen.blit(font.render("Finals", True, (0, 0, 0)), (width/2 - font.render("Finals", True, (0, 0, 0)).get_rect().width / 2, 16))
		pointadd = 20

	pygame.display.flip()
	clock.tick(fps)

	if start > 0: start -= 1

	if ends > 0:

		if ends == 120:
			change = 0
			ends -= 1

			if wins[0] == 2 and not WAITUNTILONE:
				print(f"{name[tournament[mark]]} Wins, {name[tournament[mark+1]]} Loses. ", end="")
				match[tournament[mark]] += 2
				match[tournament[mark+1]] += 2
				winnum[tournament[mark]] += 2
				if wins[1] == 0:
					point2[tournament[mark + 0] - 1] += 2
					point2[tournament[mark + 1] - 1] -= 2
					print("Straight Victory!")
				else:
					print("")
					match[tournament[mark]] += 1
					match[tournament[mark+1]] += 1
					winnum[tournament[mark+1]] += 1
				tournament[mark + 1] = -1
				mark += 2
				change = 1
			elif wins[1] == 2 and not WAITUNTILONE:
				print(f"{name[tournament[mark+1]]} Wins, {name[tournament[mark]]} Loses. ", end="")
				match[tournament[mark]] += 2
				match[tournament[mark+1]] += 2
				winnum[tournament[mark+1]] += 2
				if wins[0] == 0:
					point2[tournament[mark + 0] - 1] -= 2
					point2[tournament[mark + 1] - 1] += 2
					print("Straight Victory!")
				else:
					print("")
					match[tournament[mark]] += 1
					match[tournament[mark+1]] += 1
					winnum[tournament[mark]] += 1
				tournament[mark + 0] = -1
				mark += 2
				change = 1
				
		elif ends > 2:
			ends -= 1

		else:
			WHITE = (233, 233, 242)
			GRAY = (32, 32, 32)
			RED = (255, 0, 0)
			RHITE = (255, 150, 150)
			BHITE = (150, 150, 255)
			BLACK = (0, 0, 0)
			ends = 0
			arrows = []
			blocks = []
			nowall = 0
			nowallt = 0
			start = 75
			angle = random.random()*math.pi
			sp[0].vx = math.cos(angle) * 6
			sp[0].vy = math.sin(angle) * 6
			angle = random.random()*math.pi
			sp[1].vx = math.cos(angle) * 6
			sp[1].vy = math.sin(angle) * 6
			
			if change == 0:
				players = deepcopy(sp)
			else:
				if mark + 2 > len(tournament):
					while -1 in tournament:
						tournament.remove(-1)
					mark = 0
					for i in range(15):
						if (i+1) in tournament:
							point[i] = pointadd
					print(tournament)
				if len(tournament) <= 1:
					finished = 1
				if finished == 0:
					sp = [Player(width/2 - ROOMSIZE/2.5, height/2, colors[tournament[mark + 0]], tournament[mark + 0], 1), Player(width/2 + ROOMSIZE/2.5, height/2, colors[tournament[mark + 1]], tournament[mark + 1], 2)]
					players = deepcopy(sp)
					change = 0
					wins = [0, 0]
					start = 50
#					print(tournament)
				else:
					if not PERMANENTMATCH:
						pointtotal = [pointtotal[i] + point[i]+ point2[i] for i in range(FIGHTERS)]

						print(f"{name[tournament[0]]} Wins!")
						print("-=-=-=-")
						for i in range(FIGHTERS):
							print(f"{name[i+1]}: {point[i]} Pt.")
						print(f"Total: {pointtotal}")
						for i in range(FIGHTERS):
							print(f"{name[i+1]}: {winnum[i+1]} / {match[i+1]}, {int(winnum[i+1]/match[i+1]*1000)/10}%")
						print("-=-=-=-=-=-=-=-=-")
					finished = 0

					point = [-5] * FIGHTERS
					point2= [0] * FIGHTERS

					change = 0
					wins = [0, 0]
					start = 50

					mark = 0
					tournament = [i+1 for i in range(FIGHTERS)]
					finished = 0
					random.shuffle(tournament)
					if PERMANENTMATCH:
#						perma[1] += 1
						tournament = deepcopy(perma)
					players = [Player(width/2 - ROOMSIZE/2.5, height/2, (255, 255, 140), tournament[0], 1), Player(width/2 + ROOMSIZE/2.5, height/2, (140, 140, 255), tournament[1], 2)]
					sp = deepcopy(players)
					start = 75
					print(tournament)