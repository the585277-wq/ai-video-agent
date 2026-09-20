from datetime import datetime
import random

topics = [
    "Giant Monster Attacks Earth",
    "AI Virtual Animal Adventure",
    "Boy Finds a Magical Genie",
    "Future Robot War",
    "Supernatural Forest Mystery",
    "Giant Alien Invasion",
    "Epic AI Action Story"
]

topic = random.choice(topics)
date = datetime.now().strftime("%Y-%m-%d")

content = f"""
AI VIDEO DAILY PLAN
Date: {date}

Trending-style Topic:
{topic}

Video Type: AI Cinematic Shorts
Aspect Ratio: 9:16
Duration: 30 seconds

Status: Idea generated successfully.
"""

with open("daily_video_plan.txt", "w") as file:
    file.write(content)

print("Daily video idea generated!")
print(topic)
