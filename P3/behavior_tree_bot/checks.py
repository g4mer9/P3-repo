

def if_neutral_planet_available(state):
    return any(state.neutral_planets())

def if_planet_in_range(state):
    return any(state.distance(p.ID, q.ID) <= 20 for p in state.my_planets() for q in state.not_my_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

def is_a_weak_planet(state): 
    #check if there are any weak planets 
    my_planets = state.my_planets()
    if not my_planets:
        return False 
    #add up the total amount of ships in all planets
    total_ships = 0 
    for planet in my_planets:
        total_ships += planet.num_ships
      
    #calculate average
    average_num_ships = total_ships / len(my_planets)
    threshold = 0.8 * average_num_ships
    #return any planet that has less ships than the average (weak planet) 
    return any(planet.num_ships < threshold for planet in my_planets) 
      
    