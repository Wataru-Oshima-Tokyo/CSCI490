import random
import threading
import heapq
import numpy as np
import pygame
import time

ORIGINAL_MAP_SIZE = (1660, 1660)
NEW_MAP_SIZE = (100, 100)
NUM_WAYPOINTS = 40

def convert_coordinates(coord, old_size, new_size):
    x_ratio = new_size[0] / old_size[0]
    y_ratio = new_size[1] / old_size[1]
    return int(coord[0] * x_ratio), int(coord[1] * y_ratio)

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, goal, map_size):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = []
    heapq.heappush(open_set, (0, start))

    g_scores = {node: float('inf') for x in range(map_size[0]) for y in range(map_size[1]) for node in [(x, y)]}
    g_scores[start] = 0

    f_scores = {node: float('inf') for x in range(map_size[0]) for y in range(map_size[1]) for node in [(x, y)]}
    f_scores[start] = heuristic(start, goal)

    came_from = dict()

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1]

        for neighbor in [(current[0] + dx, current[1] + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]:
            if 0 <= neighbor[0] < map_size[0] and 0 <= neighbor[1] < map_size[1]:
                tentative_g_score = g_scores[current] + 1
                if tentative_g_score < g_scores[neighbor]:
                    came_from[neighbor] = current
                    g_scores[neighbor] = tentative_g_score
                    f_scores[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    if neighbor not in [item[1] for item in open_set]:
                        heapq.heappush(open_set, (f_scores[neighbor], neighbor))

    return None




def create_robots(max_robots, map_size):
    num_robots = max_robots #random.randint(1, max_robots)
    robot_positions = [tuple(np.random.randint(0, map_size[i], num_robots).tolist()) for i in range(2)]
    return list(zip(*robot_positions))

def create_random_waypoints(number_of_waypoints, map_size):
    return [(random.randint(0, map_size[0] - 1), random.randint(0, map_size[1] - 1)) for _ in range(number_of_waypoints)]

def draw_robot(screen, position, color):
    pygame.draw.circle(screen, color, position, 5)

def draw_waypoint(screen, position, color):
    pygame.draw.circle(screen, color, position, 3)

def convert_coordinates(coord, old_size, new_size):
    x_ratio = new_size[0] / old_size[0]
    y_ratio = new_size[1] / old_size[1]
    return int(coord[0] * x_ratio), int(coord[1] * y_ratio)

def invert_coordinates(coord, old_size, new_size):
    x_ratio = old_size[0] / new_size[0]
    y_ratio = old_size[1] / new_size[1]
    return int(coord[0] * x_ratio), int(coord[1] * y_ratio)

def main(original_robots, original_waypoints):
    robots = []
    waypoints = []
    for robot in original_robots:
        robots.append(convert_coordinates(robot, ORIGINAL_MAP_SIZE, NEW_MAP_SIZE))

    for waypoint in original_waypoints:
        waypoints.append(convert_coordinates(waypoint, ORIGINAL_MAP_SIZE, NEW_MAP_SIZE))

    print("robot", robots)
    print("waypoints", waypoints)

    visited_waypoints = set()
     # ロボットにラベルを追加します
    robot_labels = ['Robot ' + chr(ord('A') + i) for i in range(len(robots))]
    # ロボットごとの経路を格納するリスト
    robot_paths = [None] * len(robots)
    while waypoints:
        for robot, label in zip(robots, robot_labels):
            if not waypoints:
                break

            closest_waypoint = None
            min_distance = float('inf')
            robot_path = None

            for waypoint in waypoints:
                path = a_star(robot, waypoint, NEW_MAP_SIZE)
                if path:
                    distance = len(path)
                    if distance < min_distance:
                        min_distance = distance
                        closest_waypoint = waypoint
                        robot_path = path

            if closest_waypoint:
                waypoints.remove(closest_waypoint)
                visited_waypoints.add(closest_waypoint)
                # ロボットの経路を更新
                robot_index = robots.index(robot)
                robot_paths[robot_index] = robot_path
                robots[robot_index] = robot_path[-1]  # ロ
                # print(f"{label} at {robot} moves to waypoint {closest_waypoint} following path {robot_path}")

                print(f"{label} at {invert_coordinates(robot, ORIGINAL_MAP_SIZE, NEW_MAP_SIZE)} moves to waypoint {invert_coordinates(closest_waypoint, ORIGINAL_MAP_SIZE, NEW_MAP_SIZE)}")

    print("All waypoints visited.")


if __name__ == "__main__":
    robots = create_robots(2, ORIGINAL_MAP_SIZE)
    waypoints = create_random_waypoints(NUM_WAYPOINTS, ORIGINAL_MAP_SIZE)
    main(robots,waypoints )


