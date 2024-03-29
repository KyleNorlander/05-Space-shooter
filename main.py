import sys, logging, os, random, math, open_color, arcade

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MARGIN = 30
SCREEN_TITLE = "Andromeda's Armada"
NUM_ENEMIES = 10
STARTING_LOCATION = (400,100)
BULLET_DAMAGE = 10
ENEMY_HP = 100
HIT_SCORE = 10
KILL_SCORE = 100
PLAYER_HP = 50
INITIAL_VELOCITY = 3

class Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        ''' 
        initializes the bullet
        Parameters: position: (x,y) tuple
            velocity: (dx, dy) tuple
            damage: int (or float)
        '''
        super().__init__("assets/Player/PNG/Sprites/Missiles/spaceMissiles_012.png", 0.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage

    def update(self):
        '''
        Moves the bullet
        '''
        self.center_x += self.dx
        self.center_y += self.dy

class Enemy_Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        super().__init__("PNG/laserGreen3.png", 0.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage
    def update(self):
        self.center_x += self.dx
        self.center_y += self.dy

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/Player/PNG/Sprites/Ships/spaceShips_005.png", 0.5)
        (self.center_x, self.center_y) = STARTING_LOCATION
        self.hp = PLAYER_HP

class Enemy(arcade.Sprite):
    def __init__(self, position):
        '''
        initializes an alien enemy
        Parameter: position: (x,y) tuple
        '''
        super().__init__("PNG/shipGreen_manned.png", 0.5)
        self.hp = ENEMY_HP
        (self.center_x, self.center_y) = position  #Heres my movement problem
        self.dx = random.randrange(-2,2)
        self.dy = random.randrange(-2,2)

    def update(self):
        print("updating")
        self.center_x += self.dx
        self.center_y += self.dy
        if self.center_x <= 0:
            self.dx = abs(self.dx)
        if self.center_y <= 0:
            self.dy = abs(self.dy)
        if self.center_x >= SCREEN_WIDTH:
            self.dx = abs(self.dx)*-1
        if self.center_y >= SCREEN_HEIGHT:
            self.dy = abs(self.dy)*-1

class Window(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.background = arcade.load_texture('assets/spacebackground.png')
        'sets background'
        self.set_mouse_visible(True)
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.player = Player()
        self.score = 0
        self.win = False
        self.lose = False

    def setup(self):
        '''
        Set up enemies
        ''' 
        enemy = ['enemy']

        for i in range(NUM_ENEMIES):

            x = random.randint(MARGIN,SCREEN_WIDTH-MARGIN)
            y = random.randint(MARGIN,SCREEN_HEIGHT-MARGIN)
            self.enemy_sprite = Enemy((x,y))
            self.enemy_sprite.mass = 1
            self.enemy_sprite.hp = 100
            self.enemy_list.append(self.enemy_sprite)


    def update(self, delta_time):
        self.bullet_list.update()
        self.enemy_bullet_list.update()
        self.enemy_list.update()
        if (not (self.win or self.lose)): 
            for e in self.enemy_list:
                for b in self.bullet_list:
                    if (abs(b.center_x - e.center_x) <= e.width / 2 and abs(b.center_y - e.center_y) <= e.height / 2):
                        self.score += HIT_SCORE
                        e.hp -= b.damage
                        b.kill()
                        if (e.hp <= 0):
                            e.kill()
                            self.score += KILL_SCORE
                            if (len(self.enemy_list) == 0):
                                self.win = True
                if (random.randint(1, 75) == 1):
                    self.enemy_bullet_list.append(Enemy_Bullet((e.center_x, e.center_y - 15), (0, -10), BULLET_DAMAGE))
                for b in self.enemy_bullet_list:
                    if (abs(b.center_x - self.player.center_x) <= self.player.width / 2 and abs(b.center_y - self.player.center_y) <= self.player.height / 2):
                        self.player.hp -= b.damage
                        b.kill()
                        if (self.player.hp <= 0):
                            self.lose = True                

                            

   
    def on_draw(self):
        arcade.start_render()
        self.background.draw(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, SCREEN_WIDTH, SCREEN_HEIGHT)
        arcade.draw_text(str(self.score), 20, SCREEN_HEIGHT - 40, open_color.white, 16)
        arcade.draw_text("Health: {}".format(self.player.hp), 20, 40, open_color.white, 16)

        if (self.player.hp > 0):
            self.player.draw()

        self.bullet_list.draw()
        self.enemy_bullet_list.draw()
        self.enemy_list.draw()
        if (self.lose):
            self.draw_game_loss()
        elif (self.win):
            self.draw_game_won()

    def draw_game_loss(self):
        arcade.draw_text(str("GAME OVER"), SCREEN_WIDTH / 2 - 90, SCREEN_HEIGHT / 2 - 10, open_color.white, 30)

    def draw_game_won(self):
        arcade.draw_text(str("YOU WON!"), SCREEN_WIDTH / 2 - 90, SCREEN_HEIGHT / 2 - 10, open_color.white, 30)
     
    def on_mouse_motion(self, x, y, dx, dy):
        '''
        The player moves left and right with the mouse
        '''
        self.player.center_x = x
        self.player.center_y = y
        self.set_mouse_visible(False) 


    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            x = self.player.center_x - 12
            y = self.player.center_y + 15
            bullet = Bullet((x,y),(0,10),BULLET_DAMAGE)
            self.bullet_list.append(bullet)
        if button == arcade.MOUSE_BUTTON_RIGHT:
            x = self.player.center_x + 12
            y = self.player.center_y + 15
            bullet = Bullet((x,y),(0,10),BULLET_DAMAGE)
            self.bullet_list.append(bullet)
           

def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()