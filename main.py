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

# Default prompt (jodi user kono command na dey, tahole trending topic use hobe)
default_prompt = """
You are an expert AI Video Creator and Thumbnail Designer. Create a complete video production plan for a 30-second YouTube Short / TikTok / Instagram Reel.

Follow this exact structure:

--- SECTION 1: VIDEO IDEA ---
1. Trending Topic
2. Video Title
3. Target Audience

--- SECTION 2: GOOGLE FLOW PROMPTS (With Voice) ---
Provide 5 separate visual prompts for Google Flow. 
Each prompt MUST include:
- Visual description (Cinematic, camera angles, lighting)
- The exact VOICEOVER TEXT or DIALOGUE spoken in that scene. 
- Format: "Prompt 1: [Visual Description] The character says: '[Exact voiceover text]'"

--- SECTION 3: THUMBNAIL DESIGN ---
Provide 1 detailed thumbnail design.
Include:
- Thumbnail Text (Max 4-5 words)
- Thumbnail Image Prompt (Detailed for AI image generator)
- Color Scheme
- Emotion/Expression

--- SECTION 4: CAPCUT EDITING GUIDE ---
Step-by-step guide for CapCut editing.
- Order of clips, Transitions, Text overlays, Music suggestion, Export settings.

--- SECTION 5: SOCIAL MEDIA STRATEGY ---
- Best time to post
- Hashtags (10-15)
- Caption
"""

# Jodi user command dey, tahole seta prompt hishebe use hobe
if USER_COMMAND.strip() != "":
    prompt = f"""
    {default_prompt}
    
    *** MOST IMPORTANT INSTRUCTION ***
    The user has specifically requested the following topic: "{USER_COMMAND}"
    You MUST create the entire video plan, script, and thumbnail based ONLY on this specific topic. 
    Do NOT choose a random trending topic. 
    Follow the user's command exactly.
    """
else:
    prompt = default_prompt

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

            print("Video Plan generated successfully based on your command!")
            break
            
    except Exception as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        if hasattr(e, 'read'):
            print(e.read().decode('utf-8'))
        
        if attempt < max_retries - 1:
            time.sleep(5)
        else:
            print("All attempts failed.")
