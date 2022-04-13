import math

class Asteroid:
    def __init__(self,speed_x, speed_y, pos_x, pos_y, size):
        """
        creates a new asteroid, with position and initial velocity (x,y) and size between 1 and 3
        :param speed_x: initial x speed coordinate
        :param speed_y: initial y speed coordinate
        :param pos_x: initial x coordinate
        :param pos_y: initial y coordinate
        :param size: initial size
        """
        self.__speed_x = speed_x
        self.__speed_y = speed_y
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__size = size

    def get_size(self):
        """
        :return: asteroid size
        """
        return self.__size

    def get_pos(self):
        """
        :return: asteroid position as tuple (x,y)
        """
        return self.__pos_x, self.__pos_y

    def get_speed(self):
        """
        :return: asteroid speed as tuple (x,y)
        """
        return self.__speed_x, self.__speed_y

    def set_pos(self, pos):
        """
        sets the asteroid at pos
        :param pos: position for the asteroid to be placed, tuple of the form (x,y)
        """
        self.__pos_x = pos[0]
        self.__pos_y = pos[1]

    def get_radius(self):
        """
        :return: asteroid radius
        """
        return (self.__size * 10) - 5

    def has_intersection(self, obj):
        """
        checks for intersection between the asteroid and obj
        :param obj: object to check if it intersects with the asteroid
        :return: True if the object intersects with the asteroid, False otherwise
        """
        distance = math.sqrt((obj.get_pos()[0] - self.__pos_x)**2 + (obj.get_pos()[1] - self.__pos_y)**2)
        if distance <= self.get_radius() + obj.get_radius():
            # collision
            return True
        return False