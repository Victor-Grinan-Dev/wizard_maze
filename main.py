import turtle
import random

"""
    1-the blue turtle will get the power and shot it 
    2- the power will hit a turtle and become a power again that can be picked up
    3-only one power can be picked by the player at the time
"""

win = turtle.Screen()
win.bgcolor("black")
win.title("A Maze Game")
win.setup(700, 700)
win.tracer(0)

# register shapes
# sprites = ["./assets/wall.gif", "./assets/gold.gif", "./assets/explosion.gif", "./assets/powerup.gif"]
# for sprite in sprites:
# turtle.register_shape(sprite)


# todo: make powerup to follow player

# create pen
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)


class Treasure(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("circle")
        self.color("yellow")
        self.penup()
        self.speed(0)
        self.gold = 100
        self.goto(x, y)

    def destroy(self):
        self.goto(700 + 100, 700 + 100)
        self.hideturtle()
        # self.reset() # not working


class PowerUp(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("circle")
        self.color("lightblue")
        self.penup()
        self.speed(0)
        self.goto(x, y)

    def is_collision(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = ((a ** 2) + (b ** 2)) ** 0.5

        if distance < 5:
            return True
        else:
            return False

    def destroy(self):
        self.goto(700 + 100, 700 + 100)
        self.hideturtle()
        # self.reset() # not working


class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.color("blue")
        self.shape("turtle")
        self.penup()
        self.speed(0)
        self.gold = 0
        self.is_alive = True
        self.power_active = False
        self.elements = [self]

    def is_collision(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = ((a ** 2) + (b ** 2)) ** 0.5

        if distance < 5:
            return True
        else:
            return False

    @staticmethod
    def is_wall(coords):
        return coords in walls

    def go_up(self):
        self.setheading(90)
        move_to_x = self.xcor()
        move_to_y = self.ycor() + 24
        if not self.is_wall((move_to_x, move_to_y)):
            self.goto(move_to_x, move_to_y)

    def go_down(self):
        self.setheading(270)
        move_to_x = self.xcor()
        move_to_y = self.ycor() - 24
        if not self.is_wall((move_to_x, move_to_y)):
            self.goto(move_to_x, move_to_y)

    def go_left(self):
        self.setheading(180)
        move_to_x = self.xcor() - 24
        move_to_y = self.ycor()
        if not self.is_wall((move_to_x, move_to_y)):
            self.goto(move_to_x, move_to_y)

    def go_right(self):
        self.setheading(0)
        move_to_x = self.xcor() + 24
        move_to_y = self.ycor()
        if not self.is_wall((move_to_x, move_to_y)):
            self.goto(move_to_x, move_to_y)

    def fire(self):
        if self.power_active:
            print("fire!!!")


class Enemy(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("turtle")
        self.color("red")
        self.penup()
        self.speed(0)
        self.gold = 100
        self.goto(x, y)
        self.direction = random.choice(["up", "down", "left", "right", "stay"])
        self.current_direction = None
        self.dx = 0
        self.dy = 0

    def move(self):

        if self.direction == "up":
            self.setheading(90)
            self.dx = 0
            self.dy = 24
            self.current_direction = "up"
        elif self.direction == "down":
            self.setheading(270)
            self.dx = 0
            self.dy = -24
            self.current_direction = "down"
        elif self.direction == "left":
            self.setheading(180)
            self.dx = -24
            self.dy = 0
            self.current_direction = "left"
        elif self.direction == "right":
            self.setheading(0)
            self.dx = 24
            self.dy = 0
            self.current_direction = "right"
        else:
            self.dx = 0
            self.dy = 0

        # chase the player
        if self.is_close(player):
            if player.xcor() < self.xcor():
                self.current_direction = "left"
            elif player.xcor() > self.xcor():
                self.current_direction = "right"
            elif player.xcor() < self.ycor():
                self.current_direction = "down"
            elif player.xcor() > self.ycor():
                self.current_direction = "up"

        move_to_x = self.xcor() + self.dx
        move_to_y = self.ycor() + self.dy
        if (move_to_x, move_to_y) not in walls and (move_to_x, move_to_y) not in enemies_current_pos:
            self.goto(move_to_x, move_to_y)
        else:
            self.direction = random.choice(["up", "down", "left", "right"])

            while self.direction == self.current_direction:
                self.direction = random.choice(["up", "down", "left", "right"])

        turtle.ontimer(self.move, t=random.randint(500, 1000))  # t=random.randint(500, 1000)

    def destroy(self):
        self.goto(700 + 100, 700 + 100)
        self.hideturtle()

    def is_close(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = ((a ** 2) + (b ** 2)) ** 0.5

        if distance < 75:
            return True
        else:
            return False


# crate levels
levels = [""]  # initialized "" so every level have his own number as index

level_1 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X XX P T XXXX        E   X",
    "X XX  U     X      XXXX  X",
    "X XX  XXXXXXXXXXXXXXXX   X",
    "X             XX        TX",
    "X   XXXXXXXXXXXX    XXXXXX",
    "X                        X",
    "X         XXXXXXXXXXXXXXXX",
    "X E                    E X",
    "XX XXXXXXXXXXXXXXX       X",
    "X                      E X",
    "X XXXXXXXXXXXXXXXXXXXXX XX",
    "X  E                     X",
    "X          XXXXXXXXXXXXXXX",
    "X E               XXX  T X",
    "XXXXX XXXXXXX     XXX    X",
    "X                 XXX    X",
    "X   XXXXXXXXXXXX  XXX    X",
    "X                  x   E X",
    "X T      XXXXXXXXXXXXX XXX",
    "X                        X",
    "XX     XXXXXX           BX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXX"]

levels.append(level_1)

walls = []
treasures = []
enemies = []
enemies_current_pos = []
powerups = []


def setup_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]
            # converting the index position in turtle coords
            screen_x = -288 + (x * 24)
            screen_y = 288 - (y * 24)

            if character == "X":
                pen.goto(screen_x, screen_y)
                pen.shape("square")
                pen.color("white")
                pen.stamp()
                walls.append((screen_x, screen_y))
            if character == "P":
                player.goto(screen_x, screen_y)

            if character == "T":
                treasures.append(Treasure(screen_x, screen_y))

            if character == "E":
                enemies.append(Enemy(screen_x, screen_y))
                for enemy_ in enemies:
                    turtle.ontimer(enemy_.move, t=300)

            if character == "U":
                powerups.append(PowerUp(screen_x, screen_y))


pen = Pen()
player = Player()

setup_maze(levels[1])

win.listen()
win.onkey(player.go_up, "w")
win.onkey(player.go_up, "Up")
win.onkey(player.go_down, "s")
win.onkey(player.go_down, "Down")
win.onkey(player.go_left, "a")
win.onkey(player.go_left, "Left")
win.onkey(player.go_right, "d")
win.onkey(player.go_right, "Right")

for enemy in enemies:
    turtle.ontimer(enemy.move, 250)

while player.is_alive:
    win.update()
    for treasure in treasures:
        if player.is_collision(treasure):
            player.gold += treasure.gold
            print(f"Player Gold: {player.gold}")
            treasure.destroy()
            treasures.remove(treasure)

    for enemy in enemies:
        if player.is_collision(enemy):
            enemy.destroy()
            player.shape("explosion.gif")
            print("GAME OVER")
            player.is_alive = False
            win.update()

    enemies_current_pos = []
    for enemy in enemies:
        enemies_current_pos.append(enemy.position())

    for powerup in powerups:
        if player.is_collision(powerup) and not player.power_active:
            player.power_active = True
            powerup.hideturtle()
            # powerup.goto(player.xcor(), player.ycor())

win.mainloop()
