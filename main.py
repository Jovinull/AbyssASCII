import os

run = True
menu = True
play = False
rules = False
key = False

HP = 50
HPMAX = HP
ATK = 3
pot = 1
elix = 0
gold = 0
x = 0
y = 0

map = [
    # x = 0       x = 1         x = 2        x = 3         x = 4          x = 5        x = 6
    ["plains",  "plains",     "plains",     "plains",     "forest",     "mountain",     "cave"],      # y = 0
    ["forest",  "forest",     "forest",     "forest",     "forest",     "hills",    "mountain"],  # y = 1
    ["forest",  "fields",     "bridge",     "plains",     "hills",      "forest",      "hills"],     # y = 2
    ["plains",  "shop",       "town",       "major",      "plains",     "hills",    "mountain"],  # y = 3
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
    "major": {
        "t": "major",
        "e": False},
}

current_tile = map[y][x]
print(current_tile)
name_of_tile = biom[current_tile]['t']
print(name_of_tile)
enemy_tile = biom[current_tile]['e']
print(enemy_tile)

def clear():
    os.system('cls')

def draw():
    print('xX-----------------xX')

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
            print("I'm the creator of this game and these are the rules")
            rules = False
            choice = ''
            input('> ')
        
        else:
            choice = input('# ')
        
        if choice == '1':
            clear()
            name = input("# What's your name, hero? ")
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
                    print('Welcome back, ' + name + '!')
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
        draw()
        print('LOCATION: ' + biom[map[y][x]]['t'])
        draw()
        print('NAME: ' + name)
        print('HP: ' + str(HP) + '/' + str(HPMAX))
        print('ATK ' + str(ATK))
        print('POTIONS: ' + str(pot))
        print('ELIXIRS: ' + str(elix))
        print('GOLD: ' + str(gold))
        print('COORD', x, y)
        draw()
        print('0 - SAVE AND QUIT')
        if y > 0:
            print("1 - NORTH")
        if x < x_len:
            print("2 - EAST")
        if y < y_len:
            print("3 - SOUTH")
        if x > 0:
            print("4 - WEST")
        draw()
        
        dest = input('# ')
        
        if dest == '0':
            play = False
            menu = True
            save()
        elif dest == "1":
            if y > 0:
                y -= 1

        elif dest == "2":
            if x < x_len:
                x += 1

        elif dest == "3":
            if y < y_len:
                y += 1

        elif dest == "4":
            if x > 0:
                x -= 1
