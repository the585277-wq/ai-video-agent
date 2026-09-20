import os
import urllib.request
import json
from datetime import datetime

API_KEY = os.environ.get("GEMINI_API_KEY")

prompt = """
Create a detailed YouTube Shorts AI video plan AND a full voiceover script.
Choose a creative, original, trending-style topic.

Part 1: Video Plan (Include):
1. Video title
2. 5 cinematic scenes
3. AI image prompts
4. AI video prompts
5. YouTube description
6. Hashtags

Part 2: Voiceover Script (Include):
Write a 30-second engaging voiceover script based on the video plan above. 
The script should be conversational, hook the viewer in the first 3 seconds, and have a clear call to action at the end.

Format: 9:16
Duration: 30 seconds
No copyrighted characters.
"""

url = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-1.5-flash:generateContent?key=" + API_KEY
)

data = json.dumps({
    "contents": [{
        "parts": [{"text": prompt}],
        "role": "user"
    }]
}).encode("utf-8")

request = urllib.request.Request(
    url,
    data=data,
    headers={"Content-Type": "application/json"},
    method="POST"
)

try:
    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read())
        content = result["candidates"][0]["content"]["parts"][0]["text"]

        # Save the full response (Plan + Script)
        with open("daily_video_plan.txt", "w", encoding="utf-8") as file:
            file.write(content)

        # Save only the script part for easy access
        # (Splitting the text to find the Script section)
        if "Part 2" in content:
            script_part = content.split("Part 2")[1]
            with open("daily_script.txt", "w", encoding="utf-8") as script_file:
                script_file.write("Part 2" + script_part)
        else:
            with open("daily_script.txt", "w", encoding="utf-8") as script_file:
                script_file.write("Script not found. Check full plan file.")

        print("Daily AI video plan and script generated successfully!")
        
except Exception as e:
    print(f"Error occurred: {e}")
    if hasattr(e, 'read'):
        print(e.read().decode('utf-8'))
