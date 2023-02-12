import pygame
import random
import math

WIDTH = 800
HEIGHT = 600
BOID_COUNT = 50
GREEN =     (  0, 255,   0)
class Boid:
    def __init__(self):
        self.position = [random.uniform(0, WIDTH), random.uniform(0, HEIGHT)]
        self.velocity = [random.uniform(-1, 1), random.uniform(-1, 1)]

    def update(self, boids):
        separation = [0, 0]
        alignment = [0, 0]
        cohesion = [0, 0]
        count = 0
        for other in boids:
            if other is self:
                continue
            distance = math.hypot(self.position[0] - other.position[0], self.position[1] - other.position[1])
            if distance > 0 and distance < 50:
                separation[0] += (self.position[0] - other.position[0]) / distance
                separation[1] += (self.position[1] - other.position[1]) / distance
                alignment[0] += other.velocity[0]
                alignment[1] += other.velocity[1]
                cohesion[0] += other.position[0]
                cohesion[1] += other.position[1]
                count += 1
        if count > 0:
            separation[0] /= count
            separation[1] /= count
            alignment[0] /= count
            alignment[1] /= count
            cohesion[0] /= count
            cohesion[1] /= count
            cohesion[0] = (cohesion[0] - self.position[0]) / 100
            cohesion[1] = (cohesion[1] - self.position[1]) / 100
        self.velocity[0] += separation[0] + alignment[0] + cohesion[0]
        self.velocity[1] += separation[1] + alignment[1] + cohesion[1]
        self.velocity = [min(3, max(-3, v)) for v in self.velocity]
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.position[0] = max(0, min(WIDTH, self.position[0]))
        self.position[1] = max(0, min(HEIGHT, self.position[1]))

        #do random behvior here with 1%
        if random.randint(0,100) < 1:
            self.velocity[0] *= -1
        if random.randint(0,100) < 1:
            self.velocity[1] *= -1

        if ((self.position[0] ==0 and self.position[1] == 0 )  #top-left
        or (self.position[0] ==WIDTH and self.position[1] == 0 )  #top-right
        or (self.position[0] ==0 and self.position[1] == HEIGHT ) #bottom-left
        or (self.position[0] ==WIDTH and self.position[1] == HEIGHT )): #bottom-right
            self.position = [random.uniform(0, WIDTH), random.uniform(0, HEIGHT)]


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    boids = [Boid() for i in range(BOID_COUNT)]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill((255, 255, 255))
        for boid in boids:
            boid.update(boids)
            print(boid.position)
            pygame.draw.circle(screen, GREEN, [int(x) for x in boid.position], 4)
        pygame.display.flip()
        pygame.display.update()
            # clock.tick(60)

    #Setting FPS
    
if __name__ == "__main__":
    main()