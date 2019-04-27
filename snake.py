import pygame, time, random, os

pygame.init()

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

window_width = 1000
screen_width = 800
screen_heigth = 600

gameDisplay = pygame.display.set_mode((window_width, screen_heigth))

pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

class segment():
    def __init__(self, x, y, color):
        self.color = color
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.rect(gameDisplay, self.color, [self.x, self.y, 20, 20])

class snake():
    def __init__(self, speed):
        self.speed = speed

    def move(self, key):
        if key == 'r':
            head.x += self.speed
        if key == 'l':
            head.x -= self.speed
        if key == 'u':
            head.y -= self.speed
        if key == 'd':
            head.y += self.speed
        head.draw()
    
    def die(self):
        tail = [segment(x,y,white),segment(screen_width+100,screen_heigth+100,white),segment(screen_width+100,screen_heigth+100,white)]   
        time.sleep(1)
        gameLoop(tail)

    def grow(self,tail):
        tail.append(segment(20,20,white))
        food.x = random.randrange(0,screen_width,20)
        food.y = random.randrange(0,screen_heigth,20)


def display_text(msg, color, x, y):
    
    font = pygame.font.SysFont('verdana',25)
    text = font.render(msg, True, color)
    gameDisplay.blit(text, [x,y])

def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                    break    
def gameLoop(tail):
    global highscore
    score = 0
    difficulty = 0.09
    xs = []
    ys = []

    head.x = screen_width/2
    head.y = screen_heigth/2

    left = False
    right = True
    up = False
    down = False

    food.x = random.randrange(0,screen_width,20)
    food.y = random.randrange(0,screen_heigth,20)

    while True:
        movement_done = True
        paused = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause()
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_LEFT and not right and movement_done:
                    left = True
                    right = False
                    up = False
                    down = False
                if event.key == pygame.K_RIGHT and not left and movement_done:
                    right = True
                    left = False
                    down = False
                    up = False
                if event.key == pygame.K_UP and not down and movement_done:
                    up = True
                    down = False
                    right = False
                    left = False
                if event.key == pygame.K_DOWN and not up and movement_done:
                    down = True
                    up = False
                    right = False
                    left = False

                movement_done = False


        xs = [head.x] #Head's (x,y) position is saved before movement
        ys = [head.y]
        
        if left:
            player.move('l')
        if right:
            player.move('r')
        if up:
            player.move('u')
        if down:
            player.move('d')


        if head.x+20 > screen_width or head.x < 0 or head.y + 20 > screen_heigth or head.y < 0:
            player.die()

        if head.x == food.x and head.y == food.y:
            player.grow(tail)
            score += 10
            if score % 50 == 0 and difficulty > 0.01:
                difficulty -= 0.01
            if score > int(highscore):
                f.seek(0)
                f.write(str(score))
                f.seek(0)
                highscore = f.read()

        gameDisplay.fill(black)

        pygame.draw.rect(gameDisplay, white, [0,0,800,600],1)

        display_text('Score:', white, 830, 20)
        display_text(str(score), white, 950,20)
        display_text('Highscore:', white, 830, 50)
        display_text(highscore, white, 950, 50)
        display_text('P to pause', white, 830, 300)
        display_text('Q to exit', white, 830, 330)

        food.draw()
        head.draw()
        j = 0 

        for i in tail:              #For each segment of the tail:
            xs.append(i.x)          #Add the current segment position to xs
            ys.append(i.y)
            i.x=xs[j]               #The current segment's position is changed to it's respective position 
            i.y=ys[j]
            i.draw()
            if head.x == i.x and head.y == i.y:
                player.die()
            j += 1

        pygame.display.update()
        time.sleep(difficulty)
        clock.tick(60)
        
x = screen_width/2
y = screen_heigth/2

head = segment(x, y, white)
tail = [segment(x,y,white),segment(screen_width+100,screen_heigth+100,white),segment(screen_width+100,screen_heigth+100,white)]
player = snake(20)

food_x = random.randrange(0,screen_width,20)
food_y = random.randrange(0,screen_heigth,20)
food = segment(food_x, food_y, white)

try:
    f = open('highscore.txt', 'r+')
except:
    f = open('highscore.txt', 'w+')
    f.write('1')

f.seek(0)
highscore = f.read()
gameLoop(tail)
f.close()
