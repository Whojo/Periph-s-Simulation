class Car:
    RADIUS = 12
    def __init__(self, pos, speed):
        self.pos = pos
        self.speed = speed
        self.next = None

    def set_image(self, image):
        self.image = image
