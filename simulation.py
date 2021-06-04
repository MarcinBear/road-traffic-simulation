import numpy as np

from utils import *


def simulation(T, intensity_scale, params):

    up, down, right, left = [0, 1], [0, -1], [1, 0], [-1, 0]
    town_map = Grid(50, 50)
    bounds_x = [-1, 43]
    bounds_y = [-1, 30]

    car_models = {
                  'A': (12, 0,  up),
                  'B': (28, 0,  up),
                  'C': (42, 20, left),
                  'D': (0, 18,  right),
                  'E': (10, 29, down),
                  'F': (35, 29, down),
                  'G': (26, 29, down)
                  }

    lambdas = [lam1, lam2, lam3, lam4, lam5, lam6, lam7]
    roads = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    cars = []
    arrivals = {}
    states = []
    light_colors = []
    light_params = {}

    for index, light in enumerate(params):
        light_params[f'tau{index + 1}'] = light['T(🟢)']
        light_params[f'sigma{index + 1}'] = light['T(🔴...)']
        light_params[f'pi{index + 1}'] = [light['P(🡱)'], light['P(🡳)'], light['P(🡰)'], light['P(🡲)']]

    # current direction: UP
    t1  = TrafficLights(town_map,  up, (12, 5), light_params['tau1'], light_params['pi1'], light_params['sigma1'])
    t3  = TrafficLights(town_map,  up, (12, 18), light_params['tau3'], light_params['pi3'], light_params['sigma3'])
    t7  = TrafficLights(town_map,  up, (28, 18), light_params['tau7'], light_params['pi7'], light_params['sigma7'])

    # current direction: DOWN
    t5  = TrafficLights(town_map, down, (10, 20), light_params['tau5'], light_params['pi5'], light_params['sigma5'])
    t9  = TrafficLights(town_map, down, (26, 20), light_params['tau9'], light_params['pi9'], light_params['sigma9'])
    t12 = TrafficLights(town_map, down, (35, 20), light_params['tau12'], light_params['pi12'], light_params['sigma12'])
    t2  = TrafficLights(town_map, down, (10, 7), light_params['tau2'], light_params['pi2'], light_params['sigma2'])

    # current direction: RIGHT
    t4  = TrafficLights(town_map, right, (10, 18), light_params['tau4'], light_params['pi4'], light_params['sigma4'])
    t8  = TrafficLights(town_map, right, (26, 18), light_params['tau8'], light_params['pi8'], light_params['sigma8'])
    t11 = TrafficLights(town_map, right, (35, 18), light_params['tau11'], light_params['pi11'], light_params['sigma11'])

    # current direction: LEFT
    t6  = TrafficLights(town_map, left, (12, 20), light_params['tau6'], light_params['pi6'], light_params['sigma6'])
    t10 = TrafficLights(town_map, left, (28, 20), light_params['tau10'], light_params['pi10'], light_params['sigma10'])
    t13 = TrafficLights(town_map, left, (37, 20), light_params['tau13'], light_params['pi13'], light_params['sigma13'])

    S1 = Intersection([t1, t2])
    S2 = Intersection([t3, t4, t5, t6])
    S3 = Intersection([t7, t8, t9, t10])
    S4 = Intersection([t11, t12, t13])
    intersections = [S1, S2, S3, S4]

    lights_by_position = {(12, 5): t1, (10, 7): t2,  (12, 18): t3, (10, 18): t4, (10, 20): t5, (12, 20): t6, (28, 18): t7,
                          (26, 18): t8, (26, 20): t9, (28, 20): t10, (35, 18): t11, (35, 20): t12, (37, 20): t13}
    lights = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13]

    for i in range(7):
        arrivals[roads[i]] = generate_arrivals(lambdas[i], T, scale=intensity_scale)

    for t_ in range(T):  # ************* MAIN LOOP ************* #

        for intersection in intersections:
            intersection.tick()

        for road in roads:
            while t_ == arrivals[road][0]:
                cars.append(Car(*car_models[road]))
                arrivals[road] = np.delete(arrivals[road], 0)

        for car in cars:
            current_position = car.position()
            current_direction = car.direction
            x = current_position[0]
            y = current_position[1]
            next_x = x + current_direction[0]
            next_y = y + current_direction[1]

            if not car.out:

                if next_x in bounds_x or next_y in bounds_y:
                    car.out = True
                    car.bye_bye()

                else:
                    if current_position in lights_by_position:  # NOTE: if car
                        if lights_by_position[current_position].green:
                            new_direction = lights_by_position[current_position].new_direction()
                            next_x = x + new_direction[0]
                            next_y = y + new_direction[1]
                            if np.cross(current_direction, new_direction) == 1:  # turning left?
                                car.move()
                                car.move()
                            elif current_direction == [-u for u in new_direction]:  # TODO one if below
                                car.move()
                                if car.direction == up:
                                    car.direction = left
                                elif car.direction == down:
                                    car.direction = right
                                elif car.direction == left:
                                    car.direction = down
                                elif car.direction == right:
                                    car.direction = up
                                car.move()
                                car.move()

                            car.direction = new_direction
                            car.move()

                        elif current_position == (35, 21) and current_direction == down:  # TODO more efficient if
                            car.direction = t12.new_direction()
                        else:
                            car.wait()

                    if town_map.grid[next_x, next_y] not in (1, car.direction):  # collision check
                        car.move()
                        town_map.set_one(next_x, next_y)
                    else:  # collision
                        car.wait()

        states.append([car.position() for car in cars])

        town_map.update(states[-1])

        for light in lights:
            if not light.green:
                light.set_red()

        new_colors = []
        for light in lights:
            if light.green:
                new_colors.append("#17a323")
            else:
                new_colors.append("#f55d67")
        light_colors.append(new_colors)

    return states, light_colors
