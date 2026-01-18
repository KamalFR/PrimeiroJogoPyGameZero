import pgzrun
import math
import random
from pygame import Rect as rect

WIDTH = 896
HEIGHT = 640

GRAVITY = 0.8
JUMP_FORCE = -16
WALK_SPEED = 4
FISH_SPEED = 6
BEE_SPEED = 3
FRAMES = 0

game_state = "MENU"
sound_enabled = True

button_start = Actor('buttonlong_blue', (WIDTH / 2, HEIGHT / 2 - 100))
button_sound = Actor('buttonround_blue', (WIDTH / 2, HEIGHT / 2))
verified = Actor('iconcheck_bronze', (WIDTH / 2, HEIGHT / 2))
button_exit = Actor('buttonlong_blue', (WIDTH / 2, HEIGHT / 2 + 100))
background = Actor('background_color_trees', (WIDTH / 2, HEIGHT / 2))
water = Actor('water', (WIDTH / 2, HEIGHT / 2))
player = Actor('character_pink_front', (32, 384))
player.v_y = 0
player.direction = "RIGHT"

MAP = [

    "              ",
    "     V        ",
    "    555    B  ",
    "         555  ",
    "              ",
    "       S    34",
    "P     36422211",
    "364222111   11",
    "111   111 F 11",
    "111 F 111   11"
]

blocks = []
static_enemies = []
fish_enemies = []
bee_enemies = []


for line_index, line in enumerate(MAP):
    for col_index, char in enumerate(line):
        pos = (col_index * 64 + 32, line_index * 64 + 32)
        if char == "1":
            blocks.append(Actor('terrain_purple_block_center', pos))
        elif char == "2":
            blocks.append(Actor('bridge_logs', pos))
        elif char == "3":
            blocks.append(Actor('terrain_purple_block_top_left', pos))
        elif char == "4":
            blocks.append(Actor('terrain_purple_block_top_right', pos))
        elif char == "5":
            blocks.append(Actor('block_blue', pos))
        elif char == "6":
            blocks.append(Actor('terrain_purple_block_top', pos))
        elif char == "S":
            static_enemies.append(Actor('barnacle_attack_a', pos))
        elif char == "F":
            fish = Actor('fish_purple_up', pos)
            fish.state = "DOWN"
            fish_enemies.append(fish)
            fish.y_start = fish.y
        elif char == "P":
            player.pos = pos
            player.start_pos = pos
        elif char == "B":
            bee = Actor('bee_a_left', pos)
            bee.moving = "LEFT"
            bee_enemies.append(bee)
            bee.x_start = bee.x
        elif char == "V":
            victory = Actor('flag_yellow_a', pos)

on_ground = False

all_enemies = static_enemies + fish_enemies + bee_enemies

def draw():
    screen.clear()
    if game_state == "MENU":
        button_start.draw()
        screen.draw.text("START", center=button_start.pos, fontsize=40, color="white")
        
        button_sound.draw()
        if sound_enabled:
            verified.draw()

        button_exit.draw()
        screen.draw.text("EXIT", center=button_exit.pos, fontsize=40, color="white")
        
    if game_state == "PLAYING":
        background.draw()
        water.draw()
        for block in blocks:
            block.draw()
        player.draw()
        for enemy in all_enemies:
            enemy.draw()
        victory.draw()
        
    if game_state == "VICTORY":
        screen.fill((50, 200, 50))
        screen.draw.text("VOCÊ VENCEU!", center=(WIDTH/2, HEIGHT/2), fontsize=100, color="white")
        screen.draw.text("Pressione ESC para o Menu", center=(WIDTH/2, HEIGHT/2 + 100), fontsize=30)
            
def on_mouse_down(pos):
    global game_state, sound_enabled
    if game_state == "MENU":
        if button_start.collidepoint(pos):
            game_state = "PLAYING"
        elif button_sound.collidepoint(pos):
            sound_enabled = not sound_enabled
        elif button_exit.collidepoint(pos):
            exit()

def update():
    global game_state, on_ground
    
    if game_state == "PLAYING":
        
        if keyboard.a: 
            player.x -= WALK_SPEED
            for b in blocks:
                if player.colliderect(b):
                    player.left = b.right
        
        if keyboard.d: 
            player.x += WALK_SPEED
            for b in blocks:
                if player.colliderect(b):
                    player.right = b.left
        
        
        player.v_y += GRAVITY
        player.y += player.v_y
        
        if player.x < 0 or player.x > WIDTH:
            player.pos = player.start_pos
            player.v_y = 0
        
        on_ground = False
        for b in blocks:
            if player.colliderect(b):
                if player.v_y > 0: 
                    player.bottom = b.top
                    player.v_y = 0
                    on_ground = True
                elif player.v_y < 0: 
                    player.top = b.bottom
                    player.v_y = 0

        if keyboard.w and on_ground:
            player.v_y = JUMP_FORCE
            on_ground = False
            
        for fish in fish_enemies:
            if fish.state == "UP":
                fish.y -= FISH_SPEED
                if fish.y < fish.y_start - 200: 
                    fish.state = "DOWN"
            else:
                fish.y += FISH_SPEED
                if fish.y > fish.y_start: 
                    fish.state = "UP"
                
            if player.colliderect(fish.inflate(-25, -25)):
                player.pos = player.start_pos
                player.v_y = 0
                
        for enemy in static_enemies:
            if player.colliderect(enemy.inflate(-40, -40)):
                player.pos = player.start_pos
                player.v_y = 0
                
        for bee in bee_enemies:
            if bee.moving == "LEFT":
                bee.x -= BEE_SPEED
                if bee.x < bee.x_start - 150:
                    bee.moving = "RIGHT"
            else:
                bee.x += BEE_SPEED
                if bee.x > bee.x_start:
                    bee.moving = "LEFT"
                    
            if player.colliderect(bee.inflate(-20, -20)):
                player.pos = player.start_pos
                player.v_y = 0
                
        if player.colliderect(victory):
            game_state = "VICTORY"
                
        update_animation()
    
    if game_state == "VICTORY":
        if keyboard.escape:
            game_state = "MENU"
            player.pos = player.start_pos
            player.v_y = 0
    
    if sound_enabled:
            sounds.beepbox.play(-1)  
    if not sound_enabled:
            sounds.beepbox.stop()
                    
def update_animation():
    global FRAMES
    if not on_ground:
        if player.v_y < 0:
            player.image = 'character_pink_jump'
        else:
            player.image = 'character_pink_duck'
    
    elif keyboard.a or keyboard.d:
        # Change walking frames every 10 updates
        if (FRAMES // 10) % 2 == 0:
            player.image = 'character_pink_walk_a'
        else:
            player.image = 'character_pink_walk_b'
    
    else:
        player.image = 'character_pink_front'
    
    for enemy in static_enemies:
            if (FRAMES // 10) % 2 == 0:
                enemy.image = 'barnacle_attack_a'
            else:
                enemy.image = 'barnacle_attack_b'
                
    for bee in bee_enemies:
        if bee.moving == "LEFT":
            if (FRAMES // 10) % 2 == 0:
                bee.image = 'bee_a_left'
            else:
                bee.image = 'bee_b_left'
        else:
            if (FRAMES // 10) % 2 == 0:
                bee.image = 'bee_a_right'
            else:
                bee.image = 'bee_b_right'
    
    for fish in fish_enemies:
        if fish.state == "UP":
            if (FRAMES // 10) % 2 == 0:
                fish.image = 'fish_purple_up'
            else:
                fish.image = 'fish_purple_up2'
        else:
            if (FRAMES // 10) % 2 == 0:
                fish.image = 'fish_purple_down'
            else:
                fish.image = 'fish_purple_down2'   
                      
    FRAMES += 1
    
    if(FRAMES >= 10000):     #avoid overflow
        FRAMES = 0
        
pgzrun.go()