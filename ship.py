import math
RADIUS_SHIP = 1
class Ship:
    def __init__(self,pos_x, pos_y, speed_x, speed_y, orientation):
        """
        creates a new ship, with position (x,y), initial speed (x,y) and angle x in degrees
        :param pos_x: initial x coordinate
        :param pos_y: initial y coordinate
        :param speed_x: initial x speed coordinate
        :param speed_y: initial y speed coordinate
        :param orientation: initial orientation
        """
        self.__speed_x = speed_x
        self.__speed_y = speed_y
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__orientation = orientation

    def set_pos(self, pos):
        """
        sets the ship at pos
        :param pos: position for the ship to be placed, tuple of the form (x,y)
        """
        self.__pos_x = pos[0]
        self.__pos_y = pos[1]

    def get_orientation(self):
        """
        :return: ship orientation
        """
        return self.__orientation

    def get_pos(self):
        """
        :return: ship position as tuple (x,y)
        """
        return self.__pos_x, self.__pos_y

    def get_speed(self):
        """
        :return: ship speed as tuple (x,y)
        """
        return self.__speed_x, self.__speed_y

    def rotate_left(self, rotation_left):
        """
        rotates the ship left
        """
        self.__orientation += rotation_left

    def rotate_right(self, rotation_right):
        """
        rotates the ship right
        """
        self.__orientation -= rotation_right

    def accelerate(self):
        """
        accelerates the ship
        """
        self.__speed_x += math.cos(math.radians(self.__orientation))
        self.__speed_y += math.sin(math.radians(self.__orientation))

    def get_radius(self):
        """
        :return: ship radius
        """
        return RADIUS_SHIP