# Demon Hunter 2017 - Janusz z Sosnowca
# https://docs.google.com/document/d/18VyOV4oTtuUEzCtoHzlJny2LTRh_ZyFmWj0aXPC6f68/edit?usp=sharing
#Demon 뿅 Hero 웃 
import os
import sys
from random import randint
import readchar
import emoji

# Faza 2
# 1. Nad mapą wyświetlać HP gracza w postaci X/Y gdzie X to aktualne życie, a Y maksymalne dostępne
# 1A. Do funkcji draw dodam interface wyswietlajacy Health na Healthmax typu liczbowego z klasy gracza 
# 2. Przy próbie wejścia na demona rysuje się nowy typ ekranu walki 
# 2A. Podczas wykonywania move_object sprawdze jakiego typu jest obiekt jesli jest to typ Demon aktywuje tryb walki ktory jest petla trwajacy az do smierci jednej ze stron lub ucieczki
# walka odbywa się w systemie turowym (gracz zaczyna) i polega na wyborze przez gracza jednej z
# dostępnych opcji:
# a) Uderz - uderza demona za 1HP   |  odejmij 1pkt hp z instancji klasy Demon, jesli jego hp < 1 przerywa walke
# b) Uciekaj - ucieka z walki i zostawia demona z HP tyle ile mu zostało   |  przerywa walke opuszczajac loop. Instancja Demona pozostaja na miejscu z pozostalym hp
# Po wygraniu walki demon znika a w jego miejsce pojawia się zwykły teren  |  Po otrzymaniu ciosu jesli hp < 1 przerwij tryb walki i zmien typ pola na Ground

MOVE_UP = ['w', 'W', 38]
MOVE_DOWN = ['s', 'S', 39]
MOVE_LEFT = ['a', 'A', 40]
MOVE_RIGHT = ['d', 'D', 37]
ESCAPE = ['q', 'Q', 27]
OPTION_1 = ['1']
OPTION_2 = ['2']
OPTION_3 = ['3']
OPTION_4 = ['4']
OPTION_5 = ['5']
BOARD_WIDTH = 25
BOARD_HEIGHT = 25

# Do poprawy:
# 1. Operowanie powinno odbywac się na instancjach a nie na klasach (np. Board.hit(Hero)).
# Klasa to tylko pojemnik do opisania. Wywoływanie metod na klasie to tak jakbym chciał przemalować
# swój samochód i zawołał Car.paint("red") który przemaluje wszystko samochody na świecie
# 2. board i player nie mogą być zmiennymi globalnymi - muszą być definiowane na poziomie funkcji
# main() - do poprawy
# 3. Niespójnie wyświetlanie HP dla gracza i demona. Jeden ma metodę show_hp która robi coś
# a drugi ma też taką metodę która zwraca tylko HP

# Faza 3:
# 1. Zmiana formy atakowania, aby dostępny były dwa tryby: 1. Pięść 2. Kop
# Pięśc ma 80% szansy na trafienie celu, Kop ma 55% na trafienie ale zadaje 2dmg
# Demon ma dwa ataki: Gryzienie (1HP - 60% na trafienie), Atak skrzydłem (3HP - 10% na trafienei)
# 2. Wyświetlanie battleloga - na ekranie walki pod spodem prezentowana jest pełna
# lista akcji wykonanych podczas walki zarówno przez gracza jak i demona np
# - Gracz używa ciosu Kop. Nie trafia
# - Demon używa ciosu Gryzienie. Zadanie obrażenia: 1
# itd.
# 3. W losowym punkcie mapy umieścić wyjście. Gdy gracz na nie wejdzie cała plansza się resetuje,
# gracz odzyskuje utracone życie i może kontynuować podróż. W górnym-prawym rogu planszy umieścić
# informację który to świat (czyli ile razy gracz wszedł w wyjście)
# Faza 4:
# 1. Zmiana grafiki wyjścia na emoji
# 2. Wyświetlanie świata w prawym rogu ekranu (tak jak kończy się mapa) (done)
# 3. Wyświetlanie ikon gracza i przeciwnika podczas walki (done)
# 4. Prezentowanie battleloga podczas walki, a nie po jej zakończeniu (done)
# 5. Dodanie 2 nowych typów przeciwników do mapy (Slime, Tief - done)
# 6. Inwencja własna - udoskonalenie gry (wizualnie lub mechaniki)

class MapItem(object):
    symbol = None
    walkable = False
    fightable = False
    positionx = None
    positiony = None
    
    @staticmethod
    def get_random():
        rnd = randint(1, 100)
        
        if rnd <= 2:
            return Demon()

        if rnd <= 4:
            return Slime()

        if rnd <= 5:
            return Thief()
        
        if rnd <= 10:
            return Tree()
            
        return Ground()
    
    def set_position(self, x, y):
        self.positionx = x;
        self.positiony = y;
        
    def __str__(self):
        return emoji.emojize(self.symbol)

class Attack():
    name = None
    damage = None
    hit_chance = None
    def __init__(self, name, damage, hit_chance):
        self.name = name
        self.damage = damage
        self.hit_chance = hit_chance
    def hit():
        return self.damage;
    #def punch(self):
    #    self.name = "punch"
    #    self.damage = 1
    #    self.hit_chance = 80
    #    print('TESTPUNCH')
    
class Enemy(MapItem):
    fightable = True
    health_max = None
    health = None
    attacks = []
    
    def show_hp(self):
        return ('Hp: {}/{} '.format(self.Health, self.Healthmax))
    
    def __init__(self):
        self.attacks = self.get_attacks()
        self.health = self.health_max
        
    
    def get_attacks(self):
        return []


class Tree(MapItem):
    symbol = ':evergreen_tree:'

class Portal(MapItem):
    symbol = 'O'

class Demon(Enemy):
    name = 'Demon'
    symbol = ':imp:'
    health_max = 5
        
    def get_attacks(self):
        return [Attack("Bite", 1, 60), Attack("Wing attack", 3, 10)]
    
class Slime(Enemy):
    name = 'Slime'
    symbol = ':turtle:'
    health_max = 3
    
    def get_attacks(self):
        return [Attack("Jump", 1, 70), Attack("Splash", 2, 10)]
        

class Thief(Enemy):
    name = 'Thief'
    symbol = ':new_moon_with_face:'
    health_max = 4

    def get_attacks(self):
        return [Attack("Cut", 2, 50), Attack("Shot", 3, 10)]


class Ground(MapItem):
    symbol = ':herb:'
    walkable = True

class Hero(MapItem):
    name = 'Hero'
    symbol = ':runner:'
    Healthmax = 20
    Health = 20
    Level = 1
    Experience = 0
    attacks = []
    def __init__(self):
        self.attacks = [Attack("Punch", 1, 80), Attack("Kick", 2, 60)]
        
    def get_move(self):
        userinput = readchar.readchar()
        if userinput in MOVE_UP:
            return -1, 0
        elif userinput in MOVE_RIGHT:
            return 0, 1
        elif userinput in MOVE_DOWN:
            return 1, 0
        elif userinput in MOVE_LEFT:
            return 0, -1
        elif userinput in ESCAPE:
            sys.exit(0)
        return None

    def show_hp(self):
        return ('Hp: {}/{} '.format(self.Health, self.Healthmax))

class Board():
    mapa = []
    portalscounter = 0
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
    def set_object(self, obj):
        self.mapa[obj.positionx][obj.positiony] = obj
    
    def generate_data(self):  #Map generate
        for i in range(self.width):
            row = []
            self.mapa.insert(i, row)
            for j in range(self.height):
                row.insert(j, [])
                obj = MapItem.get_random();
                obj.set_position(i,j)
                self.set_object(obj)
        x = randint(0, 20)
        y = randint(0, 20)
        portal = Portal()
        portal.set_position(x, y)
        self.set_object(portal)
    
    def draw(self, player):
        self.clear_screen()
        print(' Hp ', player.Health,'/',player.Healthmax, ' Lvl:', player.Level,'                                                   ', self.portalscounter)
        for row in self.mapa:
            for obj in row:
                print(' {} '.format(obj), end="")
            print('');

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def move_object(self, obj, x, y): #Obj = player
        new_x = obj.positionx + x
        new_y = obj.positiony + y
        if new_x >= self.width or new_x < 0:
            return
        if new_y >= self.height or new_y < 0:
            return
        item = self.mapa[new_x][new_y]     
        if item.fightable:
            fight = Fight(obj, item, self)
            fight.fight()
        if item.symbol == Portal.symbol:
            #self.trought_portal(obj) #GENERATE NEW WORLD
            self.trought_portal(obj);
        if not item.walkable:
            return

        obj.under = self.mapa[new_x][new_y] # Under player
        self.mapa[new_x][new_y] = obj # Set player position on map
        self.mapa[obj.positionx][obj.positiony] = obj.under
        obj.set_position(new_x, new_y)
    
    def trought_portal(self, player):
        self.mapa = []
        self.clear_screen()
        self.generate_data()
        player.set_position(player.positionx, player.positiony)
        self.set_object(player)
        self.portalscounter = self.portalscounter + 1

    def get_center_position(self):
        x = int(self.width/2)
        y = int(self.height/2)
        return x,y

class Fight(): 
    battlelog = [] #Add to enemy
    player = None
    board = None
    enemy = None
    def __init__(self, player, enemy, board):
        self.player = player
        self.board = board
        self.enemy = enemy
    def fight(self):  
        while self.player.Health > 0 and self.enemy.Health > 0:
            self.draw_health()
            self.draw_select_menu()
            self.draw_battlelog(self.enemy.battlelog)
            key = self.get_key()
            if key == 1: #ATACK
                #self.hit(self.enemy)
                self.hit_menu_draw()
            elif key == 2:
                pass
            elif key == 3: #Run
                break
            else:
                return
            #AI TURN
            self.ai_attack()
    def hero_died(self):
        self.board.clear_screen()
        print("You Died")
        self.get_key()

    def ai_attack(self):
        if self.enemy.Health <= 0:
            return
        rnd = randint(0, 1)
        self.hit(self.player, self.enemy.attacks[rnd], self.enemy)

    def get_key(self):
        userinput = readchar.readchar()
        if userinput in OPTION_1:
            return 1
        elif userinput in OPTION_2:
            return 2
        elif userinput in OPTION_3:
            return 3
        elif userinput in OPTION_4:
            return 4
        elif userinput in OPTION_5:
            return 5
        return None

    def draw_health(self):
        self.board.clear_screen()
        print(self.player, ' ', self.player.show_hp(), '     ')
        print(self.enemy, ' ', self.enemy.show_hp())

    def draw_select_menu(self):
        print('1/Attack 3/Run') #!

    def hit(self, target, attack, attacker):
        rnd = randint(1, 100)
        hit = False
        if (not rnd > attack.hit_chance): #Hit
            target.Health = target.Health - attack.damage
            hit = True
        self.save_to_battlelog(target, attack, hit, attacker) #miss?
        if target.Health > 0:
            pass #BREAK FIGHT
        else: #DEAD TARGET
            if(target == self.player):
                self.hero_died() #Hero died
                sys.exit(0)
            self.add_experience()
            del self.battlelog[:]
            obj = Ground()
            obj.set_position(target.positionx, target.positiony)
            self.board.set_object(obj)

    def add_experience(self):
        self.player.Experience = self.player.Experience + 1
        if self.player.Experience > 10:
            self.player.Level = self.player.Level + 1
            self.player.Healthmax = self.player.Healthmax + 2
            self.player.Health = self.player.Healthmax
            self.player.Experience = 0

    def save_to_battlelog(self, target, attack, hit, attacker):
        if(hit == True):
            log = ('{} use {} ability. {} take {} dmg'.format(attacker.name, attack.name, target.name, attack.damage))
        else:
            log = ('{} use {} ability. He missed'.format(attacker.name, attack.name))
        self.battlelog.append(log)
        #self.enemy.battlelog.append(log)

    def draw_battlelog(self, enemy):
        for log in self.battlelog:
            print(log)

    def hit_menu_draw(self):
        i = 1
        self.board.clear_screen()
        self.draw_health()
        for Attack in self.player.attacks:
            print(i,'|',Attack.name, 'Dmg:', Attack.damage)
            i = i + 1
        print(i, '|','Back')
        key = self.get_key()
        if key > i:
            return
        elif key == i:
            return
        else:
            self.hit(self.enemy, self.player.attacks[key-1], self.player)


def main():
    board = Board(BOARD_WIDTH, BOARD_HEIGHT)#
    board.generate_data()
    player = Hero() #
    center_x, center_y = board.get_center_position()
    player.set_position(center_x, center_y)

    board.set_object(player)
    
    while True:
        board.draw(player)
        movement = player.get_move()
        if movement is None:
            continue
            
        x, y = movement[0], movement[1]

        board.move_object(player, x, y)

main()