from car import Car
from peripherique import Peripherique
from graph import Graph

if __name__== "__main__":
    periph = Peripherique()
    graph = Graph(periph)
    graph.start_loop()
