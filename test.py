import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Button with Dynamic Text")

# Define the button color and font
BUTTON_COLOR = (255, 0, 0)
FONT = pygame.font.Font(None, 36)

# Create the button surface
button_rect = pygame.Rect(100, 100, 200, 100)
button_surface = pygame.Surface((200, 100))
button_surface.fill(BUTTON_COLOR)

# Define the initial button text
button_text = "Click me!"

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Change the button text on click
            button_text = "You clicked me!"
    
    # Create the text surface with the current button text
    text_surface = FONT.render(button_text, True, (255, 255, 255))
    
    # Center the text on the button surface
    text_rect = text_surface.get_rect(center=button_surface.get_rect().center)
    
    # Blit the text surface onto the button surface
    button_surface.blit(text_surface, text_rect)
    
    # Draw the button onto the screen
    screen.blit(button_surface, button_rect)
    
    # Update the display
    pygame.display.flip()