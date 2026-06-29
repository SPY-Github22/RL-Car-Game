import pygame as pg

pg.init()

race_track = pg.display.set_mode((800, 600))
pg.display.set_caption("Window")
clock = pg.time.Clock()

a, b = 400, 300 #position
x, y = 0, 0 #x = movement, y = turning
turn_speed = 1
speed = 10

race_track.fill((0,0,0))

clock.tick(60)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        x -= speed
    if keys[pg.K_RIGHT]:
        x += speed
    if keys[pg.K_DOWN]:
        y -= turn_speed
    if keys[pg.K_UP]:
        y -= turn_speed
    pg.draw.rect(race_track, (255,0,0), (a, b, 20, 20))




