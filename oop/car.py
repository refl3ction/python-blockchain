from vehicle import Vehicle


class Car(Vehicle):

    def brag(self):
        print('My car is cool.')


car1 = Car()
car1.drive()

print(car1)
print(car1.get_warning())
