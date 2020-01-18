import pygame
import sys
import random
from bisect import bisect_left
from random import randint


# инициализация модуля pygame
pygame.init()
# задание параметров дисплея
display_width = 1280
display_height = 720
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('FightingGame')
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
tomato = (255, 99, 71)
coral = (255, 127, 80)
orangered = (255, 69, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
FPS = 24
FPSClock = pygame.time.Clock()
titlefont = pygame.font.Font('fonts/GOODTIME.ttf', 64)
msgfont = pygame.font.Font('fonts/GOODTIME.ttf', 32)
smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("", 50)
largefont = pygame.font.SysFont("comicsansms", 85)
codefont = pygame.font.SysFont("comicsansms", 20)
copyrfont = pygame.font.SysFont("comicsansms", 18)


# функции вывода текста на дисплей
def text_objects(text, color, type="small"):
    if type == "title":
        textSurface = titlefont.render(text, True, color)
    if type == "small":
        textSurface = smallfont.render(text, True, color)
    if type == "medium":
        textSurface = medfont.render(text, True, color)
    if type == "large":
        textSurface = largefont.render(text, True, color)
    if type == "code":
        textSurface = codefont.render(text, True, color)
    return textSurface, textSurface.get_rect()


def message_to_screen(msg: object, color: object, y_displace: object = 0, type: object = "small") -> object:
    textSurf, textRect = text_objects(msg, color, type)
    textRect.center = (int(display_width / 2), int(display_height / 2) + y_displace)
    gameDisplay.blit(textSurf, textRect)


# класс игрока
class Fighter(pygame.sprite.Sprite):
    def __init__(self, x, y, images):
        pygame.sprite.Sprite.__init__(self)
        self.loadImages(images)
        self.image = self.i01
        self.imageNum = 0
        self.frameRefreshRate = 2
        self.frameStatus = 0
        self.frameStatusRRate = 10
        self.frame = 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.isplayerone = True
        self.idle = True
        self.hp = False
        self.mp = False
        self.lp = False
        self.hpc = False
        self.mpc = False
        self.lpc = False
        self.ko = False
        self.win = False

    def loadImages(self, images):
        self.i00 = pygame.image.load(images[0]).convert_alpha()
        self.i01 = pygame.image.load(images[1]).convert_alpha()
        self.i02 = pygame.image.load(images[2]).convert_alpha()
        self.i03 = pygame.image.load(images[3]).convert_alpha()
        self.i11 = pygame.image.load(images[4]).convert_alpha()
        self.i12 = pygame.image.load(images[5]).convert_alpha()
        self.i13 = pygame.image.load(images[6]).convert_alpha()
        self.i21 = pygame.image.load(images[7]).convert_alpha()
        self.i22 = pygame.image.load(images[8]).convert_alpha()
        self.i23 = pygame.image.load(images[9]).convert_alpha()
        self.images = (
            self.i00, self.i01, self.i02, self.i03, self.i11, self.i12, self.i13, self.i21, self.i22, self.i23)

    def update(self):
        self.status()
        if self.isplayerone:
            self.image = self.images[self.imageNum]
        else:
            self.image = pygame.transform.flip(self.images[self.imageNum], True, False)

    def draw(self, Surface):
        Surface.blit(self.image, (self.rect.x, self.rect.y))

    def status(self):
        if self.idle:
            self.frame += 1
            if self.frame >= self.frameRefreshRate:
                if (self.imageNum >= 0) and (self.imageNum < 3):
                    self.imageNum += 1
                else:
                    self.imageNum = 0
                self.frame = 0
        if self.hp:
            self.frameStatus += 1
            self.imageNum = 4
            if self.frameStatus > self.frameStatusRRate:
                self.imageNum = 0
                self.frameStatus = 0
                self.hp = False
        if self.mp:
            self.frameStatus += 1
            self.imageNum = 5
            if self.frameStatus > self.frameStatusRRate:
                self.imageNum = 0
                self.frameStatus = 0
                self.mp = False
        if self.lp:
            self.frameStatus += 1
            self.imageNum = 6
            if self.frameStatus > self.frameStatusRRate:
                self.imageNum = 0
                self.frameStatus = 0
                self.lp = False
        if self.hpc:
            self.frameStatus += 1
            self.imageNum = 7
            if self.frameStatus > self.frameStatusRRate:
                self.imageNum = 0
                self.frameStatus = 0
                self.hpc = False
        if self.mpc:
            self.frameStatus += 1
            self.imageNum = 8
            if self.frameStatus > self.frameStatusRRate:
                self.imageNum = 0
                self.frameStatus = 0
                self.mpc = False
        if self.lpc:
            self.frameStatus += 1
            self.imageNum = 9
            if self.frameStatus > self.frameStatusRRate:
                self.imageNum = 0
                self.frameStatus = 0
                self.lpc = False


# задание списка спрайтов игрока
fighter1_sprites = (
    'fighters/fighter1/00.png', 'fighters/fighter1/01.png', 'fighters/fighter1/02.png', 'fighters/fighter1/03.png',
    'fighters/fighter1/11.png', 'fighters/fighter1/12.png',
    'fighters/fighter1/13.png', 'fighters/fighter1/21.png', 'fighters/fighter1/22.png', 'fighters/fighter1/23.png')
fighter2_sprites = (
    'fighters/fighter2/00.png', 'fighters/fighter2/01.png', 'fighters/fighter2/02.png', 'fighters/fighter2/03.png',
    'fighters/fighter2/11.png', 'fighters/fighter2/12.png',
    'fighters/fighter2/13.png', 'fighters/fighter2/21.png', 'fighters/fighter2/22.png', 'fighters/fighter2/23.png')
# задание фоновых изображений
backgrounds = ["backgrounds/background1.jpg", "backgrounds/background2.jpg", "backgrounds/background3.jpg",
               "backgrounds/background4.jpg", "backgrounds/background5.jpg"]
background1 = pygame.image.load(backgrounds[random.randrange(0, 5)]).convert()
message1 = pygame.image.load("backgrounds/message1.png").convert()
message2 = pygame.image.load("backgrounds/message2.png").convert()
message3 = pygame.image.load("backgrounds/message3.jpg").convert()
# создание первого игрока
fighter1 = Fighter(300, 200, fighter1_sprites)
fighter1.isplayerone = True
# создание второго игрока
fighter2 = Fighter(display_width - 300 - 400, 200, fighter2_sprites)
fighter2.isplayerone = False


# опции игроков


# функция выбора опции компьютерным игроком
# уровень сложности: лёгкий
def easyCom():
    options = ('high', 'mid', 'low', 'nc')
    compChoice = random.choice(options)
    return compChoice


# функция выбора опции компьютерным игроком
# уровень сложности: обычный
def normalCom():
    options = ('high', 'mid', 'low')
    compChoice = random.choice(options)
    return compChoice


# фуекция выбора опции компьютерным игроком
# уровень сложности: высокий
def weighted_choice(values, weights):
    total = 0
    cum_weights = []
    for w in weights:
        total += w
        cum_weights.append(total)
    x = random.random() * total
    i = bisect_left(cum_weights, x)
    return values[i]


class hardCom():
    def __init__(self):
        self.choices = ['mid', 'high', 'low']
        self.prevchoice = None  # computer move
        self.prevmove = None  # my move
        self.prevres = None
        self.dataarr = [[0. for _ in range(3)] for _ in range(3)]  # result, roll

        self.gameMat = []
        self.gameMat.append([1, 0, 2])
        self.gameMat.append([2, 1, 0])
        self.gameMat.append([0, 2, 1])
        self.beatMat = [1, 2, 0]

        self.rollMat = []
        self.rollMat.append([0, 1, 2])
        self.rollMat.append([2, 0, 1])
        self.rollMat.append([1, 2, 0])

        self.losecount = 0;
        self.playrand = False
        self.mult = 1.0

    def gameRes(self, c1, c2):
        i1 = self.choices.index(c1)
        i2 = self.choices.index(c2)
        return self.gameMat[i1][i2]

    def getRoll(self, c1, c2):
        i1 = self.choices.index(c1)
        i2 = self.choices.index(c2)
        return self.rollMat[i1][i2]

    def getRollbyInd(self, i1, i2):
        return self.rollMat[i1][i2]

    def rollInd(self, i1, inc):

        row = self.rollMat[i1]
        ind = row.index(inc)
        return ind

    def predict(self):
        if self.prevchoice is None or self.prevres is None:
            ret = self.choices[randint(0, 2)]
            self.prevmove = ret
            return ret
        arr = self.dataarr[self.prevres]

        predictedroll = weighted_choice([0, 1, 2], arr)
        predictedchoice = self.rollInd(self.prevchoice, predictedroll)

        choice = self.beatMat[predictedchoice]
        if self.playrand:
            self.playrand = False

            choice = randint(0, 2)

        self.prevmove = self.choices[choice]
        return self.choices[choice]

    def store(self, c):

        i1 = self.choices.index(c)

        if not (self.prevchoice is None or self.prevres is None):
            roll = self.getRollbyInd(self.prevchoice, i1)
            for i in range(3):
                for j in range(3):
                    self.dataarr[i][j] *= 0.9
            self.dataarr[self.prevres][roll] += 1

        self.prevchoice = i1
        self.prevres = self.gameRes(c, self.prevmove)


# функция отображения количества здоровья
def healthbar(player1_health, player2_health):
    if player1_health > 9:
        player1_hcolor = green
    elif player1_health > 4:
        player1_hcolor = yellow
    else:
        player1_hcolor = red
    if player2_health > 9:
        player2_hcolor = green
    elif player2_health > 4:
        player2_hcolor = yellow
    else:
        player2_hcolor = red
    pygame.draw.rect(gameDisplay, black, (15, 20, 510, 35))
    pygame.draw.rect(gameDisplay, black, (755, 20, 510, 35))
    if player1_health > 0:
        pygame.draw.rect(gameDisplay, player1_hcolor, (20, 25, player1_health * 25, 25))
    if player2_health > 0:
        pygame.draw.rect(gameDisplay, player2_hcolor, (1280 - 20 - player2_health * 25, 25, player2_health * 25, 25))


# функция отрисовки вспышки
def explosion(x, y, size=50):

    explode = True

    while explode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        colorChoices = [red, orangered, tomato, coral]
        magnitude = 1
        while magnitude < size:
            exploding_bit_x = x + random.randrange(-1 * magnitude, magnitude)
            exploding_bit_y = y + random.randrange(-1 * magnitude, magnitude)
            pygame.draw.circle(gameDisplay, colorChoices[random.randrange(0,4)],
                               (exploding_bit_x,exploding_bit_y),random.randrange(10,15))
            magnitude += 1
            pygame.display.update()
            FPSClock.tick(FPS)
        explode = False

# функция изменения цвета таймера
def timercolor(originalTime):
    if originalTime < 6:
        return red
    else:
        return blue


# функция паузы
def pause():
    paused = True
    message_to_screen("PAUSED", white, 0, 'large')
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
        FPSClock.tick(FPS)


# главное меню игры
def gameMenu():
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    menu = False
                    levelChoose()
                if event.key == pygame.K_d:
                    menu = False
                    fight("human")
                elif event.key == pygame.K_s:
                    pygame.quit()
                    quit()
        gameDisplay.fill(black)
        message_to_screen("ANdruha Krasava", blue, -250, "title")
        gameDisplay.blit(msgfont.render("COMPUTER (press w)", True, blue), (700, 300))
        gameDisplay.blit(msgfont.render("Human (press d)", True, blue), (700, 350))
        gameDisplay.blit(msgfont.render("Quit (press s)", True, blue), (700, 400))
        fighter1.update()
        fighter1.draw(gameDisplay)
        pygame.display.update()
        FPSClock.tick(FPS)


# выбор уровня сложности
def levelChoose():
    levelChoose = True
    while levelChoose:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    levelChoose = False
                    fight('easy')
                if event.key == pygame.K_w:
                    levelChoose = False
                    fight('normal')
                if event.key == pygame.K_e:
                    levelChoose = False
                    fight('hard')
                if event.key == pygame.K_BACKSPACE:
                    gameMenu()
        gameDisplay.fill(black)
        message_to_screen("choose difficulty level", blue, -250, "title")
        gameDisplay.blit(msgfont.render("hacker (press q)", True, white), (500, 300))
        gameDisplay.blit(msgfont.render("pro (press w)", True, blue), (500, 350))
        gameDisplay.blit(msgfont.render("noob (press e)", True, red), (500, 400))
        pygame.display.update()
        FPSClock.tick(FPS)


# игровой процесс
def fight(opponent="normal"):
    background1 = pygame.image.load(backgrounds[random.randrange(0, 5)]).convert()
    player1_loses = False
    player2_loses = False
    players_draw = False
    originalTime = 5
    player1_health = 20
    player2_health = 20
    endframe = 0
    kekerloler = 0
    playersChoice = 'mid'
    computersChoice = 'mid'
    player2Choice = 'mid'
    if opponent == 'hard':
        com = hardCom()
        computersChoice = com.predict()
    isfight = True
    while isfight:
        # задаем таймер для хода игроков
        if originalTime != 0:
            if kekerloler != 10:
                kekerloler += 1
            else:
                kekerloler = 0
                originalTime -= 1
        else:
            originalTime = 5
        displayingTime = str(originalTime)
        # считывание нажатий клавиш первого игрока
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # задание выбора первого игрока
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    gameMenu()
                if event.key == pygame.K_p:
                    pause()
                if event.key == pygame.K_d:
                    playersChoice = 'mid'
                if event.key == pygame.K_w:
                    playersChoice = 'high'
                if event.key == pygame.K_s:
                    playersChoice = 'low'
                if event.key == pygame.K_LEFT:
                    player2Choice = 'mid'
                if event.key == pygame.K_UP:
                    player2Choice = 'high'
                if event.key == pygame.K_DOWN:
                    player2Choice = 'low'
        if originalTime % 10 == 0:
            # задание выбора второго игрока
            if opponent == "easy":
                computersChoice = easyCom()
            elif opponent == "normal":
                computersChoice = normalCom()
            elif opponent == "hard":
                com.store(playersChoice)
                computersChoice = com.predict()
            elif opponent == "human":
                computersChoice = player2Choice
            # возможные варианты событий игры
            if (playersChoice == 'high') and (computersChoice == 'high'):
                fighter1.hpc = True
                fighter2.hpc = True
                player1_health -= 1
                player2_health -= 1
            if (playersChoice == 'high') and (computersChoice == 'mid'):
                fighter1.hp = True
                fighter2.mpc = True
                player2_health -= 1
            if (playersChoice == 'high') and (computersChoice == 'low'):
                fighter1.hpc = True
                fighter2.lp = True
                player1_health -= 1
            if (playersChoice == 'mid') and (computersChoice == 'high'):
                fighter1.mpc = True
                fighter2.hp = True
                player1_health -= 1
            if (playersChoice == 'mid') and (computersChoice == 'mid'):
                fighter1.mpc = True
                fighter2.mpc = True
                player1_health -= 1
                player2_health -= 1
            if (playersChoice == 'mid') and (computersChoice == 'low'):
                fighter1.mp = True
                fighter2.lpc = True
                player2_health -= 1
            if (playersChoice == 'low') and (computersChoice == 'high'):
                fighter1.lp = True
                fighter2.hpc = True
                player2_health -= 1
            if (playersChoice == 'low') and (computersChoice == 'mid'):
                fighter1.lpc = True
                fighter2.mp = True
                player1_health -= 1
            if (playersChoice == 'low') and (computersChoice == 'low'):
                fighter1.lpc = True
                fighter2.lpc = True
                player1_health -= 1
                player2_health -= 1
            if (playersChoice == 'nc') and (computersChoice == 'high'):
                fighter1.mpc = True
                fighter2.hp = True
                player1_health -= 1
            if (playersChoice == 'nc') and (computersChoice == 'mid'):
                fighter1.mpc = True
                fighter2.mp = True
                player1_health -= 1
            if (playersChoice == 'nc') and (computersChoice == 'low'):
                fighter1.mpc = True
                fighter2.hp = True
                player1_health -= 1
            if (playersChoice == 'high') and (computersChoice == 'nc'):
                fighter1.hp = True
                fighter2.mpc = True
                player2_health -= 1
            if (playersChoice == 'mid') and (computersChoice == 'nc'):
                fighter1.mp = True
                fighter2.mpc = True
                player2_health -= 1
            if (playersChoice == 'low') and (computersChoice == 'nc'):
                fighter1.lp = True
                fighter2.mpc = True
                player2_health -= 1
            print(playersChoice, computersChoice, player1_health, player2_health)
        # условия на конец поединка
        if player1_health == 0 or player2_health == 0:
            endframe += 1
        if (player1_health == 0) and (player2_health != 0) and endframe > 11:
            player1_loses = True
            isfight = False
            continue
        elif (player1_health != 0) and (player2_health == 0) and endframe > 10:
            player2_loses = True
            isfight = False
            continue
        elif (player1_health == 0) and (player2_health == 0) and endframe > 10:
            players_draw = True
            isfight = False
            continue
        # отображение фонового изображения
        gameDisplay.blit(background1, (0, 0))
        # отрисовка полосок здоровья
        healthbar(player1_health, player2_health)
        # отрисовка таймера
        message_to_screen(displayingTime, timercolor(originalTime), -320, "title")
        # отрисовка игроков
        fighter1.update()
        fighter1.draw(gameDisplay)
        fighter2.update()
        fighter2.draw(gameDisplay)
        # обновление изображения на экране
        FPSClock.tick(FPS)
        pygame.display.update()
    if player1_loses:
        print("Player 2 wins!")
        player2_winmessage()
    if player2_loses:
        print("Player 1 wins!")
        player1_winmessage()
    if players_draw:
        print("Draw!")
        draw_winmessage()


# сообщение о выигрыше первого игрока
def player1_winmessage():
    p1message = True
    while p1message:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_BACKSPACE:
                    gameMenu()
        gameDisplay.blit(message1, (0, 0))
        pygame.display.update()
        FPSClock.tick(FPS)


# сообщение о выигрыше второго игрока
def player2_winmessage():
    p2message = True
    while p2message:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_BACKSPACE:
                    gameMenu()
        gameDisplay.blit(message2, (0,0))
        pygame.display.update()
        FPSClock.tick(FPS)


# сообщение о ничьей
def draw_winmessage():
    p3message = True
    while p3message:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_BACKSPACE:
                    gameMenu()
        gameDisplay.blit(message3, (0, 0))
        pygame.display.update()
        FPSClock.tick(FPS)


gameMenu()
