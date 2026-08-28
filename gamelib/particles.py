"""
Simple particle system
"""

import pygame
import random

class ParticleManager:
    """
    Manage particles like spawning them updating and drawing them
    """
    
    def __init__(self):
        self.particles: list[Particle] = []

    def spawn(
                self,
                pos: pygame.Vector2,
                spawn_range: pygame.Vector2= pygame.Vector2(0, 0),
                slowdown: float=0.9,
                start_speed: float=5,
                color: tuple[int, int, int, int] | tuple[int, int, int]=(255, 255, 255, 255),
                size: float=5,
                lifetime: float = 60,
                amount: int = 5,
                direction: pygame.Vector2 | None = None,
                spread: float = 0,
                # spread_type = 'default'
            ):
        """
        Create particles on screen\n
        Exclude alpha value on color for particles with no alpha\n
        Setting direction makes the particles go that direction instead of random\n
        Particles should have delta time\n
        Particles are limited to one color only
        """
        
        lifetime /= 60
        particle_speed = start_speed
        for _ in range(amount):
            if direction is None:
                vel = pygame.Vector2(
                random.uniform(-1, 1),
                random.uniform(-1, 1)
            )
            else:
                angle = random.gauss(sigma=spread/2.5)
                particle_speed = start_speed * random.uniform(0.7, 1.3)
                vel = direction.rotate(angle)

            if vel.length_squared() == 0:
                continue
            
            vel = vel.normalize() * particle_speed
            
            if spawn_range.length_squared() != 0:
                new_pos = pygame.Vector2(pos.x + random.uniform(0, spawn_range.x), pos.y + random.uniform(0, spawn_range.y))
            else:
                new_pos = pos.copy()
                
            self.particles.append(Particle(new_pos, slowdown, vel, list(color), size, lifetime))

    def update(self, dt):
        for particle in self.particles:
            particle.update(dt)
        self.particles = [particle for particle in self.particles if particle.lifetime > 0]
            
    def draw(self, screen, x_offset=0, y_offset=0):
        for particle in self.particles:
            particle.draw(screen, x_offset, y_offset)
    
class Particle:
    def __init__(self, pos: pygame.Vector2, slowdown: float, vel: pygame.Vector2, color: list[int], size: float, lifetime:float):
        self.vel = vel.copy() * 60
        self.color = color.copy()
        self.pos = pos.copy()
        self.slowdown = slowdown
        self.size = size
        self.lifetime = lifetime
        self.max_lifetime = lifetime
    
        if len(self.color) == 3:
            self.color.append(255)
        
    def update(self, dt):
        self.pos += self.vel * dt
        self.vel *= self.slowdown ** (dt * 60)
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        self.color[3] = max(0, min(255, alpha))
        self.lifetime -= dt
        
    def draw(self, screen, x_offset, y_offset):
        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        surf.fill(self.color)

        screen.blit(
            surf,
            (
                self.pos.x - x_offset - self.size / 2,
                self.pos.y - y_offset - self.size / 2
            )
        )