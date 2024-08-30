# To fix
# # Even chance for spawn point should be weighted for width and height
# # Ships collide, check full paths when spawning
# # Typing word under most complete ship word
# # Dead ship sprite
# # Drift and spin out
# # Score
    # Game over screen
# # Sound on wrong character
# # Stop user typing on incorrect
# # No space at start of words
# # Visuals
    # Cannon shots
    # waves
    # stuff in water/air
    # boat trails/ripple fx
# # Birds in sky to get points
# # Barrels in water for points or heals?

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

from words import *
from floors import *

class Game:
    def __init__(self):
        # Initialize Pygame and set up the display
        pygame.init()
        self.width = 1500
        self.height = 1000
        self.window = pygame.display.set_mode((self.width, self.height))
        self.ship_base_speed = 0.22

        self.bg_grid_offset_x = 0
        self.bg_grid_offset_y = 0
        self.scroll_speed_x = 0
        self.scroll_speed_y = 0

        self.player_alive = True
        self.score = 0

        self.ships = []
        self.destroyed_ships = dict({})

        self.bounce_sound = pygame.mixer.Sound("resources/saya_cute.ogg")
        self.hit_sound = pygame.mixer.Sound("resources/saya_kick_deeper.ogg")
        self.got_hit_sound = pygame.mixer.Sound("resources/tok10.ogg")

        # Set window properties
        self.programIcon = pygame.image.load('icon.png')
        pygame.display.set_icon(self.programIcon)
        caption = "Lost at C"
        pygame.display.set_caption(caption)

        # Custom window modifications
        hpyt_window = ctypes.windll.user32.GetActiveWindow()
        maximize_minimize_button.hide(hpyt_window)
        border_color.set(hpyt_window, (24, 24, 37))
        hwnd = ctypes.windll.user32.GetActiveWindow()
        title_bar_color.set(hwnd, '#181825')


        self.bg_grid = pygame.image.load("resources\\pir\\PNG\\Default size\\Tiles\\tile_73.png").convert_alpha()
        self.bg_x = 0
        self.bg_y = 0

        # Create initial set of ships
        #self.make_ships(7)

    def add_score(self, amount):
        self.score += amount
        print ("score:",self.score)

    def angle_to_velocities(self, angle):
        # Convert angle from degrees to radians
        radians = math.radians(angle)

        # Calculate the x and y components
        x = math.cos(radians) * 1
        y = math.sin(radians) * 1

        x = round(x, 3)
        y = round(y, 3)

        x = x*self.ship_base_speed
        y = y*self.ship_base_speed

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
                        temp_x, temp_y = self.random_oob_coord()
                        angle = self.angle_to_center([temp_x, temp_y])
                        velocities = self.angle_to_velocities(angle)
                        x, y = temp_x, temp_y

                if type == "common":
                    ship = Ship(x=x, y=y, velocities=velocities, angle=angle, game=self)
                if type == "rare":
                    ship = Rare(x=x, y=y, velocities=velocities, angle=angle, game=self)
                if type == "legendary":
                    ship = Legendary(x=x, y=y, velocities=velocities, angle=angle, game=self)
                self.ships.append(ship)

    def _draw_background(self):        
        
        # Determine the number of rows and columns needed
        cols = (self.width // 124) + 1
        rows = (self.height // 124) + 1

        # Draw the grid
        for row in range(rows):
            for col in range(cols):
                x = col * 124
                y = row * 124
                self.grid_sprite = self.sprite = pygame.image.load(choice(floors)).convert_alpha()
                self.window.blit(self.grid_sprite, (x, y))


    def draw_bg(self, dt):
        # Define the speed and frequency of the sinusoidal movement
        speed = 16  # Pixels per second for movement
        frequency = 0.5  # Frequency of the sinusoidal movement

        # Calculate the amount of offset in both x and y directions
        self.bg_x += speed * dt * abs(math.cos(frequency * pygame.time.get_ticks() / 1000.0))
        self.bg_y += speed * dt * abs(math.sin(frequency * pygame.time.get_ticks() / 1000.0))


        # Calculate the number of tiles needed to cover the screen
        cols = (self.width // 64) + 2  # Adding extra tile to cover the entire screen
        rows = (self.height // 64) + 2  # Adding extra tile to cover the entire screen

        # Draw the background
        for row in range(rows):
            for col in range(cols):
                # Calculate the position of the tile with scrolling effect
                x = (col * 64) - int(self.bg_x) % 64
                y = (row * 64) - int(self.bg_y) % 64

                # Wrap around the background
                if x < -64:
                    x += cols * 64
                elif x >= self.width:
                    x += cols * 64

                if y < -64:
                    y += rows * 64
                elif y >= self.height:
                    y += rows * 64

                self.window.blit(self.bg_grid, (x, y))
                
        # Reset bg_x and bg_y to prevent them from going too far
        #if self.bg_x < -64:
        #    self.bg_x += 64
        #if self.bg_y < -64:
        #    self.bg_y += 64


    def check_destroy_ship(self, word):
        for ship in self.ships:
            if ship.word.lower() == word:
                ship.destroyed()
                self.add_score(ship.kill_score())
                self.player.word = ""



    def main_game_loop(self):
        clock = pygame.time.Clock()
        spawn_director = SpawnDirector(self)
        self.player = Player(self)

        """angle = 90
        ship = Ship(x=150, y=150, velocities=self.angle_to_velocities(angle), angle=angle, game=self)
        self.ships.append(ship)"""


        while True:
            self.dt = clock.tick() / 1000.0  # Delta time in seconds
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.ACTIVEEVENT:
                    if event.gain == 0:  # Window loses focus
                        pass  # Handle focus loss (pause, mute, etc.)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if pygame.key.get_mods() & pygame.KMOD_CTRL:
                            # Ctrl + Backspace: Clear the entire typed word
                            self.player.word = ""
                        else:
                            # Regular Backspace: Remove the last character from the typed word
                            self.player.word = self.player.word[:-1]
                    elif event.key == pygame.K_RETURN:
                        # Check if the typed word matches any ship's word
                        self.check_destroy_ship(self.player.word)
                        # Reset the typed word
                        self.player.word = ""
                    elif event.key == pygame.K_SPACE:
                        # Add a space to the typed word
                        self.player.word += " "
                    elif pygame.K_a <= event.key <= pygame.K_z:
                        # Add the pressed letter to the typed word
                        self.player.word += pygame.key.name(event.key)
                        self.check_destroy_ship(self.player.word)

            for ship in self.ships:
                for other_ship in self.ships:
                    if ship != other_ship:
                        pass
                ship.move(self.dt)
            
            spawn_director.update(self.dt)

            #self.bg_grid_offset_x = (self.bg_grid_offset_x + self.scroll_speed_x * self.dt * 60) % 107
            #self.bg_grid_offset_y = (self.bg_grid_offset_y + self.scroll_speed_y * self.dt * 60) % 107

            #self.window.fill("#ABE3F5")
            self.draw_bg(self.dt)

            for ship in self.ships:
                ship.draw(self.window)

            self.player.draw(self.window)
            
            pygame.display.flip()
                       
    def gameover(self, ship):
        self.alive = False

class Ship:
    def __init__(self, x, y, velocities, angle, game, radius = 20):
        self.x = x
        self.y = y
        self.radius = radius 
        self.x_speed = velocities[0] * 300  # Adjust speed factor as needed
        self.y_speed = velocities[1] * 300  # Adjust speed factor as needed
        self.colour = (243, 139, 168)
        self.angle = -angle
        self.game = game
        self.height = self.game.height
        self.width = self.game.width

        self.score = 5

        self.sprite = pygame.image.load("resources\\pir\\PNG\\retina\\ships\\ship (4).png").convert_alpha()

        self.word = choice(easy_words).lower()
        #self.word = choice(letters)

    def move(self, dt):
        self.x += self.x_speed * dt
        self.y += self.y_speed * dt
        
        self.check_if_hit_player()

    def destroyed(self):
        self.game.ships.remove(self)
        self.game.destroyed_ships[self] = 5
        self.game.hit_sound.play()
        print (f"removed {self.word}")

    def check_collision(self, other):
        pass

    def check_if_hit_player(self):
        kill_distance = 100

        center = [self.game.width/2, self.game.height/2]

        if self.x < center[0] + kill_distance and self.x > center[0] - kill_distance and self.y > center[1] - kill_distance and self.y < center[1] + kill_distance:
            self.game.player.hit(self)
            print(F"Hit: {self.x} {self.y}")

    def occupying(self, x, y):
        saferad = self.radius + self.radius * 1.5
        if self.x - saferad < x < self.x + saferad and self.y - saferad < y < self.y + saferad:
            return True
        else:
            return False

    def same_before_index(self, string):
        for i in range(len(string)):
            if self.word[i] == string[i]:
                pass
            else:
                return i
        return len(string)

    def partial_correct(self, string):
        for i in range(len(string)):
            if self.word[i] == string[i]:
                pass
            else:
                return i
        return len(string)

    def __draw(self, surface):
        # Rotate the sprite by the given angle
        rotated_sprite = pygame.transform.rotate(self.sprite, self.angle)

        # Get the sprite's rect and set its center to (self.x, self.y)
        sprite_rect = self.sprite.get_rect(center=(self.x, self.y))
        
        # Blit the sprite on the surface
        surface.blit(rotated_sprite, sprite_rect)
        
        # Define the font and size
        font = pygame.font.Font(None, 36)  # None for default font, 36 is font size
        
        # Render the text in white
        text_surface = font.render(self.word, True, (255, 255, 255))
        
        # Create a black outline by rendering the text multiple times slightly offset
        outline_surface = font.render(self.word, True, (0, 0, 0))
        
        # Draw the outline around the text
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            outline_rect = outline_surface.get_rect(center=(self.x + dx, self.y + dy))
            surface.blit(outline_surface, outline_rect)
        
        # Draw the drop shadow (slightly offset black text)
        shadow_surface = font.render(self.word, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect(center=(self.x + 2, self.y + 2))
        surface.blit(shadow_surface, shadow_rect)
        
        # Blit the white text on top of the outline and shadow
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        surface.blit(text_surface, text_rect)

    def draw(self, surface):
        # Rotate the sprite by the given angle
        rotated_sprite = pygame.transform.rotate(self.sprite, self.angle)

        # Get the sprite's rect and set its center to (self.x, self.y)
        sprite_rect = self.sprite.get_rect(center=(self.x, self.y))
        
        # Blit the sprite on the surface
        surface.blit(rotated_sprite, sprite_rect)
        
        # Define the font and size
        font = pygame.font.Font(None, 36)  # None for default font, 36 is font size

        # Define the text and split it into two parts
        full_text = self.word

        # Render the text in red for the left half
        alt_color = (255, 22, 22)
        white_color = (255, 255, 255)
        
        split_index = self.same_before_index(self.game.player.word)

        if self.word.startswith(self.game.player.word):
            alt_color = (22, 255, 22)


        # Split the text into left and right halves
        left_half = full_text[:split_index]
        right_half = full_text[split_index:]
        
        # Render the left half in red
        left_surface = font.render(left_half, True, alt_color)
        
        # Render the right half in white
        right_surface = font.render(right_half, True, white_color)
        
        # Calculate positions
        left_rect = left_surface.get_rect(midright=(self.x, self.y))
        right_rect = right_surface.get_rect(midleft=(self.x, self.y))
        
        # Draw the outline and shadow for both text parts
        # Outline
        outline_surface_red = font.render(left_half, True, (0, 0, 0))
        outline_surface_white = font.render(right_half, True, (0, 0, 0))
        
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            surface.blit(outline_surface_red, left_rect.move(dx, dy))
            surface.blit(outline_surface_white, right_rect.move(dx, dy))
        
        # Shadow
        shadow_surface_red = font.render(left_half, True, (0, 0, 0))
        shadow_surface_white = font.render(right_half, True, (0, 0, 0))
        surface.blit(shadow_surface_red, left_rect.move(2, 2))
        surface.blit(shadow_surface_white, right_rect.move(2, 2))
        
        # Blit the text parts on top of the shadow and outline
        surface.blit(left_surface, left_rect)
        surface.blit(right_surface, right_rect)

    def kill_score(self):
        return self.score

class Rare(Ship):
    def __init__(self, x, y, velocities, angle, game):
        super().__init__(x, y, velocities, angle, game, radius = 20)
        self.sprite = pygame.image.load("resources\\pir\\PNG\\retina\\ships\\ship (6).png").convert_alpha()
        self.word = choice(rare_words).lower()

        self.score = 10

class Legendary(Ship):
    def __init__(self, x, y, velocities, angle, game):
        super().__init__(x, y, velocities, angle, game, radius = 20)
        self.sprite = pygame.image.load("resources\\pir\\PNG\\retina\\ships\\ship (3).png").convert_alpha()
        self.word = choice(legendary_words).lower()

        self.score = 20

class Player:
    def __init__(self, game):
        self.word = ""
        #self.sprite = pygame.image.load("resources\\sp\\PNG\\Retina\\character_roundGreen.png").convert_alpha()
        self.sprite = pygame.image.load("resources\\pir\\PNG\\retina\\Ships\\ship (2).png").convert_alpha()

        self.angle = 0
        self.game = game
        self.x = self.game.width/2
        self.y = self.game.height/2


        self.health = 3

    def draw(self, surface):
        new_size = (113, 66)
        scaled_sprite = pygame.transform.scale(self.sprite, new_size)

        # Rotate the sprite by the given angle
        rotated_sprite = pygame.transform.rotate(scaled_sprite, self.angle)

        # Get the sprite's rect and set its center to (self.x, self.y)
        sprite_rect = self.sprite.get_rect(center=(self.x, self.y))
        
        # Blit the sprite on the surface
        surface.blit(rotated_sprite, sprite_rect)
        
        # Define the font and size
        font = pygame.font.Font(None, 69)  # None for default font, 36 is font size
        
        # Render the text in white
        text_surface = font.render(self.word, True, (255, 255, 255))
        
        # Create a black outline by rendering the text multiple times slightly offset
        outline_surface = font.render(self.word, True, (0, 0, 0))
        
        # Draw the outline around the text
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            outline_rect = outline_surface.get_rect(center=(self.x + dx, self.y + dy))
            surface.blit(outline_surface, outline_rect)
        
        # Draw the drop shadow (slightly offset black text)
        shadow_surface = font.render(self.word, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect(center=(self.x + 2, self.y + 2))
        surface.blit(shadow_surface, shadow_rect)
        
        # Blit the white text on top of the outline and shadow
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        surface.blit(text_surface, text_rect)

    def hit(self, ship):
        self.word = ""

        self.game.got_hit_sound.play()

        self.game.ships.remove(ship) 

        self.health += -1

        if self.health <= 0:
            self.sprite = pygame.image.load("resources\\pir\\PNG\\retina\\Ships\\ship (20).png").convert_alpha()
            self.game.gameover(ship)
        elif self.health == 1:
            self.sprite = pygame.image.load("resources\\pir\\PNG\\retina\\Ships\\ship (14).png").convert_alpha()
        elif self.health == 2:
            self.sprite = pygame.image.load("resources\\pir\\PNG\\retina\\Ships\\ship (8).png").convert_alpha()


class SpawnDirector:
    def __init__(self, game):
        self.game = game  # Reference to the game object
        self.time_since_last_spawn = 0.0
        self.base_spawn_rate = 0.5  # Initial spawn rate: enemies per second
        self.spawn_rate_increase = 0.05  # Rate increase per second
        self.max_spawn_rate = 0.82  # Cap the spawn rate

        # Probabilities for different enemy types (base probabilities)
        self.common_chance = 0.85
        self.rare_chance = 0.1
        self.legendary_chance = 0.05

        # Rate at which the rare and legendary spawn chances increase
        self.rare_chance_increase = 0.002  # Increase per second
        self.legendary_chance_increase = 0.001  # Increase per second

        # Maximum limits for rare and legendary chances
        self.max_rare_chance = 0.5
        self.max_legendary_chance = 0.2


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
            print(f"Spawned 1 legendary enemy! Current spawn rate: {self.base_spawn_rate:.2f} enemies per second.")
            self.game.make_ships(1, type="legendary")
        elif random_value <= self.rare_chance + self.legendary_chance:
            print(f"Spawned 1 rare enemy! Current spawn rate: {self.base_spawn_rate:.2f} enemies per second.")
            self.game.make_ships(1, type="rare")
        else:
            print(f"Spawned 1 common enemy. Current spawn rate: {self.base_spawn_rate:.2f} enemies per second.")
            self.game.make_ships(1, type="common")

if __name__ == "__main__":
    game = Game()

    game.main_game_loop()