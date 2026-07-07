import pygame
import os

pygame.init()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Window size
WIDTH, HEIGHT = 950, 760
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Engagement Rate Calculator")

# Fonts
title_font = pygame.font.SysFont("arial", 46, bold=True)
subtitle_font = pygame.font.SysFont("arial", 22)
section_font = pygame.font.SysFont("arial", 20, bold=True)
text_font = pygame.font.SysFont("arial", 19)
small_font = pygame.font.SysFont("arial", 16)
pixel_font = pygame.font.SysFont("couriernew", 13, bold=True)

# Colors
BACKGROUND = (246, 245, 252)
CARD = (255, 255, 255)
DARK = (24, 30, 45)
GRAY = (105, 112, 132)
LIGHT_GRAY = (238, 240, 246)
BORDER = (210, 214, 226)
PURPLE = (126, 87, 230)
WHITE = (255, 255, 255)

# Dictionary: platform benchmark engagement rates
benchmarks = {
    "Instagram": 3.0,
    "TikTok": 4.5,
    "X / Twitter": 1.0,
    "Facebook": 1.5,
    "LinkedIn": 2.0,
    "YouTube": 4.0
}

platforms = ["Instagram", "TikTok", "X / Twitter", "Facebook", "LinkedIn", "YouTube"]
selected_platform = "Instagram"

# Dictionary: user input values
inputs = {
    "Followers": "",
    "Likes": "",
    "Comments": "",
    "Shares": "",
    "Saves": ""
}

active_input = None
result_text = "Enter your metrics to see your engagement rate."


def load_logo(filename):
    """Load and resize a social media logo image."""
    image_path = os.path.join(BASE_DIR, filename)
    logo = pygame.image.load(image_path)
    return pygame.transform.scale(logo, (28, 28))


# Dictionary: platform logos
logos = {
    "Instagram": load_logo("instagram.png"),
    "TikTok": load_logo("tiktok.png"),
    "X / Twitter": load_logo("twitter.png"),
    "Facebook": load_logo("facebook.png"),
    "LinkedIn": load_logo("linkedin.png"),
    "YouTube": load_logo("youtube.png")
}


def draw_text(text, font, color, x, y):
    """Draw text on the screen."""
    image = font.render(text, True, color)
    screen.blit(image, (x, y))


def calculate_engagement_rate(followers, likes, comments, shares, saves):
    """Calculate total engagement and engagement rate."""
    total = likes + comments + shares + saves
    rate = (total / followers) * 100
    return total, rate


def classify_performance(rate, total):
    """Classify engagement using both rate and total engagement."""
    if total < 25:
        return "Poor Engagement"

    elif total < 75:
        if rate < 5:
            return "Poor Engagement"
        else:
            return "Average Engagement"

    elif total < 250:
        if rate < 3:
            return "Average Engagement"
        else:
            return "Strong Engagement"

    else:
        if rate < 1:
            return "Poor Engagement"
        elif rate < 3:
            return "Average Engagement"
        elif rate < 8:
            return "Strong Engagement"
        else:
            return "Excellent Engagement"


def get_tip(level):
    """Return a marketing tip based on performance."""
    if level == "Poor Engagement":
        return "Tip: Improve hooks, captions, and consistency."
    elif level == "Average Engagement":
        return "Tip: Ask questions and test stronger formats."
    elif level == "Strong Engagement":
        return "Tip: Strong post! Try more reels/carousels."
    else:
        return "Tip: Excellent! Repeat this content style."


def get_results():
    """Calculate engagement results and feedback."""
    try:
        followers = int(inputs["Followers"])
        likes = int(inputs["Likes"])
        comments = int(inputs["Comments"])
        shares = int(inputs["Shares"])
        saves = int(inputs["Saves"])

        if followers <= 0:
            return "Followers must be greater than 0."

        total, rate = calculate_engagement_rate(followers, likes, comments, shares, saves)
        level = classify_performance(rate, total)
        tip = get_tip(level)
        benchmark = benchmarks[selected_platform]

        if rate > benchmark:
            comparison = "Above Benchmark"
        elif rate == benchmark:
            comparison = "At Benchmark"
        else:
            comparison = "Below Benchmark"

        return (
            f"{rate:.2f}% Engagement Rate\n"
            f"Total Engagement: {total}\n"
            f"Performance: {level}\n"
            f"{comparison}\n"
            f"{tip}"
        )

    except ValueError:
        return "Please enter numbers in every box."


def reset_inputs():
    """Clear all input boxes."""
    for key in inputs:
        inputs[key] = ""


running = True

while running:
    screen.fill(BACKGROUND)

    # Header
    draw_text("Engagement Rate", title_font, DARK, 300, 25)
    draw_text("Calculator", title_font, PURPLE, 370, 78)
    draw_text("Measure your social media performance instantly.", subtitle_font, GRAY, 270, 135)

    # Platform card
    pygame.draw.rect(screen, CARD, (95, 190, 760, 175), border_radius=18)
    pygame.draw.rect(screen, BORDER, (95, 190, 760, 175), width=2, border_radius=18)
    draw_text("SELECT PLATFORM", section_font, GRAY, 125, 215)

    platform_buttons = []
    platform_positions = [
        (125, 260), (365, 260), (605, 260),
        (125, 315), (365, 315), (605, 315)
    ]

    for i, platform in enumerate(platforms):
        x, y = platform_positions[i]
        rect = pygame.Rect(x, y, 215, 42)
        platform_buttons.append((platform, rect))

        if platform == selected_platform:
            button_color = PURPLE
            text_color = WHITE
        else:
            button_color = LIGHT_GRAY
            text_color = DARK

        pygame.draw.rect(screen, button_color, rect, border_radius=10)
        screen.blit(logos[platform], (x + 12, y + 7))
        draw_text(platform, text_font, text_color, x + 52, y + 10)

    # Metrics card
    pygame.draw.rect(screen, CARD, (95, 385, 760, 145), border_radius=18)
    pygame.draw.rect(screen, BORDER, (95, 385, 760, 145), width=2, border_radius=18)
    draw_text("POST METRICS", section_font, GRAY, 125, 405)

    input_rects = {}
    labels = list(inputs.keys())
    input_positions = [
        (125, 455), (365, 455), (605, 455),
        (125, 505), (365, 505)
    ]

    for i, label in enumerate(labels):
        x, y = input_positions[i]
        draw_text(label, small_font, GRAY, x, y - 22)

        rect = pygame.Rect(x, y, 215, 32)
        input_rects[label] = rect

        box_color = WHITE if active_input == label else LIGHT_GRAY
        pygame.draw.rect(screen, box_color, rect, border_radius=8)
        pygame.draw.rect(screen, BORDER, rect, width=2, border_radius=8)

        value = inputs[label] if inputs[label] else "e.g. 1000"
        value_color = DARK if inputs[label] else (145, 150, 165)
        draw_text(value, text_font, value_color, x + 10, y + 5)

    # Action buttons
    calculate_button = pygame.Rect(280, 555, 180, 40)
    reset_button = pygame.Rect(500, 555, 180, 40)

    pygame.draw.rect(screen, PURPLE, calculate_button, border_radius=10)
    pygame.draw.rect(screen, LIGHT_GRAY, reset_button, border_radius=10)

    draw_text("Calculate", text_font, WHITE, 330, 565)
    draw_text("Reset", text_font, DARK, 565, 565)

    # Results card
    pygame.draw.rect(screen, CARD, (95, 600, 760, 135), border_radius=18)
    pygame.draw.rect(screen, BORDER, (95, 600, 760, 135), width=2, border_radius=18)
    draw_text("RESULTS", section_font, GRAY, 125, 612)

    y_text = 635
    for line in result_text.split("\n"):
        draw_text(line, pixel_font, DARK, 125, y_text)
        y_text += 15

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = event.pos

            for platform, rect in platform_buttons:
                if rect.collidepoint(mouse):
                    selected_platform = platform

            active_input = None
            for label, rect in input_rects.items():
                if rect.collidepoint(mouse):
                    active_input = label

            if calculate_button.collidepoint(mouse):
                result_text = get_results()

            if reset_button.collidepoint(mouse):
                reset_inputs()
                result_text = "Enter your metrics to see your engagement rate."

        if event.type == pygame.KEYDOWN and active_input:
            if event.key == pygame.K_BACKSPACE:
                inputs[active_input] = inputs[active_input][:-1]
            elif event.unicode.isdigit():
                inputs[active_input] += event.unicode

    pygame.display.update()

pygame.quit()