import os
import random
import sys
import time
import re
from healthbar import StatusBar, BarStyle
from styles import COLOR_GREEN1, COLOR_DARK, COLOR_YELLOW, COLOR_RED, SYMBOL_BLOCK, SYMBOL_EMPTY, BOX_TL, BOX_TR, BOX_BL, BOX_BR, BOX_H, BOX_V, BOX_T, BOX_B, COLOR_DEFAULT, get_rgb
import graphics
from engine import RetroEngine

# Initialize Engine
engine = RetroEngine(width=80, height=45)

run = True
menu = True
play = False
rules = False
key = False
fight = False
standing = True
buy = False
speak = False
boss = False

HP = 50
HPMAX = HP
ATK = 3
pot = 1
elix = 0
gold = 100
x = 0
y = 0

# Health bar setup
health_bar_style = BarStyle(symbol_full=SYMBOL_BLOCK, symbol_empty=SYMBOL_EMPTY, length=15, color_full=COLOR_GREEN1, color_empty=COLOR_DARK)
health_bar = StatusBar("HP", HP, HPMAX, health_bar_style, color_warning=COLOR_YELLOW, color_critical=COLOR_RED)

map = [
    ["plains",  "plains",     "plains",     "plains",     "forest",     "mountain",     "cave"],
    ["forest",  "forest",     "forest",     "forest",     "forest",     "hills",    "mountain"],
    ["forest",  "fields",     "bridge",     "plains",     "hills",      "forest",      "hills"],
    ["plains",  "shop",       "town",       "mayor",      "plains",     "hills",    "mountain"],
    ["plains",  "fields",     "fields",     "plains",     "hills",      "mountain", "mountain"],
]

y_len = len(map) - 1
x_len = len(map[0]) -1

biom = {
    "plains": {"t": "plains", "e": True},
    "forest": {"t": "forest", "e": True},
    "fields": {"t": "fields", "e": False},
    "town": {"t": "town", "e": False},
    "hills": {"t": "hills", "e": True},
    "mountain": {"t": "mountian", "e": True},
    "cave": {"t": "cave", "e": True},
    "shop": {"t": "shop", "e": False},
    "bridge": {"t": "bridge", "e": True},
    "mayor": {"t": "mayor", "e": False},
}

e_list = ["Goblin", "Orc", "Slime"]

mobs = {
    "Goblin": {"hp": 15, "at": 3, "go": 8},
    "Orc": {"hp": 35, "at": 5, "go": 18},
    "Slime": {"hp": 30, "at": 2, "go": 12},
    "Dragon": {"hp": 100, "at": 8, "go": 100}
}

name = "Hero"

def clear():
    engine.clear_grid()

def typewriter(text, delay=0.03):
    # For Pygame, we'll just add the text and render (maybe simulate typing later)
    # Since we use a grid, we'll need a way to manage message logs
    pass

def animate_art(art, delay=0.05):
    # This will be handled by the UI drawing functions
    pass

def strip_ansi(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def draw_ui(left_lines, right_lines, title="ABYSS ASCII"):
    engine.clear_grid()
    width_left = 40
    width_right = 36
    
    # Header
    engine.add_text(0, 0, f"{BOX_TL}{BOX_H * width_left}{BOX_T}{BOX_H * width_right}{BOX_TR}")
    
    # Content rows
    max_rows = max(len(left_lines), len(right_lines))
    for i in range(max_rows):
        left = left_lines[i] if i < len(left_lines) else ""
        right = right_lines[i] if i < len(right_lines) else ""
        
        # Parse colors from lines (very basic parsing)
        # In a real engine we'd have a better way, but for now we'll strip ansi 
        # for positioning and handle a few specific color constants
        
        l_clean = strip_ansi(left)
        r_clean = strip_ansi(right)
        
        # Basic color mapping for rendering
        # This is a bit complex for a simple grid, so we'll just render plain text 
        # and maybe add a color property to left/right lines in a next iteration
        
        engine.add_text(0, i+1, BOX_V)
        # We'll just render the clean text for now to ensure layout
        engine.add_text(1, i+1, l_clean)
        engine.add_text(width_left + 1, i+1, BOX_V)
        engine.add_text(width_left + 2, i+1, r_clean)
        engine.add_text(width_left + width_right + 2, i+1, BOX_V)
        
    # Footer
    engine.add_text(0, max_rows + 1, f"{BOX_BL}{BOX_H * width_left}{BOX_B}{BOX_H * width_right}{BOX_BR}")
    engine.render()

def save():
    data = [name, str(HP), str(ATK), str(pot), str(elix), str(gold), str(x), str(y), str(key)]
    with open("load.txt", "w") as f:
        for item in data:
            f.write(item + "\n")

def heal(amount):
    global HP, health_bar
    if HP + amount < HPMAX:
        HP += amount
    else:
        HP = HPMAX
    health_bar.update(HP)

def battle():
    global fight, play, run, HP, pot, elix, gold, boss
    enemy = "Dragon" if boss else random.choice(e_list)
    hp = mobs[enemy]["hp"]
    hpmax = hp
    atk = mobs[enemy]["at"]
    g = mobs[enemy]["go"]

    while fight:
        left = ["", f"  {BOX_H * 10} ENEMY {BOX_H * 10}", "", f"  DEFEAT THE {enemy.upper()}!", ""]
        art_name = f"{enemy.upper()}_ART"
        enemy_art = getattr(graphics, art_name, "")
        if enemy_art:
            for line in enemy_art.strip('\n').split('\n'):
                left.append(f"  {line}")
        left.append("")
        left.append(f"  HP: {hp}/{hpmax}")
        # Simplistic UI for now, no nested ANSI in list
        left.append(f"  ATK: {atk}")
        left.append(f"  GOLD DROP: {g}")

        right = ["", f"  {BOX_H * 8} PLAYER STATS {BOX_H * 8}", ""]
        health_bar.update(HP)
        right.append(f"  HEALTH: {HP}/{HPMAX}")
        right.append("")
        right.append(f"  {BOX_H * 8} INVENTORY {BOX_H * 8}", )
        right.append(f"  POTIONS: {pot}")
        right.append(f"  ELIXIRS: {elix}")
        right.append("")
        right.append(f"  {BOX_H * 8} ACTIONS {BOX_H * 8}", )
        right.append("  1 - ATTACK")
        if pot > 0: right.append("  2 - USE POTION (30HP)")
        if elix > 0: right.append("  3 - USE ELIXIR (MAXHP)")
        
        draw_ui(left, right)
        choice = engine.wait_for_input()

        if choice == "1":
            hp -= ATK
            if hp > 0:
                HP -= atk
        elif choice == "2" and pot > 0:
            pot -= 1
            heal(30)
            HP -= atk
        elif choice == "3" and elix > 0:
            elix -= 1
            heal(50)
            HP -= atk

        if HP <= 0:
            fight = False
            play = False
            run = False
        if hp <= 0:
            fight = False
            gold += g
            if random.randint(0, 100) <= 30:
                pot += 1
            if boss:
                play = False
                run = False

def shop():
    global buy, gold, pot, elix, ATK
    while buy:
        left = ["", f"  {BOX_H * 10} SHOP {BOX_H * 10}", ""]
        for line in graphics.SHOPKEEPER_ART.strip('\n').split('\n'):
            left.append(f"  {line}")
        left.append("")
        left.append("    POTION         ELIXIR")
        left.append("    +30 HP         MAX HP")

        right = ["", f"  {BOX_H * 8} YOUR POCKET {BOX_H * 8}", "", f"  GOLD: {gold}", ""]
        right.append(f"  {BOX_H * 8} INVENTORY {BOX_H * 8}")
        right.append(f"  POTIONS: {pot}")
        right.append(f"  ELIXIRS: {elix}")
        right.append(f"  WEAPON ATK: {ATK}")
        right.append("")
        right.append(f"  {BOX_H * 8} ACTIONS {BOX_H * 8}")
        right.append("  1 - BUY POTION  (5G)")
        right.append("  2 - BUY ELIXIR  (8G)")
        right.append("  3 - WEAPON UPGRADE (10G)")
        right.append("  4 - LEAVE SHOP")

        draw_ui(left, right)
        choice = engine.wait_for_input()

        if choice == "1" and gold >= 5:
            pot += 1
            gold -= 5
        elif choice == "2" and gold >= 8:
            elix += 1
            gold -= 8
        elif choice == "3" and gold >= 10:
            ATK += 2
            gold -= 10
        elif choice == "4":
            buy = False

def mayor():
    global speak, key
    while speak:
        engine.clear_grid()
        lines = graphics.MAYOR_ART.strip('\n').split('\n')
        for i, line in enumerate(lines):
            engine.add_text(2, i+2, line)
        
        y_off = len(lines) + 4
        if ATK < 10:
            engine.add_text(2, y_off, "Prefeito: Você ainda não é forte o suficiente!")
            key = False
        else:
            engine.add_text(2, y_off, "Prefeito: O destino do reino está em suas mãos!")
            key = True
        
        engine.add_text(2, y_off + 2, "1 - LEAVE")
        engine.render()
        choice = engine.wait_for_input()
        if choice == "1":
            speak = False

def cave():
    global boss, key, fight
    while boss:
        engine.clear_grid()
        lines = graphics.CAVE_ART.strip('\n').split('\n')
        for i, line in enumerate(lines):
            engine.add_text(2, i+2, line)
        
        y_off = len(lines) + 4
        engine.add_text(2, y_off, "Caverna do Dragão...")
        if key: engine.add_text(2, y_off + 2, "1 - USE KEY")
        engine.add_text(2, y_off + 3, "2 - TURN BACK")
        engine.render()
        
        choice = engine.wait_for_input()
        if choice == "1" and key:
            fight = True
            battle()
        elif choice == "2":
            boss = False

if __name__ == "__main__":
    while run:
        while menu:
            engine.clear_grid()
            engine.add_text(10, 5, "1 - NEW GAME")
            engine.add_text(10, 7, "2 - LOAD GAME")
            engine.add_text(10, 9, "3 - RULES")
            engine.add_text(10, 11, "4 - QUIT")
            engine.render()
            
            choice = engine.wait_for_input()
            if choice == "1":
                name = engine.get_input_text(10, 15, "Qual o seu nome, herói? ")
                menu = False
                play = True
            elif choice == "2":
                try:
                    with open('load.txt', 'r') as f:
                        load_list = f.readlines()
                        name = load_list[0].strip()
                        HP = int(load_list[1])
                        ATK = int(load_list[2])
                        pot = int(load_list[3])
                        elix = int(load_list[4])
                        gold = int(load_list[5])
                        x = int(load_list[6])
                        y = int(load_list[7])
                        key = load_list[8].strip() == 'True'
                        menu = False
                        play = True
                except:
                    pass
            elif choice == "4":
                run = False

        while play:
            save()
            if not standing:
                if biom[map[y][x]]['e']:
                    if random.randint(0, 100) <= 30:
                        fight = True
                        battle()
            
            if play:
                left = ["", f"  {BOX_H * 8} EXPLORATION {BOX_H * 8}", ""]
                left.append(f"  LOCATION: {biom[map[y][x]]['t'].upper()}")
                left.append(f"  COORD: ({x}, {y})")
                left.append("")
                loc_type = biom[map[y][x]]['t'].upper()
                loc_art = getattr(graphics, f"{loc_type}_ART", "")
                if loc_art:
                    for line in loc_art.strip('\n').split('\n'):
                        left.append(f"  {line}")

                right = ["", f"  {name.upper()}", ""]
                right.append(f"  HEALTH: {HP}/{HPMAX}")
                right.append(f"  ATK: {ATK}")
                right.append(f"  GOLD: {gold}")
                right.append("")
                right.append(f"  INVENTORY")
                right.append(f"  POTIONS: {pot}")
                right.append(f"  ELIXIRS: {elix}")
                right.append("")
                right.append(f"  NAVIGATION")
                if y > 0: right.append("  1 - NORTH")
                if x < x_len: right.append("  2 - EAST")
                if y < y_len: right.append("  3 - SOUTH")
                if x > 0: right.append("  4 - WEST")
                if pot > 0: right.append("  5 - USE POTION")
                if map[y][x] in ["shop", "mayor", "cave"]:
                    right.append(f"  7 - ENTER {map[y][x].upper()}")
                right.append("  0 - QUIT")

                draw_ui(left, right)
                dest = engine.wait_for_input()
                
                if dest == '0':
                    play = False
                    menu = True
                elif dest == "1" and y > 0:
                    y -= 1
                    standing = False
                elif dest == "2" and x < x_len:
                    x += 1
                    standing = False
                elif dest == "3" and y < y_len:
                    y += 1
                    standing = False
                elif dest == "4" and x > 0:
                    x -= 1
                    standing = False
                elif dest == "5" and pot > 0:
                    pot -= 1
                    heal(30)
                    standing = True
                elif dest == "7":
                    if map[y][x] == "shop": buy = True; shop()
                    elif map[y][x] == "mayor": speak = True; mayor()
                    elif map[y][x] == "cave": boss = True; cave()
                else:
                    standing = True
