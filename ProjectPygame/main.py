import os
import math

import pygame

# from mob_1 import first_mob

path = [[-50, 455], [154, 455], [200, 495], [710, 507], [767, 424], [710, 298], [450, 298], [390, 205],
        [450, 110], [1250, 110]]
towers_first_lvl = [[]]
pygame.init()
all_sprites = pygame.sprite.Group()
mob_sprites = pygame.sprite.Group()
TOWER_SPRITES = pygame.sprite.Group()
TOWER_BUILDING_SPRITES = pygame.sprite.Group()
TOWER_BOUGHT = pygame.sprite.Group()
TOWER_BOUGHT_RING = pygame.sprite.Group()
ARCHERS = pygame.sprite.Group()
BUILDING_PLACE_COORDS = [[400, 385], [580, 380], [495, 595], [850, 380], [497, 160], [685, 157], [870, 155]]


def load_image(name):
    fullname = os.path.join('img', name)
    image = pygame.image.load(fullname)
    return image


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(mob_sprites)
        self.frames = []
        self.frames_kill = []
        self.count = 0
        self.cut_sheet(sheet, columns, rows)
        self.cut_sheet(load_image("kill_enemy.png"), 3, 1)
        for i in range(len(self.frames)):
            self.frames[i] = pygame.transform.scale(self.frames[i], (40, 40))
        for i in range(len(self.frames_kill)):
            self.frames_kill[i] = pygame.transform.scale(self.frames_kill[i], (60, 40))
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.x = path[0][0]
        self.y = path[0][1]
        self.kill_enemy = 0
        self.speed_increase = 10
        self.rect = self.rect.move(x, y)
        self.flipped = False
        self.health = 10
        self.cur_frame_kill = 0
        self.move_enemy = True


    def cut_sheet(self, sheet, columns, rows):
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
        print(len(self.frames_kill))
        if self.kill_enemy == 3:
            self.kill()
        if self.health <= 0:
            self.kill_enemy += 1
            self.cur_frame_kill = (self.cur_frame_kill + 1) % len(self.frames_kill)
            self.image = self.frames_kill[self.cur_frame_kill]
            self.move_enemy = False
        else:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        if self.x >= 1270:
            self.kill()

    def move(self):
        if self.move_enemy:
            x1, y1 = path[self.count]
            if self.count + 1 >= len(path):
                x2, y2 = (1250, 278)
            else:
                x2, y2 = path[self.count + 1]

            dirn = ((x2 - x1) * 2, (y2 - y1) * 2)

            length = math.sqrt((dirn[0]) ** 2 + (dirn[1]) ** 2)
            dirn = (dirn[0] / length * self.speed_increase, dirn[1] / length * self.speed_increase)
            if (dirn[0] < 0 and not (self.flipped)):
                self.flipped = True
                for x, img in enumerate(self.frames):
                    self.frames[x] = pygame.transform.flip(img, True, False)
            elif dirn[0] > 0 and self.flipped:
                self.flipped = False
                for x, img in enumerate(self.frames):
                    self.frames[x] = pygame.transform.flip(img, True, False)

            move_x, move_y = ((self.x + dirn[0]), (self.y + dirn[1]))
            self.x = move_x
            self.y = move_y
            # Go to next point
            if dirn[0] >= 0:  # moving right
                if dirn[1] >= 0:  # moving down
                    if self.x >= x2 and self.y >= y2:
                        self.count += 1
                else:
                    if self.x >= x2 and self.y <= y2:
                        self.count += 1
            else:  # moving left
                if dirn[1] > 0:  # moving down
                    if self.x <= x2 and self.y >= y2:
                        self.count += 1
                else:
                    if self.x <= x2 and self.y <= y2:
                        self.count += 1
            self.rect.x = self.x
            self.rect.y = self.y


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
        self.radius = 170
        # self.image = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA, 32)
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 10)
        # self.rect = pygame.Rect(x - self.radius + 25, y - self.radius / 2 - 15, 2 * self.radius, 2 * self.radius)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
    def attack(self):
        for i in mob_sprites:
            if math.sqrt((self.x - i.rect.x) ** 2 + (self.y - i.rect.y) ** 2 ) < self.radius:
                i.health -= 1
                self.flipped_x = self.x - i.rect.x
                return True
        return False
    def update(self):
        if self.attack():
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        if self.flipped_x < 0 and self.flipped:
            self.flipped = False
            for x, img in enumerate(self.frames):
                self.frames[x] = pygame.transform.flip(img, True, False)
        elif self.flipped_x > 0 and not self.flipped:
            self.flipped = True
            for x, img in enumerate(self.frames):
                self.frames[x] = pygame.transform.flip(img, True, False)
    def get(self):
        return (self.x, self.y)


class BuildingPlaces(pygame.sprite.Sprite):
    image = load_image("b_p.png")

    def __init__(self, x, y):
        super().__init__(TOWER_BUILDING_SPRITES)
        self.image = BuildingPlaces.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.building_place_num = BUILDING_PLACE_COORDS.index([x, y])
def cause_enemy():
    AnimatedSprite(load_image("walk-1.png"), 4, 1, -50, 255)


for i in range(len(BUILDING_PLACE_COORDS)):
    x = BUILDING_PLACE_COORDS[i][0]
    y = BUILDING_PLACE_COORDS[i][1]
    BuildingPlaces(x, y)

clock = pygame.time.Clock()
size = width, height = 1200, 705
screen = pygame.display.set_mode(size)
sprite = pygame.sprite.Sprite()
sprite.image = load_image("map-main.png")
sprite.image = pygame.transform.scale(sprite.image, (1200, 705))
sprite.rect = sprite.image.get_rect()
all_sprites.add(sprite)
screen.fill(pygame.Color('blue'))
AnimatedSprite(load_image("walk-1.png"), 4, 1, -50, 255)

fps = 10
running = True
tower_building = False
count = 0
c = 0
SPAWNENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNENEMY, 1000)
while running:
    for event in pygame.event.get():
        if event.type == SPAWNENEMY:
            AnimatedSprite(load_image("walk-1.png"), 4, 1, -50, 255)
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            print(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos[0], event.pos[1]
            for sp in TOWER_BOUGHT:
                if sp.rect.collidepoint(x, y):
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
                else:
                    TOWER_BOUGHT_RING = pygame.sprite.Group()
                    TOWER_BOUGHT = pygame.sprite.Group()

            for sp in TOWER_BUILDING_SPRITES:
                if sp.rect.collidepoint(x, y):
                    tower_building = sp.building_place_num
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

    all_sprites.draw(screen)
    mob_sprites.draw(screen)
    TOWER_BUILDING_SPRITES.draw(screen)
    TOWER_BOUGHT_RING.draw(screen)
    TOWER_BOUGHT.draw(screen)
    TOWER_SPRITES.draw(screen)
    ARCHERS.draw(screen)
    for m in mob_sprites:
        m.move()
        m.update()
    for a in ARCHERS:
        a.update()
        pygame.draw.circle(screen, (255, 0, 0, 50), a.get(), 170, 1)

    # for i in range(1, len(path)):
    #     pygame.draw.line(screen, (255, 0, 0), (path[i - 1]), (path[i]), 1)
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
