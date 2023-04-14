import heapq
import threading
import numpy as np
import random
from itertools import permutations

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(graph, start, end):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        current = heapq.heappop(frontier)[1]

        if current == end:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(end, next)
                heapq.heappush(frontier, (priority, next))
                came_from[next] = current

    return came_from, cost_so_far

def reconstruct_path(came_from, start, end):
    path = [end]
    node = end
    while node != start:
        node = came_from[node]
        path.append(node)
    path.reverse()
    return path

class Graph:
    def __init__(self, map_size, waypoints):
        self.map_size = map_size
        self.waypoints = waypoints

    def in_bounds(self, pos):
        x, y = pos
        return 0 <= x < self.map_size[0] and 0 <= y < self.map_size[1]

    def neighbors(self, pos):
        x, y = pos
        neighbors = [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        return [n for n in neighbors if self.in_bounds(n)]

    def cost(self, current, next):
        return 1


def create_random_waypoints(number_of_waypoints, map_size):
    return [(random.randint(0, map_size[0] - 1), random.randint(0, map_size[1] - 1)) for _ in range(number_of_waypoints)]


def calculate_path_length(path, graph):
    length = 0
    for i in range(len(path) - 1):
        length += graph.cost(path[i], path[i + 1])
    return length

def two_opt_swap(route, i, k):
    return route[:i] + route[i:k + 1][::-1] + route[k + 1:]

def two_opt(path, graph):
    best_path = path
    best_length = calculate_path_length(path, graph)

    improved = True
    while improved:
        improved = False
        for i in range(1, len(best_path) - 2):
            for k in range(i + 1, len(best_path) - 1):
                new_path = two_opt_swap(best_path, i, k)
                new_length = calculate_path_length(new_path, graph)

                if new_length < best_length:
                    best_path = new_path
                    best_length = new_length
                    improved = True

    return best_path

def assign_waypoints(robot_positions, waypoints):
    assigned_waypoints = [[] for _ in robot_positions]
    shortest_paths = [[] for _ in robot_positions]
    min_total_distance = float('inf')

    for perm in permutations(waypoints):
        total_distance = 0
        for i, (start, assigned_waypoint) in enumerate(zip(robot_positions, perm)):
            total_distance += heuristic(start, assigned_waypoint)
            assigned_waypoints[i].append(assigned_waypoint)
            shortest_paths[i].append((start, assigned_waypoint))

        if total_distance < min_total_distance:
            min_total_distance = total_distance
            best_assigned_waypoints = [tuple(waypoint) for waypoint in assigned_waypoints]
            best_shortest_paths = shortest_paths
    return best_assigned_waypoints, best_shortest_paths

def robot_path(start, waypoints, map_size, robot_name):
    graph = Graph(map_size, waypoints)
    path = []

    for waypoint in waypoints:
        came_from, cost_so_far = a_star(graph, start, waypoint)
        partial_path = reconstruct_path(came_from, start, waypoint)
        path += partial_path[:-1]
        start = waypoint

    path.append(waypoints[-1])
    optimized_path = two_opt(path, graph)

    print(f"ロボット {robot_name} の経路: {optimized_path}")

def main():
    robot_positions = [(3, 3), (2, 7), (6, 9)]
    number_of_waypoints = 5
    map_size = (20, 20)
    robot_names = ['A', 'B', 'C']
    threads = []

    waypoints = create_random_waypoints(number_of_waypoints, map_size)
    assigned_waypoints, shortest_paths = assign_waypoints(robot_positions, waypoints)

    for i, (position, waypoints) in enumerate(zip(robot_positions, assigned_waypoints)):
        thread = threading.Thread(target=robot_path, args=(position, waypoints, map_size, robot_names[i]))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
