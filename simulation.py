import math
import random
import PySimpleGUI as sg

class car:
    def __init__(self, pos, speed):
        self.pos = pos
        self.speed = speed

    def set_image(self, image):
        self.image = image


class peripherique:
    ROAD_LEN = 70000
    NB_CARS = 13
    DEFAULT_SPEED = 140

    CENTER = (200, 200)
    CAR_RADIUS = 12
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

    def is_space_available(self, id):
        """
        Check that the SPACE_BETWEEN_CARS is respected if a car is added at this id
        """
        SPACE_BETWEEN_CARS = 3500
        i = -SPACE_BETWEEN_CARS + 1
        while i < SPACE_BETWEEN_CARS and self.road[(id + i) % self.ROAD_LEN] == 0:
            i += 1

        return i >= SPACE_BETWEEN_CARS

    def init_cars(self):
        """
        Initialize the cars on the road
        """
        TRIES_LIMIT = 100
        for i in range(self.NB_CARS):
            # Find a id for the new car
            id = random.randint(0, self.ROAD_LEN)
            tries = 0
            while tries < TRIES_LIMIT and not self.is_space_available(id):
                id = random.randint(0, self.ROAD_LEN)
                tries += 1

            if tries == TRIES_LIMIT:
                print(f"{i} is the maximum amount of cars on this road")
                return

            # Alocate the id to the new car
            self.cars.append(car(id, self.DEFAULT_SPEED))
            self.road[id] = 1

    def move_car(self, i):
        """
        Adjust the speed of the car and move it
        """
        # Adjust the speed of the car


        # Move the car
        self.road[self.cars[i].pos] = 0
        self.cars[i].pos = (self.cars[i].pos + self.cars[i].speed) % self.ROAD_LEN
        self.road[self.cars[i].pos] = 1

    def x_y_to_circle(self, i):
        """
        Transform the index of the list to (x, y) on the circle
        """
        T = i / self.ROAD_LEN * 2 * math.pi
        return math.cos(T), math.sin(T)

    def x_y_to_graph(self, x, y, radius):
        """
        Transform (x, y) of the circle to the actual (x, y) of the graph
        """
        return self.CENTER[0] + x * radius, self.CENTER[1] + y * radius

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


class graph:
    GRAPH_SIZE = (400, 400)
    SIMULATION = [
        [
            sg.Graph(canvas_size=GRAPH_SIZE, graph_bottom_left=(0,0),
                graph_top_right=GRAPH_SIZE, key='graph')
        ]
    ]

    OPTION = [
        [sg.Text("Actions")],
        [sg.Button("Create a Slow Down")],
        [sg.Button("Send the Cleaners")]
    ]

    LAYOUT = [
        [sg.Text("Periph's Simulation")],
        [
            sg.Column(SIMULATION),
            sg.VSeperator(),
            sg.Column(OPTION),
        ]
    ]

    def __init__(self, periph):
        """
        Open the window and print its content
        """
        self.periph = periph

        self.window = sg.Window("Periph's Simulation", self.LAYOUT)
        self.graph = self.window['graph']
        self.window.Finalize()

        self.draw_periph()
        self.draw_cars()

    def draw_periph(self):
        """
        Draw 2 circles to represent the sides of the road
        """
        self.outer_circle = self.graph.DrawCircle(self.periph.CENTER, self.periph.OUTER_RADIUS, line_color='white')
        self.inner_circle = self.graph.DrawCircle(self.periph.CENTER, self.periph.INNER_RADIUS, line_color='white')

    def draw_cars(self):
        """
        Draw circles that represent the cars
        """
        for car in self.periph.cars:
            x, y = self.periph.x_y_to_circle(car.pos)
            x, y = self.periph.x_y_to_graph(x, y, self.periph.INNER_RADIUS + self.periph.ROAD_WIDTH / 2)
            image = self.graph.DrawCircle((x, y), self.periph.CAR_RADIUS, fill_color='red')
            car.set_image(image)

    def move_cars(self):
        """
        Move all the car respectively to their behavior
        """
        # Calculate new position
        for i in range(self.periph.NB_CARS):
            self.periph.move_car(i)

        # Redraw it
        for car in self.periph.cars:
            x, y = self.periph.x_y_to_circle(car.pos)
            x, y = self.periph.x_y_to_graph(x, y, self.periph.INNER_RADIUS + self.periph.ROAD_WIDTH / 2)

            # Relocate() does not use the same marker as DrawCircle(), so it must be adjusted with CAR_RADIUS
            self.graph.RelocateFigure(car.image, x - self.periph.CAR_RADIUS, y + self.periph.CAR_RADIUS) 

    def start_loop(self):
        """
        Create the event loop that manage buttons and cars' movements
        """
        while True:
            event, values = self.window.read(timeout=20)

            if event == sg.WIN_CLOSED:
                break
            if event == "Create a Slow Down":
                self.periph.create_a_slow_down()
            if event == "Send the Cleaners":
                self.periph.send_the_cleaners()

            self.move_cars()

        self.window.close()


### MAIN ###
if __name__== "__main__":
    periph = peripherique()
    graph = graph(periph)
    graph.start_loop()
