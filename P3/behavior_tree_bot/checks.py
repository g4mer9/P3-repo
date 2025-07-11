

def if_neutral_planet_available(state):
    return any(state.neutral_planets())

def if_planet_in_range(state):
    return any(state.distance(p.ID, q.ID) <= 20 for p in state.my_planets() for q in state.not_my_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())
