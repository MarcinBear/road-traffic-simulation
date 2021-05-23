import numpy as np


class Car:

    def __init__(self, x, y, direction):
        self.x = x  # spawn x
        self.y = y  # spawn y
        self.direction = direction
        self.out = False

    def position(self):
        return self.x, self.y

    def move(self):
        self.x += self.direction[0]
        self.y += self.direction[1]

    def wait(self):
        pass

    def bye_bye(self):
        for _ in range(5):
            self.move()
        self.direction = [0, 0]

    def __copy__(self):
        return type(self)(self.x, self.y, self.direction)


class Grid:

    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        self.grid = np.zeros((self.max_x, self.max_y), dtype='object')

    def reset(self):
        self.grid = np.zeros((self.max_x, self.max_y), dtype='object')

    def set_one(self, i, j):
        self.grid[i, j] = 1

    def set_blockade(self, i, j, direction):
        self.grid[i, j] = direction

    def set_zero(self, i, j):
        self.grid[i, j] = 0

    def update(self, state):
        self.reset()
        for i, j in state:
            self.set_one(i, j)


class TrafficLights:

    def __init__(self, town_map, in_direction, position, tau, pi, sigma):

        up, down, left, right = [0, 1], [0, -1], [-1, 0], [1, 0]
        self.town_map = town_map
        self.in_direction = in_direction
        self.position = position
        self.out_directions = [up, down, left, right]
        self.tau = tau      # green light duration
        self.pi = pi        # new direction distribution
        self.sigma = sigma  # red lights durations for other roads after green light goes out
        self.green = False
        self.time = 0

    def time_update(self):
        self.time += 1

    def light_update(self, t):
        self.green = not self.green

    def new_direction(self):
        p = np.array(self.pi) / sum(self.pi)
        index = int(np.random.choice(4, 1, p=p))
        return self.out_directions[index]

    def set_red(self):
        self.green = False
        self.town_map.set_blockade(self.position[0], self.position[1], self.in_direction)

    def set_green(self):
        self.green = True
        self.town_map.set_zero(self.position[0], self.position[1])

    def change_light(self):
        if self.green:
            self.set_red()
        else:
            self.set_green()


class Intersection:

    def __init__(self, traffic_lights):
        self.time = 0
        self.traffic_lights = traffic_lights
        self.active_light = self.traffic_lights[0]
        self.active_light.set_green()
        self.time = 0

    def update_current(self):
        self.traffic_lights = np.roll(self.traffic_lights, -1)
        self.active_light = self.traffic_lights[0]

    def tick(self):
        # self.time += 1
        if self.time == 0:
            self.update_current()
            for light in self.traffic_lights:
                light.set_red()
            self.active_light.set_green()
        elif self.time > self.active_light.tau:
            self.active_light.set_red()
            self.time = -self.active_light.sigma
        self.time += 1


lam1 = lambda t: 0.8 + 0.8 * np.sin(t/2)
lam2 = lambda t: np.exp((2 * np.sin(t/12 + 3) - 0.9)**3)
lam3 = lambda t: 0.5
lam4 = lambda t: 0.7 + 0.6 * np.sin(t/7 + 2)**2 * np.cos(t/3 + 1)
lam5 = lambda t: 0.2 + 0.2 * np.sign(np.sin(t/24 + 6))
lam6 = lambda t: 0.1 + 0.1 * np.sin(np.sqrt(t))
lam7 = lambda t: 0.3 + 0.3 * np.sin(4 * np.sin(t/2))


def inhomogeneous_poisson(lam, T, M=None):
    if M is None:
        M = max(np.vectorize(lam)(np.linspace(0, T, int(1000 * T))))
    S = []
    t = 0
    U1 = np.random.uniform(0, 1)
    t = t - 1 / M * np.log(U1)
    while t < T:
        U2 = np.random.uniform(0, 1)
        if U2 <= lam(t) / M:
            S.append(t)
        U1 = np.random.rand()
        t = t - 1 / M * np.log(U1)
    return np.array(S)


def generate_arrivals(lam, T, scale=10, M=None):
    S = inhomogeneous_poisson(lam, T, M)
    S = scale * S
    if S.size in (0, 1):
        return np.array([99999, 99999])  # adding big numbers to prevent from IndexError
    else:
        S = S - S[0]
        return np.hstack((np.round(S), np.array([99999, 99999])))  # adding big numbers to prevent from IndexError
