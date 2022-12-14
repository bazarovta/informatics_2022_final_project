#import tkinter
#from tkinter.filedialog import *
from Player import Player
from Enemy import Enemy

#import random

import time
import pygame


def main():
    '''
    the main program
    '''
    WIDTH = 1200
    HEIGHT = 600
    
    pygame.init()
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    first_font = pygame.font.SysFont("comicsansms", 35)
    screen.fill('WHITE')
    first_page = first_font.render("Press Space", True, (255, 0, 0))
    image = pygame.image.load("quest_1/fon.png")
    first_image = pygame.transform.scale(image, (600, 600))
    screen.blit(first_image, (300,0))
    screen.blit(first_page, (500, 350))
    
    pygame.display.update()
    pygame.event.clear()
    

    FPS = 30

    text = pygame.font.Font(None, 50)
    text_data = pygame.font.Font(None, 30)
    
    clock = pygame.time.Clock()

    shells = []


    status = True

    #N = random.randint(1, 4)
    N = 3

    enemies = []

    for i in range(N):
        enemies.append(Enemy(screen))


    player = Player(screen)

    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                break
            
    life = False
    losing = False

    while (status):
        del_shells = []
        del_enemies = []
        screen.fill('WHITE')
        for shell in shells:
            shell.draw()
        player.draw()
        for enemy in enemies:
            enemy.draw()
        text_health_player = text_data.render(str(player.health), True, (0, 255, 0))
        screen.blit(text_health_player, (20, 30))
        for i in range(len(enemies)):
            enemy = enemies[i]
            text_health_enemy = text_data.render(str(enemy.health), True, (255, 0, 0))
            screen.blit(text_health_enemy, (30 + 60 * (i + 1), 30))
        pygame.display.update()
        clock.tick(FPS)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.attack = True
                for enemy in enemies:
                    player.attack_on_enemy(enemy)
            elif event.type == pygame.MOUSEBUTTONUP:
                player.attack = False
        pressed_keys = pygame.key.get_pressed()
        player.move(pressed_keys)
            
        for i in range(len(enemies)):
            enemy = enemies[i]
            if (player.x - enemy.x - enemy.size/2) ** 2 + (player.y - enemy.y - enemy.size/2) ** 2 <= enemy.R ** 2:
                enemy.move_near_player(player)
                if enemy.stamina == 100:
                    shells = enemy.fire(shells, player)
                    enemy.stamina -= 1
                elif enemy.stamina < 100 and enemy.stamina > 0:
                    enemy.stamina -= 1
                elif enemy.stamina <= 0:
                    enemy.stamina = 100
            else:
                enemy.move_far_from_player()
                
            if enemy.health <= 0:
                del_enemies.append(i) 
        for i in range(len(del_enemies)):
            enemies.pop(del_enemies[i])
            for j in range(len(del_enemies)):
                if del_enemies[j] > del_enemies[i]:
                    del_enemies[j] -= 1
            
        for i in range(len(shells)):
            sh = shells[i]
            sh.move()
            if sh.hittest(player) and sh.live > 0:
                player.health -= 10
                sh.live = 0
            if player.health <= 0:
                screen.fill('RED')
                text_score_2 = text.render('You lost', True, (0, 0, 0))
                screen.blit(text_score_2, (WIDTH / 2 - 105, HEIGHT / 2 - 50))
                pygame.display.update()
                time.sleep(2)
                losing = True
                break
            if sh.live <= 0:
                del_shells.append(i)
        
        if not losing:
            for i in range(len(del_shells)):
                shells.pop(del_shells[i])
                for j in range(len(del_shells)):
                    if del_shells[j] > del_shells[i]:
                        del_shells[j] -= 1   
                    
            if player.health > 0 and len(enemies) <= 0:
                screen.fill('GREEN')
                life = True
                text_score_2 = text.render('YOU WIN', True, (0, 0, 0))
                text_advice = text_data.render('Close window to exit', True, (0, 0, 0))
                screen.blit(text_score_2, (WIDTH / 2 - 100, HEIGHT / 2 - 50))
                screen.blit(text_advice, (WIDTH / 2 - 125, HEIGHT / 2))
                pygame.display.update()
                while status:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            status = False
        else:
            player.health = 100
            enemies = []
            for i in range(N):
                enemies.append(Enemy(screen))
            shells = []
            losing = False
            
    return life  
