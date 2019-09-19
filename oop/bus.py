from vehicle import Vehicle


class Bus(Vehicle):

    def __init__(self, starting_top_speed=100):
        super().__init__(starting_top_speed)
        self.passengers = []

    def add_group(self, passengers):
        self.passengers.extend(passengers)


bus = Bus(150)
bus.add_warnings('Testing')
bus.add_group(['Denis', 'Max'])

print(bus)
print(bus.passengers)
