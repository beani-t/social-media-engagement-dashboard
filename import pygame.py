import pygame
import sys

pygame.init()

# Window
WIDTH = 950
HEIGHT = 760
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Engagement Rate Calculator")

# Colors
BG = (245, 244, 250)
CARD = (255, 255, 255)
PURPLE = (130, 87, 229)
LIGHT_GRAY = (230, 230, 238)
GRAY = (120, 120, 140)
DARK = (30, 30, 50)
WHITE = (255, 255, 255)
BORDER = (220, 220, 230)

# Fonts
title_font = pygame.font.SysFont("arial", 46, bold=True)
subtitle_font = pygame.font.SysFont("arial", 22)
section_font = pygame.font.SysFont("arial", 20, bold=True)
text_font = pygame.font.SysFont("arial", 16)
pixel_font = pygame.font.SysFont("couriernew", 13, bold=True)

# Load logos
def load_logo(filename):
    """Load and resize logo images."""
    logo = pygame.image.load(filename)
    return pygame.transform.scale(logo, (30, 30))

logos = {
    "Instagram": load_logo("instagram.png"),
    "TikTok": load_logo("tiktok.png"),
    "Twitter": load_logo("twitter.png"),
    "Facebook": load_logo("facebook.png"),
    "LinkedIn": load_logo("linkedin.png"),
    "YouTube": load_logo("youtube.png")
}

# Platform buttons
platform_buttons = [
    ("Instagram", pygame.Rect(130, 320, 220, 48)),
    ("TikTok", pygame.Rect(380, 320, 220, 48)),
    ("Twitter", pygame.Rect(630, 320, 220, 48)),
    ("Facebook", pygame.Rect(130, 390, 220, 48)),
    ("LinkedIn", pygame.Rect(380, 390, 220, 48)),
    ("YouTube", pygame.Rect(630, 390, 220, 48))
]

selected_platform = "Instagram"

# Input boxes
input_rects = {
    "followers": pygame.Rect(130, 540, 220, 40),
    "likes": pygame.Rect(380, 540, 220, 40),
    "comments": pygame.Rect(630, 540, 220, 40),
    "shares": pygame.Rect(130, 610, 220, 40),
    "saves": pygame.Rect(380, 610, 220, 40)
}

inputs = {
    "followers": "",
    "likes": "",
    "comments": "",
    "shares": "",
    "saves": ""
}

active_input = None

# Buttons
calculate_button = pygame.Rect(300, 680, 180, 50)
reset_button = pygame.Rect(520, 680, 180, 50)

result_text = "Enter metrics to calculate engagement."

# Benchmarks
benchmarks = {
    "Instagram": 3.0,
    "TikTok": 5.0,
    "Twitter": 1.0,
    "Facebook": 1.5,
    "LinkedIn": 2.0,
    "YouTube": 4.0
}

# Tips
tips = {
    "Poor Engagement": "Tip: Try posting more consistently and use stronger hooks.",
    "Average": "Tip: Good start! Test better captions and hashtags.",
    "Good": "Tip: Nice work! Keep engaging with your audience.",
    "Excellent": "Tip: Excellent! Keep building community interaction."
}

def draw_text(text, font, color, x, y):
    """Draw text on screen."""
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def calculate_results():
    """Calculate engagement rate and performance."""
    global result_text

    try:
        followers = int(inputs["followers"])
        likes = int(inputs["likes"])
        comments = int(inputs["comments"])
        shares = int(inputs["shares"])
        saves = int(inputs["saves"])

        if followers <= 0:
            result_text = "Followers must be greater than 0."
            return

        total = likes + comments + shares + saves
        rate = (total / followers) * 100

        # Realistic thresholds
        if rate < 1:
            performance = "Poor Engagement"
        elif rate < 3:
            performance = "Average"
        elif rate < 6:
            performance = "Good"
        else:
            performance = "Excellent"

        benchmark = benchmarks[selected_platform]

        if rate >= benchmark:
            benchmark_text = "Above Benchmark"
        else:
            benchmark_text = "Below Benchmark"

        result_text = (
            f"{rate:.2f}% Engagement Rate\n"
            f"Total Engagement: {total}\n"
            f"Performance: {performance}\n"
            f"{benchmark_text}\n"
            f"{tips[performance]}"
        )

    except:
        result_text = "Please enter valid numbers."

def reset_inputs():
    """Reset all text boxes."""
    global inputs, result_text

    inputs = {
        "followers": "",
        "likes": "",
        "comments": "",
        "shares": "",
        "saves": ""
    }

    result_text = "Enter metrics to calculate engagement."

running = True

while running:

    screen.fill(BG)

    # Header
    draw_text("Engagement Rate", title_font, DARK, 260, 80)
    draw_text("Calculator", title_font, PURPLE, 360, 145)
    draw_text(
        "Measure your social media performance instantly.",
        subtitle_font,
        GRAY,
        260,
        220
    )

    # Platform card
    pygame.draw.rect(screen, CARD, (95, 280, 760, 170), border_radius=18)
    pygame.draw.rect(screen, BORDER, (95, 280, 760, 170), width=2, border_radius=18)

    draw_text("SELECT PLATFORM", section_font, GRAY, 125, 310)

    for platform, rect in platform_buttons:

        color = PURPLE if platform == selected_platform else LIGHT_GRAY

        pygame.draw.rect(screen, color, rect, border_radius=12)

        logo_key = platform
        if platform == "Twitter":
            logo_key = "Twitter"

        screen.blit(logos[logo_key], (rect.x + 12, rect.y + 9))

        text_color = WHITE if platform == selected_platform else DARK

        label = platform
        if platform == "Twitter":
            label = "X / Twitter"

        draw_text(label, text_font, text_color, rect.x + 55, rect.y + 13)

    # Metrics card
    pygame.draw.rect(screen, CARD, (95, 470, 760, 200), border_radius=18)
    pygame.draw.rect(screen, BORDER, (95, 470, 760, 200), width=2, border_radius=18)

    draw_text("POST METRICS", section_font, GRAY, 125, 500)

    labels = {
        "followers": (130, 530),
        "likes": (380, 530),
        "comments": (630, 530),
        "shares": (130, 600),
        "saves": (380, 600)
    }

    for key, rect in input_rects.items():

        draw_text(key.capitalize(), text_font, GRAY, labels[key][0], labels[key][1])

        pygame.draw.rect(screen, LIGHT_GRAY, rect, border_radius=10)
        pygame.draw.rect(screen, BORDER, rect, width=2, border_radius=10)

        draw_text(inputs[key], text_font, DARK, rect.x + 12, rect.y + 10)

    # Buttons
    pygame.draw.rect(screen, PURPLE, calculate_button, border_radius=12)
    pygame.draw.rect(screen, LIGHT_GRAY, reset_button, border_radius=12)

    draw_text("Calculate", subtitle_font, WHITE, 345, 690)
    draw_text("Reset", subtitle_font, DARK, 575, 690)

    # Results card
    pygame.draw.rect(screen, CARD, (95, 740, 760, 125), border_radius=18)
    pygame.draw.rect(screen, BORDER, (95, 740, 760, 125), width=2, border_radius=18)

    draw_text("RESULTS", section_font, GRAY, 125, 750)

    y_text = 780

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
                calculate_results()

            if reset_button.collidepoint(mouse):
                reset_inputs()

        if event.type == pygame.KEYDOWN and active_input:

            if event.key == pygame.K_BACKSPACE:
                inputs[active_input] = inputs[active_input][:-1]

            elif event.unicode.isdigit():
                inputs[active_input] += event.unicode

    pygame.display.update()

pygame.quit()
sys.exit()