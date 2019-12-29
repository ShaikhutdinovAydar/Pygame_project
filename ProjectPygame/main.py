import os
import math

import time
import pygame

# from mob_1 import first_mob

path = [[-50, 455], [154, 455], [200, 495], [710, 507], [767, 424], [710, 298], [450, 298], [390, 205], [450, 110],
         [1250, 110]]
# path = [[-50, 455], [157, 455], [228, 512], [268, 512], [343, 480], [390, 512], [689, 515], [744, 481], [767, 423], [741, 356], [696, 340], [494, 340], [437, 247], [413, 210], [430, 153], [456, 117], [475, 98], [1250, 78]]
pygame.init()
all_sprites = pygame.sprite.Group()
mob_sprites = pygame.sprite.Group()


def load_image(name):
    fullname = os.path.join('img', name)
    image = pygame.image.load(fullname).convert_alpha()
    return image


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(mob_sprites)
        self.frames = []
        self.count = 0
        self.cut_sheet(sheet, columns, rows)
        for i in range(len(self.frames)):
            self.frames[i] = pygame.transform.scale(self.frames[i], (40, 40))
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.x = path[0][0]
        self.y = path[0][1]
        self.speed_increase = 10
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                # r = sheet.subsurface(pygame.Rect(frame_location, self.rect.size))
                # r = pygame.transform.scale(self.image, (150, 200))
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def move(self):

        x1, y1 = path[self.count]
        if self.count + 1 >= len(path):
            x2, y2 = (1250, 278)
        else:
            x2, y2 = path[self.count + 1]

        dirn = ((x2 - x1) * 2, (y2 - y1) * 2)

        length = math.sqrt((dirn[0]) ** 2 + (dirn[1]) ** 2)
        dirn = (dirn[0] / length * self.speed_increase, dirn[1] / length * self.speed_increase)
        # if dirn[0] < 0 and not(self.flipped):
        #     self.flipped = True
        #     for x, img in enumerate(self.imgs):
        #         self.imgs[x] = pygame.transform.flip(img, True, False)

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
        print(self.count)


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
drawing = True
count = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            print(event.pos)
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    mob_sprites.draw(screen)
    # count += 1
    # if count == 2:
    #     first_mob.update()
    #     count = 0
    for m in mob_sprites:
        m.move()
        m.update()
    count += 1
    if count == 20:
        count = 0
    for i in range(1, len(path)):
        pygame.draw.line(screen, (255, 0, 0), (path[i - 1]), (path[i]), 1)

    # first_mob.move()
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
