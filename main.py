import pygame
import sys
import os
from car import Car
from process_track import process_track

# Configuration
WIDTH, HEIGHT = 1000, 800  # Will be overridden by track image size
FPS = 60

# Starting position (adjust these based on your track's start line)
START_X = 400
START_Y = 400
START_ANGLE = 90  # Pointing to the right

def main():
    global START_X, START_Y
    pygame.init()
    
    # Setup track files
    track_path = "track.png"
    mask_path = "track_mask.png"
    
    if not os.path.exists(track_path):
        print(f"Error: {track_path} not found!")
        print("Please save your track image as 'track.png' in this directory and run again.")
        sys.exit(1)
        
    if not os.path.exists(mask_path):
        print(f"{mask_path} not found. Generating it now from {track_path}...")
        if not process_track(track_path, mask_path):
            sys.exit(1)
            
    # Load track images
    track_image = pygame.image.load(track_path)
    mask_image = pygame.image.load(mask_path)
    
    # Scale window to image size
    img_width, img_height = track_image.get_size()
    screen = pygame.display.set_mode((img_width, img_height))
    pygame.display.set_caption("2D RL Car Game Environment")
    
    # Create the Pygame mask from the processed mask image
    # In the mask image, we want the dilated walls (white) to be the collision area.
    # pygame.mask.from_surface uses the alpha channel or colorkey.
    # We will convert white (255,255,255) to a collision mask.
    mask_surface = pygame.Surface((img_width, img_height))
    mask_surface.blit(mask_image, (0, 0))
    mask_surface.set_colorkey((0, 0, 0)) # Make black transparent, so white is solid
    track_mask = pygame.mask.from_surface(mask_surface)
    
    # Initialize car (smaller size as requested)
    car = Car(START_X, START_Y, width=10, height=20)
    car.angle = START_ANGLE
    
    clock = pygame.time.Clock()
    
    running = True
    while running:
        clock.tick(FPS)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Reset on spacebar
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                car.reset(START_X, START_Y, START_ANGLE)
            # Allow clicking to set a new spawn point
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                START_X, START_Y = event.pos
                car.reset(START_X, START_Y, START_ANGLE)
                
        # Input handling
        keys = pygame.key.get_pressed()
        forward = keys[pygame.K_UP] or keys[pygame.K_w]
        backward = keys[pygame.K_DOWN] or keys[pygame.K_s]
        left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        
        # Update
        if not car.crashed:
            car.move(forward, backward, left, right)
            car.update()
            
            # Check collision
            car.check_collision(track_mask)
            
        # Draw
        screen.blit(track_image, (0, 0))
        car.draw(screen)
        
        # Raycasting for RL visualization
        car.cast_rays(screen, track_mask, draw=True)
        
        # Info overlay
        font = pygame.font.SysFont("Arial", 20)
        speed_text = font.render(f"Speed: {abs(car.speed):.1f}", True, (0, 0, 0))
        status_text = font.render("CRASHED - Press Space to reset" if car.crashed else "", True, (255, 0, 0))
        screen.blit(speed_text, (10, 10))
        screen.blit(status_text, (10, 40))
        
        pygame.display.flip()
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
