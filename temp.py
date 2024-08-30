import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top-Down Ripple Effect")

# Colors
OCEAN_BLUE = (28, 107, 160)
LIGHT_BLUE = (173, 216, 230)
BACKGROUND_COLOR = (240, 248, 255)

# Ripple parameters
ripple_count = 5  # Number of ripple layers
ripple_speed = 0.03
ripple_amplitude = 20
ripple_frequency = 0.05

# Main loop
running = True
time = 0

while running:
    screen.fill(BACKGROUND_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update ripple time
    time += ripple_speed

    # Draw ripples
    for i in range(ripple_count):
        # Ripple parameters
        radius = (i + 1) * 80  # Distance between ripples
        color_intensity = 200 - i * 30  # Color fade effect
        ripple_color = (OCEAN_BLUE[0], OCEAN_BLUE[1], color_intensity)

        # Draw the ripple
        for angle in range(0, 360, 10):  # Draw smooth circular ripples
            x = WIDTH // 2 + int(radius * math.cos(math.radians(angle)))
            y = HEIGHT // 2 + int(radius * math.sin(math.radians(angle)))
            pygame.draw.circle(screen, ripple_color, (x, y), 2)  # Small circles for ripple effect

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
