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

def decay_pheromones(pheromone_trails: dict[int: dict], decay_coefficient: float):
    for start_city, destination_cities in pheromone_trails:
        for k, destination_city in destination_cities:
            destination_city = destination_city * decay_coefficient




## ======================================================================
## Program Run
start_time = time.time()

cities_map = get_cities_from_file("../TravellingSalesman/ulysses16(1).csv")
city_list = get_list_of_cities(cities_map)

pheromone_trails = get_pheromone_trails([0,1,2,3])

decay = 0.5

decay_pheromones(pheromone_trails, decay)

print(pheromone_trails)


## Program End
end_time = time.time()
## ======================================================================
print(f"\n\nTime: {end_time-start_time}\n========================================")