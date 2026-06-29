import pygame as pg
import math

pg.init()

# 1. Load Images
track_image = pg.image.load("track2.png")
mask_image = pg.image.load("track_mask.png")

# Set window size to match track image
width, height = track_image.get_size()
race_track = pg.display.set_mode((width, height))
pg.display.set_caption("RL Car Game - Phase 4")
clock = pg.time.Clock()

car_image = pg.Surface((20, 20), pg.SRCALPHA)
car_image.fill((255, 0, 0))
pg.draw.rect(car_image, (255, 255, 255), (0, 0, 20, 5)) 

a, b = 400, 300 #position
angle = 0
velocity = 0
crashed = False

# Raycasting setup
ray_angles = [-60, -30, 0, 30, 60]
ray_max_length = 200

running = True
while running:
    clock.tick(60)
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            crashed = False
            a, b = 400, 300
            angle = 0
            velocity = 0

    if not crashed:
        keys = pg.key.get_pressed()
        
        if keys[pg.K_LEFT]:
            angle += 4
        if keys[pg.K_RIGHT]:
            angle -= 4
            
        if keys[pg.K_UP]:
            velocity += 0.2
        elif keys[pg.K_DOWN]:
            velocity -= 0.2
        else:
            if velocity > 0:
                velocity -= 0.1
            elif velocity < 0:
                velocity += 0.1
            if abs(velocity) < 0.1:
                velocity = 0

        velocity = max(-3, min(velocity, 6))

        a -= math.sin(math.radians(angle)) * velocity
        b -= math.cos(math.radians(angle)) * velocity
    
    # 2. Draw Track (instead of black background)
    race_track.blit(track_image, (0, 0))
    
    # 3. Collision Detection
    if 0 <= int(a) < width and 0 <= int(b) < height:
        if mask_image.get_at((int(a), int(b)))[0] == 255:  # Hit a white pixel on mask
            crashed = True
            
    # 4. Raycasting (Laser Sensors)
    distances = []
    for offset_angle in ray_angles:
        ray_angle = angle + offset_angle
        length = 0
        hit = False
        target_x, target_y = int(a), int(b)
        
        while not hit and length < ray_max_length:
            target_x = int(a - math.sin(math.radians(ray_angle)) * length)
            target_y = int(b - math.cos(math.radians(ray_angle)) * length)
            
            if 0 <= target_x < width and 0 <= target_y < height:
                if mask_image.get_at((target_x, target_y))[0] == 255:
                    hit = True
            else:
                hit = True # Hit edge of screen
                
            if not hit:
                length += 5 # Raycast step size
                
        distances.append(length)
        color = (255, 0, 0) if hit and length < ray_max_length else (0, 255, 0)
        pg.draw.line(race_track, color, (a, b), (target_x, target_y), 2)
        pg.draw.circle(race_track, color, (target_x, target_y), 4)

    # Draw Car
    if crashed:
        rotated_car = pg.transform.rotate(car_image, angle)
        rect = rotated_car.get_rect(center=(a, b))
        pg.draw.rect(race_track, (0,0,0), rect) # Turn black if crashed
    else:
        rotated_car = pg.transform.rotate(car_image, angle)
        rect = rotated_car.get_rect(center=(a, b))
        race_track.blit(rotated_car, rect)

    pg.display.flip()

pg.quit()
