import os
import math
import random
import pygame
import time

# creating a screen and countdown
clock = pygame.time.Clock()
size = width, height = 1200, 705
screen = pygame.display.set_mode(size)
resume = True
file = "background_music.mp3"
pygame.mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.play(-1)

# function for loading images
def load_image(name):
    fullname = os.path.join('img', name)
    image = pygame.image.load(fullname).convert_alpha()
    return image


# start screen
def start_screen():
    global resume
    FPS = 30

    first_screen = pygame.sprite.Group()
    background = pygame.sprite.Sprite()

    # create starter picture for game
    background.image = load_image("starter_screen_1.png")
    background.image = pygame.transform.scale(background.image, (1200, 705))
    background.rect = background.image.get_rect()
    first_screen.add(background)

    # create start game button
    start_btn = pygame.sprite.Sprite()
    start_btn.image = load_image("start_game_btn.png")
    start_btn.image = pygame.transform.scale(start_btn.image, (200, 100))
    start_btn.rect = start_btn.image.get_rect()
    start_btn.rect.x = 500
    start_btn.rect.y = 302
    first_screen.add(start_btn)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                resume = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if start_btn.rect.collidepoint(x, y):
                    # if player push on button starting the game
                    return
        first_screen.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


# class for animated characters
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, speed_increase, health, scale_x, scale_y, money_to_kill):
        super().__init__(mob_sprites)
        self.frames = []
        self.frames_kill = []
        self.count = 0
        self.cut_sheet(sheet, columns, rows)
        self.cut_sheet(load_image("kill_enemy.png"), 3, 1)
        for i in range(len(self.frames)):
            self.frames[i] = pygame.transform.scale(self.frames[i], (scale_x, scale_y))
        for i in range(len(self.frames_kill)):
            self.frames_kill[i] = pygame.transform.scale(self.frames_kill[i], (60, 40))
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.x = path[0][0]
        self.y = path[0][1]
        self.kill_enemy = 0
        self.speed_increase = speed_increase
        self.rect = self.rect.move(x, y)
        self.flipped = False
        self.health = health
        self.cur_frame_kill = 0
        self.move_enemy = True
        self.count_animation = 3
        self.count_animation_1 = 0
        self.money_to_kill = money_to_kill

    def cut_sheet(self, sheet, columns, rows):
        # create animated images
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                if columns == 3:
                    self.frames_kill.append(sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size)))
                else:
                    self.frames.append(sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size)))

    def update(self):
        global money, health
        self.count_animation_1 += 1

        # if enemy is dead kill him sprite
        if self.kill_enemy == 3:
            money += 7
            self.kill()

        # if enemy health <= 0 replace him sprite for dead sprite
        if self.health <= 0:
            self.kill_enemy += 1
            self.cur_frame_kill = (self.cur_frame_kill + 1) % len(self.frames_kill)
            self.image = self.frames_kill[self.cur_frame_kill]
            self.move_enemy = False

        # animated
        elif self.count_animation == self.count_animation_1:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.count_animation_1 = 0

        # if enemy reach the end kill him sprite
        if self.x >= 1270:
            health -= 1
            self.kill()

    def move(self):
        if self.move_enemy:
            x1, y1 = path[self.count]

            # if enemy is reach the last point
            if self.count + 1 >= len(path):
                x2, y2 = (1250, 278)
            else:
                x2, y2 = path[self.count + 1]

            # find out the path of the Pythagorean theorem
            dirn = ((x2 - x1) * 2, (y2 - y1) * 2)
            length = math.sqrt((dirn[0]) ** 2 + (dirn[1]) ** 2)
            dirn = (dirn[0] / length * self.speed_increase, dirn[1] / length * self.speed_increase)

            # if enemy is turning left
            if (dirn[0] < 0 and not (self.flipped)):
                self.flipped = True
                for x, img in enumerate(self.frames):
                    self.frames[x] = pygame.transform.flip(img, True, False)

            # if enemy is turning right
            elif dirn[0] > 0 and self.flipped:
                self.flipped = False
                for x, img in enumerate(self.frames):
                    self.frames[x] = pygame.transform.flip(img, True, False)

            move_x, move_y = ((self.x + dirn[0]), (self.y + dirn[1]))
            self.x = move_x
            self.y = move_y
            if dirn[0] >= 0:  # moving right
                if dirn[1] >= 0:  # moving down
                    if self.x >= x2 and self.y >= y2:
                        self.count += 1
                else:  # moving up
                    if self.x >= x2 and self.y <= y2:
                        self.count += 1
            else:  # moving left
                if dirn[1] > 0:  # moving down
                    if self.x <= x2 and self.y >= y2:
                        self.count += 1
                else:  # moving up
                    if self.x <= x2 and self.y <= y2:
                        self.count += 1

            # move enemy
            self.rect.x = self.x
            self.rect.y = self.y


# Archer tower class
class ArcherTower(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(ARCHERS)
        self.frames = []
        self.count = 0
        self.cut_sheet(sheet, columns, rows)
        for i in range(len(self.frames)):
            self.frames[i] = pygame.transform.scale(self.frames[i], (40, 40))
        self.cur_frame = 0

        self.x = x + 20
        self.y = y + 70
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.flipped = False
        self.flipped_x = 0
        self.radius = 200
        self.count_animation = 0

        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 10)

        self.time = time.time()
        self.time_for_array = time.time()
        self.price = 100
        self.damage = 1

    def cut_sheet(self, sheet, columns, rows):
        # create animated images
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def attack(self):
        for i in mob_sprites:

            # if enemy in radius
            if math.sqrt((self.x - i.rect.x) ** 2 + (
                    self.y - i.rect.y) ** 2) < self.radius:
                self.time_for_array = time.time()
                i.health -= self.damage
                self.flipped_x = self.x - i.rect.x

                # creating arrow sprite
                arrow = pygame.sprite.Sprite()
                arrow.image = arrow_image
                arrow.image = pygame.transform.scale(arrow.image, (7, 15))
                arrow.rect = arrow.image.get_rect()

                # move arrow
                dirn = ((self.x - i.rect.x - 10) * 2, (self.y - i.rect.y) * 2)
                length = math.sqrt((dirn[0]) ** 2 + (dirn[1]) ** 2)
                if self.y - i.rect.y > 0:
                    # if i in self.array:
                    #     r = 40
                    # else:
                    #     r = 20
                    r = random.randint(10, 60)
                else:
                    r = random.randint(10, 100)
                    # if i in self.array:
                    #     r = 60
                    # else:
                    #     r = 30
                dirn = (dirn[0] / length * r, dirn[1] / length * r)
                move_x, move_y = ((self.x - dirn[0]), (self.y - dirn[1]))

                # turn arrow by a suitable degree
                position = pygame.math.Vector2(self.x, self.y)
                enemy_pos = pygame.math.Vector2(i.rect.x + 30, i.rect.y + 30)
                pos = enemy_pos - position
                y_axis = pygame.math.Vector2(0, -1)
                angle = -y_axis.angle_to(pos)
                arrow.image = pygame.transform.rotate(arrow.image, angle)

                # move arrow
                arrow.rect.x = move_x
                arrow.rect.y = move_y - 50
                ARROW.add(arrow)
                ARROW.draw(screen)
                arrow.kill()

                return True

        return False

    def update(self):

        # attack at a certain time
        if time.time() - self.time_for_array >= 0.1:
            if self.attack():
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]

        # turn archer left when he attack enemy
        if self.flipped_x < 0 and self.flipped:
            self.flipped = False
            for x, img in enumerate(self.frames):
                self.frames[x] = pygame.transform.flip(img, True, False)

        # turn archer right when he attack enemy
        elif self.flipped_x > 0 and not self.flipped:
            self.flipped = True
            for x, img in enumerate(self.frames):
                self.frames[x] = pygame.transform.flip(img, True, False)

    def get(self):
        # send pos
        return (self.x, self.y)

    def upgrade_tower(self):
        # upgrade tower
        self.price += 50
        self.damage += 1
        self.radius += 20


# class for places
class BuildingPlaces(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(TOWER_BUILDING_SPRITES)
        self.image = load_image("building_place.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.building_place_num = BUILDING_PLACE_COORDS.index([x, y])


# main function
def main():
    global path, all_sprites, mob_sprites, TOWER_SPRITES, TOWER_BUILDING_SPRITES, TOWER_BOUGHT, TOWER_BOUGHT_RING, \
        ARCHERS, ARROW, BUILDING_PLACE_COORDS, arrow_image, screen, money, health, resume

    # path
    path = [[-80, 455], [154, 455], [200, 495], [710, 507], [767, 424], [710, 298], [450, 298], [390, 205],
            [450, 110], [1250, 110]]
    time_now = time.time()
    BUILDING_PLACE_COORDS = [[400, 385], [580, 380], [495, 595], [850, 380], [497, 160], [685, 157], [870, 155]]
    waves = [20, 30, 25, 40, 50]
    waves_2 = [0, 10, 20, 30, 0]
    # starter characteristics game
    money = 300
    health = 10
    pygame.init()
    clock = pygame.time.Clock()
    size = width, height = 1200, 705
    screen = pygame.display.set_mode(size)

    # all  groups sprites
    all_sprites = pygame.sprite.Group()
    mob_sprites = pygame.sprite.Group()
    information_menu_bar = pygame.sprite.Group()
    TOWER_SPRITES = pygame.sprite.Group()
    TOWER_BUILDING_SPRITES = pygame.sprite.Group()
    TOWER_BOUGHT = pygame.sprite.Group()
    TOWER_BOUGHT_RING = pygame.sprite.Group()
    ARCHERS = pygame.sprite.Group()
    ARROW = pygame.sprite.Group()

    # create information bar
    menu_bar = pygame.sprite.Sprite()
    menu_bar.image = load_image("information_bar_in_game.png")
    menu_bar.image = pygame.transform.scale(menu_bar.image, (200, 100))
    menu_bar.rect = menu_bar.image.get_rect()
    menu_bar.rect.x = 20
    menu_bar.rect.y = 20
    information_menu_bar.add(menu_bar)

    # create pause button
    pause_pic = pygame.sprite.Sprite()
    pause_pic.image = load_image("pause.png")
    pause_pic.image = pygame.transform.scale(pause_pic.image, (55, 55))
    pause_pic.rect = pause_pic.image.get_rect()
    pause_pic.rect.x = 230
    pause_pic.rect.y = 20
    information_menu_bar.add(pause_pic)

    # arrow image
    arrow_image = load_image("arrow.png")
    arrow_image = pygame.transform.rotate(arrow_image, 90)

    # set building places
    for i in range(len(BUILDING_PLACE_COORDS)):
        x = BUILDING_PLACE_COORDS[i][0]
        y = BUILDING_PLACE_COORDS[i][1]
        BuildingPlaces(x, y)

    # create map
    map = pygame.sprite.Sprite()
    map.image = load_image("map-main.png")
    map.image = pygame.transform.scale(map.image, (1200, 705))
    map.rect = map.image.get_rect()
    all_sprites.add(map)

    PAUSE = False
    fps = 30
    running = True
    count_of_enimes = 0
    count_of_wave = 0

    # spawn enemies
    SPAWNENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWNENEMY, 500)

    # creating music




    # start game
    while running:
        time_wait = time.time() - time_now
        for event in pygame.event.get():

            # if player quit game
            if event.type == pygame.QUIT:
                running = False
                resume = False

            # spawn enemies
            if event.type == SPAWNENEMY and 0 != waves[count_of_wave] and (
                    time_wait >= 20 or (count_of_wave == 0 and time_wait >= 5)):
                waves[count_of_wave] -= 1
                AnimatedSprite(load_image("bat_enemy.png"), 4, 1, -50, 255, 5, 5, 60, 40, 3)
                AnimatedSprite(load_image("walk-1.png"), 4, 1, -50, 255, 3, 10, 40, 40, 5)
                if 0 == waves[count_of_wave]:
                    count_of_wave += 1
                    time_now = time.time()
            if count_of_wave == len(waves) - 1 and len(mob_sprites) == 0:
                    return
            # mousebutton events
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos[0], event.pos[1]

                # put pause
                if pause_pic.rect.collidepoint(x, y) and not PAUSE:
                    PAUSE = True
                    pause_pic.image = pygame.transform.scale(load_image("start_btn.png"), (55, 55))

                # remove pause
                elif pause_pic.rect.collidepoint(x, y) and PAUSE:
                    PAUSE = False
                    pause_pic.image = pygame.transform.scale(load_image("pause.png"), (55, 55))

                if not PAUSE:

                    # if player clicked in buy tower
                    for sp in TOWER_BOUGHT:
                        if sp.rect.collidepoint(x, y) and money >= 100:
                            for s in TOWER_BUILDING_SPRITES:
                                if s.rect.x == sp.rect.x and s.rect.y == sp.rect.y + 15:
                                    s.kill()
                            TOWER_BOUGHT_RING = pygame.sprite.Group()
                            TOWER_BOUGHT = pygame.sprite.Group()
                            tower = pygame.sprite.Sprite()
                            tower.image = pygame.transform.scale(load_image("archer_tower.png"), (110, 110))
                            tower.rect = tower.image.get_rect()
                            tower.rect.x = sp.rect.x - 5
                            tower.rect.y = sp.rect.y - 30
                            TOWER_SPRITES.add(tower)
                            ArcherTower(load_image("archer_2.png"), 6, 1, sp.rect.x + 25, sp.rect.y - 35)
                            money -= 100
                        else:
                            TOWER_BOUGHT_RING = pygame.sprite.Group()
                            TOWER_BOUGHT = pygame.sprite.Group()

                    # if player clicked on teh place for tower
                    for sp in TOWER_BUILDING_SPRITES:
                        if sp.rect.collidepoint(x, y):
                            TOWER_BOUGHT_RING = pygame.sprite.Group()
                            TOWER_BOUGHT = pygame.sprite.Group()

                            buy_tower_ring = pygame.sprite.Sprite()
                            buy_tower_ring.image = pygame.transform.scale(load_image("tower-builder.png"), (100, 100))

                            buy_tower_ring.rect = buy_tower_ring.image.get_rect()
                            buy_tower_ring.rect.x = sp.rect.x
                            buy_tower_ring.rect.y = sp.rect.y - 15
                            TOWER_BOUGHT_RING.add(buy_tower_ring)

                            buy_tower = pygame.sprite.Sprite()
                            buy_tower.image = pygame.transform.scale(load_image("archer_tower_buy.png"), (40, 40))
                            buy_tower.rect = buy_tower.image.get_rect()
                            buy_tower.rect.x = sp.rect.x
                            buy_tower.rect.y = sp.rect.y - 15
                            TOWER_BOUGHT.add(buy_tower)

        # draw all groups
        all_sprites.draw(screen)
        information_menu_bar.draw(screen)
        mob_sprites.draw(screen)
        TOWER_BUILDING_SPRITES.draw(screen)
        TOWER_SPRITES.draw(screen)
        ARCHERS.draw(screen)
        TOWER_BOUGHT_RING.draw(screen)
        TOWER_BOUGHT.draw(screen)

        # updating enemies
        if not PAUSE:
            for m in mob_sprites:
                m.move()
                m.update()

        # updating archers
        for a in ARCHERS:
            if not PAUSE:
                a.update()
        if health == 0:
            return
        # information bar text
        font = pygame.font.SysFont('serif', 18)
        text = font.render(f"{health}", 1, (255, 55, 0))
        text_x = 110
        text_y = 25
        screen.blit(text, (text_x, text_y))
        text = font.render(f"{money}", 1, (255, 255, 0))
        text_y = 60
        screen.blit(text, (text_x, text_y))
        text = font.render(f"{count_of_wave + 1} / {len(waves)}", 1, (255, 255, 0))
        text_y = 95
        screen.blit(text, (text_x, text_y))
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()


if __name__ == "__main__":
    while resume:
        start_screen()
        if resume:
            main()
