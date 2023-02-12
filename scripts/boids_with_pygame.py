# """
# The Boids algorithm is a simulation of bird flocking behavior, which can be implemented visually in Python using a graphics library such as Pygame. Here's an example of how you could implement Boids in Python with Pygame:

# """



# import pygame
# import random
# import math

# # Initialize the screen
# screen = pygame.display.set_mode((800, 600))
# clock = pygame.time.Clock()

# # Define the boids class
# class Boid:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#         self.velocity_x = random.uniform(-1, 1)
#         self.velocity_y = random.uniform(-1, 1)
#         self.size = 10

#     def update(self, boids):
#         # Rule 1: Boids try to fly towards the center of mass of neighboring boids
#         center_of_mass_x = 0
#         center_of_mass_y = 0
#         for boid in boids:
#             if boid == self:
#                 continue
#             center_of_mass_x += boid.x
#             center_of_mass_y += boid.y
#         center_of_mass_x /= len(boids) - 1
#         center_of_mass_y /= len(boids) - 1
#         self.velocity_x += (center_of_mass_x - self.x) / 100
#         self.velocity_y += (center_of_mass_y - self.y) / 100

#         # Rule 2: Boids try to keep a small distance away from other objects (including other boids)
#         distance = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
#         if distance < 50:
#             self.velocity_x -= (self.velocity_x / distance) * 2
#             self.velocity_y -= (self.velocity_y / distance) * 2

#         # Rule 3: Boids try to match velocity with nearby boids
#         average_velocity_x = 0
#         average_velocity_y = 0
#         for boid in boids:
#             if boid == self:
#                 continue
#             average_velocity_x += boid.velocity_x
#             average_velocity_y += boid.velocity_y
#         average_velocity_x /= len(boids) - 1
#         average_velocity_y /= len(boids) - 1
#         self.velocity_x += (average_velocity_x - self.velocity_x) / 8
#         self.velocity_y += (average_velocity_y - self.velocity_y) / 8

#         # Update the position based on the velocity
#         self.x += self.velocity_x
#         self.y += self.velocity_y

# # Initialize the boids
# boids = [Boid(random.uniform(0, 800), random.uniform(0, 600)) for i in range(50)]

# # Main loop
# running = True
# while running:
#     # Handle events
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#     for boid in boids:
#         boid.update(boids)
#     # Clear the screen
#     pygame.display.update()

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