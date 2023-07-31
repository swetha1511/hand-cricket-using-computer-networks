import pygame
pygame.init()
from network import Network
import pickle

pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client 1")
background_image = pygame.image.load("Hand_Cricket1.jpeg").convert()

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("freesansbold.ttf", 40)
        text = font.render(self.text, 1, (0, 0, 0))
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(wind, game, p):
    global text1, text2
    wind.fill((200, 175, 2))
    if not (game.connected()):
        font = pygame.font.SysFont("Segoe UI", 60)
        text = font.render("Waiting for Opponent to join..",1, (220, 220, 255), True)
        wind.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:
        font = pygame.font.SysFont("Segoe UI", 40)
        text = font.render("You are", 1, (255, 255, 255))
        wind.blit(text, (80, 165))
        font = pygame.font.SysFont("Segoe UI", 40)
        text = font.render("Opponent is ", 1, (255, 255, 255))
        wind.blit(text, (380, 165))

        if p == 1 and game.done_bat[0] == 1:
            text1 = font.render("Batsman", 1, (255, 255, 255))
            text2 = font.render("Bowler", 1, (255, 255, 255))
        elif p == 0 and game.done_bat[0] == 1:
            text1 = font.render("Bowler", 1, (255, 255, 255))
            text2 = font.render("Batsman", 1, (255, 255, 255))
        elif p == 1:
            text1 = font.render("Bowler", 1, (255, 255, 255))
            text2 = font.render("Batsman", 1, (255, 255, 255))
        elif p == 0:
            text1 = font.render("Batsman", 1, (255, 255, 255))
            text2 = font.render("Bowler", 1, (255, 255, 255))

        wind.blit(text1, (100, 200))
        wind.blit(text2, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)

        if game.bothWent():
            text1 = font.render(move1, 1, (0, 0, 0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0, 0, 0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0, 0, 50))
            else:
                text1 = font.render("Waiting..", 1, (0, 0, 50))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0, 0, 0))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting..", 1, (0, 0, 0))

        score1 = game.get_player_score(0)
        score2 = game.get_player_score(1)

        if p == 1:
            wind.blit(text2, (100, 350))
            wind.blit(text1, (400, 350))
            t_score1 = font.render(str(score2), 1, (255, 75, 75))
            t_score2 = font.render(str(score1), 1, (255, 75, 75))
        else:
            wind.blit(text1, (100, 350))
            wind.blit(text2, (400, 350))
            t_score1 = font.render(str(score1), 1, (255, 75, 75))
            t_score2 = font.render(str(score2), 1, (255, 75, 75))

        wind.blit(t_score1, (100, 250))
        wind.blit(t_score2, (400, 250))

        if game.done_bat[0] ==1 and game.done_bat[1] ==1:
            pass
        elif game.done_bat[0] == 1 and game.get_player_score(1) == 0 and p == 1:
            text0 = font.render("OPPONENT IS OUT", 1, (255, 75, 75))
            wind.blit(text0, (75, 100))
        elif game.done_bat[0] == 1 and game.get_player_score(1) == 0 and p == 0:
            text0 = font.render("YOU ARE OUT", 1, (255, 75, 75))
            wind.blit(text0, (75, 100))

        for btn in btns:
            btn.draw(wind)

    pygame.display.update()


btns = [Button("1", 75, 400, (255, 255, 255)), Button("2", 275, 400, (255, 255, 255)), Button("3", 475, 400, (255, 255, 255)),
        Button("4", 75, 525, (255, 255, 255)), Button("5", 275, 525, (255, 255, 255)), Button("6", 475, 525, (255, 255, 255)), ]


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)
    while run:
        clock.tick(60)
        try:
            game = n.send("get")
            #print("game id =",game.id)
            #print("game score =",game.score)
            # print("got the game ")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            print("game.bothWent() = ",game.bothWent())
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("score")
            except:
                run = False
                print("Couldn't get game for score")
                break

        #print("game.done_bat[0] = ", game.done_bat[0], "and game.done_bat[0] =", game.done_bat[1])

        if game.done_bat[0] and game.done_bat[1]:
            print("result")
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("Segoe UI", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (255, 75, 75))
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255, 75, 75))
            else:
                text = font.render("You Lost!", 1, (255, 75, 75))

            win.blit(text, (220, 25))
            pygame.display.update()
            pygame.time.delay(3000)

        for event in pygame.event.get():
            # print(pygame.event.get())
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                                print(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)
                                print(btn.text)
        # print("redrawWindow() player ",player)
        redrawWindow(win, game, player)


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(5)
        win.fill((255, 255, 255))
        font = pygame.font.SysFont("Segoe UI", 60)
        text = font.render("Tap to Play!", 1, (150, 0, 0))
        win.blit(text, (195, 10))
        pygame.display.update()

        for event in pygame.event.get():
            # print(pygame.event.get())
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
        win.blit(background_image, [70, 100])

        pygame.display.update()

    main()


while True:
    menu_screen()