import math
import random
import time
from typing import Dict

def get_cities_from_file(file_name):
    csv_file = open(file_name, "r")
    cities_map = []
    for line in csv_file:
        city = []
        for coord in line.split(","):
            coord = coord.rstrip()
            city += [float(coord)]
        cities_map += [city]

    return cities_map

def get_list_of_cities(cities_map):
    return list(range(len(cities_map)))

def get_cost_of_route(route, cities_map):
    total = 0
    i = 0

    while i < len(route)-1:
        total += get_cost_between_cities(cities_map, route[i],route[i+1])
        i += 1
    total += get_cost_between_cities(cities_map, route[-1], route[0])

    return total

def get_cost_between_cities(cities_map, city_1, city_2):

    return distance_between_coords(cities_map[city_1][0],
                                cities_map[city_2][0],
                                cities_map[city_1][1],
                                cities_map[city_2][1])

def distance_between_coords(x1, x2, y1, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def generate_random_route(city_list):
    copy = city_list[1:]
    random.shuffle(copy)
    city_list[1:] = copy
    return city_list

def get_pheromone_trails(city_list):
    return {first_city: {second_city: 1 for second_city in city_list if second_city > first_city} for first_city in city_list if first_city < len(city_list)-1}

def decay_pheromones(pheromone_trails: dict, decay_coefficient: float):
    for start_city in pheromone_trails:
        for destination_city in pheromone_trails[start_city]:
            pheromone_trails[start_city][destination_city] = pheromone_trails[start_city][destination_city] * decay_coefficient

def update_pheromones_for_route(cities_map, pheromone_trails, route: list, coefficient):
    length = get_cost_of_route(route, cities_map)
    i = 0

    while i < len(route)-1:
        temp = [route[i], route[i+1]]
        temp.sort()
        pheromone_trails[temp[0]][temp[1]] += coefficient/length
        i += 1
    temp = [route[0], route[-1]]
    temp.sort()
    pheromone_trails[temp[0]][temp[1]] += coefficient/length

def find_closest_city(cities_map, city_list, current_city, visited):
    possible_cities = [city for city in city_list if city not in visited]
    closest_city = random.choice(possible_cities)
    closest_distance = get_cost_between_cities(cities_map, current_city, closest_city)

    for city in possible_cities:
        city_distance = get_cost_between_cities(cities_map, current_city, city)
        if  city_distance < closest_distance:
            closest_distance = city_distance
            closest_city = city

    return closest_city

def greedy_construct_route(cities_map, city_list: list):
    next_city = random.choice(city_list)
    greedy_route = []
    greedy_route.append(next_city)

    i = 0
    while i < len(city_list) -1:
        next_city = find_closest_city(cities_map, city_list, next_city, greedy_route)
        greedy_route.append(next_city)
        i+=1

    return greedy_route

## ======================================================================
## Program Run
start_time = time.time()

cities_map = get_cities_from_file("../TravellingSalesman/ulysses16(1).csv")
city_list = get_list_of_cities(cities_map)

# pheromone_trails = get_pheromone_trails([0,1,2,3])

# print(pheromone_trails)

# update_pheromones_for_route(cities_map, pheromone_trails, [0,1,3,2], 8)

# print(pheromone_trails)

route = greedy_construct_route(cities_map, city_list)
print(route)
print(get_cost_of_route(route, cities_map))


## Program End
end_time = time.time()
## ======================================================================
print(f"\n\nTime: {end_time-start_time}\n========================================")