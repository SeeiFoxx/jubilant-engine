import pygame

pygame.init()

# Set up the window
window_width = 640
window_height = 480
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Text Boxes")

# Set up the font
font = pygame.font.Font(None, 36)

# Define the text for each box
text_1 = "Hello, this is box 1."
text_2 = "Hi there, this is box 2."

# Define the positions for each box
box_1_pos = (50, 50)
box_2_pos = (50, 150)

# Define the currently selected box
current_box = 1

# Define the colors for the boxes
selected_color = (0, 0, 0)
selected_bg_color = (228, 192, 27)
unselected_color = (255, 255, 255)
unselected_bg_color = (0, 0, 0)

# Define the arrow image (https://flaticons.net/customize.php?dir=Application&icon=Navigation-Right.png)
arrow_image = pygame.image.load("arrow.png")

# Draw the initial boxes on the screen
box_1 = font.render(text_1, True, selected_color, selected_bg_color)
box_2 = font.render(text_2, True, unselected_color, unselected_bg_color)
screen.blit(box_1, box_1_pos)
screen.blit(box_2, box_2_pos)

# Draw the arrow next to the selected box
arrow_pos = (box_1_pos[0] - arrow_image.get_width(), box_1_pos[1])
screen.blit(arrow_image, arrow_pos)

pygame.display.flip()

# Game loop
running = True
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                # Switch the selected box
                if current_box == 1:
                    current_box = 2
                else:
                    current_box = 1
                # Render the boxes
                screen.fill((0, 0, 0))
                if current_box == 1:
                    box_1 = font.render(text_1, True, selected_color, selected_bg_color)
                    box_2 = font.render(text_2, True, unselected_color, unselected_bg_color)
                    arrow_pos = (box_1_pos[0] - arrow_image.get_width(), box_1_pos[1])
                else:
                    box_1 = font.render(text_1, True, unselected_color, unselected_bg_color)
                    box_2 = font.render(text_2, True, selected_color, selected_bg_color)
                    arrow_pos = (box_2_pos[0] - arrow_image.get_width(), box_2_pos[1])
                screen.blit(box_1, box_1_pos)
                screen.blit(box_2, box_2_pos)
                screen.blit(arrow_image, arrow_pos)
                pygame.display.flip()
            elif event.key == pygame.K_RETURN:
                # Select the current box
                if current_box == 1:
                    print("Box 1 selected.")
                elif current_box == 2:
                    print("Box 2 selected.")

    # Update the screen
    pygame.display.update()

# Quit pygame
pygame.quit()