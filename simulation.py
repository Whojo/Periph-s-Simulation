import math
import random
import PySimpleGUI as sg

ROAD_LEN = 70000
NB_CARS = 13
DEFAULT_SPEED = 140

PERIPH_CENTER = (200, 200)
CAR_RADIUS = 12
ROAD_WIDTH = 40
OUTER_RADIUS = 150
INNER_RADIUS = OUTER_RADIUS - ROAD_WIDTH

road = [0] * ROAD_LEN # the road : 0 = no car/ 1 = a car
cars_id = [0] * NB_CARS # index of the car on the road
cars_speed = [DEFAULT_SPEED] * NB_CARS

def is_space_available(space):
    """
    Check that the SPACE_BETWEEN_CARS is respected if a car is added at space
    """
    SPACE_BETWEEN_CARS = 3500
    i = -SPACE_BETWEEN_CARS + 1
    while i < SPACE_BETWEEN_CARS and road[(space + i) % ROAD_LEN] == 0:
        i += 1

    return i >= SPACE_BETWEEN_CARS

def init_cars():
    """
    Initialize the cars on the road
    """
    TRIES_LIMIT = 100
    for i in range(NB_CARS):
        # Find a space for the new car
        space = random.randint(0, ROAD_LEN)
        tries = 0
        while tries < TRIES_LIMIT and not is_space_available(space):
            space = random.randint(0, ROAD_LEN)
            tries += 1

        if tries == TRIES_LIMIT:
            print(f"{i} is the maximum amount of cars on this road")
            return

        # Alocate the space to the new car
        cars_id[i] = space
        road[cars_id[i]] = 1

def move_cars():
    """
    Move all the car respectively to their behavior
    """
    # Calculate new position
    for i in range(NB_CARS):
        move_car(i)

    # Redraw it
    for car_image, i in zip(cars_image, cars_id):
        x, y = x_y_to_circle(i)
        x, y = x_y_to_graph(x, y, INNER_RADIUS + ROAD_WIDTH / 2)

        # Relocate() does not use the same marker as DrawCircle(), so it must be adjusted with CAR_RADIUS
        graph.RelocateFigure(car_image, x - CAR_RADIUS, y + CAR_RADIUS) 

def move_car(i):
    """
    Adjust the speed of the car and move it
    """
    # Adjust the speed of the car
    

    # Move the car
    road[cars_id[i]] = 0
    cars_id[i] = (cars_id[i] + cars_speed[i]) % ROAD_LEN
    road[cars_id[i]] = 1

def x_y_to_circle(i):
    """
    Transform the index of the list to (x, y) on the circle
    """
    T = i / ROAD_LEN * 2 * math.pi
    return math.cos(T), math.sin(T)

def x_y_to_graph(x, y, radius):
    """
    Transform (x, y) of the circle to the actual (x, y) of the graph
    """
    return PERIPH_CENTER[0] + x * radius, PERIPH_CENTER[1] + y * radius

def create_a_slow_down():
    """
    Randomly choose a car and slow it a little bit
    """
    rdn_car = random.randint(0, NB_CARS)

def send_the_cleaners():
    """
    Add cleaners cars on the periph; Define their speed
    """
    pass



### MAIN ###
simulation = [
    [
        sg.Graph(canvas_size=(400, 400), graph_bottom_left=(0,0),
            graph_top_right=(400, 400), key='graph')
    ]
]

options = [
    [sg.Text("Actions")],
    [sg.Button("Create a Slow Down")],
    [sg.Button("Send the Cleaners")]
]

layout = [
    [sg.Text("Periph's Simulation")],
    [
        sg.Column(simulation),
        sg.VSeperator(),
        sg.Column(options),
    ]
]

# Create the window
window = sg.Window("Periph's Simulation", layout)
window.Finalize()

# Draw the Periph
graph = window['graph']
outer_circle = graph.DrawCircle(PERIPH_CENTER, OUTER_RADIUS, line_color='white')
inner_circle = graph.DrawCircle(PERIPH_CENTER, INNER_RADIUS, line_color='white')

# Draw the cars
cars_image = []
init_cars()
for car_id in cars_id:
    x, y = x_y_to_circle(car_id)
    x, y = x_y_to_graph(x, y, INNER_RADIUS + ROAD_WIDTH / 2)
    car = graph.DrawCircle((x, y), CAR_RADIUS, fill_color='red')
    cars_image.append(car)

# Create an event loop
while True:
    event, values = window.read(timeout=20)

    if event == sg.WIN_CLOSED:
        break
    if event == "Create a Slow Down":
        create_a_slow_down()
    if event == "Send the Cleaners":
        send_the_cleaners()

    # Moving the cars
    move_cars()

window.close()
