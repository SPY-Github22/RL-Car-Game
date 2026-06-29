import pygame
import math
import numpy as np

class Car:
    def __init__(self, x, y, width=20, height=40):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # Physics
        self.angle = 0 # In degrees
        self.speed = 0
        self.max_speed = 5
        self.acceleration = 0.2
        self.friction = 0.05
        self.rotation_speed = 3
        
        # State
        self.crashed = False
        self.color = (200, 50, 50)
        
        # Create the car surface (a simple rectangle for now)
        self.original_image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.original_image.fill(self.color)
        
        # Add a visual indicator for the front of the car
        pygame.draw.rect(self.original_image, (255, 255, 255), (0, 0, self.width, 10))
        
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
        # For collision
        self.mask = pygame.mask.from_surface(self.image)
        
        # Raycasting config
        self.ray_angles = [-90, -45, 0, 45, 90] # relative to car angle
        self.ray_length = 150
        self.distances = [self.ray_length] * len(self.ray_angles)
        self.ray_end_points = []
        
    def move(self, forward, backward, left, right):
        if self.crashed:
            return

        if forward:
            self.speed += self.acceleration
        elif backward:
            self.speed -= self.acceleration
            
        if self.speed > 0:
            self.speed -= self.friction
        elif self.speed < 0:
            self.speed += self.friction
            
        # Stop completely if speed is very low
        if abs(self.speed) < self.friction:
            self.speed = 0
            
        self.speed = max(-self.max_speed/2, min(self.speed, self.max_speed))
        
        # Only allow turning if moving
        if self.speed != 0:
            turn_direction = 1 if self.speed > 0 else -1
            if left:
                self.angle += self.rotation_speed * turn_direction
            if right:
                self.angle -= self.rotation_speed * turn_direction
                
        # Calculate velocity
        radians = math.radians(self.angle)
        dx = math.sin(radians) * self.speed
        dy = math.cos(radians) * self.speed
        
        self.x += dx
        self.y += dy
        
    def update(self):
        # Rotate the image
        # Pygame rotation is counter-clockwise, so we pass positive angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)
        
    def check_collision(self, track_mask):
        offset = (int(self.rect.left), int(self.rect.top))
        # track_mask is a Pygame mask representing the walls
        if track_mask.overlap(self.mask, offset):
            self.crashed = True
            self.color = (50, 50, 50)
            self.original_image.fill(self.color)
            pygame.draw.rect(self.original_image, (100, 100, 100), (0, 0, self.width, 10))
            return True
        return False

    def cast_rays(self, screen, track_mask, draw=True):
        self.ray_end_points = []
        self.distances = []
        
        car_center = (self.x, self.y)
        
        for ray_angle in self.ray_angles:
            # Calculate absolute angle in radians
            angle_rad = math.radians(self.angle + ray_angle)
            
            # Start position
            start_x, start_y = car_center
            
            # Move along the ray until collision or max length
            length = 0
            hit = False
            
            while length < self.ray_length:
                target_x = int(start_x + math.sin(angle_rad) * length)
                target_y = int(start_y + math.cos(angle_rad) * length)
                
                # Check if point is outside screen or hits a wall
                if (target_x < 0 or target_x >= track_mask.get_size()[0] or 
                    target_y < 0 or target_y >= track_mask.get_size()[1]):
                    hit = True
                    break
                    
                # Pygame mask uses (x,y) coordinates
                if track_mask.get_at((target_x, target_y)):
                    hit = True
                    break
                    
                length += 1
                
            self.distances.append(length)
            end_point = (target_x, target_y)
            self.ray_end_points.append(end_point)
            
            if draw:
                color = (255, 0, 0) if hit else (0, 255, 0)
                pygame.draw.line(screen, color, car_center, end_point, 1)
                pygame.draw.circle(screen, color, end_point, 3)
                
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
    def reset(self, start_x, start_y, start_angle):
        self.x = start_x
        self.y = start_y
        self.angle = start_angle
        self.speed = 0
        self.crashed = False
        self.color = (200, 50, 50)
        self.original_image.fill(self.color)
        pygame.draw.rect(self.original_image, (255, 255, 255), (0, 0, self.width, 10))
