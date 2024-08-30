# To fix
# # Even chance for spawn point should be weighted for width and height
# # Ships collide, check full paths when spawning

# Ideas
"""Rare Enemies:
    Multisyllable Words: Words with multiple syllables or complex pronunciations, like "circumvent" or "procrastinate."
    Foreign Words: Words borrowed from other languages that might be less familiar, like "schadenfreude" (German) or "savoir-faire" (French).
    Technical Terms: Specialized jargon from fields like science, medicine, or technology, such as "quasar" or "neuroplasticity."
    Palindromes: Words that read the same forwards and backwards, like "level" or "rotor."
    Homophones: Words that sound the same but have different meanings, like "knight" and "night."

Legendary Enemies:
    Uncommon Words: Extremely rare or archaic words, such as "flummox" or "quidnunc."
    Long Words: Very lengthy words that are challenging to type, like "antidisestablishmentarianism" or "hippopotomonstrosesquipedaliophobia."
    Anagrams: Words that are scrambled versions of other words, making players type out a specific word to solve the puzzle, like "listen" to get "silent."
    Acronyms: Complex acronyms that require knowledge or context, like "NATO" or "NASA."
    Mythical Words: Words from mythology or fantasy, such as "chimera" or "gorgon."""

import pygame
import pygame.gfxdraw
import sys
from random import *
from hPyT import *
import ctypes
import threading  # Import threading module
import time
import math
import tkinter as tk

from resources import *

class Game:
    def __init__(self):
        # Initialize Pygame and set up the display
        pygame.init()
        self.width = 1500
        self.height = 1000
        self.window = pygame.display.set_mode((self.width, self.height))
        self.ship_base_speed = 5

        self.bg_grid_offset_x = 0
        self.bg_grid_offset_y = 0
        self.scroll_speed_x = 0
        self.scroll_speed_y = 0


        self.ships = []

        self.bounce_sound = pygame.mixer.Sound("resources/saya_cute.ogg")
        self.hit_sound = pygame.mixer.Sound("resources/saya_kick_deeper.ogg")

        # Set window properties
        self.programIcon = pygame.image.load('icon.png')
        pygame.display.set_icon(self.programIcon)
        caption = " "
        pygame.display.set_caption(caption)

        # Custom window modifications
        hpyt_window = ctypes.windll.user32.GetActiveWindow()
        maximize_minimize_button.hide(hpyt_window)
        border_color.set(hpyt_window, (24, 24, 37))
        hwnd = ctypes.windll.user32.GetActiveWindow()
        title_bar_color.set(hwnd, '#181825')

        # Create initial set of ships
        #self.make_ships(7)

    def angle_to_velocities(self, angle):
        # Convert angle from degrees to radians
        radians = math.radians(angle)

        # Calculate the x and y components
        x = math.cos(radians) * 1
        y = math.sin(radians) * 1

        x = round(x, 3)
        y = round(y, 3)

        return [x, y]

    def random_oob_coord(self):
        if bool(getrandbits(1)):
            x = self.width * random()
            if bool(getrandbits(1)):
                y = 0
            else:
                y = self.height
        else:
            y = self.height * random()
            if bool(getrandbits(1)):
                x = 0
            else:
                x = self.width

        #x = round(x,1)
        #y = round(y,1)
        return [x,y]

    def angle_to_center(self, coord):
        # Calculate the center of the window
        center_x = self.width / 2
        center_y = self.height / 2
        
        # Calculate the difference between the point and the center
        delta_x = coord[0] - center_x
        delta_y = coord[1] - center_y
        
        # Calculate the angle using atan2, which handles the correct quadrant for the angle
        angle_radians = math.atan2(delta_y, delta_x)
        
        # Convert the angle to degrees for easier interpretation, if needed
        angle_degrees = math.degrees(angle_radians)
        
        return angle_degrees - 180

    def make_ships(self, amount, type):
            for i in range(amount):
                x, y = self.random_oob_coord()

                angle = self.angle_to_center([x, y])
                velocities = self.angle_to_velocities(angle)

                for ship in self.ships:
                    while ship.occupying(x, y):
                        x, y = self.random_oob_coord()

                        angle = self.angle_to_center([x, y])
                        velocities = self.angle_to_velocities(angle)

                ship = Ship(x=x, y=y, velocities=velocities, game=self)
                self.ships.append(ship)

    def draw_background(self):
        pass

    def main_game_loop(self):
        clock = pygame.time.Clock()
        spawn_director = SpawnDirector(self)

        while True:
            self.dt = clock.tick() / 1000.0  # Delta time in seconds
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.ACTIVEEVENT:
                    if event.gain == 0:  # Window loses focus
                        pass  # Handle focus loss (pause, mute, etc.)

            for ship in self.ships:
                for other_ship in self.ships:
                    if ship != other_ship:
                        pass
                ship.move(self.dt)
            
            spawn_director.update(self.dt)

            #self.bg_grid_offset_x = (self.bg_grid_offset_x + self.scroll_speed_x * self.dt * 60) % 107
            #self.bg_grid_offset_y = (self.bg_grid_offset_y + self.scroll_speed_y * self.dt * 60) % 107

            self.window.fill((30, 30, 46))

            for ship in self.ships:
                ship.draw(self.window)
            
            pygame.display.flip()
                       
    def gameover(self, ship):
        self.ships.remove(ship) 

class Ship:
    def __init__(self, x, y, velocities, game, radius = 20):
        self.x = x
        self.y = y
        self.radius = radius 
        self.x_speed = velocities[0] * 300  # Adjust speed factor as needed
        self.y_speed = velocities[1] * 300  # Adjust speed factor as needed
        self.colour = (243, 139, 168)
        self.game = game
        self.height = self.game.height
        self.width = self.game.width

    def move(self, dt):
        self.x += self.x_speed * dt
        self.y += self.y_speed * dt
        
        self.check_if_hit_player()


    def check_collision(self, other):
        pass

    def check_if_hit_player(self):
        kill_distance = 20

        center = [self.game.width/2, self.game.height/2]

        if self.x < center[0] + kill_distance and self.x > center[0] - kill_distance:
            self.game.gameover(self)
        elif self.y < center[1] + kill_distance and self.y > center[1] - kill_distance:
            self.game.gameover(self)

    def occupying(self, x, y):
        saferad = self.radius + self.radius * 1.5
        if self.x - saferad < x < self.x + saferad and self.y - saferad < y < self.y + saferad:
            return True
        else:
            return False

    def draw(self, surface):
        pygame.gfxdraw.filled_ellipse(surface, int(self.x), int(self.y), self.radius, self.radius, self.colour)

class Player:
    def __init__(self, typing):
        typing = ""

class SpawnDirector:
    def __init__(self, game):
        self.game = game  # Reference to the game object
        self.time_since_last_spawn = 0.0
        self.base_spawn_rate = 12.0  # Initial spawn rate: enemies per second
        self.spawn_rate_increase = 0.1  # Rate increase per second
        self.max_spawn_rate = 12.5  # Cap the spawn rate

        # Probabilities for different enemy types (base probabilities)
        self.common_chance = 0.9
        self.rare_chance = 0.09
        self.legendary_chance = 0.01

        # Rate at which the rare and legendary spawn chances increase
        self.rare_chance_increase = 0.002  # Increase per second
        self.legendary_chance_increase = 0.001  # Increase per second

        # Maximum limits for rare and legendary chances
        self.max_rare_chance = 0.3
        self.max_legendary_chance = 0.1


    def update(self, delta_time):
        # Increase the spawn rate over time
        self.base_spawn_rate = min(self.max_spawn_rate, self.base_spawn_rate + self.spawn_rate_increase * delta_time)

        # Increase rare and legendary spawn chances over time
        self.rare_chance = min(self.max_rare_chance, self.rare_chance + self.rare_chance_increase * delta_time)
        self.legendary_chance = min(self.max_legendary_chance, self.legendary_chance + self.legendary_chance_increase * delta_time)

        # Adjust common chance to maintain total probability of 1
        self.common_chance = 1.0 - self.rare_chance - self.legendary_chance

        # Calculate time between spawns based on the current spawn rate
        spawn_interval = 1.0 / self.base_spawn_rate

        # Update the time since the last spawn
        self.time_since_last_spawn += delta_time

        # Check if it's time to spawn a new enemy
        if self.time_since_last_spawn >= spawn_interval:
            self.spawn_enemy()
            # Reset the spawn timer
            self.time_since_last_spawn -= spawn_interval

    def spawn_enemy(self):
        # Determine the type of enemy to spawn based on probabilities
        random_value = random()
        if random_value <= self.legendary_chance:
            self.game.make_ships(1, type="legendary")
            print(f"Spawned 1 legendary enemy! Current spawn rate: {self.base_spawn_rate:.2f} enemies per second.")
        elif random_value <= self.rare_chance + self.legendary_chance:
            self.game.make_ships(1, type="rare")
            print(f"Spawned 1 rare enemy! Current spawn rate: {self.base_spawn_rate:.2f} enemies per second.")
        else:
            self.game.make_ships(1, type="common")
            print(f"Spawned 1 common enemy. Current spawn rate: {self.base_spawn_rate:.2f} enemies per second.")

if __name__ == "__main__":
    game = Game()

    game.main_game_loop()