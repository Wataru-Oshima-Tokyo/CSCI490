"""
In this code, we first subscribe to the /map topic to receive 
the OccupancyGrid messages that represent the map data in Rviz. 
Then, we convert the OccupancyGrid message to a 2D numpy array 
and process the data to convert it to Pygame coordinates. 
Finally, we initialize Pygame, draw the map on the Pygame s
creen and run the main loop to display the map.
"""



import rospy
from nav_msgs.msg import OccupancyGrid
import numpy as np
import pygame

def map_callback(map_msg):
    # Convert the OccupancyGrid message to a 2D numpy array
    map_data = np.array(map_msg.data, dtype=np.int8)
    map_data = map_data.reshape((map_msg.info.height, map_msg.info.width))

    # Convert the map data to Pygame coordinates
    pygame_map = np.zeros((map_msg.info.height, map_msg.info.width, 3), dtype=np.uint8)
    for i in range(map_msg.info.height):
        for j in range(map_msg.info.width):
            value = map_data[i][j]
            if value == 0:
                # Free space
                pygame_map[i][j] = [255, 255, 255]
            elif value == 100:
                # Occupied space
                pygame_map[i][j] = [0, 0, 0]
            else:
                # Unknown space
                pygame_map[i][j] = [128, 128, 128]

# Subscribing to the map topic
rospy.Subscriber("/map", OccupancyGrid, map_callback)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((map_msg.info.width, map_msg.info.height))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the map on the Pygame screen
    screen.blit(pygame_map, (0, 0))
    pygame.display.update()

# Quit Pygame
pygame.quit()