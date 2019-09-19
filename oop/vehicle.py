class Vehicle:

    def __init__(self, starting_top_speed=100):
        self.top_speed = starting_top_speed
        self.__warnings = []  # Convetion to not change this attribute from outside the class
        pass

    def __repr__(self):
        # Representation of the object when print is called
        return f'Top Speed: {self.top_speed}, Warnings: {self.__warnings}'

    def add_warnings(self, warning):
        self.__warnings.append(warning)

    def get_warning(self):
        return self.__warnings

    def drive(self):
        print('I am driving but not faster than {}'.format(self.top_speed))
