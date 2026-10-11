import pygame
import sys
import os
import json
import ctypes

pygame.init()

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

window = pygame.display.set_mode((800, 600))
window.fill((181, 101, 29)) # light brown table
pygame.display.set_caption("Brownie Clicker")

button = pygame.surface.Surface((125, 125))
button.fill((0, 0, 0))
button = pygame.image.load(os.path.join(BASE_DIR, "imgs", "brownie.png")).convert_alpha()
button = pygame.transform.scale(button, (125, 125))

settingsbutton = pygame.surface.Surface((150, 50))
settingsbutton.fill((255, 255, 255))

backbutton = pygame.surface.Surface((150, 50))
backbutton.fill((255, 255, 255))

resetbutton = pygame.surface.Surface((150, 50))
resetbutton.fill((255, 255, 255))

shopbutton = pygame.surface.Surface((150, 50))
shopbutton.fill((255, 255, 255))

buybutton = pygame.surface.Surface((450, 50))
buybutton.fill((255, 255, 255))

statsbutton = pygame.surface.Surface((150, 50))
statsbutton.fill((255, 255, 255))

if os.path.exists("savefile.json"):
    with open("savefile.json", "r") as file:
        data = json.load(file)
        points = data["points"]
        multiplier = data["multiplier"]
        multiplieramount = data["multiplieramount"]
        amountclicked = data["clicked"]
        totalpoints = data["total"]
        spent = data["spent"]
else:
    points = 0
    multiplier = 1
    multiplieramount = 0
    amountclicked = 0
    totalpoints = 0
    spent = 0

font = pygame.font.SysFont(None, 48)
fontonscreen = font.render("Click the brownie to gain points!", True, (0, 0, 0))
pointsonscreen = font.render("Points: " + str(round(points, 1)), True, (0, 0, 0))
settingsonscreen = font.render("Settings", True, (0, 0, 0))
backonscreen = font.render("Go Back", True, (0, 0, 0))
resetonscreen = font.render("Reset", True, (0, 0, 0))
shoponscreen = font.render("Shop", True, (0, 0, 0))
buyonscreen = font.render("Buy a multiplier (Costs 60)", True, (0, 0, 0))
buytextonscreen = font.render("Which items would you like to buy?", True, (0, 0, 0))
statsonscreen = font.render("Stats", True, (0, 0, 0))
yourstatsonscreen = font.render("Your stats", True, (0, 0, 0))
amountclickedonscreen = font.render("You have clicked: " + str(amountclicked), True, (0, 0, 0))
totalpointsonscreen = font.render("Your total gained points: " + str(round(totalpoints, 1)), True, (0, 0, 0))
spentpointsonscreen = font.render("You have spent total of: " + str(spent), True, (0, 0, 0))
multiplieronscreen = font.render("You have total of " + str(multiplieramount) + " multipilers", True, (0, 0, 0))

button_x = 350
button_y = 250
button_interact = button.get_rect(topleft=(button_x, button_y))

settingsbutton_x = 50
settingsbutton_y = 100
settings_interact = settingsbutton.get_rect(topleft=(settingsbutton_x, settingsbutton_y))

backbutton_x = 50
backbutton_y = 200 # this is why game engines are better than pygame
back_interact = backbutton.get_rect(topleft=(backbutton_x, backbutton_y))

resetbutton_x = 50
resetbutton_y = 300
reset_interact = resetbutton.get_rect(topleft=(resetbutton_x, resetbutton_y))

shopbutton_x = 50
shopbutton_y = 400
shop_interact = shopbutton.get_rect(topleft=(shopbutton_x, shopbutton_y))

buybutton_x = 350
buybutton_y = 250 # since we're not clicking on the same button, it should be good (hopefully or I'm crashing out)
buy_interact = buybutton.get_rect(topleft=(buybutton_x, buybutton_y))

statsbutton_x = 50
statsbutton_y = 500
stats_interact = statsbutton.get_rect(topleft=(statsbutton_x, statsbutton_y))

game_state = 1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if game_state == 1:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_interact.collidepoint(event.pos):
                    points += 1 * multiplier
                    amountclicked += 1
                    totalpoints += 1 * multiplier
                    with open("savefile.json", "w") as file:
                        json.dump({"points": round(points, 1), "multiplier": multiplier, "clicked": amountclicked, "total": round(totalpoints, 1), "spent": spent, "multiplieramount": multiplieramount}, file)
                    pointsonscreen = font.render("Points: " + str(round(points, 1)), True, (0, 0, 0))
                    amountclickedonscreen = font.render("You have clicked: " + str(amountclicked), True, (0, 0, 0)) # making sure this also auto updates
                    totalpointsonscreen = font.render("Your total gained points: " + str(round(totalpoints, 1)), True, (0, 0, 0))
                elif settings_interact.collidepoint(event.pos):
                    #print("settings button pressed")
                    game_state = 2
                elif shop_interact.collidepoint(event.pos):
                    game_state = 3
                elif stats_interact.collidepoint(event.pos):
                    game_state = 4

        if game_state == 2:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_interact.collidepoint(event.pos):
                    #print("going back")
                    game_state = 1
                elif reset_interact.collidepoint(event.pos):
                    #print("reset clicked")
                    warningmsg = ctypes.windll.user32.MessageBoxW(0, "Would you like to reset your save?", "Brownie Clicker", 4) # 6 is yes 7 is no
                    if (warningmsg == 6):
                        with open("savefile.json", "w") as file:
                            json.dump({"points": 0, "multiplier": 1, "clicked": 0, "total": 0, "spent": 0, "multiplieramount": 0}, file)
                        points = 0
                        amountclicked = 0
                        multiplier = 1
                        multiplieramount = 0
                        totalpoints = 0
                        spent = 0
                        game_state = 1
                        pointsonscreen = font.render("Points: " + str(points), True, (0, 0, 0)) # auto update is annoying
                        amountclickedonscreen = font.render("You have clicked: " + str(amountclicked), True, (0, 0, 0)) # same here
                        multiplieronscreen = font.render("You have total of " + str(multiplieramount) + " multipilers", True, (0, 0, 0))
                        spentpointsonscreen = font.render("You have spent total of: " + str(spent), True, (0, 0, 0))

        if game_state == 3:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_interact.collidepoint(event.pos):
                    game_state = 1
                elif buy_interact.collidepoint(event.pos):
                    if (points < 60):
                        buyonscreen = font.render("You can't afford this", True, (0, 0, 0))
                    else:
                        points -= 60
                        spent += 30
                        multiplier += 0.1
                        multiplieramount += 1
                        pointsonscreen = font.render("Points: " + str(round(points, 1)), True, (0, 0, 0))
                        multiplieronscreen = font.render("You have total of " + str(multiplieramount) + " multipilers", True, (0, 0, 0))
                        spentpointsonscreen = font.render("You have spent total of: " + str(spent), True, (0, 0, 0))

        if game_state == 4:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_interact.collidepoint(event.pos):
                    game_state = 1

    window.fill((181, 101, 29))

    if game_state == 1:
        window.blit(pointsonscreen, (50, 50))
        window.blit(fontonscreen, (180, 160))
        window.blit(button, button_interact)

        settingsbutton.blit(settingsonscreen, settingsonscreen.get_rect(center=settingsbutton.get_rect().center))
        window.blit(settingsbutton, settings_interact)
        shopbutton.blit(shoponscreen, shoponscreen.get_rect(center=shopbutton.get_rect().center))
        window.blit(shopbutton, shop_interact)
        statsbutton.blit(statsonscreen, statsonscreen.get_rect(center=statsbutton.get_rect().center))
        window.blit(statsbutton, stats_interact)

    if game_state == 2: # settings
        backbutton.blit(backonscreen, backonscreen.get_rect(center=backbutton.get_rect().center))
        window.blit(backbutton, back_interact)

        resetbutton.blit(resetonscreen, resetonscreen.get_rect(center=resetbutton.get_rect().center))
        window.blit(resetbutton, reset_interact)

    if game_state == 3: # shop
        backbutton.blit(backonscreen, backonscreen.get_rect(center=backbutton.get_rect().center))
        window.blit(backbutton, back_interact)
        window.blit(pointsonscreen, (50, 50))
        window.blit(buytextonscreen, (180, 120))
        window.blit(multiplieronscreen, (180, 160))
        buybutton.blit(buyonscreen, buyonscreen.get_rect(center=buybutton.get_rect().center))
        window.blit(buybutton, buy_interact)

    if game_state == 4: # stats
        backbutton.blit(backonscreen, backonscreen.get_rect(center=backbutton.get_rect().center))
        window.blit(backbutton, back_interact)
        window.blit(yourstatsonscreen, (50, 50))
        window.blit(amountclickedonscreen, (210, 160))
        window.blit(totalpointsonscreen, (210, 200))
        window.blit(spentpointsonscreen, (210, 240))


    pygame.display.flip()