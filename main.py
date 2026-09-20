import os
import urllib.request
import json
import time

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
    "models/gemini-3.6-flash:generateContent?key=" + API_KEY
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

# Ekhane auto-retry logic add kora hoyeche
max_retries = 3
for attempt in range(max_retries):
    try:
        with urllib.request.urlopen(request) as response:
            result = json.loads(response.read())
            content = result["candidates"][0]["content"]["parts"][0]["text"]

            with open("daily_video_plan.txt", "w", encoding="utf-8") as file:
                file.write(content)

            if "Part 2" in content:
                script_part = content.split("Part 2")[1]
                with open("daily_script.txt", "w", encoding="utf-8") as script_file:
                    script_file.write("Part 2" + script_part)
            else:
                with open("daily_script.txt", "w", encoding="utf-8") as script_file:
                    script_file.write("Script not found. Check full plan file.")

            print("Daily AI video plan and script generated successfully!")
            break  # Kaj sokol hole loop theke beriye jabe
            
    except Exception as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        if hasattr(e, 'read'):
            error_msg = e.read().decode('utf-8')
            print(error_msg)
        
        if attempt < max_retries - 1:
            print("Server busy. Waiting 5 seconds and trying again...")
            time.sleep(5) # 5 second wait korbe
        else:
            print("All attempts failed. Server is too busy right now.")
