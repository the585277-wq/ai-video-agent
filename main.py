import os
import urllib.request
import json
import time

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("Error: GEMINI_API_KEY is missing!")
    exit(1)

# GitHub Actions theke user er command neya hocche
USER_COMMAND = os.environ.get("USER_PROMPT", "")

if not USER_COMMAND:
    # Jodi user kono command na dey, tobei default prompt use hobe
    prompt = """
    Create a detailed YouTube Shorts AI video plan AND a full voiceover script.
    Choose a creative, original, trending-style topic.
    Include 5 cinematic scenes, AI image prompts, AI video prompts, title, description, hashtags.
    Also write a 30-second voiceover script with a hook and call to action.
    """
else:
    # Jodi user command dey, tahole setai prompt hishebe use hobe
    prompt = USER_COMMAND
    print(f"User Command Received: {prompt}")

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

max_retries = 3
for attempt in range(max_retries):
    try:
        with urllib.request.urlopen(request) as response:
            result = json.loads(response.read())
            content = result["candidates"][0]["content"]["parts"][0]["text"]

            with open("daily_video_plan.txt", "w", encoding="utf-8") as file:
                file.write(content)

            with open("daily_script.txt", "w", encoding="utf-8") as script_file:
                script_file.write(content)

            print("AI Content generated successfully!")
            break
            
    except Exception as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        if hasattr(e, 'read'):
            print(e.read().decode('utf-8'))
        
        if attempt < max_retries - 1:
            time.sleep(5)
        else:
            print("All attempts failed.")
