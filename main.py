#  Mr0o
#  Simple Fireworks Simulator
#
#  This is a simple fireworks simulator using pygame for input and basic graphics
#  The firework sound used fo this was taken from here: https://www.youtube.com/watch?v=AUPPBNDCFk4
#  Inspiration for this project comes from The Coding Train: https://www.youtube.com/watch?v=CKeyIbT3vXI
#
#  There are probably plenty of areas where performance could be improved
#  There are also plenty of ways that this could be made more accurate or interesting
#
#  Feel free to do whatever you want with this

import pygame
import sys  # used to exit the program immediately
from random import randint, random  # used for random integers and floats

from vectors import Vector, createRandomVector

#  screen width and height parameters
WIDTH = 1200
HEIGHT = 900

pygame.init()  # initialize pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # display surface
alpha_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)  # alpha surface
clock = pygame.time.Clock()  # game clock
pygame.display.set_caption("Simple Fireworks Simulator")


class Particle:
    def __init__(self, x, y, explosion):  # the 'explosion' argument is a boolean that specifies whether this is a Firework Particle or an explosion Particle
        self.pos = Vector(x, y)
        if not explosion:
            self.vel = Vector(random() * randint(-1, 1), -randint(int(HEIGHT/128), int(HEIGHT/75)))
        else:
            self.vel = createRandomVector(10)
            self.vel.setMag(random() * randint(1, 4))

        self.acc = Vector(0, 0)

    def applyForce(self, force):
        self.acc.add(force)

    def update(self):
        self.vel.add(self.acc)
        self.pos.add(self.vel)

    def draw(self, color):
        pygame.draw.circle(alpha_surface, color, [self.pos.vx, self.pos.vy], 2)


class Firework:
    def __init__(self):
        # the firework stuff
        self.firework = Particle(randint(0, WIDTH), HEIGHT, False)
        self.color = (random() * 255, random() * 255, random() * 255)

        # the explosion stuff
        self.exploded = False
        self.explosion_particles = []
        self.rmag = (random() + 1) * randint(2, 3)
        self.lifetime = randint(100, 150)
        self.alive = True

    def update(self):
        if not self.exploded:
            self.firework.applyForce(gravity)
            self.firework.update()
        else:
            self.lifetime -= 1
            if self.lifetime < 0:
                self.explosion_particles.clear()
                self.alive = False
            for i, p in enumerate(self.explosion_particles):
                p.applyForce(Vector(0, random() * 0.0003))
                p.vel.limitMag(self.rmag)
                p.update()

        if self.firework.vel.vy >= -1 and not self.exploded:  # if the firework y velocity reaches -1 then explode
            self.explode()
            pygame.mixer.Sound.play(explode_sound)

    def explode(self):
        self.exploded = True

        for i in range(randint(40, 450)):  # create a random amount of particles ranging 40 to 450
            particle = Particle(self.firework.pos.vx, self.firework.pos.vy, True)
            self.explosion_particles.append(particle)

    def draw(self):
        if not self.exploded:
            self.firework.draw(self.color)
        else:
            for p in self.explosion_particles:
                p.draw(self.color)


def update():
    if randint(0, 1000) < 5:  # 0.5% chance of creating a new firework each frame
        fireworks.append(Firework())

    for index, fw in enumerate(fireworks):
        fw.update()
        if not fw.alive:
            del fireworks[index]


def draw():
    for i in fireworks:
        i.draw()


explode_sound = pygame.mixer.Sound("explode.wav")
fireworks = [Firework()]
gravity = Vector(0, 0.002)

# main loop
while True:
    for event in pygame.event.get():  # check events and quit if the program is closed
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    alpha_surface.fill((255, 255, 255, 220), special_flags=pygame.BLEND_RGBA_MULT)
    screen.fill((0, 0, 0))  # black screen

    screen.blit(alpha_surface, (0, 0))

    update()  # update the simulation
    draw()  # draw everything to the screen

    pygame.display.update()
    clock.tick(60)
