import sys
sys.path.insert(0, '../')
from planet_wars import issue_order
from random import choice
import logging


def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)
    
def production_attempt(state):
    
    # looping over all planets to find the first one that has enough ships to send and is close enough to the target planet
    for my_planet in state.my_planets():
    
        # grab all target planets that are not currently targeted by my fleets
        # and sort them by number of ships
        target_planets = [planet for planet in state.not_my_planets()
                        if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
        target_planets = sorted(target_planets, key=lambda p: p.num_ships, reverse=False)

        if target_planets:
            # target the weakest planet
            target_planet = target_planets[0]
            if(target_planet.owner == 0):
                # if the target planet is neutral, we can send any number of ships
                required_ships = target_planet.num_ships + 1
            else:
                # if the target planet is owned by an enemy, we need to send enough ships to conquer it
                required_ships = target_planet.num_ships + state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate + 1
            # if we have enough ships to send, issue the order
            if my_planet.num_ships > required_ships:
                return issue_order(state, my_planet.ID, target_planet.ID, required_ships)
    return False

def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

#defensive strategy
def reinforce_weakest_planets(state):
    #find which planets can send fleets to help weaker planets
    total_ships = sum(planet.num_ships for planet in state.my_planets())
    if len(state.my_planets()) != 0:
        average_before_threshold = total_ships / len(state.my_planets()) 
    else: 
        return False
    average_ships = average_before_threshold * 0.8

    #track if the action occurred:
    action_occurred = False 

    #make lists of the stronger and weaker planets 
    stronger_planets = [planet for planet in state.my_planets() if planet.num_ships > average_ships]
    weaker_planets = [planet for planet in state.my_planets() if planet.num_ships < average_ships]

    for weak_planet in weaker_planets: #for each weaker planet, find a nearby strong planet
        planet_distances = {} 
        #make a dictionary of all the distances so we can find the minimum 
        #distance (key = planet.ID, value = planet distance)
        for strong_planet in stronger_planets: 
            #find the distance between the current weak and strong planets
            distance = state.distance(weak_planet.ID, strong_planet.ID) 
            planet_distances[strong_planet.ID] = distance
        nearest_strong_planet_id = min(planet_distances, key = planet_distances.get) 
        #attach the id to the planet object
        nearest_strong_planet = None
        for planet in stronger_planets: 
            if planet.ID == nearest_strong_planet_id:
                nearest_strong_planet = planet
                break
        #now that we know which planet will be sending reinforcement to the current weak planet, 
        # we need to figure out how much it will send
        weak_receives = average_ships - weak_planet.num_ships #how many it needs to be at the average
        #how many can the strong one give before its at the average
        strong_gives = nearest_strong_planet.num_ships - average_ships 

        if (strong_gives <= 0) or (weak_receives <= 0):
            continue #dont do anything 
        #strong cannot send all that weak needs, but will send as much as it can :
        elif (weak_receives >= strong_gives) and strong_gives > 0: 
            issue_order(state, nearest_strong_planet.ID, weak_planet.ID, strong_gives)
            action_occurred = True
        else: #(strong_gives > weak_receives) and weak_receives > 0, strong has more than enough ships to send, 
            #so it will just send what weak needs
            issue_order(state, nearest_strong_planet.ID, weak_planet.ID, weak_receives)
            action_occurred = True
        
    return action_occurred



            






    

        
    

