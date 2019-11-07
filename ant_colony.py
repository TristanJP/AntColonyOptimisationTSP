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

def get_cities_probability_list(cities_map, city_list, pheromone_trails, current_city, possible_cities):
    # NEEDS WORK

    alpha = 1
    beta = 1

    value = lambda alpha, beta, cities : math.pow(pheromone_trails[cities[0]][cities[1]], alpha) * (1/math.pow(get_cost_between_cities(cities_map, current_city, city), beta))

    my_dict = {city: 0 for city in city_list if not current_city}
    for city in city_list:
        if city == current_city: 
            my_dict[city] = 0 
            continue
        cities = [current_city, city]
        cities.sort()
        my_dict[city] = value(alpha, beta, cities)
        if city not in possible_cities:
            my_dict[city] = 0
    return my_dict

def ant_choose_city(cities_map, city_list, pheromone_trails, current_city, visited_cities):
    possible_cities = [city for city in city_list if city not in visited_cities]

    city_probabilities = get_cities_probability_list(cities_map, city_list, pheromone_trails, current_city, possible_cities)

    running_total = 0
    for city, probability in city_probabilities.items():
        running_total += probability
        city_probabilities[city] = running_total

    i = random.random() * city_probabilities[len(city_probabilities)-1]

    next_city = 0
    for city in city_probabilities:
        if i <= city_probabilities[city]:
            next_city = city
            break

    return city

def ant_construct_route(cities_map, city_list, pheromone_trails):
    new_route = []
    start = random.choice(city_list)
    new_route.append(start)
    i = 0
    while i < len(city_list) -1:
        new_route.append(ant_choose_city(cities_map,city_list,pheromone_trails,new_route[-1],new_route))
        i+= 1
    
    return new_route

def ant_search(cities_map, city_list, pheromone_trails, steps):
    i = 1
    while i <= steps:
        route = ant_construct_route(cities_map, city_list, pheromone_trails)
        decay_pheromones(pheromone_trails, 0.5)
        update_pheromones_for_route(cities_map,pheromone_trails,route,1)
        print(f"{i}: {route} ({get_cost_of_route(route, cities_map)})")
        i += 1
    return route

## ======================================================================
## Program Run
start_time = time.time()

cities_map = get_cities_from_file("../TravellingSalesman/ulysses16(1).csv")
city_list = get_list_of_cities(cities_map)
pheromone_trails = get_pheromone_trails(city_list)

route = ant_search(cities_map,city_list,pheromone_trails,1000)

print(route)
print(get_cost_of_route(route, cities_map))

## Program End
end_time = time.time()
## ======================================================================
print(f"\n\nTime: {end_time-start_time}\n========================================")