import math
import random
from car import Car

class Peripherique:
    ROAD_LEN = 70000
    NB_CARS = 13
    DEFAULT_SPEED = 140

    CENTER = (200, 200)
    ROAD_WIDTH = 40
    OUTER_RADIUS = 150
    INNER_RADIUS = OUTER_RADIUS - ROAD_WIDTH

    def __init__(self):
        """
        Initialize the road and the cars
        """
        self.road = [0] * self.ROAD_LEN # the road : 0 = no car/ 1 = a car
        self.cars = []
        self.init_cars()

    @classmethod
    def x_y_to_circle(cls, pos, radius):
        """
        Transform the index of the list to (x, y) on the circle
        """
        angle = pos / cls.ROAD_LEN * 2 * math.pi
        return (cls.CENTER[0] + math.cos(angle) * radius,
                cls.CENTER[1] + math.sin(angle) * radius)

    def is_space_available(self, id):
        """
        Check that the SPACE_BETWEEN_CARS is respected if a car is added at this id
        """
        SPACE_BETWEEN_CARS = 3500
        space = -SPACE_BETWEEN_CARS + 1
        while space < SPACE_BETWEEN_CARS and self.road[(id + space) % self.ROAD_LEN] == 0:
            space += 1

        return space >= SPACE_BETWEEN_CARS

    def init_cars(self):
        """
        Initialize the cars on the road
        """
        TRIES_LIMIT = 100
        for nb_car in range(self.NB_CARS):
            # Find a id for the new car
            id = random.randint(0, self.ROAD_LEN)
            tries = 0
            while tries < TRIES_LIMIT and not self.is_space_available(id):
                id = random.randint(0, self.ROAD_LEN)
                tries += 1

            if tries == TRIES_LIMIT:
                print(f"{nb_car} is the maximum amount of cars on this road")
                return

            # Alocate the id to the new car
            self.cars.append(Car(id, self.DEFAULT_SPEED))
            self.road[id] = 1

    def move_car(self, car):
        """
        Adjust the speed of the car and move it
        """
        # Adjust the speed of the car


        # Move the car
        self.road[car.pos] = 0
        car.pos = (car.pos + car.speed) % self.ROAD_LEN
        self.road[car.pos] = 1

    def create_a_slow_down(self):
        """
        Randomly choose a car and slow it a little bit
        """
        rdn_car = random.randint(0, self.NB_CARS)
        # TODO: Finish it

    def send_the_cleaners(self):
        """
        Add cleaners cars on the periph; Define their speed
        """
        pass # TODO
