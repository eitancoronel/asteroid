from screen import Screen
import math
import sys
import random
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
DEFAULT_ASTEROIDS_NUM = 5
INITIAL_LIVES = 3
INITIAL_SCORE = 0
MAX_TORPEDOES = 10
MAX_LIFE_TORPEDO = 200
SCORE_POINTS = {1 : 100, 2: 50, 3: 20}
MIN_INITIAL_ASTEROID_SPEED = 1
MAX_INITIAL_ASTEROID_SPEED = 4
INITIAL_ASTEROID_SIZE = 3
ROTATION_LEFT = 7
ROTATION_RIGHT = 7
QUIT_MSG = "Key q has been pressed \nYou've forced to quit the game!"
WIN_MSG = "You won the game! \n CONGRATULATIONS!!!!"
LOSE_MSG = "You lost the game! \n Come back soon. Maybe next time!"
COLLISION_MSG = ("Collision!", "You've collided with an asteroid \nYou lost 1 life")
END_MSG = "End of the game!"

class GameRunner:

    def __init__(self, asteroids_amount = DEFAULT_ASTEROIDS_NUM):
        self.__screen = Screen()

        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y

        self.__x_delta = self.__screen_max_x - self.__screen_min_x
        self.__y_delta = self.__screen_max_y - self.__screen_min_y

        # creates the ship
        ship_initial_x = random.randint(self.__screen_min_x, self.__screen_max_x)
        ship_initial_y = random.randint(self.__screen_min_y, self.__screen_max_y)
        self.__ship = Ship(ship_initial_x, ship_initial_y, 0, 0, 0)

        # creates the asteroids
        self.__asteroids = []
        # Iterates still there are asteroids_amount on the screen
        while len(self.__asteroids) < asteroids_amount:
            asteroid_initial_x = random.randint(self.__screen_min_x, self.__screen_max_x)
            asteroid_initial_y = random.randint(self.__screen_min_y, self.__screen_max_y)
            self.__asteroid = Asteroid(random.randint(MIN_INITIAL_ASTEROID_SPEED,MAX_INITIAL_ASTEROID_SPEED),
                                       random.randint(MIN_INITIAL_ASTEROID_SPEED,MAX_INITIAL_ASTEROID_SPEED),
                                        asteroid_initial_x, asteroid_initial_y, INITIAL_ASTEROID_SIZE)
            # checks if an asteroid collide with a ship when created
            if self.__asteroid.has_intersection(self.__ship) == False:
                self.__asteroids.append(self.__asteroid)
                self.__screen.register_asteroid(self.__asteroid, self.__asteroid.get_size())

        self.__torpedoes = []
        self.__score = INITIAL_SCORE
        self.__lives = INITIAL_LIVES

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You should not to change this method!
        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        self.conditions_end()
        # actions for the ship
        self.ship_action()

        # actions for the asteroids
        self.asteroid_action()

        # actions for the torpedoes
        if self.__screen.is_space_pressed() and len(self.__torpedoes) < MAX_TORPEDOES:
            speed_x = self.__ship.get_speed()[0] + (2 * math.cos(math.radians(self.__ship.get_orientation())))
            speed_y = self.__ship.get_speed()[1] + (2 * math.sin(math.radians(self.__ship.get_orientation())))
            self.__torpedo = Torpedo(self.__ship.get_pos()[0], self.__ship.get_pos()[1],
                                     speed_x, speed_y, self.__ship.get_orientation())
            self.__screen.register_torpedo(self.__torpedo)
            self.__torpedoes.append(self.__torpedo)
        cur_torp = []
        cur_ast = []
        for torp in self.__torpedoes:
            torp.set_life_plus_one()
            if torp.get_life() >= MAX_LIFE_TORPEDO:
                cur_torp.append(torp)
                continue
            torp.set_pos(self.new_pos(torp.get_pos(), torp.get_speed()))
            self.__screen.draw_torpedo(torp, torp.get_pos()[0], torp.get_pos()[1], torp.get_orientation())
            for ast in self.__asteroids:
                if torp in cur_torp or ast in cur_ast:
                    continue
                else:
                    if ast.has_intersection(torp):
                        # update points
                        self.update_points(ast)
                        # split asteroids (if size > 1) or remove them (if size = 1)
                        if ast.get_size() > 1:
                            self.asteroid_split(torp,ast)
                        cur_ast.append(ast)
                        cur_torp.append(torp)
        # Removes asteroids and torpedoes from the screen and from their class
        for i in cur_ast:
            if i in self.__asteroids:
                self.__screen.unregister_asteroid(i)
                self.__asteroids.remove(i)
        for j in cur_torp:
            if j in self.__torpedoes:
                self.__screen.unregister_torpedo(j)
                self.__torpedoes.remove(j)


    def ship_action(self):
        """
        sets the position and movement of the ship
        """
        self.__ship.set_pos(self.new_pos(self.__ship.get_pos(), self.__ship.get_speed()))
        self.__screen.draw_ship(self.__ship.get_pos()[0], self.__ship.get_pos()[1], self.__ship.get_orientation())
        if self.__screen.is_left_pressed():
            self.__ship.rotate_left(ROTATION_LEFT)
        if self.__screen.is_right_pressed():
            self.__ship.rotate_right(ROTATION_RIGHT)
        if self.__screen.is_up_pressed():
            self.__ship.accelerate()

    def asteroid_action(self):
        """
        sets the position and movement of the asteroids
        """
        ast_curr = []
        for asteroid in self.__asteroids:
            asteroid.set_pos(self.new_pos(asteroid.get_pos(), asteroid.get_speed()))
            self.__screen.draw_asteroid(asteroid, asteroid.get_pos()[0], asteroid.get_pos()[1])
            if asteroid.has_intersection(self.__ship):
                self.__screen.show_message(COLLISION_MSG[0], COLLISION_MSG[1])
                self.__screen.remove_life()
                self.__lives -= 1
                if self.__lives == 0:
                    self.conditions_end()
                ast_curr.append(asteroid)
        for i in ast_curr:
             if i in self.__asteroids:
                self.__screen.unregister_asteroid(i)
                self.__asteroids.remove(i)


    def update_points(self,ast):
        """
        upadte the points on the game's screen
        :param ast: asteroid object that have collided with a torpedo
        """
        if ast.get_size() == 1:
            self.__score += SCORE_POINTS[1]
            self.__screen.set_score(self.__score)
        if ast.get_size() == 2:
            self.__score += SCORE_POINTS[2]
            self.__screen.set_score(self.__score)
        if ast.get_size() == 3:
            self.__score += SCORE_POINTS[3]
            self.__screen.set_score(self.__score)

    def conditions_end(self):
        """
        Checks the conditions in which the game should end
        """
        if self.__lives == 0:
            self.finish_game(LOSE_MSG)
        if len(self.__asteroids) == 0:
            self.finish_game(WIN_MSG)
        if self.__screen.should_end():
            self.finish_game(QUIT_MSG)

    def finish_game(self, msg):
        """
        shows an informative message and ends the game
        :param msg: informative message
        """
        self.__screen.show_message(END_MSG, msg)
        self.__screen.end_game()
        sys.exit()

    def asteroid_split(self, torp, ast):
        """
        Splits an asteroid to two new smaller ones
        :param torp: torpedo that causes the splitting
        :param ast: asteroid to be split
        """
        # add two new asteroids
        new_speed_x = (torp.get_speed()[0] + ast.get_speed()[0]) / \
                      (math.sqrt(ast.get_speed()[0] ** 2 + ast.get_speed()[1] ** 2))
        new_speed_y = (torp.get_speed()[1] + ast.get_speed()[1]) / \
                      (math.sqrt(ast.get_speed()[0] ** 2 + ast.get_speed()[1] ** 2))
        # first new asteroid (positive velocity)
        self.__asteroid1 = Asteroid(new_speed_x, new_speed_y, ast.get_pos()[0],
                                   ast.get_pos()[1], ast.get_size() - 1)
        self.__asteroids.append(self.__asteroid1)
        self.__screen.register_asteroid(self.__asteroid1, self.__asteroid1.get_size())
        # second new asteroid (negative velocity)
        self.__asteroid2 = Asteroid(-new_speed_x, -new_speed_y, ast.get_pos()[0],
                                       ast.get_pos()[1],ast.get_size() - 1)
        self.__asteroids.append(self.__asteroid2)
        self.__screen.register_asteroid(self.__asteroid2, self.__asteroid2.get_size())

        # remove the old asteroid and torpedo from our current object's list
        # unregister the old asteroid from the screen

    def new_pos(self, pos, speed):
        """
        :param pos: tuple of objects position (x,y)
        :param speed: tuple of objects speed (x,y)
        :return: tuple (x,y) with the new position for the object
        """
        new_x = self.__screen_min_x + (pos[0] + speed[0] - self.__screen_min_x) % self.__x_delta
        new_y = self.__screen_min_y + ( pos[1] + speed[1] - self.__screen_min_y) % self.__y_delta
        return new_x, new_y

def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)



