import PySimpleGUI as sg
from peripherique import Peripherique

class Graph:
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
        self.outer_circle = self.graph.DrawCircle(Peripherique.CENTER,
                Peripherique.OUTER_RADIUS, line_color='white')
        self.inner_circle = self.graph.DrawCircle(Peripherique.CENTER,
                Peripherique.INNER_RADIUS, line_color='white')

    def draw_cars(self):
        """
        Draw circles that represent the cars
        """
        car = self.periph.cars.next
        while car:
            x, y = Peripherique.x_y_to_circle(car.pos,
                    Peripherique.INNER_RADIUS + Peripherique.ROAD_WIDTH / 2)
            image = self.graph.DrawCircle((x, y), car.RADIUS, fill_color='red')
            car.set_image(image)

            car = car.next

    def move_cars(self):
        """
        Move all the car respectively to their behavior
        """
        car = self.periph.cars.next
        while car:
            self.periph.move_car(car)

            x, y = Peripherique.x_y_to_circle(car.pos,
                    Peripherique.INNER_RADIUS + Peripherique.ROAD_WIDTH / 2)

            # Relocate() does not use the same marker as DrawCircle(), so it must be adjusted with CAR_RADIUS
            self.graph.RelocateFigure(car.image, x - car.RADIUS, y + car.RADIUS) 

            car = car.next

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
