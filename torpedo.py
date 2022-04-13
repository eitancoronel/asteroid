TORPEDO_RADIUS = 4
class Torpedo:
    def __init__(self, pos_x, pos_y, speed_x, speed_y, orientation):
        """
        creates a new torpedo, with position (x,y), initial speed (x,y), angle x in degrees and life 0
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
        self.__life = 0

    def get_orientation(self):
        """
        :return: torpedo orientation
        """
        return self.__orientation

    def get_pos(self):
        """
        :return: torpedo position as tuple (x,y)
        """
        return self.__pos_x, self.__pos_y

    def get_speed(self):
        """
        :return: torpedo speed as tuple (x,y)
        """
        return self.__speed_x, self.__speed_y

    def set_pos(self, pos):
        """
        sets the torpedo at pos
        :param pos: position for the torpedo to be placed, tuple of the form (x,y)
        """
        self.__pos_x = pos[0]
        self.__pos_y = pos[1]

    def get_radius(self):
        """
        :return: torpedo radius
        """
        return TORPEDO_RADIUS

    def set_life_plus_one(self):
        """
        sets torpedo life
        """
        self.__life += 1

    def get_life(self):
        """
        :return: torpedo life
        """
        return self.__life