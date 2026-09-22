import os
import urllib.request
import json
import time

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("Error: GEMINI_API_KEY is missing!")
    exit(1)

USER_COMMAND = os.environ.get("USER_PROMPT", "")

default_prompt = """
You are an expert AI Video Creator and Thumbnail Designer. Your job is to create a complete video production plan for a 30-second YouTube Short / TikTok / Instagram Reel.

IMPORTANT: For Google Flow, you must create prompts that INCLUDE the voiceover/dialogue directly inside the prompt. 

Follow this exact structure:

--- SECTION 1: VIDEO IDEA ---
1. Trending Topic: (A catchy topic)
2. Video Title: (Engaging title)
3. Target Audience: (Who will watch this)

--- SECTION 2: GOOGLE FLOW PROMPTS (With Voice) ---
Provide 5 separate visual prompts that I can directly copy-paste into Google Flow. 
Each prompt MUST include:
- Visual description (Cinematic, camera angles, lighting)
- The exact VOICEOVER TEXT or DIALOGUE that should be spoken in that scene. 
- Format: "Prompt 1: [Visual Description] The character says: '[Exact voiceover text]'"
- Keep each scene 3-5 seconds long.

--- SECTION 3: THUMBNAIL DESIGN ---
Provide 1 detailed thumbnail design for this video.
Include:
- Thumbnail Text (Short, punchy, max 4-5 words, big bold font)
- Thumbnail Image Prompt (Detailed description for AI image generator like Midjourney or Leonardo AI)
- Color Scheme (Which colors will pop on screen)
- Emotion/Expression (What should the character's face look like?)

--- SECTION 4: CAPCUT EDITING GUIDE ---
Provide a step-by-step guide on how to edit this in CapCut:
- Order of clips
- Recommended transitions (e.g., Zoom in, Fade)
- Where to add text overlays
- Music suggestion (mood/genre)
- Best export settings

--- SECTION 5: SOCIAL MEDIA STRATEGY ---
- Best time to post
- Hashtags (10-15 trending hashtags)
- Caption for the post
"""

if not USER_COMMAND:
    prompt = default_prompt
else:
    prompt = f"""
    {default_prompt}
    
    ADDITIONAL USER INSTRUCTION: {USER_COMMAND}
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

            print("Full Production Plan with Thumbnail Design generated successfully!")
            break
            
    except Exception as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        if hasattr(e, 'read'):
            print(e.read().decode('utf-8'))
        
        if attempt < max_retries - 1:
            time.sleep(5)
        else:
            print("All attempts failed.")
