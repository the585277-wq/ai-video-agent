import os
import urllib.request
import json
from datetime import datetime

API_KEY = os.environ.get("GEMINI_API_KEY")

prompt = """
Create a detailed YouTube Shorts AI video plan.
Choose a creative, original, trending-style topic.
Include:
1. Video title
2. 5 cinematic scenes
3. AI image prompts
4. AI video prompts
5. YouTube description
6. Hashtags

Format: 9:16
Duration: 30 seconds
No copyrighted characters.
"""

url = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-2.5-flash:generateContent?key=" + API_KEY
)

data = json.dumps({
    "contents": [{
        "parts": [{"text": prompt}]
    }]
}).encode("utf-8")

request = urllib.request.Request(
    url,
    data=data,
    headers={"Content-Type": "application/json"},
    method="POST"
)

with urllib.request.urlopen(request) as response:
    result = json.loads(response.read())

content = result["candidates"][0]["content"]["parts"][0]["text"]

with open("daily_video_plan.txt", "w", encoding="utf-8") as file:
    file.write(content)

print("Daily AI video plan generated successfully!")
