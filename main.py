
import os
import random
import sys
import time
import re
from healthbar import StatusBar, BarStyle
from styles import COLOR_GREEN1, COLOR_DARK, COLOR_YELLOW, COLOR_RED, SYMBOL_BLOCK, SYMBOL_EMPTY, BOX_TL, BOX_TR, BOX_BL, BOX_BR, BOX_H, BOX_V, BOX_T, BOX_B, COLOR_DEFAULT
import graphics

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

# Graphics constants are now imported from graphics.py

map = [
    # x = 0       x = 1         x = 2        x = 3         x = 4          x = 5        x = 6
    ["plains",  "plains",     "plains",     "plains",     "forest",     "mountain",     "cave"],      # y = 0
    ["forest",  "forest",     "forest",     "forest",     "forest",     "hills",    "mountain"],  # y = 1
    ["forest",  "fields",     "bridge",     "plains",     "hills",      "forest",      "hills"],     # y = 2
    ["plains",  "shop",       "town",       "mayor",      "plains",     "hills",    "mountain"],  # y = 3
    ["plains",  "fields",     "fields",     "plains",     "hills",      "mountain", "mountain"],  # y = 4
]

y_len = len(map) - 1
x_len = len(map[0]) -1

biom = {
    "plains": {
        "t": "plains",
        "e": True},
    "forest": {
        "t": "forest",
        "e": True},
    "fields": {
        "t": "fields",
        "e": False},
    "town": {
        "t": "town",
        "e": False},
    "hills": {
        "t": "hills",
        "e": True},
    "mountain": {
        "t": "mountian",
        "e": True},
    "cave": {
        "t": "cave",
        "e": True},
    "shop": {
        "t": "shop",
        "e": False},
    "bridge": {
        "t": "bridge",
        "e": True},
    "mayor": {
        "t": "mayor",
        "e": False},
}

e_list = ["Goblin", "Orc", "Slime"]

mobs = {
    "Goblin": {
        "hp": 15,
        "at": 3,
        "go": 8
    },
    "Orc": {
        "hp": 35,
        "at": 5,
        "go": 18
    },
    "Slime": {
        "hp": 30,
        "at": 2,
        "go": 12
    },
    "Dragon": {
        "hp": 100,
        "at": 8,
        "go": 100
    }
}

current_tile = map[y][x]
print(current_tile)
name_of_tile = biom[current_tile]['t']
print(name_of_tile)
enemy_tile = biom[current_tile]['e']
print(enemy_tile)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw():
    print('xX---------------------------------Xx')

def typewriter(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def animate_art(art, delay=0.05):
    for line in art.split('\n'):
        print(line)
        time.sleep(delay)

def draw_ui(left_lines, right_lines, title="ABYSS ASCII"):
    width_left = 40
    width_right = 36
    
    def strip_ansi(text):
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)
    
    # Header
    print(f"{COLOR_DEFAULT}{BOX_TL}{BOX_H * (width_left)}{BOX_T}{BOX_H * (width_right)}{BOX_TR}")
    
    # Content rows
    max_rows = max(len(left_lines), len(right_lines))
    for i in range(max_rows):
        left = left_lines[i] if i < len(left_lines) else ""
        right = right_lines[i] if i < len(right_lines) else ""
        
        l_clean = strip_ansi(left)
        r_clean = strip_ansi(right)
        
        l_pad = " " * (width_left - len(l_clean))
        r_pad = " " * (width_right - len(r_clean))
        
        print(f"{BOX_V}{left}{l_pad}{BOX_V}{right}{r_pad}{BOX_V}")
        
    # Footer
    print(f"{BOX_BL}{BOX_H * width_left}{BOX_B}{BOX_H * width_right}{BOX_BR}{COLOR_DEFAULT}")

def save():
    list = [
        name,
        str(HP),
        str(ATK),
        str(pot),
        str(elix),
        str(gold),
        str(x),
        str(y),
        str(key),
    ]

    f = open("load.txt", "w")

    for item in list:
        f.write(item + "\n")
    f.close()


def heal(amount):
    global HP, health_bar
    if HP + amount < HPMAX:
        HP += amount
    else:
        HP = HPMAX
    health_bar.update(HP)
    print(f"{name} healed for {amount} HP!")

def battle():
    global fight, play, run, HP, pot, elix, gold, boss

    if not boss:
        enemy = random.choice(e_list)
    else:
        enemy = "Dragon"
        clear()
        animate_art(graphics.DRAGON_ART, 0.02)
        typewriter("O AR ESTÁ QUENTE... A TERRA TREME...", 0.05)
        typewriter("UM RUGIDO ASSSITADOR ECOA PELA CAVERNA!", 0.05)
        time.sleep(1)
    hp = mobs[enemy]["hp"]
    hpmax = hp
    atk = mobs[enemy]["at"]
    g = mobs[enemy]["go"]

    while fight:
        clear()
        
        # Left Panel: Enemy Art & Info
        left = []
        left.append("")
        left.append(f"  {BOX_H * 10} ENEMY {BOX_H * 10}")
        left.append("")
        left.append(f"  DEFEAT THE {enemy.upper()}!")
        left.append("")
        # Add Enemy Art
        art_name = f"{enemy.upper()}_ART"
        enemy_art = getattr(graphics, art_name, "")
        if enemy_art:
            for line in enemy_art.strip('\n').split('\n'):
                left.append(f"  {line}")
        left.append("")
        left.append(f"  HP: {hp}/{hpmax}")
        # Simple text bar for enemy
        enemy_bar_len = 20
        filled = round((hp/hpmax) * enemy_bar_len) if hpmax else 0
        left.append(f"  [{COLOR_RED}{SYMBOL_BLOCK * filled}{COLOR_DARK}{SYMBOL_EMPTY * (enemy_bar_len-filled)}{COLOR_DEFAULT}]")
        left.append("")
        left.append(f"  ATK: {atk}")
        left.append(f"  GOLD DROP: {g}")

        # Right Panel: Player Stats & Menu
        right = []
        right.append("")
        right.append(f"  {BOX_H * 8} PLAYER STATS {BOX_H * 8}")
        right.append("")
        health_bar.maximum = HPMAX
        health_bar.update(HP)
        hp_render = health_bar.render(simple=True).split('\n')
        right.append(f"  HEALTH: {hp_render[0]}")
        right.append("")
        right.append(f"  POTIONS: {pot} (O)")
        right.append(f"  ELIXIRS: {elix} (X)")
        right.append("")
        right.append(f"  {BOX_H * 8} ACTIONS {BOX_H * 8}")
        right.append("")
        right.append("  1 - ATTACK")
        if pot > 0:
            right.append("  2 - USE POTION (30HP)")
        if elix > 0:
            right.append("  3 - USE ELIXIR (50HP)")
        
        draw_ui(left, right)
        
        choice = input("# ")

        if choice == "1":
            hp -= ATK
            typewriter(f"{name} desferiu um golpe de {ATK} de dano no {enemy}!")
            if hp > 0:
                HP -= atk
                typewriter(f"O {enemy} contra-atacou causando {atk} de dano!")
            input("> ")

        elif choice == "2":
            if pot > 0:
                pot -= 1
                heal(30)
                HP -= atk
                print(enemy + " dealt " + str(atk) + " damage to " + name + ".")
            else:
                print("You don't have any potions!")
            input("> ")
        
        elif choice == "3":
            if elix > 0:
                elix -= 1
                heal(50)
                HP -= atk
                print(enemy + " dealt " + str(atk) + " damage to " + name + ".")
            else:
                print("You don't have any elixirs!")
            input("> ")

        if HP <= 0:
            typewriter(f"O {enemy} derrotou {name}...", 0.06)
            draw()
            fight = False
            play = False
            run = False
            typewriter("FIM DE JOGO", 0.1)
            input("> ")

        if hp <= 0:
            typewriter(f"{name} derrotou o {enemy}!", 0.04)
            draw()
            fight = False
            gold += g
            typewriter(f"Você encontrou {g} de ouro no corpo do {enemy}.")
            if random.randint(0, 100) <= 30:
                pot += 1
                print("You found a potion on the " + enemy + "!")
                typewriter("Congratulations! You've defeated the dragon and won the game!", 0.05)
                play = False
                run = False
            input("> ")
            clear()

def shop():
    global buy, gold, pot, elix, ATK

    while buy:
        clear()
        # Add Shopkeeper Art
        for line in graphics.SHOPKEEPER_ART.strip('\n').split('\n'):
            print(f"  {line}")
        draw()
        print("Welcome to the shop!")
        draw()
        print("GOLD: " + str(gold))
        print("POTIONS: " + str(pot))
        print("ELIXIRS: " + str(elix))
        print("ATK: " + str(ATK))
        draw()
        print("1 - BUY POTION (30HP) - 5 GOLD")
        print("2 - BUY ELIXIR (MAXHP) - 8 GOLD")
        print("3 - UPGRADE WEAPON (+2ATK) - 10 GOLD")
        print("4 - LEAVE")
        draw()

        choice = input("# ")

        if choice == "1":
            if gold >= 5:
                pot += 1
                gold -= 5
                print("You've bought a potion!")
            else:
                print("Not enough gold!")
            input("> ")

        elif choice == "2":
            if gold >= 8:
                elix += 1
                gold -= 8
                print("You've bought an elixir!")
            else:
                print("Not enough gold!")
            input("> ")

        elif choice == "3":
            if gold >= 10:
                ATK += 2
                gold -= 10
                print("You've upgraded your weapon!")
            else:
                print("Not enough gold!")
            input("> ")

        elif choice == "4":
            buy = False

def mayor():
    global speak, key

    while speak:
        clear()
        # Add Mayor Art
        for line in graphics.MAYOR_ART.strip('\n').split('\n'):
            print(f"  {line}")
        draw()
        typewriter("Prefeito: Olá, " + name + "!", 0.04)
        if ATK < 10:
            typewriter("Prefeito: Você ainda não é forte o suficiente para enfrentar o dragão!", 0.04)
            typewriter("Prefeito: Continue treinando e volte quando sua espada estiver mais afiada.", 0.04)
            key = False
        else:
            typewriter("Prefeito: Sinto que você está pronto. O destino do reino está em suas mãos!", 0.04)
            typewriter("Prefeito: Pegue esta chave, mas tenha cuidado... o dragão não terá piedade.", 0.04)
            key = True

        draw()
        print("1 - LEAVE")
        draw()

        choice = input("# ")

        if choice == "1":
            speak = False

def cave():
    global boss, key, fight

    while boss:
        clear()
        animate_art(graphics.CAVE_ART, 0.03)
        draw()
        typewriter("Você está na entrada da Caverna do Dragão. O medo sopra do interior...", 0.04)
        draw()
        if key:
            print("1 - USE KEY")
        print("2 - TURN BACK")
        draw()

        choice = input("# ")

        if choice == "1":
            if key:
                fight = True
                battle()
        elif choice == "2":
            boss = False

if __name__ == "__main__":
    while run:
        while menu:
            clear()
            draw()
            print('1, NEW GAME')
            print('2, LOAD GAME')
            print('3, RULEs')
            print('4, QUIT GAME')
            draw()
            
            if rules:
                clear()
                draw()
                typewriter("REGRAS DO JOGO:", 0.05)
                print("- Use os números para navegar e agir.")
                print("- Enfrente monstros para ganhar ouro e experiência.")
                print("- Fale com o Prefeito para destravar o desafio final.")
                print("- Derrote o Dragão para vencer o jogo.")
                draw()
                rules = False
                choice = ''
                input('> Pressione ENTER para voltar')
            
            else:
                choice = input('# ')
            
            if choice == '1':
                clear()
                animate_art(graphics.TITLE_ART)
                print()
                typewriter("No abismo mais profundo, onde os caracteres ASCII desaparecem no nada...")
                typewriter("Um herói é convocado para enfrentar a escuridão.")
                print()
                name = input("# Qual o seu nome, herói? ")
                clear()
                typewriter(f"Bem-vindo, {name}. Sua jornada começa agora...")
                time.sleep(1)
                menu = False
                play = True
            elif choice == '2':
                try:
                    f = open('load.txt', 'r')
                    load_list = f.readlines()
                    if len(load_list) == 9:
                        name = load_list[0][:-1]
                        HP = int(load_list[1][:-1])
                        ATK = int(load_list[2][:-1])
                        pot = int(load_list[3][:-1])
                        elix = int(load_list[4][:-1])
                        gold = int(load_list[5][:-1])
                        x = int(load_list[6][:-1])
                        y = int(load_list[7][:-1])
                        key = bool(load_list[8][:-1])
                        clear()
                        typewriter(f"Bem-vindo de volta, {name}!", 0.04)
                        input('> ')
                        menu = False
                        play = True
                    else:
                        print('Corrupt save file!')
                        input('> ')
                except OSError:
                    print('No loadable save file!')
                    input('> ')
            elif choice == '3':
                rules = True
            elif choice == '4':
                quit()

        while play:
            save() # autosave
            clear()
            
            if not standing:
                if biom[map[y][x]]['e']:
                    if random.randint(0, 100) <= 30:
                        fight = True
                        battle()
            
            if play:
            
                # Left Panel: Location & World
                left = []
                left.append("")
                left.append(f"  {BOX_H * 8} EXPLORATION {BOX_H * 8}")
                left.append("")
                left.append(f"  LOCATION: {biom[map[y][x]]['t'].upper()}")
                left.append(f"  COORD: ({x}, {y})")
                left.append("")
                # Add Location Art
                loc_type = biom[map[y][x]]['t'].upper()
                art_name = f"{loc_type}_ART"
                loc_art = getattr(graphics, art_name, "")
                if loc_art:
                    for line in loc_art.strip('\n').split('\n'):
                        left.append(f"  {line}")
                left.append("")
                left.append(f"  The path ahead is {biom[map[y][x]]['t']}.")
                if map[y][x] in ["shop", "mayor", "cave"]:
                    left.append(f"  {COLOR_YELLOW}!! INTEREST POINT DETECTED !!{COLOR_DEFAULT}")
                
                # Right Panel: Player Status & Menu
                right = []
                right.append("")
                right.append(f"  {BOX_H * 8} {name.upper()} {BOX_H * 8}")
                right.append("")
                health_bar.maximum = HPMAX
                health_bar.update(HP)
                hp_render = health_bar.render(simple=True).split('\n')
                right.append(f"  HEALTH: {hp_render[0]}")
                right.append(f"  ATK: {ATK}")
                right.append(f"  GOLD: {gold}")
                right.append("")
                right.append(f"  POTIONS: {pot}  ELIXIRS: {elix}")
                right.append("")
                right.append(f"  {BOX_H * 8} NAVIGATION {BOX_H * 8}")
                right.append("")
                if y > 0: right.append("  1 - NORTH")
                if x < x_len: right.append("  2 - EAST")
                if y < y_len: right.append("  3 - SOUTH")
                if x > 0: right.append("  4 - WEST")
                if pot > 0: right.append("  5 - USE POTION")
                if elix > 0: right.append("  6 - USE ELIXIR")
                if map[y][x] in ["shop", "mayor", "cave"]:
                    right.append(f"  7 - ENTER {map[y][x].upper()}")
                right.append("  0 - SAVE AND QUIT")

                draw_ui(left, right)
                
                dest = input('# ')
                
                if dest == '0':
                    play = False
                    menu = True
                    save()
                elif dest == "1":
                    if y > 0:
                        y -= 1
                        standing = False

                elif dest == "2":
                    if x < x_len:
                        x += 1
                        standing = False

                elif dest == "3":
                    if y < y_len:
                        y += 1
                        standing = False

                elif dest == "4":
                    if x > 0:
                        x -= 1
                        standing = False
                
                elif dest == "5":
                    if pot > 0:
                        pot -= 1
                        heal(30)
                    else:
                        print("You don't have any potions!")
                    input("> ")
                    standing = True
                
                elif dest == "6":
                    if elix > 0:
                        elix -= 1
                        heal(50)
                    else:
                        print("You don't have any elixirs!")
                    input("> ")
                    standing = True
                
                elif dest == "7":
                    if map[y][x] == "shop":
                        buy = True
                        shop()
                    elif map[y][x] == "mayor":
                        speak = True
                        mayor()
                    elif map[y][x] == "cave":
                        boss = True
                        cave()
                
                else:
                    standing = True
